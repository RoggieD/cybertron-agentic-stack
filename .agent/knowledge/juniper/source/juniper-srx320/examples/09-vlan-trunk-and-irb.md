# Juniper SRX320 VLAN Trunk and Routed VLAN Interface Example

## Scope

This example explains a VLAN-based segmentation design using:

- Ethernet switching
- Access ports
- Trunk ports
- VLAN membership
- Routed VLAN interfaces
- Security zones
- Inter-VLAN policy control

This is a design and configuration-pattern example.

Exact syntax must be verified against the installed Junos release and active SRX320 switching model before production use.

---

## Example Topology

### VLAN 10

Name:

USERS

Subnet:

192.0.2.0/24

Gateway:

192.0.2.1

Security Zone:

trust

---

### VLAN 20

Name:

SERVERS

Subnet:

198.18.0.0/24

Gateway:

198.18.0.1

Security Zone:

servers

---

### VLAN 30

Name:

GUEST

Subnet:

203.0.113.0/24

Gateway:

203.0.113.1

Security Zone:

guest

---

## Design Objective

Provide Layer 2 segmentation between:

- Users
- Servers
- Guests

Each VLAN has a Layer 3 gateway on the SRX.

Security policy controls traffic between VLANs because each routed VLAN interface belongs to a security zone.

---

## Access Port Concept

An access port carries traffic for one VLAN.

Example intent:

ge-0/0/3

belongs to:

VLAN 10 USERS

An endpoint connected to that port sends ordinary untagged Ethernet frames.

The switch function associates that traffic with VLAN 10.

---

## Trunk Port Concept

A trunk port carries multiple VLANs using VLAN tags.

Example intent:

ge-0/0/4

carries:

VLAN 10

VLAN 20

VLAN 30

Typical use cases include connectivity to:

- Managed switch
- Hypervisor
- Wireless access point
- Another VLAN-aware device

---

## VLAN Definitions

The VLAN database should clearly define:

- VLAN name
- VLAN ID
- Routed interface
- Member interfaces

Conceptually:

USERS -> VLAN 10

SERVERS -> VLAN 20

GUEST -> VLAN 30

Exact Junos hierarchy should be verified before implementation.

---

## Routed VLAN Interface

A routed VLAN interface provides Layer 3 gateway functionality for a VLAN.

On Junos platforms, this may use an integrated routing and bridging interface.

Common conceptual naming includes:

irb.10

irb.20

irb.30

Example design:

irb.10 -> 192.0.2.1/24

irb.20 -> 198.18.0.1/24

irb.30 -> 203.0.113.1/24

Do not assume IRB syntax is identical across all SRX320 Junos releases.

---

## Security Zone Assignment

Each routed VLAN interface may be assigned to a security zone.

Example:

irb.10 -> trust

irb.20 -> servers

irb.30 -> guest

This creates security boundaries between the VLANs.

---

## Inter-VLAN Routing

Because the SRX owns the Layer 3 gateway for each VLAN, traffic between VLANs is routed by the SRX.

Routing alone does not imply permission.

Security policy must permit the inter-zone traffic.

---

## Example Users-to-Servers Policy

Example objective:

Allow users to reach an HTTPS application on the server network.

Conceptually:

trust -> servers

Source:

192.0.2.0/24

Destination:

198.18.0.20

Application:

HTTPS

Action:

permit

Production policy should use specific address objects and applications.

---

## Example Guest Policy

Guest traffic should generally be isolated from trusted internal resources.

Example objective:

guest -> untrust

Permit Internet access.

guest -> trust

Deny unless there is a specific requirement.

guest -> servers

Deny unless there is a specific requirement.

---

## DHCP Considerations

DHCP may be provided by:

- SRX
- Windows Server
- Dedicated DHCP server
- Another network service

If DHCP server resides on another subnet, relay may be required.

Do not assume the SRX itself should provide DHCP.

---

## DNS Considerations

Each VLAN may use:

- Internal DNS
- Public DNS
- Dedicated DNS policy

