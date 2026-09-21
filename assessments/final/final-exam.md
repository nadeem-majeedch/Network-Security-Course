---
exam: final
week: 16
type: exam
clos: [CLO-8, CLO-9, CLO-10, CLO-11, CLO-12, CLO-13, CLO-14, CLO-15]
lectures: [L17, L32]
marks: 100
duration: 150 min
status: complete
artifact-type: student-exam
answer-key: instructor/answer-keys/final-answer-key.md
---

# Final Examination — Network Security (Week 16)

> **Duration:** 150 minutes · **Total:** 100 marks · **Coverage:** L17–L32
> (Modules 5–8) with integration across the full course.
> **Structure:** Part I written (60 marks) + Part II embedded forensic
> practical (40 marks). The practical uses the course dataset
> (`docs/labs/datasets/` — authorized, simulated evidence only).

## Part I — Written (60 marks)

### Section A — Multiple Choice (8 × 2 = 16 marks)

**A1.** WPA2-PSK's core weakness vs WPA3-Personal:
A. Weak ciphers · B. Offline-verifiable handshake enables dictionary attacks ·
C. Short range · D. No encryption

**A2.** A cloud security group differs from a network ACL by being:
A. Stateless · B. Stateful and instance-attached · C. Subnet-wide ·
D. IAM-based

**A3.** Zeek's primary value in monitoring:
A. Packet blocking · B. Rich protocol-level behavioral logging ·
C. NAT · D. Encryption

**A4.** CVSS environmental scoring exists because base scores ignore:
A. Dates · B. Asset context (exposure, criticality, compensations) ·
C. Vendors · D. Protocols

**A5.** The containment principle "reversible before irreversible" protects:
A. Bandwidth · B. Evidence and against costly wrong actions ·
C. Reputations · D. Licenses

**A6.** "Network-attributed, host-unattributed" in a timeline means:
A. The host confessed · B. Network telemetry shows it; host telemetry for
the window is absent · C. Logs were deleted · D. The network is guilty

**A7.** In a board report, MTTD beats "rules installed" because it is:
A. Simpler · B. An outcome metric of detection capability ·
C. Cheaper · D. Vendor-reported

**A8.** Zero-trust phase gates primarily:
A. Delay procurement · B. Convert each tranche into measured evidence
before the next · C. Replace pilots · D. Avoid reporting

### Section B — Short Answer (4 × 6 = 24 marks)

**B1.** Your VPC flow logs show an app instance sending 200 MB/day to one
external IP for 9 days. Give the attribution-first verification (two
checks) and the containment that doesn't touch the instance. *(Bloom: Analyze · CLO-13 · 6)*

**B2.** A scanning program finds 4,600 findings. Explain the three
prioritization inputs beyond CVSS base score that make remediation
orderable. *(Bloom: Evaluate · CLO-10 · 6)*

**B3.** Distinguish **eradication** from **recovery** in IR, and state the
go/no-go criterion that most often gates a file-server restore. *(Bloom: Understand · CLO-11 · 6)*

**B4.** A threat-hunt hypothesis must be *falsifiable*. Restate this weak
hypothesis properly: "look for weird beaconing." *(Bloom: Apply · CLO-12 · 6)*

### Section C — Applied Scenario (20 marks)

**C1.** A 6-analyst SOC faces: (i) alert class A — 900/day, 4 min each,
~1% TP; (ii) class B — 1,400/day, 2 min, ~0% TP (policy violations);
(iii) class H — 300/day, 5 min, ~0.3% TP, *broken correlation rule*;
(iv) class G — 8/day, 30 min, ~60% TP (data-staging heuristic).
Compute the daily analyst-minutes per class; then argue, with numbers,
which **two** to fix first — and why the *largest-volume* class is not
automatically first. State the regression-safety proof for your changes.
*(Bloom: Evaluate · CLO-9 · 20)*

## Part II — Forensic Practical (40 marks)

> Uses `docs/labs/datasets/incident-week-pcap.pcap` and
> `incident-week-logs/` (the Lab-13/15 evidence). Tshark/Zeek available
> on the exam range. All analysis on the provided simulated evidence.

**P1. Evidence handling (8 marks).** You receive the PCAP and log bundle.
State the two integrity steps you perform *before* analysis, with the
commands. *(Bloom: Apply · CLO-14 · 8)*

**P2. Timeline reconstruction (14 marks).** From the dataset, produce a
timeline (5–8 entries) of the incident: initial access, credential use,
staging, exfiltration attempt. Tag each entry with its source (PCAP/log)
and a confidence level (corroborated/supported). *(Bloom: Analyze · CLO-14 · 14)*

**P3. Attack-path synthesis (12 marks).** From your timeline: name the
initial-access vector, the two controls that would have broken the chain
earliest (one technical, one process), and the single detection you would
write first — with its logic. *(Bloom: Evaluate · CLO-15 · 12)*

**P4. Reporting (6 marks).** Draft the incident report's opening paragraph
(≤120 words) in defensible form: facts with sources, confidence labels,
one explicit unknown. *(Bloom: Create · CLO-14 · 6)*

**Total: 100 marks**
