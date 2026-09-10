#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "knowledge" / "registry.json"

TEXT_SUFFIXES = {".md", ".txt", ".rst", ".json", ".yaml", ".yml"}


def words(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z0-9_.:-]+", text.lower()))


def load_registry():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def matching_kbs(query: str):
    q = query.lower()
    matches = []

    for kb in load_registry().get("knowledge_bases", []):
        if not kb.get("enabled", False):
            continue

        triggers = [str(t).lower() for t in kb.get("triggers", [])]
        if any(trigger in q for trigger in triggers):
            matches.append(kb)

    return matches


def iter_files(kb):
    base = ROOT.parent / kb["path"]

    if not base.exists():
        return

    for path in sorted(base.rglob("*")):
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def score_text(query_words, text):
    if not query_words:
        return 0
    body_words = words(text)
    return len(query_words & body_words)


def retrieve(query: str, max_results: int = 5):
    query_words = words(query)
    results = []

    for kb in matching_kbs(query):
        for path in iter_files(kb):
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue

            score = score_text(query_words, text)
            if score <= 0:
                continue

            results.append({
                "kb": kb["id"],
                "name": kb["name"],
                "path": str(path.relative_to(ROOT.parent)),
                "score": score,
                "content": text[:4000],
            })

    results.sort(key=lambda r: (-r["score"], r["path"]))
    return results[:max_results]


def main():
    if len(sys.argv) < 2:
        print("usage: kb_retrieve.py '<query>'", file=sys.stderr)
        return 2

    query = " ".join(sys.argv[1:])
    print(json.dumps(retrieve(query), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
