# Course Architecture — Network Security

**Document ID:** NSC-ARCH-001 · **Status:** Approved baseline · **Version:** 1.0
**Normative pairing:** `course-requirements.md` (what) → this document (how it is structured)
**Related:** `content-inventory.md`, `implementation-roadmap.md`

---

## 1. Design Principles

1. **Defense-forward framing.** Attacks are taught to the depth needed to design,
   configure, and verify defenses; labs operate only inside authorized lab ranges.
2. **Protocol-first.** Every control is anchored to the protocol layer it protects or
   inspects, so students reason from packets upward rather than memorizing products.
3. **Progressive difficulty.** 8 modules rise from packet fundamentals (Module 1) to
   forensic reconstruction and capstone integration (Module 8); within each module,
   case studies and labs ramp from guided to open-ended.
4. **Every hour does double duty.** Each 2-hour lecture pairs ~70 minutes of core
   instruction with ~40 minutes of hands-on lab or case-study work and ~10 minutes of
   wrap-up/assessment, keeping the practical load high without extra contact hours.
5. **Instructor/student separation by construction.** Solutions and speaker notes are
   authored in `instructor/` from day one so publication separation is never a
   retrofit (Requirements §7.3).
6. **Validation as a gate, not a claim.** Content status moves `draft → review →
   complete` only after passing the gates in Requirements §9, with observed results
   recorded — never asserted.

## 2. Eight-Module Architecture

| # | Module | Lectures | Weeks | CLOs | Difficulty band |
|---|---|---|---|---|---|
| 1 | Network & Security Foundations | L01–L04 | 1–2 | CLO-1 | Beginner |
| 2 | Network Threats & Attack Surface | L05–L08 | 3–4 | CLO-2 | Beginner→Intermediate |
| 3 | Secure Network Architecture & Perimeter Controls | L09–L12 | 5–6 | CLO-3, CLO-4 | Intermediate |
| 4 | Cryptography & Secure Protocols | L13–L16 | 7–8 | CLO-5, CLO-6, CLO-7 | Intermediate |
| 5 | Wireless & Cloud Network Security | L17–L20 | 9–10 | CLO-8, CLO-13 | Intermediate→Advanced |
| 6 | Detection & Vulnerability Management | L21–L24 | 11–12 | CLO-9, CLO-10, CLO-12 | Advanced |
| 7 | Incident Response & Defense Operations | L25–L28 | 13–14 | CLO-11, CLO-12 | Advanced |
| 8 | Network Forensics & Capstone | L29–L32 | 15–16 | CLO-14, CLO-15 | Expert |

## 3. Master Lecture Map (32 lectures × 2 h = 64 contact hours)

### Module 1 — Network & Security Foundations (Beginner)

| Lec | Week | Title (2 h) | Core topics | Practice in session | CLO |
|---|---|---|---|---|---|
| L01 | 1 | Security Mindset & the Network Threat Landscape | CIA triad, threat/asset/risk, attacker classes, course ethics & authorization rules | Topology orientation lab; class threat-discussion | 1 |
| L02 | 1 | Protocol Deep Dive I — Ethernet, ARP, IP, ICMP | Frame anatomy, ARP resolution & cache, IP addressing, ICMP behavior & misuse | Wireshark: capture & annotate ARP/IP/ICMP exchanges | 1 |
| L03 | 2 | Protocol Deep Dive II — TCP, UDP, DNS, DHCP | Handshake & teardown, ports, DNS recursion, DHCP lease flow, protocol weaknesses | Wireshark: TCP streams + DNS/DHCP trace analysis | 1 |
| L04 | 2 | Applied Packet Analysis & Web Protocols | HTTP(S) on the wire, Wireshark filtering/dissection craft, packet triage workflow | Guided capture-analysis lab (Quiz 1 in week 2) | 1 |

### Module 2 — Network Threats & Attack Surface (Beginner→Intermediate)

| Lec | Week | Title (2 h) | Core topics | Practice in session | CLO |
|---|---|---|---|---|---|
| L05 | 3 | Threat Modeling & Attacker Anatomy | Cyber kill chain, MITRE ATT&CK tactics, attack trees, scoping a model | Build an attack tree for a lab network (Case set A) | 2 |
| L06 | 3 | Layer-2 & LAN Attacks | ARP spoofing, MAC flooding, STP manipulation, VLAN hopping — and each defense | Lab range: observe & detect L2 attack traffic | 2 |
| L07 | 4 | Sniffing, MITM & Session Attacks | Passive/active sniffing, MITM patterns, session hijacking, DNS spoofing — detection focus | Detect & document MITM in provided captures | 2 |
| L08 | 4 | DoS/DDoS & Infrastructure Abuse | Flood taxonomy, amplification/reflection, botnets, rate limiting & sinkholing | Analyze simulated flood telemetry (Quiz 2) | 2 |

