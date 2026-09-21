---
case: cs-100
title: Capstone Integration — Full-Scope Walkthrough (Solution)
difficulty: expert
module: 8
lecture-anchor: L32
clos: [CLO-14, CLO-15]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-100 — Solution: Full-Scope Incident Walkthrough

> **INSTRUCTOR ONLY.** Model solution for cs-100.

## Model Solution

### 1. Phase-by-phase walkthrough (with before/after delta)

| Phase | Capability exercised (course) | Decision | Evidence basis | Pre-program delta |
|---|---|---|---|---|
| **Detection** | MTTD discipline + anomaly detection (M6, cs-067/068) | Trust the 11:05 impossible-travel alert; corroborate vs IdP + device logs | Two-source: IdP anomaly + session context | Pre-program: MTTD 19–41 d — this likely *never detected*; the 2.5 h MTTD is the program's headline |
| **Containment** | Reversibility labeling + credential-vs-host logic (cs-082/088) | Kill session, disable account (**reversible**); do *not* wipe the user's device — it's not implicated | Single-source trigger, corroborated at action time by IdP logs | Pre-program: VPN without MFA → attacker would have had network-level access; containment would have been host-hunt, not session-kill |
| **Eradication** | Hunt falsification (cs-096 H4) + persistence discipline (cs-085's burn-everything rule applied to tokens) | Day-1 hunt replay finds the *second* token → revoke; assume *all* session/refresh tokens for the identity are burned | Hunt replay = systematic, not lucky | Pre-program: no hunt capability — the second token survives, re-entry follows in days |
| **Recovery** | Awareness-vs-certainty (cs-090) + go/no-go criteria (cs-084) | Re-enable after token revocation + device compliance check; finance app access *stays restricted* until policy gap closes | Criteria list, not optimism | Pre-program: ad-hoc restore decisions |
| **Post-incident** | cs-086 review conversion + cs-094 board format | 3 owned findings: holding-statement template (cs-099's gap), finance-app policy set review, push-fatigue number-changing rollout | Findings owned/dated/verifiable | Pre-program: 14 vague items, zero closure |

### 2. The MFA-approval lesson

The attacker beat MFA with *push fatigue* — a user approved a
fraudulent push. Honest limit: **MFA authenticates the factor, not
the approver's judgment; it stops credential theft, not session
and consent theft.** What bounded the damage anyway (both already
in the estate): **device trust** — the unmanaged-device policy
collapsed the session to read-only on a restricted app set (the
attacker hit the *edge* of that set, not its center), and
**detection** — the IdP anomaly rule plus the hunt's token-baseline
(H4) caught both the session and the persistence. The chain:
MFA-limit → device trust → detection → hunt. No single control;
the *stack* held at its weakest point's cost (3 invoice records).

### 3. Policy failure vs pilot-coverage failure

**This is a pilot-coverage failure, not a policy failure.** The
policy itself ("unmanaged device → read-only + restricted app
set") is *correct* and worked exactly as designed — the attacker
got read-only, which is why the export was 3 records, not the
database. The failure is that the finance app was **not in the
restricted set**: the app inventory (cs-093 step 3) hadn't
classified it yet. Distinction and fixes:
- **Policy failure** (rule wrong): fix = policy redesign with
  gate evidence (pilot data, SLO checks).
- **Coverage failure** (rule right, scope incomplete): fix =
  inventory completion + classification backlog burn-down with
  the *sensitivity-first* ordering (finance before pet-projects),
  plus a coverage metric in the board report ("apps classified:
  14/40") — coverage debt made visible, per cs-094's honesty
  discipline.
Boards conflate these; the report must not.

### 4. Board paragraph (≤120 words)

> "On [date], a phishing attack led to an MFA push being
> mistakenly approved; the attacker accessed one finance
> application from an unmanaged device and exported three
> invoice records affecting one individual. Our zero-trust
> controls restricted the session to read-only, anomaly detection
> ended the session within 2.5 hours, and a threat hunt found and
> revoked a second stolen token the same day — eliminating the
> persistence path. Two honest limits: MFA push fatigue remains
> a human-factors risk, and the finance app sat outside our
> strictest policy set because classification is incomplete.
> We ask the board to fund number-changing MFA rollout and the
> classification backlog's completion — both are scoped, owned,
> and scheduled within the existing program."

(119 words: incident, response, two limits, ask.)

## Alternative Solutions

- **Classifying it a policy failure:** over-corrects into
  redesigning a rule that worked — the coverage/ policy
  distinction exists precisely to prevent this misdirected
  spending.
- **Recovery without the app restriction:** faster user
  convenience, unacceptable — the gap is *known and open*;
  restoring full access before it closes recreates the condition
  (cs-084's written-acceptance logic applies if business
  overrules).

## Tradeoffs

- Session-kill speed vs user disruption: a 2.5-hour kill is fast
  enough that disruption is minor — the reversal asymmetry
  favors acting.
- Read-only fallback vs blocking unmanaged devices entirely:
  blocking is stronger but breaks the contractor population; the
  restricted-set model is the deliberate design tradeoff, and
  this incident is its validation (3 records, not 3,000).

## Common Mistakes

- Calling MFA "broken" (it worked; it was *insufficient alone* —
  the honest limit).
- Fixing the wrong layer (policy redesign instead of inventory
  completion).
- Omitting the second-token eradication (the hunt's whole
  value in one line — and the most commonly missed step).
- A board paragraph that reports activity instead of the
  ask-and-limits structure.

## Instructor Prompts

- "Which phase's decision would have gone *differently* under the
  pre-program estate — and what does that delta prove the program
  bought?"
- "Why is 'coverage failure' the more honest label here — and
  what would change your mind?"
- "What makes the board paragraph's two-limits structure credible
  rather than defensive?"

## Rubric (10 pts)

| Criterion | Pts |
|---|---|
| Walkthrough table: all 5 phases, capabilities, evidence bases, deltas | 4 |
| MFA-limit answer: honest limit + two bounding controls | 2 |
| Policy-vs-coverage distinction defended, fixes for each | 2 |
| Board paragraph ≤120 w with incident/response/limits/ask | 2 |

## Safety Notes

- Simulated; no real IOCs; course-taught concepts only.

---

*End of the 100-case collection. This case integrates the full
curriculum: modules 1–8, the IR lifecycle, the ZT program, the hunt
program, and the governance line from findings to board.*
