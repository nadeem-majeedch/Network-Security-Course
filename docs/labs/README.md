# NS-401 Lab Curriculum — Index

Sixteen practical activities, one per week, embedded in the lecture blocks
(see syllabus §7). Labs are graded by evidence discipline: **partial-but-
documented beats undocumented-complete** — stated in Week 1, applied everywhere.

## The 16 labs

| Lab | Week | Title | Module | Primary CLO | Core-lab coverage (mission) |
|---|---|---|---|---|---|
| [Lab-01](lab-01-range-orientation-baseline.md) | 1 | Lab-Range Orientation, Baseline & Topology Documentation | 1 | CLO-1 | Baseline + topology documentation; first capture |
| [Lab-02](lab-02-wireshark-protocol-analysis.md) | 2 | Packet Capture & Protocol Analysis with Wireshark | 1 | CLO-1 | Wireshark analysis; TCP/DNS/DHCP investigation |
| [Lab-03](lab-03-l2-attack-evidence-analysis.md) | 3 | Layer-2 Attack Evidence Analysis (ARP/DHCP) | 2 | CLO-2 | DNS/DHCP/ARP traffic investigation |
| [Lab-04](lab-04-mitm-flood-telemetry.md) | 4 | MITM & Flood Telemetry Analysis | 2 | CLO-2 | Sniffing/DoS attack concepts as evidence |
| [Lab-05](lab-05-segmentation-proxy-egress-design.md) | 5 | Segmentation & Proxy Egress Design | 3 | CLO-3 | Segmentation & secure architecture design |
| [Lab-06](lab-06-firewall-rulebase-acl-audit.md) | 6 | Firewall Rulebase Build & ACL Audit (pfSense) | 3 | CLO-4 | Firewall rules & ACL design (**Pract-1**) |
| [Lab-07](lab-07-pki-tls-audit.md) | 7 | Lab PKI, TLS Configuration Audit | 4 | CLO-6 | TLS/certificate inspection (**Pract-2**) |
| [Lab-08](lab-08-site-to-site-vpn.md) | 8 | Site-to-Site VPN Build & Evaluate | 4 | CLO-7 | VPN concepts & configuration |
| [Lab-09](lab-09-wireless-characterization-cloud-segmentation.md) | 9 | Wireless Characterization + VPC Segmentation | 5 | CLO-8 | Wireless security analysis (safe) |
| [Lab-10](lab-10-wpa-enterprise-cloud-flow-logs.md) | 10 | WPA-Enterprise Build + Cloud Flow Logs | 5 | CLO-8, CLO-13 | Enterprise wireless & cloud assurance (**Pract-3**) |
| [Lab-11](lab-11-flow-collector-suricata.md) | 11 | Flow Collector + Suricata Ruleset | 6 | CLO-9 | IDS/IPS & monitoring (**Pract-4**) |
| [Lab-12](lab-12-zeek-vulnerability-hardening-cycle.md) | 12 | Zeek Analysis + Vulnerability→Hardening→Verify Cycle | 6 | CLO-10 | Vulnerability assessment; hardening & verification |
| [Lab-13](lab-13-incident-triage.md) | 13 | Incident Triage on a Staged Intrusion | 7 | CLO-11 | Incident response with network evidence |
| [Lab-14](lab-14-tabletop-threat-hunt.md) | 14 | IR Tabletop + Guided Threat Hunt | 7 | CLO-11, CLO-12 | IR preparation; hunting |
| [Lab-15](lab-15-forensic-timeline-report.md) | 15 | Forensic Timeline & Findings Report | 8 | CLO-14 | Network forensics discipline |
| [Lab-16](lab-16-capstone-ir-simulation.md) | 16 | Capstone IR Simulation | 8 | CLO-11, CLO-14, CLO-15 | Capstone integration |

## Datasets

Generated reproducibly by [`setup/generate_lab_datasets.py`](setup/generate_lab_datasets.py)
into [`datasets/`](datasets/) — verify before use: `sha256sum -c SHA256SUMS`
(checksums in [datasets/SHA256SUMS](datasets/SHA256SUMS)). All traffic in the
datasets is **synthetic and benign-shaped** — evidence for defensive analysis
only (the generator's docstring documents every scenario).

## Safety (binding — syllabus §9)

All hands-on work happens **only** inside the instructor-authorized lab range
against lab-owned targets. No out-of-scope scanning, no tooling applied to real
networks, no destructive payloads. Every lab's §Authorization & Safety Notes is
part of the graded artifact.