### Module 3 — Secure Network Architecture & Perimeter Controls (Intermediate)

| Lec | Week | Title (2 h) | Core topics | Practice in session | CLO |
|---|---|---|---|---|---|
| L09 | 5 | Defense in Depth & Network Segmentation | Zones, VLANs, DMZ patterns, microsegmentation, zero-trust direction | Design exercise: segment a flat network (Case set B) | 3 |
| L10 | 6 | Firewalls: Concepts & Placement | Packet filter vs stateful vs NGFW, policy ordering, HA pairs, placement | Build a pfSense rulebase for a given policy | 3, 4 |
| L11 | 6 | ACLs & Rulebase Engineering | Router ACL semantics, rule auditing (shadowing, redundancy), least privilege | Write & audit ACLs against a policy spec | 4 |
| L12 | 5 | NAT, Proxies, Egress & NAC | NAT modes, explicit/transparent proxies, egress filtering, 802.1X/NAC overview | Proxy + egress policy lab (Quiz 3 in week 5) | 3 |

### Module 4 — Cryptography & Secure Protocols (Intermediate)

| Lec | Week | Title (2 h) | Core topics | Practice in session | CLO |
|---|---|---|---|---|---|
| L13 | 7 | Cryptographic Foundations | Symmetric vs asymmetric, hashes & HMAC, PKI & certificates, key lifecycle | OpenSSL: generate, sign, verify a lab PKI chain | 5 |
| L14 | 7 | TLS Deep Dive | Handshake (1.2 vs 1.3), cipher suites, certificate validation, common misconfigurations | TLS inspection with Wireshark + sslyze-style config audit | 6 |
| L15 | 8 | IPsec & Legacy VPN Architecture | IKE phases, tunnel vs transport, ESP/AH, site-to-site design | Wire up a site-to-site IPsec tunnel in the lab | 7 |
| L16 | 8 | Modern VPNs & Crypto Agility | WireGuard, TLS-VPN patterns, key rotation, post-quantum direction, VPN failure modes | Compare & evaluate VPN designs (Midterm, week 8) | 5, 7 |

### Module 5 — Wireless & Cloud Network Security (Intermediate→Advanced)

| Lec | Week | Title (2 h) | Core topics | Practice in session | CLO |
|---|---|---|---|---|---|
| L17 | 9 | Wireless Fundamentals & Threats | 802.11 operation, WEP→WPA2→WPA3 evolution, open/guest risks | Analyze a wireless capture; crack-nothing, characterize-what-you-see lab | 8 |
| L18 | 10 | Enterprise Wireless & Rogue Defense | 802.1X/EAP, RADIUS, WPA3-Enterprise, rogue AP & evil-twin defense | Build WPA2/WPA3-Enterprise auth in lab (Quiz 4) | 8 |
| L19 | 9 | Cloud Networking I — VPC Design & Controls | VPC/VNet design, security groups vs NACLs, route tables, NAT gateways | Cloud lab: build a segmented VPC with SG rules | 13 |
| L20 | 10 | Cloud Networking II — Hybrid & Assurance | Private endpoints, flow logs, hybrid connectivity, shared-responsibility deltas | Enable flow logs & write a cloud egress policy (Quiz 4) | 13 |

### Module 6 — Detection & Vulnerability Management (Advanced)

| Lec | Week | Title (2 h) | Core topics | Practice in session | CLO |
|---|---|---|---|---|---|
| L21 | 11 | Monitoring Foundations | Log sources, flow data (NetFlow/IPFIX), SIEM concepts, sensor placement | Build a flow-collector view of lab traffic | 12 |
| L22 | 11 | IDS/IPS — Signatures & Tuning | Snort/Suricata rule anatomy, alert tuning, false-positive management | Write & deploy custom Suricata rules (Case set C) | 9 |
| L23 | 12 | Zeek & Anomaly Detection | Zeek logs, protocol metadata, baselining, anomaly-driven alerts | Zeek log analysis & a custom notice policy | 9, 12 |
| L24 | 12 | Vulnerability Management Cycle | Asset discovery, Nessus/OpenVAS scanning, CVSS + context, remediation SLAs | Full scan→prioritize→remediate cycle on lab hosts (Assignment 5) | 10 |

