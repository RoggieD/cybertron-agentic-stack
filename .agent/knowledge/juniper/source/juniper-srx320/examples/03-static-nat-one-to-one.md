# Juniper SRX320 Static NAT One-to-One Example

## Scope

This example demonstrates a one-to-one static NAT mapping between a public IP address and an internal server.

It demonstrates:

- Static NAT rule set
- One-to-one address mapping
- Security policy integration
- Routing considerations
- Verification and troubleshooting

This configuration is an educational example only.

It is not production configuration.

---

## Example Topology

Public IP:

198.51.100.30

Internal Server:

192.0.2.30

WAN Zone:

untrust

Internal Zone:

trust

WAN Interface:

ge-0/0/0.0

Internal Interface:

ge-0/0/1.0

---

## Traffic Objective

Map:

198.51.100.30

to:

192.0.2.30

The mapping is intended to provide a consistent one-to-one relationship between the public and internal addresses.

---

## Create Internal Address Object

Create an address-book object for the internal server:

set security zones security-zone trust address-book address STATIC-SERVER 192.0.2.30/32

---

## Create Static NAT Rule Set

Create a static NAT rule set for traffic entering from the untrust zone:

set security nat static rule-set INTERNET-STATIC from zone untrust

---

## Create Static NAT Rule

Match the public address:

set security nat static rule-set INTERNET-STATIC rule STATIC-SERVER-MAP match destination-address 198.51.100.30/32

Translate to the internal address:

set security nat static rule-set INTERNET-STATIC rule STATIC-SERVER-MAP then static-nat prefix 192.0.2.30/32

---

## Create Security Policy

Create a policy from untrust to trust.

Example permitting HTTPS only:

set security policies from-zone untrust to-zone trust policy ALLOW-STATIC-SERVER-HTTPS match source-address any

set security policies from-zone untrust to-zone trust policy ALLOW-STATIC-SERVER-HTTPS match destination-address STATIC-SERVER

set security policies from-zone untrust to-zone trust policy ALLOW-STATIC-SERVER-HTTPS match application junos-https

set security policies from-zone untrust to-zone trust policy ALLOW-STATIC-SERVER-HTTPS then permit

---

## Optional Logging

For troubleshooting:

set security policies from-zone untrust to-zone trust policy ALLOW-STATIC-SERVER-HTTPS then log session-init

set security policies from-zone untrust to-zone trust policy ALLOW-STATIC-SERVER-HTTPS then log session-close

Use logging selectively on high-volume services.

---

## Review Candidate Configuration

Run:

show | compare

---

## Validate Configuration

Run:

commit check

Correct any reported errors before commit.

---

## Safe Commit

If remote management could be affected:

commit confirmed

Verify both management access and the published service before confirming.

---

## Verify Static NAT

Review configuration:

show configuration security nat static

Review operational rule information:

show security nat static rule all

---

## Verify Security Policy

Run:

show security policies

For more detail:

show security policies detail

---

## Verify Route to Internal Server

Run:

show route 192.0.2.30

The translated destination must be reachable through the expected internal interface.

---

## Verify Sessions

While testing:

show security flow session destination-prefix 192.0.2.30

Session information may show:

- Original public address
- Internal translated address
- Security policy
- Protocol
- Session state

---

## Expected Inbound Flow

1. External client connects to 198.51.100.30.
2. Packet enters the untrust zone.
3. Static NAT rule STATIC-SERVER-MAP matches.
4. Destination is translated to 192.0.2.30.
5. Routing identifies the internal path.
6. Destination security zone is determined.
7. Security policy permits the desired application.
8. Stateful session is created.
9. Traffic reaches the internal server.

---

## Expected Return Flow

The return traffic is associated with the existing stateful session.

The SRX maintains the address mapping for the flow.

The internal system should use a return path that is compatible with the SRX session.

---

## Static NAT vs Destination NAT

Static NAT and destination NAT are not identical.

Static NAT is commonly associated with a fixed one-to-one mapping.

Destination NAT is commonly used for:

- Port forwarding
- Service publishing
- Many-to-one or service-specific translation

Choose the NAT type based on the required behavior.

Do not select static NAT simply because a server has a public IP.

---

## Security Policy Still Required

Static NAT does not automatically permit inbound traffic.

A security policy is still required for the allowed traffic path.

Use least privilege.

If only HTTPS is required, do not automatically permit all applications.

---

## Public Address Routing

The upstream network must deliver traffic for the public IP to the SRX.

Depending on ISP design, this may involve:

- Public subnet directly connected to the SRX
- Routed public address block
- Upstream static routing
- Proxy ARP requirements
- Provider-specific behavior

Do not assume a static NAT rule alone makes the public IP reachable.

---

## Proxy ARP

Some deployments may require proxy ARP so the SRX responds for a translated public address on a directly connected Ethernet network.

Whether proxy ARP is required depends on the upstream addressing and routing design.

Do not add proxy ARP automatically.

Verify the ISP and Layer 2 topology first.

---

## Internal Server Requirements

Verify:

- Correct IP address
- Correct subnet mask
- Correct default gateway
- Required service is listening
- Host firewall permits the service
- Application is healthy
- Return traffic follows the intended path

---

## Troubleshooting Sequence

If static NAT traffic fails, verify:

1. Public IP routing
2. WAN interface
3. Static NAT rule
4. Static NAT rule match
5. Internal route
6. Security-zone assignments
7. Security policy
8. Internal server
9. Return path
10. Session table
11. Logs
12. Proxy ARP if relevant to the topology

---

## Important Notes

This example uses documentation-only IP addresses.

Do not copy these addresses into production.

Do not assume:

- ge-0/0/0 is WAN
- ge-0/0/1 is the internal interface
- trust and untrust are production zone names
- proxy ARP is required
- all services should be permitted
- the ISP delivers public addresses in the same way in every deployment

Verify actual topology first.

---

## Public Release Guidance

Published examples should use:

- Documentation address ranges
- Generic hostnames
- Generic interface roles
- Generic service names

Do not include real public IP addresses, internal hostnames, customer names, or sensitive topology.

---

## AI Guidance

When using this example:

- Treat all values as examples.
- Do not invent production public addresses.
- Verify whether static NAT is actually appropriate.
- Verify upstream routing.
- Verify proxy ARP requirements separately.
- Verify security policy separately.
- Verify return routing.
- Prefer live Junos output when diagnosing production traffic.

---

## Document Status

Document Type: Configuration Example

Example Type: Static NAT One-to-One Mapping

Knowledge Base: Juniper SRX320 Knowledge Base

Version: 0.1.0

Status: Example / Non-Production
