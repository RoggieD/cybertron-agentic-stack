# Juniper SRX320 Dual-WAN Failover Concepts

## Scope

This example describes the design concepts involved in providing Internet failover across two WAN connections on a Juniper SRX320.

It covers:

- Primary and backup WAN interfaces
- Default-route preference
- Reachability monitoring
- Route failover
- NAT considerations
- Security-zone design
- Failure detection
- Recovery behavior
- Validation and troubleshooting

This document is a design example.

It is not a complete production configuration.

---

## Example Topology

### Primary ISP

Interface:

ge-0/0/0.0

Zone:

untrust-primary

Public Network:

198.51.100.0/24

SRX Address:

198.51.100.10/24

Gateway:

198.51.100.1

---

### Backup ISP

Interface:

ge-0/0/2.0

Zone:

untrust-backup

Public Network:

203.0.113.0/24

SRX Address:

203.0.113.10/24

Gateway:

203.0.113.1

---

### Internal LAN

Interface:

ge-0/0/1.0

Zone:

trust

Network:

192.0.2.0/24

Gateway:

192.0.2.1

---

## Design Objective

Normal traffic should use the primary ISP.

If the primary path becomes unusable, traffic should fail over to the backup ISP.

When the primary path becomes healthy again, traffic may return to the primary path according to the chosen recovery policy.

---

## Basic Route Preference

One design uses two default routes with different preferences.

Conceptually:

Primary route:

0.0.0.0/0 via 198.51.100.1

Backup route:

0.0.0.0/0 via 203.0.113.1

The primary route should be preferred while healthy.

The backup route should become active when the primary route is unavailable.

Do not assume that interface-down detection alone is sufficient.

---

## Physical Failure vs Upstream Failure

A WAN interface may remain physically up even when Internet connectivity through the provider has failed.

Examples:

- ISP upstream routing failure
- Provider gateway still responds but Internet path is broken
- Fiber or cable modem remains Ethernet-up
- Provider DNS fails
- Upstream transit outage

Therefore, robust failover should monitor meaningful reachability beyond simple Ethernet link state.

---

## Reachability Monitoring

Reachability monitoring may test one or more remote targets.

Possible targets include:

- ISP gateway
- Provider upstream router
- Stable public IP
- Multiple independent external targets

A single test target can create false failover if that target alone becomes unavailable.

Use monitoring targets that accurately represent path health.

---

## RPM and IP Monitoring Concepts

Junos may use Real-Time Performance Monitoring and related IP-monitoring functionality to detect path failure and influence routing behavior.

A monitoring design may:

1. Send probes through the primary WAN.
2. Detect repeated probe failure.
3. Modify route preference or install a backup route.
4. Direct new traffic through the secondary WAN.
5. Restore the primary route when health returns.

Exact configuration depends on Junos version and desired behavior.

---

## Failure Thresholds

Do not fail over on a single lost packet.

Monitoring should account for:

- Probe interval
- Successive loss
- Recovery threshold
- Latency
- Packet loss
- Flapping prevention

Failover that is too sensitive can cause route instability.

Failover that is too slow can extend outages.

---

## Default Route Design

The routing table should clearly indicate which WAN path is preferred.

Documentation should record:

Primary Route:

Primary Preference:

Backup Route:

Backup Preference:

Health Monitoring:

Failover Trigger:

Recovery Trigger:

---

## Security Zones

WAN interfaces may be placed in:

- A shared untrust zone
- Separate untrust zones

Example:

untrust-primary

untrust-backup

Separate zones can make policy and NAT intent more explicit.

The correct design depends on operational requirements.

---

## Security Policies

Internal users may require outbound policies toward both WAN zones.

Example concepts:

trust -> untrust-primary

trust -> untrust-backup

Policies should permit only required traffic.

Do not assume one policy automatically covers both zones.

---

## Source NAT

Source NAT must account for the active egress WAN.

Interface-based NAT can simplify failover because traffic may use the address assigned to the active egress interface.

Example concept:

trust -> untrust-primary uses primary interface source NAT

trust -> untrust-backup uses backup interface source NAT

---

## NAT Pool Considerations

Explicit public NAT pools can complicate failover.

A public IP assigned by ISP-A may not be usable through ISP-B.

Therefore, failover design must distinguish between:

- Provider-specific public IPs
- Portable address space
- Interface NAT
- NAT pools
- Static NAT
- Published services

Do not assume outbound and inbound failover have the same design requirements.

