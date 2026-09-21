# cs-095 — Capstone V: Designing the First Full IR Exercise

> **Simulated scenario.** The estate and exercise are fictional.

## Difficulty & Domain

- **Difficulty:** Expert · **Domain:** Incident response · **CLO:** CLO-15
- **Est. time:** 25 minutes · **Anchor:** L32 (Capstone Presentations & Course Synthesis)

## Scenario

Meridian Health Analytics' capstone arc ends with the exercise
cs-094's board asked for: a full incident-response exercise — not a
tabletop discussion, a *timed operational drill* with injected
telemetry, decisions under time pressure, and observer scoring.
You design it. The constraints: 4 hours, 12 participants (IR + ops +
comms + legal liaison), zero production impact, and the exercise
must produce findings the board can fund against.

## Stakeholders

- **CISO (you)** — exercise designer and controller.
* **Participants** — IR + ops + comms + legal liaison; first drill
  with this team shape.
- **Observers** — 2; score decisions, not people.
- **Board** — receives the findings-and-funding case.

## Network Context

- Scenario: the cs-082 ransomware-precursor pattern in the Meridian
  estate (EDR alerts on a file server, staging egress, service
  account lateral movement) — *injected as synthetic telemetry*
  into a lab mirror of the estate.
- Lab mirror: simulated EDR console (scripted alerts on schedule),
  synthetic SIEM queries (pre-built results), simulated phone tree
  (controllers role-play external parties).
- Injects: 9 scheduled + 2 conditional (fired on participant
  action, e.g., if they isolate the server).

## Available Evidence

- The exercise design brief: objectives (test detection-to-decision
  chain, comms tree, containment authority, legal-escalation
  trigger), constraints, inject schedule skeleton.
- Scoring rubric skeleton: decision timeliness, corroboration
  discipline (three-way rule), containment reversibility labeling,
  comms accuracy.
- The cs-086 review conversion rule (output items must be owned,
  dated, verifiable).

## Student Task

1. Design the **inject schedule**: 9 scheduled + 2 conditional
   injects across 4 hours, each with its *tested objective* (what
   decision it forces) and the scoring hook it creates. Show the
   escalation arc (why this order).
2. Define the **scoring rubric**: 5 criteria, each with an
   observable anchor (what a good decision looks like at time T)
   and what observers record. Decisions, not people.
3. Design the **zero-production-impact guarantee**: what is
   simulated vs real, and the rules that keep the exercise from
   touching production (the two rules that matter most).
4. Plan the **debrief → board case**: how exercise findings convert
   (via the cs-086 rule) into the board's findings-and-funding
   page; give the 3 findings you expect this design to produce.

## How to Approach This (Reasoning Scaffold)

- Injects are *decision forcings*, not plot: each tests one
  objective (who decides isolation? when does legal engage? what
  does comms say at hour 2 with 30% facts?).
- Conditional injects are what make a drill a *test* — they respond
  to participant action, closing the gap between script and
  reality.
- Production-safety rules must be *structural* (different network,
  no real credentials, controller veto), not behavioral promises.

## CLO Mapping

- **CLO-15** — Capstone synthesis: operational readiness by design.

## Safety Notes

- Simulated exercise design; no production-touching steps; injects
  are synthetic telemetry descriptions, not attack tooling.
