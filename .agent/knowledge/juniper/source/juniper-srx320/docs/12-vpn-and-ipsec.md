# Juniper SRX320 VPN and IPsec

## Scope

This document explains VPN and IPsec concepts for the Juniper SRX320 running Junos OS.

It is intended for:

- Site-to-site VPN planning
- Remote connectivity
- ScreenOS-to-Junos migration
- VPN troubleshooting
- Security policy integration
- Routing validation
- AI-assisted operations

This document provides platform-level guidance and does not represent a specific production VPN configuration unless explicitly labeled.

---

## VPN Overview

The SRX320 can provide encrypted connectivity between networks or endpoints.

Common VPN use cases include:

- Site-to-site VPN
- Branch connectivity
- Partner connectivity
- Remote network access
- Secure traffic over untrusted networks

VPN operation depends on multiple components working together.

These may include:

- IKE
- IPsec
- Authentication
- Routing
- Security policies
- Traffic selectors
- NAT behavior
- Interface configuration

---

## IKE

Internet Key Exchange establishes and manages secure keying relationships between VPN peers.

IKE configuration commonly includes:

- Peer address
- Authentication method
- Pre-shared key or certificate
- Encryption algorithm
- Authentication algorithm
- Diffie-Hellman group
- Lifetime
- IKE version

Exact supported options depend on Junos version.

---

## IKE Versions

Common IKE versions include:

- IKEv1
- IKEv2

Where supported and appropriate, IKEv2 may provide operational and security advantages.

Do not assume the remote peer supports the same IKE version.

Peer compatibility must be verified.

---

## Authentication

VPN peers may authenticate using:

- Pre-shared keys
- Certificates

Secrets must not be stored in public knowledge-base content.

Production pre-shared keys, private keys, and certificate private material must be protected.

---

## IPsec

IPsec protects the actual data traffic after successful IKE negotiation.

IPsec configuration may define:

- Encryption
- Authentication
- Protocol
- Lifetime
- Perfect Forward Secrecy
- Traffic selectors

The exact configuration model depends on VPN type and Junos release.

---

## Route-Based VPN

Route-based VPNs commonly use secure tunnel interfaces.

A common Junos tunnel interface family is:

st0

Example logical interface:

st0.0

Routing directs traffic into the VPN tunnel.

Route-based VPNs can provide flexible integration with:

- Static routing
- Dynamic routing
- Multiple networks
- Security zones

---

## Policy-Based VPN

Some legacy environments may use policy-based VPN designs.

Migration from ScreenOS should identify the actual VPN behavior before choosing an SRX design.

Do not blindly recreate policy-based VPN behavior if a route-based design is more appropriate.

---

## Secure Tunnel Interfaces

Tunnel interfaces should be documented with:

- Interface name
- Logical unit
- Security zone
- IP addressing if used
- VPN association
- Routing purpose
- Monitoring state

Do not assume all VPNs use the same tunnel interface.

---

## VPN Security Zones

Route-based VPN tunnel interfaces may be assigned to security zones.

A dedicated VPN zone may be used.

Example concepts include:

vpn

partners

branches

Zone names are deployment-specific.

Do not assume a particular zone name.

---

## Security Policies

VPN traffic may require security policies between:

- Internal zone and VPN zone
- VPN zone and internal zone
- VPN zone and DMZ
- VPN zone and other destination zones

Policies should use least privilege.

Document:

- Source network
- Destination network
- Applications
- Business purpose

---

## Routing

Route-based VPN traffic requires correct routing.

Verify:

- Destination route
- Tunnel interface
- Next-hop behavior
- Return route
- Routing instance

A VPN may be established while application traffic still fails because routing is incorrect.

---

## NAT and VPN

NAT can interfere with VPN traffic if not designed correctly.

Possible considerations include:

- Source NAT exemption
- Destination NAT interaction
- Overlapping address spaces
- NAT traversal
- Public peer addressing

Do not assume VPN traffic should be NATed.

Verify the intended design.

---

## NAT Traversal

NAT traversal may be required when one or both VPN peers are behind NAT.

This commonly involves UDP encapsulation.

Compatibility must be verified with the remote peer.

---

## Traffic Selectors

Traffic selectors define which traffic should be protected by IPsec.

Depending on design, selectors may include:

- Local network
- Remote network
- Protocol
- Port

Selector mismatch can prevent VPN negotiation or traffic forwarding.

---

## Proxy IDs

Legacy VPN configurations may use proxy IDs.

