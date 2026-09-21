---
quiz: quiz-05
week: 14
type: graded
clos: [CLO-11, CLO-14]
lectures: [L25, L26, L27, L28, L29, L30]
marks: 15
duration: 20 min
bloom-range: Apply–Evaluate
status: complete
artifact-type: student-quiz
answer-key: instructor/answer-keys/quiz-05-answer-key.md
---

# Quiz 5 — Incident Response & Forensics (Week 14, Graded)

> 20 minutes · 15 marks · CLO-11, CLO-14 · covers L25–L30.
> Answer all questions.

## Section A — Multiple Choice (5 × 1 = 5 marks)

**Q1.** The NIST incident response lifecycle phase that includes
**eradication and recovery** activities is:

A. Detection & analysis
B. Containment
C. Post-incident activity
D. Preparation, containment, eradication/recovery — per the phase model

*Bloom: Remember · CLO-11 · 1 mark*

**Q2.** "Reversible before irreversible" containment ordering exists to:

A. Speed up the incident
B. Avoid destroying evidence and avoid costly wrong actions while scope is uncertain
C. Satisfy regulators automatically
D. Bypass management approval

*Bloom: Understand · CLO-11 · 1 mark*

**Q3.** The forensic practice most directly served by recording hash values
of acquired images is:

A. Compression verification
B. Evidence integrity verification across the chain of custody
C. Faster copying
D. Encryption of evidence

*Bloom: Understand · CLO-14 · 1 mark*

**Q4.** In a multi-source timeline, a single-source event entry should be:

A. Stated as fact
B. Labeled with its source and a confidence level (e.g., "supported", not "corroborated")
C. Excluded from the report
D. Assigned to the least reliable system's clock

*Bloom: Apply · CLO-14 · 1 mark*

**Q5.** The metric that best indicates *detection capability* improvement
over quarters is:

A. Number of alerts closed
B. Mean time to detect (MTTD) for confirmed incidents
C. Number of SIEM rules installed
D. Storage used by logs

*Bloom: Analyze · CLO-11 · 1 mark*

## Section B — Short Answer (2 × 3 = 6 marks)

**Q6.** Your team suspects ransomware staging on a file server. Give the
**first three containment actions** in order, labeling each reversible or
irreversible, with one sentence on why each is in that position. *(Bloom: Apply · CLO-11 · 3 marks)*

**Q7.** A reviewer asks why your incident report says "network-attributed,
host-unattributed" for one event window. Explain what that phrase means
and why it is *stronger* than a smooth-sounding claim. *(Bloom: Evaluate · CLO-14 · 3 marks)*

## Section C — Scenario (4 marks)

**Q8.** Day 9 of an incident: two storage buckets confirmed accessed, three
more "suspect but unproven." The regulator's clock started at awareness
(day 0); forensics needs 5 more days.

(a) State the notification principle that resolves the accuracy-vs-timeliness
conflict. *(2 marks)*
(b) Draft the first two lines of the phased notice — one fact, one labeled
unknown. *(2 marks)*

*Bloom: Evaluate · CLO-11, CLO-14 · 4 marks*

**Total: 15 marks**
