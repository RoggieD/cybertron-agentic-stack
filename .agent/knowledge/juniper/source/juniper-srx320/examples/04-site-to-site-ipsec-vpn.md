# Juniper SRX320 Route-Based Site-to-Site IPsec VPN Example

## Scope

This example demonstrates the structure of a route-based site-to-site IPsec VPN using a secure tunnel interface.

It demonstrates:

- IKE proposal
- IKE policy
- IKE gateway
- IPsec proposal
- IPsec policy
- IPsec VPN
- st0 tunnel interface
- VPN security zone
- Static routing
- Bidirectional security policies
- Verification and troubleshooting

This configuration is an educational example only.

It is not production configuration.

---

## Example Topology

### Local Site

Local Public IP:

198.51.100.10

Local LAN:

192.0.2.0/24

WAN Interface:

ge-0/0/0.0

LAN Zone:

trust

WAN Zone:

untrust

VPN Zone:

vpn

### Remote Site

Remote Public IP:

203.0.113.10

Remote LAN:

203.0.113.128/25

### Tunnel

Secure Tunnel Interface:

st0.0

---

## Traffic Objective

Traffic between:

192.0.2.0/24

and:

203.0.113.128/25

should traverse the encrypted IPsec tunnel.

Routing determines that the remote network is reachable through:

st0.0

Security policies separately determine whether traffic is permitted.

---

## Configure Secure Tunnel Interface

Create the logical tunnel interface:

set interfaces st0 unit 0 family inet

This example uses an unnumbered point-to-point tunnel interface.

Actual deployments may use numbered tunnel interfaces when required by routing or design.

---

## Create VPN Security Zone

Create a dedicated VPN zone:

set security zones security-zone vpn interfaces st0.0

---

## Configure IKE Proposal

Create an IKE proposal:

set security ike proposal SITE-A-IKE-PROPOSAL authentication-method pre-shared-keys

set security ike proposal SITE-A-IKE-PROPOSAL dh-group group14

set security ike proposal SITE-A-IKE-PROPOSAL authentication-algorithm sha-256

set security ike proposal SITE-A-IKE-PROPOSAL encryption-algorithm aes-256-cbc

set security ike proposal SITE-A-IKE-PROPOSAL lifetime-seconds 28800

These parameters are examples only.

Actual cryptographic settings must match the remote peer and should be selected according to current security requirements and Junos support.

---

## Configure IKE Policy

Create an IKE policy referencing the proposal:

set security ike policy SITE-A-IKE-POLICY proposals SITE-A-IKE-PROPOSAL

This example uses IKEv2 only.

IKEv1 main/aggressive negotiation mode is therefore not configured.

Configure the pre-shared key:

set security ike policy SITE-A-IKE-POLICY pre-shared-key ascii-text "<REPLACE-WITH-SECURE-PSK>"

Do not store production pre-shared keys in public documentation.

---

## Configure IKE Gateway

Create the remote IKE gateway:

set security ike gateway SITE-A-GATEWAY ike-policy SITE-A-IKE-POLICY

set security ike gateway SITE-A-GATEWAY address 203.0.113.10

set security ike gateway SITE-A-GATEWAY external-interface ge-0/0/0.0

set security ike gateway SITE-A-GATEWAY version v2-only

The remote peer must support the selected IKE version.

---

## Configure IPsec Proposal

Create an IPsec proposal:

set security ipsec proposal SITE-A-IPSEC-PROPOSAL protocol esp

set security ipsec proposal SITE-A-IPSEC-PROPOSAL authentication-algorithm hmac-sha-256-128

set security ipsec proposal SITE-A-IPSEC-PROPOSAL encryption-algorithm aes-256-cbc

set security ipsec proposal SITE-A-IPSEC-PROPOSAL lifetime-seconds 3600

These parameters are examples only.

They must match the remote peer.

---

## Configure IPsec Policy

Create the IPsec policy:

set security ipsec policy SITE-A-IPSEC-POLICY perfect-forward-secrecy keys group14

set security ipsec policy SITE-A-IPSEC-POLICY proposals SITE-A-IPSEC-PROPOSAL

---

## Configure IPsec VPN

Create the VPN object:

set security ipsec vpn SITE-A-VPN bind-interface st0.0

set security ipsec vpn SITE-A-VPN ike gateway SITE-A-GATEWAY

set security ipsec vpn SITE-A-VPN ike ipsec-policy SITE-A-IPSEC-POLICY

set security ipsec vpn SITE-A-VPN establish-tunnels immediately

---

## Configure Route to Remote Network

Route the remote network through the secure tunnel:

set routing-options static route 203.0.113.128/25 next-hop st0.0

Routing, not the security policy, determines that traffic should use the route-based VPN.

---

## Create Remote Network Address Object

Create an address object for the remote network:

set security zones security-zone vpn address-book address REMOTE-LAN 203.0.113.128/25

---

## Create Local Network Address Object

Create an address object for the local LAN:

set security zones security-zone trust address-book address LOCAL-LAN 192.0.2.0/24

---

## Allow Local-to-Remote Traffic

Create a policy from trust to vpn:

set security policies from-zone trust to-zone vpn policy LOCAL-TO-SITE-A match source-address LOCAL-LAN

set security policies from-zone trust to-zone vpn policy LOCAL-TO-SITE-A match destination-address REMOTE-LAN

set security policies from-zone trust to-zone vpn policy LOCAL-TO-SITE-A match application any

set security policies from-zone trust to-zone vpn policy LOCAL-TO-SITE-A then permit

