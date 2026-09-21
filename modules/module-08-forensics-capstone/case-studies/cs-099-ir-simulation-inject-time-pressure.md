---
case: cs-099
title: IR Simulation — Handling Injects Under Time Pressure
difficulty: expert
domain: Incident response
module: 8
lecture-anchor: L31
clos: [CLO-11, CLO-15]
time-estimate: 25 min (5 min reasoning + 20 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-099-solution.md
---

# cs-099 — IR Simulation: Handling Injects Under Time Pressure

> **Simulated scenario.** The exercise, injects, and estate are fictional.

## Difficulty & Domain

- **Difficulty:** Expert · **Domain:** Incident response · **CLO:** CLO-11, CLO-15
- **Est. time:** 25 minutes · **Anchor:** L31 (Capstone Workshop & IR Simulation)

## Scenario

You are now *in* the exercise cs-095 designed. The lab mirror of
Meridian is live; injects arrive on schedule; two observers score
decisions. This case runs the drill in miniature: you receive the
first five injects in compressed form and must produce, for each,
the decision, its reversibility label, and its corroboration
basis — in *exercise conditions* (incomplete information, a
pushy executive, a legal clock). The skill: decision quality
under injected uncertainty, not case-study leisure.

## Stakeholders

- **IR team (you)** — deciding, on the clock.
- **Observers** — scoring corroboration, reversibility, timeliness.
- **Controller** — delivers injects; holds the veto.
- **Role-played exec/legal** — pressure sources.

## Network Context

- Lab mirror: EDR alerts scripted, SIEM queries pre-built, no
  production path (controller veto active).
- Inject clock: each inject below arrives with a countdown;
  decisions due before the next inject.

## Available Evidence

**The five injects (compressed):**

| T | Inject |
|---|---|
| 0:10 | EDR: mass file-rename on FS-mirror-01 |
| 0:30 | SIEM: staging egress from same host to unknown domain |
| 0:50 | Role-played VP (controller): "Our biggest customer is calling — did we lose their data? I need an answer NOW." |
| 1:10 | SIEM: svc_ops interactive login on DB-mirror-02 (never seen before) |
| 1:30 | Legal role-play: "Regulator clock — did awareness start? When do we notify?" |

## Student Task

For **each inject**, within the exercise rules, produce:
1. The **decision** (contain? communicate? escalate? — one line).
2. The **corroboration basis** (which sources support it — the
   three-way rule where applicable; "single-source, acting on
   asymmetry" where that's the honest basis, per cs-082).
3. The **reversibility label** and the fallback if wrong.
4. The **communication line** for injects 3 and 5 — exact words.

Then answer the **exercise-level question**: which inject forced
the *worst* decision-quality tradeoff, and what does that reveal
about the estate's real preparedness?

## How to Approach This (Reasoning Scaffold)

- The exercise scores *decision structure* under pressure, not
  clairvoyance: corroboration basis stated + reversibility
  labeled + fallback named = full marks *even when the decision
  later proves wrong*.
- Executive and legal injects test the cs-090/094 discipline:
  facts + labeled unknowns + next-update commitment; never
  invention under pressure.
- Time pressure punishes the unstated: an unspoken assumption is
  scored as no assumption.

## CLO Mapping

- **CLO-11** — Detection, triage, and containment decisions.
- **CLO-15** — Capstone-level integration under exercise conditions.

## Safety Notes

- Simulated exercise; no production systems; synthetic telemetry.
