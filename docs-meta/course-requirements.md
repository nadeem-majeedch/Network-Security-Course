# Course Requirements — Network Security

**Document ID:** NSC-REQ-001 · **Status:** Approved baseline · **Version:** 1.0
**Program:** BS Computer Science / BS Data Science · **Semester:** 7th (Senior)
**Source of truth for all course design, content, and validation decisions.**
**Related documents:** `content-inventory.md`, `course-architecture.md`, `implementation-roadmap.md`

---

## 1. Course Identity

| Attribute | Value |
|---|---|
| Course title | Network Security |
| Course code | NS-401 |
| Credit structure | 3 + 1 (3 theory hours + 1 lab hour per week × 16 weeks) |
| Contact hours | 64 total (32 lectures × 2 hours; labs are integrated into lecture blocks and case-study sessions) |
| Duration | 16 weeks · 2 lectures per week |
| Lecture length | 2 hours each |
| Total lectures | **32** (exactly — see §9 Validation Gate V1) |
| Total modules | **8** (exactly — see §9 Validation Gate V2) |
| Case studies | **≥ 100** problem-solving case studies, progressively difficult |
| Prerequisites | Computer Networks (routing, TCP/IP, subnetting), Operating Systems (processes, permissions), Programming (Python or equivalent), Discrete Mathematics |
| Target audience | BS Computer Science and BS Data Science, 7th semester (senior undergraduates) |
| Delivery mode | In-person lecture + hands-on lab + case-study discussion + capstone project |

## 2. Course Description

A senior-level, practice-intensive course covering the security of networked systems
end to end: how network protocols work and fail, how real attacks against them are
structured, and how defenders design, deploy, monitor, and forensically analyze secure
network architectures. Students progress from packet-level fundamentals to enterprise
secure design, cryptographic protocols, wireless and cloud networking, intrusion
detection, vulnerability management, incident response, and network forensics. Every
module pairs theory with a hands-on lab and graded case studies; the course culminates
in a team capstone: a full defensive design, hardening, detection engineering, and
incident-response exercise over a simulated enterprise network.

All lab work is conducted in isolated, authorized lab environments (local VMs,
containerized ranges, or instructor-provided sandbox infrastructure). No activity is
ever directed at systems the students do not own or are not explicitly authorized to
test. See §8 Ethics and Legal Boundaries.

## 3. Program Learning Outcome Alignment

| PLO | Statement | Primary coverage |
|---|---|---|
| PLO-1 | Engineering Knowledge | Modules 1–3 (protocol and threat fundamentals) |
| PLO-2 | Problem Analysis | Modules 2, 4, 6 (threat modeling, traffic analysis, vuln assessment) |
| PLO-3 | Design/Development of Solutions | Modules 3, 4, 7 (secure architecture, segmentation, IR design) |
| PLO-4 | Investigation | Module 8 (network forensics) |
| PLO-5 | Modern Tool Usage | All lab components (Wireshark, Suricata, Zeek, nmap, OpenSSL, cloud CLIs) |
| PLO-8 | Ethics | Module 1 + standing lab rules (§8) |
| PLO-9 | Individual and Team Work | Capstone teams of 3–4 |
| PLO-10 | Communication | Capstone report + IR tabletop briefing deliverables |

*(PLO numbering follows the standard Washington-Accord-style graduate attribute set used
by the affiliated program; institutions with different numbering should remap — the
CLO→PLO matrix in `course-architecture.md` §6 is the binding mapping.)*

## 4. Course Learning Outcomes (CLOs)

On successful completion, the student will be able to:

