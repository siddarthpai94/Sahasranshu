import json
from pathlib import Path

from sahasranshu.core.manifest import load_manifest
from sahasranshu.ingestion.pdf import pdf_to_pages

def main():
    manifest_path = "data/US/FED/2024/Dec/manifests/2024-12-18_FOMC_Statement.json"
    m = load_manifest(manifest_path)

    pdf_path = Path(m.relative_path)
    pages = pdf_to_pages(pdf_path)

    out_pages = Path("data/US/FED/2024/Dec/processed") / f"{m.doc_id}.pages.json"
    out_pages.parent.mkdir(parents=True, exist_ok=True)
    out_pages.write_text(json.dumps({"doc_id": m.doc_id, "pages": pages}, ensure_ascii=False, indent=2))

    print("Wrote:", out_pages)

if __name__ == "__main__":
    main()
