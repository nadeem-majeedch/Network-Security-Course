---
case: cs-067
solution-for: modules/module-06-detection-vulnerability/case-studies/cs-067-baseline-deviation-in-flow-data.md
difficulty: advanced
module: 6
lecture-anchor: L21
clos: [CLO-12]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-067 Solution — Baseline Deviation (INSTRUCTOR ONLY)

## Model Solution

**Adjudication table:**

| # | Most likely | Discriminating check | Confidence |
|---|---|---|---|
| D1 (new tuple .55→PLC) | **Legitimate change** — the QA workstation (.55) installed Tue, ticketed | Match .55's MAC/hostname to the Tue install ticket + DHCP inventory; if identity matches the ticketed QA box → auto-clear | **High** once identity confirms |
| D2 (poll 5 s → 4.7 s, 3 d) | **The attack** — a replaced/misconfigured (or compromised) PLC-class device altering the poll cadence; sustained 3 days with no ticket | Out-of-band: compare PLC asset inventory + firmware serials against historian's device registry; check *which* PLC-side device answers — a swapped unit has a different MAC/serial; config-diff the controller's scan rate (nobody ticketed a change) | **Medium→High** — the sustained-without-ticket pattern is the tell |
| D3 (3× volume, 40 min, 02:00 Wed) | **Legitimate change** — the scheduled patching window (firmware tooling bursts volume) | Match against the change calendar (window was scheduled, undisclosed to you but real); tooling's traffic signature (burst-then-stop) | **High** once calendar confirms |

**Why D2 and not D1/D3:** D1 is a *new-but-explainable* actor (identity
resolvable to a ticket); D3 is a *bounded burst* matching a known tool's
signature during a known window; D2 is a **persistent behavioral change
in a fixed-pair relationship with no change record** — in OT, poll
cadence is a *config property* of engineered systems, and unexplained
persistence is exactly what a swapped/compromised device produces
(either by its own misconfiguration or to groom quieter collection).
The attack-shaped-as-maintenance is the case's point: D3 *looks* like
the attack (volume!) and D2 *is* (periodicity, quiet, sustained).

**Why baselines lie — three failure modes:**

| Failure mode | Mechanism | Exercised by |
|---|---|---|
| **Drift** | the world changed slowly; the 30-day window mixes old and new reality → σ widens, alerts blur | D2 partially (if cadence crept) |
| **Unannounced change** | legitimate change with no feed into the baseline → deviation fires on *normal* | D1, D3 (both had real-world causes, no change-feed) |
| **Attacker-shaped-as-change** | adversary stages activity to mimic maintenance/upgrade patterns → baseline can't distinguish intent | D2's scenario class |

**Baseline-hygiene loop:**

1. **Change-feed integration:** ticketing system → baseline tool API:
   approved changes register actor-identity + window; the *tool* then
   either suppresses alerts for registered tuples or tags them
   "change-correlated" for the analyst. The one check that would have
   **auto-cleared D1:** tuple-actor matching — new tuple + matching
   change ticket = cleared-with-note (this is the loop's highest-value
   single feature).
2. **Shadow period:** any registered change puts its tuples in
   *monitor-not-alert* for 7 days — the baseline learns the new normal
   before enforcing it; deviations *within* the shadow period still log
   (pattern evidence) but don't page.
3. **OT-specific check (the D2 killer):** device-identity correlation —
   flow tuple + MAC/serial registry diff; a poll-cadence change with an
   unchanged device serial is config-drift (benign-ish); cadence change
   *with* a new serial is a replacement event requiring a ticket that
   doesn't exist → escalate as the attack case. Auto-enrich every OT
   deviation with asset identity before paging.

## Alternative Solutions

- **D3 as the attack:** volume-first intuition; rejected — 02:00
  maintenance windows and burst-signatures are the *costliest* false
  positives in OT (wake a plant at 02:00 for a patch job and the
  monitoring program loses its allies). The case rewards resisting
  volume-theatre.
- **D1 as the attack (new tuple = new device):** plausible if the QA
  install ticket didn't exist — the identity check *decides*; the
  answer's quality is in naming the check, not guessing the verdict.
- **Tune the baseline thresholds until quiet:** destroys the system's
  only honest signal (D2's class); hygiene loop > knob-turning.

## Tradeoffs

- Shadow-period length (7 d) vs detection latency for attacker-shaped
  changes: shadow applies to *registered* changes only — attacker
  activity isn't registered, so it pages immediately; the trade is
  benign-change noise vs attack latency, and the feed breaks the tie.
- OT out-of-band checks (asset registry diffs) cost OT-team cooperation:
  budget the relationship, not just the tooling.
- 3σ vs fixed thresholds: σ adapts to drift but widens with attacks
  (slow-boil evasion) — keep fixed floors on *fixed-pair* OT relations
  where the physics is constant.

## Common Mistakes

- Volume-first adjudication (D3 panic).
- Verdicts without naming the discriminating check (guesses, not
  adjudication).
- Missing that D1's ticket *exists* (the evidence was in the premise).
- Baseline tuning as the fix (silences D2's class).

## Instructor Prompts

- "Which deviation would you page the plant at 02:00 for — and what does
  that answer cost you either way?"
- "What single integration removes half these alerts permanently?"
- "Why is 'sustained without ticket' more damning than 'big'?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Identity/config/process discriminators per deviation |
| Technical accuracy | 25% | Baseline mechanics, OT poll semantics |
| Alternatives considered | 20% | Volume-first and threshold-tuning rejections |
| Communication | 15% | Adjudication table + hygiene loop |

**Timing:** reveal at 5:00 + 10; "sustained without ticket" is the
sentence to land.

## CLO Mapping

- **CLO-12** — Baseline analytics and deviation adjudication.
