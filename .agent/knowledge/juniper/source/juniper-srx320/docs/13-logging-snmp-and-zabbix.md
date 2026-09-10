# Juniper SRX320 Logging, SNMP, and Zabbix Monitoring

## Scope

This document explains logging, SNMP, telemetry-oriented monitoring, and Zabbix integration concepts for the Juniper SRX320.

It is intended for:

- Device health monitoring
- Interface monitoring
- Security event visibility
- Capacity monitoring
- Alerting
- Syslog integration
- SNMP integration
- AI-assisted troubleshooting

This document provides platform-level guidance and does not represent a specific production monitoring configuration unless explicitly labeled.

---

## Monitoring Philosophy

Monitoring should answer three questions:

1. Is the SRX reachable?
2. Is the SRX healthy?
3. Is the SRX forwarding traffic as expected?

Monitoring should cover both device health and service behavior.

A device responding to ping does not prove that:

- Interfaces are healthy
- Security policies are working
- NAT is working
- VPNs are operational
- Published services are reachable

---

## Monitoring Categories

Recommended monitoring categories include:

- Device reachability
- Interface state
- Interface utilization
- Interface errors
- CPU utilization
- Memory utilization
- Storage utilization
- Uptime
- Chassis alarms
- System alarms
- Security events
- VPN status
- Routing status
- Configuration changes
- Environmental sensors where available

---

## ICMP Reachability

ICMP may be used for basic availability monitoring.

Ping can indicate:

- Device reachability
- Basic network path availability
- Approximate latency

Ping does not validate:

- SNMP
- Routing policy
- NAT
- Security policy
- Application health

ICMP should be treated as a basic availability signal only.

---

## SNMP Overview

SNMP may be used to collect operational metrics from the SRX320.

Common monitoring targets include:

- Interface counters
- Interface status
- CPU
- Memory
- Uptime
- Chassis information
- Device health
- Environmental status

Available metrics depend on Junos version, platform support, and MIB implementation.

---

## SNMP Versions

Common SNMP versions include:

- SNMPv2c
- SNMPv3

SNMPv3 provides stronger security capabilities and should be preferred where practical.

SNMPv2c uses community strings and should be restricted carefully.

---

## SNMP Security

SNMP should be restricted to authorized monitoring systems.

Consider:

- Source-address restrictions
- Security-zone host-inbound settings
- Firewall filters
- SNMP version
- Authentication
- Encryption
- Credential protection

Never expose SNMP broadly to untrusted networks.

---

## SNMP Credentials

Production SNMP credentials must not be stored in public documentation.

Do not publish:

- Community strings
- Authentication passwords
- Privacy passwords
- SNMPv3 secrets

Public examples should use placeholders.

---

## Host-Inbound SNMP

SNMP traffic destined to the SRX itself may require host-inbound permission on the appropriate security zone or interface.

If SNMP monitoring fails, verify:

1. IP reachability
2. Routing
3. Security zone
4. Host-inbound SNMP permission
5. SNMP configuration
6. Source restrictions
7. Credentials
8. Monitoring-server configuration

---

## Useful SNMP Verification

Useful Junos configuration review may include:

show configuration snmp

show configuration security zones

show interfaces terse

show system uptime

Exact command availability may vary by Junos version.

---

## Syslog

The SRX may send system logs to an external syslog server.

Remote syslog improves:

- Retention
- Centralization
- Searchability
- Incident correlation
- Audit history

Syslog should complement, not replace, direct operational commands.

---

## Events Worth Logging

Useful event categories may include:

- Administrative login
- Authentication failure
- Configuration commit
- Interface up/down
- Chassis alarms
- System alarms
- Security policy events
- Routing events
- VPN events
- Service failures

---

## Security Policy Logging

Security policies may log:

- Session initiation
- Session closure

Policy logging can help verify traffic behavior.

Excessive logging can create unnecessary load.

Use policy logging where it provides operational or security value.

---

## Local Logs

Useful commands may include:

show log messages

show log <filename>

show log ?

Available log files depend on configuration and Junos release.

---

## Configuration Change Monitoring

Configuration changes should be visible through commit history.

Useful command:

show system commit

Monitoring or logging systems may also track configuration changes.

Configuration-change visibility is useful for:

- Troubleshooting
- Audit
- Incident response
- Change management

---

## Zabbix Integration

Zabbix may monitor the SRX320 using:

- ICMP
- SNMP
- External checks
- Syslog integration
- Custom scripts
- API or telemetry integrations where applicable

The simplest initial design is usually:

1. ICMP reachability
2. SNMP interface monitoring
3. CPU and memory monitoring
4. Uptime
5. Chassis/system alarms
6. Syslog forwarding

---

## Zabbix Host Definition

Recommended Zabbix host documentation should include:

Host Name:

Display Name:

Management IP:

SNMP Version:

