---
case: cs-092
title: Capstone II — Remediation Roadmap (Solution)
difficulty: expert
module: 8
lecture-anchor: L30
clos: [CLO-15]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-092 — Solution: Remediation Roadmap Under Constraints

> **INSTRUCTOR ONLY.** Model solution for cs-092.

## Model Solution

### 1. Six-month roadmap (3 staff, dependency-ordered)

| Month | Workstream | Owner | Output |
|---|---|---|---|
| 1 | **IR plan activation**: draft → review → tabletop with ops+DS reps | CISO + sysadmin-1 | Live IR plan, tested comms tree |
| 1–2 | **VPN MFA** for the 30 legacy users (pilot 5 → all) | net-admin | MFA enforced; exception register empty |
| 2–4 | **EDR rollout** to remaining 40% servers (batches by criticality: data-holding first) | sysadmin-2 | 100% server coverage + agent-offline alerting |
| 3 | **Tabletop #2** using EDR alerts (detection→response drill) | CISO | Tested detections, tuned runbooks |
| 3–5 | **Quick wins + hygiene**: public S3 closed (1 d), notebook-repo credential purge + pre-commit hook (2 d), DA reduction to ≤8 with JIT elevation (process, weeks) | shared | Findings F1/F3/F4 closed or shrunk |
| 4–6 | **Design only** (not build): segmentation + zero-trust design doc for next budget cycle | net-admin (20% time) | The cs-093/094 design input |
| 5–6 | **Access-review + vuln-mgmt cadence institutionalization** | CISO | The process evidence the questionnaire wants |

**Deliberately deferred:** segmentation build (12–18 months,
needs dedicated eng), NDR purchase (detection value real but staff
band absent — EDR completion first), DS data-platform re-architecture
(design-only this cycle). Deferral logic: staff-band + dependency
order, not importance.

### 2. The 60-day questionnaire play

**Fastest evidence (already fundable in month 1–2):** IR plan
(exists + tabletop minutes), VPN MFA (config export), EDR coverage
(coverage report), vuln-mgmt cadence (scan schedule + SLA doc),
access reviews (calendar + first review's output).

**Honest in-progress answers:** segmentation ("designed, build
scheduled next FY"), NDR ("evaluating, EDR completion first"),
DA reduction ("in progress, 41→28 at submission, target 8").

**Must NOT be fudged (answer truthfully even if it costs):** MFA on
*all* remote access (the exception register must be empty or the
"no" is permanent — answer "partial, complete by [month 2]"), and
any question about *incident history* (the honest answer is the
one whose paper trail exists).

**Evidence trick:** the questionnaire's "describe your process"
questions are answered with *artifacts of the roadmap itself* —
tabletop minutes, rollout reports, review calendars. Nothing is
written for the questionnaire that the roadmap doesn't produce.

### 3. DS velocity conflict — the implementation shape

- **EDR on servers, not on notebook runtimes:** EDR lands on the
  *server fleet* (training hosts get it too, but policies tuned:
  no scan-storms during scheduled training windows, performance
  tag in policies). Developer endpoints get standard policy; the
  *interactive* workflow (notebooks, experiments) is not the
  enforcement point.
- **Data governance via platform, not per-run friction:**
  bucket policies fixed once (public → CF/VPCE-only), credentials
  moved to a secrets manager with **role-based access at
  session-start** (one re-auth per session, not per run) +
  pre-commit hook in the shared repo (zero runtime cost).
- **The deal with the DS lead:** EDR rollout lands on *their*
  failure mode (the mining incident cs-088 pattern — a compromised
  node freezes the whole cluster for days). Velocity cost is
  bounded and *measured*: rollout batches report job-throughput
  delta; if >10%, policy tunes before proceeding. That's the
  acceptance mechanism — a *measured* guardrail, not a promise.

### 4. Quick wins (≤2 staff-days each)

| Win | Closes/shrinks | Days | Questionnaire value |
|---|---|---|---|
| Close 4 public S3 buckets | F3 (full) | 1 | data protection section |
| Pre-commit hook + repo credential purge | F4 (full) | 2 | credential management section |
| Agent-offline alerting rule in SIEM | F7 (part) | 0.5 | monitoring section |
| IR plan published + on-call card | F8 (full) | 1 | incident response section (the "exists and tested" answer) |
| MFA pilot on 5 VPN users | F2 (start) | 1 | remote access section |

## Alternative Solutions

- **Hire a responder before tooling:** defensible if budget allows
  staff not tools — with 3 staff, the CISO *is* the responder;
  the roadmap's tabletop cadence is the substitute.
- **Buy NDR month 1:** strongest detection add, rejected for staff
  band — an unwatched sensor is shelfware; sequence after EDR.

## Tradeoffs

- Questionnaire honesty vs funding optics: "in progress" answers
  with real artifacts beat fudged "yes" answers that diligence
  interviews demolish.
- Build vs design: segmentation *design* this cycle costs 20% of
  one engineer and makes next year's ask credible; building it
  half-way with 3 staff risks worse than not starting.

## Common Mistakes

- Parallel workstreams for a 3-person team (nothing finishes).
- Writing questionnaire answers with no producing artifact.
- Meeting the DS guardrail by excluding DS assets from controls
  (creates the safe zone cs-088 exploited).
- Deferring the IR plan because "tooling is more urgent" — the
  plan is the multiplier.

## Instructor Prompts

- "Which questionnaire answer is worth the most per artifact-hour?"
- "What makes the DS lead's acceptance *measured* rather than
  promised?"
- "If one sysadmin resigns in month 3, which workstream slips and
  which must not?"

## Rubric (10 pts)

| Criterion | Pts |
|---|---|
| Roadmap: dependency logic + realistic staffing + deferrals | 3 |
| Questionnaire play: honest-in-progress + two must-not-fudge | 3 |
| DS velocity solution (platform-side, measured guardrail) | 2 |
| Quick wins: ≤5, sized, mapped to findings | 2 |

## Safety Notes

- Simulated; no real vendor or customer implied.
