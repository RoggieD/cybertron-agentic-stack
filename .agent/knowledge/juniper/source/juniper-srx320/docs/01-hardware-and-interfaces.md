# Juniper SRX320 Hardware and Interfaces

## Scope

This document describes SRX320 hardware and interface concepts used throughout the knowledge base.

It provides platform-level guidance and does not define a specific production interface assignment unless explicitly labeled.

---

## Platform Role

The Juniper SRX320 is a branch-class security gateway designed to provide:

- Stateful firewalling
- Routing
- Network Address Translation
- VPN services
- Interface and VLAN segmentation
- Security policy enforcement
- Monitoring and logging
- Administrative access

The SRX320 may be deployed as:

- Internet edge firewall
- Branch firewall
- VPN gateway
- Internal segmentation firewall
- Routing and security gateway

---

## Interface Naming

Junos uses structured interface names.

Common Ethernet interface naming includes:

ge-0/0/0
ge-0/0/1
ge-0/0/2

The interface name identifies:

- Interface type
- FPC
- PIC
- Port

A logical unit is appended after a period.

Example:

ge-0/0/0.0

The physical interface and logical interface are not the same configuration object.

Physical interface:

ge-0/0/0

Logical unit:

ge-0/0/0.0

---

## Physical and Logical Interfaces

Junos separates physical interface properties from logical interface configuration.

Physical interface configuration may include:

- Link settings
- MTU
- Description
- Speed and duplex behavior
- Ethernet options

Logical interface units may include:

- IPv4 addressing
- IPv6 addressing
- VLAN identifiers where applicable
- Routing family
- Switching family
- Security-zone membership

VLAN tagging behavior may involve physical-interface and logical-unit configuration depending on the interface design and Junos feature being used.

---

## Routed Interfaces

A routed interface typically uses:

family inet

for IPv4.

Example structure:

interfaces {
    ge-0/0/0 {
        unit 0 {
            family inet {
                address 192.0.2.1/24;
            }
        }
    }
}

This is an example only.

It is not a production configuration.

---

## IPv6 Interfaces

IPv6 commonly uses:

family inet6

Example structure:

interfaces {
    ge-0/0/0 {
        unit 0 {
            family inet6 {
                address 2001:db8::1/64;
            }
        }
    }
}

This is an example only.

---

## Ethernet Switching

SRX interfaces may be configured for Ethernet switching depending on Junos version and platform configuration.

Switching-related interface configuration may use:

family ethernet-switching

Common use cases include:

- Access ports
- VLAN membership
- Internal switched LAN segments

Switching behavior must be verified against the installed Junos version and active device configuration.

---

## VLANs

VLANs provide Layer 2 segmentation.

A VLAN configuration may include:

- VLAN name
- VLAN ID
- Member interfaces
- Routed VLAN interface
- Security zone assignment

Do not assume a VLAN is routed simply because it exists.

Layer 2 membership and Layer 3 routing are separate functions.

---

## Interface Descriptions

Interface descriptions should be used whenever practical.

Good descriptions identify the connected device or function.

Examples:

WAN_TO_ISP

LAN_CORE_SWITCH

DMZ_SWITCH

MGMT_NETWORK

Descriptions improve:

- Troubleshooting
- Change control
- Configuration review
- AI retrieval accuracy

---

## Interface Status Verification

Useful operational commands include:

show interfaces terse

show interfaces

show interfaces extensive

show interfaces ge-0/0/0

These commands may help verify:

- Administrative state
- Link state
- Logical units
- IP addressing
- Traffic counters
- Errors
- Negotiated link parameters

---

## Interface Troubleshooting

When troubleshooting an interface, verify:

1. Physical link state
2. Administrative state
3. Logical unit configuration
4. IP addressing
5. VLAN membership
6. Routing
7. Security-zone assignment
8. Security policy
9. NAT behavior
10. Error counters

Do not jump directly to firewall policy troubleshooting before verifying basic interface state.

---

## Security Zone Relationship

A routed interface typically participates in SRX security processing through security-zone assignment.

An interface may be technically up and routed while traffic still fails because:

- It is in the wrong security zone
- It is not assigned to a security zone
- No policy permits the traffic
- NAT is incorrect
- Routing is incorrect

Interface troubleshooting must therefore include security context.

---

## Host-Inbound and Management Access

Traffic destined to the SRX itself may be permitted selectively on security zones or specific interfaces using host-inbound configuration.

Examples of supported host-inbound system services include:

- ssh
- https
- ping
- snmp
- dhcp
- dns

SSH and HTTPS are commonly associated with administrative access.

Other host-inbound services, such as DHCP or DNS, may serve operational functions and should not automatically be treated as management services.

Only required host-inbound services should be enabled.

Internet-facing interfaces should use restrictive host-inbound access.

---

## Loopback Interfaces

Loopback interfaces may be used for:

- Stable management addressing
- Routing protocol identifiers
- Monitoring
- VPN endpoints
- Service binding

Common Junos loopback interface name:

lo0

A loopback address is independent of the operational state of a specific physical Ethernet port.

---

## Interface Addressing Principles

When documenting interface addressing:

- Record CIDR notation
- Identify subnet role
- Identify security zone
- Identify connected device or network
- Identify whether the address is static or dynamic
- Identify whether NAT applies
- Identify whether the interface is production, target, or legacy

---

## Production Interface Mapping

Production interface assignments must not be inferred.

The following must be verified directly from the SRX320:

- WAN interface
- LAN interface
- DMZ interface
- Management interface
- VLAN trunks
- Access ports
- Logical units
- IP addresses
- Zone assignments

Until verified, these values should remain undocumented or labeled as SRX320_TARGET.

---

## Recommended Verification Commands

Use the following commands when building the production interface map:

show interfaces terse

show configuration interfaces

show configuration security zones

show route

show ethernet-switching table

Availability and output may vary depending on Junos version and interface mode.

---

## AI Guidance

When using this document:

- Do not invent interface assignments.
- Do not assume ge-0/0/0 is WAN.
- Do not assume ge-0/0/1 is LAN.
- Distinguish physical interfaces from logical units.
- Verify zone membership before diagnosing policy behavior.
- Treat examples as examples unless explicitly marked verified.
- Prefer live configuration output over assumptions.

---

## Document Status

Document Type: Hardware and Interfaces

Knowledge Base: Juniper SRX320 Knowledge Base

Version: 0.1.0

Status: Initial Build
