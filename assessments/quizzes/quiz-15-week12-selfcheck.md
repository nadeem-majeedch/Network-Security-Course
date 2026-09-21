---
quiz: quiz-15
week: 12
type: self-check
clos: [CLO-9, CLO-10]
lectures: [L23, L24]
marks: 10
duration: 15 min
bloom-range: Understand–Apply
status: complete
artifact-type: student-quiz
answer-key: instructor/answer-keys/quiz-15-answer-key.md
---

# Self-Check Quiz 15 — Week 12 (Vulnerability Assessment & Hardening)

> Not graded — use after L23/L24. Answers in the course answer key.

1. **(MCQ)** An unauthenticated vulnerability scan of a subnet primarily
   provides:
   A. Definitive package-level inventory · B. External-view exposure
   (services/reachable flaws) with false negatives expected ·
   C. Proof of exploitability · D. Configuration baselines

2. **(MCQ)** The correct order for a scan program is:
   A. Scan → patch → discover assets · B. Discover assets → authorize
   window → scan → prioritize → remediate → verify · C. Patch → scan →
   verify · D. Prioritize → scan → discover

3. **(MCQ)** Two CVSS-identical vulns get different priorities because:
   A. Different colors in the report · B. Environmental factors — one
   asset is internet-reachable and business-critical · C. Different
   scanners · D. Random triage

4. **(MCQ)** Server hardening's verification step must:
   A. Trust the checklist · B. Re-scan/test against the baseline and
   confirm service functionality · C. Only check the OS version ·
   D. Skip documentation

5. **(MCQ)** Which is a *compensating* control for an unpatchable legacy
   host?
   A. Ignoring it · B. Network isolation to required flows only +
   monitoring · C. Mailing the vendor · D. Deleting the asset from the
   inventory

6. **(Short)** Why does an asset inventory gap silently break a
   vulnerability program? *(2 marks)*

7. **(Diagram)** A scan-architecture diagram shows the scanner, the DMZ,
   internal servers, and a management VLAN. Mark where scan traffic must
   be *explicitly allowed* by firewalls, and the one rule pair most often
   forgotten. *(2 marks)*

8. **(Short)** Distinguish "remediation" from "mitigation" in one
   sentence each, with one example of an acceptable permanent mitigation. *(2 marks)*

**Total: 10 marks**
