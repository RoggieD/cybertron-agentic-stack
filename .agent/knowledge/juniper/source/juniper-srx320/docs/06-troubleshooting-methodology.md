# Juniper SRX320 Troubleshooting Methodology

## Scope

This document defines a structured troubleshooting process for the Juniper SRX320.

It is intended for:

- AI-assisted troubleshooting
- Production incident response
- Firewall migration validation
- Configuration debugging
- Connectivity troubleshooting
- NAT troubleshooting
- Security policy troubleshooting
- Routing troubleshooting
- Management access troubleshooting

This methodology should be used before making configuration changes whenever practical.

---

## Core Principle

Diagnose before changing.

The troubleshooting process should separate the problem into layers and verify each layer with evidence.

Avoid changing multiple subsystems simultaneously.

A controlled troubleshooting process should:

1. Define the symptom.
2. Identify the affected traffic path.
3. Verify physical and interface state.
4. Verify addressing.
5. Verify routing.
6. Verify security zones.
7. Verify NAT.
8. Verify security policy.
9. Verify session state.
10. Review logs.
11. Make one controlled change.
12. Test the result.
13. Preserve rollback options.
14. Document the outcome.

---

## Step 1 — Define the Symptom

Clearly define what is failing.

Examples:

- Host cannot reach Internet
- Published service is unreachable
- Ping succeeds but application fails
- SSH to SRX fails
- Traffic works in one direction only
- NAT rule does not appear to match
- Security policy does not appear to match
- Route exists but traffic does not pass

Avoid vague descriptions such as:

"The firewall is broken."

---

## Step 2 — Define the Traffic Flow

Identify:

- Source IP
- Source interface
- Source zone
- Destination IP
- Destination interface
- Destination zone
- Protocol
- Source port if relevant
- Destination port
- Expected NAT behavior
- Expected route
- Expected security policy

The complete traffic path should be understood before changing configuration.

---

## Step 3 — Verify Interface State

Useful commands may include:

show interfaces terse

show interfaces <interface>

show interfaces extensive

Verify:

- Physical link state
- Administrative state
- Logical unit
- IP address
- Interface errors
- VLAN configuration
- Link speed where relevant

---

## Step 4 — Verify Addressing

Confirm:

- Source subnet
- Destination subnet
- Interface IP
- Prefix length
- Default gateway
- Public address when applicable
- Translated address when applicable

Do not assume an IP address or prefix is correct because it appears familiar.

---

## Step 5 — Verify Routing

Useful commands may include:

show route <destination>

show route 0.0.0.0/0

show route protocol static

show route forwarding-table

Verify:

- Active route
- Next hop
- Outgoing interface
- Route preference
- Routing instance
- Return route

---

## Step 6 — Verify Security Zones

Useful commands may include:

show configuration security zones

show security zones

Confirm:

- Source interface zone
- Destination interface zone
- Host-inbound settings when traffic terminates on the SRX

Do not assume interface roles from physical port numbers.

---

## Step 7 — Verify NAT

Useful commands may include:

show configuration security nat

show security nat source rule all

show security nat destination rule all

show security nat static rule all

Verify:

- Correct NAT type
- Rule-set scope
- Rule ordering
- Address match
- Protocol match
- Port match
- Translation pool
- Translated destination or source

---

## Step 8 — Verify Security Policy

Useful commands may include:

show security policies

show security policies detail

Use show security match-policies with the actual flow criteria where appropriate. Supply source and destination zones, source and destination IP addresses, ports, and protocol as applicable.

Verify:

- Source zone
- Destination zone
- Source address
- Destination address
- Application
- Action
- Policy ordering

Remember that NAT and policy evaluation may use different address states depending on the traffic path.

---

## Step 9 — Verify Session State

Useful commands may include:

show security flow session

show security flow session source-prefix <address>

show security flow session destination-prefix <address>

Session information may reveal:

- Policy match
- NAT translation
- Source and destination
- Traffic direction
- Session state

Existing sessions may need to be considered after policy or NAT changes.

Do not clear sessions unnecessarily.

---

## Step 10 — Review Logs

Useful commands may include:

show log messages

Policy-specific logs may also be available when logging is enabled.

Look for:

- Denied traffic
- Interface transitions
- Authentication failure
- Commit errors
- Routing events
- System alarms
- Service failures

Logs should be treated as evidence.

---

## Step 11 — Test from the SRX

Testing directly from the SRX can help isolate the failure domain.

Useful commands may include:

ping <destination>

traceroute <destination>

Where supported, specify a source address or interface when necessary.

A successful test from the SRX does not automatically prove that transit traffic is working.

---

## Step 12 — Test Both Directions

