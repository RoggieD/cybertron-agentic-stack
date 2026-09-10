# Juniper SRX320 High Availability, Clustering, and Redundancy

## Scope

This document explains high-availability and redundancy concepts relevant to Juniper SRX platforms, including chassis clustering.

It is intended for:

- High-availability design
- Redundant firewall deployment
- Failure-domain planning
- Migration planning
- Operational troubleshooting
- AI-assisted infrastructure design

This document provides platform-level guidance and does not represent a specific production cluster configuration unless explicitly labeled.

---

## High Availability Overview

High availability is intended to reduce service interruption when a firewall component, interface, node, or path fails.

HA design may involve:

- Redundant SRX nodes
- Chassis clustering
- Redundant Ethernet links
- Redundant switches
- Redundant WAN connections
- Redundant power
- Redundant routing paths

High availability should be designed as an end-to-end system.

Two firewalls alone do not create complete redundancy.

---

## Chassis Cluster Concept

Junos chassis clustering allows two compatible SRX devices to operate as a coordinated security system.

The cluster may provide:

- Control-plane redundancy
- Data-plane redundancy
- Stateful failover
- Redundant interfaces
- Configuration synchronization
- Session synchronization where supported

Exact capabilities depend on platform and Junos version.

---

## Cluster Nodes

A chassis cluster typically contains two nodes.

Conceptually:

Node 0

Node 1

One node may hold the active role for a redundancy group while the other provides backup capability.

Different redundancy groups may control different resources.

---

## Redundancy Groups

Redundancy groups define failover ownership.

Common concepts include:

- Redundancy group 0
- Redundancy group 1 and higher

Redundancy group 0 commonly relates to control-plane redundancy.

Additional redundancy groups may manage data-plane interface ownership.

Exact behavior should be verified against the platform and Junos release.

---

## SRX320 Cluster Interface Repurposing

On an SRX320, enabling chassis clustering and rebooting changes the role and numbering of several built-in interfaces.

In chassis cluster mode:

- ge-0/0/0 is repurposed as the fxp0 management interface.
- ge-0/0/1 is repurposed as the fxp1 control-link interface.
- Interfaces on node 1 are renumbered using the SRX320 cluster offset.
- Fabric links are user-selected Gigabit Ethernet interfaces supported for the platform.

Any standalone configuration using ge-0/0/0 or ge-0/0/1 must therefore be reviewed before cluster formation.

Do not design an SRX320 cluster as though the standalone interface map remains unchanged after clustering is enabled.

---

## Control Link

Cluster nodes require communication for control-plane coordination.

Control links are used for functions such as:

- Cluster state
- Configuration synchronization
- Node coordination

A control-link failure can affect cluster operation.

---

## Fabric Link

Fabric links may carry traffic and state information between cluster nodes.

Depending on platform design, fabric connectivity may support:

- Session synchronization
- Packet forwarding
- State exchange

Fabric-link health is critical to stable cluster operation.

---

## Redundant Ethernet Interfaces

Redundant Ethernet interfaces may provide a logical interface backed by physical links on different cluster nodes.

A common Junos naming concept is:

reth

Example:

reth0

A reth interface may remain logically available if one node or member interface fails.

---

## Physical Member Interfaces

Physical interfaces may be assigned as members of a redundant Ethernet interface.

Documentation should record:

- Node
- Physical interface
- Redundant Ethernet interface
- Role
- Connected switch
- VLAN
- Security zone

Do not assume symmetric physical connectivity unless verified.

---

## Switch Redundancy

Firewall HA should consider upstream and downstream switching.

A cluster connected to only one physical switch may still have a major single point of failure.

Consider:

- Dual switches
- Independent power
- Link aggregation where appropriate
- Redundant uplinks
- Spanning-tree behavior
- VLAN consistency

---

## WAN Redundancy

Firewall clustering does not automatically provide ISP redundancy.

WAN resiliency may require:

- Multiple providers
- Multiple circuits
- Dynamic routing
- Static route tracking
- RPM or health monitoring
- Route preference
- Failover policy

The WAN design must be considered separately from firewall node redundancy.

---

## Failure Domains

Identify failure domains explicitly.

Examples include:

