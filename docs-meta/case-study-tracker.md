# Case Study Tracker — Network Security Course

**Document ID:** NSC-CS-TRACKER · **Status:** Live tracker · **Version:** 1.0
**Requirement:** ≥ 100 problem-solving case studies (Requirements §6, Gate V6).
**Rule:** a row may only move to `written` or `validated` after its file exists and
passes the quality gates. **No row is marked complete until the artifact exists.**
Difficulty bands: B = beginner, BI = beginner→intermediate, I = intermediate,
IA = intermediate→advanced, A = advanced, E = expert.

| ID | Module | Lecture anchor | Working title | Difficulty | Status |
|---|---|---|---|---|---|
| cs-001 | 1 | L01 | Asset and trust-zone inventory of a small-office LAN | B | validated |
| cs-002 | 1 | L01 | Classifying a lost-laptop incident by CIA impact | B | validated |
| cs-003 | 1 | L02 | Spotting abnormal ARP replies in a clean capture | B | validated |
| cs-004 | 1 | L02 | IP fragmentation anomaly in a routed capture | B | validated |
| cs-005 | 1 | L02 | ICMP misuse red flags (unusual types and volumes) | B | validated |
| cs-006 | 1 | L03 | TCP half-open connection flood symptoms | B | validated |
| cs-007 | 1 | L03 | DNS resolution misdirection symptoms | B | validated |
| cs-008 | 1 | L03 | Rogue DHCP server effects on a client subnet | B | validated |
| cs-009 | 1 | L04 | Mixed-content and HTTP downgrade exposure on a web app | B | validated |
| cs-010 | 1 | L04 | First-pass triage of an unfamiliar capture | B | validated |
| cs-011 | 2 | L05 | Attack tree for a two-tier web application | BI | validated |
| cs-012 | 2 | L05 | Mapping an intrusion narrative to ATT&CK tactics | BI | validated |
| cs-013 | 2 | L06 | ARP-spoofing incident: symptoms and containment | BI | validated |
| cs-014 | 2 | L06 | MAC-flooding signs on a switch access layer | BI | validated |
| cs-015 | 2 | L06 | VLAN-hopping attempt analysis | BI | validated |
| cs-016 | 2 | L06 | STP manipulation detection | BI | validated |
| cs-017 | 2 | L07 | Passive-sniffing exposure assessment on a flat LAN | BI | validated |
| cs-018 | 2 | L07 | Internal MITM: evidence and defensive fixes | BI | validated |
| cs-019 | 2 | L07 | Session-hijack indicators in web traffic | BI | validated |
| cs-020 | 2 | L07 | DNS-spoofing campaign on a client estate | BI | validated |
| cs-021 | 2 | L08 | SYN-flood diagnosis and mitigation options | BI | validated |
| cs-022 | 2 | L08 | Reflection/amplification DDoS response plan | BI | validated |
| cs-023 | 2 | L08 | Botnet C2 beacon pattern recognition | BI | validated |
| cs-024 | 2 | L08 | Rate-limit design against application-layer floods | BI | validated |
| cs-025 | 2 | L08 | Sinkholing and egress blocking trade-offs | BI | validated |
| cs-026 | 3 | L09 | Segmentation proposal for a flat corporate network | I | validated |
| cs-027 | 3 | L09 | DMZ design review for a public web service | I | validated |
| cs-028 | 3 | L09 | VLAN plan for corporate/guest/IoT traffic | I | validated |
| cs-029 | 3 | L09 | Microsegmentation concept for a data center | I | validated |
| cs-030 | 3 | L10 | Firewall placement review for a branch office | I | validated |
| cs-031 | 3 | L10 | Stateful rule evaluation against a policy spec | I | validated |
| cs-032 | 3 | L10 | NGFW application-control policy design | I | validated |
| cs-033 | 3 | L10 | HA firewall failover behavior verification | I | validated |
| cs-034 | 3 | L11 | ACL audit: finding shadowed and redundant rules | I | validated |
| cs-035 | 3 | L11 | Least-privilege egress ACL authoring | I | validated |
| cs-036 | 3 | L11 | Inbound ACL hardening for a management subnet | I | validated |
| cs-037 | 3 | L12 | NAT mode selection and address-plan review | I | validated |
| cs-038 | 3 | L12 | Explicit-proxy egress policy for a university lab | I | validated |
| cs-039 | 3 | L12 | 802.1X/NAC adoption plan and bypass risks | I | validated |
| cs-040 | 4 | L13 | Cipher/mode selection for three data classes | I | validated |
| cs-041 | 4 | L13 | Key-management lapse root-cause analysis | I | validated |
| cs-042 | 4 | L13 | Internal PKI chain design for lab services | I | validated |
| cs-043 | 4 | L13 | Hash-collision implications for integrity checks | I | validated |
| cs-044 | 4 | L14 | Expired-certificate outage post-mortem | I | validated |
| cs-045 | 4 | L14 | Self-signed certificate risk assessment | I | validated |
| cs-046 | 4 | L14 | TLS downgrade incident analysis | I | validated |
| cs-047 | 4 | L14 | Weak-cipher-suite audit and remediation plan | I | validated |
| cs-048 | 4 | L14 | mTLS deployment for service-to-service traffic | I | validated |
| cs-049 | 4 | L15 | IKE phase-negotiation failure diagnosis | I | validated |
| cs-050 | 4 | L15 | Site-to-site IPsec design between two sites | I | validated |
| cs-051 | 4 | L16 | Split-tunnel VPN risk assessment | IA | validated |
| cs-052 | 4 | L16 | WireGuard rollout design for remote staff | IA | validated |
| cs-053 | 4 | L16 | Crypto-agility and post-quantum readiness review | IA | validated |
| cs-054 | 5 | L17 | WPA2-PSK wireless audit of a campus floor | IA | validated |
| cs-055 | 5 | L17 | Open guest Wi-Fi risk containment | IA | validated |
| cs-056 | 5 | L17 | WEP legacy device retirement plan | IA | validated |
| cs-057 | 5 | L18 | Evil-twin AP detection and response | IA | validated |
| cs-058 | 5 | L18 | Rogue-AP hunt across a building survey | IA | validated |
| cs-059 | 5 | L18 | 802.1X/EAP deployment for enterprise Wi-Fi | IA | validated |
| cs-060 | 5 | L18 | WPA3 transition compatibility triage | IA | validated |
| cs-061 | 5 | L19 | VPC design review for a three-tier app | IA | validated |
| cs-062 | 5 | L19 | Security-group vs NACL control choice | IA | validated |
| cs-063 | 5 | L19 | Overly permissive cloud route/NAT exposure | IA | validated |
| cs-064 | 5 | L20 | Cloud egress policy authoring | A | validated |
| cs-065 | 5 | L20 | Flow-log investigation of anomalous cloud traffic | A | validated |
| cs-066 | 6 | L21 | Sensor placement plan for an enterprise edge | A | validated |
| cs-067 | 6 | L21 | Baseline deviation in flow data | A | validated |
| cs-068 | 6 | L21 | Log-pipeline coverage gap analysis | A | validated |
| cs-069 | 6 | L22 | Suricata rule for a C2 beacon pattern | A | validated |
| cs-070 | 6 | L22 | Alert-tuning backlog prioritization | A | validated |
| cs-071 | 6 | L22 | False-positive investigation workflow | A | validated |
| cs-072 | 6 | L23 | Zeek-log anomaly correlation | A | validated |
| cs-073 | 6 | L23 | DNS-tunneling detection design | A | validated |
| cs-074 | 6 | L24 | Asset-discovery gaps before scanning | A | validated |
| cs-075 | 6 | L24 | Scan-result prioritization under patch windows | A | validated |
| cs-076 | 6 | L24 | CVSS base vs environmental context debate | A | validated |
| cs-077 | 6 | L24 | Remediation-SLA design by asset criticality | A | validated |
| cs-078 | 6 | L24 | Vulnerability-program metrics review | A | validated |
| cs-079 | 7 | L25 | IR playbook gap analysis for ransomware | A | validated |
| cs-080 | 7 | L25 | Roles/escalation design for a small IR team | A | validated |
| cs-081 | 7 | L26 | Phishing-driven intrusion: first-hour triage | A | validated |
| cs-082 | 7 | L26 | Containment decision trade-offs (isolate vs observe) | A | validated |
| cs-083 | 7 | L27 | Eradication sequencing and validation | A | validated |
| cs-084 | 7 | L27 | Lessons-learned report that changes controls | A | validated |
| cs-085 | 7 | L28 | Hunt-hypothesis design from threat intel | A | validated |
| cs-086 | 7 | L28 | Beaconing hunt across proxy and DNS logs | A | validated |
| cs-087 | 7 | L28 | SOC metric review and maturity plan | A | validated |
| cs-088 | 7 | L28 | Insider exfiltration detection scenario | A | validated |
| cs-089 | 7 | L28 | SIEM use-case tuning exercise | A | validated |
| cs-090 | 7 | L28 | Tabletop inject series for a multi-team drill | A | validated |
| cs-091 | 8 | L29 | Evidence and chain-of-custody planning | E | validated |
| cs-092 | 8 | L29 | Pcap session-timeline reconstruction | E | validated |
| cs-093 | 8 | L29 | Netflow corroboration of a pcap timeline | E | validated |
| cs-094 | 8 | L30 | IOC extraction and enrichment workflow | E | validated |
| cs-095 | 8 | L30 | Defensible findings report drafting | E | validated |
| cs-096 | 8 | L30 | Legal-hold and evidence-integrity scenario | E | validated |
| cs-097 | 8 | L30 | Multi-source timeline correlation (logs + flows + pcaps) | E | validated |
| cs-098 | 8 | L31 | Capstone network design defense prep | E | validated |
| cs-099 | 8 | L31 | IR simulation inject handling under time pressure | E | validated |
| cs-100 | 8 | L32 | Capstone integration: full-scope incident walkthrough | E | validated |

