# cs-094 — Capstone IV: The Board Risk Report

> **Simulated scenario.** The estate and metrics are fictional.

## Difficulty & Domain

- **Difficulty:** Expert · **Domain:** Risk management · **CLO:** CLO-15
- **Est. time:** 25 minutes · **Anchor:** L31 (Capstone: Design Defense)

## Scenario

The capstone closes where governance lives: the quarterly board
risk report. Six months of data exist (cs-091–093 execution): IR
plan live, VPN MFA done, EDR at 100% of servers, ZT program in
phase 2, MTTD improved from 19–41 days to 9 days, one contained
incident (a cryptomining compromise caught in 4 hours), and a
funding round that closed. The CISO has 15 minutes of board time.
Produce the report: what the board must decide or know, in their
language, with the technical story *underneath* it — and the
discipline to leave things out.

## Stakeholders

- **Board** — fiduciary duty; non-technical; 15 minutes.
- **CISO (you)** — reporting; wants the ZT phase-3 funding.
- **External auditor** — reads the same report.
- **CTO** — co-signs; owns some unfunded asks.

## Network Context

- Metrics: MTTD 34/41/19 d → 9 d (trend across 4 quarters); MTTR
  19 d → 6 d; EDR coverage 60%→100%; MFA coverage 97%→100%; ZT
  pilots: 2 apps, 98.5% access-decision success; velocity probe:
  ≤7% overhead.
- Incidents: 1 contained (cryptomining, caught 4 h, 0 data impact);
  2 near-misses (phish blocked, tainted-update blocked at freeze).
- Open risks: segmentation build unfunded; DS data-governance
  phase 2; key-person dependency (the net-admin).
- Budget: ZT phase-3 ask (branch + ERP + privileged access).

## Available Evidence

- The four-quarter metric trend (above) with collection method
  notes (what each metric measures, what it misses).
- The incident post-mortem (cs-086-style review, 5 action items,
  4 closed).
- The ZT phase-2 exit report (gates met).
- Audit letter: two observations (evidence vintages, IR plan
  currency).

## Student Task

1. Structure the **report**: the 5 sections a board report needs
   (position, trend, incidents, asks, decisions needed) — with the
   *one-line takeaway* per section that a non-technical director
   retains.
2. Design the **metric choices**: which 5 metrics earn their place,
   how each is honestly bounded (what it misses), and which
   tempting metric you deliberately exclude (and why).
3. Make the **ask**: the ZT phase-3 case in board language — what
   it buys, what happens if deferred, tied to the risk trend (not
   fear, not tech).
4. Write the **bad-news paragraph**: the key-person dependency and
   the segmentation gap — how the report states open risk without
   either alarm or burying.

## How to Approach This (Reasoning Scaffold)

- A board report is a *decision instrument*, not a status update:
  every section either informs oversight or requests a decision;
  anything else is noise the reader must wade through.
- Metrics earn inclusion by *decidability*: does this number change
  what the board does? MTTD does (response capability trend);
  "alerts closed" doesn't.
- Bad news travels best with a plan attached: risk stated + owner +
  mitigation path = governance; risk stated alone = alarm; risk
  omitted = liability.

## CLO Mapping

- **CLO-15** — Capstone synthesis: governance communication.

## Safety Notes

- Simulated; no real fiduciary advice.
