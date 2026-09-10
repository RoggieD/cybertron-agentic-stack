# Juniper ScreenOS to Junos Migration

## Scope

This document provides migration guidance for moving from Juniper SSG devices running ScreenOS to Juniper SRX devices running Junos OS.

It is intended to support:

- Configuration migration
- Feature mapping
- Firewall replacement
- Operational transition
- Policy conversion
- NAT conversion
- Interface conversion
- Troubleshooting during migration

This document focuses on translating configuration intent and architecture.

It does not support blind command-for-command conversion.

---

## Core Migration Principle

ScreenOS and Junos are different operating systems with different configuration models.

Do not treat Junos as a newer syntax version of ScreenOS.

Migration should translate:

- Intent
- Security boundaries
- Interface roles
- Routing behavior
- NAT behavior
- Policy logic
- Management requirements

rather than translating literal commands.

---

## Platform Difference

ScreenOS commonly appears on:

- SSG-series devices
- NetScreen platforms

Junos commonly appears on:

- SRX-series devices
- Juniper routing and switching platforms

ScreenOS typically uses a flatter command model.

Junos uses a hierarchical candidate configuration with commit behavior.

---

## Configuration Workflow Difference

### ScreenOS

ScreenOS configuration changes may take effect immediately depending on the command.

Typical administration uses commands beginning with:

set

unset

get

save

### Junos

Junos configuration changes are staged in candidate configuration.

Typical workflow:

configure

set ...

show | compare

commit check

commit

exit

This transactional workflow is a major operational difference.

---

## Commit and Rollback

Junos supports configuration rollback.

Useful concepts include:

commit

commit check

commit confirmed

rollback

show | compare

ScreenOS administrators should become comfortable with the candidate configuration model before production migration.

---

## Interface Migration

ScreenOS interface naming differs from Junos.

ScreenOS examples may include:

ethernet0/0

ethernet0/1

ethernet0/2

Junos examples may include:

ge-0/0/0

ge-0/0/1

ge-0/0/2

Do not assume a direct numerical mapping.

Each physical interface must be mapped by actual function.

Migration documentation should record:

- Legacy interface
- Legacy role
- Legacy IP
- Legacy zone
- New SRX interface
- New logical unit
- New IP
- New zone
- Verification state

---

## Security Zone Migration

Both ScreenOS and Junos use security-zone concepts, but configuration syntax and behavior differ.

Common ScreenOS zones may include:

Trust

Untrust

DMZ

Junos may use:

trust

untrust

dmz

or custom names.

Zone names should be chosen deliberately.

Do not assume legacy zone names must be preserved exactly.

---

## Security Policy Migration

ScreenOS policies should be translated based on:

- Source zone
- Destination zone
- Source address
- Destination address
- Service
- Action
- Logging
- Business purpose

A policy should not be migrated merely because it exists.

During migration, determine whether each policy is:

- Required
- Redundant
- Obsolete
- Overly broad
- Duplicated
- Temporary

Migration is an opportunity to clean policy sets.

---

## Address Objects

Legacy address objects should be inventoried before migration.

Record:

- Object name
- Zone
- Address
- Prefix
- Purpose
- Policy references

Address objects should be recreated in Junos using clear and consistent naming.

Avoid carrying forward meaningless or ambiguous legacy names.

---

## Service Objects

Legacy ScreenOS service objects should be mapped to:

- Built-in Junos applications
- Custom Junos applications

For each service, record:

- Protocol
- Source port if relevant
- Destination port
- Timeout behavior if relevant
- Policies using the service

Do not assume a ScreenOS service name has an identical Junos application equivalent.

---

## Source NAT Migration

ScreenOS source NAT behavior may be implemented differently in Junos.

Legacy configuration should be analyzed for:

- Interface NAT
- Policy-based NAT
- Source translation pools
- Public address usage

Junos source NAT is typically configured under:

security nat source

Migration should reproduce intended behavior, not syntax.

---

## Destination NAT Migration

Legacy inbound mapping should be documented by function.

Record:

- Public IP
- Public port
- Protocol
- Internal IP
- Internal port
- Incoming interface
- Source restrictions
- Related security policy

Then build equivalent Junos destination NAT and policy configuration.

---

## MIP and VIP Migration

ScreenOS may use constructs such as:

- MIP
- VIP

These should not be copied literally into Junos.

The migration should identify the actual function.

A legacy MIP may correspond conceptually to:

- Static NAT

A legacy VIP may correspond conceptually to:

- Destination NAT
- Port translation

Verify actual behavior before choosing the Junos implementation.

---

## Static NAT Migration

One-to-one address mappings should be documented independently of legacy syntax.

Record:

- Public address
- Internal address
- Directionality
- Related policy
- Routing requirements
- Service purpose