---

## Allow Remote-to-Local Traffic

Create the reverse-direction policy:

set security policies from-zone vpn to-zone trust policy SITE-A-TO-LOCAL match source-address REMOTE-LAN

set security policies from-zone vpn to-zone trust policy SITE-A-TO-LOCAL match destination-address LOCAL-LAN

set security policies from-zone vpn to-zone trust policy SITE-A-TO-LOCAL match application any

set security policies from-zone vpn to-zone trust policy SITE-A-TO-LOCAL then permit

For production use, replace application any with specific applications whenever practical.

---

## NAT Considerations

Site-to-site VPN traffic normally should not be accidentally source-NATed to the Internet-facing address.

Review existing source NAT rule sets carefully.

If source NAT rules are broad, ensure VPN traffic does not unintentionally match them.

Do not add NAT exemptions blindly.

Verify actual NAT processing and traffic design first.

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

## Safe Commit

If management access could be affected:

commit confirmed

Verify management and VPN behavior before confirming the commit.

---

## Verify Tunnel Interface

Run:

show interfaces st0 terse

Verify that:

st0.0

exists and is in the expected state.

---

## Verify IKE Security Association

Run:

show security ike security-associations

For more detail:

show security ike security-associations detail

Verify that the expected peer has an established IKE association.

---

## Verify IPsec Security Association

Run:

show security ipsec security-associations

For more detail:

show security ipsec security-associations detail

Verify that an IPsec security association exists for the VPN.

---

## Verify Route

Run:

show route 203.0.113.128/25

The active route should direct the remote network through:

st0.0

---

## Verify Security Policies

Run:

show security policies

Verify both directions:

trust -> vpn

vpn -> trust

---

## Verify Sessions

During traffic testing:

show security flow session

Where useful:

show security flow session source-prefix 192.0.2.0/24

or:

show security flow session destination-prefix 203.0.113.128/25

---

## Expected Traffic Flow

### Local to Remote

1. Host in 192.0.2.0/24 sends traffic to 203.0.113.128/25.
2. SRX receives the packet from the trust zone.
3. Route lookup selects st0.0.
4. Destination zone is vpn.
5. LOCAL-TO-SITE-A policy permits the traffic.
6. IPsec processing encrypts the packet.
7. Encrypted traffic exits the WAN interface toward the remote peer.

### Remote to Local

1. Encrypted traffic arrives from the remote peer.
2. IPsec processing decrypts the packet.
3. Traffic enters through st0.0 in the vpn zone.
4. Routing selects the local LAN.
5. SITE-A-TO-LOCAL policy permits the traffic.
6. Traffic exits toward the local host.

---

## Troubleshooting Sequence

If the VPN does not work, troubleshoot in layers.

### Peer Reachability

Verify:

- Remote public IP
- WAN routing
- ISP connectivity
- External interface

### IKE

Verify:

- IKE version
- Pre-shared key
- Encryption
- Authentication
- Diffie-Hellman group
- Peer address

### IPsec

Verify:

- IPsec proposal
- PFS
- Encryption
- Authentication
- Security association state

### Tunnel Interface

Verify:

- st0.0 exists
- st0.0 is in the expected zone

### Routing

Verify:

- Remote route
- Local route
- Return route

### Security Policies

Verify:

- trust to vpn
- vpn to trust
- Address objects
- Applications

### NAT

Verify that VPN traffic is not being translated unexpectedly.

### Application

Test the actual application across the tunnel.

An established VPN does not prove application connectivity.

---

## Traffic Selectors

Some deployments, especially interoperability with third-party VPN peers, may require explicit traffic selectors.

Traffic selectors may define:

- Local prefix
- Remote prefix
- Protocol
- Source port
- Destination port

Do not add traffic selectors unless the VPN design or peer requirements call for them.

---

## Important Notes

This example uses documentation-only IP address ranges.

Do not copy these addresses into production.

Do not assume:

- ge-0/0/0.0 is the WAN interface
- st0.0 is available
- trust, untrust, and vpn are the correct zone names
- group14 is appropriate for every deployment
- AES-256-CBC is the preferred algorithm for every Junos release
- IKEv2 is supported by every remote peer
- application any is appropriate for production
- no traffic selectors are required

Verify platform, Junos version, and peer requirements.

---

## Security Guidance

For production deployments:

- Use strong cryptographic algorithms supported by both peers
- Protect pre-shared keys
- Prefer certificates where appropriate
- Restrict traffic with specific security policies
- Monitor VPN state
- Monitor application reachability
- Review VPN configuration periodically
- Replace obsolete cryptographic algorithms

---

## Public Release Guidance

Before publishing VPN examples:

- Remove real peer IP addresses
- Remove pre-shared keys
- Remove private keys
- Remove internal network information
- Remove internal hostnames
- Replace sensitive values with documentation examples

Never distribute live VPN secrets.

---

## AI Guidance

When using this example:

- Treat all IP addresses as examples.
- Never invent VPN credentials.
- Never expose production pre-shared keys.
- Verify Junos version.
- Verify remote-peer requirements.
- Verify IKE before IPsec.
- Verify IPsec before application troubleshooting.
- Verify routing separately.
- Verify security policies separately.
- Verify NAT separately.
- Do not assume an established tunnel means the service is working.

---

## Document Status

Document Type: Configuration Example

Example Type: Route-Based Site-to-Site IPsec VPN

Knowledge Base: Juniper SRX320 Knowledge Base

Version: 0.1.0

Status: Example / Non-Production
