---
lecture: L28
module: 7
week: 14
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L28 Speaker Notes — SOC Operations, Maturity & Threat Intelligence

## Delivery Guide
The maturity model must stay descriptive, not aspirational marketing: maturity is
measured by *outcomes* (dwell time, coverage, time-to-tune), not slide tiers. The
TI pipeline build (sources → scoring → dissemination) and the maturity self-
assessment are the working blocks; the shift-lead rotation and the metrics wall
(dwell time, MTTD) anchor the human side. Quiz 5 today; capstone prep (L29/L30)
previews the close.

## Timing Plan
0–15 SOC anatomy (shifts, roles, escalation paths) · 15–35 maturity model
(outcome-based read) + self-assessment walkthrough · 35–55 TI lifecycle: source
scoring (reliability × recency × relevance) · 55–65 break · 65–90 TI pipeline
workshop (feed → score → package → disseminate) · 90–105 metrics wall (what we
measure, what it changes) · 105–115 Quiz 5 · 115–120 exit ticket + capstone
preview. **Compression:** shift-lead anatomy can lean on L25's roster; the TI
pipeline and self-assessment are the graded spine.

## Teaching Demonstrations
1. Feed scoring live: three sample intel items scored on the rubric — one stale, one vendor-hyped, one high-relevance; the scores drive what gets packaged.
2. Maturity self-assessment: run the instrument on the *course's own lab SOC* (built across L21–L23) — the class discovers its maturity honestly, with evidence.
3. Dissemination formats: same finding, three shapes (exec brief, analyst note, detection rule) — audience-driven writing shown side by side.

## Expected Student Difficulties
1. Maturity-tier envy ("we need to be tier 4") — outcomes-not-tiers is the correction; the self-assessment with evidence makes it concrete.
2. Intel hoarding ("collect everything") — relevance scoring and the packaging demo show that undisseminated intel is inventory, not capability.
3. Metrics as theater — the metrics wall pairs each number with the decision it changes; no decision, no metric.

## Discussion Facilitation
Q3 (CTI team of one) rewards the pipeline answer: even one analyst can score,
package, and disseminate on cadence — scale the process, not the headcount. Q5
(quantify SOC value): steer to dwell-time and coverage deltas, not ticket counts;
DS students should lead the metric-design.

## Lab Troubleshooting (pipeline context)
- Feed formats inconsistent: normalization step is the point — STIX-ish minimal schema on the board, map everything into it.
- Students skip scoring: the packaged output without scores reveals itself in review; grade the rubric's use, not the volume.
- Self-assessment inflation: require one evidence line per claimed level.

## Accessibility Notes
- Metrics wall: text table version; verbal walkthrough of each pairing.
- TI items: distributed as plain text; scoring rubric read aloud once.

## CS & Data Science Applications
- **CS:** the TI pipeline is a data product with SLAs — ingestion, scoring, publication map to their API/service design instincts.
- **DS:** the flagship metrics lecture: MTTD/dwell-time distributions, scoring rubrics as ordinal models, coverage as recall — assign DS students the metric-design section of the capstone report.

## Links
Plan: `modules/module-07-incident-response/lectures/lecture-28-soc-operations-threat-hunting.md` · Student page: `docs/lectures/lecture-28-soc-operations-threat-hunting.md` · Answers: `teaching/answer-keys/answer-key-module-07.md`