Then implement the equivalent Junos static NAT design.

---

## Routing Migration

Inventory all legacy routes.

Include:

- Default route
- Static routes
- Connected networks
- Dynamic routing if used
- Policy-based routing if used

For each route, record:

- Destination prefix
- Next hop
- Interface
- Purpose
- Current necessity

Do not automatically migrate obsolete routes.

---

## Management Migration

Inventory management services on the legacy firewall.

Examples:

- SSH
- HTTPS
- Telnet
- SNMP
- Syslog
- NTP
- DNS
- Administrative users

Migration should improve security where practical.

Legacy insecure protocols should not be recreated automatically.

---

## VPN Migration

VPN configuration requires independent review.

Document:

- VPN type
- Peer address
- Authentication method
- Encryption
- Local networks
- Remote networks
- Routing
- Policies
- NAT exemptions
- Operational purpose

Do not assume ScreenOS VPN configuration maps directly to Junos syntax.

---

## Logging Migration

Record legacy logging behavior before migration.

Include:

- Policy logging
- Syslog destinations
- SNMP monitoring
- Event logging
- Administrative logging

Verify equivalent logging after migration.

---

## Migration Inventory

Before configuring the SRX, collect:

1. Legacy configuration backup
2. Interface map
3. Zone map
4. Address objects
5. Service objects
6. Security policies
7. Source NAT rules
8. Destination NAT rules
9. Static mappings
10. Routes
11. VPN configuration
12. Management services
13. Logging configuration
14. Monitoring configuration
15. Public IP assignments

---

## Migration Mapping Table

Each migrated feature should be documented with a mapping.

Recommended fields:

Legacy Platform

Legacy Feature

Legacy Object

Legacy Configuration State

Target SRX Feature

Target Junos Object

Target Configuration State

Validation Method

Verification Date

Notes

---

## Migration States

Use the following configuration states:

### LEGACY_PRODUCTION

Confirmed configuration operating on the legacy ScreenOS firewall.

### SRX320_TARGET

Planned replacement configuration on the SRX320.

### SRX320_VERIFIED_PRODUCTION

Configuration confirmed to be operating correctly on the SRX320.

Do not mark migrated items as verified until tested.

---

## Migration Testing

Test each major function independently.

Recommended order:

1. Management access
2. Interface state
3. Internal routing
4. Default route
5. Internet connectivity
6. Source NAT
7. Internal zone traffic
8. DMZ traffic
9. Destination NAT
10. Published services
11. Static NAT
12. VPN
13. Monitoring
14. Logging

---

## Parallel Validation

Where practical, validate legacy and target configurations side by side before cutover.

Compare:

- Routes
- Policies
- NAT mappings
- Public services
- Management access
- Monitoring
- Logging

Do not rely only on configuration review.

Functional testing is required.

---

## Cutover Planning

A firewall migration should define:

- Maintenance window
- Current configuration backup
- Target configuration backup
- Console access
- Physical cable map
- Public IP mapping
- Rollback procedure
- Test plan
- Success criteria
- Failure criteria

---

## Rollback Planning

Rollback should be possible without redesigning the network during the outage.

A practical rollback plan may include:

- Preserved legacy firewall configuration
- Documented cable locations
- Known-good legacy device
- Saved SRX configuration
- Clear decision point for rollback

Do not dismantle the rollback path before the SRX has been verified.

---

## Migration Documentation Discipline

Do not combine legacy and target configuration without labels.

Every migration note should make clear whether information is:

LEGACY_PRODUCTION

SRX320_TARGET

SRX320_VERIFIED_PRODUCTION

This prevents AI systems and administrators from confusing historical and current state.

---

## AI Guidance

When using this document:

- Never translate ScreenOS commands literally without understanding intent.
- Never assume interface numbering maps directly.
- Never assume MIP equals one exact Junos feature without verification.
- Never assume VIP equals one exact Junos feature without verification.
- Treat NAT, policy, and routing as separate migration tasks.
- Identify obsolete legacy configuration instead of blindly copying it.
- Preserve rollback capability.
- Prefer verified behavior over configuration similarity.
- Keep legacy and SRX configuration states clearly separated.

---

## Public Release Guidance

Before publishing migration examples:

- Remove real public IP addresses
- Remove private production addressing
- Remove internal hostnames
- Remove usernames
- Remove VPN secrets
- Remove customer identifiers
- Replace sensitive topology with documentation examples

The commercial value should come from the migration methodology, mappings, troubleshooting logic, and tested examples rather than reproducing proprietary vendor documentation.

---

## Document Status

Document Type: ScreenOS to Junos Migration

Knowledge Base: Juniper SRX320 Knowledge Base

Version: 0.1.0

Status: Initial Build
