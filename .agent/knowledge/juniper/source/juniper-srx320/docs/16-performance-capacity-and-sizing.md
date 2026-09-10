# Juniper SRX320 Performance, Capacity, and Sizing

## Scope

This document explains performance, capacity, and sizing considerations for the Juniper SRX320.

It is intended for:

- Deployment planning
- Capacity review
- Performance troubleshooting
- Firewall replacement decisions
- WAN sizing
- VPN sizing
- Monitoring
- AI-assisted infrastructure analysis

This document provides platform-level guidance and does not represent a specific production performance baseline unless explicitly labeled.

---

## Performance Philosophy

Firewall sizing should be based on actual workload, not only advertised maximum throughput.

Real-world performance can be affected by:

- Security services
- Packet size
- Session count
- NAT
- VPN encryption
- Logging
- Routing
- Application mix
- Traffic direction
- Concurrent connections
- Software version
- Feature configuration

Published platform specifications should be treated as design inputs, not guaranteed production results.

---

## Key Capacity Dimensions

Important capacity dimensions include:

- Firewall throughput
- IPsec VPN throughput
- Maximum concurrent sessions
- New sessions per second
- Interface bandwidth
- CPU utilization
- Memory utilization
- Packet rate
- Logging volume

No single metric describes total device capacity.

---

## Throughput

Throughput measures the amount of traffic forwarded over time.

Common units include:

- Mbps
- Gbps

Throughput should be evaluated separately for:

- Plain firewall traffic
- NAT traffic
- VPN traffic
- Traffic with additional inspection features

Do not assume all traffic types achieve the same throughput.

---

## Packet Size

Packet size can materially affect firewall performance.

A device may process fewer packets per second when handling a large number of small packets compared with larger packets at the same bandwidth.

Performance analysis should consider:

- Bandwidth
- Packet rate
- Average packet size

---

## Packets Per Second

Packets per second can be a more useful metric than bandwidth for certain workloads.

High packet-rate workloads may include:

- DNS
- VoIP
- Gaming
- Scanning
- DDoS traffic
- Small transactional packets

A link may be far below maximum bandwidth while still creating high packet-processing load.

---

## Concurrent Sessions

Stateful firewalls maintain connection state.

Concurrent session load may increase with:

- Large user populations
- Web browsing
- Cloud applications
- Streaming
- NAT
- Server publishing
- Scanning
- Long-lived sessions

Session capacity should be considered independently from bandwidth.

---

## New Sessions Per Second

New session creation rate can affect performance.

High session-establishment workloads may occur during:

- Application bursts
- Large client populations
- Web traffic spikes
- Scanning activity
- DDoS events

A device may have available bandwidth while becoming constrained by session creation rate.

---

## CPU Utilization

CPU usage should be monitored during:

- Peak traffic
- VPN activity
- Heavy logging
- Routing changes
- Configuration commits
- Troubleshooting traces
- Attack traffic

Short CPU spikes may be normal.

Sustained high CPU requires investigation.

---

## Memory Utilization

Memory should be monitored for:

- Current usage
- Trend
- Session growth
- Process behavior
- System alarms

High memory usage alone does not automatically indicate failure.

Evaluate it in context.

---

## NAT Performance

NAT introduces state and translation processing.

Performance may be influenced by:

- Number of translations
- Session volume
- Translation pools
- Port utilization
- Bidirectional traffic
- Published services

NAT troubleshooting should include both resource usage and rule correctness.

---

## VPN Performance

VPN traffic adds encryption and decryption workload.

VPN performance depends on:

- Encryption algorithm
- Authentication algorithm
- Tunnel count
- Packet size
- Traffic volume
- Concurrent sessions
- Hardware acceleration
- Junos version

Do not assume plain firewall throughput equals VPN throughput.

---

## Logging Impact

Excessive logging can affect:

- CPU
- Storage
- Network utilization
- Remote syslog systems
- Troubleshooting clarity

Avoid enabling high-volume logging without a defined purpose.

---

## Flow Tracing Impact

Flow tracing can generate significant diagnostic data.

It should be:

