---
case: cs-070
solution-for: modules/module-06-detection-vulnerability/case-studies/cs-070-alert-tuning-backlog-prioritization.md
difficulty: advanced
module: 6
lecture-anchor: L22
clos: [CLO-9]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-070 Solution — Tuning Backlog (INSTRUCTOR ONLY)

## Model Solution

**Value framework:**

```
Score = (analyst-minutes reclaimed/day) × (0%-TP confidence)
        + (trust-restoration factor) + (true-positive-latency reduction)
Regression gate: no change ships without a 30-day replay diff showing
                 zero suppressed true positives (or a signed acceptance).
```

Apply (daily-minutes reclaimed per candidate):

| Cand | Class | Minutes/day reclaimed | Extra factors | Score (ordered) |
|---|---|---|---|---|
| (6) fix H's lookup | H | 300×5 = **1,500** | *trust restoration*: H currently trains analysts to dismiss a class designed for high-value correlation — fixing returns a functioning signal to the pool | **1** |
| (1) auto-close B + digest | B | 1,400×2 = **2,800** | ~0% TP → near-zero risk; but zero trust/latency value (pure plumbing) | **2** (by raw minutes — the *math* puts it here; the trap is treating math-#1 as sprint-#1) |
| (4) enrich D w/ HR geo | D | ~60% of 40×15 = **360** | *TP-latency*: 8% TP class gets cleaner — fewer false pages of the *real* travelers | **3** |
| (3) suppress C by source | C | 700×3 = **2,100** | ~0% TP; risk ≈ 0 *if* source-scoping is exact (scanner IP + scan-window); scored below B only on execution-risk (a mis-scoped suppress hides a real scan-shaped attack) | **4** |
| (2) baseline A by host-class | A | ~50% of 900×4 = **1,800** | real but multi-sprint; partial credit per class | 5 |
| (9) kill legacy dup of A | A | overlaps (2) | counts *with* (2), not alone | 6 |
| (8) F playbook | F | 60×10×~50% = **300** | F has 35% TP — automation risk on *true* positives; playbook only w/ replay proof | 7 |
| (5) E thresholds | E | 25×20×~40% = **200** | E is new — baseline first (this *is* candidate 5's work); keep | 8 |
| (7) raise G threshold | G | negative value | G is 60% TP at 8/day — *raising* its threshold trades your best signal for minutes; **reject** | — |

**The sprint-3 pick: (6), (4), (3).** Reasoning: raw minutes favor
(1)(3)(6); the *framework* elevates (6) (trust restoration — 1,500
minutes AND a working high-value class), keeps (3) (2,100 minutes,
near-zero risk, one precise suppress), and takes (4) (360 minutes but
the only candidate that *improves a TP-bearing class's latency*). (1)
auto-close is scheduled next sprint with the same replay gate — the math
already justified it; the sprint fits what regression-testing can cover
in two weeks.

**The biggest-volume trap:** B (1,400/day) *is* mathematically the top
minutes-reclaim (2,800) — the trap is assuming that makes it the
obvious sprint-#1. It doesn't, for two reasons: (a) auto-closing a
policy class is operationally trivial (a filter + digest) that doesn't
need *this* sprint's engineering attention, while (6) un-breaks a
detection the SOC *needs* working; (b) risk asymmetry — B's 0% TP makes
it safe *whenever executed*, while (6) and (4) compound (a working H
class and clean D pages improve every *future* day). When *would* B be
#1? When analyst attrition/burnout is the binding constraint (minutes
beat signal quality), or when B's volume breaks SLAs *today* —
frameworks encode the situation, not just the arithmetic.

**Regression-safety rule (CISO artifact):** every tuning change ships
with a **30-day historical replay diff**: replay the *pre-change*
detection logic and the post-change logic over the last 30 days of
telemetry; the diff lists every alert the change would suppress, and
each suppressed alert is dispositioned (TP/FP/benign). **Zero
undispositioned suppressions and zero true positives suppressed** (or a
signed risk acceptance per exception) is the merge gate. The artifact
converts "don't tune away detection" from a slogan into a test.

## Alternative Solutions

- **(1)(3)(6) by raw minutes:** defensible pure-math pick; loses (4)'s
  latency value — acceptable if stated.
- **(2) first (biggest *security* class):** A's 900/day matters, but
  host-class baselining is a multi-sprint build; sprint-#1 on it
  delivers partial value late — sequencing failure.
- **Reject (7) silently:** the better move is *documenting* the
  rejection — G's threshold stays because its TP-rate is the pool's
  best; the CISO artifact includes the no-change rationale.

## Tradeoffs

- Sprint capacity vs replay-gate throughput: the gate costs a day per
  change — it *is* why only 3 fit; don't bypass it to fit 5.
- Trust-restoration weighting: soft-factor scoring invites gamed
  numbers — anchor it (H's class history: what % of its *intended*
  signals were dismissed unread?).
- Auto-close digests still need a human skim: B's weekly digest is 10
  minutes — the class is contained, not deleted.

## Common Mistakes

- Ranking by alert volume alone (B-first without the trust/latency
  factors).
- Suppressing C broadly (mis-scoped suppress = hidden real scans — the
  regression gate exists for exactly this).
- Touching G (the best class) for minutes.
- No replay artifact (the CISO fear stays rational).

## Instructor Prompts

- "Show the formula where B wins sprint-#1 — what changed in the
  situation?"
- "What does the replay diff for candidate (3) look like — name one
  suppressed alert that would make you re-scope it."
- "Why is *rejecting* candidate (7) part of the deliverable?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Multi-factor formula; trap reasoning explicit |
| Technical accuracy | 25% | TP/minutes math correct |
| Alternatives considered | 20% | Alternate sprint picks with conditions |
| Communication | 15% | Ranked table + regression artifact |

**Timing:** reveal at 5:00 + 10; the B-trap discussion is the debrief's
center.

## CLO Mapping

- **CLO-9** — Alert-tuning economics and regression discipline.
