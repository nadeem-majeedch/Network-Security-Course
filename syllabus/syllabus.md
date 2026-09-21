# NS-401 Network Security — Course Syllabus

**Version:** 1.0 · **Effective:** Fall semester (16 weeks) · **Governance:** aligned to `docs-meta/course-requirements.md` (NSC-REQ-001) and `docs-meta/course-architecture.md` (NSC-ARCH-001)

---

## 1. Course Information

| Field | Value |
|---|---|
| Course code & title | NS-401 — Network Security |
| Program | BS Computer Science / BS Data Science, 7th semester |
| Credit structure | 3 + 1 (theory + integrated lab/case practice) |
| Contact hours | 64 (32 lectures × 2 hours; labs and case work are embedded in lecture blocks) |
| Lectures per week | 2 |
| Assessment components | 5 quizzes · 4 lab practicals · 7 assignments · midterm · final · capstone |
| Instructor / office hours | *(institution to complete)* |
| Lab environment | Isolated, instructor-authorized virtual lab range only (see §9) |

## 2. Course Description

Network Security is a senior-level, practice-intensive course that teaches how
networked systems are attacked and, more importantly, how they are defended. The
course grounds every security control in the protocols it protects: students first
master the behavior of Ethernet, ARP, IP, ICMP, TCP, UDP, DNS, DHCP, and HTTP —
including IPv4/IPv6 addressing and routing — and then study how reconnaissance,
spoofing, sniffing, denial-of-service, and man-in-the-middle techniques exploit those
exact mechanics. With that foundation, the course turns to the defender's craft:
designing segmented, zero-trust architectures with firewalls, ACLs, NAT, and proxies;
protecting communications with symmetric and asymmetric cryptography, TLS, IPsec, and
VPNs; securing wireless and enterprise networks; extending controls into cloud and
container environments; operating IDS/IPS and monitoring pipelines; running the
vulnerability-management cycle; and leading incident response and network forensics.

Every week pairs theory with hands-on work: guided packet analysis, firewall and ACL
construction, IDS rule authoring, cloud lab exercises, and staged incident triage.
A sequence of more than 100 problem-solving case studies — escalating from
beginner scenarios to expert-level investigations — develops the judgment that
separates a tool operator from a security engineer. The course culminates in a team
capstone: students design, harden, monitor, and defend a simulated enterprise network,
then lead an incident-response exercise and defend their architecture and forensic
findings before a panel.

Graduates leave able to read a network the way an attacker does and to build one the
way a defender must — with defensible designs, tuned detections, disciplined evidence
handling, and clear communication to both technical and executive audiences.

## 3. Prerequisites

**Formal (course credit required):**

1. **Computer Networks** — OSI/TCP-IP layers, IP addressing and subnetting, basic routing and switching, client/server model.
2. **Operating Systems** — processes and permissions, filesystem concepts, virtualization basics.
3. **Programming (Python preferred)** — scripting, file I/O, basic data structures.
4. **Discrete Mathematics** — logic and modular arithmetic (supports the cryptography module).

**Recommended (not required):** Linux command-line fluency; exposure to Wireshark or any packet analyzer; an introductory information-security or IT-security course.

**Readiness self-check — you should already be able to:**

- Explain what happens, protocol by protocol, between entering a URL and seeing a page.
- Subnet an IPv4 range and explain NAT vs routing.
- Use a terminal to navigate files, install packages, and run a script.
- Read a simple Python program and modify it.

Students needing a refresher should complete the Week-0 bridge readings posted by the instructor before Lecture 1.

## 4. Course Learning Outcomes (CLOs) — Measurable

On successful completion, the student will be able to (Bloom level in parentheses;
"given X, do Y" criteria are the measurable bar used in grading):

