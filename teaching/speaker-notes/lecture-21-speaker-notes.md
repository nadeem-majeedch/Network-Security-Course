---
lecture: L21
module: 6
week: 11
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L21 Speaker Notes — Monitoring Foundations

## Delivery Guide
Module 6 is where the course's analysis threads converge — say so explicitly. The
telemetry-tier trade-offs are best taught by *question*: "which family answers
this?" beats any table recital. The flow-collector + baseline lab produces the
course's first written analytical artifact (the baseline paragraph) — grade it as
writing, not just numbers. Assignment 4 briefing (detection rules, due W11) closes
the session.

## Timing Plan
0–10 telemetry matching game · 10–35 flow anatomy (nfdump on the dataset) · 35–55
log pipeline design · 55–65 break · 65–85 sensor placement worksheet · 85–110
flow-collector + baseline build · 110–120 exit ticket + Assignment-4 briefing. 
**Compression:** placement worksheet to two scenarios if behind; the baseline
paragraph stays — it's the graded artifact.

## Teaching Demonstrations
1. nfdump reads: top-10 conversations → one-way SYN storms → beacon-candidate query; narrate each as a *question answered*.
2. Pipeline sketch build: sources → normalizer → SIEM hot → archive, drawn live and kept as the class reference.
3. Sampling caveat: show sampled-vs-unsampled counts on the same data (prepared) — thresholds change.

## Expected Student Difficulties
1. "Collect everything" instinct — the parsing-debt horror story plus storage math reframes it.
2. Flow-data overreach ("flows show everything") — the payload question ("what was said?") exposes the boundary.
3. Baseline-writing anxiety — provide the sentence stem: "Normal for this hour looks like … because …".

## Discussion Facilitation
Q4 (inline IPS sign-off) is an organizational question: elicit *who* owns
availability risk and *what* bypass design they'd demand — answers here predict
capstone monitoring maturity. Q5 (which alerts to a human): ask for the precision
consequence of each choice.

## Lab Troubleshooting (collector context)
- nfdump version flag drift: use the lab sheet's pinned commands.
- Flows missing: export not enabled on the range router — verify exporter config first.
- Baseline paragraphs too thin: require ≥3 quantitative anchors (top talker share, flow counts, cadence period).

## Accessibility Notes
- Terminal outputs: text files distributed; outputs read aloud with structure.
- The pipeline diagram: text-stage list version available.

## CS & Data Science Applications
- **CS:** pipelines are ETL systems — collection/normalization/storage map directly to their data-engineering coursework.
- **DS:** this is *the* DS lecture: flow records as time-series features, top-N tables, periodicity (beacon cadence), and baseline statistics — name every one; invite DS students to lead the baseline read.

## Links
Plan: `modules/module-06-detection-vulnerability/lectures/lecture-21-monitoring-foundations.md` · Student page: `docs/lectures/lecture-21-monitoring-foundations.md` · Answers: `teaching/answer-keys/answer-key-module-06.md`
