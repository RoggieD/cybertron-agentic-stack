# Juniper SRX320 Configuration Backup and Recovery

## Scope

This document explains configuration backup, rollback, rescue configuration, and recovery practices for the Juniper SRX320 running Junos OS.

It is intended for:

- Production change control
- Firewall migration
- Configuration recovery
- Administrative lockout prevention
- Software maintenance
- Incident response
- AI-assisted troubleshooting

This document provides platform-level guidance and does not contain site-specific production configuration.

---

## Recovery Philosophy

Recovery capability should exist before risky changes are made.

Before modifying critical configuration, identify:

- Current configuration state
- Known-good rollback point
- Console access
- Backup location
- Recovery method
- Expected validation steps

Do not rely on memory during an outage.

---

## Candidate Configuration

Junos uses a candidate configuration model.

Changes are staged before activation.

Typical workflow:

configure

show | compare

commit check

commit

The active configuration remains unchanged until commit succeeds.

---

## Commit Check

Use:

commit check

to validate the candidate configuration before activation.

This may detect:

- Syntax errors
- Invalid references
- Dependency problems
- Configuration inconsistencies

A successful commit check does not guarantee that the resulting network behavior will be correct.

Operational validation is still required.

---

## Commit Confirmed

commit confirmed is useful when a change could interrupt management access.

Examples include changes to:

- Management IP
- Routing
- Default route
- Security zones
- Host-inbound services
- Interface addressing
- Firewall filters
- Administrative access

A confirmed commit becomes temporary until explicitly confirmed.

If access is lost and the commit is not confirmed, Junos can automatically return to the previous configuration.

---

## Recommended Remote Change Workflow

For a potentially disruptive remote change:

1. Verify console or fallback access if possible.
2. Enter configuration mode.
3. Make one logical change.
4. Run show | compare.
5. Run commit check.
6. Use commit confirmed.
7. Verify management access.
8. Verify affected services.
9. Confirm the commit.
10. Record the change.

Do not confirm the commit until validation succeeds.

---

## Rollback

Junos stores previous configuration revisions.

Rollback can restore an earlier candidate configuration.

Common concepts include:

rollback 0

rollback 1

rollback 2

The meaning of rollback numbers should be verified before use.

Review differences before committing a rollback.

---

## Review Before Rollback

Before activating a rollback:

show | compare

Review what will change.

A rollback may revert more than the one configuration item currently under investigation.

Do not assume rollback affects only the most recent line change.

---

## Commit History

Useful operational commands may include:

show system commit

Commit history can help identify:

- Commit time
- Administrator
- Commit method
- Previous revisions
- Potential rollback points

This information is useful when troubleshooting changes that occurred recently.

---

## Rescue Configuration

Junos supports a rescue configuration.

A rescue configuration should represent a known-good baseline.

It can provide an additional recovery path when the active configuration becomes unusable.

A rescue configuration should not be created from an unverified configuration.

---

## Rescue Configuration Principles

Before saving a rescue configuration, verify:

- Management access
- Interface configuration
- Routing
- Security zones
- Security policies
- NAT
- Required services
- Monitoring
- Administrative access

The rescue configuration should represent stable operation.

---

## Configuration Backup

Configuration backups should be stored outside the SRX.

Recommended backup events include:

- Initial deployment
- Before major changes
- After successful migration
- Before Junos upgrades
- After verified policy changes
- After NAT changes
- After routing changes
- After management changes

---

## Backup Content

A configuration backup should include enough information to reconstruct the firewall.

Recommended content includes:

- Active configuration
- Junos version
- Hardware model
- Interface map
- Routing
- Security zones
- Security policies
- NAT configuration
- Administrative settings
- Monitoring settings
- VPN configuration if applicable
- Relevant certificates where appropriate and securely handled

Secrets should be protected.

---

## File Naming

Use descriptive backup names.

Example pattern:

srx320-config-YYYY-MM-DD-HHMM.conf

Optional additions may include:

- hostname
- environment
- change ticket
- version

Avoid ambiguous names such as:

backup.conf

new.conf

final.conf

---

## Backup Integrity

A backup should be:

- Readable
- Complete
- Stored off-device
- Protected from unauthorized access
- Versioned
- Tested when practical

A backup that cannot be restored is not a reliable recovery mechanism.

---

## Console Recovery

Serial console access is especially valuable when:

- Management IP is unknown
- Routing is broken
- Security policy blocks management
- Host-inbound configuration is incorrect
- Network interfaces are misconfigured
- Administrative access is lost

Console access bypasses many network-dependent failure conditions.

---

## Recovery Decision Process

When recovery is required:

1. Identify the failure.
2. Determine whether management access is still available.
3. Review recent commit history.
4. Identify a known-good revision.
5. Review rollback differences.
6. Restore the minimum necessary configuration.
7. Validate management access.
8. Validate production traffic.
9. Document the recovery.

---

## Do Not Reboot First

A reboot should not be the default response to a configuration problem.

Rebooting may:

- Extend an outage
- Hide useful evidence
- Fail to correct configuration errors
- Introduce additional risk

Use configuration evidence and rollback mechanisms first when appropriate.

---

## Software Recovery

Software-related recovery may require:

- Alternate boot media
- Junos package recovery
- Console access
- Boot loader interaction
- Installation media

Exact recovery procedures depend on hardware and Junos version.

Version-specific procedures should be verified against authoritative Juniper documentation.

---

## Backup Security

Configuration backups may contain sensitive information.

Protect:

- Password hashes
- Authentication configuration
- SNMP credentials
- VPN configuration
- Certificates
- Internal addressing
- Public service mappings
- Administrative usernames

Do not publish raw production configurations.

---

## Public Release Guidance

Before including configuration examples in a public or commercial package:

- Remove credentials
- Remove public IP addresses
- Remove private topology
- Remove internal hostnames
- Remove serial numbers
- Remove VPN secrets
- Replace environment-specific values with documentation examples

Preserve the recovery procedure while removing deployment-specific data.

---

## AI Guidance

When using this document:

- Prefer rollback over unnecessary rebuilds.
- Recommend commit check before activation.
- Recommend commit confirmed when lockout risk exists.
- Do not assume rollback numbers without verification.
- Do not recommend reboot as the first response.
- Preserve console access where possible.
- Protect sensitive configuration backups.
- Distinguish platform guidance from production state.

---

## Document Status

Document Type: Configuration Backup and Recovery

Knowledge Base: Juniper SRX320 Knowledge Base

Version: 0.1.0

Status: Initial Build
