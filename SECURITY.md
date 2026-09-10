# Security Policy

## Supported versions

CyberTron is currently in early development. Security fixes are applied to the
current `main` branch unless otherwise documented in a release.

## Reporting a vulnerability

Do not publish suspected security vulnerabilities in a public issue.

Report vulnerabilities privately to the project maintainer through an
appropriate private contact method associated with the repository owner.

Include, when possible:

- affected file or component
- reproduction steps
- expected and observed behavior
- security impact
- whether secrets, credentials, network access, or code execution are involved
- suggested mitigation, if known

## Security model

CyberTron is designed to be local-first, but local operation does not make a
deployment automatically secure.

CyberTron can interact with:

- local language models
- external AI providers
- knowledge bases
- filesystem content
- shell and automation tooling
- network services
- agent harnesses
- optional third-party integrations

Users are responsible for reviewing permissions, provider configuration,
network exposure, and operational controls before enabling those capabilities.

## Secrets and credentials

Do not commit:

- API keys
- passwords
- tokens
- private keys
- production credentials
- unredacted firewall configurations
- sensitive internal network information

Use environment variables, secret stores, or other appropriate local secret
management mechanisms.

The repository provides `.env.example` only as a configuration template.

## Knowledge bases

Knowledge-base source material may have its own copyright, licensing, privacy,
or redistribution restrictions.

CyberTron does not automatically grant permission to publish or redistribute
third-party source material that a user chooses to retrieve or index.

Production-specific knowledge should be sanitized before publication.

## Agent and automation safety

Agentic workflows can modify files, execute commands, access network resources,
or invoke external systems depending on the harness and permissions provided.

Before enabling mutating workflows:

1. Inspect the intended operation.
2. Verify the target and affected resources.
3. Preserve a rollback path.
4. Apply least-privilege permissions.
5. Test changes in a controlled environment when practical.
6. Review results before expanding automation scope.

Bounded agent loops and approval controls reduce risk but do not replace an
operating-system sandbox or other isolation boundary.

## External providers

External AI providers may receive prompts, context, retrieved material, or
other data depending on configuration.

Use external providers only when intentionally configured and when the data
being sent is appropriate for that provider.

The default CyberTron configuration is local-first through Ollama.

## Network exposure

Do not expose local model endpoints, dashboards, management interfaces, or
agent control services directly to untrusted networks without appropriate
authentication and network controls.

## Dependencies and upstream code

CyberTron is a derivative work based on Agentic Stack and also interacts with
third-party software and documentation.

Security issues may originate in:

- CyberTron-specific code
- upstream Agentic Stack code
- Python or JavaScript dependencies
- external AI providers
- local models
- third-party tools and integrations

Where appropriate, vulnerabilities should also be reported to the relevant
upstream project or vendor.

## No security certification

CyberTron has not been independently security certified or formally audited.

Use in production environments should be based on the user's own risk
assessment, testing, and operational controls.
