# Juniper SRX320 Troubleshooting Published Services

## Scope

This document provides a structured troubleshooting workflow for externally published services behind a Juniper SRX320.

It applies to services using:

- Destination NAT
- Static NAT
- Security policies
- Public IP routing
- Internal servers
- Stateful sessions

Examples include:

- HTTPS
- SMTP
- SSH
- Custom TCP services
- Custom UDP services

This is a troubleshooting methodology example.

It is not production configuration.

---

## Primary Principle

Do not change NAT or security policy first.

Identify the failure domain.

A published service depends on multiple layers:

1. Public DNS if used
2. Public IP routing
3. WAN interface
4. NAT rule
5. Security policy
6. Internal route
7. Internal server
8. Return path
9. Application
10. Session state

Each layer should be verified independently.

---

## Example Service

Public Address:

198.51.100.20

Public Port:

443

Protocol:

TCP

Internal Server:

192.0.2.20

Internal Port:

443

External Zone:

untrust

Internal Zone:

trust

This example uses documentation-only addresses.

---

## Step 1 — Define the Failure

Record the exact symptom.

Examples:

- Connection timeout
- Connection refused
- TLS handshake failure
- Service reachable internally but not externally
- Service works from some locations only
- NAT counter does not increment
- Security policy does not match

Avoid vague descriptions such as:

"The firewall is blocking it."

---

## Step 2 — Confirm DNS Separately

If a hostname is used, resolve it.

Verify that the public DNS record points to the expected public IP.

A DNS problem is not a NAT problem.

Test the public IP directly when appropriate.

---

## Step 3 — Test from a Real External Network

Use a genuinely external source where practical.

Internal testing may behave differently because of:

- Routing
- NAT reflection
- Split DNS
- Internal address resolution
- Different security policy

External validation should reflect the actual client path.

---

## Step 4 — Verify Public Routing

Confirm that traffic for the public IP is expected to reach the SRX.

Possible delivery models include:

- Address configured on WAN subnet
- Routed public subnet
- Static route from ISP
- Proxy ARP on directly connected subnet

If the provider does not deliver the public IP to the SRX, NAT configuration cannot fix the problem.

---

## Step 5 — Verify WAN Interface

Run:

show interfaces terse

Verify:

- Expected WAN interface is up
- Logical unit exists
- Expected address is present if applicable

For more detail:

show interfaces <wan-interface>

---

## Step 6 — Verify Destination NAT

Run:

show configuration security nat destination

Then:

show security nat destination rule all

Verify:

- Correct rule set
- Correct incoming scope
- Correct public destination
- Correct protocol
- Correct destination port
- Correct NAT pool
- Correct rule order

---

## Step 7 — Verify Static NAT if Used

If static NAT is used instead of destination NAT:

show configuration security nat static

show security nat static rule all

Do not troubleshoot both NAT types unless both are actually present.

---

## Step 8 — Verify Internal Route

Run:

show route 192.0.2.20

Confirm:

- Route exists
- Correct egress interface
- Correct destination zone
- No unexpected more-specific route

---

## Step 9 — Verify Security Zone

Run:

show configuration security zones

Confirm:

- Incoming interface belongs to expected external zone
- Internal interface belongs to expected destination zone

Do not assume zone assignments.

---

## Step 10 — Verify Security Policy

Run:

show security policies

For more detail:

show security policies detail

Use show security match-policies with the actual flow criteria where appropriate.

Example pattern:

show security match-policies from-zone <source-zone> to-zone <destination-zone> source-ip <source-ip> destination-ip <destination-ip> source-port <source-port> destination-port <destination-port> protocol <protocol>

Verify:

- Source zone
- Destination zone
- Source address
- Destination address
- Application
- Action
- Rule ordering

Use values from the real flow. Do not invent placeholders during production troubleshooting.

---

## Step 11 — Understand Translated Destination

For destination NAT traffic, security policy evaluation must account for the translated internal destination according to Junos processing behavior.

Verify that the policy destination object represents the correct internal server or subnet.

Do not blindly match the public address in the security policy.

---

## Step 12 — Verify Session Table

During an external connection attempt:

show security flow session destination-prefix 192.0.2.20

Also inspect:

show security flow session

Look for:

- External source
- Original destination
- Translated destination
- Policy
- Session state
- Return traffic

---

## Step 13 — Interpret Session Evidence

### No Session

Possible causes:

- Public routing failure
- NAT rule not matching
- Security policy deny
- Traffic never reaches SRX

### Session Exists but No Return Traffic

Possible causes:

- Internal server down
- Wrong server gateway
- Host firewall
- Application not listening
- Return routing problem

### Session Has Bidirectional Traffic but Application Fails

Possible causes:

- Application problem
- TLS failure
- Protocol mismatch
- Backend failure

---

## Step 14 — Verify Internal Server Reachability

