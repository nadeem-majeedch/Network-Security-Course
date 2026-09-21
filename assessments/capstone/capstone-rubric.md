---
capstone: rubric
type: grading-rubric
marks: 100
weight: 15%
status: complete
artifact-type: student-visible-rubric
instructor-band-detail: instructor/answer-keys/capstone-rubric-bands.md
---

# Capstone Grading Rubric (100 points)

> Weightings visible to students; detailed band anchors live in the
> instructor key (`instructor/answer-keys/capstone-rubric-bands.md`).

| # | Criterion | Pts | What "strong" looks like |
|---|---|---|---|
| 1 | **Architecture & design quality** | 25 | Zones by sensitivity+behavior; every control has a *verification method*; one honest deferral with accepted risk + pairing control; budget realism honored |
| 2 | **Threat model integration** | 15 | Top threats grounded in the org profile; each maps to a control that plausibly breaks its chain; no generic boilerplate |
| 3 | **Build evidence integrity** | 20 | ≥4 controls implemented with configs + before/after replay results; tested-vs-assumed labeled per control; evidence reproducible |
| 4 | **Incident exercise learning** | 15 | Decisions carry reversibility labels; design's misses identified; two owned, dated amendments |
| 5 | **Report quality** | 15 | cs-094 board paragraph structure; honest-limits section names what wasn't tested; prose is defensible (sources, confidence) |
| 6 | **Defense performance** | 10 | Weakness statement offered unprompted; evidence-chained answers; fallback positions pre-thought; no improvised concessions without written-risk framing |

## Band thresholds

| Total | Band | Descriptor |
|---|---|---|
| 85–100 | Outstanding | Defense-grade; would pass a professional design review with minor notes |
| 70–84 | Proficient | Sound design + evidence; gaps in one criterion, owned honestly |
| 55–69 | Developing | Mechanically present but thin evidence or generic threat model |
| <55 | Insufficient | Claims without verification; safety/scope violations |

## Hard rules (any violation caps the capstone at 54)

- No external scanning or unauthorized targets; course range only.
- No offensive tooling or exploit payloads in deliverables.
- No fabricated test results — every "tested" claim must have reproducible
  evidence (spot-checked by the panel).
- Instructor answer material (any `instructor/` tree file) may not appear
  in team submissions.
