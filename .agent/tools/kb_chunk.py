#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "knowledge" / "registry.json"

MIN_CHARS = 250
TARGET_CHARS = 900
MAX_CHARS = 1800


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "section"


def load_registry():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def get_kb(kb_id: str):
    for kb in load_registry().get("knowledge_bases", []):
        if kb.get("id") == kb_id:
            return kb

    raise SystemExit(f"Knowledge base not found in registry: {kb_id}")


def resolve_agent_path(value: str) -> Path:
    path = Path(value)

    if path.is_absolute():
        return path

    if value.startswith(".agent/"):
        return ROOT.parent / value

    return ROOT / value


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

    paragraphs = [
        p.strip()
        for p in re.split(r"\n\s*\n", text)
        if p.strip()
    ]

    chunks = []
    current = ""

    for paragraph in paragraphs:
        candidate = (
            paragraph
            if not current
            else current + "\n\n" + paragraph
        )

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

            if (
                len(pending_body) < MIN_CHARS
                and len(candidate) <= TARGET_CHARS
            ):
                pending_heading = (
                    f"{pending_heading} / {heading}"
                )
                pending_body = candidate
            else:
                combined.append(
                    (pending_heading, pending_body)
                )
                pending_heading = heading
                pending_body = block

    if pending_body:
        combined.append(
            (pending_heading, pending_body)
        )

    final = []

    for heading, body in combined:
        parts = split_large_text(body)

        if len(parts) == 1:
            final.append((heading, parts[0]))
        else:
            for i, part in enumerate(parts, start=1):
                final.append(
                    (f"{heading} — Part {i}", part)
                )

    return final


def chunk_document(
    kb_id: str,
    path: Path,
    source_root: Path,
    output_root: Path,
):
    rel = path.relative_to(source_root)
    text = path.read_text(
        encoding="utf-8",
        errors="replace",
    )

    sections = split_markdown_sections(text)
    sections = normalize_sections(sections)

    records = []

    for index, (heading, body) in enumerate(
        sections,
        start=1,
    ):
        content = f"# {heading}\n\n{body}".strip()

        digest = hashlib.sha256(
            (
                str(rel)
                + "\n"
                + heading
                + "\n"
                + content
            ).encode("utf-8")
        ).hexdigest()

        chunk_id = (
            f"{slugify(path.stem)}-"
            f"{index:03d}-"
            f"{digest[:12]}"
        )

        record = {
            "chunk_id": chunk_id,
            "kb": kb_id,
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
    if len(sys.argv) != 2:
        print(
            "usage: kb_chunk.py <kb-id>",
            file=sys.stderr,
        )
        return 2

    kb_id = sys.argv[1]
    kb = get_kb(kb_id)

    source_value = kb.get("source_path")
    chunk_value = kb.get("chunk_path")

    if not source_value:
        raise SystemExit(
            f"{kb_id}: source_path missing from registry"
        )

    if not chunk_value:
        raise SystemExit(
            f"{kb_id}: chunk_path missing from registry"
        )

    source_root = resolve_agent_path(source_value)
    output_root = resolve_agent_path(chunk_value)

    extensions = {
        ext.lower()
        for ext in kb.get(
            "source_extensions",
            [".md", ".txt"],
        )
    }

    if not source_root.exists():
        raise SystemExit(
            f"{kb_id}: source path does not exist: "
            f"{source_root}"
        )

    output_root.mkdir(
        parents=True,
        exist_ok=True,
    )

    for existing in output_root.glob("*.json"):
        existing.unlink()

    records = []

    for path in sorted(source_root.rglob("*")):
        if not path.is_file():
            continue

        if path.suffix.lower() not in extensions:
            continue

        records.extend(
            chunk_document(
                kb_id,
                path,
                source_root,
                output_root,
            )
        )

    print("KB:", kb_id)
    print(
        "SOURCE DOCUMENTS:",
        len({
            record["source_path"]
            for record in records
        }),
    )
    print("CHUNKS:", len(records))
    print("OUTPUT:", output_root)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