| CLO | Statement | Bloom level | Assessment | Module |
|---|---|---|---|---|
| **CLO-1** | Explain the operation of core network protocols (Ethernet, ARP, IP, ICMP, TCP, UDP, DNS, HTTP/HTTPS, DHCP) and identify their security-relevant properties and weaknesses. | C2 – Understand | Quiz 1, Midterm | 1 |
| **CLO-2** | Classify network threats and attack techniques (spoofing, sniffing, MITM, DoS/DDoS, lateral movement, C2 exfiltration) and map each to the protocol layer and network position it exploits. | C4 – Analyze | Quiz 2, Case studies | 2 |
| **CLO-3** | Design segmented, defense-in-depth network architectures (zones, VLANs, firewalls, ACLs, NAT, proxy egress) that satisfy stated security requirements and trade-offs. | C5 – Evaluate→Create | Assignment 1, Capstone design | 3 |
| **CLO-4** | Configure and verify host- and network-based firewall and ACL policy sets, and audit an existing rule base for correctness, shadowing, and least privilege. | C3 – Apply | Lab practical, Assignment 2 | 3 |
| **CLO-5** | Apply symmetric, asymmetric, and hash cryptographic primitives correctly and select appropriate algorithms, key sizes, and modes for a given confidentiality/integrity requirement. | C3 – Apply | Quiz 3, Assignment 3 | 4 |
| **CLO-6** | Analyze TLS protocol behavior (handshake, certificate validation, versions, cipher suites) and detect and remediate common TLS misconfigurations. | C4 – Analyze | Lab practical, Case studies | 4 |
| **CLO-7** | Design and evaluate site-to-site and remote-access VPN solutions (IPsec, WireGuard, TLS-VPN) including trust model, key management, and failure modes. | C5 – Evaluate | Midterm, Capstone | 4 |
| **CLO-8** | Secure wireless networks (WPA2/WPA3 enterprise, rogue AP defense, RF-survey basics) and evaluate a wireless deployment against known attack classes. | C4 – Analyze | Lab practical, Quiz 4 | 5 |
| **CLO-9** | Deploy and tune network intrusion detection (signature and anomaly based: Snort/Suricata, Zeek) and write custom detection rules for given threat scenarios. | C5 – Evaluate→Create | Assignment 4, Lab practical | 6 |
| **CLO-10** | Operate a vulnerability management cycle: asset discovery, authenticated/unauthenticated scanning, risk-based prioritization (CVSS + context), and remediation tracking. | C3 – Apply | Assignment 5, Case studies | 6 |
| **CLO-11** | Execute the incident response lifecycle (prepare, detect, analyze, contain, eradicate, recover, lessons learned) on a simulated network intrusion, producing defensible artifacts. | C5 – Evaluate→Create | Capstone IR exercise, Final exam | 7 |
| **CLO-12** | Design monitoring and logging pipelines (flow data, SIEM ingestion, detection engineering, alert triage) and justify sensor placement and coverage decisions. | C5 – Evaluate | Assignment 6, Capstone | 6, 7 |
| **CLO-13** | Apply network security controls in cloud environments (VPC design, security groups, NACLs, private endpoints, flow logs) and compare shared-responsibility implications to on-prem. | C4 – Analyze | Quiz 5, Assignment 7 | 5 |
| **CLO-14** | Conduct network forensics: reconstruct session timelines from pcaps and flow/netflow records, extract IOCs, and write a factual findings report with chain-of-custody discipline. | C5 – Evaluate→Create | Final exam practical, Capstone | 8 |
| **CLO-15** | Communicate security findings and designs effectively to technical and executive audiences in written reports and briefings. | A2/A3 – Communication | Capstone report, IR briefing | 3, 7, 8 (cross-cutting) |

**CLO→assessment mapping is normative**; every graded artifact must cite the CLOs it
assesses. Coverage verification is Validation Gate V4 (§9).

## 5. Grading and Assessment Plan

| Component | Weight | CLO coverage | Notes |
|---|---|---|---|
| Quizzes (5 × 3%) | 15% | CLO-1, 2, 5, 8, 13 | In-lecture, 20 min, closed book |
| Lab practicals (4 × 5%) | 20% | CLO-4, 6, 8, 9 | Graded hands-on tasks in lab env |
| Assignments (7 × 5%) | 35% | CLO-3, 4, 5, 9, 10, 12, 13 | Mix of design docs and configs |
| Midterm examination | 10% | CLO-1, 2, 3, 5, 7 | Weeks 1–8 material |
| Capstone project | 15% | CLO-3, 7, 11, 12, 14, 15 | Team of 3–4, weeks 9–16 |
| Final examination | 5% written + practical embedded | CLO-11, 14 | Includes forensic practical |

Instructor-only answer keys, rubrics, and exam solutions live **only** under
`instructor/` and are excluded from the GitHub Pages publication pipeline (§7, §9-V5).

## 6. Case Study Requirement

- **Minimum 100** problem-solving case studies distributed across all eight modules,
  increasing in difficulty within and across modules (beginner → expert).
- Each case study is a scenario + artifacts (logs, pcaps, configs, topology) + a
  question set + (instructor copy) a model solution and grading rubric.
- Distribution floor per module: 10 cases minimum; capstone-adjacent integrative cases
  in Modules 7–8.
- Authoritative tracker: `docs-meta/case-study-tracker.md` (created in Phase 2).

## 7. Repository Conventions (Normative)

### 7.1 Directory layout

```
/
├── docs-meta/                  # Course governance docs (this set)
├── syllabus/                   # Student-facing syllabus
├── modules/
│   ├── module-01-<slug>/       # One directory per module (see 7.2 slugs)
│   │   ├── module-overview.md
│   │   ├── lectures/
│   │   │   ├── lecture-01-<slug>.md
│   │   │   └── ...
│   │   ├── labs/
│   │   │   ├── lab-01-<slug>.md
│   │   │   └── ...
│   │   ├── case-studies/
│   │   │   ├── cs-001-<slug>.md
│   │   │   └── ...
│   │   ├── quizzes/
│   │   └── assignments/
│   └── ...
├── assessments/
│   ├── midterm/
│   └── final/
├── capstone/
├── instructor/                 # INSTRUCTOR-ONLY (answer keys, solutions, rubrics,
│   │                           #   speaker notes, exam keys) — never published
│   ├── answer-keys/
│   ├── speaker-notes/
│   └── instructor-manual.md
├── site/                       # GitHub Pages publication source
└── .github/workflows/          # CI: link check, build, publish
```

