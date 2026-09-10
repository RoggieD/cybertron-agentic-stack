# Juniper SRX320 Overview

## Scope

This document provides a high-level technical overview of the Juniper SRX320 platform and establishes the terminology used throughout this knowledge base.

It is intended to support:

- AI-assisted troubleshooting
- Configuration planning
- Firewall administration
- Junos learning
- ScreenOS-to-Junos migration
- Open WebUI RAG retrieval
- Reusable technical reference material

This file describes platform concepts.

It does not represent a specific production configuration unless explicitly labeled as such.

---

## Platform

Vendor: Juniper Networks

Product Family: SRX Series Services Gateways

Model: SRX320

Operating System: Junos OS

Primary Functions:

- Stateful firewalling
- Security policy enforcement
- Network Address Translation
- Routing
- VLAN and interface management
- VPN services
- Traffic inspection
- Logging and monitoring
- Network segmentation
- Administrative access control

---

## Junos Configuration Model

Junos uses a hierarchical configuration model.

Configuration is organized into logical sections such as:

- system
- interfaces
- routing-options
- protocols
- security
- vlans
- policy-options

Some Junos features also use other top-level hierarchies, including services.

Administrative services such as SSH and HTTPS are commonly configured under:

system services

Configuration changes are staged before becoming active.

A change does not take effect until it is committed.

Typical workflow:

1. Enter configuration mode.
2. Make configuration changes.
3. Review changes.
4. Validate configuration.
5. Commit changes.
6. Verify operation.

---

## Operational Modes

Junos commonly uses two primary CLI modes.

### Operational Mode

Operational mode is used for:

- Viewing system status
- Running diagnostic commands
- Viewing interfaces
- Viewing routes
- Viewing sessions
- Viewing logs
- Testing connectivity

Operational mode prompt commonly ends with:

>

Example:

user@srx320>

### Configuration Mode

Configuration mode is used for modifying configuration.

Configuration mode prompt commonly ends with:

#

Example:

user@srx320#

Enter configuration mode with:

configure

Exit configuration mode with:

exit

---

## Configuration Hierarchy

Junos configuration is hierarchical rather than based on a flat command list.

Example hierarchy:

security
  zones
  policies
  nat

interfaces
  ge-0/0/0
  ge-0/0/1

routing-options
  static

This structure makes it important to understand where a configuration statement belongs.

---

## Commit Model

Junos supports transactional configuration changes.

Changes made in configuration mode are candidates until committed.

Useful concepts include:

- commit
- commit check
- commit confirmed
- rollback
- compare

### commit

Activates the candidate configuration.

### commit check

Validates configuration syntax and dependencies without activating the change.

### commit confirmed

Activates the configuration temporarily.

If the configuration is not confirmed within the specified period, Junos automatically rolls back.

This is particularly useful when modifying:

- management access
- routing
- firewall policies
- interface addressing
- security zones

### rollback

Restores a previous configuration state.

### show | compare

Displays differences between the current candidate configuration and the active configuration.

---

## Security Zones

SRX firewall behavior is built around security zones.

Interfaces are assigned to zones.

Common zone concepts include:

- trust
- untrust
- dmz
- management

Zone names can be customized.

Traffic passing between zones is controlled by security policies.

Security policy evaluation can also apply to traffic between interfaces assigned to the same zone.

Factory-default policies and explicitly configured intrazone policies may affect same-zone behavior, so do not assume that traffic within a zone is automatically permitted.

---

## Security Policies

Security policies determine whether traffic is permitted between security zones.

Policies commonly evaluate:

- Source zone
- Destination zone
- Source address
- Destination address
- Application or service
- Action
- Logging options

Policies are directional.

A policy allowing traffic from one zone to another does not automatically create a policy in the reverse direction.

Stateful session behavior allows return traffic for established permitted sessions.

---

## Network Address Translation

The SRX platform supports several NAT types.

Primary NAT categories include:

- Source NAT
- Destination NAT
- Static NAT

### Source NAT

Changes the source address of outbound traffic.

Commonly used for Internet access from private networks.

### Destination NAT

Changes the destination address of incoming traffic.

Commonly used for port forwarding or publishing internal services.

### Static NAT

Creates a fixed one-to-one address translation.

Static NAT may be used when an internal system must consistently map to a public address.

---

## Routing

The SRX320 can perform routing in addition to firewalling.

Common routing functions include:

- Default routes
- Static routes
- Dynamic routing protocols
- Directly connected networks

Routing and security policy are separate concepts.

A valid route does not automatically permit traffic.

A security policy does not create a route.

Both must be correct for traffic to pass successfully.

---

## Interfaces

Physical interfaces on the SRX320 commonly use Junos naming conventions such as:

ge-0/0/0
ge-0/0/1
ge-0/0/2

Logical interface units are referenced using a unit number.

Example:

ge-0/0/0.0

Interface configuration may include:

- IPv4 addressing
- IPv6 addressing
- VLAN membership
- Ethernet switching
- Routed interfaces
- Security-zone assignment

Actual interface usage must be verified on the specific firewall.

Never assume that a particular physical interface is WAN, LAN, DMZ, or management without confirming the configuration.

---

## Interface, Routing, Policy, and NAT Relationship

Successful firewall traffic flow may depend on multiple configuration layers.

For the first packet of a new flow, processing can include:

1. Ingress physical and logical interface
2. Ingress security zone
3. Static NAT evaluation
4. Destination NAT evaluation
5. Route and destination-zone lookup
6. Security policy lookup
7. Reverse static NAT processing where applicable
8. Source NAT evaluation
9. Session installation
10. Egress processing

Not every flow uses every NAT stage.

Static NAT and destination NAT are evaluated before route and security policy lookup, while source NAT is evaluated after route and security policy lookup.

Troubleshooting should evaluate each applicable layer independently.

---

## ScreenOS and Junos

Juniper SSG devices commonly used ScreenOS.

The SRX320 uses Junos OS.

ScreenOS and Junos differ significantly in:

- Command syntax
- Configuration hierarchy
- Policy structure
- NAT configuration
- Interface configuration
- Administrative workflow
- Commit behavior

ScreenOS commands must not be treated as Junos commands.

Migration should focus on translating intent and function, not performing literal command conversion.

---

## Knowledge Classification

Every deployment-specific document in this knowledge base should identify configuration state when relevant.

Supported states:

### LEGACY_PRODUCTION

Configuration associated with the previous Juniper SSG firewall environment.

### SRX320_TARGET

Planned SRX320 configuration that has not yet been verified in production.

### SRX320_VERIFIED_PRODUCTION

Configuration confirmed to be active and operating successfully on the SRX320.

---

## AI Guidance

When answering questions using this knowledge base:

- Do not assume production details that are not documented.
- Distinguish platform behavior from site-specific configuration.
- Prefer verified configuration over planned configuration.
- Prefer recent verified data over historical data.
- Clearly identify uncertainty.
- Avoid fabricating interface assignments, IP addresses, policies, routes, or NAT rules.
- Recommend verification commands when production state is unknown.

---

## Document Status

Document Type: Platform Overview

Knowledge Base: Juniper SRX320 Knowledge Base

Version: 0.1.0

Status: Initial Build
