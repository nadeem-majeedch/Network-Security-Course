---
lecture: L27
module: 7
week: 14
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L27 Speaker Notes — Eradication, Recovery & Lessons Learned

## Delivery Guide
The arc closes: the incident that "ends" badly ends again. Persistence hunting
(autostart, scheduled tasks, golden-ticket concepts — conceptual, not exploit
detail) and the safe restoration order are the technical spine. The recovery-go/
no-go board is the judgment exercise. TPR brief (L28) closes the session. The
Week-14 quiz covers Modules 7 content to date.

## Timing Plan
0–15 eradication vs containment boundary (why eradication can't start blind) ·
15–40 persistence mechanisms (conceptual map + hunt evidence patterns) · 40–55
hypothesis-driven hunting (one pivot demonstrated) · 55–65 break · 65–80
restoration order + credential-hygiene decision (rotate *what first*?) · 80–100
recovery go/no-go board (two candidate states judged) · 100–110 lessons-learned
anatomy (blameless, actionable) · 110–120 exit ticket + TPR brief. 
**Compression:** the hunting pivot can be described rather than demonstrated; the
go/no-go board and restoration order are the graded spine.

## Teaching Demonstrations
1. Persistence map: autostart → scheduled task → credential theft (golden ticket, conceptual) — for each, the *evidence* it leaves and the *hunt* that finds it.
2. Restoration order demo: DNS before DHCP before AD? Class orders the list, then the canonical order revealed — the reasoning (dependency direction) is the lesson.
3. Go/no-go board live: two recovery states (one with residual beacon still unexplained, one clean) — class votes with justification; the checklist decides, not seniority.

## Expected Student Difficulties
1. "Clean scan = clean host" — persistence lives where scans don't look; the map's evidence column is the counter.
2. Restore-everything enthusiasm — dependency-ordered restoration prevents the re-compromise loop; the demo's reveal moment lands it.
3. Blameless feels soft — reframe: blameless ≠ consequence-free; it means fixing systems, not shooting messengers, because fear suppresses the reports you need.

## Discussion Facilitation
Q2 (the rebooted host that phones home again) rewards hypothesis-driven thinking:
what survived? credentials, scheduled task, or persistence on another host — make
students rank the hypotheses and name the hunt for each. Q4 (golden-ticket
concepts, defensive framing): keep it to detection (forged-ticket anomalies,
Kerberoasting indicators) and response (KRBTGT rotation) — no exploitation detail.

## Lab Troubleshooting (go/no-go context)
- Teams rubber-stamp "go": require the checklist items *named aloud*, not just checked.
- Restoration order argued from habit: force the dependency argument ("what does the next service need?").
- Lessons-learned drifts into blame: the facilitator sentence-stem card ("the process allowed…") keeps it systemic.

## Accessibility Notes
- The go/no-go board: written candidate-state cards so voting doesn't depend on rapid speech.
- Persistence map: text-outline version alongside the diagram.

## CS & Data Science Applications
- **CS:** restoration is dependency-graph traversal — topological order made operational; CS students will see their algorithms coursework in a new light.
- **DS:** lessons-learned metrics (time-to-detect per phase, hunt yield) are the feedback loop for detection models — DS students design the measurement.

## Links
Plan: `modules/module-07-incident-response/lectures/lecture-27-eradication-recovery-lessons-learned.md` · Student page: `docs/lectures/lecture-27-eradication-recovery-lessons-learned.md` · Answers: `teaching/answer-keys/answer-key-module-07.md`
