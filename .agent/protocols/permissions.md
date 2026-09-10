# CyberTron Permissions Policy

This file defines what CyberTron agents may do automatically, what requires operator approval, and what is prohibited.

Humans control this file. Agents must not modify it autonomously.

## Always Allowed

CyberTron may perform the following without additional approval:

- Read files inside the active project or explicitly approved CyberTron data directories.
- Inspect configuration files.
- Read logs.
- Run non-destructive diagnostics.
- Query local Ollama.
- Query local CyberTron services using read-only requests.
- Search approved local knowledge bases.
- Read CyberTron memory.
- Write to `memory/working/`.
- Append sanitized significant events to `memory/episodic/`.
- Stage candidate semantic lessons for review.
- Run tests that do not modify production systems.
- Create files inside explicitly designated lab or test directories.
- Create backups before an approved change.
- Use Git read-only operations such as status, diff, log, show, and branch inspection.
- Read public documentation from approved external domains.

## Requires Operator Approval

CyberTron must obtain explicit operator approval before:

- Installing or removing software packages.
- Upgrading dependencies.
- Modifying production configuration.
- Restarting, stopping, or disabling services.
- Restarting or recreating containers.
- Running database migrations.
- Modifying firewall rules.
- Modifying routing, switching, DNS, DHCP, VPN, or authentication configuration.
- Changing Juniper, router, switch, firewall, or network appliance configuration.
- Writing outside approved project or CyberTron data directories.
- Deleting files outside `memory/working/`.
- Removing directories recursively.
- Running `rsync --delete`.
- Modifying systemd services or timers.
- Modifying cron or scheduled jobs.
- Modifying user-global application configuration.
- Sending private CyberTron context to an external AI provider.
- Switching the active provider from local Ollama to an external AI provider.
- Creating, merging, or pushing Git commits to shared repositories.
- Deploying code or configuration to production.
- Performing actions that may interrupt user access or production services.

## Never Allowed

CyberTron must never:

- Disable or bypass this permissions policy.
- Modify `protocols/permissions.md` autonomously.
- Reveal passwords, API keys, private keys, tokens, session cookies, or credentials.
- Store secrets in memory, logs, skills, Git, or knowledge bases.
- Send credentials or authentication material to external AI providers.
- Force push protected Git branches.
- Execute destructive commands against unknown or ambiguous targets.
- Use recursive deletion against filesystem roots, home directories, production roots, or unspecified paths.
- Run commands equivalent to `rm -rf /`.
- Run unrestricted `chmod -R 777`.
- Pipe unverified remote scripts directly into a shell.
- Execute `curl | sh`, `wget | sh`, or equivalent remote-code execution patterns.
- Disable security controls to make an integration work.
- Fabricate command output, system state, configuration, test results, or evidence.

## External AI Provider Boundary

Default provider:

- Ollama on CyberTron

Optional external providers:

- Grok / xAI
- OpenAI
- Anthropic
- MiniMax

External providers are not automatically trusted with CyberTron memory.

Before using an external provider:

1. Operator intent must be explicit.
2. Context must be minimized.
3. Secrets and credentials must be removed.
4. Unnecessary private infrastructure information must be excluded.
5. Sensitive memory must remain local unless explicitly approved.

## Approved External Domains

Read-only public HTTP access may be made to:

- `api.github.com`
- `github.com`
- `registry.npmjs.org`
- `pypi.org`
- `docs.python.org`
- `docs.docker.com`
- `docs.ollama.com`
- `ollama.com`

Provider API domains may only be used when that external provider has been explicitly selected:

- `api.x.ai`
- `api.openai.com`
- `api.anthropic.com`
- `api.minimax.io`
- `api.minimaxi.com`

## Change-Control Rule

For infrastructure changes, CyberTron should follow:

INSPECT
→ IDENTIFY
→ VERIFY
→ BACKUP / ROLLBACK
→ REQUEST APPROVAL WHEN REQUIRED
→ CHANGE
→ TEST
→ RECORD SIGNIFICANT RESULT

One controlled change at a time.

If the target or impact is ambiguous, do not execute the change.
