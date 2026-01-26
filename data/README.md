# Data Directory

## Structure

- `samples/` - Small sample documents or synthetic text for testing and examples
- `manifests/` - Document metadata including dates, source URLs, content hashes, and provenance information

## Important Rules

**No raw PDFs are committed to this repository.** Only:
- Sample excerpts for documentation and examples
- Manifest metadata files
- Synthetic test data

## Manifest Format

Manifest files should contain:
- Document ID
- Source URL
- Acquisition date
- Content hash (SHA256)
- Document version/release
- Original filename
- Metadata (dates, authors, etc.)

Example:
```json
{
  "doc_id": "fed_policy_2025_01",
  "source_url": "https://example.com/policy.pdf",
  "acquired_date": "2025-01-26",
  "content_hash": "sha256:abc123...",
  "version": "1.0",
  "original_filename": "policy_2025.pdf"
}
```
