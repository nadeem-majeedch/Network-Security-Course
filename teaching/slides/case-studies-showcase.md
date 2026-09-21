---
marp: true
theme: default
paginate: true
showcase: case-studies
covers: [cs-001, cs-100]
clos: [CLO-1, CLO-2, CLO-3, CLO-4, CLO-5, CLO-6, CLO-7, CLO-8, CLO-9, CLO-10, CLO-11, CLO-12, CLO-13, CLO-14, CLO-15]
duration: 45 min (induction/orientation use; reusable at case-set time)
status: complete
artifact-type: showcase-deck
speaker-notes: embedded
---

# The 100-Case Collection — Showcase & Method

**Network Security · Orientation Deck**

*Five minutes on the projector. Reason. Discuss. Reveal. Debrief.*

<!-- notes: OPEN (3 min). Purpose: introduce the case method in week 1
so the first cs-001 run feels familiar. This deck also opens each
graded case-set session (Sets A/B/C). -->

---

## Session Overview

- Learn the five-step case protocol
- Meet the collection's structure and arc
- See graded case sets and the safety frame

## How Every Case Runs

1. **Project** the case (scenario + evidence tables only)
2. **Reason** ~5 minutes — pairs or solo
3. **Discuss approaches** — collect 2–3 before revealing anything
4. **Reveal** the model solution — reasoning first, answer second
5. **Debrief** — tradeoffs + common mistakes

- Solutions live in the instructor tree — never projected

<!-- notes: (5 min) The pedagogy protocol from case-index §7 verbatim.
The "collect approaches first" step is where learning happens — skip it
and cases become answer-delivery. -->

---

## The Collection at a Glance

| Tier | Cases | What they train |
|---|---|---|
| Beginner (cs-001–020) | 20 | protocol reading fluency |
| Intermediate (cs-021–045) | 25 | attack mechanics → design judgment |
| Advanced (cs-046–075) | 30 | operational + detection reasoning |
| Expert (cs-076–100) | 25 | multi-stage incidents, governance, synthesis |

- 20 domains · 117 case→CLO mappings · every CLO ≥4 times

<!-- notes: (4 min) The tier logic: each tier *uses* the prior tier's
vocabulary. Point to case-index for the full maps. -->

---

## The Meridian Arc (cs-091–100)

- The expert tier is one continuous story: **Meridian Health Analytics**
- Assessment → roadmap → zero-trust design → board report → IR
  exercise → threat hunt → forensics → defense prep → simulation →
  full-scope walkthrough
- Your capstone rehearses the same arc in D1–D4

<!-- notes: (5 min) The arc map is the capstone's shadow — say so
explicitly. Students who see the arc structure their capstone better. -->

---

## Case Anatomy (What You Always Get)

- Scenario + stakeholders + **network context** + evidence tables
- Student task with a reasoning scaffold
- CLO mapping + time estimate
- In the key (instructor-only): model solution, alternatives,
  tradeoffs, common mistakes, prompts, rubric

<!-- notes: (4 min) The 19-element anatomy, student side vs instructor
side. "Reasoning scaffold" = the approach hints — use them, they're
scaffolding not spoilers. -->

---

## Showcases: One Slide Each

- **cs-003** — abnormal ARP replies (beginner: read the wire)
- **cs-031** — stateful rule evaluation (intermediate: order = policy)
- **cs-070** — alert-tuning economics (advanced: math beats instinct)
- **cs-081** — phishing first-hour (advanced: reversible-first)
- **cs-097** — multi-source timeline (expert: honesty is defensibility)

<!-- notes: (10 min) Five one-slide showcases: project each case's
scenario table, run a 60-second micro-reasoning round per case, then
show the case's *task* (not the solution). This is the collection's
trailer. -->

---

## Graded Case Sets (Three per Term)

| Set | Window | Tier mix | Weight |
|---|---|---|---|
| A | weeks 4–5 | 2 beginner + 1 intermediate | in-assignment marks |
| B | week 8 | 2 intermediate + 1 advanced | in-assignment marks |
| C | week 13 | 2 advanced + 1 expert | in-assignment marks |

- 25 minutes, closed book, written reasoning
- Rubric: decomposition, evidence, mechanism, solution, communication

<!-- notes: (5 min) The evaluation protocol's student-visible half.
"The written reasoning is the assessed artifact" — identical
conclusions with different evidence use score differently. -->

---

## Safety Frame (Every Semester, Every Case)

- All cases are **simulated fiction**, labeled as such
- No offensive tooling, no real IOCs, no target identification
- Reasoning about attack *mechanics* builds defense — case files never
  contain operational attack procedure

<!-- notes: (3 min) The safety frame is short because the collection
was built with it. State it plainly; move on. -->

---

## How to Study With the Bank

- Cases pair with lectures (anchor mapping in the index)
- Self-test: read the case, outline your reasoning, *then* check the
  solution's reasoning shape (not just the answer)
- The common-mistakes sections are the highest-value reading

<!-- notes: (4 min) Study advice: the common-mistakes sections are
where the exam lives. Close: first case runs next session. -->

---

## References

- Index: `docs-meta/case-index.md` (tiers, domains, CLO maps)
- Protocol: `assessments/case-study-evaluation/case-evaluation-rubric.md`
- Cases: `modules/module-*/case-studies/`