During ScreenOS-to-Junos migration, document:

- Local network
- Remote network
- Protocol
- Port if relevant

Then determine the appropriate Junos traffic selector or VPN configuration.

Do not assume proxy-ID syntax maps directly.

---

## Dead Peer Detection

Dead Peer Detection may be used to detect unavailable peers.

This can improve tunnel recovery and failure detection.

Exact behavior and configuration depend on Junos version and peer compatibility.

---

## Perfect Forward Secrecy

Perfect Forward Secrecy may be used for IPsec key negotiation.

PFS configuration should match the remote peer.

A mismatch may prevent successful IPsec negotiation.

---

## VPN Monitoring

VPN monitoring may include:

- IKE status
- IPsec status
- Tunnel interface state
- Traffic counters
- Peer reachability
- Routing
- Application tests

Monitoring should verify actual traffic flow, not just tunnel establishment.

---

## Useful VPN Commands

Operational commands may include:

show security ike security-associations

show security ike security-associations detail

show security ipsec security-associations

show security ipsec security-associations detail

show interfaces st0 terse

show security flow session

show route

Exact syntax and output may vary by Junos version.

---

## VPN Troubleshooting

When a VPN fails, separate the problem into stages.

### Stage 1 — Peer Reachability

Verify:

- Peer IP
- Routing
- WAN connectivity
- Upstream firewall behavior

### Stage 2 — IKE Negotiation

Verify:

- IKE version
- Authentication
- Proposal
- Diffie-Hellman group
- Lifetime
- Peer identity

### Stage 3 — IPsec Negotiation

Verify:

- IPsec proposal
- PFS
- Traffic selectors
- Proxy IDs
- Lifetime

### Stage 4 — Routing

Verify:

- Local route
- Tunnel interface
- Remote network route
- Return route

### Stage 5 — Security Policy

Verify:

- Source zone
- Destination zone
- Address objects
- Application
- Policy direction

### Stage 6 — NAT

Verify:

- NAT exemption
- Source NAT
- Destination NAT
- Overlapping addressing

### Stage 7 — Application

Verify the actual service across the tunnel.

Tunnel establishment alone does not prove application connectivity.

---

## Common VPN Failure Causes

Common causes include:

- Wrong peer IP
- Incorrect pre-shared key
- IKE version mismatch
- Encryption mismatch
- Authentication mismatch
- Diffie-Hellman mismatch
- PFS mismatch
- Traffic selector mismatch
- Missing route
- Wrong security policy
- NAT interference
- Overlapping subnets
- Return-routing failure

---

## ScreenOS Migration

When migrating a ScreenOS VPN, inventory:

- Legacy VPN name
- Peer address
- Authentication method
- IKE settings
- IPsec settings
- Local networks
- Remote networks
- Proxy IDs
- Routing
- Policies
- NAT exemptions
- Monitoring

Translate the VPN design, not the literal commands.

---

## Production VPN Documentation

For each production VPN, record:

VPN Name:

VPN Type:

Peer Address:

IKE Version:

Authentication Type:

Local Networks:

Remote Networks:

Tunnel Interface:

Security Zone:

Routing:

Security Policies:

NAT Exemption:

Monitoring:

Operational Status:

Configuration State:

Verification Date:

Notes:

Do not store secrets in this record.

---

## Configuration States

Use:

LEGACY_PRODUCTION

SRX320_TARGET

SRX320_VERIFIED_PRODUCTION

A tunnel should not be marked verified merely because IKE or IPsec is established.

Verify application traffic.

---

## Public Release Guidance

Before publishing VPN examples:

- Remove peer IP addresses
- Remove internal networks
- Remove pre-shared keys
- Remove certificate private material
- Remove usernames
- Remove internal hostnames
- Replace deployment-specific values with documentation examples

Preserve the architecture and troubleshooting logic without exposing sensitive configuration.

---

## AI Guidance

When using this document:

- Never request or expose VPN secrets unnecessarily.
- Do not assume tunnel establishment means traffic works.
- Verify IKE and IPsec separately.
- Verify routing separately.
- Verify security policy separately.
- Verify NAT separately.
- Do not invent peer settings.
- Treat ScreenOS VPN migration as functional translation, not syntax conversion.
- Prefer live operational output when troubleshooting.

---

## Document Status

Document Type: VPN and IPsec

Knowledge Base: Juniper SRX320 Knowledge Base

Version: 0.1.0

Status: Initial Build
