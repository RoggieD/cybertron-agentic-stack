# CyberTron Agent Infrastructure

This `.agent/` directory is CyberTron's portable brain.

It provides persistent memory, reusable skills, operational protocols, and shared agent context across supported harnesses. The underlying AI model may change; the CyberTron brain should remain portable and durable.

## Core Architecture

CyberTron separates state into four memory layers:

1. `memory/personal/` — stable operator preferences and interaction conventions
2. `memory/working/` — current task state, checkpoints, hypotheses, and next actions
3. `memory/episodic/` — structured operational history and significant events
4. `memory/semantic/` — approved lessons, architectural decisions, and distilled knowledge

Do not collapse these layers into one flat memory store.

## Default Model Provider

CyberTron's default inference provider is local Ollama.

Preferred default model:
- `qwen3.5:9b`

External providers may be configured, but must remain optional.

Supported provider policy:
- Ollama: default and preferred
- Grok/xAI: optional external provider
- OpenAI: optional external provider
- Anthropic: optional external provider
- MiniMax: optional external provider

Do not send private CyberTron context to an external provider unless explicitly permitted.

## Context Loading Order

Always load these when available:

1. `memory/personal/PREFERENCES.md`
2. `memory/working/WORKSPACE.md`
3. `memory/working/REVIEW_QUEUE.md`
4. `memory/semantic/DECISIONS.md`
5. accepted lessons from `memory/semantic/LESSONS.md`
6. query-relevant episodic memories
7. matched skills
8. `protocols/permissions.md`

Do not treat provisional, rejected, superseded, or quarantined lessons as trusted operational guidance.

## Working Memory

Use `memory/working/WORKSPACE.md` for current task state.

Record:
- current objective
- systems or files being examined
- verified facts
- active hypotheses
- changes performed
- test results
- rollback information
- next operational step

Keep working memory concise and current.

Do not store secrets, credentials, API keys, private keys, authentication tokens, or passwords.

## Episodic Memory

Significant operational events may be logged to:

`memory/episodic/AGENT_LEARNINGS.jsonl`

Useful events include:
- successful fixes
- failed approaches
- unexpected behavior
- important diagnostics
- configuration discoveries
- operator corrections
- rollback events

Do not blindly promote episodic events into permanent semantic memory.

## Semantic Memory

`memory/semantic/DECISIONS.md` records deliberate architectural and workflow decisions.

`memory/semantic/LESSONS.md` contains distilled accepted lessons.

Semantic knowledge should represent information worth carrying across future sessions and harnesses.

Permanent lessons require review before acceptance.

## Review and Graduation

Candidate lessons should be reviewed before becoming trusted semantic memory.

Use the existing review workflow:
- `tools/list_candidates.py`
- `tools/graduate.py`
- `tools/reject.py`
- `tools/reopen.py`
- `tools/retract_lesson.py`

Never rubber-stamp generated lessons.

Prefer evidence-backed, reusable lessons over one-off observations.

## Skills

Skills live under:

`skills/`

Load skills only when their triggers match the current task.

CyberTron skills should eventually cover areas such as:
- Linux administration
- Docker and container troubleshooting
- networking
- Juniper operations
- Open WebUI
- Ollama
- n8n
- infrastructure diagnostics
- knowledge-base operations
- security verification
- backup and recovery

Skills should contain reusable procedure and reasoning patterns, not secrets or environment-specific credentials.

## Knowledge Bases

Large reference material should not be dumped into always-on memory.

CyberTron knowledge bases should remain separate from core memory and be retrieved only when relevant.

Examples:
- Juniper documentation
- Linux references
- Open WebUI documentation
- Ollama documentation
- internal infrastructure reference material
- business-specific knowledge packs

Memory records what CyberTron has learned.

Knowledge bases provide source material CyberTron can retrieve.

Do not confuse the two.

## Operational Workflow

For hands-on technical tasks use:

INSPECT
→ IDENTIFY
→ VERIFY
→ BACKUP / ROLLBACK
→ CHANGE
→ TEST
→ RECORD SIGNIFICANT RESULT

Prefer evidence over assumptions.

Make one controlled change at a time.

Do not repeat a previously verified step unless new evidence justifies it.

## Safety and Change Control

Before destructive, irreversible, privileged, or service-disrupting operations:

1. identify the exact target
2. explain expected impact
3. preserve a rollback path when feasible
4. obtain operator approval when required by `protocols/permissions.md`

Never bypass permissions or safety controls.

Never modify `protocols/permissions.md` autonomously.

## Provider Privacy Boundary

Local Ollama may receive normal CyberTron operational context.

External providers must receive only the minimum context necessary for the requested task.

Before sending context externally:
- exclude credentials and secrets
- exclude authentication material
- exclude unnecessary internal infrastructure details
- exclude private memory not required for the task

When uncertain, keep processing local.

## Logging

Log significant actions and outcomes, not every trivial internal step.

Avoid storing:
- full secrets
- raw credentials
- unnecessary full prompts
- large raw file contents
- sensitive configuration dumps

Prefer short factual records that are useful for future troubleshooting.

## CyberTron Design Principle

Models are replaceable.

CyberTron's durable value is its accumulated:
- memory
- skills
- decisions
- workflows
- evaluated lessons
- knowledge integrations

The brain should remain usable even when the underlying model, GPU, UI, or agent harness changes.
