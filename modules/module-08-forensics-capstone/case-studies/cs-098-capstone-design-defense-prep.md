---
case: cs-098
title: Capstone Design Defense — Surviving the Panel
difficulty: expert
domain: Enterprise architecture
module: 8
lecture-anchor: L31
clos: [CLO-15]
time-estimate: 25 min (5 min reasoning + 20 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-098-solution.md
---

# cs-098 — Capstone Design Defense: Surviving the Panel

> **Simulated scenario.** The estate, panel, and question bank are fictional.

## Difficulty & Domain

- **Difficulty:** Expert · **Domain:** Enterprise architecture · **CLO:** CLO-15
- **Est. time:** 25 minutes · **Anchor:** L31 (Capstone Workshop & IR Simulation)

## Scenario

The course's design defense is next week. A panel (one network
architect, one SOC lead, one DS faculty) will probe your Meridian-
based design (the cs-091→093 arc) for the three things panels
always probe: **the weakest dependency**, **the cost of being
wrong**, and **what you cut and why**. This case is defense
preparation as a skill: you build the anticipated-question bank,
the honest-weakness statement, and the fallback positions — then
stress-test a classmate's defense.

## Stakeholders

- **You (candidate)** — defending a design you'll be asked to
  modify live.
- **The architect** — probes feasibility and dependencies.
- **The SOC lead** — probes detection/response implications.
- **DS faculty** — probes the research-velocity tradeoffs.

## Network Context

- The design under defense: ZT phase-3 (branch + ERP identity
  evaluation + privileged access), segmentation design for the
  legacy tail, per-job credentials for the DS cluster — from
  cs-093's phases, now at defense depth.
- Course artifacts available as evidence: findings register
  (cs-091), roadmap (cs-092), ZT design (cs-093), metrics story
  (cs-094).

## Available Evidence

- **Known weak points in the design** (be honest with yourself
  first): ERP identity evaluation rides on legacy app auth that
  can't natively do per-request; the ZT model leans on one IdP
  (new single point of failure); the segmentation *build* is
  deferred while the design assumes it for the legacy tail.
- **Panel question archetypes:** dependency challenge ("what if X
  is down?"), adversarial ("how does this fail silently?"),
  alternative ("why not just buy Y?"), scope ("what did you
  deliberately not do?"), evidence ("what measured result backs
  this?").

## Student Task

1. Build the **question bank**: 10 questions the panel will ask
   (2 per archetype above, aimed at *this* design), each with a
   3-sentence model answer that cites course evidence.
2. Write the **honest-weakness statement**: the design's single
   weakest dependency, stated *by you first* — with the mitigation
   and the fallback if the mitigation fails. (Panels trust
   candidates who name the weakness before they find it.)
3. Prepare the **fallback positions**: for the two most likely
   live-modification demands ("drop phase 3 to save money",
   "cut the legacy-tail segmentation"), the pre-thought answer:
   what you'd cut, what risk you'd accept in writing, what you'd
   never cut.
4. Do the **stress-test swap**: exchange designs with a partner;
   attack theirs with your bank for 10 minutes; note which
   question types actually broke defenses (feed this back into
   your own prep).

## How to Approach This (Reasoning Scaffold)

- A defense is won on *evidence chains*, not bravado: every answer
  traces to an artifact (findings, gates, measured probes) — the
  panel is testing whether the design is a system or a story.
- Naming the weakness first converts the panel's best attack into
  your credibility moment — but only with mitigation + fallback
  attached.
- Fallback positions are pre-negotiated risk acceptance: in the
  room you *choose* between prepared positions; improvised
  concessions read as fragility.

## CLO Mapping

- **CLO-15** — Capstone synthesis: design communication under challenge.

## Safety Notes

- Simulated panel; no real assessment.