Where practical, verify:

Source -> Destination

and

Destination -> Source

This helps identify:

- Return routing problems
- Asymmetric routing
- NAT problems
- Stateful session problems
- Upstream firewall issues

---

## Common Failure Domains

### Physical

Examples:

- Cable failure
- Interface down
- Speed negotiation issue
- Hardware alarm

### Layer 2

Examples:

- Wrong VLAN
- Trunk mismatch
- Switching issue

### Layer 3

Examples:

- Wrong IP address
- Wrong subnet mask
- Missing route
- Wrong next hop

### Security Zone

Examples:

- Interface in wrong zone
- Missing zone assignment
- Incorrect host-inbound configuration

### NAT

Examples:

- Wrong rule-set scope
- Wrong address match
- Wrong translation pool
- Rule order problem

### Security Policy

Examples:

- Missing policy
- Wrong direction
- Wrong address object
- Wrong application
- Policy order issue

### Stateful Session

Examples:

- Stale session
- Asymmetric path
- Return traffic does not match expected session

### Application

Examples:

- Service not listening
- Wrong destination port
- TLS problem
- Application failure

Do not assume the SRX is responsible until the failure domain is identified.

---

## Packet Capture

Packet capture can be useful when other evidence is insufficient.

Capture should be narrowly scoped.

Filter by:

- Source address
- Destination address
- Protocol
- Port
- Interface

Avoid broad production captures that generate excessive data.

Packet captures may expose sensitive information and should be handled accordingly.

---

## Flow Trace

Junos flow tracing can provide detailed security-processing information.

Flow tracing may help diagnose:

- Policy matching
- NAT processing
- Session creation
- Packet drops
- Routing interaction

Flow tracing can adversely affect scale and performance and may increase security risk.

Juniper strongly recommends using trace, tracing, or traceoptions commands only under JTAC guidance. If flow tracing is used, keep it narrowly scoped, collect only the required evidence, and disable it immediately after troubleshooting.

Exact configuration depends on Junos version.

---

## Change Control

Before making a configuration change:

1. Record the current state.
2. Run show | compare.
3. Preserve rollback capability.
4. Use commit check.
5. Use commit confirmed when lockout risk exists.
6. Make one logical change.
7. Verify operation.
8. Confirm the commit.
9. Record the result.

---

## Commit Confirmed

commit confirmed is recommended when modifying configuration that could interrupt management connectivity.

Examples include:

- Interface addressing
- Default route
- Security zones
- Host-inbound management
- Firewall filters
- Management routing

If the administrator loses access and cannot confirm the change, Junos can automatically roll back.

---

## Rollback

Rollback is a recovery mechanism, not a substitute for understanding the problem.

Before rollback:

- Identify which configuration version is required.
- Review differences.
- Understand what other changes may also be reverted.

Useful concepts include:

show system commit

rollback <number>

show | compare

commit

---

## Troubleshooting Discipline

Avoid:

- Random configuration changes
- Changing routing and policy simultaneously
- Broad permit-any rules as a permanent fix
- Disabling security features without evidence
- Clearing all sessions without cause
- Rebooting as the first troubleshooting step

Prefer:

- Evidence
- Controlled tests
- Narrow changes
- Verification
- Rollback capability
- Documentation

---

## AI Troubleshooting Rules

When an AI assistant uses this methodology:

- Ask for or inspect actual command output when production state is unknown.
- Do not invent interfaces, routes, zones, NAT rules, or policies.
- Identify the failure domain before recommending a change.
- Recommend one controlled change at a time.
- Explain the expected result of each test.
- Stop and reassess when observed output contradicts the working hypothesis.
- Preserve management access.
- Warn before disruptive actions.
- Prefer reversible changes.
- Record confirmed findings separately from assumptions.

---

## Incident Documentation

A troubleshooting record should include:

- Date and time
- Symptom
- Source
- Destination
- Protocol and port
- Observed behavior
- Commands executed
- Evidence collected
- Root cause
- Change made
- Verification result
- Rollback method
- Configuration state

Configuration state must be one of:

LEGACY_PRODUCTION

SRX320_TARGET

SRX320_VERIFIED_PRODUCTION

---

## Public Release Guidance

Before publishing troubleshooting examples:

- Remove production IP addresses
- Remove internal hostnames
- Remove usernames
- Remove credentials
- Remove public service mappings
- Remove customer-identifying information
- Sanitize packet captures and logs

Preserve the troubleshooting method while removing environment-specific sensitive data.

---

## Document Status

Document Type: Troubleshooting Methodology

Knowledge Base: Juniper SRX320 Knowledge Base

Version: 0.1.0

Status: Initial Build
