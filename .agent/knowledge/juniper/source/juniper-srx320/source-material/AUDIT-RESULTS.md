# Juniper SRX320 Knowledge Base — Batch Technical Audit Results

## Audit Date

2026-09-09

## Scope

The uploaded knowledge base was reviewed as a package rather than document-by-document.

Reviewed:

- 17 core documentation files
- 10 configuration/design/troubleshooting examples
- 9 JSON Schema files
- validation manifest
- authoritative-source registry
- private production template

## Result

The package is suitable as a documentation-checked knowledge-base baseline, subject to the limitations below.

No content is being represented as live-device-verified.

The actual SRX320 Junos release remains unknown until serial or network access to the device is available.

## Corrections Made During Batch Audit

### Security policies

- Clarified that security policy lookup also applies between interfaces in the same zone.
- Clarified that an applicable permitting intrazone policy is required; factory-default trust policies can affect behavior on supported platforms.
- Replaced bare show security match-policies guidance with flow-criteria-based usage.

### NAT

- Clarified destination NAT processing relative to route and security-policy lookup.

### Management and version identification

- Corrected guidance that could imply show system software is the primary Junos version command.
- show version is now identified as the base Junos release command.

### Troubleshooting

- Strengthened flow-tracing warnings to reflect Juniper guidance concerning performance and security impact and JTAC supervision.

### Chassis clustering

- Added SRX320-specific cluster interface repurposing guidance.
- Documented that ge-0/0/0 becomes fxp0 and ge-0/0/1 becomes fxp1 after cluster formation/reboot.
- Added warning that standalone interface assumptions cannot be carried directly into cluster mode.

### Software upgrades

- Added stronger release-specific upgrade-path guidance for the SRX300 line.
- Explicitly requires current Juniper documentation before reusing request system software add options.

## Validation Levels

### documentation-checked

Means the content has been compared with authoritative Juniper documentation.

It does not mean the configuration has passed commit check on the target device.

### syntax-validated

Not yet achieved for the package as a whole.

Requires Junos syntax/commit validation on an appropriate release.

### lab-verified

Not yet achieved for the package as a whole.

### live-device-verified

Not yet achieved.

Live SRX320 access is still required.

## Remaining High-Priority Work

When the SRX320 is available through serial console:

1. Capture show version.
2. Capture show chassis hardware.
3. Capture show interfaces terse.
4. Capture show configuration interfaces.
5. Capture show configuration security zones.
6. Capture show configuration security policies.
7. Capture show configuration security nat.
8. Capture show route.
9. Establish the exact Junos release as the validation target.
10. Run commit-check validation only on controlled candidate configurations.

## Publication / Commercial Packaging

The current package separates general technical material from the private production record and uses reserved/documentation address space in examples.

Before public release, perform a final secret/topology scan and keep the private directory out of the public package even if it currently contains only placeholders.

Do not claim Juniper certification, Juniper endorsement, or live-device validation.

## Overall Status

Documentation Audit: COMPLETE

JSON Schema Structural Validation: COMPLETE

Example Documentation Audit: COMPLETE

Live SRX320 Validation: PENDING

Target Junos Version: UNKNOWN

Knowledge Base State: SRX320_TARGET
