---
artifact-type: lab-inventory
status: complete
instructor-only: false
last-updated: session 5 (lab curriculum)
---

# Lab Curriculum Inventory & Validation Report

Status ledger for the practical lab layer: `docs/labs/` (student handouts +
datasets), `teaching/lab-answer-keys/` (instructor-only). This document records
what exists, what was tested, and what remains open. Nothing here is claimed
complete unless it is.

## 1. What exists now

| Layer | Files | Contents |
|---|---|---|
| `docs/labs/README.md` | 1 | Lab program overview, range requirements, tested-vs-untested labeling policy, submission norms |
| `docs/labs/lab-01…16-*.md` | 16 | Student handouts, Lab-01…Lab-16, one per week, weeks 1–16 |
| `docs/labs/setup/generate_lab_datasets.py` | 1 | Stdlib-only, seeded PCAP/flow/log generator (reproducible) |
| `docs/labs/datasets/` | 7 | 6 datasets + SHA256SUMS (verified) |
| `teaching/lab-answer-keys/lab-01…16-answer-key.md` | 16 | Instructor-only keys: expected observations, analysis answers, grading anchors, rubric application, cleanup verification |

**Lab-01…Lab-16 numbering is normative** — it matches the syllabus calendar and
CLO matrix exactly (Lab-N runs in week N). Do not renumber.

## 2. Lab-to-mission-core-lab mapping

| # | Mission core lab | Course lab | Week | Lectures | CLO | Dataset |
|---|---|---|---|---|---|---|
| 1 | Baseline & topology documentation | Lab-01 Range Orientation & Baseline | 1 | L01, L02 | CLO-1 | — (live range) |
| 2 | Wireshark packet capture & analysis | Lab-02 Wireshark Protocol Analysis | 2 | L03, L04 | CLO-1 | lab02-normal-traffic.pcap |
| 3 | DNS/DHCP/ARP/TCP-IP investigation | Lab-03 L2 Attack Evidence (ARP/DHCP) | 3 | L05, L06 | CLO-2 | lab03-l2-attacks.pcap |
| — | (attack telemetry, mission-supported) | Lab-04 MITM & Flood Telemetry | 4 | L07, L08 | CLO-3 | lab04-mitm-flood.pcap |
| 5 | Segmentation & secure architecture | Lab-05 Segmentation/Proxy/Egress Design | 5 | L09, L10 | CLO-4 | — (design) |
| 4 | Firewall rules & ACL design | Lab-06 Firewall Rulebase & ACL Audit | 6 | L11, L12 | CLO-5 | — (rulebases in handout) |
| 6 | TLS/certificate inspection | Lab-07 PKI & TLS Audit | 7 | L13, L14 | CLO-6 | — (lab PKI) |
| 7 | VPN concepts & configuration | Lab-08 Site-to-Site VPN | 8 | L15, L16 | CLO-7 | — (lab VPN) |
| 11 | Wireless security analysis (safe) | Lab-09 Wireless Characterization & Cloud Seg | 9 | L17, L19 | CLO-12 | — (authorized capture) |
| — | (cloud flows, mission-scope: cloud networking) | Lab-10 WPA-Enterprise & Cloud Flow Logs | 10 | L18, L20 | CLO-13 | — (lab WPA + flow logs) |
| 8 | IDS/IPS or monitoring w/ prepared traffic | Lab-11 Flow Collector & Suricata | 11 | L21, L22 | CLO-8 | lab11-flows.csv |
| — | (behavioral detection, mission-scope: monitoring) | Lab-12 Zeek & Vulnerability-Hardening Cycle | 12 | L23, L24 | CLO-9/CLO-10 | — (lab Zeek + scanner) |
| 12 | Incident response using network evidence | Lab-13 Incident Triage | 13 | L25, L26 | CLO-11 | lab13-incident.pcap |
| — | (hunting, mission-scope: threat intel/hunting) | Lab-14 Tabletop Threat Hunt | 14 | L27, L28 | CLO-14 | — (prepared hunt pack) |
| — | (forensics, mission-scope: network forensics) | Lab-15 Forensic Timeline & Report | 15 | L29, L30 | CLO-15 | lab15-forensics.pcap |
| — | (capstone IR simulation) | Lab-16 Capstone IR Simulation | 16 | L31, L32 | CLO-11/CLO-15 | lab13-incident.pcap (extended) |

All 12 mission core labs are covered; the 4 additional labs (04, 10, 14, 16)
come from the course's own scope requirements (attack telemetry, cloud,
hunting, capstone).

## 3. Validation — actual observed results

**Command:** `python docs-meta/validate_labs.py` — **13/13 PASS, exit code 0**.

