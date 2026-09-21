---
marp: true
theme: default
paginate: true
lecture: L31
week: 16
clos: [CLO-11, CLO-15]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# Capstone Workshop & IR Simulation

**Network Security · Lecture 31 · Week 16**

*You designed it, built it — now the injects arrive.*

<!-- notes: OPEN (2 min). Hook: "Today the course runs its own cs-095
exercise — your architecture, live injects, decisions on the clock." -->

---

## Learning Objectives

1. **Run** the team's capstone architecture under inject pressure
2. **Decide** with stated corroboration basis and reversibility labels
3. **Communicate** under pressure: holding-statement discipline
4. **Handle** the legal-clock inject without inventing certainty
5. **Convert** exercise failures into owned amendments

<!-- notes: (1 min) Objectives map to cs-099's inject set and the
capstone's D3 deliverable. The observers' rubric (cs-095's five
criteria) is on the wall during the drill. -->

---

## Exercise Ground Rules

- Lab mirror only; controller veto on anything production-shaped
- Injects arrive on schedule; decisions due before the next inject
- Observers score **decisions, not people** (corroboration,
  reversibility, timeliness, comms accuracy)

<!-- notes: (4 min) The scoring frame keeps candor alive — same reason
as cs-086's blameless rule. Teams that fear scoring hide decisions. -->

---

## The Inject Arc (90-Minute Compressed Run)

| T | Inject | Tests |
|---|---|---|
| 0:00 | EDR alert: mass rename on FS-mirror | triage start, lead named |
| 0:20 | staging egress from same host | three-way corroboration |
| 0:40 | VP demands customer-data answer | holding statement |
| 1:00 | svc_ops interactive on DB-mirror | credential blast radius |
| 1:20 | legal: "regulator clock?" | awareness-vs-certainty |

<!-- notes: (6 min) cs-099's inject set is the schedule. The arc logic:
scope builds, pressure peaks, closure. Each inject's *expected
decision* is in cs-099's key — observers carry it. -->

---

## The Scoring Rubric (Wall Copy)

| Criterion | Anchor |
|---|---|
| Corroboration | ≥2 sources before containment calls |
| Reversibility | labels at decision time |
| Timeliness | lead ≤10 min; containment ≤30 min |
| Comms accuracy | facts + unknowns, no invention |
| Legal trigger | criteria stated correctly |

<!-- notes: (3 min) Read once; observers reference during the run.
Mirrors cs-095's rubric — capstone D3 uses the same five. -->

---

## Debrief Protocol

1. Timeline walk — what happened, no editorializing
2. Decision review — where did corroboration hold? where did it slip?
3. Amendment capture — two owned, dated changes per team minimum
4. The design question: which inject exposed an *architecture* gap vs a
   *runbook* gap?

<!-- notes: (8 min) The design-vs-runbook distinction is the capstone
D3's deepest question: architecture gaps go into D1's revision; runbook
gaps into the amendment list. Both owned. -->

---

## Workshop: Capstone Build Clinic (remaining time)

- Teams work D2 evidence packs: configs, replay results, tested-vs-
  assumed labels
- Instructor checkpoint: each team states its *weakest dependency* and
  its fallback (cs-098's discipline)
- Defense-signup: 25-minute panels, report due 48 h before

<!-- notes: (50 min workshop block) Circulate per team: 5-minute
checkpoint each. The weakness statement is the gate — teams that can't
name it aren't ready to defend. Defense guide: assessments/capstone/
defense-guide.md. -->

---

## CS/DS Example: Exercise Findings as Data

- The inject timeline is a dataset: decision latency, corroboration
  counts, comms accuracy — measurable readiness
- Teams quote their own numbers in the defense ("lead named in 7 min")

<!-- notes: (3 min) DS framing: readiness becomes measurable — their
own exercise produces the analytics for their defense. -->

---

## Activity: The Full Run (the lecture IS the activity)

- Run the five injects + debrief per the protocol above

<!-- notes: The lecture's activity block is the exercise itself;
timing notes embedded above. Observers: TA + instructor. -->

---

## Case Study: cs-099 (the run uses its injects)

- Cases cs-095/cs-099 are today's materials — design + inject set

<!-- notes: (2 min) Point students to both case files as the exercise's
documentation. -->

---

## Formative Check

- The debrief's amendment list *is* the formative artifact — collected
  per team.

<!-- notes: (2 min) Amendments go into D3's exercise record — graded
there. -->

---

## References & Next

- `assessments/capstone/defense-guide.md`; cs-095/cs-099 case files
- Diagrams: `diagrams/08-ir-lifecycle-workflow.md`
- **Next (L32):** capstone defense & course synthesis
