---
assignment: assignment-05
type: answer-key
instructor-only: true
distribution: never-publish-to-students
clos: [CLO-10]
marks: 100
status: complete
---

# Answer Key — Assignment 5 (Vulnerability Management Program)

> **INSTRUCTOR ONLY.** Program-design assignment — anchors below.

## Grading anchors

### 1. Program lifecycle (25)
All six stages present with *role owners* (asset owner vs security vs
ops distinguished) = 20+; authenticated scans for server classes +
unauthenticated only for external view = the expected strategy split;
cadence tied to asset criticality (crown jewels weekly/monthly, the rest
quarterly) rather than one-size. Missing verification stage caps at 18.

### 2. Prioritization framework (25)
Must combine: CVSS base (10) + environmental (reachability/exposure/
criticality/compensating controls) (10) + known-exploited/threat intel
as an escalator (5). The worked example must *separate* two identical
scores — e.g., "CVE-A 9.8 on an internet-facing crown-jewel service vs
CVE-B 9.8 on an isolated host with compensating firewall: A = 24 h SLA,
B = standard window." Frameworks that output only "sort by CVSS" cap at
15/25.

### 3. SLA table (20)
Tiers (e.g., critical/known-exploited 24–72 h, high 7–14 d, medium 30 d,
low 90 d) with **clock-start defined** (the honest answer: at triage/
assignment — detection alone punishes the scanner team for backlog) (10);
exception path with named risk-acceptance owner + expiry + review (10).
Undefined clock-start caps at 14.

### 4. Metric set (20)
The four families with defined numerators/denominators/sources:
- **Works:** % criticals remediated within SLA (or MTTR-by-tier).
- **Matters:** incidents/exploitations linked to unpatched known vulns
  (target: zero; exposure-window days is the honest proxy).
- **Coverage:** % assets scanned in window (per authenticated split).
- **Decay:** median backlog age / % of backlog >90 d.
Numbers without definitions ("reduce backlog") cap at 12/20.

### 5. Quick-win plan (10)
Expected shape: (1) fix the *specific* two incident-linked vulns +
verify; (2) authenticated scan of the crown-jewel class (credibility
through better data, not more volume); (3) public SLA + burn-down
communication. 30-day realism required.

## Common failure patterns

- SLA clocks that start at "scan time" with no triage stage (operationally
  false — scans dump thousands at once).
- Metrics that are activity ("scans run") vs outcome (cs-094's decidability
  rule).
- No exception path — real programs die on the first unpatchable system.
