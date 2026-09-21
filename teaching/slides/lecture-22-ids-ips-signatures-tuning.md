---
marp: true
theme: default
paginate: true
lecture: L22
week: 11
clos: [CLO-9]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# IDS/IPS — Signatures & Tuning

**Network Security · Lecture 22 · Week 11**

*Detection is engineering: signals, noise, and the economics between.*

<!-- notes: OPEN (2 min). Hook: "A detection you can't afford to
operate is worse than none — you trained everyone to ignore it." -->

---

## Learning Objectives

1. **Distinguish** signature vs anomaly detection by failure modes
2. **Read** IDS alert anatomy (SID, classification, threshold)
3. **Compute** alert economics: volume × minutes × TP rate
4. **Tune** with regression safety (replay before/after)
5. **Design** escalation criteria that are measurable

![bg right:34% fit](diagrams/07-ids-ips-workflow.md)

<!-- notes: (1 min) Objectives 3–5 are assignment-4's three tasks and
the Pract-4 practical. cs-070's backlog case is the economics story. -->

---

## Signature Detection: Known Patterns

- Match known byte/behavior patterns — precise, explainable
- Failure mode: **blind to novel attacks** (the zero-day gap)
- Strength: low false-positive *when scoped well*

<!-- notes: (4 min) Quiz-11 Q2's answer. The scoped-well caveat is the
lecture's hinge — unscoped signatures drown in FPs. -->

---

## Anomaly Detection: Deviations from Baseline

- Learns normal (L21's baselines) → alerts on deviation
- Finds novel behavior — at the price of **novel false positives**
- Strengths: encrypted-traffic behavior, long-game detection

<!-- notes: (4 min) The tradeoff table completes: signatures = known
evil, anomaly = unknown weird. Zeek (L23) is the behavioral platform. -->

---

## Alert Anatomy & Thresholds

```
 alert tcp $HOME_NET any -> $EXTERNAL_NET 443 \
   (msg:"beacon-suspect"; flow:established; \
    threshold:count 10, seconds 600; sid:1000001;)
```

- Thresholds/counters shape FP profiles *in the rule*
- Every rule needs: rationale, expected FP rate, tuning knobs

<!-- notes: (5 min) Read the rule aloud; map each clause to assignment
4's rule task. The "expected FP rate" requirement is the discipline
the assignment grades. -->

---

## Alert Economics (The Math Slide)

```
 daily cost = alerts/day × minutes/alert
 true burden = cost × (1 − TP rate)
```

- Class A: 900 × 4 = 3,600 min (1% TP)
- Class B: 1,400 × 2 = 2,800 min (0% TP)
- Class H: 300 × 5 = 1,500 min (0.3% TP, *broken rule*)

<!-- notes: (6 min) The exam's Section C lives here (cs-070's data).
The trust-damage argument: H's broken rule *poisons a channel*, not
just wastes minutes. Pure "biggest number first" fails the exam
question. -->

---

## Tuning with Regression Safety

1. Name the FP driver (what legit behavior triggers it?)
2. Scope narrowly (IPs, hosts, direction) — don't delete coverage
3. **Replay**: before/after on ≥30 days data; TP diff must be zero
4. Document: change record + FP profile (the CISO artifact)

<!-- notes: (6 min) Assignment-4's graded core. "Deleting rules caps at
60%" is the assignment's stated rule — the replay step is why. -->

---

## Escalation Criteria: Measurable Only

- Page: N consecutive matches + destination not allow-listed
- Queue: single match, known-good window
- "Analyst judgment" is not a criterion (quiz-11 Q6's territory)

<!-- notes: (4 min) Measurability is the rubric line. The course's
honest-metrics discipline (cs-077/cs-094) applied to detection. -->

---

## CS/DS Example: Tuning on Flow Analytics

- The beacon rule (L23's pattern) tuned on *distribution statistics*:
  interval regularity, volume bands
- FP profile: polling agents — allow-list by publisher/behavior class

<!-- notes: (3 min) DS framing: tuning is statistical hypothesis
testing on traffic — the DS skill set is the point of assignment 4. -->

---

## Activity: Rank the Backlog (6 min)

Nine tuning candidates, three sprint slots — rank with the economics
formula and defend one *counter-intuitive* skip.

<!-- notes: (6 min) cs-070's exercise compressed. The counter-
intuitive skip (usually B, the loudest) is where the economics beats
instinct. -->

---

## Case Study: cs-070 (5 min)

- The full backlog case — framework, math, and the trap

<!-- notes: (5 min) If used in the activity slot, run cs-069 (rule
design for C2) here instead — case-index rotation. -->

---

## Formative Check

- Oral: what does regression safety prove, and to whom?

<!-- notes: (2 min) Exit oral: zero lost TPs on replay — proven to the
CISO/SOC, not just yourself. -->

---

## References & Next

- Suricata/Zeek documentation (rule syntax classes)
- Diagrams: `diagrams/07-ids-ips-workflow.md`
- **Next (L23):** Zeek & anomaly detection — behavior at scale
