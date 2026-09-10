# Juniper SRX320 Destination NAT Web Server Example

## Scope

This example demonstrates publishing an internal HTTPS web server through a Juniper SRX using destination NAT.

It demonstrates:

- Destination NAT pool
- Destination NAT rule set
- HTTPS port matching
- Security address object
- Inbound security policy
- Validation and troubleshooting

This configuration is an educational example only.

It is not production configuration.

---

## Example Topology

Public IP:

198.51.100.20

Internal Web Server:

192.0.2.20

Public Service:

HTTPS TCP/443

WAN Interface:

ge-0/0/0.0

LAN Interface:

ge-0/0/1.0

WAN Zone:

untrust

LAN Zone:

trust

---

## Traffic Objective

External clients connect to:

198.51.100.20 TCP/443

The SRX translates the destination to:

192.0.2.20 TCP/443

The traffic is then permitted by a security policy from:

untrust -> trust

---

## Create Internal Server Address Object

Create an address-book object in the destination security zone:

set security zones security-zone trust address-book address WEB-SERVER 192.0.2.20/32

---

## Create Destination NAT Pool

Create a destination NAT pool pointing to the internal server:

set security nat destination pool WEB-SERVER-POOL address 192.0.2.20/32

---

## Create Destination NAT Rule Set

Create a rule set for traffic entering from the untrust zone:

set security nat destination rule-set INTERNET-INBOUND from zone untrust

---

## Create HTTPS Destination NAT Rule

Match the public IP:

set security nat destination rule-set INTERNET-INBOUND rule HTTPS-WEB match destination-address 198.51.100.20/32

Match TCP:

set security nat destination rule-set INTERNET-INBOUND rule HTTPS-WEB match protocol tcp

Match HTTPS:

set security nat destination rule-set INTERNET-INBOUND rule HTTPS-WEB match destination-port 443

Apply destination NAT:

set security nat destination rule-set INTERNET-INBOUND rule HTTPS-WEB then destination-nat pool WEB-SERVER-POOL

---

## Create Security Policy

Create a policy from untrust to trust:

set security policies from-zone untrust to-zone trust policy ALLOW-WEB-HTTPS match source-address any

Match the translated internal server object:

set security policies from-zone untrust to-zone trust policy ALLOW-WEB-HTTPS match destination-address WEB-SERVER

Match HTTPS:

set security policies from-zone untrust to-zone trust policy ALLOW-WEB-HTTPS match application junos-https

Permit the traffic:

set security policies from-zone untrust to-zone trust policy ALLOW-WEB-HTTPS then permit

---

## Optional Policy Logging

For troubleshooting or auditing, session logging may be enabled where appropriate.

Example:

set security policies from-zone untrust to-zone trust policy ALLOW-WEB-HTTPS then log session-init

set security policies from-zone untrust to-zone trust policy ALLOW-WEB-HTTPS then log session-close

Logging should be used deliberately because high-volume services can generate substantial log traffic.

---

## Review Candidate Configuration

Before commit:

show | compare

---

## Validate Configuration

Run:

commit check

Correct any configuration errors before activation.

---

## Safe Commit

If the change could affect remote administration:

commit confirmed

Verify service and management connectivity before confirming.

---

## Verify Destination NAT Configuration

Review configuration:

show configuration security nat destination

Review operational NAT rules:

show security nat destination rule all

---

## Verify Security Policy

Review policy:

show security policies

For additional detail:

show security policies detail

Where supported, policy matching may also be inspected with:

show security match-policies

---

## Verify Route to Internal Server

Run:

show route 192.0.2.20

The SRX must have a valid route to the translated destination.

---

## Verify Session Creation

While testing an inbound connection:

show security flow session destination-prefix 192.0.2.20

Session output may reveal:

- Original destination
- Translated destination
- Source address
- Policy match
- Session state

---

## Expected Traffic Flow

1. External client connects to 198.51.100.20 TCP/443.
2. Packet enters the untrust zone.
3. Destination NAT rule HTTPS-WEB matches.
4. Destination address is translated to 192.0.2.20.
5. Route lookup identifies the internal destination path.
6. Destination security zone is determined.
7. Security policy ALLOW-WEB-HTTPS permits the traffic.
8. Stateful session is created.
9. Traffic reaches 192.0.2.20 TCP/443.
10. Return traffic follows the established session.

---

## Destination NAT and Policy Lookup

Destination NAT and security policy are separate processing functions.

The NAT rule performs address translation.

The security policy provides authorization for the traffic.

A destination NAT rule does not automatically permit the connection.

For destination-NAT traffic, policy design must account for the translated destination according to Junos security-processing behavior.

---

## Server Requirements

The internal server must also be configured correctly.

Verify:

- Server is powered on
- Correct IP address
- Correct subnet mask
- Correct default gateway
- TCP/443 service is listening
- Host firewall permits HTTPS
- Application is healthy
- Return traffic passes through the SRX

---

## Return Path

The web server must return traffic through a path compatible with the SRX session.

If the server uses another gateway, asymmetric routing may occur.

Symptoms may include:

- SYN reaches server but connection fails
- One-way traffic
- Incomplete TCP handshake
- Session timeouts

---

## Troubleshooting Sequence

If HTTPS is not reachable externally, verify:

1. WAN interface state
2. Public IP routing
3. Destination NAT rule match
4. Destination NAT pool
5. Internal route
6. Destination security zone
7. Address object
8. Security policy
9. Session table
10. Internal server state
11. Internal server gateway
12. Return path
13. Logs

---

## Testing from Outside

Test the published service from a genuinely external network where possible.

Testing from inside the same network may involve different routing or NAT behavior and may not accurately represent Internet access.

---

## Important Notes

This example uses documentation-only IP ranges.

Do not copy these addresses into production.

Do not assume:

- ge-0/0/0 is WAN
- ge-0/0/1 is LAN
- untrust and trust are the production zone names
- TCP/443 is the desired published service
- the public IP is configured directly on the SRX interface
- this exact NAT design matches every ISP topology

Verify the actual deployment first.

---

## Security Guidance

Published services increase external attack surface.

Before exposing a service:

- Confirm business need
- Restrict ports
- Patch the server
- Review host firewall
- Use TLS
- Monitor the service
- Consider source restrictions where practical
- Log useful security events

Do not expose administrative interfaces merely because destination NAT makes it possible.

---

## AI Guidance

When using this example:

- Treat all addresses as examples.
- Treat interface assignments as examples.
- Treat zone names as examples.
- Do not invent production public IP addresses.
- Verify the translated destination.
- Verify routing separately.
- Verify security policy separately.
- Verify server health separately.
- Verify return routing.
- Use live Junos output when troubleshooting production traffic.

---

## Document Status

Document Type: Configuration Example

Example Type: Destination NAT HTTPS Web Server

Knowledge Base: Juniper SRX320 Knowledge Base

Version: 0.1.0

Status: Example / Non-Production
