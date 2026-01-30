import argparse
import asyncio
import json
from pathlib import Path

from sahasranshu.config.settings import Settings
from sahasranshu.core.manifest import load_manifest
from sahasranshu.engines import assemble
from sahasranshu.ingestion.pdf import pdf_to_pages
from sahasranshu.llm.gemini_client import GeminiClient


def _pages_to_text(pages):
    return "\n\n".join(p["text"] for p in pages)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "manifest",
        nargs="?",
        default="data/US/FED/2024/Dec/manifests/2024-12-18_FOMC_Statement.json",
    )
    parser.add_argument(
        "--use-llm",
        action="store_true",
        help="Call live LLM (requires GEMINI_API_KEY in env / settings)",
    )
    parser.add_argument(
        "--record-llm",
        action="store_true",
        help="Record raw LLM responses to tests/fixtures/gemini_responses/",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Use mock data (offline mode)",
    )
    args = parser.parse_args()

    settings = Settings()

    manifest_path = args.manifest
    m = load_manifest(manifest_path)

    pdf_path = Path(m.relative_path)
    pages = pdf_to_pages(pdf_path)

    out_pages = Path(pdf_path.parent) / "processed" / f"{m.doc_id}.pages.json"
    out_pages.parent.mkdir(parents=True, exist_ok=True)
    out_pages.write_text(
        json.dumps({"doc_id": m.doc_id, "pages": pages}, ensure_ascii=False, indent=2)
    )

    print("Wrote:", out_pages)

    if args.use_llm or args.mock:
        # prepare text
        text = _pages_to_text(pages)

        # ---------------------------------------------------------
        # FIND PREVIOUS MANIFEST
        # ---------------------------------------------------------
        previous_text = None
        prev_date = None  # Initialize prev_date for later use
        try:
            from datetime import datetime

            current_date = datetime.strptime(m.publication_date, "%Y-%m-%d")

            # Find previous manifest to do delta analysis
            # 1. List all available manifests
            project_root = Path(
                __file__
            ).parent.parent  # Assuming script is in sahasranshu/scripts/
            # Recursive glob to satisfy user directory structure
            all_manifests = []
            for f in project_root.glob(
                "data/US/FED/2024/*/manifests/*.json"
            ):  # Assuming pattern
                # Skip the current one or anything that's not a manifest file
                if f.resolve() == Path(manifest_path).resolve():
                    continue

                try:
                    candidate = load_manifest(f)
                    c_date = datetime.strptime(candidate.publication_date, "%Y-%m-%d")
                    if c_date < current_date:
                        all_manifests.append((c_date, f))
                except Exception:
                    # ignore parse errors or non-manifests
                    pass

            # Sort by date descending (closest to current is first)
            all_manifests.sort(key=lambda x: x[0], reverse=True)

            if all_manifests:
                prev_date, prev_path = all_manifests[0]
                print(f"Found previous manifest: {prev_path} ({prev_date.date()})")

                # Load previous text
                # We need to load the PDF->pages if processed, or just grab the file path from manifest
                # For simplicity, assuming the 'processed' sibling exists as in the standard pipeline
                # or we just re-process/re-read the text.
                # Let's rely on the manifest -> text logic.
                pm = load_manifest(prev_path)
                prev_pdf_path = Path(pm.relative_path)
                # Quick check if processed json exists
                prev_processed_path = (
                    Path(prev_path).parent.parent
                    / "processed"
                    / f"{pm.doc_id}.pages.json"
                )

                if prev_processed_path.exists():
                    pt_obj = json.loads(prev_processed_path.read_text())
                    previous_text = _pages_to_text(pt_obj["pages"])
                else:
                    # Fallback: process it now (fast enough for one file)
                    print(f"Processing previous file on the fly: {prev_pdf_path}")
                    if prev_pdf_path.exists():
                        p_pages = pdf_to_pages(prev_pdf_path)
                        previous_text = _pages_to_text(p_pages)
                    else:
                        print(f"Warning: Previous PDF not found at {prev_pdf_path}")

            else:
                print("No previous manifest found.")

        except Exception as e:
            print(f"Error finding previous manifest: {e}")
        # ---------------------------------------------------------

        analysis = None
        project_root = Path(__file__).parent  # run_one.py is in project root
        processed_dir = Path(pdf_path.parent) / "processed"

        if args.mock:
            print("--- MOCK MODE: Skipping LLM, using canned analysis ---")
            mock_file = project_root / "web_view" / "mock_analysis.json"
            if mock_file.exists():
                with open(mock_file, "r") as f:
                    analysis = json.load(f)
            else:
                # Fallback implementation if file missing
                analysis = {
                    "stances": [{"topic": "Mock Topic", "evidence": "Mock Evidence"}],
                    "deltas": [],
                    "hypotheses": [],
                }

        else:  # Real LLM Call
            api_key = settings.gemini_api_key
            if not api_key:
                raise RuntimeError(
                    "GEMINI API key not configured in settings (set GEMINI_API_KEY in env or .env)"
                )

            record_path = None
            if args.record_llm or settings.llm_record_responses:
                record_path = str(settings.llm_records_dir)

            client = GeminiClient(
                api_key=api_key,
                model=settings.gemini_model,
                retries=10,  # Aggressive retries for free tier
                backoff_factor=2.0,
                record_responses=bool(record_path),
                record_path=record_path,
            )

            print("Running analysis with live LLM (this will incur API usage)...")
            analysis = asyncio.get_event_loop().run_until_complete(
                assemble.run_pipeline(
                    text=text, llm_client=client, previous_text=previous_text
                )
            )

        # Post-Processing (Common for both mock and real LLM)
        # Inject Meta
        if analysis is not None:  # Ensure analysis was loaded/generated
            if "meta" not in analysis:
                analysis["meta"] = {}
            analysis["meta"]["current_date"] = m.publication_date
            analysis["meta"]["previous_date"] = (
                prev_date.strftime("%Y-%m-%d") if prev_date else "N/A"
            )

            # Save output
            out_analysis = processed_dir / f"{m.doc_id}.analysis.json"
            out_analysis.write_text(json.dumps(analysis, ensure_ascii=False, indent=2))
            print("Wrote analysis:", out_analysis)

            # Also render memo
            from sahasranshu.reporting.memo_renderer import render_memo

            memo_text = render_memo(analysis)

            # Embed memo in analysis for easier frontend loading (CORS safe)
            analysis["memo_content"] = memo_text

            out_memo = processed_dir / f"{m.doc_id}.memo.md"
            out_memo.write_text(memo_text)
            print("Wrote memo:", out_memo)

            # Re-save analysis with the embedded memo
            out_analysis.write_text(json.dumps(analysis, ensure_ascii=False, indent=2))

            # Update Web View
            try:
                web_view_json = project_root / "web_view" / "analysis.json"
                web_view_json.write_text(
                    json.dumps(analysis, ensure_ascii=False, indent=2)
                )

                web_view_memo = project_root / "web_view" / "memo.md"
                web_view_memo.write_text(memo_text)
                print(
                    f"Updated Dashboard Data:\n  - {web_view_json}\n  - {web_view_memo}"
                )
            except Exception as e:
                print(f"Could not update dashboard: {e}")


if __name__ == "__main__":
    main()
