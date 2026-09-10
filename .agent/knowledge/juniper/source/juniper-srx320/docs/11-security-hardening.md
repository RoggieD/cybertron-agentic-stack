# Juniper SRX320 Security Hardening

## Scope

This document provides security-hardening guidance for the Juniper SRX320 running Junos OS.

It is intended for:

- Production deployment
- Firewall migration
- Administrative access control
- Exposure reduction
- Configuration review
- Monitoring
- Incident prevention
- AI-assisted security analysis

This document provides platform-level guidance and does not represent a specific production hardening configuration unless explicitly labeled.

---

## Hardening Philosophy

Security hardening should reduce attack surface without making the firewall unnecessarily difficult to operate.

Primary goals include:

- Least privilege
- Minimal exposed services
- Restricted management access
- Strong authentication
- Secure logging
- Controlled administrative access
- Configuration protection
- Reliable recovery capability
- Regular software maintenance

Hardening should remain proportional to operational risk.

---

## Management Plane Protection

Administrative access should be limited to trusted systems and networks.

Management services may include:

- SSH
- HTTPS
- SNMP
- Console
- NETCONF where used

Avoid exposing management services directly to untrusted networks unless there is a documented requirement and appropriate protection.

---

## SSH

SSH should be preferred over insecure remote CLI protocols.

Recommended practices include:

- Restrict SSH to trusted management networks
- Use named administrative accounts
- Prefer key-based authentication where appropriate
- Disable unused accounts
- Limit root access
- Review authentication logs
- Use strong credentials

Do not publish SSH keys or credential material.

---

## Telnet

Telnet transmits data without modern encryption protections.

It should generally be disabled unless required for a tightly controlled legacy use case.

Do not enable Telnet merely for convenience.

---

## HTTPS

HTTPS management should be:

- Restricted to trusted networks
- Protected with TLS
- Disabled if not required
- Reviewed for certificate quality
- Limited by host-inbound configuration

Avoid exposing browser-based administration to untrusted networks without a specific operational requirement.

---

## Root Access

Direct root login should be limited where practical.

Prefer:

- Named administrative accounts
- Appropriate login classes
- Traceable user activity
- Strong authentication

Root credentials should be protected and excluded from documentation.

---

## Administrative Accounts

Administrative accounts should be reviewed periodically.

Document:

- Username
- Role
- Login class
- Authentication method
- Operational purpose
- Status

Remove stale or unnecessary accounts.

---

## Authentication

Where supported and appropriate, authentication may use:

- Local credentials
- SSH keys
- Centralized authentication
- RADIUS
- TACACS+

Do not depend on an external authentication service without retaining a recovery path.

---

## Host-Inbound Services

Host-inbound traffic determines which services can reach the SRX itself.

Only enable services that are operationally required.

Examples include:

- ssh
- https
- ping
- snmp

Review host-inbound configuration on each security zone and interface.

Do not enable all services broadly.

---

## Untrusted Interfaces

Internet-facing or otherwise untrusted interfaces should receive especially restrictive management configuration.

Review:

- Host-inbound services
- Firewall filters
- Routing protocol exposure
- Management access
- Discovery protocols
- Published services

The default posture should minimize unnecessary exposure.

---

## Security Policies

Security policies should follow least-privilege principles.

Prefer:

- Specific source networks
- Specific destinations
- Specific applications
- Clear policy names
- Documented business purpose

Avoid broad rules such as:

source-address any
destination-address any
application any

unless they are justified and understood.

---

## Deny and Logging Strategy

Not every denied packet needs to be logged.

Logging should provide useful security and troubleshooting visibility without overwhelming storage or processing resources.

Consider logging:

- Administrative access attempts
- Important security policy matches
- Critical denied traffic
- Configuration events
- Authentication failures

---

## NAT Exposure

Destination NAT and static NAT may expose internal systems externally.

Every published service should be reviewed for:

- Business need
- Public IP
- Public port
- Internal destination
- Security policy
- Source restrictions
- Application security
- Monitoring
- Patch status

Do not treat NAT as a security control by itself.

---

## Unused Services

Disable unnecessary system services.

Potential examples include:

- Unused management protocols
- Legacy services
- Unused routing protocols
- Unused VPN services
- Unused discovery protocols

