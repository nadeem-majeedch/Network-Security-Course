---
lecture: L25
module: 7
week: 13
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L25 Speaker Notes — Incident Response Lifecycle & Preparation

## Delivery Guide
This module shifts the register: less protocol, more process and judgment. The
design-thinking clinic is the engine — students *build* runbook preconditions from
failure modes, not memorize phases. The contact-sheet drill is deliberately
uncomfortable: at 2 a.m. the org chart is irrelevant, the roster is everything.
End by framing the two-week capstone arc (L31 workshop → L32 defense) so Module 8
planning starts tonight.

## Timing Plan
0–10 incident framing (definitions matter: event → incident) · 10–35 lifecycle +
ICS/SCADA variant · 35–55 design-thinking clinic (failure-mode → precondition) ·
55–65 break · 65–75 contact-sheet drill + severity calibration · 75–110 runbook
lab (ransomware & DDoS branches) · 110–120 exit ticket + capstone-arc briefing. 
**Compression:** the drill can shrink to one scenario; the runbook lab is the
graded spine and never gets cut.

## Teaching Demonstrations
1. Severity calibration: three incident descriptions, class assigns P1–P4, disagreements surfaced and resolved *on record* (the rubric is the artifact).
2. Runbook precondition checklist build: one failure mode (e.g., "no out-of-band comms") → its precondition ("roster with personal contacts, tested quarterly") — do two live, students do the rest.
3. ICS contrast: IT incident (restore fast) vs OT incident (safety first) — the two response orders side by side.

## Expected Student Difficulties
1. "The plan is the document" — correct gently: the plan is the *capability*; the document is one artifact. The clinic exists to prove it.
2. Role confusion in drills (everyone wants to be incident commander) — assign roles in the lab and rotate; the roster is the fix, said aloud.
3. Scope anxiety on ICS — keep it conceptual: safety-first ordering and one-way data flow vocabulary; no OT exploits.

## Discussion Facilitation
Q3 (comms compromise during IR) rewards the out-of-band answer — push to concrete
(roster contacts, alternate channel, pre-agreed code phrase). Q5 (no-notice
exercise): expect resistance ("unfair!") — that's the pedagogical point; real
incidents are unscheduled.

## Lab Troubleshooting (runbook context)
- Teams freeze on blank runbooks: seed each with the preconditions list from the clinic.
- Severity inflation (everything P1): apply the rubric aloud, per scenario; the calibration demo pays off here.
- ICS runbook drifts into IT-isms: check the response *order* (safety → containment → restoration), not the wording.

## Accessibility Notes
- Drills are spoken/rapid: provide written scenario cards so no student depends only on real-time speech.
- Severity rubric: high-contrast one-pager; read criteria aloud before the drill.

## CS & Data Science Applications
- **CS:** runbooks are state machines with human transitions — design, idempotency, and rollback instincts transfer directly.
- **DS:** severity calibration is rubric-based labeling; incident metrics (MTTD/MTTR) are the datasets Module 7 builds on — DS students own the metric definitions.

## Links
Plan: `modules/module-07-incident-response/lectures/lecture-25-ir-lifecycle-preparation.md` · Student page: `docs/lectures/lecture-25-ir-lifecycle-preparation.md` · Answers: `teaching/answer-keys/answer-key-module-07.md`
