---
case: cs-093
title: Capstone III — Zero-Trust Migration Design for a Hybrid Estate
difficulty: expert
domain: Zero trust
module: 8
lecture-anchor: L31
clos: [CLO-15]
time-estimate: 25 min (5 min reasoning + 20 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-093-solution.md
---

# cs-093 — Capstone III: Zero-Trust Migration Design for a Hybrid Estate

> **Simulated scenario.** The estate and constraints are fictional.

## Difficulty & Domain

- **Difficulty:** Expert · **Domain:** Zero trust · **CLO:** CLO-15
- **Est. time:** 25 minutes · **Anchor:** L31 (Capstone: Design Defense)

## Scenario

Meridian Health Analytics, six months later (cs-091/092 done: IR
live, VPN MFA done, EDR at 100% of servers): the board has approved
the next investment — a zero-trust migration. The mandate is
deliberately open: "design our zero-trust *approach*," not "buy a
product." You must produce the migration design: what zero trust
means *here*, the phasing that doesn't break a 60-person DS group
or 12 branch sites, and the identity/architecture prerequisite
chain — with the honest statement of what zero trust will *not*
fix.

## Stakeholders

- **Board** — funding a multi-year program; wants phase gates.
- **CTO/CISO** — own the design; 3 staff still (1 hire approved).
- **DS lead** — velocity guardrail now institutionalized (measured ≤10%).
- **Branch staff** — 12 sites, latency-sensitive apps on-prem.

## Network Context

- As-is: perimeter VPN (MFA now), flat-ish internal with VLAN
  islands, hybrid AD/AWS identity (separate), EDR 100% servers,
  SIEM fw+AD+EDR, no NDR.
- Branch: MPLS to DC1; local internet breakout for SaaS at 4 sites.
- Apps: ERP (on-prem), analytics platform (AWS), SaaS suite, DS
  cluster (AWS sandbox account, peered).
- The DS velocity guardrail: any per-request auth added to
  experiment paths must show measured ≤10% overhead.

## Available Evidence

- cs-092 outputs: IR plan live, MFA done, EDR coverage report,
  segmentation *design doc* (not built).
- Access analysis (from SIEM): top 20 app flows by volume and
  sensitivity — the natural pilot candidates.
- Branch latency SLOs: ERP interactions ≤150 ms round-trip.

## Student Task

1. Define **what zero trust means for this estate**: the policy
   model (identity-centric per-request decisions), what replaces
   VPN-centric access, and the **prerequisite chain** (identity
   consolidation → device trust → policy engine → per-app
   enforcement) with what each step unblocks.
2. Design the **migration phasing** (3–4 phases, phase gates with
   measurable exit criteria) — pilot selection logic (which 2 apps,
   why those), branch handling, and the DS-cluster treatment.
3. State **what zero trust will not fix** — the honest list — and
   what the roadmap pairs it with.
4. Make the **board argument**: why phase gates + measured
   guardrails beat a big-bang program; quantify the guardrail
   enforcement mechanism (the velocity probe from cs-092,
   institutionalized).

## How to Approach This (Reasoning Scaffold)

- Zero trust is an *access-policy model*, not a product: the design
  question is "who/what decides, on what signals, per request" —
  the product question comes after the model.
- Identity consolidation is the root prerequisite: per-request
  decisions need one authoritative identity plane; the AD/AWS
  split is the first wall.
- Pilots are chosen by *policy variety*, not size: two apps whose
  access patterns stress different conditions (device trust,
  location, session risk) prove the model faster than two similar
  apps.

## CLO Mapping

- **CLO-15** — Capstone synthesis: architecture program design.

## Safety Notes

- Simulated; no vendor endorsement.
