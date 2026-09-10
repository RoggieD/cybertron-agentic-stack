# Juniper SRX320 Source NAT Pool Example

## Scope

This example demonstrates source NAT using an explicitly defined public address pool.

It demonstrates:

- Source NAT pool creation
- Source NAT rule set
- Source address matching
- Public address translation
- Security policy integration
- Verification and troubleshooting

This configuration is an educational example only.

It is not production configuration.

---

## Example Topology

Internal Network:

192.0.2.0/24

Internal Zone:

trust

External Zone:

untrust

WAN Interface:

ge-0/0/0.0

LAN Interface:

ge-0/0/1.0

Public NAT Address:

198.51.100.50

---

## Traffic Objective

Hosts on:

192.0.2.0/24

should access external networks using:

198.51.100.50

as the translated source address.

---

## Create Source NAT Pool

Create a pool containing the public address:

set security nat source pool INTERNET-SNAT-POOL address 198.51.100.50/32

---

## Create Source NAT Rule Set

Create a rule set for traffic moving from trust to untrust:

set security nat source rule-set TRUST-TO-INTERNET from zone trust

set security nat source rule-set TRUST-TO-INTERNET to zone untrust

---

## Create Source NAT Rule

Match the internal network:

set security nat source rule-set TRUST-TO-INTERNET rule TRUST-SNAT-POOL match source-address 192.0.2.0/24

Apply the source NAT pool:

set security nat source rule-set TRUST-TO-INTERNET rule TRUST-SNAT-POOL then source-nat pool INTERNET-SNAT-POOL

---

## Configure Security Policy

Allow trusted hosts outbound access:

set security policies from-zone trust to-zone untrust policy TRUST-INTERNET match source-address any

set security policies from-zone trust to-zone untrust policy TRUST-INTERNET match destination-address any

set security policies from-zone trust to-zone untrust policy TRUST-INTERNET match application any

set security policies from-zone trust to-zone untrust policy TRUST-INTERNET then permit

For production use, narrow applications where practical.

---

## Routing Requirement

The SRX must have a valid route toward the external network.

Typical designs include a default route.

Example:

set routing-options static route 0.0.0.0/0 next-hop 198.51.100.1

This is an example only.

---

## Public Address Reachability

The upstream network must deliver return traffic for:

198.51.100.50

to the SRX.

Depending on provider design, this may involve:

- Directly connected public subnet
- Routed public subnet
- Upstream static route
- Proxy ARP
- Provider-specific addressing

Do not assume the NAT pool address is usable merely because it is configured on the SRX.

---

## Proxy ARP Consideration

If the public NAT address resides on a directly connected Ethernet subnet and is not configured directly on an interface, proxy ARP may be required.

Whether proxy ARP is necessary depends on the upstream Layer 2 and routing design.

Do not configure proxy ARP automatically.

Verify the ISP topology first.

---

## Review Candidate Configuration

Run:

show | compare

---

## Validate Configuration

Run:

commit check

Correct any errors before activation.

---

## Safe Commit

If the change may affect remote access:

commit confirmed

Verify traffic before confirming the commit.

---

## Verify Source NAT Configuration

Run:

show configuration security nat source

---

## Verify Operational NAT Rules

Run:

show security nat source rule all

Verify that:

- Rule set is active
- Source match is correct
- Translation pool is correct

---

## Verify Routing

Run:

show route 0.0.0.0/0

Also verify the path to any specific test destination.

---

## Verify Security Policy

Run:

show security policies

Verify:

trust -> untrust

is permitted.

---

## Verify Sessions

Generate traffic from an internal host.

Then run:

show security flow session source-prefix 192.0.2.0/24

Look for:

- Original internal address
- Translated source address
- Security policy
- Session state

---

## Expected Traffic Flow

1. Internal host sends traffic toward the Internet.
2. Packet enters the trust zone.
3. Route lookup selects the external path.
4. Destination zone is untrust.
5. Source NAT rule TRUST-SNAT-POOL matches.
6. Source address is translated to 198.51.100.50.
7. Security policy permits traffic.
8. Stateful session is created.
9. Return traffic is translated back to the original internal host.

---

## Source NAT Pool vs Interface NAT

Interface NAT typically uses the egress interface address.

A source NAT pool uses an explicitly defined translated address or address range.

Source NAT pools may be useful when:

- Multiple public IP addresses are available
- Specific systems require a particular outbound identity
- Different internal networks require different public addresses
- Provider addressing design supports routed public pools

Use the simplest design that meets the requirement.

---

## Multiple Public Addresses

A pool may contain multiple addresses depending on the design.

When multiple addresses are used, document:

- Address range
- Purpose
- Associated internal networks
- Upstream routing
- Port allocation behavior
- Monitoring

Do not assume all systems require their own public source address.

---

## Troubleshooting Sequence

If source NAT pool traffic fails, verify:

1. Internal interface state
2. Internal host gateway
3. Source zone
4. Source NAT rule set
5. Source NAT rule match
6. NAT pool
7. Security policy
8. Default route
9. Upstream gateway
10. Public address routing
11. Proxy ARP if applicable
12. Session table
13. Return path
14. DNS separately from IP connectivity

---

## Common Problems

### Rule Does Not Match

Possible causes:

- Wrong source zone
- Wrong destination zone
- Wrong source subnet
- Rule ordering issue

### Translation Occurs but No Return Traffic

Possible causes:

- Public address not routed to SRX
- Proxy ARP requirement
- Upstream routing problem
- Asymmetric return path

### Traffic Leaves but Application Fails

Possible causes:

- DNS
- Remote service
- MTU
- Application issue
- Upstream filtering

Do not assume every failure is caused by NAT.

---

## Important Notes

This example uses documentation-only IP ranges.

Do not copy these values into production.

Do not assume:

- 198.51.100.50 belongs to the SRX
- ge-0/0/0.0 is WAN
- ge-0/0/1.0 is LAN
- trust and untrust are production zone names
- proxy ARP is required
- a source NAT pool is preferable to interface NAT

Verify the actual deployment first.

---

## Public Release Guidance

Before publishing source NAT examples:

- Replace real public addresses
- Remove internal hostnames
- Remove customer-specific networks
- Remove provider identifiers
- Replace environment-specific data with documentation values

---

## AI Guidance

When using this example:

- Treat all values as examples.
- Do not invent production public IP addresses.
- Verify public address ownership and routing.
- Verify whether proxy ARP is required.
- Verify NAT rule matching.
- Verify security policy separately.
- Verify routing separately.
- Prefer live session output during troubleshooting.

---

## Document Status

Document Type: Configuration Example

Example Type: Source NAT Pool

Knowledge Base: Juniper SRX320 Knowledge Base

Version: 0.1.0

Status: Example / Non-Production
