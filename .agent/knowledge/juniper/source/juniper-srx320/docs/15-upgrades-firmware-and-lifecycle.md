# Juniper SRX320 Upgrades, Firmware, and Lifecycle

## Scope

This document explains Junos software maintenance, upgrade planning, firmware considerations, lifecycle management, and rollback strategy for the Juniper SRX320.

It is intended for:

- Junos upgrades
- Security maintenance
- Platform lifecycle planning
- Maintenance-window preparation
- Recovery planning
- AI-assisted operational guidance

This document provides platform-level guidance and does not represent a specific production upgrade plan unless explicitly labeled.

---

## Upgrade Philosophy

Do not upgrade a production SRX solely because a newer Junos release exists.

Upgrade when there is a clear operational reason, such as:

- Security fix
- Hardware support
- Required feature
- Stability improvement
- Vendor recommendation
- Supportability requirement
- Compatibility requirement

Every upgrade should have a rollback plan.

---

## Pre-Upgrade Requirements

Before upgrading Junos, verify:

1. Current Junos version
2. Hardware model
3. Available storage
4. Current configuration backup
5. Rescue configuration
6. Console access
7. Management access
8. Upgrade path
9. Target release compatibility
10. Maintenance window
11. Rollback method
12. Post-upgrade validation plan

---

## Current Version Verification

Use:

show version

to identify the running Junos OS release.

Confirm the hardware platform with:

show chassis hardware

The command show system software displays loaded Junos software extensions on classic Junos OS and should not be used as the primary source for the base Junos version.

Record the current version before any change.

---

## Release Selection

Select a Junos release based on:

- SRX320 hardware support
- Juniper support guidance
- Security advisories
- Feature requirements
- Known issues
- Upgrade-path requirements
- Operational stability

Do not assume the newest available release is automatically the best production choice.

---

## Release Notes

Review release notes before upgrade.

Look for:

- New features
- Deprecated features
- Removed features
- Known issues
- Fixed issues
- Behavioral changes
- Security changes
- Upgrade restrictions

Version-specific changes may affect existing configuration.

---

## Configuration Backup

Before upgrade, create an off-device backup of the active configuration.

The backup should be:

- Current
- Complete
- Readable
- Stored securely
- Associated with the correct device
- Associated with the current Junos version

Do not rely only on rollback files stored on the SRX itself.

---

## Rescue Configuration

A known-good rescue configuration should exist before major maintenance.

Verify that the rescue configuration represents a stable baseline.

Do not overwrite a good rescue configuration with an unverified candidate.

---

## Console Access

Console access is strongly recommended during software maintenance.

Console access may be required if:

- Network management fails
- Boot process fails
- Interface behavior changes
- Configuration migration fails
- Recovery mode is required

---

## Storage Verification

Verify sufficient storage before transferring or installing software.

Useful commands may include:

show system storage

Do not begin an upgrade if available storage is uncertain.

---

## Image Verification

Software images should be obtained from an authorized and trusted source.

Where checksums or signatures are provided:

- Verify integrity
- Confirm image name
- Confirm platform compatibility
- Confirm expected release

Do not install unverified images.

---

## Upgrade Path

Some Junos upgrades may require intermediate versions.

Do not assume a direct upgrade path is supported between arbitrary releases.

Verify the supported upgrade path for:

- Current version
- Target version
- SRX320 platform

---

## Maintenance Window

Plan upgrades within an appropriate maintenance window.

The window should account for:

- Image transfer
- Installation
- Reboot
- Boot verification
- Configuration validation
- Traffic testing
- Rollback time

Do not allocate only enough time for the successful path.

Include recovery time.

---

## Upgrade Execution

Exact installation commands depend on Junos version and deployment method.

Before executing an upgrade:

- Confirm image path
- Confirm platform
- Confirm target release
- Confirm backup
- Confirm console access
- Confirm rollback plan

Use authoritative version-specific Juniper documentation for exact upgrade commands.

SRX300-line upgrade procedures can contain release-specific requirements and exceptions. For example, particular upgrade or downgrade paths can require specific request system software add options. Never reuse an installation command from another Junos release without checking the current SRX upgrade documentation and supported upgrade path.

---

