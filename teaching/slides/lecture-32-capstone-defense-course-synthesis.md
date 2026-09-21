---
marp: true
theme: default
paginate: true
lecture: L32
week: 16
clos: [CLO-14, CLO-15]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# Capstone Defense & Course Synthesis

**Network Security · Lecture 32 · Week 16**

*Prove the design, then connect the whole course.*

<!-- notes: OPEN (2 min). Frame the session: defenses run in parallel
tracks; the synthesis deck closes the course for everyone together. -->

---

## Learning Objectives

1. **Defend** the capstone design against the five question archetypes
2. **Present** the board paragraph as the course's communication
  standard
3. **Synthesize** one defense chain spanning protocol → architecture →
  detection → response
4. **Evaluate** peers' designs with evidence-based questions
5. **Chart** the learning path beyond this course

<!-- notes: (1 min) Objective 3 is QB-050's synthesis question — the
course's integration test. Objective 5 is the honest careers slide. -->

---

## Defense Format (25 min per team)

- 10 min presentation: pains → architecture → evidence → exercise
- 15 min questions: the five archetypes (dependency, adversarial,
  alternative, scope, evidence)
- The weakness statement offered unprompted = the credibility move
- Panel scores criterion 6 independently, then reconciles

<!-- notes: (5 min) The defense guide's compression. Audience members
(not defending yet) take evidence-based question notes — objective 4's
peer role. Rubric: assessments/capstone/capstone-rubric.md. -->

---

## The Board Paragraph: Course Standard

- ≤120 words: incident/response summary, two honest limits, one ask
- Decidability rule: every metric changes what the board does
- Deferral ≠ failure — unnamed risk is the failure

<!-- notes: (4 min) cs-094's structure as the course's writing
standard. The D4 report grades it; defenses read it aloud. -->

---

## Synthesis: One Chain Through the Course

```
 Protocol fact (M1)     → ARP trusts unauthenticated broadcast
 Architecture (M3)      → management VLANs segmented, DAI on
 Detection (M6)         → Zeek flags gratuitous-ARP bursts
 Response (M7)          → runbook: isolate port, rotate creds,
                          reversible-first
 Governance (M8)        → the finding becomes an owned control change
```

- Each link names its module's mechanism — that's the course in one
  chain

<!-- notes: (6 min) QB-050's model shape walked link by link. Ask
students to draft *their own* chain from their capstone — the defense's
synthesis question is exactly this. Five minutes, then defenses. -->

---

## What the Course Deliberately Did NOT Cover

- Offensive tooling craft (by design — defensive framing, ADR-001)
- Single-vendor product administration (concepts > products)
- Formal cryptography proofs (mechanisms + limitations, not math)
- Compliance-framework paperwork (principles transfer, frameworks
  vary)

<!-- notes: (4 min) The honest scope statement per mission rule 9 —
name what's out and why. Students deserve the boundary. -->

---

## Where This Goes Next (Careers & Learning)

- Roles: SOC analyst → detection engineer → IR → security
  architect; DS-security: model/data-pipeline security
- Certifications as *checkpoints*, not education (name the class, not
  the marketing)
- Keep the lab habit: home range + course case bank + hunt practice

<!-- notes: (4 min) Career slide kept honest: course → role mapping
without vendor hype. The case bank (100 cases) remains usable
post-course — say so. -->

---

## CS/DS Example: The Synthesis Chain, DS Edition

- Protocol: DNS first-answer trust → design: resolver control +
  allow-list → detection: entropy analysis (your toolkit) → response:
  egress containment → governance: the telemetry-gap request filed

<!-- notes: (3 min) The DS-flavored chain mirrors the previous slide —
both drafts are welcome in defenses. -->

---

## Activity: The Defenses Run (the session IS the activity)

- Parallel panels per the schedule; synthesis deck between blocks

<!-- notes: The session's body is the defense blocks; this deck
bookends them. Timing: 4 teams × 25 min + breaks fits a 2-hour block
with two parallel panels; single-panel weeks split across two
sessions. -->

---

## Case Study: cs-100 (5 min)

- The full-scope walkthrough — the integration case, projected between
  defense blocks for the waiting teams

<!-- notes: (5 min) cs-100 as the integration showcase while panels
rotate. Its walkthrough table is the course's own summary. -->

---

## Formative Check

- The defense *is* the formative assessment; rubric bands recorded in
  the instructor key.

<!-- notes: (1 min) Scores reconcile per panel calibration rule; notes
recorded in capstone-rubric-bands.md's table. -->

---

## Course Close: The Three Sentences That Persist

1. *Identity on the wire is a claim — build controls that prove it.*
2. *Reversible before irreversible — order actions by the cost of being
  wrong.*
3. *State the unknown — honesty is defensibility.*

<!-- notes: (3 min) The course's three through-lines, read slowly.
These are on the final's synthesis question and in every professional
incident report worth reading. Close with the ethics contract one last
time: defensive, authorized, honest. -->

---

## References & Next

- Full course index: `docs-meta/case-index.md`, assessment coverage
- **Post-course:** the lab range and case bank remain usable — keep
  hunting.