### Module 7 — Incident Response & Defense Operations (Advanced)

| Lec | Week | Title (2 h) | Core topics | Practice in session | CLO |
|---|---|---|---|---|---|
| L25 | 13 | IR Lifecycle & Preparation | NIST 800-61 lifecycle, roles, playbooks, evidence handling basics | Draft an IR playbook for a lab scenario | 11 |
| L26 | 13 | Detection, Triage & Containment | Alert triage, scoping an intrusion, containment strategy trade-offs | Triage a staged multi-source incident | 11, 12 |
| L27 | 14 | Eradication, Recovery & Lessons Learned | Eradication/recovery playbooks, metrics, post-incident review discipline | Run a tabletop exercise (Assignment 6) | 11 |
| L28 | 14 | SOC Operations & Threat Hunting | Hunt hypotheses, intel-driven hunting, SOC metrics & maturity | Execute a guided hunt in lab telemetry (Quiz 5) | 12 |

### Module 8 — Network Forensics & Capstone (Expert)

| Lec | Week | Title (2 h) | Core topics | Practice in session | CLO |
|---|---|---|---|---|---|
| L29 | 15 | Forensic Fundamentals | Evidence types, chain of custody, pcap & netflow analysis workflow | Reconstruct a session timeline from a pcap | 14 |
| L30 | 15 | Advanced Forensics & Reporting | Timeline correlation across logs/flows, IOC extraction, defensible reporting | Produce a findings report from a staged incident | 14, 15 |
| L31 | 16 | Capstone Workshop & IR Simulation | Capstone design reviews, live IR simulation in the capstone range | Team design reviews + IR simulation run | 11, 15 |
| L32 | 16 | Capstone Defense & Course Synthesis | Team defenses, course retrospective, career/certification pathways | Capstone defense sessions (Final exam window) | 14, 15 |

**Case-study infusion:** the four graded case-study sets (A: L05–L08, B: L09–L12,
C: L21–L24, D: L25–L30) plus module-specific cases in every week deliver the ≥100
case-study requirement; the authoritative count and tracker live in
`docs-meta/case-study-tracker.md` (Phase 2 deliverable — not yet created).

## 4. CLO → Module → Lecture Coverage Matrix

| CLO | Taught in lectures | Assessed by | Covered? |
|---|---|---|---|
| CLO-1 | L01–L04 | Quiz 1, Midterm | ✅ |
| CLO-2 | L05–L08 | Quiz 2, Case sets A | ✅ |
| CLO-3 | L09, L10, L12 | Assignment 1, Capstone design | ✅ |
| CLO-4 | L10, L11 | Lab practical, Assignment 2 | ✅ |
| CLO-5 | L13, L16 | Quiz 3, Assignment 3 | ✅ |
| CLO-6 | L14 | Lab practical, Case sets | ✅ |
| CLO-7 | L15, L16 | Midterm, Capstone | ✅ |
| CLO-8 | L17, L18 | Lab practical, Quiz 4 | ✅ |
| CLO-9 | L22, L23 | Assignment 4, Lab practical | ✅ |
| CLO-10 | L24 | Assignment 5, Case sets | ✅ |
| CLO-11 | L25, L26, L27, L31 | Capstone IR exercise, Final | ✅ |
| CLO-12 | L21, L23, L26, L28 | Assignment 6, Capstone | ✅ |
| CLO-13 | L19, L20 | Quiz 5, Assignment 7 | ✅ |
| CLO-14 | L29, L30, L32 | Final exam practical, Capstone | ✅ |
| CLO-15 | L30, L31, L32 | Capstone report, IR briefing | ✅ |

## 5. Weekly Schedule & Assessment Calendar

