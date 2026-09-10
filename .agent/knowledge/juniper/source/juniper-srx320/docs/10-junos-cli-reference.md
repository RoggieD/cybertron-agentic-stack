# Juniper SRX320 Junos CLI Reference

## Scope

This document provides a compact operational and configuration command reference for Juniper SRX320 administration.

It is intended for:

- Daily administration
- Troubleshooting
- Configuration review
- Change validation
- Migration work
- AI-assisted operations

This is a reference guide, not a substitute for understanding command impact.

---

## CLI Modes

### Operational Mode

Operational mode is used for status, diagnostics, monitoring, and verification.

Prompt commonly ends with:

>

Example:

user@srx320>

### Configuration Mode

Configuration mode is used to modify candidate configuration.

Enter with:

configure

Prompt commonly ends with:

#

Example:

user@srx320#

Exit with:

exit

---

## General Help

Use:

?

to display context-sensitive help.

Use:

help topic <keyword>

or:

help reference <keyword>

where supported.

Tab completion may be used to complete commands and object names.

---

## Configuration Review

Show current configuration:

show configuration

Show configuration in set format:

show configuration | display set

Show a specific hierarchy:

show configuration interfaces

show configuration security

show configuration routing-options

---

## Candidate Configuration Review

In configuration mode:

show

Show differences between candidate and active configuration:

show | compare

This should be reviewed before commit.

---

## Commit Commands

Validate without activating:

commit check

Activate candidate configuration:

commit

Activate temporarily:

commit confirmed

Commit with a message:

commit comment "description"

Exact syntax support may vary by Junos version.

---

## Rollback

View commit history:

show system commit

In configuration mode, load a previous revision:

rollback <number>

Review differences:

show | compare

Then commit if appropriate.

Do not use rollback numbers without verifying what they represent.

---

## Interface Commands

Quick interface summary:

show interfaces terse

Detailed interface information:

show interfaces

Show one interface:

show interfaces ge-0/0/0

Extended counters and errors:

show interfaces extensive

Show interface configuration:

show configuration interfaces

---

## Routing Commands

Show routing table:

show route

Show one destination:

show route <destination>

Show default route:

show route 0.0.0.0/0

Show static routes:

show route protocol static

Show forwarding table:

show route forwarding-table

Show ARP:

show arp

---

## Security Zone Commands

Show zone configuration:

show configuration security zones

Operational zone information:

show security zones

Use these commands to verify interface-to-zone relationships.

---

## Security Policy Commands

Show configured policies:

show configuration security policies

Operational policy view:

show security policies

Detailed policy information:

show security policies detail

Test policy matching using the actual flow criteria:

show security match-policies from-zone <source-zone> to-zone <destination-zone> source-ip <source-ip> destination-ip <destination-ip> source-port <source-port> destination-port <destination-port> protocol <protocol>

Use values from the real flow and omit only options that are genuinely not applicable to the command form supported by the installed Junos release.

---

## Session Commands

Show active sessions:

show security flow session

Filter by source:

show security flow session source-prefix <address>

Filter by destination:

show security flow session destination-prefix <address>

Session output can help identify:

- Policy match
- NAT translation
- Protocol
- Traffic direction
- Session state

---

## NAT Commands

Show all NAT configuration:

show configuration security nat

Show source NAT configuration:

show configuration security nat source

Show destination NAT configuration:

show configuration security nat destination

Show static NAT configuration:

show configuration security nat static

Operational source NAT rules:

show security nat source rule all

Operational destination NAT rules:

show security nat destination rule all

Operational static NAT rules:

show security nat static rule all

Exact syntax may vary by Junos version.

---

## System Commands

Show version:

show version

Show hardware:

show chassis hardware

Show chassis alarms:

show chassis alarms

Show system alarms:

show system alarms

Show uptime:

show system uptime

Show storage:

show system storage

Show processes:

show system processes extensive

---

## Logging Commands

Show main system log:

show log messages

Additional log files depend on configuration.

Use:

show log ?

to inspect available logs where supported.

---

## Connectivity Testing

Ping:

ping <destination>

Traceroute:

traceroute <destination>

Where needed and supported, specify source addressing to test a particular path.

A successful test from the SRX does not prove transit traffic is working.

---

## Configuration Search

Display configuration lines matching text:

show configuration | match <pattern>

Display set-format configuration and match:

show configuration | display set | match <pattern>

This is useful for quickly locating:

- IP addresses
- Interface names
- Policy names
- NAT objects
- Routes

---

## Output Filtering

Common output filters include:

| match

| except

| count

| display set

| no-more

Examples:

show configuration | display set

show interfaces terse | match ge-

show route | no-more

Filter availability may vary.

---

## Configuration Navigation

In configuration mode, use hierarchy navigation such as:

edit

up

top

Example:

edit security policies

Return one level:

up

Return to top:

top

---

## Set and Delete

Add configuration:

set <hierarchy>

Remove configuration:

delete <hierarchy>

Do not delete configuration without reviewing dependencies and rollback options.

---

## Rename and Replace

Junos supports configuration manipulation functions such as:

rename

replace

These can be useful but should be handled carefully because they may affect multiple references.

Verify changes with:

show | compare

before commit.

---

## Deactivate and Activate

Configuration may be deactivated without deleting it.

Concepts include:

deactivate

activate

This can be useful when temporarily disabling configuration while preserving it.

Always verify version-specific behavior.

---

## Commit Safety Workflow

Recommended workflow:

1. configure
2. Make one logical change.
3. show | compare
4. commit check
5. commit confirmed when lockout risk exists
6. Test
7. Confirm commit
8. Document result

---

## Troubleshooting Command Sequence

A common high-level sequence is:

show interfaces terse

show route <destination>

show configuration security zones

show security policies

show configuration security nat

show security flow session

show log messages

The exact sequence should match the failure domain.

---

## Commands to Treat Carefully

Use caution with commands or actions that:

- Clear sessions
- Delete configuration
- Roll back multiple revisions
- Reboot the device
- Restart services
- Change management addressing
- Change default routing
- Change zone membership
- Change NAT rules
- Change security policies

Always understand impact before execution.

---

## Version Awareness

Command syntax, output, and feature availability may differ between Junos releases.

Before relying on a version-specific command, verify:

show version

Do not assume all SRX320 systems run the same Junos release.

---

## AI Guidance

When using this reference:

- Prefer read-only operational commands first.
- Do not fabricate command output.
- Do not assume command availability across all Junos versions.
- Explain destructive or disruptive commands before recommending them.
- Use show | compare before commit.
- Use commit check before activation.
- Use commit confirmed when management lockout is possible.
- Verify observed state before recommending configuration changes.

---

## Document Status

Document Type: Junos CLI Reference

Knowledge Base: Juniper SRX320 Knowledge Base

Version: 0.1.0

Status: Initial Build