SNMP Interface:

Template:

Host Group:

Availability Method:

Configuration State:

Verification Date:

Notes:

Do not store SNMP secrets in public documentation.

---

## Interface Monitoring

Monitor important interfaces for:

- Operational status
- Administrative status
- Inbound traffic
- Outbound traffic
- Errors
- Discards
- CRC errors where available
- Utilization percentage
- Unexpected link changes

WAN, LAN, DMZ, VPN, and trunk interfaces should be prioritized.

---

## Interface Naming

Zabbix discovery may identify interfaces using:

- Interface name
- Interface alias
- Interface description
- SNMP index

Meaningful Junos interface descriptions improve monitoring usability.

Examples:

WAN_TO_ISP

LAN_CORE

DMZ_SWITCH

VPN_BRANCH

---

## Interface Thresholds

Thresholds should reflect actual link capacity and business importance.

Examples may include:

- High bandwidth utilization
- Interface down
- Error-rate increase
- Discard-rate increase

Avoid generic thresholds without understanding the link.

---

## CPU Monitoring

CPU utilization should be monitored for abnormal sustained usage.

Short spikes may be normal.

Sustained high CPU may indicate:

- Excessive logging
- High session load
- Routing activity
- Management activity
- Software issue
- Attack traffic

CPU alerts should consider duration, not only instantaneous value.

---

## Memory Monitoring

Monitor memory trends rather than relying only on a single threshold.

High memory usage may not automatically indicate a fault.

Evaluate:

- Current usage
- Trend
- System behavior
- Process state
- Alarms

---

## Uptime Monitoring

Uptime can help identify:

- Unexpected reboot
- Power loss
- Software crash
- Planned maintenance
- Device replacement

Unexpected uptime resets should trigger investigation.

---

## Chassis and System Alarms

Useful commands may include:

show chassis alarms

show system alarms

Alarm monitoring can help identify:

- Hardware fault
- Environmental issue
- Configuration issue
- System condition requiring attention

---

## VPN Monitoring

If VPNs are deployed, monitor:

- IKE state
- IPsec state
- Tunnel interface
- Peer reachability
- Traffic
- Route availability
- Application reachability

Tunnel status alone does not prove service availability.

---

## Route Monitoring

Important routes may be monitored for presence or reachability.

Examples include:

- Default route
- Critical internal routes
- VPN routes
- DMZ routes

Route monitoring should focus on business-critical paths.

---

## Published Service Monitoring

Externally published services should be tested from an appropriate external vantage point.

Examples include:

- HTTPS
- SMTP
- VPN
- Custom applications

Internal testing alone may not detect:

- Destination NAT problems
- Public routing problems
- ISP issues
- External firewall behavior

---

## Monitoring Troubleshooting

When Zabbix cannot monitor the SRX:

1. Verify SRX reachability.
2. Verify management IP.
3. Verify route from Zabbix server.
4. Verify security zone.
5. Verify host-inbound SNMP permission.
6. Verify SNMP configuration.
7. Verify source restrictions.
8. Verify credentials.
9. Verify Zabbix interface configuration.
10. Review logs.

---

## Useful Operational Commands

Commands may include:

show interfaces terse

show interfaces extensive

show system uptime

show chassis alarms

show system alarms

show system processes extensive

show system storage

show configuration snmp

show configuration system syslog

show system commit

Exact support and syntax may vary by Junos version.

---

## Monitoring Documentation

Production monitoring records should identify:

- Monitoring platform
- Monitoring server
- Management address
- SNMP version
- Template
- Monitored interfaces
- Alert thresholds
- Syslog destination
- VPN monitoring
- Route monitoring
- Published service monitoring
- Configuration state
- Verification date

---

## Configuration States

Use:

LEGACY_PRODUCTION

SRX320_TARGET

SRX320_VERIFIED_PRODUCTION

Do not mark monitoring as verified until data is successfully being collected.

---

## Public Release Guidance

Before publishing monitoring examples:

- Remove monitoring server IPs
- Remove internal hostnames
- Remove SNMP credentials
- Remove community strings
- Remove SNMPv3 secrets
- Remove private syslog destinations
- Replace environment-specific addresses with documentation values

Preserve monitoring logic and architecture without exposing deployment-sensitive information.

---

## AI Guidance

When using this document:

- Do not invent SNMP credentials.
- Do not assume SNMP is enabled.
- Verify host-inbound configuration.
- Verify monitoring-server routing.
- Treat ICMP, SNMP, and service monitoring as separate checks.
- Do not assume tunnel-up means service-up.
- Prefer trend analysis over single-point metrics.
- Verify Junos version before relying on version-specific OIDs or behavior.

---

## Document Status

Document Type: Logging, SNMP, and Zabbix Monitoring

Knowledge Base: Juniper SRX320 Knowledge Base

Version: 0.1.0

Status: Initial Build