### 7.2 Naming rules

- Modules: `module-NN-<kebab-slug>` (e.g., `module-01-network-fundamentals`).
- Lectures: `lecture-NN-<kebab-slug>.md`, NN = 01–32 global lecture number.
- Labs: `lab-NN-<kebab-slug>.md`, NN = 01–16 (one lab per week).
- Case studies: `cs-NNN-<kebab-slug>.md`, NNN = 001–100+ global.
- Assignments: `assignment-NN-<kebab-slug>.md`, NN = 01–07.
- Quizzes: `quiz-NN-<slug>.md`, NN = 01–05.
- No spaces in file or directory names. Lowercase kebab-case everywhere.
- Every content file starts with the standard YAML front-matter block (module,
  lecture number, CLOs covered, difficulty, estimated minutes).

### 7.3 Student/instructor separation (normative)

- Public student tree: everything **except** `instructor/`.
- `instructor/` contains: answer keys, model solutions, grading rubrics, exam keys,
  full speaker notes, and the instructor manual.
- The Pages build (§7.4) must exclude `instructor/` and CI must fail if any
  `instructor/` path appears in the published output (Validation Gate V5).
- Student-facing files may include *questions* but never *answers*; answers live in
  the mirrored path under `instructor/answer-keys/` with identical basenames.

### 7.4 Publication

- GitHub Pages serves from `site/` (built from the public tree).
- `.github/workflows/pages.yml` builds and deploys; `.github/workflows/ci.yml` runs
  validation gates on every push and PR.

## 8. Ethics and Legal Boundaries (Normative, course-wide)

1. All hands-on work occurs only in instructor-authorized lab environments.
2. No scanning, probing, or exploitation of systems without explicit written
   authorization. Course examples use lab ranges, deliberately vulnerable VMs, and
   public capture repositories only.
3. Every lab front page carries the authorization statement; instructors must not
   distribute tooling recipes whose only use is unauthorized access.
4. Responsible-disclosure framing is taught in Module 7 and required in the capstone.
5. Student work must be their own; AI assistance policy is set by the institution and
   stated in the syllabus.

## 9. Validation Gates (Normative)

Every gate is checked by CI where automatable and recorded with **actual observed
results** (never asserted) in `docs-meta/content-inventory.md`.

| Gate | Requirement | Method |
|---|---|---|
| **V1** | Exactly 32 lectures planned, numbered 01–32, no gaps or duplicates | Script/CI count of `lecture-NN` slugs across modules |
| **V2** | Exactly 8 modules, `module-01` … `module-08` | Directory count + name check |
| **V3** | Total contact hours = 64 (32 × 2) | Sum of lecture hour fields in front matter |
| **V4** | Every CLO (1–15) is assessed by ≥ 1 graded artifact and taught by ≥ 1 lecture | Front-matter CLO aggregation script |
| **V5** | No `instructor/` content in Pages build output | CI artifact scan of published tree |
| **V6** | ≥ 100 case studies, globally unique `cs-NNN` ids | Count + id uniqueness check |
| **V7** | All internal links resolve; all labs list required tooling | Link checker + lab front-matter check |
| **V8** | Each lecture has speaker notes in `instructor/speaker-notes/` | Path pairing check |

**Current status: all gates are UNTESTED (planning-stage documents only).** Baseline
results will be recorded in `content-inventory.md` as content lands, phase by phase.

## 10. Content Quality Standard

A lecture file is *complete* when it contains: learning objectives (CLO-linked),
prerequisites, a timed section plan for 120 minutes, core content with diagrams
(described or ASCII/mermaid), at least one worked example, a lab or case-study
hook, a summary, and 5+ self-check questions. A file that lacks any of these must
carry `status: draft` in front matter and must not be counted as complete in any
inventory or report. **No draft content may be presented as complete** (Mission rule 9).

## 11. Technical Validation Standard

- All lab commands must be tested in the reference lab environment before a lab is
  marked `status: complete`; the tested command transcript is stored under
  `instructor/lab-verification/`.
- All configurations (firewall rules, TLS configs, Suricata rules, cloud policies)
  must be validated against the stated tool versions pinned in the lab front matter.
- External references must resolve (CI link check) and be authoritative primary
  sources (RFCs, vendor docs, standards bodies) where possible.
- Packet captures used in labs must come from lab-generated traffic or public
  repositories with stated licenses (e.g., Malware-Traffic-Analysis.net usage policy).

## 12. Out of Scope

- Offensive red-team tradecraft beyond what is needed to understand defenses.
- Any activity against non-lab infrastructure.
- Institution-specific LMS integration (repository remains LMS-neutral).

---

*End of NSC-REQ-001 v1.0. Changes to any normative section require updating
`course-architecture.md` and `implementation-roadmap.md` in the same change set.*
