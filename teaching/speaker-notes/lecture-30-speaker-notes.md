---
lecture: L30
module: 8
week: 15
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L30 Speaker Notes — Advanced Forensics & Reporting

## Delivery Guide
This is the writing lecture — the capstone report (due L32) is drafted *here*,
with the exact structure it will be graded on. Attribution discipline (indicators
vs attribution), memory-forensics concepts (defensive framing), and the
executive-vs-technical audience split are the content. The peer-review round uses
the capstone rubric itself, so feedback tonight transfers directly.

## Timing Plan
0–15 triage report feedback (common gaps from L29's drafts) · 15–35 advanced
techniques overview (memory forensics concepts, encrypted-traffic inference —
defensive framing throughout) · 35–55 attribution discipline (indicators ≠
attribution; the over-claim example) · 55–65 break · 65–85 capstone report
structure walkthrough (template distributed) + drafting block · 85–110 peer review
against the rubric + revision notes · 110–120 exit ticket + defense-format brief. 
**Compression:** memory-forensics concepts to one slide; the structure walkthrough
and peer review are the graded spine.

## Teaching Demonstrations
1. Attribution over-claim: a real-shaped report that says "APT-X did this" from three IP indicators — class finds the leaps; the hedged rewrite shown.
2. Audience split: the same finding written as exec brief (impact, ask) vs analyst note (evidence, confidence) — side by side, then class rewrites one into the other.
3. Confidence calibration: three claims from L29's dataset, class assigns corroborated/single-source/inferred, disputes resolved against the rubric.

## Expected Student Difficulties
1. Report as story dump — the structure (facts → interpretation → confidence → recommendation) is a discipline, not bureaucracy; the peer review enforces it.
2. Attribution enthusiasm — indicators are fingerprints, attribution is identity; the over-claim demo shows how the leap reads to a lawyer or a journalist.
3. Writing avoidance ("we're engineers") — reframe: the report *is* the deliverable; an unreported finding protects no one.

## Discussion Facilitation
Q4 (encrypted C2 inference) stays defensive: infer from cadence/size/destination
reputation — the DS framing (classification from traffic features) is welcome;
exploitation detail is not. Q2 (exec wants a name): role-play the hedged answer —
"indicators consistent with…, attribution requires…" is a career skill.

## Lab Troubleshooting (drafting context)
- Drafts missing confidence labels: the rubric line is quoted back; revision tonight.
- Peer review too kind: require one "strongest challenge" per review — kindness is not calibration.
- Structure collapse under revision: the template's section headers are load-bearing; forbid free-form.

## Accessibility Notes
- Peer review involves reading others' drafts: large-print and screen-reader-friendly templates; extended time documented.
- The drafting block: quiet-room option for students with processing needs.

## CS & Data Science Applications
- **CS:** reports are technical documentation with an API contract — precision, versioning, and review culture transfer.
- **DS:** confidence labeling is calibrated uncertainty communication; the exec/analyst split is audience-adapted summarization — both are DS communication skills in disguise.

## Links
Plan: `modules/module-08-forensics-capstone/lectures/lecture-30-advanced-forensics-reporting.md` · Student page: `docs/lectures/lecture-30-advanced-forensics-reporting.md` · Answers: `teaching/answer-keys/answer-key-module-08.md`
