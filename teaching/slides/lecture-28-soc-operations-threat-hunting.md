---
marp: true
theme: default
paginate: true
lecture: L28
week: 14
clos: [CLO-12]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# SOC Operations & Threat Hunting

**Network Security · Lecture 28 · Week 14**

*From waiting for alerts to going looking.*

<!-- notes: OPEN (2 min). Hook: "Alerts catch the loud. Hunts find the
quiet." -->

---

## Learning Objectives

1. **Describe** SOC functions: triage, detection engineering, threat
  intel
2. **Read** maturity by *outcomes* (dwell time, coverage, time-to-tune)
  — not slide tiers
3. **Design** falsifiable hunt hypotheses from your own blind spots
4. **Run** the TI pipeline: sources → scoring → dissemination
5. **Hand off** hunt outputs to the SOC without becoming unpaid alert
  engineering

<!-- notes: (1 min) Objective 3 is cs-096's case and the capstone's
hunt design; objective 5's boundary rule keeps the program honest. -->

---

## The SOC's Functions

| Function | Work | Metric |
|---|---|---|
| Triage | alert corroboration | MTTD/MTTR |
| Detection engineering | rules + FP profiles | coverage, time-to-tune |
| Threat intel | context + indicators | actionable-feed rate |
| Hunting | hypothesis-driven search | coverage documented |

- Functions ≠ tiers: maturity is *outcomes*, not org-chart paint

<!-- notes: (5 min) The outcome-metrics row is the anti-marketing
slide: dwell time, coverage, time-to-tune — cs-094's decidability rule
applies to maturity claims. Quiz-12 Q2's dwell-time definition. -->

---

## The TI Pipeline

- Sources: vendor feeds, ISACs, internal IR (your own best intel)
- Scoring: provenance, age, relevance — not all IOCs are equal
- Dissemination: detection rules + hunt tasks + blocklists (each
  downstream format differs)

<!-- notes: (5 min) cs-089's trusted-channel case shows TI *arriving*
— the pipeline's intake discipline. Quiz-12 Q8's two-checks rule (local
corroboration + provenance) is the consumer side. -->

---

## Indicator Quality: Feeds Lie By Omission

- IOCs age; CDNs share IPs; provenance varies
- The two checks before acting (L12/L26 continuity): local corroboration
  + indicator provenance/age
- False-positive IOC action = blocking your own customers

<!-- notes: (4 min) cs-096's consumer discipline. QB-033's question
reads this slide. -->

---

## Hunt: Hypothesis-Driven, Falsifiable

- Hypothesis from *your* blind spots, not generic threat lists
- Form: "if X, we would see/not see Y — in source Z, window W"
- Falsification closes the hypothesis with *documented absence*

<!-- notes: (6 min) cs-096's H1–H5 are the worked set. The near-miss
artifacts as hunting ground truth (the "would-have-been" path) is the
lecture's sharpest method point. -->

---

## No-Findings Still Ships

- Coverage documentation: technique, source, window, method, result
- Detection candidates: the queries become scheduled rules (with FP
  profiles)
- Baselines: per-role/per-identity — permanent anomaly inputs
- Telemetry-gap list: filed as engineering requests, not complaints

<!-- notes: (5 min) The empty-hunt re-arms the estate — cs-096's §3.
The boundary rule: hunters stop at validated query + FP profile; SOC
owns tuning. If SOC can't resource it, the detection doesn't ship. -->

---

## CS/DS Example: The Hunt That's Just Analytics

- Hunt hypotheses are statistical claims; the method is anomaly
  analysis on telemetry (the DS toolkit, aimed)
- cs-096's H3/H4 (role baselines, token refresh patterns) = pure
  behavioral analytics

<!-- notes: (4 min) DS framing: hunting is where their statistics meet
security — the capstone's hunt deliverable is a DS-grade analysis with
security intent. -->

---

## Activity: Write the Hypothesis (6 min)

Blind spot: 30 EDR-less legacy workstations. Write the falsifiable
hypothesis + the two data sources + the absence-condition.

<!-- notes: (6 min) cs-096's H1 template. Grading the absence-condition
("no periodicity + identity within baseline → closed") is the
falsifiability test. -->

---

## Case Study: cs-088 (5 min)

- The GPU-cluster scoping case — blind spots found the hard way

<!-- notes: (5 min) If used, run cs-096 here per rotation. The case
shows the cost of the blind spot the hunt would have mapped. -->

---

## Formative Check

- Oral: what does an empty hunt contribute? Name two outputs.

<!-- notes: (2 min) Exit oral: coverage documentation + detection
candidates (+ baselines, gap list). -->

---

## References & Next

- NIST SP 800-94 (detection context); TaHiTI-style hunt methodology
  (method reference)
- **Next (L29):** forensic fundamentals — module 8 begins
