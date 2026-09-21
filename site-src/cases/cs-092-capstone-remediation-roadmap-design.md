# cs-092 — Capstone II: The Remediation Roadmap Under Real Constraints

> **Simulated scenario.** The estate, budget, and politics are fictional.

## Difficulty & Domain

- **Difficulty:** Expert · **Domain:** Enterprise architecture · **CLO:** CLO-15
- **Est. time:** 20 minutes · **Anchor:** L30 (Capstone: Architecture & Assessment Clinic)

## Scenario

Continuing Meridian Health Analytics (cs-091): the board funded your
top-3 (IR activation, VPN MFA, EDR completion) plus a $250k/
6-month remediation budget. The constraints are real: the DS group
will not accept tooling that slows experiment turnaround >10%; the
ops team has one net-admin and two sysadmins; and an external
security questionnaire from a *prospective enterprise customer* is
due in 60 days — the funding round's diligence depends on it. Design
the roadmap: sequencing, staffing, quick wins vs structural work,
and how the roadmap's *evidence* feeds the questionnaire.

## Stakeholders

- **Board/funding round** — diligence story in 60 days.
- **CTO/CISO** — owns delivery with 3 technical staff.
- **DS lead** — velocity guardrail (≤10% slowdown).
- **Ops team** — 3 people, all the toil lands here.

## Network Context

- As cs-091: hybrid estate, 2 DCs, AWS prod + ds-sandbox, flat
  internal design, SIEM with fw+AD only, EDR 60%.
- Funded work: (1) IR plan activation + tabletop, (2) VPN MFA for
  the legacy team, (3) EDR to 100% servers.
- Unfunded backlog: segmentation redesign, DA reduction, DS data
  governance (public buckets, cached creds).

## Available Evidence

- cs-091 findings register (12 findings, 3 funded).
- Staffing: 1 net-admin, 2 sysadmins, 0 dedicated security staff.
- Questionnaire: 140 questions, mostly control-existence + process
  evidence (IR plan, access reviews, vuln mgmt cadence).
- DS group: 60 staff, ~2,000 notebook runs/week; any per-run
  friction compounds fast.

## Student Task

1. Produce the **6-month roadmap** (months 1–6) with workstreams,
   owners from the 3-person team, and the dependency logic —
   including what the roadmap *deliberately defers* and why.
2. Design the **60-day questionnaire play**: which funded items
   produce questionnaire evidence fastest, what can be answered
   honestly *during* remediation ("in progress, target Q3"), and
   the two answers that must NOT be fudged.
3. Solve the **DS velocity conflict**: propose the implementation
   shape for EDR-on-servers and data-governance controls that meets
   the ≤10% velocity guardrail — what makes it acceptable to the DS
   lead?
4. Define the **quick-win list**: ≤5 items, each ≤2 staff-days,
   each closing or shrinking a cs-091 finding — with their
   questionnaire value.

## How to Approach This (Reasoning Scaffold)

- Roadmaps under constraint are *portfolio + sequencing* problems:
  dependency order (identity before segmentation; IR before
  tooling sprawl) and staff reality (3 people cannot do 6
  workstreams in parallel).
- The questionnaire is an *output* of remediation, not a parallel
  writing exercise: every honest "yes" needs an artifact the
  roadmap produces.
- Velocity guardrails are met by *where* controls sit (baseline
  images, platform-side) not by *whether* they exist.

## CLO Mapping

- **CLO-15** — Capstone synthesis: roadmap, constraints, evidence.

## Safety Notes

- Simulated; no real vendor commitments implied.
