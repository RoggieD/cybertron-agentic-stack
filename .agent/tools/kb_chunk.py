#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]

MIN_CHARS = 250
TARGET_CHARS = 900
MAX_CHARS = 1800


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "section"


def split_markdown_sections(text: str):
    sections = []
    heading = "Document"
    buffer = []

    def flush():
        nonlocal buffer
        body = "\n".join(buffer).strip()
        if body:
            sections.append((heading, body))
        buffer = []

    for line in text.splitlines():
        if re.match(r"^#{1,6}\s+", line):
            flush()
            heading = re.sub(r"^#{1,6}\s+", "", line).strip()
        else:
            buffer.append(line)

    flush()
    return sections


def split_large_text(text: str, max_chars: int = MAX_CHARS):
    if len(text) <= max_chars:
        return [text]

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks = []
    current = ""

    for paragraph in paragraphs:
        candidate = paragraph if not current else current + "\n\n" + paragraph

        if len(candidate) <= max_chars:
            current = candidate
            continue

        if current:
            chunks.append(current)
            current = ""

        if len(paragraph) <= max_chars:
            current = paragraph
        else:
            for i in range(0, len(paragraph), max_chars):
                piece = paragraph[i:i + max_chars].strip()
                if piece:
                    chunks.append(piece)

    if current:
        chunks.append(current)

    return chunks


def normalize_sections(sections):
    combined = []
    pending_heading = None
    pending_body = ""

    for heading, body in sections:
        block = body.strip()

        if not pending_body:
            pending_heading = heading
            pending_body = block
        else:
            candidate = pending_body + "\n\n" + block

            if len(pending_body) < MIN_CHARS and len(candidate) <= TARGET_CHARS:
                pending_heading = f"{pending_heading} / {heading}"
                pending_body = candidate
            else:
                combined.append((pending_heading, pending_body))
                pending_heading = heading
                pending_body = block

    if pending_body:
        combined.append((pending_heading, pending_body))

    final = []

    for heading, body in combined:
        parts = split_large_text(body)

        if len(parts) == 1:
            final.append((heading, parts[0]))
        else:
            for i, part in enumerate(parts, start=1):
                final.append((f"{heading} — Part {i}", part))

    return final


def chunk_document(path: Path, source_root: Path, output_root: Path):
    rel = path.relative_to(source_root)
    text = path.read_text(encoding="utf-8", errors="replace")

    sections = split_markdown_sections(text)
    sections = normalize_sections(sections)

    records = []

    for index, (heading, body) in enumerate(sections, start=1):
        content = f"# {heading}\n\n{body}".strip()

        digest = hashlib.sha256(
            (str(rel) + "\n" + heading + "\n" + content).encode("utf-8")
        ).hexdigest()

        chunk_id = f"{slugify(path.stem)}-{index:03d}-{digest[:12]}"

        record = {
            "chunk_id": chunk_id,
            "kb": "juniper",
            "source_path": str(rel),
            "source_title": path.stem,
            "section": heading,
            "sha256": digest,
            "content": content,
        }

        outfile = output_root / f"{chunk_id}.json"
        outfile.write_text(
            json.dumps(record, indent=2) + "\n",
            encoding="utf-8",
        )

        records.append(record)

    return records


def main():
    source_root = ROOT / "knowledge" / "juniper" / "source" / "juniper-srx320"
    output_root = ROOT / "knowledge" / "juniper" / "chunks"

    output_root.mkdir(parents=True, exist_ok=True)

    for existing in output_root.glob("*.json"):
        existing.unlink()

    records = []

    for path in sorted(source_root.rglob("*")):
        if not path.is_file():
            continue

        if path.suffix.lower() not in {".md", ".txt"}:
            continue

        records.extend(
            chunk_document(path, source_root, output_root)
        )

    print("SOURCE DOCUMENTS:", len({
        record["source_path"] for record in records
    }))
    print("CHUNKS:", len(records))
    print("OUTPUT:", output_root)


if __name__ == "__main__":
    raise SystemExit(main())