| Check | Result |
|---|---|
| B1a/b — 16 handouts, weeks 1–16 aligned to file numbers | ✅ |
| B2 — all 17 required sections present in every handout | ✅ |
| B3 — front matter complete (lab id, week, module, CLOs, lectures, key link) | ✅ |
| B4a/b — 16 instructor keys, substantive, `instructor-only: true` | ✅ |
| B5a/b — no instructor-only material leaked into handouts; key links resolve | ✅ |
| B6 — no placeholder markers in pages marked `status: complete` | ✅ |
| B7 — CLO mapping matches the syllabus matrix exactly | ✅ |
| B8 — every lab maps to its week's lectures; all lecture files exist | ✅ |
| B9 — datasets present, SHA256SUMS verified (6 files) | ✅ |
| B10 — authorization/safety section present in every handout | ✅ |

**Cross-gate regression:** `validate_plan.py` (20/20), `validate_teaching_plans.py`
(14/14), `validate_teaching_materials.py` (18/18) — all still green.

### First-run failures and triage (honest record)

1. **Validator bug (fixed in `validate_labs.py`):** a string/int comparison in
   the section-count check crashed on handouts with extra sections; and the
   authorization check's pattern missed the word "authorization" when only
   "authorized" appeared. Both fixed in the validator, not by loosening to
   vacuous passes — the checks now assert what the mission requires.
2. **Real content gap (fixed in 13 handouts):** Lab-02, 03, 04, 05, 06, 07, 08,
   10, 11, 12, 14, 15, 16 lacked an explicit *authorization basis* bullet in §7
   (they said "authorized" implicitly via lab-range language but not the
   governing word). Each now states its authorization basis explicitly — e.g.,
   Lab-03: "Authorization basis: detection-only analysis of a prepared,
   instructor-provided PCAP; no scanning, no live attacker tooling, range
   systems are the only permitted targets for any active step."
3. **Two handouts needed the word "only":** Lab-05 (design exercise *only*, no
   live systems) and Lab-07 (PKI work lab-scope *only*) now state the boundary
   unambiguously.

### Tested vs untested (mission technical requirement)

| Item | Status |
|---|---|
| `generate_lab_datasets.py` | **Tested** — runs clean on Python 3, deterministic (seeded), SHA256SUMS matches regenerated output twice |
| Dataset integrity (structurally parseable PCAP/CSV) | **Tested** — headers parsed, record counts verified post-generation |
| Lab-02/03/11/13/15 analysis commands (tshark/zeek/csv workflows) | **Untested in a live environment** — command shapes are standard tool usage against tested datasets; instructors should smoke-test in their range before first delivery. Labeled untested inside the handouts |
| Lab-01/05/06/07/08/09/10/12/14/16 environment steps (VM/container bring-up, lab PKI, WPA-Enterprise AP, cloud sandboxes) | **Untested** — depend on each institution's range; handouts mark them untested and provide fallbacks |

No fabricated results: nothing in this repo claims a lab was executed against a
live range unless this session actually executed it (only the generator and
checksum verification were executed here).

## 4. Safety posture (mission rules)

- Every handout §7 states scope, authorization basis, and prohibited actions;
  prohibited actions include real-world scanning, credential capture outside
  the range, and any destructive payload.
- Attack-adjacent labs (03, 04) are **evidence-analysis labs**: students detect
  attacks in prepared captures; they do not execute attack tooling. The
  handouts say so explicitly.
- Datasets contain no destructive or persistence-focused payloads — only
  benign-but-detectable traffic patterns (ARP spoofing pairs, SYN floods,
  DNS-tunnel-looking exfil patterns) for defensive interpretation.
- Every lab includes defensive interpretation + remediation steps (§ analysis
  and in the keys).
- Keys and handouts label cleanup/teardown steps; keys verify them.

## 5. Remaining gaps (honest scope)

These labs are complete *as authored* (handouts + keys + datasets + generator).
Still open per the master inventory:

- VM/container provisioning automation (Vagrantfile/compose) for the range —
  the handouts describe the topology but no provisioning scripts are authored.
- Slide assets for lab briefing decks.
- Lab-exam variant (a timed, graded lab assessment) — mentioned in the syllabus
  but not yet authored.
- GitHub Pages build + CI workflows (whole-repo gap, not lab-specific).
- Quizzes/exams/assignments and the 100 case-study files (separate layers).

## 6. Change log — session 5

- Created `docs/labs/README.md`, 16 handouts, 16 keys, dataset generator.
- Generated + verified 6 datasets (2 generation runs, checksums stable).
- Fixed TCP data-offset bug in generator (was `5 << 12`, must be `5 << 4`).
- Fixed validator string/int bug + authorization-pattern gap.
- Added explicit authorization-basis bullets to 13 handouts; "only" boundary to
  Lab-05/Lab-07.
- Authored `validate_labs.py`; final result 13/13 PASS.
