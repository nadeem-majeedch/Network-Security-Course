---
case: cs-091
title: Capstone I — Breach-Readiness Assessment (Solution)
difficulty: expert
module: 8
lecture-anchor: L29
clos: [CLO-15]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-091 — Solution: Breach-Readiness Assessment

> **INSTRUCTOR ONLY.** Model solution for cs-091.

## Model Solution

### 1. Assessment plan (2 assessor-weeks, ordered by dependency)

| Days | Activity | Why this order |
|---|---|---|
| 1–2 | **Ground truth vs diagrams**: asset inventory reconciliation (CMDB vs scans vs AD) | Every later finding needs a true asset list; diagrams are aspirational |
| 3–4 | **Identity review**: DA population, service accounts, MFA coverage | Identity findings gate the architecture findings' severity |
| 5–6 | **Perimeter + segmentation review**: rulebase sample-audit, VPN/MFA, VLAN design | Depends on asset list (what's actually exposed) |
| 7–8 | **Cloud review**: both accounts, S3 exposure, peering, sandbox root | Depends on identity review (root MFA, cross-account roles) |
| 9–10 | **Detection/response review**: SIEM coverage map, EDR coverage %, IR plan liveness, MTTD analysis | Detection findings *quantify* the multiplier for all prior findings |

Deliverable cadence: findings register drafted continuously, not at
the end — evidence vintages recorded as collected.

### 2. Findings register (model — 12 findings)

| # | Finding | Evidence (vintage) | Scope | Risk + quantification | Class |
|---|---|---|---|---|---|
| F1 | 41 domain admins (0.2% expected ≈ 5–10) | AD export (current) | 41 accounts | Privilege-escalation surface ×41; each a phish target | Prevent |
| F2 | VPN without MFA (legacy team) | config (current) | ~30 users | Initial-access vector; MTTD 19–41 d → attacker dwell ×20+ | Prevent |
| F3 | 4 public S3 buckets with research data, ≥6 months | bucket policy (current) | research PII | Direct exposure; funder/compliance breach | Prevent |
| F4 | Cached credentials in shared notebook repo | repo scan (current) | DS group + data lake | Credential chain into prod account | Prevent |
| F5 | 28% "any-source" fw rules, unreviewed 3 y | rulebase (current) | both DCs | Lateral movement paths; segmentation fiction | Prevent |
| F6 | Servers/workstations co-segmented | as-built review (current) | 10.0.0.0/16 | Workstation compromise = server reach | Prevent |
| F7 | EDR on 60% of servers; no NDR | coverage map (current) | 40% server fleet | Detection gap on exactly the asset class that holds data | Detect |
| F8 | No live IR plan (2 y draft) | doc review | whole org | Response capability near-zero; MTTR unbounded | Respond |
| F9 | Sandbox root without MFA | AWS config | ds-sandbox | Full sandbox compromise path; peering → prod | Prevent |
| F10 | Asset inventory 70% accurate | reconciliation | whole estate | Every control's coverage is overstated by the same 30% | Prevent (foundational) |
| F11 | Scans authenticated on 60% | scan config | server fleet | Vulnerability visibility gap; remediation flying blind | Detect |
| F12 | No detection on data-lake access anomalies | SIEM coverage map | data lake | Exfil detectability ≈ nil; ties to F3/F4 | Detect |

### 3. Priority argument (3 funded this quarter)

1. **F8 — IR plan activation + tabletop.** Rationale: with MTTD at
   19–41 days, intrusion is *likely already survivable only by
   response*; response capability multiplies the value of every
   other control and is the cheapest to stand up (a live plan +
   tabletop costs weeks, not quarters). The MTTD history makes
   "respond faster" the highest-leverage investment.
2. **F2 — VPN MFA.** Closes the cheapest initial-access vector;
   the phishing-intrusion chain (first-hour cases) begins here.
   Small scope (~30 users), immediate risk-reduction per dollar.
3. **F7 — EDR to 100% of servers (+ agent-offline alerting).**
   The detection multiplier argument: 40% of servers blind during
   19–41-day dwells. Partial coverage gives attackers a *known
   safe zone* — attackers find coverage boundaries.

Not funded now but sequenced: F1 (DA reduction — process-heavy),
F5/F6 (segmentation — architecture work), F3/F4 (DS governance —
needs the velocity negotiation; cs-092's design phase handles it).

### 4. Methodology defensibility

- **Evidence vintages on every finding** (current config, scan
  date, doc date) — no stale-evidence conclusions.
- **Reproducibility:** each finding cites the exact commands/
  queries (AD export filter, bucket-policy dump, SIEM query) so the
  auditor can re-run them.
- **Scope honesty:** the cannot-assess list (physical security, app-
  layer testing out of scope) stated up front.
- **As-built vs as-designed discipline:** findings marked when they
  contradict the *diagrams* — the gap itself is a finding (F10).
- **Quantified risk:** MTTD history used as the detection
  multiplier, not adjectives.

## Alternative Solutions

- Prioritizing F1 (41 DAs) first: defensible on raw severity, but
  it's a *process* campaign (role design, ticketing) with slow risk
  burn-down vs F2's immediate vector closure.
- Prioritizing F3 (public S3) first: defensible given funder
  exposure; the counter is that it's a one-week fix that doesn't
  need *quarter funding* — fix it immediately outside the portfolio.

## Tradeoffs

- Breadth vs depth in 2 weeks: coverage of all 6 capability areas at
  sample-depth beats deep-diving one (the estate's weakness is
  systemic, not local).
- Detection vs prevention spending: the MTTD history biases toward
  detection/response *this quarter*; prevention work proceeds in
  parallel lanes.

## Common Mistakes

- Sorting findings by severity score alone (ignores the MTTD
  multiplier and dependencies).
- Accepting the aspirational diagrams as evidence.
- Findings without evidence vintage — indefensible at audit.
- Funding 3 *prevention* findings while MTTD is 19–41 days.

## Instructor Prompts

- "Why does the asset reconciliation come before everything?"
- "Defend funding a *response* finding over a *prevention* one."
- "What would the shadowing auditor flag first in your evidence?"

## Rubric (10 pts)

| Criterion | Pts |
|---|---|
| Assessment plan ordered by dependency, 2-week realistic | 2 |
| Findings register: 10–14, evidence-vintaged, quantified | 3 |
| Priority argument using MTTD as multiplier + portfolio logic | 3 |
| Methodology defensibility (reproducible, scope-honest) | 2 |

## Safety Notes

- Simulated; no live testing described.