- SRX node failure
- Power supply failure
- Switch failure
- WAN circuit failure
- ISP failure
- Cable failure
- Interface failure
- Control-link failure
- Fabric-link failure
- Routing failure

A strong HA design minimizes shared failure domains.

---

## Stateful Failover

Stateful failover may preserve existing sessions when ownership moves between cluster nodes.

The effectiveness of failover depends on:

- Session synchronization
- Cluster health
- Interface design
- Routing
- NAT
- Application behavior
- Failure type

Do not assume all application sessions survive every type of failover.

---

## NAT and HA

NAT configuration in a cluster should be designed with failover behavior in mind.

Consider:

- Public IP ownership
- Redundant interfaces
- ARP behavior
- Upstream routing
- Session synchronization

NAT should continue functioning after failover.

---

## Routing and HA

Routing may participate in failover through:

- Static routing
- Dynamic routing
- Redundant interfaces
- Route tracking
- Upstream route convergence

Routing recovery time can affect application availability even if the firewall cluster itself fails over correctly.

---

## Security Policies and HA

Security policy should remain logically consistent across cluster nodes.

A clustered design should avoid configuration drift.

Configuration synchronization is therefore operationally important.

---

## Monitoring HA

HA monitoring should include:

- Node state
- Redundancy group state
- Control link
- Fabric link
- Redundant interfaces
- Physical member interfaces
- Cluster alarms
- Routing
- WAN state

A cluster can be partially degraded while still forwarding traffic.

---

## Useful Operational Concepts

Depending on platform and Junos version, useful operational commands may include commands related to:

- chassis cluster status
- redundancy group state
- interface state
- alarms
- system health

Exact syntax should be verified against the installed Junos version.

---

## Failover Testing

A high-availability design should be tested.

Possible controlled tests include:

- Interface failure
- Node failover
- Switch failure
- WAN failure
- Power failure

Testing should occur within an approved maintenance window.

Always document:

- Expected behavior
- Actual behavior
- Recovery time
- Session impact
- Monitoring alerts
- Rollback method

---

## Maintenance

HA can enable maintenance with reduced downtime, but failover should be validated before relying on it.

Before maintenance:

1. Verify both nodes are healthy.
2. Verify synchronization.
3. Verify redundancy groups.
4. Verify interface state.
5. Verify routing.
6. Verify monitoring.
7. Confirm rollback options.

---

## Split-Brain Risk

Cluster designs must avoid conditions where both nodes incorrectly believe they should act independently.

Control and fabric health are important to preventing inconsistent cluster behavior.

Exact safeguards depend on platform implementation.

---

## Configuration Backup

Cluster configuration should be backed up regularly.

Backups should include:

- Cluster configuration
- Node-specific configuration
- Interface mappings
- Redundancy groups
- Routing
- Security policies
- NAT
- Monitoring configuration

---

## Production HA Documentation

Production HA records should identify:

Cluster Name:

Node 0:

Node 1:

Junos Version:

Control Link:

Fabric Link:

Redundancy Groups:

Reth Interfaces:

Upstream Switches:

Downstream Switches:

WAN Design:

Routing Design:

Failover Method:

Monitoring:

Configuration State:

Verification Date:

Notes:

---

## Configuration States

Use:

LEGACY_PRODUCTION

SRX320_TARGET

SRX320_VERIFIED_PRODUCTION

Do not mark HA as verified until failover behavior has been tested.

---

## Public Release Guidance

Before publishing HA examples:

- Remove real IP addresses
- Remove internal hostnames
- Remove serial numbers
- Remove switch names
- Remove WAN circuit identifiers
- Remove customer-specific topology

Preserve HA architecture and troubleshooting logic while sanitizing deployment-specific information.

---

## AI Guidance

When using this document:

- Do not assume clustering is configured.
- Do not assume two firewalls means true redundancy.
- Identify shared failure domains.
- Treat WAN redundancy separately from firewall redundancy.
- Verify cluster health before recommending failover.
- Do not recommend uncontrolled failover testing in production.
- Prefer maintenance-window testing for disruptive HA validation.
- Distinguish design guidance from verified deployment state.

---

## Document Status

Document Type: High Availability, Clustering, and Redundancy

Knowledge Base: Juniper SRX320 Knowledge Base

Version: 0.1.0

Status: Initial Build
