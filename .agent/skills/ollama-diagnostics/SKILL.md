---
name: ollama-diagnostics
version: 2026-09-10
triggers: ["ollama", "ollama error", "ollama failing", "model not loading", "model won't load", "ollama connectivity", "ollama performance", "ollama gpu", "local model", "11434"]
tools: [bash, memory_reflect]
constraints: ["inspect before changing", "one controlled change at a time", "do not restart ollama without approval", "do not pull or delete models without approval"]
---

# Ollama Diagnostics

Use this skill when diagnosing CyberTron's local Ollama runtime, model loading,
GPU utilization, API connectivity, context behavior, or inference failures.

Do not start by restarting services or changing configuration.

## Diagnostic Loop

1. **Confirm the symptom.**
   Establish exactly what is failing:
   - Ollama API unreachable
   - model unavailable
   - model load failure
   - unexpected CPU execution
   - GPU/VRAM exhaustion
   - slow inference
   - context-size failure
   - malformed API response
   - application-to-Ollama connectivity failure

2. **Verify Ollama availability.**
   Prefer read-only checks first:
   - process/service state
   - listener on TCP 11434
   - `/api/tags`
   - `/api/ps`
   - relevant logs

3. **Verify the requested model.**
   Confirm:
   - exact model name
   - model exists locally
   - parameter size
   - quantization
   - context capability
   - model capabilities

4. **Verify GPU execution.**
   Inspect GPU utilization and VRAM rather than assuming acceleration is active.
   Compare model size and requested context against available VRAM.

5. **Isolate the client path.**
   Determine whether the failure exists:
   - directly against Ollama
   - through Open WebUI
   - through n8n
   - through CyberTron's agent harness
   - through another application

   If direct Ollama access works but an application fails, investigate the
   application integration rather than changing Ollama.

6. **Form one hypothesis.**
   Record the active hypothesis in `memory/working/WORKSPACE.md`.

7. **Test one thing.**
   Use the smallest non-destructive test that proves or disproves the hypothesis.

8. **Request approval before disruptive action.**
   Operator approval is required before:
   - restarting Ollama
   - changing Ollama environment variables
   - modifying systemd configuration
   - pulling a new model
   - deleting a model
   - modifying firewall rules
   - changing production container configuration

9. **Verify after change.**
   Re-run the original failing request.

10. **Record significant findings.**
    Log durable discoveries such as:
    - model-specific limitations
    - recurring connectivity failures
    - confirmed configuration requirements
    - GPU/VRAM constraints
    - integration-specific quirks

## Preferred Read-Only Checks

Use appropriate checks such as:

- `curl -s http://127.0.0.1:11434/api/tags`
- `curl -s http://127.0.0.1:11434/api/ps`
- `ss -lntp`
- `systemctl status ollama`
- `journalctl -u ollama`
- `nvidia-smi`
- `ollama list`
- `ollama ps`

Do not assume commands succeeded. Evaluate their output.

## CyberTron Defaults

Unless verified otherwise:

- provider: Ollama
- local API: `http://127.0.0.1:11434`
- preferred primary model: `qwen3.5:9b`

Treat these as configuration defaults, not immutable facts.

## Common Failure Boundaries

### API works locally, application fails

Likely investigate:
- application endpoint configuration
- Docker host/container networking
- `host.docker.internal`
- firewall restrictions
- application credentials/configuration
- environment variables

Do not restart Ollama merely because the application cannot reach it.

### Model loads but GPU utilization is unexpected

Inspect:
- `nvidia-smi`
- loaded model state
- VRAM consumption
- context size
- quantization
- concurrent models

Do not infer CPU/GPU execution solely from perceived response speed.

### Out-of-memory or model load problems

Check actual VRAM use before changing models or context.

Prefer reducing workload or context experimentally before making persistent
configuration changes.

## What to Log

Log significant:
- root causes
- disproven hypotheses worth remembering
- model/runtime limitations
- stable configuration requirements
- successful corrective actions

Do not log:
- API keys
- credentials
- full private prompts
- unnecessary raw logs
- sensitive infrastructure data

## Anti-patterns

- Restarting Ollama as the first troubleshooting step.
- Pulling another model before verifying the existing one.
- Assuming Open WebUI failure means Ollama failure.
- Changing multiple environment variables simultaneously.
- Declaring GPU acceleration broken without checking `nvidia-smi`.
- Increasing context size without considering VRAM impact.
- Treating a temporary incident as permanent semantic knowledge.

## Self-rewrite hook

If the same Ollama failure pattern occurs repeatedly and the root cause is
verified, stage a candidate lesson and propose a conservative update to this
skill.

Do not automatically rewrite the skill from a single incident.
