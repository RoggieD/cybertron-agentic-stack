# Juniper SRX320 Production Data Template

## Scope

This document defines the structure used to record site-specific SRX320 production information.

It is intended for private deployment documentation.

Do not publish this file publicly without sanitizing sensitive information.

---

## Deployment Identity

Environment Name:

Site Name:

Organization:

Firewall Hostname:

Platform:

Junos Version:

Serial Number:

Asset Tag:

Installation Date:

Last Verification Date:

Configuration State:

Allowed values:

LEGACY_PRODUCTION

SRX320_TARGET

SRX320_VERIFIED_PRODUCTION

---

## Administrative Access

Management IP:

Management Interface:

Management Zone:

SSH Enabled:

HTTPS Enabled:

Console Access Available:

Primary Admin Network:

Secondary Admin Network:

Authentication Method:

Notes:

---

## Interface Map

For each interface, record:

Physical Interface:

Logical Unit:

Description:

Role:

IPv4 Address:

IPv6 Address:

Prefix Length:

VLAN ID:

Security Zone:

Connected Device:

Link Speed:

Configuration State:

Verification Date:

Notes:

---

## WAN Configuration

WAN Interface:

WAN Logical Unit:

WAN IP Address:

WAN Prefix:

Upstream Gateway:

Provider:

Connection Type:

Static or Dynamic:

Public Address Block:

Default Route:

Source NAT Method:

Monitoring Status:

Configuration State:

Verification Date:

Notes:

---

## LAN Configuration

LAN Interface:

LAN Logical Unit:

LAN Network:

Gateway Address:

Security Zone:

VLAN:

Connected Switch:

DHCP Role:

DNS Role:

Routing Notes:

Configuration State:

Verification Date:

Notes:

---

## DMZ Configuration

DMZ Interface:

DMZ Logical Unit:

DMZ Network:

Gateway Address:

Security Zone:

VLAN:

Connected Switch:

Published Services:

Routing Notes:

Configuration State:

Verification Date:

Notes:

---

## Security Zones

For each security zone, record:

Zone Name:

Purpose:

Interfaces:

Host-Inbound Services:

Trust Level:

Configuration State:

Verification Date:

Notes:

---

## Security Policies

For each policy, record:

Policy Name:

Source Zone:

Destination Zone:

Source Address:

Destination Address:

Application:

Action:

Logging:

Business Purpose:

Configuration State:

Verification Date:

Notes:

---

## Source NAT

For each source NAT rule, record:

Rule Set:

Rule Name:

Source Zone:

Destination Zone:

Source Address:

Destination Address:

Protocol:

Translated Address or Pool:

Business Purpose:

Configuration State:

Verification Date:

Notes:

---

## Destination NAT

For each destination NAT rule, record:

Rule Set:

Rule Name:

Incoming Zone:

Incoming Interface:

Public Address:

Public Port:

Protocol:

Translated Address:

Translated Port:

Related Security Policy:

Business Purpose:

Configuration State:

Verification Date:

Notes:

---

## Static NAT

For each static NAT mapping, record:

Rule Name:

Public Address:

Private Address:

Incoming Zone:

Related Policy:

Business Purpose:

Configuration State:

Verification Date:

Notes:

---

## Routing

For each route, record:

Destination Prefix:

Route Type:

Next Hop:

Outgoing Interface:

Routing Instance:

Preference:

Purpose:

Configuration State:

Verification Date:

Notes:

---

## VLANs

For each VLAN, record:

VLAN Name:

VLAN ID:

Subnet:

Gateway:

Member Interfaces:

Tagged Interfaces:

Untagged Interfaces:

Security Zone:

Purpose:

Configuration State:

Verification Date:

Notes:

---

## Monitoring

Monitoring Platform:

Monitoring Address:

Protocol:

SNMP Version:

SNMP Source Restrictions:

Syslog Destination:

NTP Servers:

DNS Servers:

Monitored Interfaces:

Alerting Enabled:

Configuration State:

Verification Date:

Notes:

---

## VPN

For each VPN, record:

VPN Name:

VPN Type:

Peer Address:

Authentication Type:

Local Networks:

Remote Networks:

Routing:

Security Policies:

NAT Exemption:

Operational Status:

Configuration State:

Verification Date:

Notes:

Do not store secrets or pre-shared keys in this document.

---

## Published Services

For each externally published service, record:

Service Name:

Public Address:

Public Port:

Protocol:

Internal Address:

Internal Port:

Destination NAT Rule:

Security Policy:

Internal Hostname:

Business Purpose:

Monitoring:

Configuration State:

Verification Date:

Notes:

---

## Validation Checklist

Management access verified:

WAN link verified:

Default route verified:

DNS verified:

NTP verified:

Internet access verified:

Source NAT verified:

LAN routing verified:

DMZ routing verified:

Security policy verified:

Destination NAT verified:

Static NAT verified:

Published services verified:

Monitoring verified:

Logging verified:

VPN verified:

Configuration backup completed:

Rollback method confirmed:

---

## Known Issues

Issue:

Severity:

Affected Service:

Observed Behavior:

Workaround:

Permanent Fix:

Status:

Verification Date:

Notes:

---

## Change History

Date:

Administrator:

Change:

Reason:

Pre-Change State:

Post-Change State:

Validation Performed:

Rollback Method:

Result:

Notes:

---

## Sanitization Requirements

Before public release, remove or replace:

- Real public IP addresses
- Internal IP addresses where topology exposure is sensitive
- Hostnames
- Usernames
- Serial numbers
- Asset tags
- VPN peers
- Customer identifiers
- SNMP credentials
- SSH keys
- Authentication details
- Internal DNS names
- Monitoring destinations

Use documentation address ranges and generic identifiers in published examples.

---

## AI Guidance

When using production data:

- Prefer verified values over planned values.
- Never infer missing production values.
- Clearly identify configuration state.
- Do not expose sensitive deployment data in public output.
- Treat secrets as excluded data.
- Recommend verification commands when values are missing or stale.
- Update verification dates after successful changes.

---

## Document Status

Document Type: Production Data Template

Knowledge Base: Juniper SRX320 Knowledge Base

Version: 0.1.0

Status: Initial Build
