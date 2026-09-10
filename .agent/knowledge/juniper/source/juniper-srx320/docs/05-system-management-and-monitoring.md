# Juniper SRX320 System Management and Monitoring

## Scope

This document explains system management, administrative access, logging, monitoring, and operational verification concepts for the Juniper SRX320.

It provides platform-level guidance and does not represent a specific production management configuration unless explicitly labeled.

---

## Management Overview

SRX320 management should be designed to provide reliable administrative access while limiting unnecessary exposure.

Common management functions include:

- SSH
- HTTPS
- Console access
- SNMP
- Syslog
- NTP
- DNS
- User authentication
- Configuration backup
- Software maintenance
- Monitoring

Management access should follow least-privilege principles.

---

## Console Access

Console access provides direct local administrative access.

Console access is particularly important during:

- Initial deployment
- Network migration
- Management lockout
- Routing failure
- Firewall policy failure
- Software upgrade recovery

A production firewall migration should preserve a working console path whenever possible.

---

## SSH Management

SSH is commonly used for CLI administration.

SSH access should be restricted to trusted administrative networks or hosts.

Consider:

- Source address restrictions
- Security-zone host-inbound settings
- Strong authentication
- Administrative user roles
- Key-based authentication where appropriate

Do not expose SSH broadly to untrusted networks without a specific requirement.

---

## HTTPS Management

HTTPS may be used for browser-based administration when supported and enabled.

Management HTTPS should:

- Use trusted administrative networks
- Use TLS
- Avoid public exposure when unnecessary
- Use appropriate authentication
- Be disabled if not operationally required

---

## Host-Inbound Services

Management services destined to the SRX itself are controlled through host-inbound traffic configuration.

Examples include:

- ssh
- https
- ping
- snmp
- dns
- dhcp
- ntp-related traffic where applicable

Host-inbound services should be enabled only where required.

---

## Administrative Users

Administrative accounts should be individually identifiable when practical.

Avoid unnecessary shared credentials.

User configuration may include:

- Username
- Authentication method
- Login class
- Privilege level
- SSH public key

Administrative privilege should match operational need.

---

## Root Access

Direct root access should be handled carefully.

Where practical:

- Use named administrative accounts
- Limit direct root login
- Protect root credentials
- Avoid embedding privileged credentials in scripts or documentation

Production credentials must never be included in public knowledge-base releases.

---

## NTP

Accurate time is important for:

- Logs
- Security investigations
- Monitoring
- VPN operation
- Certificate validation
- Event correlation

The SRX should use reliable NTP sources.

Verify time using operational commands appropriate to the installed Junos version.

---

## DNS

The SRX may require DNS resolution for administrative or service functions.

DNS configuration should identify reliable resolvers.

DNS failure should not be confused with general IP connectivity failure.

When troubleshooting:

1. Test IP connectivity.
2. Test DNS resolution separately.

---

## System Logging

Junos supports local and remote logging.

Logs may include:

- System events
- Authentication events
- Interface changes
- Routing events
- Security events
- Policy logs
- Commit activity

Remote syslog is recommended when centralized operational visibility is required.

---

## Local Logs

Common operational log review may include:

show log messages

Additional log files may exist depending on configuration.

When troubleshooting, use logs as evidence rather than assuming the cause.

---

## Remote Syslog

Remote logging can improve:

- Historical retention
- Centralized analysis
- Correlation
- Incident investigation

Documentation should identify:

- Syslog destination
- Source interface or address if configured
- Facility
- Severity
- Purpose

Do not publish real logging destinations in public releases.

---

## SNMP

SNMP may be used for monitoring:

- Interface status
- Interface counters
- CPU
- Memory
- Device health
- System uptime

SNMP configuration should be restricted to authorized monitoring systems.

Prefer secure SNMP versions where practical.

Do not expose SNMP to untrusted networks.

---

## Zabbix Integration

The SRX320 may be monitored by Zabbix or another network monitoring platform.

Common monitoring targets include:

- Reachability
- Interface state
- Interface utilization
- Error counters
- CPU utilization
- Memory utilization
- Uptime
- Device temperature where supported
- Routing or VPN status where supported

Actual OIDs and supported metrics should be verified against the installed Junos version and monitoring template.

---

## Interface Monitoring

Useful commands include:

show interfaces terse

show interfaces

show interfaces extensive

Monitor for:

- Link state
- Errors
- Drops
- CRC errors
- Traffic rate
- Negotiated speed
- Duplex behavior

---

## System Health

Useful health checks may include:

show system uptime

show system processes extensive

show system storage

show chassis hardware

show chassis alarms

show system alarms

Exact command support may vary by Junos version.

---

## Commit History

Configuration history is operationally important.

Useful commands may include:

show system commit

show system rollback

These can help identify:

- Who changed configuration
- When a change occurred
- Previous configuration states
- Potential rollback points

---

## Configuration Backup

Regular configuration backups should be maintained.

Recommended backup events include:

- Before major changes
- Before software upgrades
- Before migration
- After verified production changes
- On a regular schedule

Backup copies should be stored outside the firewall.

---

## Rescue Configuration

Junos supports rescue configuration functionality.

A known-good rescue configuration can provide an additional recovery option.

The rescue configuration should represent a stable, tested baseline.

Do not create or update a rescue configuration until the active configuration has been verified.

---

## Software and Junos Version

The installed Junos version should be recorded in production documentation.

Version information is important because:

- Commands may differ
- Features may differ
- Security fixes may differ
- Hardware support may differ
- Upgrade paths may differ

Do not assume all SRX320 devices behave identically across Junos releases.

---

## Useful Version and Platform Commands

Use:

show version

to identify the running Junos OS release.

Additional platform information may be gathered with:

show chassis hardware

The command show system software displays loaded Junos software extensions on classic Junos OS and should not be treated as the primary command for identifying the base Junos release.

Exact output and available options vary by Junos release.

---

## Management Troubleshooting

When management access fails, verify:

1. Physical interface state
2. Logical interface state
3. Management IP
4. Routing
5. Security zone
6. Host-inbound service configuration
7. Firewall filter if applicable
8. Source address
9. SSH or HTTPS service status
10. Authentication
11. Logs
12. Return path

Do not immediately change security policy without confirming whether the traffic is transit traffic or host-inbound traffic.

---

## Monitoring Documentation

Production monitoring records should identify:

- Monitoring platform
- SRX management address
- Monitoring protocol
- SNMP version if used
- Monitored interfaces
- Alert thresholds
- Logging destination
- Configuration state
- Verification date

Configuration state must be one of:

LEGACY_PRODUCTION

SRX320_TARGET

SRX320_VERIFIED_PRODUCTION

---

## Public Release Guidance

Before publishing management examples:

- Remove usernames
- Remove passwords
- Remove SSH keys
- Remove SNMP credentials
- Remove management IP addresses
- Remove internal monitoring server names
- Remove syslog destinations
- Remove private NTP or DNS infrastructure
- Replace sensitive examples with generic documentation values

---

## AI Guidance

When using this document:

- Do not invent management addresses.
- Do not invent usernames.
- Do not expose secrets.
- Distinguish host-inbound traffic from transit traffic.
- Verify Junos version before relying on version-specific commands.
- Prefer console recovery when network management access is uncertain.
- Use logs and commit history as troubleshooting evidence.

---

## Document Status

Document Type: System Management and Monitoring

Knowledge Base: Juniper SRX320 Knowledge Base

Version: 0.1.0

Status: Initial Build