| CLO | Outcome statement | Measurable performance criterion |
|---|---|---|
| **CLO-1** | Explain the operation of core network protocols (Ethernet, ARP, IP/IPv6, ICMP, TCP, UDP, DNS, DHCP, HTTP/HTTPS) and identify their security-relevant properties and weaknesses. (Understand) | Given a packet capture, correctly annotate the protocol exchanges and identify ≥ 3 security-relevant behaviors. |
| **CLO-2** | Classify network threats and attack techniques (reconnaissance, spoofing, sniffing, MITM, session hijacking, DoS/DDoS, botnets) and map each to the protocol layer and network position it exploits. (Analyze) | Given an attack description or capture, correctly classify technique, layer, and vantage point, and produce an attack tree or ATT&CK mapping. |
| **CLO-3** | Design segmented, defense-in-depth network architectures (zones, VLANs, DMZ, zero-trust direction) that satisfy stated security requirements. (Evaluate→Create) | Produce a design document and topology that meets ≥ 90% of stated requirements and defends its trust-zone decisions. |
| **CLO-4** | Configure and verify host- and network-based firewall and ACL policy sets, and audit a rulebase for correctness, shadowing, and least privilege. (Apply) | Implement a policy spec as working rules with ≤ 1 critical error, and find ≥ 3 planted faults in a supplied rulebase. |
| **CLO-5** | Apply symmetric, asymmetric, and hash cryptographic primitives correctly and select appropriate algorithms, key sizes, and modes for a stated requirement. (Apply) | Given three data-protection scenarios, select and justify algorithm/mode/key-size choices and reject insecure options. |
| **CLO-6** | Analyze TLS protocol behavior (handshake, certificate validation, versions, cipher suites) and detect and remediate common TLS misconfigurations. (Analyze) | Given a TLS endpoint report, identify ≥ 3 weaknesses and produce a corrected configuration. |
| **CLO-7** | Design and evaluate site-to-site and remote-access VPN solutions (IPsec, WireGuard, TLS-VPN), including trust model, key management, and failure modes. (Evaluate) | Produce a VPN design with documented trade-offs and correctly predict behavior in 3 given failure scenarios. |
| **CLO-8** | Secure wireless networks (WPA2/WPA3 enterprise, rogue-AP defense, 802.1X/EAP) and evaluate a wireless deployment against known attack classes. (Analyze) | Given a wireless survey/capture, identify exposure classes and specify enterprise-auth controls that mitigate them. |
| **CLO-9** | Deploy and tune network intrusion detection (Snort/Suricata signatures, Zeek) and write custom detection rules for given threat scenarios. (Evaluate→Create) | Author ≥ 2 syntactically correct, targeted rules that fire on provided malicious traffic with ≤ 2 false positives. |
| **CLO-10** | Operate a vulnerability-management cycle: asset discovery, scanning, CVSS-based prioritization with context, and remediation tracking. (Apply) | Complete a full scan→prioritize→remediate→verify cycle on lab hosts with a defensible prioritization rationale. |
| **CLO-11** | Execute the incident-response lifecycle (prepare, detect, analyze, contain, eradicate, recover, lessons learned) on a simulated intrusion, producing defensible artifacts. (Evaluate→Create) | Produce a timeline, containment plan, and post-incident report that the instructor can follow without oral explanation. |
| **CLO-12** | Design monitoring and logging pipelines (flow data, SIEM ingestion, sensor placement, detection engineering, alert triage). (Evaluate) | Justify sensor placement and log-source choices against ≥ 3 given threat scenarios with coverage-gap analysis. |
| **CLO-13** | Apply network security controls in cloud environments (VPC design, security groups vs NACLs, private endpoints, flow logs) and compare shared-responsibility implications to on-premises. (Analyze) | Build a segmented cloud network meeting a control spec and explain shared-responsibility boundaries for 3 given services. |
| **CLO-14** | Conduct network forensics: reconstruct session timelines from pcaps and flow records, extract IOCs, and write a factual findings report with chain-of-custody discipline. (Evaluate→Create) | Produce a timeline corroborated by ≥ 2 evidence sources and a report with reproducible queries and IOCs. |
| **CLO-15** | Communicate security findings and designs effectively to technical and executive audiences in written reports and briefings. (Create) | Deliver a capstone defense and an executive briefing that a non-specialist panel rates ≥ satisfactory on clarity and accuracy. |

