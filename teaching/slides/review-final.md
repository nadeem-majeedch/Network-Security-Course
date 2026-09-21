---
marp: true
theme: default
paginate: true
review: final
covers: [L17, L32]
clos: [CLO-8, CLO-9, CLO-10, CLO-11, CLO-12, CLO-13, CLO-14, CLO-15]
duration: 90 min session (paired with self-check quiz 14)
status: complete
artifact-type: review-deck
speaker-notes: embedded
---

# Final Review — Modules 5–8 + Practical Prep

**Network Security · Week 16 · Review Session**

*Written judgment + forensic craft. Review both halves.*

<!-- notes: OPEN (2 min). Frame the final's shape: Part I written (60:
16 MCQ + 24 short + 20 applied) + Part II forensic practical (40) on
the course datasets. -->

---

## Session Overview

- Rebuild modules 5–8's core mechanisms
- Rehearse the SOC-economics and forensic tasks
- Practice the practical method end to end

## Exam Shape & Strategy

| Part | Marks | Advice |
|---|---|---|
| I-A: MCQ ×8 | 16 | 12 min |
| I-B: Short ×4 | 24 | 25 min — boundary language earns marks |
| I-C: SOC economics | 20 | 25 min — show the arithmetic |
| II: Forensic practical | 40 | 70 min — P1 hash first, always |

- The practical: hash → work on copies → timeline with sources →
  defensible report
- Confidence labels are worth real marks

<!-- notes: (4 min) P1's hash discipline is free marks — students who
skip it to "get to the analysis" lose 8. The confidence-ladder framing
comes next. -->

---

## Modules 5–6: Wireless, Cloud, Detection

- WPA3-SAE kills the offline crack; Enterprise = per-user identity
- SG stateful/instance vs NACL stateless/subnet **backstop**
- Flow logs = the cloud's telemetry (accept/reject per flow)
- Alert economics: volume × minutes × TP rate; tuning needs replay
  proof

<!-- notes: (8 min) Quizzes 4/10/11's sweep. The economics formula is
I-C's skeleton — walk cs-070's numbers once more (3,600/2,800/1,500/
240). The H-rule trust-damage argument is the exam's discriminator. -->

---

## I-C Preview: The SOC Economics Question

- Four classes, compute daily minutes, pick **two** fixes
- The trap: the largest-volume class is *not* automatically first
- Trust damage + true burden beat raw minutes
- Regression-safety proof = replay, zero lost TPs

<!-- notes: (6 min) The exact exam question's structure rehearsed.
Model: H first (trust poisoning), A second (3,600 min at ~1% TP), B
deferred with the auto-close argument. "Why not B first" is worth 6
marks. -->

---

## Module 7: The Response Disciplines

- Containment: reversible before irreversible (5-step order)
- The credential is the blast radius (svc_ops → estate-wide disable)
- Kill vs observe: state the *flip condition*
- Recovery: go/no-go board; backup generations; clean-layer order
- Board paragraph: incident, response, limits, ask

<!-- notes: (8 min) Quizzes 5/12's sweep. The five-step containment
table is quiz-5 Q6's exam form. cs-099's inject-3 line ("I won't
guess") is the comms standard. -->

---

## Module 8: Forensics & Synthesis

- Evidence: hash → copies → custody → contemporaneous notes
- Timeline entries: source + confidence; skew derived from common
  events
- "Network-attributed, host-unattributed" = the honest compound
- ZT phase gates; MTTD as the outcome metric; hunts are falsifiable

<!-- notes: (8 min) Diagrams 10 + quiz-14's sweep. The falsifiable-
hypothesis form (B4): measurable signal + data window + absence-
condition. QB-050's chain is the synthesis question shape. -->

---

## Part II Walkthrough: The Practical Method

```
 P1  hash originals, read-only copies          (8 mk — do this FIRST)
 P2  timeline: 5–8 entries, source-tagged,
     confidence-labeled                        (14 mk)
 P3  attack path: entry vector + two
     chain-breakers + one detection w/ logic   (12 mk)
 P4  report opening ≤120 w: sources,
     confidence, one unknown                   (6 mk)
```

- The seeded artifacts = Lab-13/15 patterns, *new timestamps* —
  pattern fluency, not memory

<!-- notes: (10 min) Walk the four tasks with their mark splits. P2's
rubric: corroborated needs two sources; P3's detection needs a
measurable threshold; P4's rubric: sources(2)+confidence(2)+unknown(2).
The honesty note about changed timestamps defuses "I remember this
one." -->

---

## The Three Sentences (Course Through-Lines)

1. Identity on the wire is a **claim** — build controls that prove it
2. **Reversible** before irreversible — order by the cost of being wrong
3. State the **unknown** — honesty is defensibility

<!-- notes: (4 min) L32's closing three, repeated as the exam's spirit.
Every Part II task grades one of these. -->

---

## Practice Run: Rapid Fire

- Oral round: SG vs NACL · kill-vs-observe flip · MTTD vs alerts-closed ·
  hunt falsifiability · WPA3's fix · the five containment steps

<!-- notes: (10 min) Rapid oral round, cold-call with peers correcting.
Each maps to a Part I item. Close with quiz-14 pointer. -->

---

## Logistics & Final Advice

- The practical uses the exam range: tshark/Zeek available, datasets
  provided — no personal laptops needed for Part II
- Read P2's entry requirements *before* touching the PCAP
- Sleep. Mechanisms > memorization.

<!-- notes: (3 min) Logistics honesty: the range is provided; personal
machines stay out of Part II (exam integrity + range access rules).
Point to quiz-14's key tonight. -->

---

## References

- Self-check quizzes 10–12, 14 (+ keys)
- Diagrams: 06, 07, 08, 09, 10
- Exam: `assessments/final/final-exam.md`; datasets:
  `docs/labs/datasets/`
