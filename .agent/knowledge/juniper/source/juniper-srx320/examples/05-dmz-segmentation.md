# Juniper SRX320 DMZ Segmentation Example

## Scope

This example demonstrates a basic three-zone firewall design using:

- trust
- dmz
- untrust

It demonstrates:

- Separate routed interfaces
- Security-zone assignment
- Inter-zone policy control
- Limited inbound access to a DMZ server
- Controlled DMZ-to-trust access
- Internet access from the DMZ
- Source NAT
- Verification and troubleshooting

This configuration is an educational example only.

It is not production configuration.

---

## Example Topology

### Trust Network

Network:

192.0.2.0/24

Gateway:

192.0.2.1

Interface:

ge-0/0/1.0

Zone:

trust

---

### DMZ Network

Network:

198.18.0.0/24

Gateway:

198.18.0.1

Interface:

ge-0/0/2.0

Zone:

dmz

Example Web Server:

198.18.0.20

---

### Untrust Network

WAN Address:

198.51.100.10/24

ISP Gateway:

198.51.100.1

Interface:

ge-0/0/0.0

Zone:

untrust

---

## Security Objective

The example intends to permit:

- trust -> untrust for Internet access
- trust -> dmz for administration or application access
- untrust -> dmz only for specific published services
- dmz -> untrust for updates and outbound services
- dmz -> trust only when explicitly required

The DMZ should not be treated as equivalent to the trusted LAN.

---

## Configure Interfaces

WAN:

set interfaces ge-0/0/0 unit 0 family inet address 198.51.100.10/24

Trust:

set interfaces ge-0/0/1 unit 0 family inet address 192.0.2.1/24

DMZ:

set interfaces ge-0/0/2 unit 0 family inet address 198.18.0.1/24

---

## Configure Security Zones

WAN:

set security zones security-zone untrust interfaces ge-0/0/0.0

Trust:

set security zones security-zone trust interfaces ge-0/0/1.0

DMZ:

set security zones security-zone dmz interfaces ge-0/0/2.0

---

## Allow Management from Trust

Permit ping:

set security zones security-zone trust interfaces ge-0/0/1.0 host-inbound-traffic system-services ping

Permit SSH:

set security zones security-zone trust interfaces ge-0/0/1.0 host-inbound-traffic system-services ssh

This example does not enable administrative management from the DMZ or untrust zones.

---

## Configure Default Route

set routing-options static route 0.0.0.0/0 next-hop 198.51.100.1

---

## Create DMZ Address Object

Create an address object for the example web server:

set security zones security-zone dmz address-book address DMZ-WEB-SERVER 198.18.0.20/32

---

## Trust to Internet Policy

Allow trusted clients to access the Internet:

set security policies from-zone trust to-zone untrust policy TRUST-INTERNET match source-address any

set security policies from-zone trust to-zone untrust policy TRUST-INTERNET match destination-address any

set security policies from-zone trust to-zone untrust policy TRUST-INTERNET match application any

set security policies from-zone trust to-zone untrust policy TRUST-INTERNET then permit

---

## Trust Source NAT

Create source NAT for the trust network:

set security nat source rule-set TRUST-TO-INTERNET from zone trust

set security nat source rule-set TRUST-TO-INTERNET to zone untrust

set security nat source rule-set TRUST-TO-INTERNET rule TRUST-SNAT match source-address 192.0.2.0/24

set security nat source rule-set TRUST-TO-INTERNET rule TRUST-SNAT then source-nat interface

---

## DMZ to Internet Policy

Permit DMZ systems to reach the Internet:

set security policies from-zone dmz to-zone untrust policy DMZ-INTERNET match source-address any

set security policies from-zone dmz to-zone untrust policy DMZ-INTERNET match destination-address any

set security policies from-zone dmz to-zone untrust policy DMZ-INTERNET match application any

set security policies from-zone dmz to-zone untrust policy DMZ-INTERNET then permit

For production use, narrow applications where practical.

---

## DMZ Source NAT

Create source NAT for the DMZ network:

set security nat source rule-set DMZ-TO-INTERNET from zone dmz

set security nat source rule-set DMZ-TO-INTERNET to zone untrust

set security nat source rule-set DMZ-TO-INTERNET rule DMZ-SNAT match source-address 198.18.0.0/24

set security nat source rule-set DMZ-TO-INTERNET rule DMZ-SNAT then source-nat interface

---

## Trust to DMZ Policy

Permit trusted administrators to reach the DMZ web server using SSH:

set security policies from-zone trust to-zone dmz policy TRUST-TO-DMZ-SSH match source-address any

set security policies from-zone trust to-zone dmz policy TRUST-TO-DMZ-SSH match destination-address DMZ-WEB-SERVER

set security policies from-zone trust to-zone dmz policy TRUST-TO-DMZ-SSH match application junos-ssh

set security policies from-zone trust to-zone dmz policy TRUST-TO-DMZ-SSH then permit

In production, replace source-address any with a dedicated administrative source where practical.