## 5. CLO → Lectures, Labs, and Assessments (Coverage Matrix)

| CLO | Lectures | Labs (weekly) | Lab practicals | Quizzes | Assignments | Exams / Capstone |
|---|---|---|---|---|---|---|
| CLO-1 | L01–L04 | Lab-01, Lab-02 | — | Quiz 1 | — | Midterm |
| CLO-2 | L05–L08 | Lab-03, Lab-04 | — | Quiz 2 | Case set A | Midterm |
| CLO-3 | L09, L10, L12 | Lab-05 | — | Quiz 3 (partial) | Assignment 1 | Capstone design |
| CLO-4 | L10, L11 | Lab-06 | Pract-1 (W6) | — | Assignment 2 | — |
| CLO-5 | L13, L16 | Lab-07, Lab-08 | — | Quiz 3 | Assignment 3 | Midterm |
| CLO-6 | L14 | Lab-07 | Pract-2 (W7) | — | Case sets B–C | — |
| CLO-7 | L15, L16 | Lab-08 | — | — | — | Midterm, Capstone |
| CLO-8 | L17, L18 | Lab-09, Lab-10 | Pract-3 (W10) | Quiz 4 | — | — |
| CLO-9 | L22, L23 | Lab-11, Lab-12 | Pract-4 (W11) | — | Assignment 4 | — |
| CLO-10 | L24 | Lab-12 | — | — | Assignment 5 | — |
| CLO-11 | L25, L26, L27, L31 | Lab-13, Lab-14, Lab-16 | — | — | Assignment 6 (partial) | Final, Capstone IR |
| CLO-12 | L21, L23, L26, L28 | Lab-11, Lab-14 | — | — | Assignment 6 | Capstone |
| CLO-13 | L19, L20 | Lab-09, Lab-10 | — | Quiz 4/5 | Assignment 7 | — |
| CLO-14 | L29, L30, L32 | Lab-15, Lab-16 | — | — | — | Final practical, Capstone |
| CLO-15 | L30, L31, L32 | Lab-15, Lab-16 | — | — | — | Capstone report + defense |

## 6. Assessment and Grading

| Component | Weight | Notes |
|---|---|---|
| Quizzes (5 × 3%) | 15% | In-lecture, ~20 min, weeks 2/4/5/10/14 (see calendar) |
| Lab practicals (4 × 5%) | 20% | Hands-on graded tasks: W6, W7, W10, W11 |
| Assignments (7 × 5%) | 35% | Mix of design documents, configurations, and analyses |
| Midterm examination | 10% | Week 8, covers Weeks 1–8 |
| Capstone project | 15% | Team of 3–4; design + build + IR exercise + defense (W9–W16) |
| Final examination | 5% | Week 16; written + embedded forensic practical |

Grading scale, resit rules, and attendance thresholds follow institutional policy *(institution to complete)*. All graded artifacts publish CLOs assessed; answer keys and rubrics live in the instructor materials and are not distributed.

## 7. Sixteen-Week Teaching Calendar

