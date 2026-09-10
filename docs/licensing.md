# Licensing

## Project license

Original Agentic Stack source code and documentation authored by Avidlive are
licensed under the [Apache License 2.0](../LICENSE). This applies to both the
source and compiled forms of that work.

Apache 2.0 does not replace the license of third-party software. A file or
component with an adjacent license or a listing below remains governed by that
license. Agentic Stack does not claim ownership of third-party work.

## Third-party boundaries

| Component | Location or use | License record |
| --- | --- | --- |
| Cavecrew and Caveman skills | `.cursor/skills/cavecrew` and `.cursor/skills/caveman` | Adjacent MIT `LICENSE` files, copyright Julius Brussee |
| Python dependencies | Installed from `requirements.txt`; not relicensed by Agentic Stack | Each dependency's published license and installed package metadata |
| Remotion and demo dependencies | `docs/demo` development tooling | Licenses declared by `docs/demo/package-lock.json`, including Remotion's separate license |

References to external coding tools, services, skills, or repositories in the
documentation do not bundle or relicense those products.

## Using Agentic Stack

You may use, modify, and redistribute the Avidlive-owned portions under Apache
2.0. Follow the license's redistribution requirements, including providing a
copy of the license, marking modified files, and retaining applicable notices.
When redistributing a bundled component, also follow its own license and
preserve the corresponding notice.

If the applicable license for a particular file is unclear, open an issue with
the exact path. Do not assume that the root Apache license overrides an
adjacent third-party license.

## CyberTron modifications

CyberTron is a derivative work based on Agentic Stack.

CyberTron-specific modifications include local-first inference support,
knowledge-base lifecycle tooling, retrieval integration, operational skills,
memory architecture, and related documentation.

CyberTron modifications are distributed under the Apache License 2.0 unless
a file or component states otherwise.

The original Agentic Stack attribution and license requirements remain in
effect for upstream-derived portions of the project.

## Open WebUI knowledge-base integration

CyberTron includes tooling that can retrieve and build a local knowledge base
from the Open WebUI documentation repository.

The Open WebUI documentation corpus and generated CyberTron chunks are not
distributed as part of this repository.

They are fetched and generated locally by the user during knowledge-base
bootstrap or refresh operations.

Source repository:

https://github.com/open-webui/docs

Open WebUI documentation, software, trademarks, and other materials remain
subject to the licenses and terms published by the Open WebUI project.

CyberTron does not relicense Open WebUI material.

## Juniper SRX320 knowledge base

CyberTron includes a structured Juniper SRX320 technical knowledge base.

The bundled knowledge base is intended to consist primarily of original
CyberTron-authored synthesis, including:

- technical explanations
- troubleshooting methodology
- configuration patterns
- migration guidance
- operational procedures
- schemas
- checklists
- AI/RAG-oriented reference material
- educational examples

Juniper Networks documentation is used as an authoritative research and
validation source and is not intended to be reproduced wholesale in this
repository.

Juniper Networks, Juniper, Junos, SRX, ScreenOS, and related product names and
marks remain the property of their respective owners.

CyberTron is not affiliated with, endorsed by, sponsored by, or certified by
Juniper Networks.

Unless explicitly stated otherwise, Juniper KB material marked
"documentation-checked" means that the material has been compared against
authoritative documentation. It does not mean that the configuration has been
syntax-validated, lab-verified, or live-device-verified.

See:

.agent/knowledge/juniper/source/juniper-srx320/source-material/authoritative-sources.md

and:

.agent/knowledge/juniper/source/juniper-srx320/source-material/AUDIT-RESULTS.md

for provenance, validation status, and publication guidance.

## Knowledge-base licensing boundary

A CyberTron knowledge-base registry entry does not imply ownership of, or a
license grant for, the underlying source material.

Users are responsible for complying with the applicable terms of any external
documentation, repository, API, service, or data source they configure
CyberTron to retrieve or index.
