---
marp: true
theme: default
paginate: true
review: midterm
covers: [L01, L16]
clos: [CLO-1, CLO-2, CLO-3, CLO-4, CLO-5, CLO-6, CLO-7]
duration: 90 min session (paired with self-check quiz 13)
status: complete
artifact-type: review-deck
speaker-notes: embedded
---

# Midterm Review — Modules 1–4

**Network Security · Week 8 · Review Session**

*The exam rewards mechanism + judgment. Review both.*

<!-- notes: OPEN (2 min). Frame: the midterm's shape — 10 MCQ, 4 short,
2 applied, 1 scenario-choice. This session walks the *mechanisms* and
the *judgment patterns* the questions test. -->

---

## Session Overview

- Rebuild the four modules' mechanism chains
- Rehearse the exam's judgment patterns
- Practice one composite scenario

## Exam Shape & Strategy

| Section | Marks | Time advice |
|---|---|---|
| A: MCQ ×10 | 20 | 15 min — answer all, flag doubts |
| B: Short ×4 | 30 | 30 min — one sentence per mark |
| C: Applied ×2 | 30 | 40 min — show work, state order logic |
| D: Scenario ×1 | 20 | 25 min — structure first, prose second |

- Blank work earns nothing: partial mechanisms = partial marks
- State assumptions where the question is open

<!-- notes: (3 min) Time budget is the strategy. "One sentence per
mark" anchors B's depth expectations. C's rubric rewards order logic
over syntax. -->

---

## Module 1: The Wire's Claims

- Encapsulation: segment → packet → frame
- **Identity on the wire = claim** (MAC, ARP, IP all spoofable)
- ARP trusts whoever shouts first; TTL kills loops
- ICMP: diagnostics that leak inventory

<!-- notes: (6 min) Quiz 1's territory. The spoofability ledger (L02)
is the unifying table — walk it once more. MCQs A1–A3 come from here. -->

---

## Module 1 in Exam Form

- B1: threat vs vulnerability vs risk — one asset, three terms
- C2-preview: read an ARP anomaly + a DNS anomaly + a flood in one
  capture
- Practice: self-check quiz 13, questions 1–3

<!-- notes: (4 min) Map each exam item to its source lecture so review
is targeted, not generic. The C2 shape (three behaviors, one capture)
is exactly midterm C2. -->

---

## Module 2: Attack Mechanics

- L2: MAC flooding (fail-open), ARP poisoning (MITM), rogue DHCP
  (both blades), VLAN hop, STP abuse
- Interception: position ≠ payload — switch features vs crypto
- DoS: volumetric / protocol-state / application — *diagnose the
  dying resource first*
- Amplification math: reply ÷ request × attacker bandwidth

<!-- notes: (8 min) The three-lecture sweep with one slide each. Quiz 2
+ quiz 7 territory. Work one amplification calc live (DNS: ~50×). -->

---

## Module 2 in Exam Form

- B2: rogue DHCP's two effects + the switch fix
- C2: the three-behavior capture (ARP storm, DNS churn, SMB SYN
  burst) — classify, contain each, name the preventing feature
- Practice: self-check quiz 7

<!-- notes: (4 min) C2's containment column is per-behavior — students
who write one containment for three behaviors lose marks. The
preventing-feature row is DAI. -->

---

## Module 3: The Defensive Architecture

- Zones by sensitivity + behavior; **unlisted = denied**
- Stateful vs stateless: the state table validates returns
- First-match ACLs: broad permits erase later denies
- Placement: every boundary = a decision point (DMZ egress!)

<!-- notes: (8 min) Diagrams 01+04 re-shown. Diagram 04's decision flow
is C1's answer skeleton — walk it with the management-VLAN example
verbatim (it IS midterm C1). -->

---

## Module 3 in Exam Form

- C1: management-VLAN ACL — jump host, monitoring subnet, deny+log,
  established, **order argument**
- D1-preview: hospital zoning — patient-safety-over-policy beats
- Practice: self-check quiz 8

<!-- notes: (5 min) C1's five elements and their marks: jump-host
permit (3), monitoring permit (3), deny+log (4), established (2),
order argument (3). D1's infusion-pump trap: broker the vendor path. -->

---

## Module 4: Claims Become Proofs

- Hash ≠ encryption ≠ authentication; signature = HMAC + non-repudiation
- Hybrid pattern: asymmetric to establish, symmetric to move data
- Chain validation: path → expiry → revocation → SAN
- Tunnel mode wraps the whole packet; PFS seals past traffic

<!-- notes: (8 min) Quiz 9's territory + midterm B3. The "AES-256 so
it's secure" fallacy (quiz-9 Q7): two counters — key exchange, endpoint
trust. -->

---

## Module 4 in Exam Form

- B3: encryption/auth/integrity + what signatures add
- B4: split-tunnel on unmanaged devices + compensations
- D2-preview: the VPN migration scenario
- Practice: self-check quiz 9

<!-- notes: (4 min) B4's honest middle: posture-gated split tunnel.
D2's certificate-lifecycle row: automated issuance + monitored expiry
(the assignment-2 lesson). -->

---

## The Judgment Patterns (Cross-Module)

1. **Asymmetry of errors** — act when wait-wrong ≫ act-wrong
2. **Diagnose before mitigating** — which resource is dying?
3. **Order = policy** — ACLs, containment, restore sequences
4. **Honest limits** — every control's failure mode is examinable

<!-- notes: (5 min) The four judgment patterns are how the exam
separates bands. Each pattern cites its lecture. This slide is the
review's thesis. -->

---

## Practice Run: The Composite Scenario

- Capture shows: ARP replies from a new MAC + DNS churn to one domain +
  flat table + unanswered SYNs
- Draft: classify each, one containment each, the design change that
  prevents the class

<!-- notes: (12 min) Full walkthrough in pairs, then debrief. This is
C2's shape with a fourth behavior added — the strongest single review
activity. Answers map to lectures 6/7/8 + quiz keys. -->

---

## Q&A + Final Advice

- Sleep > cramming; mechanisms > memorized answers
- Read the full question before answering C/D
- **Bring:** nothing but a pen — closed book

<!-- notes: (3 min) Close. Point to quiz-13's answer key for
self-verification tonight. -->

---

## References

- Self-check quizzes 6–9, 13 (+ keys for self-verification)
- Diagrams: 01, 02, 03, 04, 05
- Exam: `assessments/midterm/midterm-exam.md`