- Narrowly scoped
- Used temporarily
- Disabled after troubleshooting

Broad tracing on a busy production firewall may materially affect performance.

---

## Interface Capacity

An interface should be monitored for:

- Utilization
- Errors
- Discards
- Drops
- Link speed
- Duplex
- Bursts
- Congestion

A firewall performance issue may actually be an interface or upstream-network issue.

---

## WAN Sizing

WAN capacity planning should consider:

- Internet circuit speed
- Expected peak usage
- Growth
- VPN traffic
- Public services
- Backup traffic
- Cloud applications
- Monitoring
- Protocol overhead

The firewall should have sufficient headroom above normal expected load.

---

## Headroom

Avoid designing a firewall to operate continuously near maximum capacity.

Operational headroom is useful for:

- Traffic bursts
- Growth
- Failover
- Attacks
- Logging spikes
- New services
- Troubleshooting

A device regularly operating near its limits should be reviewed for upgrade or traffic redistribution.

---

## Monitoring Baselines

Establish normal baselines for:

- CPU
- Memory
- WAN throughput
- LAN throughput
- Session count
- New sessions per second
- Interface errors
- VPN traffic
- Logging volume

Baseline data makes abnormal behavior easier to identify.

---

## Peak vs Average

Average utilization can hide short periods of saturation.

Monitor:

- Average
- Peak
- Sustained peak
- Time of day
- Day of week

Capacity decisions should consider peak behavior, not only monthly averages.

---

## Bottleneck Identification

A performance problem may originate in:

- SRX CPU
- SRX memory
- Interface
- WAN circuit
- Upstream router
- Switch
- Server
- DNS
- Application
- VPN peer
- Storage or logging infrastructure

Do not assume the firewall is the bottleneck without evidence.

---

## Useful Operational Commands

Commands may include:

show interfaces terse

show interfaces extensive

show system processes extensive

show system uptime

show security flow session summary

show security flow session

show system storage

show chassis alarms

show system alarms

Exact commands and available metrics may vary by Junos version.

---

## Performance Troubleshooting

When performance degrades, verify:

1. Scope of affected traffic
2. Time problem began
3. Interface utilization
4. Interface errors
5. CPU usage
6. Memory usage
7. Session count
8. New session rate
9. NAT behavior
10. VPN load
11. Logging volume
12. Routing
13. Upstream network health
14. Application health

---

## Capacity Review

A capacity review should document:

WAN Speed:

Peak WAN Utilization:

LAN Speed:

Peak LAN Utilization:

CPU Baseline:

CPU Peak:

Memory Baseline:

Memory Peak:

Concurrent Sessions:

New Sessions Per Second:

VPN Throughput:

Critical Interfaces:

Observed Bottlenecks:

Growth Estimate:

Recommended Headroom:

Configuration State:

Verification Date:

Notes:

---

## Upgrade Decision

Consider replacement or redesign when:

- Peak utilization consistently approaches practical limits
- Session load approaches supported capacity
- VPN requirements exceed platform performance
- Required interfaces are insufficient
- New security features materially reduce usable capacity
- Growth projections exceed available headroom
- Software support becomes limiting

Do not replace hardware based only on age if capacity and support remain adequate.

---

## Public Release Guidance

Before publishing performance examples:

- Remove customer traffic volumes where sensitive
- Remove internal hostnames
- Remove public IP addresses
- Remove topology-specific identifiers
- Remove proprietary business usage data

Preserve capacity-planning methodology while sanitizing deployment-specific information.

---

## AI Guidance

When using this document:

- Do not assume advertised throughput equals real-world throughput.
- Evaluate packet rate, sessions, VPN, and logging separately.
- Prefer measured data over theoretical limits.
- Distinguish average utilization from peak utilization.
- Identify the actual bottleneck before recommending hardware replacement.
- Verify Junos version and enabled features.
- Recommend headroom rather than continuous operation near maximum capacity.

---

## Document Status

Document Type: Performance, Capacity, and Sizing

Knowledge Base: Juniper SRX320 Knowledge Base

Version: 0.1.0

Status: Initial Build
