---
name: kb-operations
version: 2026-09-10
triggers: ["knowledge base", "kb status", "kb verification", "knowledge retrieval health", "source update", "upstream documentation changes", "kb refresh", "kb rebuild", "kb rollback", "open webui knowledge", "juniper knowledge", "source provenance", "knowledge base maintenance"]
tools: [bash, memory_reflect]
constraints: ["inspect before mutation", "verify before and after changes", "require approval for mutating operations", "preserve rollback snapshots", "sanitize before public release"]
---

# CyberTron Knowledge Base Operations

## Purpose

Operate and maintain CyberTron's registered knowledge bases safely,
consistently, and with rollback protection.

Use this skill when the operator asks about:

- knowledge base status
- KB status
- KB verification
- knowledge retrieval health
- source updates
- upstream documentation changes
- KB refresh
- KB rebuild
- KB rollback
- Open WebUI knowledge
- Juniper knowledge
- source provenance
- knowledge base maintenance

## Operating Principle

Always prefer inspection before mutation.

Default workflow:

INSPECT
→ VERIFY
→ SOURCE-CHECK
→ IDENTIFY REQUIRED CHANGE
→ REQUEST APPROVAL FOR MUTATION
→ BACKUP
→ CHANGE
→ VERIFY
→ REPORT RESULT

## Management Tool

The CyberTron KB lifecycle tool is:

    .agent/tools/kb_manage.py

Run it from the CyberTron repository root.

## Read-Only Operations

These operations may be used without mutation approval:

    python3 .agent/tools/kb_manage.py list

    python3 .agent/tools/kb_manage.py status

    python3 .agent/tools/kb_manage.py show <kb-id>

    python3 .agent/tools/kb_manage.py verify <kb-id>

    python3 .agent/tools/kb_manage.py verify all

    python3 .agent/tools/kb_manage.py source-check <kb-id>

Read-only operations should normally be attempted before proposing changes.

## Mutating Operations

These operations modify KB state and require operator approval:

    python3 .agent/tools/kb_manage.py rebuild <kb-id>

    python3 .agent/tools/kb_manage.py refresh <kb-id>

    python3 .agent/tools/kb_manage.py refresh all

    python3 .agent/tools/kb_manage.py rollback <kb-id>

    python3 .agent/tools/kb_manage.py source-update <kb-id>

    python3 .agent/tools/kb_manage.py provenance-update <kb-id>

Do not execute or recommend mutating operations casually.

Explain what will change before requesting approval.

## Refresh Safety

Remote refresh operations must preserve the last known-good KB state.

The refresh lifecycle is:

SOURCE BACKUP
→ CHUNK BACKUP
→ STAGED SOURCE UPDATE
→ RECORD EXACT SOURCE COMMIT
→ REBUILD CHUNKS
→ UPDATE PROVENANCE
→ VERIFY
→ COMMIT RESULT IF APPROPRIATE

If any stage fails, automatic rollback should restore the previous
source and chunk snapshots.

Never bypass rollback safeguards to make a refresh succeed.

## Source Integrity

For Git-backed knowledge bases:

- compare the local provenance commit with the configured upstream branch
- stage remote content before replacing local source
- record the exact staged commit
- never infer the source commit from a later remote query
- preserve source provenance
- verify after rebuilding

## Knowledge Separation

Do not confuse knowledge-base content with CyberTron memory.

Knowledge bases contain external or reference information.

Memory contains information CyberTron learned, operator preferences,
decisions, and reviewed experience.

Do not promote KB content into semantic memory merely because it was retrieved.

## Security

Never place credentials, API keys, passwords, private tokens, private
production configurations, or other secrets into reusable knowledge bases.

Before publishing or distributing a KB:

- inspect source files
- inspect generated chunks
- inspect provenance metadata
- inspect registry configuration
- remove private infrastructure details
- verify licensing and attribution

Private operational information belongs in a separate private layer.

## Public Release Rule

A CyberTron repository or knowledge-base package must not be published
until a security and sanitization review has been completed.

Public release review should search for at least:

- API keys
- passwords
- tokens
- private keys
- internal hostnames
- internal domains
- RFC1918 IP addresses
- public static IP addresses belonging to the operator
- usernames
- email addresses
- filesystem paths containing private identifiers
- production firewall configurations
- production service credentials
- private URLs
- backup paths
- database connection strings

## Failure Handling

A failed KB operation is not automatically evidence that the KB is corrupt.

Inspect the failure, verify the current KB, and preserve rollback material.

Never delete rollback snapshots during incident diagnosis.

## Reporting

When reporting KB status, distinguish clearly between:

- confirmed state
- detected upstream changes
- assumptions
- proposed actions
- actions requiring approval

Prefer concise operational output over speculative explanation.
