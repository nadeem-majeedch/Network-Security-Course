---
case: cs-075
solution-for: modules/module-06-detection-vulnerability/case-studies/cs-075-scan-result-prioritization-under-patch-windows.md
difficulty: advanced
module: 6
lecture-anchor: L24
clos: [CLO-10]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-075 Solution — Prioritization Under Patch Windows (INSTRUCTOR ONLY)

## Model Solution

**Formula and multipliers (defined, then applied):**

```
Risk = S × E × X × (1 − C)
  S: CVSS-normalized severity        = CVSS/10
  E: exposure multiplier             = internet 3.0 | user-facing 1.5 | internal 1.0 | isolated 0.2
  X: exploitation multiplier         = wild-exploit 3.0 | no-known-exploit 1.0
  C: compensating-control discount   = verified control 0.6 | partial 0.25 | none 0
     ("verified" = tested ACL/EDR-block evidence, not diagram)
```

| ID | Math | Risk | Rank |
|---|---|---|---|
| **F2** | 0.75 × 3.0 × 3.0 × 1 = **6.75** | internet + active campaign + no control | **1** |
| **F5** | 0.98 × 1.0 × 1.0 × 1 = **0.98** | internal but crown-jewel-adjacent (signing keys, no control) | **3** |
| **F3** | 0.88 × 1.5 × 1.0 × 0.4 = **0.53** | EDR block *tested* → verified discount | **4** |
| **F1** | 1.0 × 0.2 × 1.0 × 0.4 = **0.08** | the 10.0: isolated *and* verified-ACL discount | **5** |
| **F4-class (per host)** | 0.53 × 1.5 × 1.0 × 1 = **0.80** | user-facing info-disclosure, no control | **2** as a *population* |

**The window cut (60 hosts):**

- **F2** (1 host, 2 h) — mandatory.
- **F5** (1 host, 2 h) — internal rank-3 with key custody.
- **F4-class population:** ~90 user-facing hosts carry it; formula
  threshold: patch the **58 highest-traffic user-facing** (reachability
  tiebreak: hosts with inbound-from-internet proxy paths first), effort
  30 min each → 29 h fits the 4-h window? **No** — recompute: the
  window is 4 h *calendar*; with 4 parallel operators ≈ 16 host-hours →
  58 hosts × 0.5 h = 29 host-hours exceeds it. **Cut to F4-class
  internet-path hosts only (the 12-user-facing hosts with proxy
  exposure):** 12 × 0.5 = 6 host-hours — fits with F2+F5 (4 h) at 10
  host-hours across the window. The remaining F4-class hosts → next
  window; the *threshold is now evidenced*: "internet-reachable
  first-tier only; rest queued with dates."
- **F3** (fleet, 3 h, risk 0.53 with tested control) — *deferred by
  design*: the verified EDR discount carries it to the next standard
  maintenance cycle; fleet rollouts don't belong in emergency windows.

**The CISO answer for F1 (the discipline test):**

> "CVSS 10.0 measures *severity assuming full reachability* — F1's
> host is on a backup-only network with a *tested* ACL (we re-verified
> segmentation last quarter, not just read the diagram), and no
> in-the-wild exploitation exists for it. Context-weighted risk: 0.08 —
> two orders below F2's 6.75, which is under active attack right now
> with no compensating control. Patching the 10.0 first would spend the
> window's scarcest resource on the least-reachable host. **Promotion
> trigger:** the moment any of three things changes — ACL drift alert,
> the backup network gains a route to user space, or the CVE gains a
> worm-class exploit — F1 jumps to the top of the next window
> automatically; the promotion rule is pre-written, so the decision
> makes itself."

## Alternative Solutions

- **CVSS-descending (F1 first):** the classic failure the case exists
  to break; defensible only as "budget-blind policy" — and the window
  budget makes it self-refuting.
- **Exploitation-first only (F2, then wild-exploit list):** close to
  right; misses F5's *asset criticality* (signing keys) which no
  exploitation multiplier captures — criticality deserves its own term
  (or a host-class multiplier); naming that improves the formula.
- **Compensating-control trust without evidence:** the discount is only
  honest when *tested* (EDR-block tested; ACL re-verified) — unverified
  controls get 0 discount, or the math launders hope.

## Tradeoffs

- Multiplier calibration vs simplicity: the 3.0/1.5/0.2 exposure set is
  defensible-by-argument, not universal truth — document the rationale,
  revisit annually (calibration is governance, not math).
- Fleet-deferral of F3: standard-cycle risk vs window discipline — the
  tested EDR control is what makes deferral defensible; without it, F3
  would force a fleet emergency.
- Parallel operators vs change-freeze quality: 4 parallel patchers
  raise regression risk — pre-staged rollback per host is the price.

## Common Mistakes

- CVSS-only ranking (the F1 trap).
- Unverified control discounts (hope-as-control).
- Ignoring the calendar-vs-host-hours arithmetic (the 58-host cut
  fails on hours, not on host count).
- No promotion trigger for deferred findings (deferral without a
  tripwire is just forgetting).

## Instructor Prompts

- "Recompute F1 if the ACL alert fires tomorrow — show the promotion."
- "Where would you add an asset-criticality term, and what multiplier?"
- "Why does *tested* earn the 0.6 but *documented* doesn't?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Context-multiplier logic; evidenced discounts |
| Technical accuracy | 25% | Formula arithmetic; window-hours math |
| Alternatives considered | 20% | CVSS-first/exploitation-first critiques |
| Communication | 15% | CISO answer + promotion trigger |

**Timing:** reveal at 5:00 + 10; the F1 answer is the case's
discipline payoff.

## CLO Mapping

- **CLO-10** — Context-weighted vulnerability prioritization.
