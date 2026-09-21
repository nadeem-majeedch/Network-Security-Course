---
quiz: quiz-11
week: 11
type: self-check
clos: [CLO-9, CLO-10, CLO-12]
lectures: [L21, L22, L23, L24]
marks: 10
duration: 15 min
bloom-range: Understand–Apply
status: complete
artifact-type: student-quiz
answer-key: instructor/answer-keys/quiz-11-answer-key.md
---

# Self-Check Quiz 11 — Week 11 (Detection, Monitoring & Vulnerability Management)

> Not graded — use after L21–L24. Answers in the course answer key.
> (Lab practical 4 is week 11 — this self-check warms up Lab-11/12.)

1. **(MCQ)** A NIDS placed inside the perimeter, before the switch SPAN
   port, sees:
   A. Encrypted + cleartext traffic per the mirror point · B. Only
   post-NAT internal traffic · C. Nothing without inline placement ·
   D. Endpoint process events

2. **(MCQ)** A signature-based IDS limitation is:
   A. Too fast · B. Blind to novel/unknown attack patterns ·
   C. Cannot read headers · D. Cannot generate alerts

3. **(MCQ)** Zeek's distinguishing value vs a plain IDS is:
   A. Blocking packets · B. Rich protocol-level logging of behavior ·
   C. Replacing firewalls · D. Encrypting telemetry

4. **(MCQ)** CVSS environmental score differs from base score by:
   A. Ignoring impact · B. Incorporating the asset's context
   (criticality, compensating controls, exposure) · C. Scoring only
   network vectors · D. Replacing patch status

5. **(MCQ)** The strongest argument for authenticated scans over
   unauthenticated ones:
   A. Faster · B. Sees the OS/package truth inside the host — fewer false
   negatives · C. Avoids credentials · D. Works through firewalls

6. **(Short)** In one sentence each: why does a *high-false-positive*
   rule cost more than analyst time? *(2 marks)*

7. **(Diagram)** A monitoring architecture diagram shows a SPAN from the
   core switch to a sensor, and a separate log shipper from firewalls to
   a SIEM. Mark which path sees packet-level evidence, and which sees
   policy decisions. *(2 marks)*

8. **(Short)** A patch SLA says "critical within 7 days." Name one
   metric proving the SLA works and one metric proving it *matters*. *(2 marks)*

**Total: 10 marks**
