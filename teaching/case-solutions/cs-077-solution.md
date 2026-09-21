---
case: cs-077
solution-for: modules/module-06-detection-vulnerability/case-studies/cs-077-remediation-sla-design-by-asset-criticality.md
difficulty: expert
module: 6
lecture-anchor: L24
clos: [CLO-10]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-077 Solution — Remediation SLA Design (INSTRUCTOR ONLY)

## Model Solution

**Flat-SLA failure modes:**

| # | Failure | Concrete conflict |
|---|---|---|
| 1 | **OT: too strict to be honest** | "Critical=7 days" on a running PLC line means a *line shutdown* mid-quarter — ops will either falsify or freeze scanning; the SLA breeds dishonesty, not security |
| 2 | **Internet-facing Medium: too lax** | a Medium-severity auth-bypass on the public API sits 180 days while the board's SLA chart looks green — the *actual* crown-jewel exposure waits longest (the cs-075 inversion at SLA scale) |
| 3 | **Capacity-unbacked math** | Criticals at 7 days across 3,100 findings/quarter would need ~50 patches/day — no fleet tooling, no window supports it; day 8 renders the SLA a fiction the dashboard still displays |
| 4 | **Legacy-frozen devices: no pathway** | the medical-like embedded fleet *cannot* patch — the flat SLA makes every finding on it a permanent violation, so exceptions multiply informally until the SLA means nothing |
| 5 | **No exploitation/exposure weighting** | a Critical with active wild-exploit on the internet edge and a Critical on an isolated backup host share one clock — the context cs-075 taught has no seat in the design |

**Two-dimensional SLA matrix (criticality × severity, days):**

| Criticality ↓ / Severity → | Critical | High | Medium | Low |
|---|---|---|---|---|
| **Internet-facing revenue** | **3** (+ wild-exploit: 24 h) | 14 | 60 | 120 |
| **Revenue-adjacent (POS)** | 7 | 30 | 90 | 180 |
| **Productivity (laptops/servers)** | 14 | 30 | 90 | 180 |
| **Safety (OT)** | **C-CTL pathway**¹ | C-CTL pathway¹ | 180 | next maintenance |
| **Isolated/backups** | 90 | 180 | 365 | best-effort |

¹ **OT compensating-control SLA:** patch at the plant's scheduled
maintenance windows (quarterly), *but* within 7 days deploy verified
compensating controls (segmentation check, IPS rule, physical access
note) — the SLA commits to *risk reduction*, not patch-rotation; the
control must be **tested** to stop the clock (cs-075/076 standard).
Legacy-frozen devices: same pathway, with replacement-date funding as
the exit condition (cs-056's dated-acceptance pattern).

**Promotion/trigger rules:** wild-exploit cataloging, exposure change
(host moves tiers), exploit-code release, or control-failure alert →
finding auto-promotes one row *and* one severity band; deferrals
always carry tripwires.

**Program metrics (with gaming warnings):**

| Metric | Measures | Gaming pattern to watch |
|---|---|---|
| 1. Compliance rate **by matrix cell** (not overall) | where the SLA actually holds | overall average hides the OT cell; cell-level forces honesty |
| 2. Exception rate + **aging** | the pathway's real load | exception-everything (if >15% of a cell is exceptions, the cell's SLA is wrong — recalibrate, don't moralize) |
| 3. MTTR by criticality class | throughput where it matters | closing trivial findings fast to mask slow criticals — cut MTTR *per class*, never blended |
| 4. **Context-weighted open-risk trend** (sum of cs-075 risk scores open, by month) | the number the board should watch | "closed count" as the headline (closing Low-risk items while Criticals age) — trend *risk*, not tickets |
| 5. SLA-breach **recurrence** (same finding re-opened) | fix quality | permanent-suppress-as-fixed — recurrence >5% means regression testing is failing |

**The face-saving line for the CISO:** the matrix *keeps* the board's
promises where they're real (internet-facing Criticals: 3 days is
*tighter* than the flat 7) and replaces the impossible promises with
committed pathways — "we tightened the SLAs that protect revenue and
made the safety SLAs honest; the board chart now moves by cell, not
average."

## Alternative Solutions

- **Keep flat SLA + private exception ledger:** the quiet corruption
  path — exceptions without governance become the real policy; the
  matrix *is* the governed exception system.
- **Exploitation-driven-only (no SLA bands):** maximally adaptive,
  unboardable — the board needs commitments; the matrix encodes
  judgment into commitments.
- **Asset-criticality-only (ignore severity):** inverts the error;
  both axes exist because both vary.

## Tradeoffs

- Matrix granularity (5×4 cells) vs explainability: 20 cells is the
  explainability ceiling — beyond that, the board chart and the ops
  team both lose the plot.
- Compensating-control clock-stopping vs control theater: *tested*
  controls stop clocks; documented-only controls don't — enforcement
  cost is real and worth it.
- Tight internet-facing SLAs vs change-freeze quality: 3-day SLAs need
  pre-staged rollbacks (cs-075's price of speed).

## Common Mistakes

- Designing SLAs without capacity math (failure mode 3 — the most
  common real-world variant).
- OT exclusion instead of OT pathway (ignored ≠ managed).
- Blended MTTR reporting (the gaming pattern).
- No promotion triggers (static SLAs meet dynamic threats).

## Instructor Prompts

- "Show the arithmetic that breaks the 7-day Critical SLA — how many
  patches/day does it demand?"
- "What exactly stops the OT clock — and who verifies it?"
- "Which metric would you take to the board, and why is its gaming
  pattern the one you designed against?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Both-axes logic; capacity-backed design |
| Technical accuracy | 25% | Matrix + pathway mechanics |
| Alternatives considered | 20% | Flat/exception-ledger critiques |
| Communication | 15% | Matrix table + CISO line |

**Timing:** reveal at 5:00 + 10; the capacity arithmetic is the
reality-check anchor.

## CLO Mapping

- **CLO-10** — Remediation-program design with SLA engineering.