---

## DMZ to Trust Policy

Do not create broad DMZ-to-trust access by default.

If a DMZ server requires access to a trusted internal service, create a specific policy.

Example concept:

DMZ-WEB-SERVER -> internal database TCP/5432

Such a policy should explicitly define:

- Source host
- Destination host
- Application
- Business purpose

Do not permit:

dmz -> trust application any

unless there is a specific justified requirement.

---

## Publish HTTPS Service to DMZ

Example public IP:

198.51.100.20

Create destination NAT pool:

set security nat destination pool DMZ-WEB-POOL address 198.18.0.20/32

Create rule set:

set security nat destination rule-set INTERNET-TO-DMZ from zone untrust

Match public IP:

set security nat destination rule-set INTERNET-TO-DMZ rule DMZ-HTTPS match destination-address 198.51.100.20/32

Match protocol:

set security nat destination rule-set INTERNET-TO-DMZ rule DMZ-HTTPS match protocol tcp

Match HTTPS:

set security nat destination rule-set INTERNET-TO-DMZ rule DMZ-HTTPS match destination-port 443

Apply destination NAT:

set security nat destination rule-set INTERNET-TO-DMZ rule DMZ-HTTPS then destination-nat pool DMZ-WEB-POOL

---

## Untrust to DMZ Security Policy

Permit only HTTPS to the translated DMZ server:

set security policies from-zone untrust to-zone dmz policy INTERNET-TO-DMZ-HTTPS match source-address any

set security policies from-zone untrust to-zone dmz policy INTERNET-TO-DMZ-HTTPS match destination-address DMZ-WEB-SERVER

set security policies from-zone untrust to-zone dmz policy INTERNET-TO-DMZ-HTTPS match application junos-https

set security policies from-zone untrust to-zone dmz policy INTERNET-TO-DMZ-HTTPS then permit

---

## Optional Logging

Enable session logging if operationally useful:

set security policies from-zone untrust to-zone dmz policy INTERNET-TO-DMZ-HTTPS then log session-init

set security policies from-zone untrust to-zone dmz policy INTERNET-TO-DMZ-HTTPS then log session-close

Use logging selectively for high-volume services.

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

If remote access could be affected:

commit confirmed

Verify all required traffic paths before confirming.

---

## Verification

Verify interfaces:

show interfaces terse

Verify zones:

show security zones

Verify routing:

show route

Verify security policies:

show security policies

Verify NAT:

show configuration security nat

Verify sessions:

show security flow session

---

## Expected Traffic Behavior

### Trust to Internet

Expected:

- Route through WAN
- Source NAT
- trust -> untrust permit policy

### Trust to DMZ

Expected:

- Directly connected routing
- trust -> dmz security policy
- No NAT normally required

### DMZ to Internet

Expected:

- Default route
- Source NAT
- dmz -> untrust policy

### Internet to DMZ

Expected:

- Destination NAT
- untrust -> dmz security policy
- Stateful session
- Return traffic through SRX

### DMZ to Trust

Expected:

Denied unless an explicit policy permits the required traffic.

---

## Segmentation Principle

The purpose of the DMZ is to reduce trust.

A compromised DMZ host should not automatically gain broad access to trusted internal networks.

Use:

- Separate zone
- Specific policies
- Minimal services
- Monitoring
- Logging
- Host security

Segmentation is only effective when policy remains restrictive.

---

## Troubleshooting

If DMZ traffic fails, verify:

1. Interface state
2. IP addressing
3. Zone assignment
4. Route
5. NAT if required
6. Policy direction
7. Address object
8. Application
9. Session table
10. Server default gateway
11. Server host firewall
12. Return path
13. Logs

---

## Important Notes

This example uses reserved non-production example address ranges.

The public-facing addresses use documentation ranges, while the DMZ example uses a benchmarking/test range.

Do not copy these values directly into production.

Do not assume:

- ge-0/0/0 is WAN
- ge-0/0/1 is trust
- ge-0/0/2 is DMZ
- trust, dmz, and untrust are the correct production zone names
- all DMZ hosts should receive Internet access
- all trusted hosts should administer the DMZ
- destination NAT is required for every DMZ service

Adapt the pattern to the actual environment.

---

## Security Guidance

For production DMZ design:

- Minimize DMZ-to-trust access
- Limit inbound services
- Patch DMZ systems
- Monitor published services
- Restrict administration
- Log important policy events
- Separate management traffic where practical
- Review exposed services regularly

---

## AI Guidance

When using this example:

- Treat all values as examples.
- Do not assume DMZ topology.
- Do not invent production interface assignments.
- Do not create broad DMZ-to-trust policies without justification.
- Verify NAT separately.
- Verify security policy separately.
- Verify return routing.
- Prefer live Junos output when troubleshooting.

---

## Document Status

Document Type: Configuration Example

Example Type: DMZ Segmentation

Knowledge Base: Juniper SRX320 Knowledge Base

Version: 0.1.0

Status: Example / Non-Production