| Week | Lectures | Lab (graded, 1 per week) | Assessment due |
|---|---|---|---|
| 1 | L01, L02 | Lab-01: Lab range orientation & first capture | — |
| 2 | L03, L04 | Lab-02: TCP/DNS/DHCP trace analysis | Quiz 1 |
| 3 | L05, L06 | Lab-03: L2 attack observation & detection | — |
| 4 | L07, L08 | Lab-04: MITM & flood telemetry analysis | Quiz 2 |
| 5 | L09, L12 | Lab-05: Segmentation & proxy egress design | Quiz 3, Assignment 1 |
| 6 | L10, L11 | Lab-06: pfSense rulebase build & ACL audit | Assignment 2 |
| 7 | L13, L14 | Lab-07: Lab PKI + TLS configuration audit | — |
| 8 | L15, L16 | Lab-08: Site-to-site VPN build & evaluate | **Midterm** |
| 9 | L17, L19 | Lab-09: Wireless characterization + VPC segmentation | — |
| 10 | L18, L20 | Lab-10: WPA-Enterprise build + cloud flow logs | Quiz 4 |
| 11 | L21, L22 | Lab-11: Flow collector + Suricata ruleset | Assignment 4 |
| 12 | L23, L24 | Lab-12: Zeek analysis + vulnerability scan cycle | Assignment 5 |
| 13 | L25, L26 | Lab-13: Incident triage on staged intrusion | Assignment 6 |
| 14 | L27, L28 | Lab-14: Tabletop + guided threat hunt | Quiz 5, Assignment 7 |
| 15 | L29, L30 | Lab-15: Forensic timeline & findings report | Capstone draft |
| 16 | L31, L32 | Lab-16: Capstone IR simulation | **Capstone defense + Final** |

*(Lecture sequence within weeks follows §3; the L09/L12 and L17/L19 orderings pair
concept-first lectures with their lab counterpart in the same week.)*

## 6. Instructor/Student Material Separation (verification design)

- **Student tree (public):** all content outside `instructor/`.
- **Instructor-only:** `instructor/answer-keys/`, `instructor/speaker-notes/`,
  `instructor/lab-verification/`, `instructor/instructor-manual.md`, exam keys.
- Every lecture `lecture-NN-<slug>.md` pairs with
  `instructor/speaker-notes/lecture-NN-<slug>.md` (Gate V8).
- Every case study / assignment / quiz / lab with a graded artifact pairs with an
  answer key of the same basename under `instructor/answer-keys/<category>/` (Gate V5).
- Pages workflow excludes `instructor/` and CI fails on any leak (Gate V5).

## 7. Decision Records

**ADR-001 — 8 modules × 4 lectures.** Two-week module blocks give each topic area a
complete theory→practice→assessment arc while keeping 32 lectures divisible for
validation (Gate V1/V2). Rejected: 16 single-week modules (too fragmented for
case-study sets) and 4 mega-modules (assessment cadence too slow).

**ADR-002 — Labs embedded in lecture hours.** 64 contact hours include in-session
practice; 16 weekly graded labs are the formal practical vehicle. Rejected: a separate
3-hour lab session (would exceed the 64-hour envelope and 3+1 credit structure).

**ADR-003 — Wireshark-first protocol teaching.** Packet evidence is the course's
through-line (foundations → attacks → detection → forensics all read from the same
capture format). Rejected: tool-first curricula that teach products before protocols.

**ADR-004 — Case studies as first-class graded artifacts.** 100+ case studies are
tracked individually (`docs-meta/case-study-tracker.md`) with per-module minimums, so
the Mission's "at least 100" is auditable rather than rhetorical.

**ADR-005 — Separation by directory, enforced by CI.** All instructor material lives
under one tree and is excluded at build time; automated leak detection (Gate V5) is
preferred over policy-only separation.

**ADR-006 — Single global lecture numbering (L01–L32).** Enables flat validation of
counts/hours and stable cross-references from CLOs, labs, and assessments, at the cost
of renumbering if lectures are reordered (accepted; reorder is rare and gated by review).

**ADR-007 — Markdown + front matter as the authoring format.** Files are
human-readable, diff-able, lintable, and publishable to GitHub Pages without a CMS;
YAML front matter (`clos`, `hours`, `status`) powers automated Gates V1–V8.

## 8. Compliance Check against Mission Scope

| Required scope topic | Where covered |
|---|---|
| Network protocols | M1 (L01–L04) |
| Network threats | M2 (L05–L08) |
| Secure architectures | M3 (L09), M4, M5 (L19–L20) |
| Firewalls | M3 (L10) |
| ACLs | M3 (L11) |
| Segmentation | M3 (L09), M5 (L19) |
| Cryptography | M4 (L13) |
| TLS | M4 (L14) |
| VPNs | M4 (L15–L16) |
| Wireless security | M5 (L17–L18) |
| IDS/IPS | M6 (L22–L23) |
| Monitoring | M6 (L21), M7 (L28) |
| Vulnerability management | M6 (L24) |
| Incident response | M7 (L25–L27) |
| Cloud networking | M5 (L19–L20) |
| Network forensics | M8 (L29–L30) |

All 16 mandated scope areas are mapped to specific lectures — no gaps.
