# Juniper SRX320 Knowledge Base — Authoritative Source Registry

## Purpose

This document records authoritative external sources used to validate technical content in the Juniper SRX320 Knowledge Base.

The registry exists to provide:

- Source provenance
- Validation traceability
- Maintenance references
- Release auditing
- Version-awareness
- Public and commercial packaging discipline

This file does not contain copied vendor documentation.

It records references to authoritative documentation used during research and validation.

---

## Source Priority

When validating technical content, use sources in the following order where practical:

1. Juniper Networks official Junos OS documentation
2. Juniper Networks SRX320 hardware documentation
3. Juniper Networks CLI reference
4. Juniper Networks Feature Explorer
5. Juniper Networks technical documentation and configuration guides
6. Juniper support or JTAC guidance where applicable

Third-party sources should not override current Juniper documentation.

---

## Juniper Networks Documentation

Primary Documentation Site:

https://www.juniper.net/documentation/

Use this source for:

- Junos OS behavior
- Security policies
- NAT
- Routing
- VPN
- Interfaces
- Ethernet switching
- System services
- Monitoring
- Troubleshooting
- Commit and rollback behavior

---

## SRX320 Hardware Documentation

Platform:

Juniper SRX320 Services Gateway

Primary Use:

- Physical platform characteristics
- Interface identification
- Hardware installation
- Factory-default behavior
- Console access
- Hardware-specific capabilities

Reference Type:

Juniper Networks official hardware documentation

---

## Junos NAT Documentation

Primary Topics:

- Source NAT
- Destination NAT
- Static NAT
- NAT pools
- Rule sets
- Proxy ARP
- NAT processing behavior
- NAT operational commands

Authority:

Juniper Networks Junos OS NAT documentation

---

## Junos Security Policy Documentation

Primary Topics:

- Security zones
- Inter-zone policies
- Policy matching
- Applications
- Permit and deny behavior
- Policy logging
- Policy lookup
- Translated destination behavior

Authority:

Juniper Networks Junos OS security policy documentation

---

## Junos VPN and IPsec Documentation

Primary Topics:

- IKEv1
- IKEv2
- IPsec
- Route-based VPNs
- st0 interfaces
- IKE gateways
- IPsec policies
- Traffic selectors
- Security associations
- VPN verification

Authority:

Juniper Networks Junos OS VPN/IPsec documentation

---

## Junos Ethernet Switching Documentation

Primary Topics:

- Ethernet switching
- Access ports
- Trunk ports
- VLAN membership
- IRB interfaces
- VLAN routing
- Native VLAN behavior

Authority:

Juniper Networks Junos OS Ethernet Switching documentation

---

## Junos System Services Documentation

Primary Topics:

- SSH
- HTTPS
- Host-inbound services
- System services
- Administrative access
- Management-plane configuration

Authority:

Juniper Networks Junos OS CLI reference and system services documentation

---

## Junos Routing Documentation

Primary Topics:

- Static routes
- Default routes
- Route preference
- Routing tables
- Route verification
- Routing instances

Authority:

Juniper Networks Junos OS routing documentation

---

## Junos Monitoring Documentation

Primary Topics:

- SNMP
- Syslog
- Interface monitoring
- RPM
- IP monitoring
- VPN monitoring
- System health

Authority:

Juniper Networks Junos OS network management documentation

---

## Juniper Feature Explorer

Purpose:

Verify whether a feature is supported on a specific Juniper platform or Junos release.

Primary Use:

- SRX320 feature support
- IP monitoring support
- Platform capability verification
- Release-aware validation

Authority:

Juniper Networks Feature Explorer

---

## Audit References Used — 2026-09-09

The batch technical audit used current Juniper documentation covering:

- Security Policies Overview
- Security Zones
- show security match-policies
- NAT processing and NAT rule documentation
- IPsec VPN User Guide and route-based VPN guidance
- Traffic Selectors in Route-Based VPNs
- SNMP community/client restrictions
- System and security logging
- Chassis Cluster User Guide and SRX320 interface renumbering
- Junos commit, rollback, and rescue configuration behavior
- SRX Series software installation and upgrade procedures
- SRX320 platform documentation

Exact URLs should be rechecked during future release audits because Juniper documentation locations and platform/release guidance may change.

---

## Validation Rules

A source may support a validation status of:

### documentation-checked

Use when:

- The behavior or syntax has been compared against authoritative Juniper documentation.

This does not mean:

- The command was accepted by Junos.
- The configuration passed commit check.
- The feature was tested on the target SRX320.

---

### syntax-validated

Use only when:

- Junos accepts the configuration syntax, or
- An appropriate Junos validation environment confirms the syntax.

---

### lab-verified

Use only when:

- The feature or configuration has been successfully tested in a controlled lab environment.

---

### live-device-verified

Use only when:

- The configuration or operational behavior has been directly verified on the target or equivalent SRX device.

---

## Version Awareness

Junos behavior and syntax may vary by:

- Junos release
- Platform
- Feature support
- Licensing
- Hardware generation
- Enhanced Layer 2 Software behavior
- Security feature implementation

Do not treat documentation for another platform or release as proof of SRX320 behavior unless applicability is established.

---

## Publication Rules

When this knowledge base is published:

- Do not redistribute Juniper documentation wholesale.
- Do not reproduce large vendor documentation sections.
- Prefer original explanation and synthesis.
- Cite or reference authoritative vendor documentation where appropriate.
- Do not imply Juniper endorsement.
- Do not label content vendor-certified unless such certification exists.
- Maintain validation status separately from documentation quality.

---

## Commercial Distribution

Commercial value should come from original material such as:

- Explanations
- Operational procedures
- Troubleshooting methodology
- Migration guidance
- Configuration patterns
- AI schemas
- Validation frameworks
- Checklists
- Tested examples
- Automation tooling

Vendor documentation remains the intellectual property of its respective owner.

---

## Maintenance

This registry should be reviewed when:

- A new Junos release is targeted
- SRX320 firmware is upgraded
- New configuration examples are added
- Existing examples are modified
- A technical audit discovers changed behavior
- The knowledge base is prepared for public release

---

## Current Validation State

Knowledge Base Version:

0.1.0

Target Platform:

Juniper SRX320

Target Junos Version:

Unknown until live device access is available

Current Device State:

SRX320_TARGET

Live Device Validation:

Not yet available

---

## Document Status

Document Type: Source Registry

Knowledge Base: Juniper SRX320 Knowledge Base

Version: 0.1.0

Status: Active
