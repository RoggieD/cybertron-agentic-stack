# CyberTron Architectural Decisions

This file records deliberate architectural and workflow choices that should persist across models, sessions, and agent harnesses.

Do not treat these decisions as immutable. Revisit them when evidence, requirements, or infrastructure materially changes.

---

## 2026-09-10: CyberTron uses a four-layer memory model

**Decision:** Maintain separate personal, working, episodic, and semantic memory layers.

**Rationale:** Each layer has different retention, trust, and retrieval requirements. Working state should remain temporary, operational history should remain auditable, and permanent lessons should require deliberate promotion.

**Alternatives considered:** Single flat memory directory; storing all history in vector search; relying solely on chat history.

**Status:** active

---

## 2026-09-10: Ollama is the default inference provider

**Decision:** CyberTron uses local Ollama as its default AI inference provider.

**Default model:** `qwen3.5:9b`

**Rationale:** Local inference preserves privacy, avoids unnecessary API expense, reduces dependency on external providers, and keeps CyberTron's core capabilities available independently of cloud services.

**Alternatives considered:** OpenAI as default; Anthropic as default; xAI/Grok as default; dynamic external-provider selection.

**Status:** active

---

## 2026-09-10: External AI providers are optional augmentation

**Decision:** Grok/xAI, OpenAI, Anthropic, MiniMax, and future external providers may augment CyberTron but must not become required dependencies for core operation.

**Rationale:** External models may provide stronger reasoning, current information, specialized capabilities, or additional capacity, but CyberTron should remain functional when those services are unavailable.

**Privacy rule:** External providers receive only the minimum task context necessary and must not automatically receive private CyberTron memory, credentials, authentication material, or unnecessary internal infrastructure information.

**Status:** active

---

## 2026-09-10: CyberTron's persistent brain is independent of the model

**Decision:** Memory, skills, decisions, workflows, and evaluated lessons remain separate from any individual LLM.

**Rationale:** Models, GPUs, runtimes, and user interfaces will change. CyberTron's accumulated operational knowledge should survive those replacements.

**Alternatives considered:** Model-specific memory; Open WebUI-only memory; relying on prompt templates alone.

**Status:** active

---

## 2026-09-10: Knowledge bases remain separate from core memory

**Decision:** Large reference collections and documentation are retrieved as knowledge bases rather than inserted into permanent always-on memory.

**Rationale:** Memory represents learned state and operational experience. Knowledge bases provide source material. Combining the two creates context bloat and makes provenance difficult to maintain.

**Examples:** vendor documentation, Linux references, networking documentation, application documentation, and domain-specific knowledge packs.

**Status:** active

---

## 2026-09-10: Permanent semantic lessons require review

**Decision:** Episodic observations do not automatically become trusted semantic lessons.

**Rationale:** Automatic promotion creates memory pollution, reinforces transient errors, and can turn one-time incidents into bad permanent policy.

**Workflow:** observe → stage candidate → review evidence → accept/reject → render semantic lesson.

**Status:** active

---

## 2026-09-10: CyberTron follows controlled-change operations

**Decision:** Infrastructure work follows:

INSPECT → IDENTIFY → VERIFY → BACKUP/ROLLBACK → CHANGE → TEST → RECORD

**Rationale:** One controlled change at a time makes failures diagnosable and preserves recovery paths.

**Operational rule:** Do not repeat previously verified steps unless new evidence justifies doing so.

**Status:** active

---

## 2026-09-10: Production and lab environments remain separate

**Decision:** New agentic-stack functionality is developed and tested in an isolated lab before being promoted into production CyberTron services.

**Rationale:** The framework can write memory, replace adapter files, create links, and invoke integration-specific behavior. Validation must precede production integration.

**Current development location:** `repository-local CyberTron development tree`

**Status:** active

---

## 2026-09-10: Provider credentials remain outside the brain

**Decision:** API keys, passwords, private keys, tokens, and other credentials must never be embedded in `.agent/`, semantic memory, episodic memory, skills, or source-controlled configuration.

**Rationale:** The CyberTron brain is intended to be portable, auditable, and potentially reusable across systems.

**Implementation:** providers read credentials from environment variables or an approved secrets mechanism.

**Status:** active
