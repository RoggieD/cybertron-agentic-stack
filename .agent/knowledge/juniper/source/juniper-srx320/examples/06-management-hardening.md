# Juniper SRX320 Management Hardening Example

## Scope

This example demonstrates a basic management-plane hardening pattern for a Juniper SRX320.

It demonstrates:

- Restricting management to a trusted network
- Enabling only required host-inbound services
- SSH-focused administration
- Avoiding management exposure on untrusted interfaces
- Administrative account principles
- Logging and verification

This configuration is an educational example only.

It is not production configuration.

---

## Example Topology

Trusted Management Network:

192.0.2.0/24

Trusted Interface:

ge-0/0/1.0

Trusted Zone:

trust

Untrusted Interface:

ge-0/0/0.0

Untrusted Zone:

untrust

SRX Trusted Address:

192.0.2.1/24

---

## Security Objective

Permit administrative access to the SRX from the trusted management network.

Allow only required services such as:

- SSH
- Ping

Do not enable management services on the untrusted interface unless there is a specific operational requirement.

---

## Configure Trusted Interface

Example:

set interfaces ge-0/0/1 unit 0 family inet address 192.0.2.1/24

---

## Assign Trusted Zone

set security zones security-zone trust interfaces ge-0/0/1.0

---

## Enable SSH on Trusted Interface

Permit SSH traffic destined to the SRX:

set security zones security-zone trust interfaces ge-0/0/1.0 host-inbound-traffic system-services ssh

---

## Enable Ping on Trusted Interface

Permit ICMP echo for monitoring and troubleshooting:

set security zones security-zone trust interfaces ge-0/0/1.0 host-inbound-traffic system-services ping

---

## Do Not Enable Management on Untrust

Avoid enabling host-inbound management services on the Internet-facing interface.

Do not add:

ssh

https

telnet

snmp

to the untrust interface unless explicitly required.

---

## SSH Service

Enable the SSH system service:

set system services ssh

Host-inbound SSH permission and the SSH system service are separate requirements.

Exact optional SSH parameters may vary by Junos version.

---

## Administrative Users

Use named administrative users rather than shared credentials where practical.

A production account design should identify:

- Username
- Role
- Login class
- Authentication method
- Operational purpose

Do not include real passwords or keys in public documentation.

---

## Login Classes

Administrative privilege should match operational need.

Possible concepts include:

- Full administrative access
- Read-only access
- Restricted operational access

Do not grant full administrative privilege by default to every account.

---

## Root Access

Direct root login should be limited where practical.

Prefer named administrative accounts for routine work.

Root credentials should be protected and excluded from documentation.

---

## SSH Keys

Where appropriate, use SSH public-key authentication.

Do not publish:

- Private keys
- Production public keys tied to real users
- Credential material

Public examples should use placeholders only.

---

## HTTPS Management

If HTTPS management is required, enable it only on trusted interfaces.

Example concept:

set security zones security-zone trust interfaces ge-0/0/1.0 host-inbound-traffic system-services https

Do not enable HTTPS administration on untrusted interfaces without a specific need.

---

## SNMP Management

If SNMP monitoring is required, permit SNMP only from the expected monitoring path.

Do not expose SNMP broadly.

SNMP access should be combined with:

- Source restrictions
- Secure SNMP version where practical
- Credential protection
- Monitoring-network controls

---

## Console Access

Maintain physical or serial console access where possible.

Console access is especially important before changing:

- Management IP
- Routing
- Security zones
- Host-inbound services
- Authentication
- Firewall filters

---

## Optional Management Address Objects

Where design requires tighter source control, define trusted management networks explicitly.

Example management source:

192.0.2.0/24

The exact enforcement mechanism depends on the management-plane design and Junos version.

Do not assume security policies alone govern traffic destined to the SRX itself.

---

## Host-Inbound vs Transit Traffic

Traffic destined to the SRX itself is host-inbound traffic.

Traffic passing through the SRX is transit traffic.

This distinction is critical.

A transit security policy does not replace host-inbound configuration for services such as:

- SSH to the firewall
- HTTPS to the firewall
- Ping to an SRX interface
- SNMP to the firewall

---

## Logging Administrative Activity

Administrative activity should be observable where practical.

Useful evidence may include:

- Login events
- Authentication failures
- Commit history
- System logs

Operational commands may include:

show system commit

show log messages

---

## Review Candidate Configuration

Before commit:

show | compare

---

## Validate Configuration

Run:

commit check

Correct any errors before activation.

---

## Use Commit Confirmed

When changing management access remotely:

commit confirmed

Verify:

- SSH still works
- Management IP responds
- Required routes still exist
- Trusted source can reconnect

Only then confirm the commit.

---

## Verification

Verify interface:

show interfaces terse

Verify zone:

show security zones

Verify system services:

show configuration system services

Verify host-inbound configuration:

show configuration security zones

Verify commit history:

show system commit

---

## Management Troubleshooting

If SSH fails, verify:

1. Physical interface state
2. Logical interface state
3. SRX management IP
4. Source host IP
5. Routing
6. Trusted zone assignment
7. Host-inbound SSH permission
8. SSH system service
9. Authentication
10. Logs
11. Return path

Do not immediately broaden access.

Identify the actual failure first.

---

## Lockout Recovery

If remote management is lost:

1. Wait for commit-confirmed rollback if one is active.
2. Use console access if available.
3. Review recent commit history.
4. Compare configuration.
5. Roll back only after identifying the correct revision.

Avoid rebooting as the first response.

---

## Important Notes

This example uses documentation-only IP ranges.

Do not copy the example values directly into production.

Do not assume:

- ge-0/0/1.0 is the management interface
- trust is the correct management zone
- SSH is the only required management protocol
- HTTPS must be enabled
- SNMP must be enabled
- the management network is 192.0.2.0/24

Verify the actual deployment.

---

## Security Guidance

For production management:

- Restrict source networks
- Use named accounts
- Prefer SSH over insecure protocols
- Protect credentials
- Avoid public management exposure
- Use logging
- Maintain console access
- Review stale accounts
- Disable unnecessary services

---

## AI Guidance

When using this example:

- Treat all addresses as examples.
- Do not invent production management IPs.
- Do not expose credentials.
- Distinguish host-inbound from transit traffic.
- Verify management zone and interface.
- Preserve a recovery path.
- Use commit confirmed when lockout is possible.
- Prefer restrictive management access over broad exposure.

---

## Document Status

Document Type: Configuration Example

Example Type: Management Hardening

Knowledge Base: Juniper SRX320 Knowledge Base

Version: 0.1.0

Status: Example / Non-Production
