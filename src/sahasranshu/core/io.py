"""I/O utilities for atomic writes and JSONL handling."""

import json
from pathlib import Path
from typing import Any, List, Dict


def write_jsonl(data: List[Dict[str, Any]], path: Path) -> None:
    """Write data as JSONL (atomic)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(".tmp")

    with open(temp_path, "w") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")

    temp_path.rename(path)


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    """Read JSONL file."""
    data = []
    with open(path, "r") as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data


def write_json(data: Any, path: Path) -> None:
    """Write data as JSON (atomic)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(".tmp")

    with open(temp_path, "w") as f:
        json.dump(data, f, indent=2)

    temp_path.rename(path)
