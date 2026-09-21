---
quiz: quiz-05
type: answer-key
instructor-only: true
distribution: never-publish-to-students
clos: [CLO-11, CLO-14]
marks: 15
status: complete
---

# Answer Key — Quiz 5 (Incident Response & Forensics)

> **INSTRUCTOR ONLY.** Verified against L25–L30 teaching plans; lifecycle
> per NIST SP 800-61 phase model; notification framing principles-based
> (jurisdiction-neutral, per course safety rules).

## Section A — MCQ

| Q | Answer | Justification |
|---|---|---|
| 1 | **D** | NIST's model contains the eradication-and-recovery phase; the distractors split or rename phases. |
| 2 | **B** | Reversibility ordering = cheap-to-undo actions first; protects evidence and limits wrong-action cost. |
| 3 | **B** | Hashes prove the image is unchanged end-to-end — chain-of-custody integrity, not speed/encryption. |
| 4 | **B** | Source + confidence labeling is the corroboration discipline; single-source ≠ fact, exclusion wastes evidence. |
| 5 | **B** | MTTD is an outcome measure of detection; alerts closed/rules installed are activity measures (cs-094's decidability rule). |

**Section A total: 5**

## Section B — Short answer (model answers)

**Q6 (3 marks).** (1) **EDR network-isolate the host** — *reversible*:
stops execution spread while preserving volatile evidence. (2) **Block the
staging domain at proxy/DNS** — *reversible*: severs the observed C2/stage
channel. (3) **Suspend (not delete) the new task/service** — *reversible*
and evidence-preserving; deletion destroys artifacts. Host rebuild/restore
are the irreversible actions held until scoping completes.
*(1 per action, order + label required)*

**Q7 (3 marks).** The phrase states the evidence boundary exactly: network
telemetry (flows/PCAP) attributes the activity, but no host telemetry
covers that window (agent stopped/blind), so *who/what process* ran it is
unknown. It is stronger than a smooth claim because it (1) survives
cross-examination — every clause has a named source; (2) states the
unknown instead of hiding it, which is what reviewers and courts punish
when discovered later. *(1 meaning, 2 why-stronger)*

## Section C — Scenario

**Q8.**
(a) **Phased notification**: awareness starts the clock; notify the
incident + confirmed findings now, label the unknowns as unknowns, commit
to dated updates as forensics completes. Accuracy and timeliness are paid
on both axes rather than failing one completely. *(2)*
(b) Model lines: *"Unauthorized access to a support account has been
confirmed for two storage locations containing ticket data"* (fact) /
*"Three further locations could have been reached; forensic review is in
progress and affected individuals will be informed within [N] days if
confirmed"* (labeled unknown). *(2)*

**Total: 15**

## Grading notes

- Q6: order matters; an "isolate last" ordering caps at 1/3.
- Q8: students asserting a specific statute/regulation lose precision
  marks — the course assesses the *principle* (awareness triggers,
  phasing) per the case-study convention (cs-090); jurisdiction-neutral
  language is expected.
