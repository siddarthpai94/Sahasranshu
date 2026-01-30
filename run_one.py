import argparse
import asyncio
import json
from pathlib import Path

from sahasranshu.core.manifest import load_manifest
from sahasranshu.ingestion.pdf import pdf_to_pages
from sahasranshu.config.settings import Settings
from sahasranshu.engines import assemble
from sahasranshu.llm.gemini_client import GeminiClient


def _pages_to_text(pages):
    return "\n\n".join(p["text"] for p in pages)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", default="data/US/FED/2024/Dec/manifests/2024-12-18_FOMC_Statement.json")
    parser.add_argument("--use-llm", action="store_true", help="Call live LLM (requires GEMINI_API_KEY in env / settings)")
    parser.add_argument("--record-llm", action="store_true", help="Record raw LLM responses to tests/fixtures/gemini_responses/")
    args = parser.parse_args()

    settings = Settings()

    manifest_path = args.manifest
    m = load_manifest(manifest_path)

    pdf_path = Path(m.relative_path)
    pages = pdf_to_pages(pdf_path)

    out_pages = Path(pdf_path.parent) / "processed" / f"{m.doc_id}.pages.json"
    out_pages.parent.mkdir(parents=True, exist_ok=True)
    out_pages.write_text(json.dumps({"doc_id": m.doc_id, "pages": pages}, ensure_ascii=False, indent=2))

    print("Wrote:", out_pages)

    if args.use_llm:
        # prepare text
        text = _pages_to_text(pages)

        api_key = settings.gemini_api_key
        if not api_key:
            raise RuntimeError("GEMINI API key not configured in settings (set GEMINI_API_KEY in env or .env)")

        record_path = None
        if args.record_llm or settings.llm_record_responses:
            record_path = str(settings.llm_records_dir)

        client = GeminiClient(api_key=api_key, model=settings.gemini_model, record_responses=bool(record_path), record_path=record_path)

        print("Running analysis with live LLM (this will incur API usage)...")
        analysis = asyncio.get_event_loop().run_until_complete(
            assemble.run_pipeline(text=text, llm_client=client)
        )

        out_analysis = Path(pdf_path.parent) / "processed" / f"{m.doc_id}.analysis.json"
        out_analysis.write_text(json.dumps(analysis, ensure_ascii=False, indent=2))
        print("Wrote analysis:", out_analysis)


if __name__ == "__main__":
    main()
