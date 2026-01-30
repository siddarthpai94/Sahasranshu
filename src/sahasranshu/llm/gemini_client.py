"""Gemini API client."""

from pathlib import Path
from typing import Any


class GeminiClient:
    """Client for Gemini API with timeout, retry, recording and audit telemetry."""

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-2.0-flash",
        *,
        timeout: float = 30.0,
        retries: int = 2,
        backoff_factor: float = 1.0,
        record_responses: bool = False,
        record_path: str | None = None,
        audit_enabled: bool | None = None,
        audit_path: str | None = None,
    ):
        """Initialize Gemini client.

        Args:
            api_key: Gemini API key
            model: Model name
            timeout: per-request timeout in seconds
            retries: number of retries on failure
            backoff_factor: base backoff multiplier
            record_responses: If True, save raw responses and parsed JSON to disk
            record_path: Directory to store recordings
            audit_enabled: If None, will respect Settings().llm_audit_enabled
            audit_path: Optional path to store audit JSONL
        """
        self.api_key = api_key
        self.model = model
        self.timeout = float(timeout)
        self.retries = int(retries)
        self.backoff_factor = float(backoff_factor)
        self.record_responses = record_responses
        self.record_path = Path(record_path) if record_path else None

        # Load defaults from settings when not explicitly provided
        from sahasranshu.config.settings import Settings

        settings = Settings()
        self.audit_enabled = (
            settings.llm_audit_enabled if audit_enabled is None else bool(audit_enabled)
        )
        self.audit_path = Path(audit_path) if audit_path else settings.llm_audit_path

        if self.record_responses and self.record_path:
            self.record_path.mkdir(parents=True, exist_ok=True)
        if self.audit_enabled and self.audit_path:
            self.audit_path.parent.mkdir(parents=True, exist_ok=True)

    def generate(self, prompt: str) -> str:
        """Generate response from Gemini with a per-call timeout."""
        # Import lazily so tests don't require the google.generativeai package
        try:
            import google.generativeai as genai
        except Exception as e:
            raise RuntimeError(
                "google.generativeai library is required to call the live Gemini API"
            ) from e

        genai.configure(api_key=self.api_key if hasattr(self, "api_key") else None)
        model = genai.GenerativeModel(self.model)

        # Execute the blocking call in a thread so we can enforce a timeout
        import concurrent.futures
        from concurrent.futures import ThreadPoolExecutor

        with ThreadPoolExecutor(max_workers=1) as ex:
            future = ex.submit(model.generate_content, prompt)
            try:
                response = future.result(timeout=self.timeout)
            except concurrent.futures.TimeoutError as e:
                # Cancel future and raise a timeout
                future.cancel()
                raise TimeoutError("Gemini generate() timed out") from e

        return response.text

    def extract_json(self, prompt: str) -> Any:
        """Generate JSON response from Gemini with retries and audit logging."""
        import json
        import logging
        import time
        from datetime import datetime

        from .json_guard import parse_json_response

        logger = logging.getLogger(__name__)

        attempt = 0
        last_exc = None
        while True:
            attempt += 1
            t0 = time.time()
            try:
                response = self.generate(prompt)
                parsed = parse_json_response(response)
                elapsed_ms = int((time.time() - t0) * 1000)

                # Recording
                if self.record_responses and self.record_path:
                    ts = int(time.time() * 1000)
                    slug = "".join(
                        ch if ch.isalnum() else "_" for ch in prompt[:40]
                    ).strip("_")
                    raw_file = self.record_path / f"{ts}_{slug}_raw.txt"
                    parsed_file = self.record_path / f"{ts}_{slug}_parsed.json"
                    try:
                        raw_file.write_text(response, encoding="utf-8")
                        parsed_file.write_text(
                            json.dumps(parsed, ensure_ascii=False, indent=2),
                            encoding="utf-8",
                        )
                    except Exception:
                        logger.exception(
                            "Failed to write recorded LLM response; continuing"
                        )

                # Audit entry
                if self.audit_enabled and self.audit_path:
                    self._write_audit(
                        {
                            "ts": datetime.utcnow().isoformat() + "Z",
                            "model": self.model,
                            "prompt_snippet": prompt[:120],
                            "attempt": attempt,
                            "elapsed_ms": elapsed_ms,
                            "success": True,
                            "parsed_type": type(parsed).__name__,
                        }
                    )

                return parsed

            except (
                Exception
            ) as exc:  # noqa: BLE001 - intentionally broad to capture timeouts and parse errors
                elapsed_ms = int((time.time() - t0) * 1000)
                last_exc = exc

                if self.audit_enabled and self.audit_path:
                    try:
                        self._write_audit(
                            {
                                "ts": datetime.utcnow().isoformat() + "Z",
                                "model": self.model,
                                "prompt_snippet": prompt[:120],
                                "attempt": attempt,
                                "elapsed_ms": elapsed_ms,
                                "success": False,
                                "error": str(exc),
                            }
                        )
                    except Exception:
                        logger.exception("Failed to write audit entry")

                if attempt > self.retries:
                    # Exhausted retries
                    raise

                # Backoff before next attempt
                sleep_time = self.backoff_factor * (2 ** (attempt - 1))
                time.sleep(sleep_time)

        # Should not reach here (satisfy type checker)
        raise last_exc

    def _write_audit(self, entry: dict) -> None:
        """Append a JSON-line entry to the audit file."""
        import json

        try:
            with open(self.audit_path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception:
            # Swallow to avoid breaking pipeline
            import logging

            logging.getLogger(__name__).exception("Unable to write LLM audit entry")
