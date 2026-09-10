# Juniper SRX320 Security Zones and Policies

## Scope

This document explains Junos security zones and inter-zone security policies on the Juniper SRX320.

It provides platform-level guidance and does not represent a specific production policy set unless explicitly labeled.

---

## Security Zones

Security zones are logical trust boundaries used by the SRX firewall.

Interfaces are assigned to zones.

Typical examples include:

- trust
- untrust
- dmz
- management

Zone names are configurable and may differ between environments.

A zone should represent a meaningful security boundary rather than simply an arbitrary interface grouping.

---

## Zone Membership

A routed interface normally participates in security policy processing through zone membership.

Example logical interface:

ge-0/0/1.0

An interface assigned to a zone inherits the security context of that zone.

Traffic behavior depends on:

- Source zone
- Destination zone
- Security policy
- Routing
- NAT
- Host-inbound settings
- Session state

---

## Host-Inbound Traffic

Traffic destined to the SRX device itself is handled differently from transit traffic.

Examples include:

- SSH to the firewall
- HTTPS management
- Ping to an SRX interface
- SNMP
- DHCP services
- Routing protocol traffic

Host-inbound services are configured at the security zone or interface level.

Example concept:

security {
    zones {
        security-zone trust {
            interfaces {
                ge-0/0/1.0 {
                    host-inbound-traffic {
                        system-services {
                            ssh;
                            ping;
                        }
                    }
                }
            }
        }
    }
}

This is an example only.

---

## Security Policies

Security policies control transit traffic between security zones.

A policy normally evaluates:

- Source zone
- Destination zone
- Source address
- Destination address
- Application
- Action
- Logging behavior

A typical policy action is:

permit

or

deny

---

## Policy Direction

Policies are directional.

A policy from:

trust -> untrust

does not automatically create a policy from:

untrust -> trust

However, Junos is stateful.

If a permitted session is established from trust to untrust, return traffic for that session is normally allowed automatically.

---

## Policy Matching

Security policies are evaluated in order within the relevant source-zone and destination-zone policy set.

More specific policy logic should generally appear before broad catch-all rules when rule ordering affects behavior.

A policy may match:

- Any source
- Any destination
- A specific address object
- An address set
- A predefined application
- A custom application
- Multiple applications

---

## Address Objects

Security policies commonly reference named address-book objects.

Examples:

WEB_SERVER

MAIL_SERVER

LAN_SUBNET

DMZ_SUBNET

Address objects improve readability and reduce repeated literal IP usage.

Address sets may group multiple address objects.

---

## Applications

Policies may reference applications such as:

- junos-http
- junos-https
- junos-ssh
- junos-dns
- junos-ping

Custom applications may also be defined for non-standard ports or protocols.

Application definitions should clearly identify:

- Protocol
- Destination port
- Source port when relevant
- Timeout behavior when relevant

---

## Permit Policies

A permit policy allows matching traffic to create a stateful session.

Permit policies may also include:

- Logging
- Application services
- User identity features
- Advanced inspection features

Simple permit example concept:

security {
    policies {
        from-zone trust to-zone untrust {
            policy ALLOW-INTERNET {
                match {
                    source-address any;
                    destination-address any;
                    application any;
                }
                then {
                    permit;
                }
            }
        }
    }
}

This is an example only.

---

## Deny Policies

A deny policy explicitly blocks matching traffic.

Deny policies may be used to:

- Block known destinations
- Prevent inter-zone access
- Enforce segmentation
- Create explicit audit points
- Log unauthorized traffic

Logging should be used selectively to avoid unnecessary log volume.

---

## Default Behavior

Traffic that does not match a permitting policy may be denied.

Do not assume traffic is permitted merely because:

- A route exists
- NAT is configured
- The interface is up
- The destination responds locally

Security policy must still permit transit traffic where required.

---

## Intra-Zone Traffic

Security policy lookup also applies to traffic passing between interfaces assigned to the same security zone.

A permitting intrazone policy is therefore required unless the active configuration already provides an applicable policy, such as a factory-default trust-to-trust policy on supported SRX platforms.

Behavior should be verified using:

- Current Junos version
- Active configuration
- Zone structure
- Policy configuration

Do not assume same-zone traffic is automatically permitted.

---

## Policy Logging

Security policies may log:

- Session initialization
- Session closure

Logging is useful for:

- Troubleshooting
- Security auditing
- Policy validation
- Identifying unexpected traffic

Excessive session logging can create unnecessary load and storage consumption.

---

## Policy Troubleshooting

When expected traffic is blocked, verify:

1. Source interface
2. Source security zone
3. Destination route
4. Destination security zone
5. NAT processing
6. Source address object
7. Destination address object
8. Application match
9. Policy ordering
10. Session state
11. Logs

Do not modify policies before confirming which policy is actually matching or failing to match.

---

## Useful Verification Commands

Operational commands may include:

show security zones

show security policies

show security policies detail

Use show security match-policies with the actual flow criteria when testing a policy decision, including source and destination zones, source and destination IP addresses, ports, and protocol as applicable.

show security flow session

show security flow session source-prefix <address>

show security flow session destination-prefix <address>

show log messages

Exact command availability may vary by Junos version.

---

## Policy Design Principles

Recommended principles include:

- Least privilege
- Clear policy names
- Descriptive address objects
- Explicit applications
- Limited use of application any
- Logging where operationally useful
- Avoid broad permit rules when narrower rules are practical
- Document business purpose
- Review stale rules periodically

---

## Production Policy Documentation

Production policy records should identify:

- Policy name
- Source zone
- Destination zone
- Source address
- Destination address
- Application
- Action
- Logging
- Business purpose
- Configuration state
- Verification date

Configuration state must be one of:

LEGACY_PRODUCTION

SRX320_TARGET

SRX320_VERIFIED_PRODUCTION

---

## AI Guidance

When using this document:

- Do not invent security policies.
- Do not assume zone names.
- Do not assume interface-to-zone assignments.
- Do not assume a route implies permission.
- Do not assume NAT implies permission.
- Distinguish host-inbound traffic from transit traffic.
- Verify policy direction.
- Prefer actual policy output when diagnosing production behavior.

---

## Document Status

Document Type: Security Zones and Policies

Knowledge Base: Juniper SRX320 Knowledge Base

Version: 0.1.0

Status: Initial Build
