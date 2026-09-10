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


STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by",
    "for", "from", "i", "in", "is", "it", "my", "of",
    "on", "or", "the", "to", "with"
}


NORMALIZE = {
    "troubleshoot": "troubleshoot",
    "troubleshoots": "troubleshoot",
    "troubleshooting": "troubleshoot",
    "troubleshot": "troubleshoot",

    "configure": "config",
    "configuration": "config",
    "configurations": "config",
    "configured": "config",
    "configuring": "config",

    "route": "routing",
    "routes": "routing",
    "router": "routing",

    "policies": "policy",

    "interfaces": "interface",

    "firewalls": "firewall",
}


def normalize_word(word: str) -> str:
    return NORMALIZE.get(word, word)


def meaningful_words(text: str) -> set[str]:
    return {
        normalize_word(word)
        for word in words(text)
        if word not in STOPWORDS and len(word) > 1
    }


def score_fields(query_words, query_text="", source_path="", section="", content=""):
    if not query_words:
        return 0

    path_words = meaningful_words(source_path)
    section_words = meaningful_words(section)
    content_words = meaningful_words(content)

    score = 0

    for word in query_words:
        if word in section_words:
            score += 5

        if word in path_words:
            score += 3

        if word in content_words:
            score += 1

    query_lower = query_text.lower().strip()
    section_lower = section.lower().strip()
    content_lower = content.lower()

    phrases = [
        "destination nat",
        "source nat",
        "static nat",
        "security policy",
        "site-to-site",
        "screenos to junos",
    ]

    for phrase in phrases:
        if phrase not in query_lower:
            continue

        # Strong boost when the section is actually ABOUT the queried topic.
        if section_lower == phrase or section_lower.startswith(phrase):
            score += 10

        # Smaller boost when the phrase is merely one topic in the heading.
        elif phrase in section_lower:
            score += 3

        # Content mention is supporting evidence only.
        elif phrase in content_lower:
            score += 1

    # Intent weighting: troubleshooting-oriented questions should prefer
    # troubleshooting sections over generic reference/comparison sections.
    if "troubleshoot" in meaningful_words(query_text):
        if "troubleshoot" in meaningful_words(section):
            score += 10

    return score


def retrieve_local_directory(kb, query_words, query):
    base = ROOT.parent / kb["path"]
    results = []

    if not base.exists():
        return results

    for path in sorted(base.rglob("*")):
        if not path.is_file():
            continue

        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue

        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        score = score_fields(
            query_words,
            query_text=query,
            source_path=str(path),
            content=text,
        )

        if score <= 0:
            continue

        results.append({
            "kb": kb["id"],
            "name": kb["name"],
            "path": str(path.relative_to(ROOT.parent)),
            "score": score,
            "content": text[:4000],
        })

    return results


def retrieve_chunk_directory(kb, query_words, query):
    base = ROOT.parent / kb["path"]
    results = []

    if not base.exists():
        return results

    for path in sorted(base.glob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue

        content = record.get("content", "")
        source_path = record.get("source_path", "")
        section = record.get("section", "")

        score = score_fields(
            query_words,
            query_text=query,
            source_path=source_path,
            section=section,
            content=content,
        )

        if score <= 0:
            continue

        results.append({
            "kb": kb["id"],
            "name": kb["name"],
            "path": source_path,
            "section": section,
            "chunk_id": record.get("chunk_id"),
            "score": score,
            "content": content,
        })

    return results


def retrieve(query: str, max_results: int = 5):
    query_words = meaningful_words(query)
    results = []

    for kb in matching_kbs(query):
        kb_type = kb.get("type", "local_directory")

        if kb_type == "chunk_directory":
            results.extend(
                retrieve_chunk_directory(kb, query_words, query)
            )
        else:
            results.extend(
                retrieve_local_directory(kb, query_words, query)
            )

    results.sort(
        key=lambda r: (
            -r["score"],
            r.get("path", ""),
            r.get("section", ""),
        )
    )

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
