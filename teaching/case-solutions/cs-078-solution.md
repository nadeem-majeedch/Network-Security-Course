---
case: cs-078
solution-for: modules/module-06-detection-vulnerability/case-studies/cs-078-vulnerability-program-metrics-review.md
difficulty: expert
module: 6
lecture-anchor: L24
clos: [CLO-10]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-078 Solution — Metrics Audit (INSTRUCTOR ONLY)

## Model Solution

**Metric-by-metric audit:**

| Metric | Honestly measures | Gaming mechanism | This program's evidence |
|---|---|---|---|
| Findings closed (+40%) | *activity* — tickets moved | mass-close Low/Info items; scan-scope changes; "fixed" = suppressed detection (cs-070's class) | plausible inflation — closure without risk trend corroboration is activity, not risk reduction |
| SLA compliance 96% | *clock discipline* — not risk | re-triage to lower severity → different clock (exhibit A); suppress-as-remediated | **gamed**: the red-team host was re-triaged twice, each reset restarting its clock — 96% was manufactured by re-classification |
| Scan coverage "100%" | *circularity* — 100% *of the known estate* | define estate as what the scanner can see (cs-074's witness problem); cloud/roaming/OT gaps vanish by definition | **most dangerous number**: the red-team host was "covered" — coverage meant *scanned once, ever*, not *visible now* |
| Avg age of open findings (−30%) | mix-shift — the *denominator* moved | closing old trivial findings drops the average without touching the risky old ones | the 11-month host sat in the tail the average ignored |
| Critical MTTR 9 days | speed on the loudest class | Critical-definitions drift; cs-076's score-shopping feeds this | probably real but irrelevant to the Medium class where the breach walked through |

**Why "100% coverage" is the most dangerous:** it's *circular* — the
estate is defined by what scanning sees, then scanning is praised for
covering it. Every blind class from cs-074 (cloud API-only, roaming,
firewalled, phantom-inverse) is excluded *by construction*, and the
metric launders that exclusion into a 100. The red team's host was
"covered" in the sense that it had been scanned *at some point*; what
mattered — *is it visible and assessed now?* — was false. Honest
coverage: **witness-union delta** — each asset class's authoritative
witness (cloud API, EDR, passive census) reconciled against scan
eligibility, reporting *unscanned-but-known* as the coverage gap number
(a non-100 number, always).

**Replacement metric set:**

| # | Metric | Definition | Gaming defense | Audience |
|---|---|---|---|---|
| 1 | **Context-weighted open-risk trend** | Σ (context risk score per open finding, cs-075 formula) by month; report the *sum*, not counts | sums resist re-triage only if scores recompute on change — pair with #2 | board/CISO |
| 2 | **Re-triage-rate monitor** | % of findings severity-changed per quarter + *clock-reset count* (any severity drop restarting SLA = flagged, aging *never* resets) | makes exhibit-A's pattern visible in the dashboard itself | audit/CISO |
| 3 | **Internet-facing age ceiling** | oldest open finding on an internet-facing host (single number, hard ceiling target: ≤30 d) | can't be averaged away; one number the board reads | board |
| 4 | **SLA compliance by matrix cell** | cs-077's cell-level view, never blended | blending hides cells; cells force the OT/internet honesty | ops + audit |
| 5 | **Fix-quality / recurrence rate** | % of "remediated" findings re-detected in 90 d | catches suppress-as-fix and partial patches | detection-eng + audit |
| 6 | **Witness-union coverage delta** | unscanned-but-known hosts per class (from cs-074's reconciliation) | replaces the circular 100% with an actionable number | security-eng |

*The metric that would have caught the red team's path:* #3 — an
internet-facing age ceiling makes "11 months open" a *headline*, not a
tail-statistic; #1 would have shown the risk never left (re-triage
doesn't remove exposure). The red team didn't beat the program; it beat
the *dashboard's blind spots* — and #2/#3 are the blind spots' repairs.

## Alternative Solutions

- **"Add more SLA bands (between Medium and Low)":** addresses the
  symptom (7.4 falling in a gap) but not the mechanism (re-triage
  gaming) — the monitor (#2) is the repair.
- **Third-party metric certification:** adds credibility optics;
  the gaming mechanisms above are *internal design choices* — no
  external audit fixes a metric built to flatter.
- **Risk-based VM platforms (EPSS/context tooling):** genuinely useful
  inputs to #1's formula; the metric *design* remains the program's
  job.

## Tradeoffs

- Metric count (6) vs dashboard clarity: 6 is the ceiling for a board
  slide — 3 headline (#1/#2/#3), 3 operational (#4/#5/#6).
- Never-resetting clocks vs legitimate re-triage: real severity
  corrections exist; the design answer is *age never resets, risk score
  recomputes* — corrections adjust priority, not history.
- Hard internet-ceiling vs messy realities (vendor-dependent fixes):
  ceiling breaches route to the exception pathway *visibly* — visible
  exceptions beat invisible aging.

## Common Mistakes

- Auditing the numbers without the gaming mechanisms (a metric is only
  auditable when its failure mode is named).
- Keeping "findings closed" as a headline (activity theatre).
- Coverage defined by the scanner (circularity preserved).
- No single-number ceiling metric (boards read one number; give them
  the honest one).

## Instructor Prompts

- "Point at the exact metric state that let 11 months pass as '96%
  compliant.'"
- "Why does age *never* reset while risk *recomputes*?"
- "Which replacement metric would the red team least enjoy?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Gaming-mechanism naming; circularity critique |
| Technical accuracy | 25% | Metric definitions with formulas |
| Alternatives considered | 20% | Symmetric-patches/platforming critiques |
| Communication | 15% | Audit table + replacement set |

**Timing:** reveal at 5:00 + 10; the re-triage exhibit is the smoking
gun to walk through.

## CLO Mapping

- **CLO-10** — Program-metric design with gaming resistance.
