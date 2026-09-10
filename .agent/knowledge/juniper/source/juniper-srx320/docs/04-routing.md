# Juniper SRX320 Routing

## Scope

This document explains routing concepts on the Juniper SRX320 using Junos OS.

It provides platform-level guidance for:

- Directly connected routes
- Static routes
- Default routes
- Route preference
- Routing verification
- Routing troubleshooting
- Interaction between routing, security policy, and NAT

It does not represent a specific production routing table unless explicitly labeled.

---

## Routing Overview

The SRX320 performs Layer 3 routing in addition to firewalling.

Traffic forwarding depends on a valid route to the destination.

Routing and security are separate functions.

A packet may have:

- A valid route but no permitting security policy
- A valid security policy but no usable route
- Correct NAT but incorrect routing
- Correct routing but incorrect NAT

Troubleshooting should verify each function independently.

---

## Directly Connected Routes

When an interface has an IP address configured and is operational, Junos typically installs a directly connected route for that subnet.

Example:

Interface:

ge-0/0/1.0

Address:

192.0.2.1/24

The corresponding connected route may represent:

192.0.2.0/24

This is an example only.

Connected routes depend on actual interface state and configuration.

---

## Static Routes

Static routes are manually configured routes.

Typical use cases include:

- Default Internet route
- Internal routed networks
- Remote subnets
- Management networks
- DMZ routes
- Temporary migration paths

Conceptual example:

routing-options {
    static {
        route 203.0.113.0/24 next-hop 192.0.2.254;
    }
}

This is an example only.

---

## Default Route

A default route is used when no more specific route matches a destination.

IPv4 default route:

0.0.0.0/0

Conceptual example:

routing-options {
    static {
        route 0.0.0.0/0 next-hop 198.51.100.1;
    }
}

This is an example only.

Do not assume the default gateway or WAN next hop without verification.

---

## Route Preference

Junos uses route preference values to select among competing routes.

Lower preference values are generally preferred over higher values.

Route selection may depend on:

- Route protocol
- Preference
- Route specificity
- Next-hop reachability
- Routing instance
- Policy

When multiple routes exist, verify which route is active rather than assuming one is being used.

---

## Longest Prefix Match

Routing decisions normally use longest-prefix matching.

A more specific route is preferred over a less specific route.

Example:

10.0.0.0/8

and

10.1.0.0/16

Traffic destined for:

10.1.2.3

would normally match the more specific:

10.1.0.0/16

assuming the route is valid and active.

---

## Next-Hop Reachability

A static route requires a usable next hop.

If the next hop is not reachable, the route may not be usable.

Verify:

- Interface state
- Neighbor reachability
- ARP or neighbor discovery
- Connected subnet
- Route recursion
- Routing instance

---

## Routing Tables

The main IPv4 routing table is commonly:

inet.0

IPv6 routing commonly uses:

inet6.0

Additional routing tables may exist when using:

- Routing instances
- Virtual routers
- VPNs
- Specialized services

Do not assume all routes are present in the default routing table.

---

## Useful Routing Commands

Operational commands may include:

show route

show route detail

show route terse

show route protocol static

show route 0.0.0.0/0

show route <destination>

show route forwarding-table

show interfaces terse

show arp

Exact command syntax and output may vary by Junos version.

---

## Route Verification

When verifying a route, confirm:

1. Destination prefix
2. Active route
3. Route protocol
4. Preference
5. Next hop
6. Outgoing interface
7. Next-hop reachability
8. Routing instance
9. More-specific competing routes

---

## Routing and Security Zones

Routing determines where traffic should go.

Security zones define trust boundaries.

A route may direct traffic toward an interface in a specific zone.

Security policy must still permit the traffic between the applicable source and destination zones.

Routing does not bypass security policy.

---

## Routing and NAT

Routing and NAT interact but are separate.

Possible failure scenarios include:

- Correct source NAT with wrong default route
- Correct destination NAT with no route to the translated host
- Correct route with incorrect NAT rule match
- Correct inbound path with incorrect return route
- Asymmetric routing after translation

Always verify both forward and return paths.

---

## Return Routing

Return routing is critical for stateful firewall operation.

The destination system must return traffic through a path compatible with the SRX session.

Problems may occur when:

- Multiple gateways exist
- Internal hosts use the wrong default gateway
- Policy routing changes the return path
- Another firewall handles return traffic
- Asymmetric routing exists

---

## Asymmetric Routing

Asymmetric routing occurs when forward and return traffic use different paths.

This may cause problems with:

- Stateful session tracking
- NAT
- Security policy enforcement
- Troubleshooting visibility

When asymmetric routing is suspected, examine both traffic directions.

---

## Routing Instances

Junos supports routing instances for logical separation of routing domains.

Routing instances may be used for:

- Virtual routing
- VPNs
- Tenant separation
- Specialized service paths

Do not assume an interface or route belongs to the default routing instance.

Verify active configuration when routing behavior appears inconsistent.

---

## Route Troubleshooting

When traffic is not reaching its destination, verify:

1. Source IP
2. Destination IP
3. Source interface
4. Destination route
5. Active next hop
6. Egress interface
7. Next-hop reachability
8. Security zones
9. Security policy
10. NAT behavior
11. Return route
12. Session state
13. Logs

---

## Connectivity Testing

Useful diagnostic tools may include:

ping <destination>

traceroute <destination>

show route <destination>

show arp

show security flow session

When possible, test from:

- The SRX itself
- The source network
- The destination network
- Both directions

---

## Production Routing Documentation

Production routing records should identify:

- Destination prefix
- Route type
- Next hop
- Outgoing interface
- Routing instance
- Preference if relevant
- Purpose
- Configuration state
- Verification date

Configuration state must be one of:

LEGACY_PRODUCTION

SRX320_TARGET

SRX320_VERIFIED_PRODUCTION

---

## Public Release Guidance

Before publishing routing examples:

- Replace real public IP addresses
- Remove internal infrastructure identifiers
- Remove private hostnames
- Remove customer-specific routes
- Preserve technical patterns without exposing topology

Use documentation address ranges when examples require public IP addressing.

---

## AI Guidance

When using this document:

- Do not invent routes.
- Do not invent next-hop addresses.
- Do not assume a default route exists.
- Do not assume the routing table is inet.0.
- Verify active route selection.
- Verify return routing.
- Treat routing, NAT, and security policy as separate checks.
- Prefer live routing output when diagnosing production behavior.

---

## Document Status

Document Type: Routing

Knowledge Base: Juniper SRX320 Knowledge Base

Version: 0.1.0

Status: Initial Build