## Reboot

A software upgrade may require rebooting the SRX.

Before reboot:

- Confirm maintenance approval
- Confirm configuration saved
- Confirm console access
- Confirm expected outage
- Confirm monitoring suppression if required

Do not reboot casually during troubleshooting.

---

## Post-Upgrade Validation

After the SRX returns to service, verify:

1. Junos version
2. System alarms
3. Chassis alarms
4. Interface status
5. Routing
6. Security zones
7. Security policies
8. NAT
9. Internet connectivity
10. Published services
11. VPNs
12. Monitoring
13. Logging
14. Management access
15. Performance

---

## Useful Post-Upgrade Commands

Commands may include:

show version

show chassis alarms

show system alarms

show interfaces terse

show route

show security policies

show configuration security nat

show security flow session

show system uptime

Exact syntax may vary by Junos release.

---

## Configuration Migration

Junos may automatically migrate or reinterpret configuration during upgrade.

After upgrade, inspect:

- Commit warnings
- Configuration differences
- Deprecated syntax
- Unsupported features
- Interface behavior
- Security behavior

Do not assume a successful boot means the configuration migrated perfectly.

---

## Rollback Strategy

Rollback planning should identify:

- Previous software version
- Previous configuration
- Recovery media
- Console procedure
- Decision point for rollback

Rollback should begin when defined failure criteria are met.

Do not continue experimenting indefinitely during a production outage.

---

## Failure Criteria

Examples of rollback triggers may include:

- Loss of management access
- Critical interface failure
- Routing failure
- NAT failure
- VPN failure
- Published service failure
- Severe performance degradation
- Unrecoverable configuration error

Define failure criteria before maintenance begins.

---

## Software Package Retention

Where practical, retain enough information to return to the previous known-good software state.

Document:

- Previous release
- Target release
- Installation package
- Upgrade date
- Upgrade result
- Rollback availability

---

## Security Advisories

Security advisories should be reviewed periodically.

Evaluate:

- Affected Junos releases
- SRX320 applicability
- Exploitability
- Exposure
- Available mitigation
- Fixed version
- Operational urgency

Not every advisory requires immediate emergency maintenance.

Risk should be evaluated in context.

---

## Lifecycle Management

Lifecycle planning should consider:

- Hardware age
- Vendor support status
- Software support
- Security maintenance
- Performance requirements
- Feature requirements
- Replacement planning

A working firewall can still become an operational risk if software support ends.

---

## Hardware Replacement Planning

Replacement should be considered when:

- Platform support ends
- Required Junos releases are unsupported
- Performance is insufficient
- Security requirements exceed platform capability
- Hardware reliability declines
- Required features are unavailable

Replacement should be planned, not triggered only by failure.

---

## Upgrade Documentation

Each production upgrade should record:

Device:

Current Version:

Target Version:

Upgrade Path:

Maintenance Window:

Administrator:

Backup Completed:

Rescue Configuration Verified:

Console Access Verified:

Installation Method:

Validation Results:

Problems Encountered:

Rollback Required:

Final Version:

Configuration State:

Verification Date:

Notes:

---

## Configuration States

Use:

LEGACY_PRODUCTION

SRX320_TARGET

SRX320_VERIFIED_PRODUCTION

A successful software installation does not automatically mean the firewall is fully verified.

Operational testing is required.

---

## Public Release Guidance

Before publishing upgrade examples:

- Remove hostnames
- Remove serial numbers
- Remove internal IP addresses
- Remove usernames
- Remove maintenance-ticket information
- Remove private software repository details

Preserve upgrade methodology and validation logic while sanitizing deployment-specific information.

---

## AI Guidance

When using this document:

- Do not recommend upgrading solely because a newer release exists.
- Verify current version before recommending a target version.
- Verify supported upgrade path.
- Require configuration backup and rollback planning.
- Prefer console availability for major upgrades.
- Use authoritative Juniper documentation for version-specific installation commands.
- Do not invent upgrade compatibility.
- Verify production services after upgrade.

---

## Document Status

Document Type: Upgrades, Firmware, and Lifecycle

Knowledge Base: Juniper SRX320 Knowledge Base

Version: 0.1.0

Status: Initial Build
