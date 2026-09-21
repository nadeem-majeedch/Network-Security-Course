---
case: cs-098
title: Capstone Design Defense (Solution)
difficulty: expert
module: 8
lecture-anchor: L31
clos: [CLO-15]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-098 — Solution: Design Defense Preparation

> **INSTRUCTOR ONLY.** Model solution for cs-098.

## Model Solution

### 1. Question bank (10 questions, 5 archetypes × 2, aimed at this design)

**Dependency:**
1. *"Your whole per-request model rides on one IdP. It goes down
   Monday 9 a.m. — what happens?"* → Answer: break-glass local
   auth for defined critical apps (documented in phase-3 runbook),
   fail-closed for the rest; recovery SLA from the IdP vendor;
   the *dependency is named as F-candidate* in the design's risk
   register (cs-093 §2) with this exact scenario exercised at the
   phase gate.
2. *"ERP can't do per-request auth natively — you're wrapping a
   legacy app. What breaks when the wrapper is bypassed?"* →
   Answer: the wrapper is front-door-only; compensating control is
   network-path restriction (only the wrapper's path can reach
   ERP — the legacy-tail segmentation, cs-092 design doc), so a
   bypass requires already-internal access; detection on direct
   ERP connections is a phase-3 detection deliverable.

**Adversarial:**
3. *"How does your design fail silently?"* → Answer: the honest
   candidate is policy-engine drift (rules accumulating exceptions
   until the model is perimeter-with-extra-steps); countermeasure:
   quarterly policy review with exception-expiry (cs-086's aging
   rule applied to ZT policy), exception count as a board metric.
4. *"Which control do you *hope* works but haven't tested?"* →
   Answer: break-glass procedures — named as untested until the
   phase-3 exercise (cs-095 pattern) runs them; the design's
   honesty requirement is to list untested controls, not to
   pretend the register is empty.

**Alternative:**
5. *"Why not just buy a SASE product and call it zero trust?"* →
   Answer: product ≠ policy model (cs-093 §1); procurement without
   identity consolidation inherits the AD/AWS split — the
   prerequisite chain exists because phase-2's pilot proved the
   model first (98.5% decision success, ≤7% overhead — measured,
   not vendor-slideware).
6. *"Segmentation instead of ZT — half the cost, proven
   tech?"* → Answer: segmentation is *in* the design (legacy
   tail); ZT adds the remote-access and identity model that
   segmentation cannot deliver (cs-093 phase gates evidence);
   they're complementary, not competing.

**Scope:**
7. *"What did you deliberately NOT do?"* → Answer: phishing-
   resistant MFA everywhere, DS data-platform re-architecture,
   NDR on user VLANs — each named with the pairing control that
   covers it meanwhile (cs-093 §3 discipline applied to phase 3).
8. *"What's out of scope that a peer would have included?"* →
   Answer: supply-chain/integrity controls on the vendor update
   channel (cs-089's lesson) — deferred to the platform team with
   a named owner; stated as a gap, not a claim of coverage.

**Evidence:**
9. *"What measured result backs the phase-3 claims?"* → Answer:
   phase-2 gate evidence (access-success rate, velocity probe),
   tabletop findings (cs-095's three owned fixes), MTTD trend
   (cs-094) — the chain from metrics to this tranche.
10. *"If MTTD regresses to 30 days next quarter, what in the
    design is wrong?"* → Answer: regression points to coverage
    gaps in the new planes (IdP/token telemetry — H4 of cs-096's
    hunt design was exactly this check); first response is the
    hunt's falsification discipline, not panic tuning.

### 2. Honest-weakness statement (by you first)

> "The design's weakest dependency is the IdP: phase 3 makes it
> the policy-decision root for branch, ERP, and admin access. My
> mitigation is break-glass local auth for four named critical
> apps, fail-closed elsewhere, tested at the phase gate. If that
> mitigation fails — the break-glass is stale or insufficient —
> the fallback is time-boxed manual access grants with
> compensating session logging, which I accept is a temporary
> reduction to cs-094's reported posture, and the board page
> would say so."

Weakness + mitigation + fallback + *who gets told* — the four
parts panels listen for.

### 3. Fallback positions (pre-negotiated)

**"Cut phase 3 to save money":** would cut branch-site ZT
last-first (it's the largest cost, lowest current risk — SaaS
traffic already direct), *keep* privileged-access migration (the
highest-concentration risk, cs-094's argument), and accept in
writing: branch sites remain location-trusted for one more year
with detection coverage unchanged. **Never cut:** privileged
access, policy-engine exception hygiene.

**"Cut legacy-tail segmentation":** would cut the *build* but
keep the design + the ERP path-restriction piece (the specific
control that answer 2 depends on); accept in writing: legacy
hosts remain co-segmented (cs-091 F6 stands open, reported as
such). **Never cut:** the ERP wrapper-path restriction — it's a
dependency of the whole per-request story.

### 4. Stress-test swap (what breaks defenses, from experience)

Expected findings from the 10-minute attack: candidates survive
**evidence questions** (artifacts ready) and **alternative
questions** (prepared), but break on **adversarial chains** —
"how does it fail silently" followed by "and who watches the
watcher?" The fix that transfers: every answer names its *own
monitoring* (who checks the check). Feed back: add to answers 3
and 4 a named reviewer cadence, and to the weakness statement a
reviewer for the break-glass test.

## Alternative Solutions

- **Full mock-defense rehearsal with faculty:** stronger than a
  partner swap if time allows; this design fits the course's
  one-week window.
- **Written-only defense doc:** needed as the artifact, but the
  live question dynamic is the skill being trained — the swap is
  the irreplaceable part.

## Tradeoffs

- Prepared answers vs authenticity: model answers are scaffolds;
  panels detect recitation — the prep's value is the *evidence
  chain*, not the script.
- Weakness-first vs strength-first framing: weakness-first costs
  the opening's momentum and buys the room's trust.

## Common Mistakes

- Preparing answers for questions you *like*, not the five
  archetypes.
- A weakness statement without a fallback (it reads as a
  confession, not a plan).
- Conceding scope live without a written-risk sentence.
- Not recording which questions broke you (the swap's data dies
  in the room).

## Instructor Prompts

- "Which archetype is your design weakest against, and why?"
- "What makes a fallback position 'pre-negotiated' rather than
  improvised?"
- "Who reviews your review — and why does that answer matter to
  the adversarial chain?"

## Rubric (10 pts)

| Criterion | Pts |
|---|---|
| Question bank: 10 across 5 archetypes, evidence-cited answers | 3 |
| Weakness statement: weakness + mitigation + fallback + disclosure | 2 |
| Fallback positions: cut/keep/never-cut + written-risk lines | 3 |
| Stress-test lessons fed back into own prep | 2 |

## Safety Notes

- Simulated; course-internal exercise.
