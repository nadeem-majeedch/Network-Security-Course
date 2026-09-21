---
lecture: L26
module: 7
week: 13
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L26 Speaker Notes — Detection, Triage & Containment

## Delivery Guide
The alert-burden wall is the setup: every alert triaged today is someone's
tomorrow. Teach triage as evidence *corroboration* (three-way: IDS ↔ Zeek ↔
flow), then containment as *reversible before irreversible*. The 4-hour guided
exercise (week-10 incident dataset, four phases) is the module's centerpiece —
protect its time even if the lecture compresses. Debrief verdicts in the last 15
minutes, on the record.

## Timing Plan
0–15 triage priority model (severity × confidence × blast radius) · 15–40 evidence
triage (three-way corroboration live) · 40–55 triage documentation (fields that
survive handoff) · 55–65 break · 65–75 containment ladder + ethics brief ·
75–105 **guided exercise (compressed block: triage → scope → contain → record)** ·
105–115 debrief verdicts + one-panel walkthrough · 115–120 exit ticket. 
**Compression guidance:** cut the documentation block before the exercise; the
exercise and debrief are the graded spine. The full four-phase version runs in
L31's simulation.

## Teaching Demonstrations
1. Three-way corroboration live: one alert (C2 beacon) confirmed in IDS signature, Zeek cadence, and flow asymmetry — each view adds a fact, none alone suffices.
2. Containment ladder on a live lab slice: isolate (switch ACL) → observe; then block (egress deny) → observe; narrate the visibility cost at each step.
3. Handoff note read-aloud: a deliberately thin triage note vs a complete one — the receiving analyst's questions expose the gap.

## Expected Student Difficulties
1. Premature irreversible action ("reimage it now") — the ladder's rule (reversible first, document each step) plus the evidence-preservation consequence redirect it.
2. Alert tunnel vision — corroboration is the discipline: no containment action until two independent sources agree (lab rule).
3. Containment kills visibility — name it: the observation window shrinks with each block; sequencing choices are risk decisions, not steps in a recipe.

## Discussion Facilitation
Q3 (executive pressure on a 9 a.m. demo host) is the ethics case: the right answer
is present the risk and options with evidence — role-play it briefly with a
volunteer executive; the discomfort is instructive. Q5 (containment kills
visibility): elicit the sequencing answer before giving it.

## Lab Troubleshooting (guided-exercise context)
- Teams stuck at scope: point at the three-way method — scope = hosts/talkers sharing the beacon signature.
- Over-blocking in the exercise: the visibility-cost line on the board is the arbiter; require justification per block.
- Time overrun: the exercise has a hard clock; grade the record, not the completion — partial-but-documented beats undocumented-complete.

## Accessibility Notes
- The exercise is time-pressured: written brief, extended-clock option documented in the manual (see accessibility guidance).
- Alert consoles: text exports distributed; screen-reader-friendly field order in the handoff template.

## CS & Data Science Applications
- **CS:** containment is change management under uncertainty — rollback design and blast-radius thinking are core CS instincts.
- **DS:** alert triage is classification with precision/confidence — the priority model is a cost matrix; DS students can formalize it.

## Links
Plan: `modules/module-07-incident-response/lectures/lecture-26-detection-triage-containment.md` · Student page: `docs/lectures/lecture-26-detection-triage-containment.md` · Answers: `teaching/answer-keys/answer-key-module-07.md`
