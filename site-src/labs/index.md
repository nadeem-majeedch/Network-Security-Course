---
status: complete
artifact-type: lab-workbook-page
instructor-only: false
---

# Lab Workbook

Sixteen graded labs run embedded in the 2-hour lecture blocks across the
16 weeks. Every handout follows the same structure: objectives, CLO mapping,
setup, **authorization & safety notes**, student tasks, expected observations,
analysis questions, troubleshooting, cleanup, and submission requirements.
Instructor answer keys live **outside** this website by policy.

> **Authorization frame:** all labs target the isolated course lab range,
> prepared packet captures, or simulated environments. Never apply these
> techniques to systems you do not own or have written authorization to test.

| Lab | Title | Week | Module | CLOs |
|---|---|---|---|---|
| 01 | [Range Orientation & Security Baseline](lab-01-range-orientation-baseline.md) | 1 | [M1](../modules/m01/index.md) | CLO-1 |
| 02 | [Packet Capture & Protocol Analysis](lab-02-wireshark-protocol-analysis.md) | 2 | [M1](../modules/m01/index.md) | CLO-1 |
| 03 | [Layer-2 Attack Evidence Analysis](lab-03-l2-attack-evidence-analysis.md) | 3 | [M2](../modules/m02/index.md) | CLO-2 |
| 04 | [MITM & Flood Telemetry Analysis](lab-04-mitm-flood-telemetry.md) | 4 | [M2](../modules/m02/index.md) | CLO-2 |
| 05 | [Segmentation & Proxy Egress Design](lab-05-segmentation-proxy-egress-design.md) | 5 | [M3](../modules/m03/index.md) | CLO-3, CLO-4 |
| 06 | [Firewall Rulebase & ACL Audit](lab-06-firewall-rulebase-acl-audit.md) | 6 | [M3](../modules/m03/index.md) | CLO-3, CLO-4 |
| 07 | [Lab PKI & TLS Configuration Audit](lab-07-pki-tls-audit.md) | 7 | [M4](../modules/m04/index.md) | CLO-5, CLO-6 |
| 08 | [Site-to-Site VPN Build & Evaluate](lab-08-site-to-site-vpn.md) | 8 | [M4](../modules/m04/index.md) | CLO-6 |
| 09 | [Wireless Characterization & Cloud Segmentation](lab-09-wireless-characterization-cloud-segmentation.md) | 9 | [M5](../modules/m05/index.md) | CLO-7, CLO-13 |
| 10 | [WPA-Enterprise Build & Cloud Flow Logs](lab-10-wpa-enterprise-cloud-flow-logs.md) | 10 | [M5](../modules/m05/index.md) | CLO-7, CLO-13 |
| 11 | [Flow Collector & Suricata Ruleset](lab-11-flow-collector-suricata.md) | 11 | [M6](../modules/m06/index.md) | CLO-8, CLO-9 |
| 12 | [Zeek Analysis & Vulnerability/Hardening Cycle](lab-12-zeek-vulnerability-hardening-cycle.md) | 12 | [M6](../modules/m06/index.md) | CLO-9, CLO-10 |
| 13 | [Incident Triage on a Staged Intrusion](lab-13-incident-triage.md) | 13 | [M7](../modules/m07/index.md) | CLO-11 |
| 14 | [Tabletop & Guided Threat Hunt](lab-14-tabletop-threat-hunt.md) | 14 | [M7](../modules/m07/index.md) | CLO-11, CLO-12 |
| 15 | [Forensic Timeline & Findings Report](lab-15-forensic-timeline-report.md) | 15 | [M8](../modules/m08/index.md) | CLO-14 |
| 16 | [Capstone IR Simulation](lab-16-capstone-ir-simulation.md) | 16 | [M8](../modules/m08/index.md) | CLO-11, CLO-15 |

## Tooling

Wireshark/tshark, Suricata, Zeek, pfSense VMs, containerized lab targets, and
a small cloud sandbox account provisioned by the instructor. Full environment
specs are in each handout's *Required software and hardware* section; dataset provenance
is documented in each handout's setup section.

## Grading

Each lab is graded from its submission checklist via the rubric in the
handout (structure, evidence quality, analysis depth, defensive reasoning).
The four graded lab practicals (Labs 06, 07, 10, 11 — Pract-1…4) feed the lab-assessment
component of the final grade — see [Assessments](../assessment/index.md).