---

## Published Services

Inbound service failover is more complex than outbound Internet failover.

Published services may depend on:

- Public DNS
- Public IP ownership
- Destination NAT
- Provider routing
- TTL
- Dynamic DNS
- External load balancing
- BGP
- Application-level failover

Two WAN circuits do not automatically make an inbound service redundant.

---

## Static NAT and Dual WAN

One-to-one public mappings are generally tied to a specific provider unless the address block is independently routable through both providers.

A backup ISP may require a different public address.

Application or DNS changes may therefore be necessary during failover.

---

## VPN Considerations

Site-to-site VPNs may also depend on the active WAN.

Consider:

- Peer public IP
- Local gateway
- Routing
- NAT
- IKE gateway configuration
- Remote peer expectations
- DNS-based peer identification where supported

A VPN may require separate primary and backup definitions.

---

## Existing Sessions

Existing sessions may not survive a WAN transition.

Reasons include:

- Source public IP changes
- NAT mapping changes
- Remote endpoint state
- Routing changes
- VPN changes

Failover should therefore be evaluated for both:

- New sessions
- Existing sessions

---

## Failback

When the primary WAN recovers, automatic failback may occur.

Consider whether immediate failback is desirable.

Rapid failback can cause additional disruption if the primary circuit is unstable.

Recovery logic may need hold-down or stability timers.

---

## DNS

Outbound failover may succeed while users still experience apparent failure due to DNS.

Verify:

- Resolver reachability
- Resolver routing
- ISP-specific DNS dependencies
- Public DNS accessibility

Avoid relying exclusively on provider DNS if the design requires ISP independence.

---

## Monitoring

Monitor both WAN paths independently.

Recommended metrics include:

- Interface state
- Gateway reachability
- External probe reachability
- Latency
- Packet loss
- Active default route
- NAT behavior
- Public IP
- VPN state

---

## Validation Tests

A planned failover test should verify:

1. Primary WAN normal operation
2. Primary route active
3. Primary NAT working
4. Backup path reachable
5. Primary failure detected
6. Backup route becomes active
7. New sessions use backup WAN
8. Backup NAT works
9. DNS still works
10. Monitoring detects failover
11. Primary recovery detected
12. Failback behaves as designed

---

## Controlled Failure Testing

Possible tests include:

- Disconnect primary WAN cable
- Disable primary interface
- Block monitored upstream path
- Simulate gateway loss

Testing should occur during an approved maintenance window.

Do not perform uncontrolled production failover testing.

---

## Troubleshooting Sequence

If failover does not occur:

1. Verify backup interface state
2. Verify backup gateway
3. Verify backup route
4. Verify route preference
5. Verify monitoring probes
6. Verify probe source interface
7. Verify IP-monitoring action
8. Verify security policy
9. Verify backup source NAT
10. Verify active route
11. Verify session behavior
12. Review logs

---

## Failover Occurs but Internet Still Fails

Possible causes include:

- Backup NAT missing
- Backup security policy missing
- Backup DNS unavailable
- Wrong backup route
- ISP issue
- Return routing problem
- Old sessions still bound to primary path

Test with new sessions after failover.

---

## Important Notes

This example uses documentation-only IP addresses.

Do not copy these values into production.

Do not assume:

- ge-0/0/0.0 is the primary WAN
- ge-0/0/2.0 is the backup WAN
- separate untrust zones are required
- interface NAT is always best
- one probe target is sufficient
- inbound services fail over automatically
- existing sessions survive failover

Design should reflect the actual ISP topology.

---

## Public Release Guidance

Before publishing dual-WAN examples:

- Remove real ISP names
- Remove real public IP addresses
- Remove circuit identifiers
- Remove internal hostnames
- Remove monitoring targets tied to the deployment
- Replace environment-specific values with documentation examples

---

## AI Guidance

When using this example:

- Treat all interfaces and addresses as examples.
- Distinguish link failure from upstream path failure.
- Do not assume dual WAN means inbound redundancy.
- Verify NAT for each egress path.
- Verify routing independently.
- Verify monitoring logic independently.
- Expect existing sessions to potentially break during failover.
- Recommend controlled maintenance-window testing.
- Verify Junos version before generating RPM or IP-monitoring syntax.

---

## Document Status

Document Type: Design Example

Example Type: Dual-WAN Failover Concepts

Knowledge Base: Juniper SRX320 Knowledge Base

Version: 0.1.0

Status: Example / Non-Production
