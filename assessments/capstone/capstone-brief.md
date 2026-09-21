---
capstone: brief
type: student-brief
clos: [CLO-11, CLO-14, CLO-15]
weeks: [9, 16]
weight: 15%
teams: 3-4
status: complete
artifact-type: student-capstone
related-rubrics: [assessments/capstone/capstone-rubric.md, assessments/capstone/defense-guide.md]
---

# Capstone Project — Design, Build, Exercise, Defend (Weeks 9–16)

> **Weight:** 15% · **Team:** 3–4 students · **CLO-11, CLO-14, CLO-15**
> **Supervisor checkpoint:** weeks 11 and 14 (mandatory, 10 min each).

## The mission

Design and defend a **secure network architecture** for a simulated
organization, implement its key controls on the course range, run an
incident exercise against it, and defend the whole at a 25-minute panel.

**Pick an organization profile** (or propose one):
1. Regional hospital (500 staff, medical IoT, patient records, vendor
   remote access).
2. FinTech scale-up (300 staff, payment API, cloud VPC + on-prem office,
   cardholder-data scope).
3. Research university department (DS clusters, 2,000 students, guest
   access, federally funded datasets).
4. Logistics firm (600 staff, warehouse scanners, partner EDI links,
   8 branch sites).

## The four deliverables (weeks 9→16)

### D1 — Architecture & Security Design (week 11 checkpoint)

- Network diagram (zones, enforcement points, telemetry taps).
- Threat model (top 6 threats on theSTRIDE/case-study patterns from the
  course; each with its control).
- Control set: segmentation, remote access, wireless, detection,
  vulnerability management, IR readiness — each with its *verification
  method* (how you'd prove it works).
- **Constraints to honor:** budget realism (staff of 3 in IT), no
  control without a stated tradeoff, at least one deliberate deferral
  with accepted risk (the cs-098 discipline).

### D2 — Build & Evidence (week 14 checkpoint)

- Implement ≥4 controls on the course range (typical: segmented VLANs
  with firewall policy, VPN with MFA simulation, Suricata/Zeek detection
  with one custom rule, hardening baseline + verification scan).
- Evidence pack: configs, screenshots, detection replay results
  (before/after on course datasets), the verification method output for
  each control.
- **The honesty rule:** every control's evidence states what was *tested*
  vs *assumed* (the lab's tested-vs-untested labeling standard).

### D3 — Incident Exercise (week 15)

- Run the instructor-provided inject series (3 injects, 90 minutes)
  against your architecture with your team in role.
- Deliverable: exercise record — decisions with reversibility labels,
  what your design caught/missed, two owned amendments.

### D4 — Report & Defense (week 16)

- Written report (12–18 pages): design, build evidence, exercise record,
  the board paragraph (cs-094 structure), and the honest-limits section.
- **Panel defense** (25 min: 10 presentation + 15 questions) — prepare
  via the defense guide and Self-Check Quiz 16.

## How it's graded

- Design quality (not size), evidence integrity, exercise learning,
  defense coherence. Full rubric: `capstone-rubric.md` (instructor copy
  with band anchors; the student-visible weightings are there).
- The panel asks from the defense guide's five archetypes; the honest
  weakness statement is expected, not penalized.

## Safety & authorization

- All work on the isolated course range; no external scanning, no real
  organizational data, no offensive tooling in deliverables.