Feature availability depends on Junos version.

---

## SNMP

If SNMP is used:

- Restrict source systems
- Prefer secure SNMP versions where practical
- Protect credentials
- Avoid public exposure
- Monitor authentication failures

SNMP should be treated as administrative infrastructure.

---

## Syslog

Remote logging can improve security visibility.

Important events may include:

- Administrative login
- Failed authentication
- Configuration changes
- Security policy events
- System alarms
- Interface changes

Logs should be protected against unauthorized modification.

---

## NTP

Accurate time improves:

- Log correlation
- Incident investigation
- Authentication
- Certificate validation
- Monitoring

Use trusted NTP sources.

---

## DNS

Use trusted DNS resolvers where the SRX requires name resolution.

Do not confuse DNS failure with network failure.

Avoid configuring unnecessary external resolver dependencies.

---

## Software Maintenance

Junos should be maintained at a release appropriate for:

- SRX320 hardware support
- Security fixes
- Feature requirements
- Operational stability

Do not upgrade production firewalls solely because a newer release exists.

Review:

- Release notes
- Security advisories
- Compatibility
- Upgrade path
- Rollback plan

---

## Configuration Backups

Maintain protected configuration backups.

Backups should be:

- Stored off-device
- Access-controlled
- Versioned
- Tested where practical
- Sanitized before sharing

Raw backups may contain sensitive information.

---

## Rescue Configuration

Maintain a known-good rescue configuration after the production configuration has been validated.

Do not save an unstable or partially tested configuration as the rescue baseline.

---

## Console Security

Physical console access provides powerful administrative control.

Protect physical access to:

- Firewall
- Console cable
- Serial servers
- Rack
- Network equipment

Physical access should be considered part of the security model.

---

## Firewall Filters

Firewall filters may provide additional control over traffic destined to the device or specific interfaces.

Use filters carefully.

Incorrect filters may cause management lockout or unintended traffic disruption.

Use rollback and commit confirmed where lockout is possible.

---

## Routing Protocol Security

If dynamic routing protocols are used, consider:

- Authentication
- Neighbor restrictions
- Interface scope
- Route filtering
- Route policy
- Management-plane exposure

Do not enable routing protocols on interfaces where they are not required.

---

## VPN Security

VPN security should consider:

- Strong authentication
- Current cryptographic standards
- Peer restrictions
- Network scope
- Key protection
- Logging
- Monitoring
- Rekey behavior

Do not store VPN secrets in this knowledge base.

---

## Configuration Review

Periodic configuration review should look for:

- Unused policies
- Broad permit rules
- Stale address objects
- Unused NAT mappings
- Old administrators
- Unused services
- Obsolete routes
- Unnecessary host-inbound services
- Unused VPN definitions
- Unexpected public exposure

---

## Hardening Validation

A hardening review should verify:

1. Administrative services
2. Administrative users
3. Host-inbound services
4. Security zones
5. Security policies
6. NAT exposure
7. Routing protocol exposure
8. SNMP
9. Logging
10. NTP
11. Software version
12. Configuration backup
13. Rescue configuration
14. Console access
15. Public services

---

## Change Safety

Before hardening changes:

1. Record current state.
2. Review dependencies.
3. Preserve console access.
4. Use show | compare.
5. Use commit check.
6. Use commit confirmed when lockout risk exists.
7. Test management access.
8. Test production traffic.
9. Confirm the commit.
10. Document the result.

---

## Public Release Guidance

Before publishing security examples:

- Remove real IP addresses
- Remove usernames
- Remove SSH keys
- Remove authentication details
- Remove SNMP credentials
- Remove internal hostnames
- Remove VPN peer information
- Remove public service mappings
- Replace sensitive values with documentation examples

Do not publish raw production configuration.

---

## AI Guidance

When using this document:

- Prefer least privilege.
- Do not recommend broad exposure as a permanent solution.
- Do not invent current hardening state.
- Verify management paths before recommending restrictive changes.
- Warn when a change may cause lockout.
- Protect secrets and credentials.
- Prefer reversible hardening changes.
- Distinguish security improvement from operational disruption.

---

## Document Status

Document Type: Security Hardening

Knowledge Base: Juniper SRX320 Knowledge Base

Version: 0.1.0

Status: Initial Build