From an appropriate internal source or from the SRX where supported, verify the server is reachable.

Check:

- IP address
- Subnet mask
- Default gateway
- Service port
- Host firewall
- Application state

The firewall cannot make a stopped application respond.

---

## Step 15 — Verify Service Is Listening

On the internal server, verify that the application is actually listening on the expected port.

Examples on Linux may include:

ss -lntp

or:

ss -lnup

The exact host command depends on the operating system.

---

## Step 16 — Verify Host Firewall

The internal server may have its own firewall.

Examples include:

- nftables
- iptables
- firewalld
- Windows Defender Firewall
- Application-specific ACL

A correct SRX configuration can still fail because the server rejects traffic.

---

## Step 17 — Verify Default Gateway

The internal server should normally return traffic through a path compatible with the SRX session.

If the server uses another gateway, asymmetric routing may occur.

Symptoms may include:

- SYN reaches server
- SYN-ACK leaves through another router
- External connection times out
- SRX sees only one direction

---

## Step 18 — Verify Return Route

Check the network path from the internal server back toward the external client.

Consider:

- Default gateway
- Static routes
- Multiple routers
- Multiple firewalls
- Policy routing
- Multiple WAN connections

Stateful firewalls depend on coherent session paths.

---

## Step 19 — Review Logs

Run:

show log messages

If security policy logging is enabled, review the relevant policy events.

Look for:

- Denies
- Session activity
- Interface changes
- Errors
- Unexpected resets

---

## Step 20 — Packet Capture

If the problem remains unclear, use a narrowly scoped packet capture.

Filter by:

- External source
- Public destination
- Internal destination
- Protocol
- Port

Avoid broad captures on busy production systems.

---

## Step 21 — Flow Trace

Junos flow tracing may reveal:

- NAT rule evaluation
- Policy evaluation
- Routing
- Session creation
- Packet drops

Flow tracing can affect system performance and may increase security risk.

Juniper recommends using tracing under JTAC guidance.

If tracing is used:

- Keep filters narrowly scoped
- Limit the duration
- Collect only the required evidence
- Disable tracing immediately after troubleshooting

Do not enable broad flow tracing casually in production.

---

## Common Failure Patterns

### Public IP Unreachable

Likely areas:

- ISP routing
- WAN addressing
- Proxy ARP
- Upstream route

### NAT Rule Counter Never Increments

Likely areas:

- Wrong incoming zone
- Wrong public IP
- Wrong port
- Wrong protocol
- Rule order
- Traffic never reaches SRX

### NAT Matches but Policy Does Not

Likely areas:

- Wrong destination zone
- Wrong translated destination object
- Wrong application
- Policy order

### Policy Matches but Server Never Responds

Likely areas:

- Server offline
- Host firewall
- Wrong service port
- Wrong gateway
- Return routing

### TCP Connects but TLS Fails

Likely areas:

- Certificate
- TLS configuration
- Reverse proxy
- Application
- SNI or hostname behavior

Do not change firewall policy to fix an application-layer TLS problem.

---

## Change Discipline

Only make a configuration change when evidence identifies a likely cause.

Before change:

show | compare

Then:

commit check

Use:

commit confirmed

when management connectivity could be affected.

Make one controlled change at a time.

---

## Validation After Fix

After resolving the issue, verify:

- External DNS
- External connectivity
- NAT rule
- Security policy
- Session state
- Internal service
- Return path
- Logging
- Monitoring

Document the root cause.

---

## Incident Record

Recommended fields:

Date:

Public Service:

Public Address:

Public Port:

Protocol:

Internal Server:

Internal Port:

Observed Symptom:

NAT Result:

Policy Result:

Routing Result:

Server Result:

Root Cause:

Change Made:

Validation:

Rollback Method:

Configuration State:

Notes:

---

## Important Notes

Do not assume every published-service failure is caused by the SRX.

The fault may exist in:

- DNS
- ISP
- Upstream routing
- NAT
- Policy
- Internal routing
- Server firewall
- Application
- TLS
- Return path

Troubleshoot the full path.

---

## Public Release Guidance

Before publishing troubleshooting examples:

- Remove real public IPs
- Remove internal IPs
- Remove hostnames
- Remove customer identifiers
- Remove packet captures containing sensitive data
- Remove credentials
- Replace environment-specific values with documentation examples

---

## AI Guidance

When using this document:

- Do not change NAT or security policy before gathering evidence.
- Distinguish DNS, routing, NAT, policy, host, and application failures.
- Prefer read-only commands first.
- Verify translated destination.
- Verify session state.
- Verify return traffic.
- Do not invent production topology.
- Recommend one controlled change at a time.
- Preserve rollback capability.

---

## Document Status

Document Type: Troubleshooting Example

Example Type: Published Service Troubleshooting

Knowledge Base: Juniper SRX320 Knowledge Base

Version: 0.1.0

Status: Example / Non-Production
