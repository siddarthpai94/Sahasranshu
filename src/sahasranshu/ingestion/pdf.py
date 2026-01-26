"""PDF ingestion and processing."""

from pathlib import Path
from typing import List, Dict, Any
from PyPDF2 import PdfReader


def extract_pages_from_pdf(pdf_path: Path) -> List[Dict[str, Any]]:
    """Extract pages from PDF with page IDs."""
    pages = []
    reader = PdfReader(pdf_path)

    for page_num, page in enumerate(reader.pages, 1):
        text = page.extract_text()
        pages.append(
            {
                "page_id": f"{pdf_path.stem}_page_{page_num:03d}",
                "page_number": page_num,
                "content": text,
                "source": str(pdf_path),
            }
        )

    return pages
