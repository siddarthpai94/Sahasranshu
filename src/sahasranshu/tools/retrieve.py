"""Retrieve previous release by manifest."""

from typing import Optional, Dict, Any
from pathlib import Path


def retrieve_previous_release(manifest_dir: Path, doc_id: str) -> Optional[Dict[str, Any]]:
    """Fetch previous release by manifest."""
    manifest_file = manifest_dir / f"{doc_id}_manifest.json"
    if manifest_file.exists():
        import json

        with open(manifest_file) as f:
            return json.load(f)
    return None