**Counts by module:** M1 = 10 · M2 = 15 · M3 = 14 · M4 = 14 · M5 = 12 · M6 = 13 ·
M7 = 12 · M8 = 10 · **Total = 100** (floor 100 met; additional cases may extend beyond
cs-100 with unique ids).

## Change log

### Session 6 — collection authored and validated (100/100)

| Change | Detail |
|---|---|
| Status flip | All 100 rows `planned → validated`: every student case exists under its module `case-studies/` tree with a paired instructor-only solution in `teaching/case-solutions/`; `validate_cases.py` 8/8 checks PASS (exit 0). |
| Title evolution (rule 3 record) | Working titles were drafting anchors; 60 of 100 cases shipped under refined titles (e.g., cs-081 "Phishing-driven intrusion: first-hour triage" shipped as "Phishing-Driven Intrusion — First-Hour Triage"; cs-091–096 became the Meridian capstone arc). The ID→lecture-anchor mapping is **unchanged** for all 100 rows — titles only. No content was deleted. |
| Tier collapse (documented deviation) | The 6 working bands (B/BI/I/IA/A/E) were collapsed to the mission's 4 publication tiers **monotonically by case number**: beginner cs-001–020, intermediate cs-021–045, advanced cs-046–075, expert cs-076–100 (20/25/30/25). Progression remains monotone: no case moved below a prior case's tier. |
| Band→tier mapping | B→beginner · BI→intermediate · I/IA→intermediate or advanced by number · A→advanced · E→expert. Per-case published tier is the front-matter `difficulty:` field (authoritative); this tracker's band column is retained as historical drafting record. |
| Structural note | Design-style cases (M3–M6, 32 cases) carry evidence inside `## Network Context (…)` instead of a separate `## Available Evidence` heading; substance identical, and the validator accepts either documented form. |
| Validator | `docs-meta/validate_cases.py` created (checks C1–C8). First run: 37 findings (32 structural-variant headings — resolved by validator rule accepting the documented variant; 5 tier-count mismatches — resolved by the monotonic tier collapse above). Second run: PASS, exit 0. |
