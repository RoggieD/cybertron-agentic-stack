# Juniper SRX320 Knowledge Base

## Purpose

This knowledge base provides structured technical information for the Juniper SRX320 firewall platform.

It is designed for use with local AI and retrieval-augmented generation systems such as Open WebUI, while remaining portable enough for publication, redistribution, or commercial packaging.

## Primary Platform

Vendor: Juniper Networks

Platform: SRX320

Operating System: Junos OS

Primary Use Cases:

- Firewall configuration
- Security zones
- Security policies
- Source NAT
- Destination NAT
- Static NAT
- Routing
- Interface configuration
- VLANs
- System management
- Logging
- Monitoring
- Troubleshooting
- ScreenOS-to-Junos migration
- Production firewall operations

## Knowledge Base Design

The knowledge base is divided into focused files rather than one large document.

This improves retrieval accuracy for AI systems by allowing queries to match specific technical topics without loading unrelated material.

Directory structure:

- docs/ — Primary technical knowledge
- examples/ — Configuration examples and tested patterns
- schemas/ — Structured metadata and reusable data definitions
- source-material/ — Original reference material and research sources

## Configuration State Model

Information related to the Grid Micro / Stony Point Partners deployment must clearly identify one of the following states:

### LEGACY PRODUCTION

Configuration associated with the previous Juniper SSG-series firewall using ScreenOS.

### SRX320 TARGET

Planned SRX320 configuration that has not yet been verified in production.

### SRX320 VERIFIED PRODUCTION

Configuration that has been deployed and successfully tested on the production SRX320.

Planned configuration must never be represented as verified production state.

## ScreenOS and Junos

ScreenOS and Junos are different operating systems with different configuration models.

Commands or configuration syntax from ScreenOS must not be presented as valid Junos syntax unless explicitly translated and verified.

Migration documentation should explain functional equivalence rather than performing blind command substitution.

## Operational Principles

Before making production firewall changes:

1. Inspect the current configuration.
2. Identify affected interfaces, zones, policies, NAT rules, and routes.
3. Preserve a rollback path.
4. Make one controlled change at a time.
5. Commit the change.
6. Verify connectivity and expected behavior.
7. Record the verified configuration.

Use Junos rollback and commit-confirmed capabilities when appropriate to reduce the risk of administrative lockout.

## Security Principles

- Follow least-privilege access principles.
- Avoid unnecessary exposed services.
- Restrict management access.
- Protect credentials, keys, certificates, and secrets.
- Do not publish private network information or production-sensitive configuration in public releases.
- Sanitize configuration examples before redistribution.

## AI / RAG Usage

Files should be written for reliable retrieval by AI systems.

Preferred practices:

- Clear descriptive headings
- One primary technical topic per file
- Short focused sections
- Explicit terminology
- Complete command context
- Clear distinction between examples and verified configuration
- Avoid ambiguous references such as "this", "that", or "the interface" when the actual object can be named

## Publication and Commercial Use

The knowledge base should remain portable and vendor-neutral in structure.

Original Juniper documentation should not be copied wholesale into this repository.

Commercial or public releases should consist primarily of:

- Original technical explanations
- Original troubleshooting procedures
- Configuration patterns
- Migration guidance
- Operational checklists
- Tested examples
- AI-optimized structured reference material

Vendor documentation may be cited or referenced when appropriate.

## Versioning

Changes to the knowledge base should be tracked.

Major technical updates, Junos behavior changes, corrected procedures, and verified production findings should be recorded in CHANGELOG.md.

## Status

Project status: Initial build

Platform: Juniper SRX320

Knowledge Base Type: Technical / Infrastructure / AI RAG
