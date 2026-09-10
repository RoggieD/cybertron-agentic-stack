#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, timezone
import json
import shutil
import subprocess
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

            exclude_paths = kb.get("exclude_paths", [])

            def is_excluded(path):
                rel = path.relative_to(source_path).as_posix()

                for excluded in exclude_paths:
                    excluded = str(excluded).strip()

                    if not excluded:
                        continue

                    if excluded.endswith("/"):
                        if rel.startswith(excluded):
                            return True
                    elif rel == excluded:
                        return True

                return False

            source_count = sum(
                1
                for path in source_files
                if path.suffix.lower() in extensions
                and not is_excluded(path)
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


def backup_chunks(kb_id: str):
    kb = get_kb(kb_id)

    chunk_value = kb.get("chunk_path")

    if not chunk_value:
        print(f"BACKUP: SKIP ({kb_id} has no chunk_path)")
        return None

    chunk_path = resolve_agent_path(chunk_value)

    if not chunk_path.exists():
        print(f"BACKUP: SKIP (chunk path does not exist)")
        return None

    timestamp = datetime.now(timezone.utc).strftime(
        "%Y%m%d-%H%M%S"
    )

    backup_root = ROOT / "knowledge" / kb_id / "backups"
    backup_root.mkdir(parents=True, exist_ok=True)

    backup_path = backup_root / f"chunks-{timestamp}"

    shutil.copytree(
        chunk_path,
        backup_path,
    )

    print(f"BACKUP: {backup_path}")

    return backup_path


def source_check_kb(kb_id: str):
    kb = get_kb(kb_id)
    refresh = kb.get("source_refresh")

    if not refresh:
        print(f"SOURCE CHECK: SKIP ({kb_id} has no source_refresh metadata)")
        return 0

    refresh_type = refresh.get("type")

    if refresh_type != "git":
        print(
            f"SOURCE CHECK: SKIP "
            f"(unsupported source type: {refresh_type})"
        )
        return 0

    repository = refresh.get("repository")
    branch = refresh.get("branch", "main")

    if not repository:
        print("SOURCE CHECK: FAIL (repository not configured)")
        return 1

    manifest_path = (
        ROOT
        / "knowledge"
        / kb_id
        / "metadata"
        / "source-manifest.json"
    )

    if not manifest_path.exists():
        print("SOURCE CHECK: FAIL (source manifest missing)")
        return 1

    try:
        manifest = json.loads(
            manifest_path.read_text(encoding="utf-8")
        )
    except json.JSONDecodeError:
        print("SOURCE CHECK: FAIL (invalid source manifest JSON)")
        return 1

    local_commit = manifest.get("source_commit")

    if not local_commit:
        print("SOURCE CHECK: FAIL (manifest has no source_commit)")
        return 1

    print(f"KB: {kb_id}")
    print(f"REPOSITORY: {repository}")
    print(f"BRANCH: {branch}")
    print(f"LOCAL SNAPSHOT: {local_commit}")

    result = subprocess.run(
        [
            "git",
            "ls-remote",
            repository,
            f"refs/heads/{branch}",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("SOURCE CHECK: FAIL")
        if result.stderr.strip():
            print(result.stderr.strip())
        return result.returncode or 1

    output = result.stdout.strip()

    if not output:
        print(
            f"SOURCE CHECK: FAIL "
            f"(branch not found: {branch})"
        )
        return 1

    remote_commit = output.split()[0]

    print(f"REMOTE HEAD: {remote_commit}")

    if remote_commit == local_commit:
        print("SOURCE STATUS: CURRENT")
        print("SOURCE CHECK: PASS")
        return 0

    print("SOURCE STATUS: UPDATE AVAILABLE")
    print("SOURCE CHECK: PASS")
    return 0


def rollback_kb(kb_id: str):
    kb = get_kb(kb_id)

    chunk_value = kb.get("chunk_path")

    if not chunk_value:
        print(f"ROLLBACK: FAIL ({kb_id} has no chunk_path)")
        return 1

    chunk_path = resolve_agent_path(chunk_value)
    backup_root = ROOT / "knowledge" / kb_id / "backups"

    if not backup_root.exists():
        print("ROLLBACK: FAIL (no backup directory found)")
        return 1

    backups = sorted(
        [
            path
            for path in backup_root.iterdir()
            if path.is_dir()
            and path.name.startswith("chunks-")
        ],
        reverse=True,
    )

    if not backups:
        print("ROLLBACK: FAIL (no chunk snapshots found)")
        return 1

    backup_path = backups[0]

    print(f"ROLLBACK KB: {kb_id}")
    print(f"SOURCE SNAPSHOT: {backup_path}")
    print(f"TARGET: {chunk_path}")

    if chunk_path.exists():
        shutil.rmtree(chunk_path)

    shutil.copytree(
        backup_path,
        chunk_path,
    )

    print("ROLLBACK RESTORE: PASS")
    print()
    print("POST-ROLLBACK VERIFICATION")

    result = verify_kb(kb_id)

    if result != 0:
        print("ROLLBACK: FAIL")
        return result

    print("ROLLBACK: PASS")
    return 0


def refresh_kb(kb_id: str):
    kb = get_kb(kb_id)

    if kb.get("type") != "chunk_directory":
        print(
            f"REFRESH: SKIP ({kb_id} is not a chunk_directory KB)"
        )
        return 0

    print(f"REFRESH KB: {kb_id}")

    backup_path = backup_chunks(kb_id)

    result = rebuild_kb(kb_id)

    if result != 0:
        print("REFRESH: FAIL")

        if backup_path:
            print(f"ROLLBACK AVAILABLE: {backup_path}")

        return result

    print("REFRESH: PASS")

    if backup_path:
        print(f"ROLLBACK SNAPSHOT: {backup_path}")

    return 0


def rebuild_kb(kb_id: str):
    kb = get_kb(kb_id)

    if kb.get("type") != "chunk_directory":
        print(
            f"REBUILD: SKIP ({kb_id} is not a chunk_directory KB)"
        )
        return 0

    chunker = ROOT / "tools" / "kb_chunk.py"

    if not chunker.exists():
        print(f"REBUILD: FAIL (chunker missing: {chunker})")
        return 1

    print(f"REBUILD KB: {kb_id}")
    print(f"CHUNKER: {chunker}")

    result = subprocess.run(
        [
            sys.executable,
            str(chunker),
            kb_id,
        ],
        cwd=ROOT.parent,
    )

    if result.returncode != 0:
        print(
            f"REBUILD: FAIL (chunker exit code {result.returncode})"
        )
        return result.returncode

    print("REBUILD: PASS")

    print()
    print("POST-REBUILD VERIFICATION")

    return verify_kb(kb_id)


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
        "  kb_manage.py verify all\n"
        "  kb_manage.py rebuild <kb-id>\n"
        "  kb_manage.py refresh <kb-id>\n"
        "  kb_manage.py rollback <kb-id>\n"
        "  kb_manage.py source-check <kb-id>",
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

    if command == "rebuild":
        if len(sys.argv) != 3:
            usage()
            return 2

        return rebuild_kb(sys.argv[2])

    if command == "refresh":
        if len(sys.argv) != 3:
            usage()
            return 2

        return refresh_kb(sys.argv[2])

    if command == "rollback":
        if len(sys.argv) != 3:
            usage()
            return 2

        return rollback_kb(sys.argv[2])

    if command == "source-check":
        if len(sys.argv) != 3:
            usage()
            return 2

        return source_check_kb(sys.argv[2])

    usage()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
