---
case: cs-095
title: Capstone V — First Full IR Exercise (Solution)
difficulty: expert
module: 8
lecture-anchor: L32
clos: [CLO-15]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-095 — Solution: Designing the First Full IR Exercise

> **INSTRUCTOR ONLY.** Model solution for cs-095.

## Model Solution

### 1. Inject schedule (4 h, 9 + 2 conditional)

| T | Inject | Tested objective | Scoring hook |
|---|---|---|---|
| 0:10 | EDR alert: mass rename on FS-mirror | Detection→triage start; who takes lead? | Lead named by 0:20? |
| 0:30 | SIEM: staging egress from same host | Corroboration (three-way rule) | Two-source check before decision? |
| 0:50 | **Decision point**: isolate FS-mirror? | Containment authority + reversibility labeling | Action labeled reversible/irreversible? |
| 1:10 | (conditional, if isolated) task-creation alert on a *second* host | Scope reassessment discipline | Re-corroborate before widening? |
| 1:10 | (conditional, if NOT isolated) encryption begins | Cost-of-delay lesson | Does the team re-plan under loss? |
| 1:30 | Controller as panicking VP demanding status | Comms accuracy under pressure | Status = facts + unknowns, no invention? |
| 2:00 | Synthetic "backup job ran during incident" query result | Backup-generation reasoning (cs-084) | Correct generation reasoning? |
| 2:30 | Controller as legal liaison: "regulator clock?" | Legal-escalation trigger | Trigger criteria stated correctly? |
| 3:00 | Inject: attacker "returns" (new beacon, blocked) | Eradication verification discipline | Re-verify before declaring recovery? |
| 3:30 | Recovery decision: restore path choice | Go/no-go criteria application | Criteria from cs-084 applied? |
| 3:50 | Stand-down + hot debrief start | Process closure | Actions → owned items? |

**Escalation arc logic:** scope starts single-host (confidence
building) → widens (second host) → pressure (exec + legal) →
complication (backup generation) → returns (eradication humility)
→ closure. The arc exercises the full cs-082→084→090 competency
chain in order.

### 2. Scoring rubric (5 criteria, observable anchors)

| Criterion | Good-decision anchor | Observer records |
|---|---|---|
| Corroboration discipline | ≥2 sources before containment decisions | Source counts per decision |
| Reversibility labeling | Actions labeled at decision time | Labels present/absent per action |
| Decision timeliness | Lead named ≤10 min; isolation decision ≤30 min from first alert | Timestamps vs inject times |
| Comms accuracy | Status contains facts + labeled unknowns; no invention | Verbatim quotes vs inject facts |
| Legal/regulatory trigger | Escalation criteria stated unprompted or on inject | Whether criteria cited correctly |

### 3. Zero-production-impact guarantee

**Structural rules:**
1. **Everything synthetic:** lab mirror estate, scripted EDR/SIEM,
  controller role-players. No production credential, host, or
  network is referenced by any inject; a credential leaked into
  the exercise is a real credential rotated after (rule: exercise
  uses *decoy* credentials only).
2. **Controller veto:** the exercise controller (you) holds a
  documented veto on any action that would touch production —
  participants operate *only* in the mirror; any real-system
  access attempt is an exercise finding itself (and a
  corrective-training item).

The veto is structural: the mirror is network-isolated from
production; there is *no path* to touch production even by
accident.

### 4. Debrief → board case

Findings convert via the cs-086 rule (owned, dated, verifiable) —
expected products of this design:

1. **Containment authority gap:** the 0:50 decision stalls — no
   named authority for server isolation off-hours. Fix: standing
   delegation-of-authority matrix (owner: CISO; date; done-state:
   matrix signed and exercised once).
2. **Legal-trigger ambiguity:** the 2:30 inject exposes that "when
   to call legal" lives in heads, not criteria. Fix: escalation
   criteria card in the IR plan (owner: legal liaison; done-state:
   card in plan + tabletop-verified).
3. **Backup-generation reasoning absent:** the 2:00 inject shows
   the team reasons from memory, not criteria. Fix: recovery go/
   no-go checklist added to the plan (owner: ops lead; done-state:
   checklist exercised in next backup test).

Board page: findings + owned fixes + the funding ask those fixes
imply (e.g., on-call authority tooling) — exercise → evidence →
funding, the cs-094 chain completed.

## Alternative Solutions

- **CTF-style technical exercise:** skills-testing but skips the
  governance layer (authority, legal, comms) this board asked for;
  better as the *next* exercise's advanced track.
- **Two shorter drills instead of one 4-hour:** better
  scheduling fit, breaks the escalation arc — the long arc is
  the point for a first full drill.

## Tradeoffs

- Scripted vs adaptive injects: conditional injects add
  controller workload but test *response to action* — the
  difference between a rehearsal and a test.
- Scoring granularity vs observer load: 5 criteria × 12
  participants is the practical ceiling for 2 observers.

## Common Mistakes

- Injects that test *knowledge* (quiz-like) instead of forcing
  *decisions*.
- No conditional injects — participants learn the script by
  inject 3.
- Scoring people instead of decisions (kills next year's
  participation).
- Letting the exercise touch production "just to make it real."

## Instructor Prompts

- "Which inject is the keystone — the one whose failure cascades?"
- "Why do conditional injects convert rehearsal into test?"
- "What does the board page look like if all 3 expected findings
  actually appear?"

## Rubric (10 pts)

| Criterion | Pts |
|---|---|
| Inject schedule: 9+2, objectives, escalation arc | 3 |
| Rubric: 5 criteria with observable anchors | 2 |
| Production-safety: structural rules, not promises | 2 |
| Debrief→board conversion with 3 expected findings | 3 |

## Safety Notes

- Simulated exercise design; synthetic telemetry only; no
  production-touching steps.
