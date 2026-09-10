# Juniper Knowledge Base

This knowledge base stores reference material for Juniper networking,
firewalls, ScreenOS, Junos, configuration, troubleshooting, and operations.

## Directory Structure

- `source/`
  - Original source documents.
  - Preserve source material unchanged whenever practical.

- `normalized/`
  - Cleaned and normalized text derived from source documents.
  - Suitable for review and later reprocessing.

- `chunks/`
  - Retrieval-ready knowledge chunks.
  - Each chunk should contain focused subject matter rather than entire manuals.

- `metadata/`
  - Source provenance, document metadata, versions, product family,
    software version, dates, licensing notes, and processing information.

## Knowledge Rules

1. Preserve source provenance.
2. Do not mix operational memory with vendor reference documentation.
3. Do not store passwords, secrets, private keys, or authentication tokens.
4. Version-specific commands must retain their applicable Juniper platform
   and software version whenever known.
5. ScreenOS and Junos content must not be treated as interchangeable.
6. Retrieved reference material should identify its source when possible.
7. Derived or interpreted information should be distinguishable from
   vendor-provided source material.

## Initial Scope

- Juniper SSG / ScreenOS
- Junos OS
- Firewall policies
- NAT
- VPN
- Routing
- Interfaces
- Security zones
- Logging and troubleshooting
- Configuration backup and recovery
