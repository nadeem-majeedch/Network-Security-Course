---
lecture: L29
module: 8
week: 15
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L29 Speaker Notes — Network Forensic Fundamentals

## Delivery Guide
Forensics is where every prior skill becomes evidence work: packet analysis (L04),
flow math (L21), Zeek joins (L23), corroboration (L26). The chain-of-custody drill
opens the session because admissibility discipline changes how students *touch*
data — after this, they handle lab artifacts differently. The triage timeline
build (L26's dataset, now with custody framing) is the technical spine.

## Timing Plan
0–15 evidence categories + chain-of-custody drill (sign, bag, tag) · 15–35
volatility principle (order of collection) + acquisition modes · 35–55 timeline
triage (pivot from the spike) · 55–65 break · 65–85 corroboration worksheet (three
sources, one story) · 85–105 structured triage-report writing (the graded
artifact) · 105–115 peer review · 115–120 exit ticket + Quiz 6 preview. 
**Compression:** acquisition modes can be table-only; the timeline and report are
the graded spine.

## Teaching Demonstrations
1. Chain-of-custody drill: one evidence item moves through three hands with the form filled each time — one deliberate break introduced; the class must catch it.
2. Volatility demo: same host, RAM-first vs disk-first collection — what is lost in each order (conceptual demo with the checklist, not live imaging).
3. Timeline build: three source fragments (IDS alert, Zeek conn record, flow anomaly) placed on one axis — the story emerges from corroboration.

## Expected Student Difficulties
1. Custody as paperwork theater — the break-in-the-drill makes the cost visceral: one gap and the evidence is challengeable.
2. Timeline anchoring bias — require *source labels* on every event; confidence comes from corroboration count, not narrative smoothness.
3. "Forensics = criminal cases" — corporate scope (termination, insurance, litigation readiness) broadens motivation.

## Discussion Facilitation
Q3 (colleague's laptop) is the ethics-and-legality case: policy, ownership, and
privacy boundaries — the answer is "escalate and authorize first," and the
discussion should surface *why* the shortcut is career-ending. Q5 (volatile data
lost during approval): elicit the risk-acceptance and order-of-collection answers.

## Lab Troubleshooting (worksheet context)
- Students jump to the answer without the axis: require the timeline artifact first.
- Confidence language mushy: the rubric's three levels (corroborated / single-source / inferred) are mandatory vocabulary.
- Report too narrative: the structured template's fields (facts / interpretation / confidence) separate them mechanically.

## Accessibility Notes
- The drill involves physical movement: seated variant (artifact passing) documented.
- Timeline axis: text-table version for screen readers; color never the only confidence signal.

## CS & Data Science Applications
- **CS:** evidence handling is data provenance — immutable logs, hashes, and audit trails are systems-design topics they know.
- **DS:** timeline triage is event-correlation across heterogeneous sources with confidence weighting — a fusion problem DS students can formalize.

## Links
Plan: `modules/module-08-forensics-capstone/lectures/lecture-29-forensic-fundamentals.md` · Student page: `docs/lectures/lecture-29-forensic-fundamentals.md` · Answers: `teaching/answer-keys/answer-key-module-08.md`
