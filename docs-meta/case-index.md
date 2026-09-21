---
artifact-type: case-index
status: complete
cases: 100
student-cases: 100
instructor-solutions: 100
last-updated: case-collection session
---

# Case Study Index — 100 Progressive Network Security Cases

> **Pedagogy (per mission):** the case goes on the projector first;
> ~5 minutes of individual/group reasoning; then approach
> discussion, model-solution reveal, and tradeoff analysis. Each
> case states its own time estimate (10–30 min; expert cases run
> longer by design).

## 1. Collection Overview

- **100 cases** (cs-001 … cs-100), each with a paired
  instructor-only solution under `teaching/case-solutions/`
  (19 mandated elements per case: ID, title, difficulty, domain,
  scenario, stakeholders, network context, available evidence,
  student task, expected reasoning, model solution, alternatives,
  tradeoffs, common mistakes, instructor prompts, CLO mapping,
  time estimate, rubric, safety notes).
- All scenarios are **clearly labeled simulated** fiction — no
  case presents a fictional incident as historical fact.
- Difficulty tiers follow the mission's 4-band split; the session-2
  tracker's 6 working bands were collapsed monotonically by case
  number (documented in the tracker change log).

## 2. Difficulty Mapping (mission tiers: 20/25/30/25)

| Tier | Band | Cases | Count |
|---|---|---|---|
| Beginner | beginner | cs-001–020 | **20** |
| Intermediate | intermediate | cs-021–045 | **25** |
| Advanced | advanced | cs-046–075 | **30** |
| Expert | expert | cs-076–100 | **25** |

Progressive logic: M1 cases build reading fluency (protocol
evidence), M2 attack mechanics, M3 design judgment, M4 crypto
operationalism, M5 wireless/cloud, M6 detection/vuln analytics,
M7 response judgment, M8 capstone integration. Each tier *uses*
the prior tier's vocabulary rather than repeating it.

## 3. Module Distribution

| Module | Directory | Cases | Lectures |
|---|---|---|---|
| M1 Network Foundations | `modules/module-01-network-foundations/case-studies/` | 10 (cs-001–010) | L01–L04 |
| M2 Network Threats | `modules/module-02-network-threats/case-studies/` | 15 (cs-011–025) | L05–L08 |
| M3 Secure Architecture | `modules/module-03-secure-architecture/case-studies/` | 14 (cs-026–039) | L09–L12 |
| M4 Crypto & Protocols | `modules/module-04-crypto-protocols/case-studies/` | 14 (cs-040–053) | L13–L16 |
| M5 Wireless & Cloud | `modules/module-05-wireless-cloud/case-studies/` | 12 (cs-054–065) | L17–L20 |
| M6 Detection & Vulnerability | `modules/module-06-detection-vulnerability/case-studies/` | 13 (cs-066–078) | L21–L24 |
| M7 Incident Response | `modules/module-07-incident-response/case-studies/` | 12 (cs-079–090) | L25–L28 |
| M8 Forensics & Capstone | `modules/module-08-forensics-capstone/case-studies/` | 10 (cs-091–100) | L29–L32 |

## 4. Domain Mapping (20 mission domains)

| Domain | Cases (representative) |
|---|---|
| Network security principles | cs-001, 002, 011 |
| TCP/IP protocol analysis | cs-003, 004, 005, 006, 010 |
| DNS and DHCP security | cs-007, 008, 020 |
| ARP and local network threats | cs-003, 013, 014 |
| Firewall and ACL design | cs-030, 031, 034, 035, 036 |
| Network segmentation | cs-026, 028, 029, 037 |
| VPN and secure remote access | cs-049, 050, 051, 052 |
| TLS and certificate problems | cs-044, 045, 046, 047, 048 |
| Wireless network security | cs-054, 055, 056, 057, 058, 059, 060 |
| IDS/IPS alerts | cs-069, 070, 071 |
| Network monitoring and log analysis | cs-066, 067, 068, 072 |
| Vulnerability prioritization | cs-074, 075, 076, 077, 078 |
| Enterprise architecture | cs-027, 039, 091, 092, 098 |
| Cloud network security | cs-061, 062, 063, 065 |
| Incident response | cs-079, 080, 081, 083, 086, 095, 099 |
| Network forensics | cs-087, 097 |
| Data Science infrastructure security | cs-088, 096 (cluster/pipeline cases throughout) |
| Zero trust | cs-093 |
| Risk management | cs-090, 094 |
| Multi-stage security incidents | cs-082, 084, 085, 089, 100 |

Every domain in the mission list is covered; several cases carry
secondary domains (the index lists the primary).

## 5. CLO Coverage Report

CLO mapping per case comes from the front-matter `clos:` field,
anchored to the teaching-plan CLO of the anchor lecture. Observed
counts across the collection (117 case→CLO mappings; every CLO
carried by ≥4 cases — computed from the files by
`validate_cases.py` and the index build):

| CLO | Cases carrying it | Status |
|---|---|---|
| CLO-1 | 10 (cs-001–010) | ✅ covered |
| CLO-2 | 15 (cs-011–025) | ✅ covered |
| CLO-3 | 7 | ✅ covered |
| CLO-4 | 8 | ✅ covered |
| CLO-5 | 6 | ✅ covered |
| CLO-6 | 5 | ✅ covered |
| CLO-7 | 4 | ✅ covered |
| CLO-8 | 7 | ✅ covered |
| CLO-9 | 5 | ✅ covered |
| CLO-10 | 5 | ✅ covered |
| CLO-11 | 11 | ✅ covered |
| CLO-12 | 11 | ✅ covered |
| CLO-13 | 5 | ✅ covered |
| CLO-14 | 6 | ✅ covered |
| CLO-15 | 12 | ✅ covered |

The authoritative per-case mapping is the front matter; the
validator confirms every case has non-empty CLOs resolving to the
course CLO register.

## 6. Instructor Solution Split

- **Student-facing:** the 100 case files in module trees — no
  model solutions, expected reasoning, tradeoffs, or prompts.
- **Instructor-only:** `teaching/case-solutions/cs-NNN-solution.md`,
  all front-mattered `instructor-only: true` /
  `distribution: never-publish-to-students` — model solution,
  alternatives, tradeoffs, common mistakes, prompts, rubric.
- Separation validated: student files contain no solution
  sections; solution links resolve.

## 7. Pedagogy Protocol (classroom use)

1. **Project the case** (5 min): scenario + evidence tables; no
   solution material is ever projected.
2. **Reason** (~5 min): individuals or pairs; scaffold questions
   on the slide from the case's *Student Task*.
3. **Discuss approaches** (3–5 min): collect 2–3 student
   approaches before revealing anything; the *Instructor Prompts*
   section (solution file) drives this.
4. **Reveal the model solution**: from
   `teaching/case-solutions/` — alternatives and tradeoffs last,
   so the first reveal is reasoning-shaped, not answer-shaped.
5. **Tradeoff analysis**: the case's *Tradeoffs* + *Common
   Mistakes* sections close the loop; exit ticket optional for
   graded variants.
6. **Rubric**: solution-file rubric for graded use; the
   difficulty tier sets the depth expected in reasoning, not just
   the answer.

## 8. Validation

`docs-meta/validate_cases.py` checks: 100 cases + 100 solutions,
numbering continuity, 19 required elements, tier counts
(20/25/30/25), front-matter fields (clos, anchor, solution link),
solution separation, and no solution content in student files.
Results are recorded in the validation report; no fabricated
results in this index — run the validator for current state.
