"""Convert recorded LLM parsed responses into candidate golden fixtures.

Usage:
    python scripts/convert_llm_records.py --src tests/fixtures/gemini_responses --out tests/fixtures/golden_from_llm

This script copies all *_parsed.json files into a tiled structure and writes a manifest
that you should review before committing the generated fixtures to the repository.
"""

import argparse
import json
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--src", default="tests/fixtures/gemini_responses")
    p.add_argument("--out", default="tests/fixtures/golden_from_llm")
    args = p.parse_args()

    src = Path(args.src)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    manifest = []
    for f in sorted(src.iterdir() if src.exists() else []):
        if f.name.endswith("_parsed.json"):
            payload = json.loads(f.read_text(encoding="utf-8"))
            dest = out / f.name
            dest.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            manifest.append(str(dest))

    manifest_file = out / "MANIFEST.json"
    manifest_file.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print("Wrote", len(manifest), "candidate fixtures to", out)
    print("Please review the files and decide which to commit as golden fixtures.")


if __name__ == "__main__":
    main()
