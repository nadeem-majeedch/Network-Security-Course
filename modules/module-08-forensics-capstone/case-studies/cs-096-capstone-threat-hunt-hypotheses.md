---
case: cs-096
title: Capstone VI — Designing a Hypothesis-Driven Threat Hunt
difficulty: expert
domain: Network monitoring and log analysis
module: 8
lecture-anchor: L32
clos: [CLO-15]
time-estimate: 25 min (5 min reasoning + 20 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-096-solution.md
---

# cs-096 — Capstone VI: Designing a Hypothesis-Driven Threat Hunt

> **Simulated scenario.** The estate, hypotheses, and data are fictional.

## Difficulty & Domain

- **Difficulty:** Expert · **Domain:** Network monitoring and log analysis · **CLO:** CLO-15
- **Est. time:** 25 minutes · **Anchor:** L32 (Capstone Presentations & Course Synthesis)

## Scenario

The Meridian ZT program (cs-093) is in phase 3; detection has
matured. The CISO commissions the estate's first *hypothesis-driven
threat hunt*: not alert triage, but structured searching for what
detection *misses*. You design the hunt: hypotheses grounded in this
estate's actual gaps, the queries/method per hypothesis, and the
output discipline (hunts that find nothing still must produce
value — coverage documentation).

## Stakeholders

- **CISO** — commissions; wants coverage evidence, not just findings.
- **Hunters (you + 1 DS analyst)** — 2 people, 2 weeks part-time.
- **SOC** — receives any findings as detections-to-build.
- **Board** — receives the coverage story (cs-094's next report).

## Network Context

- Telemetry: EDR (100% servers, tuned), SIEM (fw, AD, EDR, proxy,
  M365), Zeek on server VLANs, flow at the edge. No NDR on user
  VLANs; no endpoint process telemetry on the 30 legacy
  workstations; cloud flow logs (VPC) for AWS.
- Known blind spots (from cs-091/093): user-VLAN east-west traffic
  unobserved; legacy workstations EDR-less (running a controlled
  legacy app); AWS cross-account roles unmonitored for anomaly.
- Asset truth: CMDB reconciled (cs-091), 90%+ accurate.

## Available Evidence

- Detection coverage map (what SIEM rules exist, what MITRE
  techniques they claim to cover — vendor-mapped, unvalidated).
- The two near-misses (phish blocked, tainted-update blocked):
  their artifacts are available as *hunting ground truth* (what
  would we have seen if they'd succeeded?).
- Identity data: AD sign-ins, MFA logs, IdP (ZT phase-2) logs.

## Student Task

1. Write **5 hunt hypotheses** for *this* estate — each grounded in
   a stated blind spot or technique-coverage gap, phrased as a
   falsifiable claim ("if X were happening, we would see/not see
   Y"). At least one must use the near-miss artifacts.
2. For each hypothesis: the **method** (data source, query shape,
   analytic approach — statistical/behavioral/pattern), the
   **data-quality prerequisite**, and the **falsification
   condition** (what result closes the hypothesis as "not
   present").
3. Design the **no-findings output**: what a "nothing found" hunt
   contributes (coverage documentation, detection candidates,
   telemetry-gap list) — the deliverable shape when all 5 come
   back empty.
4. Make the **SOC handoff rule**: which hunt outputs become
   detections, which become telemetry requests, and how the hunt
   avoids becoming unpaid alert engineering.

## How to Approach This (Reasoning Scaffold)

- Hypotheses come from *your* gaps, not generic threat lists: the
  user-VLAN blindness and legacy workstations are this estate's
  actual exposures — hunt where you're blind, not where you're
  already watching.
- Falsifiability is what separates a hunt from browsing: each
  hypothesis states in advance what "absence" looks like.
- The near-miss artifacts are free ground truth: replay the path
  the phish *would* have taken — every gap in that replay is a
  hypothesis.

## CLO Mapping

- **CLO-15** — Capstone synthesis: proactive detection design.

## Safety Notes

- Simulated; hunting is on owned estate, authorized, passive.
