#!/usr/bin/env python3

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "knowledge" / "registry.json"


def load_registry():
    return json.loads(
        REGISTRY.read_text(encoding="utf-8")
    )


def get_kb(kb_id: str):
    for kb in load_registry().get("knowledge_bases", []):
        if kb.get("id") == kb_id:
            return kb

    raise SystemExit(
        f"Knowledge base not found: {kb_id}"
    )


def list_kbs():
    for kb in load_registry().get("knowledge_bases", []):
        status = "enabled" if kb.get("enabled") else "disabled"

        print(
            f"{kb.get('id'):15} "
            f"{status:8} "
            f"{kb.get('type', 'unknown'):16} "
            f"{kb.get('name', '')}"
        )


def show_kb(kb_id: str):
    kb = get_kb(kb_id)
    print(json.dumps(kb, indent=2))


def resolve_agent_path(value: str) -> Path:
    path = Path(value)

    if path.is_absolute():
        return path

    if value.startswith(".agent/"):
        return ROOT.parent / value

    return ROOT / value


def verify_kb(kb_id: str):
    kb = get_kb(kb_id)
    failures = []

    print(f"KB: {kb_id}")
    print(f"TYPE: {kb.get('type', 'unknown')}")
    print(f"ENABLED: {kb.get('enabled', False)}")

    source_value = kb.get("source_path")
    chunk_value = kb.get("chunk_path")

    if source_value:
        source_path = resolve_agent_path(source_value)
        print(f"SOURCE PATH: {source_path}")
        print(f"SOURCE EXISTS: {source_path.exists()}")

        if not source_path.exists():
            failures.append("source path missing")

        if source_path.exists():
            extensions = {
                ext.lower()
                for ext in kb.get(
                    "source_extensions",
                    [".md", ".txt"],
                )
            }

            source_files = [
                path
                for path in source_path.rglob("*")
                if path.is_file()
            ]

            source_count = sum(
                1
                for path in source_files
                if path.suffix.lower() in extensions
            )

            print(f"SOURCE FILES TOTAL: {len(source_files)}")
            print(f"SOURCE DOCUMENTS: {source_count}")

    if chunk_value:
        chunk_path = resolve_agent_path(chunk_value)
        print(f"CHUNK PATH: {chunk_path}")
        print(f"CHUNK PATH EXISTS: {chunk_path.exists()}")

        if not chunk_path.exists():
            failures.append("chunk path missing")

        if chunk_path.exists():
            chunk_count = len(list(chunk_path.glob("*.json")))
            print(f"CHUNKS: {chunk_count}")

    metadata_path = ROOT / "knowledge" / kb_id / "metadata" / "source-manifest.json"

    if metadata_path.exists():
        print(f"PROVENANCE: {metadata_path}")

        try:
            manifest = json.loads(
                metadata_path.read_text(encoding="utf-8")
            )
            print("PROVENANCE JSON: OK")

            if "source_file_count" in manifest:
                print(
                    "PROVENANCE SOURCE FILES:",
                    manifest["source_file_count"],
                )

                if source_value and source_path.exists():
                    if len(source_files) != manifest["source_file_count"]:
                        failures.append(
                            "source file count differs from provenance"
                        )

            if "file_count" in manifest:
                print(
                    "PROVENANCE FILES:",
                    manifest["file_count"],
                )

            if "chunk_count" in manifest:
                print(
                    "PROVENANCE CHUNKS:",
                    manifest["chunk_count"],
                )

                if chunk_value and chunk_path.exists():
                    if chunk_count != manifest["chunk_count"]:
                        failures.append(
                            "chunk count differs from provenance"
                        )

        except json.JSONDecodeError:
            print("PROVENANCE JSON: INVALID")
            failures.append("invalid provenance JSON")
    else:
        print("PROVENANCE: none")

    if failures:
        print("VERIFY: FAIL")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print("VERIFY: PASS")
    return 0


def verify_all():
    failures = 0

    for kb in load_registry().get("knowledge_bases", []):
        kb_id = kb.get("id")

        print("=" * 72)
        result = verify_kb(kb_id)

        if result != 0:
            failures += 1

    print("=" * 72)

    if failures:
        print(f"VERIFY ALL: FAIL ({failures} knowledge base(s) failed)")
        return 1

    print("VERIFY ALL: PASS")
    return 0


def usage():
    print(
        "usage:\n"
        "  kb_manage.py list\n"
        "  kb_manage.py show <kb-id>\n"
        "  kb_manage.py verify <kb-id>\n"
        "  kb_manage.py verify all",
        file=sys.stderr,
    )


def main():
    if len(sys.argv) < 2:
        usage()
        return 2

    command = sys.argv[1]

    if command == "list":
        list_kbs()
        return 0

    if command == "show":
        if len(sys.argv) != 3:
            usage()
            return 2

        show_kb(sys.argv[2])
        return 0

    if command == "verify":
        if len(sys.argv) != 3:
            usage()
            return 2

        if sys.argv[2] == "all":
            return verify_all()

        return verify_kb(sys.argv[2])

    usage()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
