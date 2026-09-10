# Juniper SRX320 Basic Edge Firewall Example

## Scope

This example demonstrates a simple SRX edge firewall design with:

- WAN interface
- LAN interface
- Trust and untrust security zones
- Default route
- Source NAT
- Basic outbound security policy

This configuration is an educational example only.

It is not production configuration.

---

## Example Topology

LAN Network:

192.0.2.0/24

LAN Gateway:

192.0.2.1

WAN Network:

198.51.100.0/24

SRX WAN Address:

198.51.100.10/24

ISP Gateway:

198.51.100.1

LAN Interface:

ge-0/0/1.0

WAN Interface:

ge-0/0/0.0

LAN Zone:

trust

WAN Zone:

untrust

---

## Configure WAN Interface

set interfaces ge-0/0/0 unit 0 family inet address 198.51.100.10/24

---

## Configure LAN Interface

set interfaces ge-0/0/1 unit 0 family inet address 192.0.2.1/24

---

## Configure Security Zones

Assign WAN interface:

set security zones security-zone untrust interfaces ge-0/0/0.0

Assign LAN interface:

set security zones security-zone trust interfaces ge-0/0/1.0

---

## Allow Basic Management from LAN

Permit ping to the SRX from the trust zone:

set security zones security-zone trust interfaces ge-0/0/1.0 host-inbound-traffic system-services ping

Permit SSH from the trust zone:

set security zones security-zone trust interfaces ge-0/0/1.0 host-inbound-traffic system-services ssh

This example intentionally does not enable management access from the untrust zone.

---

## Configure Default Route

set routing-options static route 0.0.0.0/0 next-hop 198.51.100.1

---

## Configure Source NAT

Create a source NAT rule set from trust to untrust:

set security nat source rule-set TRUST-TO-INTERNET from zone trust

set security nat source rule-set TRUST-TO-INTERNET to zone untrust

Create a rule matching the LAN network:

set security nat source rule-set TRUST-TO-INTERNET rule LAN-SOURCE-NAT match source-address 192.0.2.0/24

Translate matching traffic using the WAN interface address:

set security nat source rule-set TRUST-TO-INTERNET rule LAN-SOURCE-NAT then source-nat interface

---

## Configure Outbound Security Policy

Create a policy allowing LAN clients to reach the Internet:

set security policies from-zone trust to-zone untrust policy ALLOW-INTERNET match source-address any

set security policies from-zone trust to-zone untrust policy ALLOW-INTERNET match destination-address any

set security policies from-zone trust to-zone untrust policy ALLOW-INTERNET match application any

set security policies from-zone trust to-zone untrust policy ALLOW-INTERNET then permit

---

## Review Candidate Configuration

Before committing:

show | compare

---

## Validate Configuration

Run:

commit check

Correct any errors before continuing.

---

## Safe Commit

If management connectivity could be affected:

commit confirmed

Verify connectivity before confirming the commit.

---

## Verification

After commit, verify interfaces:

show interfaces terse

Verify default route:

show route 0.0.0.0/0

Verify security zones:

show security zones

Verify security policy:

show security policies

Verify source NAT:

show security nat source rule all

Verify active sessions:

show security flow session

---

## Expected Traffic Flow

A LAN host sends traffic toward the Internet.

Expected processing:

1. Packet enters ge-0/0/1.0.
2. Source zone is trust.
3. Routing selects the default route.
4. Destination zone is untrust.
5. Source NAT rule matches.
6. Source address is translated to the WAN interface address.
7. ALLOW-INTERNET policy permits traffic.
8. A stateful session is created.
9. Traffic exits ge-0/0/0.0.
10. Return traffic follows the established session.

---

## Troubleshooting

If LAN clients cannot reach the Internet, verify:

1. LAN host default gateway
2. ge-0/0/1.0 status
3. ge-0/0/0.0 status
4. Default route
5. ISP gateway reachability
6. Security-zone assignments
7. Source NAT rule match
8. Security policy
9. Session table
10. DNS separately from IP connectivity

---

## Important Notes

This example uses documentation-only IP ranges.

Do not copy these addresses into a production network.

Do not assume:

- ge-0/0/0 is WAN
- ge-0/0/1 is LAN
- trust and untrust are the correct production zone names
- interface source NAT is appropriate for every deployment

Adapt the pattern to the actual environment.

---

## AI Guidance

When using this example:

- Treat all addresses as examples.
- Treat all interfaces as examples.
- Treat all zone names as examples.
- Verify production interfaces before generating commands.
- Verify Junos version.
- Preserve management access.
- Use commit check before activation.
- Use commit confirmed when lockout risk exists.

---

## Document Status

Document Type: Configuration Example

Example Type: Basic Edge Firewall

Knowledge Base: Juniper SRX320 Knowledge Base

Version: 0.1.0

Status: Example / Non-Production
