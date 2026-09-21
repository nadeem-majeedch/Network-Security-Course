---
case: cs-094
title: Capstone IV — Board Risk Report (Solution)
difficulty: expert
module: 8
lecture-anchor: L31
clos: [CLO-15]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-094 — Solution: The Board Risk Report

> **INSTRUCTOR ONLY.** Model solution for cs-094.

## Model Solution

### 1. Report structure (5 sections, one-line takeaways)

| Section | Content | One-line takeaway |
|---|---|---|
| **Position** | Where we stand: controls, coverage, program status vs plan | "We can detect in days what used to take weeks." |
| **Trend** | 4-quarter metric movement (MTTD, MTTR, coverage) | "The trajectory is right and measured, not anecdotal." |
| **Incidents** | 1 contained + 2 near-misses, each with cost + lesson + closed actions | "When it happened, the system worked — 4 hours to containment." |
| **Asks** | ZT phase-3: what it buys, deferral cost | "This continues a measured program at its most efficient point." |
| **Decisions needed** | The 2 specific board decisions (fund phase-3; approve key-person mitigation) | "Two decisions today; both have plans attached." |

### 2. Metric selection (5, each bounded)

| Metric | Decides | Honest bound (stated in report) |
|---|---|---|
| MTTD (34→9 d) | Response-investment trend | Measures *detected* incidents; silent dwell is invisible — bounded by control-coverage claims |
| MTTR (19 d → 6 d) | Response maturity | Small sample (n=4); stated as trend, not rate |
| EDR coverage (60→100%) | Detection surface | Endpoint-of-one-truth: agent presence ≠ tuned detection |
| MFA coverage (100%) | Initial-access surface | Coverage ≠ phishing-resistance (phishable factors still accepted — noted) |
| ZT pilot success (98.5% + ≤7% overhead) | Program viability evidence | 2 apps ≠ estate; phase-3 asks to generalize |

**Deliberately excluded:** "alerts closed this quarter" (activity,
not outcome — undecidable); "risk score sum" (pseudo-precision);
anything without a stated collection method. The exclusion *is* the
credibility signal.

### 3. The phase-3 ask in board language

> "Phase 2 proved the model on two applications with a 98.5%
> access-success rate and under 7% performance impact — measured,
> not promised. Phase 3 extends it to branch sites and privileged
> access, where our largest remaining concentration of risk sits:
> 12 sites still depend on network location for trust, and admin
> accounts remain the highest-value target. Deferral keeps that
> concentration for another year while the threat trend (dwells
> measured in weeks, not hours) runs the other way. The program
> has hit every gate we set; this tranche continues a working
> method, not a new bet."

No fear, no tech: trend + concentration + method-proven.

### 4. The bad-news paragraph

> "Two risks remain open, both with owners and plans. First, our
> network design work (segmentation) remains unbuilt — a design
> exists, funding is requested for next FY; until built, our ZT
> program covers the highest-risk paths but not all. Second, one
> network engineer holds critical operational knowledge; we are
> mitigating through documentation, cross-training, and the
> phase-3 automation which reduces dependence — full mitigation
> lands with phase-3 delivery. We do not assess either as an
> impediment to this report's asks; both are tracked on the risk
> register with quarterly review."

Risk + owner + plan + timeline = governance. No alarm, no burial.

## Alternative Solutions

- **Appendix-heavy report:** defensible if the board's culture is
  detail-first; the 15-minute constraint argues for the 5-section
  spine with an appendix pointer.
- **Lead with the incident story:** engaging, but risks anchoring
  the board on the exception; the trend-first order makes the
  incident the *proof*, not the headline.

## Tradeoffs

- Few metrics vs richness: 5 bounded metrics inform decisions;
  20 unbounded ones inform nothing and erode trust in the 5.
- Honesty vs optics on bad news: the paragraph's plan-attached
  framing survives the audit letter's observations — burying them
  would not.

## Common Mistakes

- Metrics without bounds (a board member's first question is
  "what does that number miss?").
- Asks detached from the trend (fear-based asks get deferred to
  a security-committee cycle).
- Burying bad news in an appendix (it becomes the story when
  found).
- Reporting activity (alerts, tickets) as outcomes.

## Instructor Prompts

- "Why does MTTD earn a place but 'alerts closed' doesn't?"
- "What makes the bad-news paragraph safe to *say out loud* in the
  meeting?"
- "Which single number would a sophisticated director challenge
  first?"

## Rubric (10 pts)

| Criterion | Pts |
|---|---|
| Structure: 5 sections + retained takeaways | 2 |
| Metrics: decidability + honest bounds + one exclusion | 3 |
| Ask: trend-based, deferral cost, no fear/tech | 2 |
| Bad-news paragraph: risk + owner + plan, no alarm/burial | 3 |

## Safety Notes

- Simulated; no fiduciary advice.
