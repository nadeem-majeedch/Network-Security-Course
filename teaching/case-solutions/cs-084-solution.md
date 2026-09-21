---
case: cs-084
title: RTO vs Evidence — Recovery-Speed Conflict (Solution)
difficulty: expert
module: 7
lecture-anchor: L27
clos: [CLO-11, CLO-14]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-084 — Solution: RTO vs Evidence

> **INSTRUCTOR ONLY.** Model solution for cs-084.

## Model Solution

### 1. Recovery path: (c) rebuild + restore to new hostname/segment

| Path | Speed | Evidence | Re-infection risk |
|---|---|---|---|
| (a) restore to FS01 as-is | 4 h | OK (image captured) | **High** — unknown persistence on host |
| (b) rebuild + restore same name | 2 d | OK | Medium — attacker's environment knowledge intact |
| **(c) rebuild + new name/segment** | 2 d | OK | **Low** — breaks attacker's map |
| (d) restore now + rebuild later | 4 h + 2 d | OK | High now, lower later |

**(c)** wins when the persistence question is unresolved: it accepts
the 2-day cost to drive re-infection risk near zero, while preserving
evidence (image already captured day 1 — the 6-hour forensic add-on
is already sunk). The CIO's "restore in parallel" is fine **only**
under path (c) — restoring clean data onto a clean, *unfamiliar*
destination.

### 2. Go/no-go criteria (L27 recovery board, applied)

All must be true before restore:
1. Persistence mechanisms identified **and** confirmed bounded (W-77's
   task/service — with an explicit statement of what was *not* found).
2. Source of initial access closed (phishing path + W-77 rebuilt).
3. Egress/staging domain still blocked; no beaconing in flow since
   containment.
4. Backup generation verified clean (see §3).
5. Destination built from *current* golden image, patched against the
   initial-access vector, and placed on a new segment/name.
6. Business sign-off recorded accepting residual risk.

### 3. Backup generations: keep vs quarantine

- **Keep:** the 18:00 day-0 backup (pre-incident) — the canonical
  restore point.
- **Keep with caveat:** backups from the isolation window — the
  server was network-contained, so data writes came only from
  legitimate processes; risk is *low but not zero* (attacker could
  have planted delayed-execution content before containment). Spot-
  check for suspicious executables/scripts in restored content.
- **Quarantine:** nothing here *needs* deleting, but the generation
  boundary must be documented: any backup from *before* 18:00 day 0
  is stale; any claim of post-event attacker writes to the share must
  quarantine the affected generations.

### 4. Overrule compromise schedule

If the CIO forces speed: **restore to the new segment from the 18:00
day-0 backup only**, host on the freshly built server, keep the
blocked egress, and add compensating monitoring (Zeek on the new
segment + EDR heightened policy) for 14 days. **Written risk
acceptance:** "Restored data predates the incident by ≥6 h; users
re-create any changed-in-final-6-hours work; residual risk is
delayed-execution content in restored files, mitigated by content
spot-checks and heightened monitoring."

## Alternative Solutions

- **(d) restore-now:** defensible if finance pressure is existential;
  the write-up must name the accepted risk explicitly.
- **Wait for full eradication confirmation:** safest, but 2 days of
  $18k/h is $864k — disproportionate if go/no-go criteria are already
  satisfiable.

## Tradeoffs

- Speed vs certainty: every hour saved is $18k against a low-
  probability but high-impact re-infection.
- Same-name restore vs new-name: zero user friction vs breaking the
  attacker's map (and any name-based persistence, e.g., scripts
  referencing \\\\FS01).

## Common Mistakes

- Treating all backups during the window as tainted (containment
  changes the calculus).
- Rebuilding with the same hostname and calling it eradicated.
- No written risk acceptance when overruled — the paper trail *is*
  the lesson-learned.

## Instructor Prompts

- "Which go/no-go criterion is hardest to verify — and what's your
  proxy for it?"
- "What does the new hostname/segment actually buy you?"
- "If the CIO overrules, what *must* be in writing before the restore?"

## Rubric (10 pts)

| Criterion | Pts |
|---|---|
| Path choice with all three objectives explicit | 3 |
| Go/no-go list (≥5 criteria, correct) | 3 |
| Backup-generation reasoning correct | 2 |
| Overrule compromise with written risk acceptance | 2 |

## Safety Notes

- Simulated; no ransomware artifacts or real-incident references.
