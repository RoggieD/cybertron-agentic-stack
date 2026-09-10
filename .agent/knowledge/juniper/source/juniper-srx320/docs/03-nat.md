# Juniper SRX320 Network Address Translation

## Scope

This document explains NAT concepts on the Juniper SRX320 using Junos OS.

It provides platform-level guidance for:

- Source NAT
- Destination NAT
- Static NAT
- NAT troubleshooting
- NAT rule design
- NAT interaction with routing and security policies

It does not represent a specific production NAT configuration unless explicitly labeled.

---

## NAT Overview

Network Address Translation changes IP addressing information as traffic passes through the SRX firewall.

Primary NAT types on Junos include:

- Source NAT
- Destination NAT
- Static NAT

Each NAT type serves a different purpose.

NAT does not replace:

- Routing
- Security policies
- Interface configuration
- Security zones

A NAT rule may be correct while traffic still fails because another required component is incorrect.

---

## Source NAT

Source NAT changes the source address of traffic.

A common use case is allowing private internal hosts to access the Internet using a public address.

Source NAT is commonly applied to traffic moving from:

trust -> untrust

or from another internal security zone toward an external network.

Common source NAT approaches include:

- Interface source NAT
- Source NAT pool
- Source NAT with specific public addresses

---

## Interface Source NAT

Interface source NAT uses the IP address assigned to the egress interface.

Conceptual example:

security {
    nat {
        source {
            rule-set TRUST-TO-INTERNET {
                from zone trust;
                to zone untrust;

                rule INTERNET-SNAT {
                    match {
                        source-address 10.0.0.0/24;
                    }

                    then {
                        source-nat {
                            interface;
                        }
                    }
                }
            }
        }
    }
}

This is an example only.

It is not a production configuration.

---

## Source NAT Pools

A source NAT pool allows traffic to use one or more explicitly defined translated addresses.

A pool may contain:

- One public IP
- Multiple public IPs
- A public address range

Conceptual example:

security {
    nat {
        source {
            pool INTERNET_POOL {
                address {
                    198.51.100.10/32;
                }
            }
        }
    }
}

This example uses documentation-only addressing.

---

## Destination NAT

Destination NAT changes the destination address of incoming traffic.

Common use cases include:

- Publishing a web server
- Publishing a mail server
- Forwarding a public IP to an internal host
- Port forwarding
- Translating public services into a DMZ

Destination NAT is processed before route lookup and security policy lookup for a new flow. Security policy evaluation therefore needs to account for the translated destination address.

---

## Destination NAT Pools

Destination NAT commonly uses a destination NAT pool that identifies the internal translated destination.

Conceptual example:

security {
    nat {
        destination {
            pool WEB_SERVER {
                address 10.0.2.10/32;
            }
        }
    }
}

This is an example only.

---

## Destination NAT Rule Sets

A destination NAT rule set may match:

- Incoming zone
- Incoming interface
- Destination public address
- Protocol
- Destination port

Then it may translate the destination to:

- Internal IP address
- Internal port
- Destination NAT pool

Conceptual example:

security {
    nat {
        destination {
            rule-set INTERNET-INBOUND {
                from zone untrust;

                rule WEB-HTTPS {
                    match {
                        destination-address 198.51.100.20/32;
                        destination-port 443;
                        protocol tcp;
                    }

                    then {
                        destination-nat {
                            pool {
                                WEB_SERVER;
                            }
                        }
                    }
                }
            }
        }
    }
}

This is an example only.

---

## Static NAT

Static NAT provides a fixed one-to-one mapping between addresses.

Common use cases include:

- Dedicated public address for an internal server
- Bidirectional address translation
- Consistent public identity for an internal system

Static NAT behaves differently from simple destination NAT and should not be treated as identical.

---

## NAT Rule Matching

NAT rule matching may depend on:

- Source zone
- Destination zone
- Incoming interface
- Source address
- Destination address
- Protocol
- Port

Rule order matters within applicable NAT rule sets.

More specific rules should generally be evaluated before broader rules where order affects matching.

---

## NAT and Security Policies

NAT and security policy are separate functions.

A valid NAT rule does not automatically permit traffic.

A valid security policy does not automatically create NAT.

For inbound destination NAT traffic, policy evaluation must be understood in relation to the translated destination.

When troubleshooting, verify the exact address objects used by the applicable security policy.

---

## NAT and Routing

Routing is also independent of NAT.

Traffic may match NAT correctly but still fail because:

- No route exists
- The wrong next hop is selected
- Return routing is incorrect
- The translated destination is unreachable
- Asymmetric routing exists

Always verify routing independently.

---

## NAT and Zones

NAT rule sets may use:

- Source zone
- Destination zone
- Incoming interface

Zone membership therefore matters.

If an interface is assigned to an unexpected zone, NAT rules may fail to match.

---

## Port Forwarding

Port forwarding is commonly implemented with destination NAT.

A port-forwarding design should document:

- Public IP
- Public port
- Protocol
- Internal IP
- Internal port
- Incoming zone
- Destination security zone
- Security policy
- Business purpose

Do not document only the NAT rule.

The corresponding policy and routing behavior are part of the complete service path.

---

## Multiple Public IP Addresses

An SRX may use multiple public addresses for:

- Static NAT
- Destination NAT
- Source NAT pools
- Dedicated services
- Multiple hosted systems

When multiple public IPs exist, documentation should clearly identify:

- Address owner or service
- Translation type
- Internal destination
- Required policy
- Required route
- Verification status

---

## NAT Troubleshooting

When NAT does not behave as expected, verify:

1. Incoming interface
2. Source zone
3. Destination zone
4. NAT rule-set scope
5. NAT rule order
6. Source address match
7. Destination address match
8. Protocol match
9. Port match
10. Translation pool
11. Security policy
12. Routing
13. Return path
14. Session table
15. Logs

---

## Useful Verification Commands

Useful commands may include:

show configuration security nat

show configuration security nat source

show configuration security nat destination

show configuration security nat static

show security nat source rule all

show security nat destination rule all

show security nat static rule all

show security flow session

show security flow session source-prefix <address>

show security flow session destination-prefix <address>

show route

Exact command syntax and availability may vary by Junos version.

---

## NAT Documentation Requirements

Production NAT records should document:

- Rule name
- NAT type
- Source zone
- Destination zone
- Incoming interface if applicable
- Source address
- Destination address
- Protocol
- Port
- Translation pool
- Translated address
- Related security policy
- Business purpose
- Configuration state
- Verification date

Configuration state must be one of:

LEGACY_PRODUCTION

SRX320_TARGET

SRX320_VERIFIED_PRODUCTION

---

## Public Release Guidance

Production NAT information may expose:

- Public IP assignments
- Internal addressing
- Published services
- Infrastructure relationships

Before public release or commercial distribution:

- Replace production IP addresses with documentation ranges
- Remove customer-specific addressing
- Remove internal hostnames
- Remove sensitive service mappings
- Preserve the technical pattern without exposing the real environment

---

## AI Guidance

When using this document:

- Do not assume NAT is required.
- Do not assume NAT alone permits traffic.
- Do not invent public IP addresses.
- Do not invent internal destinations.
- Do not invent NAT pools.
- Verify rule direction.
- Verify rule order.
- Verify associated security policy.
- Verify routing separately.
- Treat examples as non-production unless explicitly marked verified.

---

## Document Status

Document Type: Network Address Translation

Knowledge Base: Juniper SRX320 Knowledge Base

Version: 0.1.0

Status: Initial Build