Guest networks may intentionally use different resolvers than trusted networks.

DNS design should align with segmentation goals.

---

## Trunk Verification

When a VLAN appears unreachable, verify:

1. Physical link
2. Trunk status
3. VLAN allowed on trunk
4. VLAN ID
5. Access-port membership
6. Routed VLAN interface
7. IP addressing
8. Security zone
9. Security policy
10. Host gateway

---

## Common VLAN Failure Causes

Possible causes include:

- Wrong VLAN ID
- VLAN missing from trunk
- Access port assigned to wrong VLAN
- Native VLAN mismatch
- Missing routed interface
- Wrong gateway address
- Wrong security zone
- Missing policy
- Incorrect endpoint addressing

---

## Native VLAN

Some trunk designs use a native or untagged VLAN.

Native VLAN behavior must match on both ends of the trunk.

Mismatch can cause:

- Unexpected untagged traffic placement
- Management loss
- Connectivity problems
- Security exposure

Do not configure a native VLAN without a clear design requirement.

---

## Hypervisor Trunks

A trunk connected to a hypervisor may carry multiple VLANs.

Document:

- Physical SRX port
- Switch port
- Hypervisor port
- VLAN IDs
- Virtual switch
- VM networks

Avoid undocumented VLAN mappings.

---

## Wireless Access Point Trunks

An access point may map SSIDs to VLANs.

Example:

CORPORATE SSID -> VLAN 10

GUEST SSID -> VLAN 30

The SRX then applies different policy to each security zone.

---

## Management VLAN

A dedicated management VLAN may be used for:

- Switches
- Hypervisors
- Access points
- Network appliances
- Administrative interfaces

Management networks should receive restrictive policy.

---

## Internet Access

Each VLAN requiring Internet access may need:

- Route
- Security policy
- Source NAT

Example paths:

trust -> untrust

servers -> untrust

guest -> untrust

Do not assume one NAT rule or policy automatically covers all security zones.

---

## Security Design

VLANs provide segmentation at Layer 2.

Security zones and policies provide Layer 3/4 access control.

A VLAN alone is not a firewall boundary.

Use both mechanisms intentionally.

---

## Verification Commands

Depending on Junos release and switching mode, useful commands may include:

show interfaces terse

show configuration interfaces

show configuration vlans

show ethernet-switching table

show security zones

show security policies

Exact command availability may vary.

---

## Troubleshooting Sequence

If a host cannot reach another VLAN:

1. Verify host IP
2. Verify subnet mask
3. Verify default gateway
4. Verify access VLAN
5. Verify trunk VLAN membership
6. Verify routed VLAN interface
7. Verify route
8. Verify security zone
9. Verify security policy
10. Verify destination host
11. Verify host firewall
12. Verify return path

---

## Important Notes

This example is intentionally version-aware.

Do not assume:

- IRB is configured the same way on every Junos release
- ge-0/0/3 is an access port
- ge-0/0/4 is a trunk port
- VLAN IDs 10, 20, and 30 are appropriate
- trust, servers, and guest are production zone names
- SRX should perform switching in every architecture

Verify installed Junos version and intended switching model before generating production commands.

---

## Public Release Guidance

Before publishing VLAN examples:

- Remove real VLAN IDs when sensitive
- Remove internal subnets
- Remove switch names
- Remove hypervisor names
- Remove SSID names
- Replace environment-specific values with generic examples

---

## AI Guidance

When using this example:

- Treat all VLAN IDs as examples.
- Treat all interfaces as examples.
- Verify Junos version before generating switching syntax.
- Verify whether IRB is used in the target design.
- Verify access vs trunk mode.
- Verify security zones separately from VLAN membership.
- Verify security policy separately from routing.
- Do not assume VLAN segmentation alone provides firewall isolation.

---

## Document Status

Document Type: Design Example

Example Type: VLAN Trunk and Routed VLAN Interface

Knowledge Base: Juniper SRX320 Knowledge Base

Version: 0.1.0

Status: Example / Non-Production
