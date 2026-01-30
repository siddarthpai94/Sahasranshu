import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Manifest:
    doc_id: str
    title: str
    publication_date: str
    source_page: str
    relative_path: str


def load_manifest(path: str | Path) -> Manifest:
    p = Path(path)
    obj = json.loads(p.read_text())
    return Manifest(
        doc_id=obj["doc_id"],
        title=obj["title"],
        publication_date=obj["publication_date"],
        source_page=obj["source"]["source_page"],
        relative_path=obj["file"]["relative_path"],
    )