| Week | Lectures (2 h each) | Graded lab | Due |
|---|---|---|---|
| 1 | L01 Security Mindset & the Network Threat Landscape · L02 Protocol Deep Dive I — Ethernet, ARP, IP, ICMP | Lab-01: lab-range orientation & first capture | — |
| 2 | L03 Protocol Deep Dive II — TCP, UDP, DNS, DHCP · L04 Applied Packet Analysis & Web Protocols | Lab-02: TCP/DNS/DHCP trace analysis | Quiz 1 |
| 3 | L05 Threat Modeling & Attacker Anatomy · L06 Layer-2 & LAN Attacks | Lab-03: L2 attack observation & detection | — |
| 4 | L07 Sniffing, MITM & Session Attacks · L08 DoS/DDoS & Infrastructure Abuse | Lab-04: MITM & flood telemetry analysis | Quiz 2 |
| 5 | L09 Defense in Depth & Network Segmentation · L12 NAT, Proxies, Egress & NAC | Lab-05: segmentation & proxy egress design | Quiz 3, Assignment 1 |
| 6 | L10 Firewalls: Concepts & Placement · L11 ACLs & Rulebase Engineering | Lab-06: pfSense rulebase build & ACL audit | Assignment 2 |
| 7 | L13 Cryptographic Foundations · L14 TLS Deep Dive | Lab-07: lab PKI + TLS configuration audit | — |
| 8 | L15 IPsec & Legacy VPN Architecture · L16 Modern VPNs & Crypto Agility | Lab-08: site-to-site VPN build & evaluate | **Midterm** |
| 9 | L17 Wireless Fundamentals & Threats · L19 Cloud Networking I — VPC Design & Controls | Lab-09: wireless characterization + VPC segmentation | Capstone brief |
| 10 | L18 Enterprise Wireless & Rogue Defense · L20 Cloud Networking II — Hybrid & Assurance | Lab-10: WPA-Enterprise build + cloud flow logs | Quiz 4 |
| 11 | L21 Monitoring Foundations · L22 IDS/IPS — Signatures & Tuning | Lab-11: flow collector + Suricata ruleset | Assignment 4 |
| 12 | L23 Zeek & Anomaly Detection · L24 Vulnerability Management Cycle | Lab-12: Zeek analysis + vulnerability scan cycle | Assignment 5 |
| 13 | L25 IR Lifecycle & Preparation · L26 Detection, Triage & Containment | Lab-13: incident triage on staged intrusion | Assignment 6 |
| 14 | L27 Eradication, Recovery & Lessons Learned · L28 SOC Operations & Threat Hunting | Lab-14: tabletop + guided threat hunt | Quiz 5, Assignment 7 |
| 15 | L29 Forensic Fundamentals · L30 Advanced Forensics & Reporting | Lab-15: forensic timeline & findings report | Capstone draft |
| 16 | L31 Capstone Workshop & IR Simulation · L32 Capstone Defense & Course Synthesis | Lab-16: capstone IR simulation | **Capstone defense + Final** |

## 8. Materials and Tooling

- **Primary references:** RFCs cited per lecture; NIST SP 800-series; MITRE ATT&CK; official tool documentation. Recommended texts (any recent edition): Stallings, *Cryptography and Network Security*; Kurose & Ross, *Computer Networking: A Top-Down Approach*; Sanders, *Practical Packet Analysis*; Bejtlich, *The Practice of Network Security Monitoring*.
- **Lab tooling (pinned per lab):** Wireshark, tcpdump, nmap, hping3, OpenSSL, pfSense, Suricata, Zeek, OpenVAS/Nessus Essentials equivalents, cloud free-tier CLIs, Docker.
- All tools are open-source or free-tier; the lab range is provisioned from local VMs/containers.

## 9. Ethics and Authorization Policy (binding)

1. All hands-on work occurs **only** in instructor-authorized lab environments.
2. Scanning, probing, or exploitation of any system without explicit written authorization is prohibited — inside and outside the course.
3. Case studies use lab ranges, deliberately vulnerable lab VMs, or public capture repositories used under their stated licenses.
4. The course teaches defense; techniques are covered to the depth needed to design, detect, and verify controls. Responsible disclosure is taught in Module 7.
5. Violations are handled under the institutional academic-integrity and computer-use policies.

## 10. Course Policies

- **Attendance:** expected; in-session labs and case work cannot be replicated individually.
- **Late work:** 10%/day to a maximum of 5 days unless arranged in advance *(institution to adjust)*.
- **Academic integrity & AI assistance:** follow institutional policy as stated by the instructor; all submitted analysis must be your own and must cite tool usage and data sources.
- **Accessibility:** students requiring accommodations should contact the institution's accessibility office; all lab exercises can be adapted.
- **Communication:** course announcements and grading go through the institutional LMS; this repository is the canonical content source.

---

*Changes to CLOs, weights, or calendar require updating the governance documents (NSC-REQ-001, NSC-ARCH-001) in the same change set. This syllabus version: 1.0.*
