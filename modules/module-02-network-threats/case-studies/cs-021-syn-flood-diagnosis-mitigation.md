---
case: cs-021
title: SYN-Flood Diagnosis and Mitigation Options
difficulty: intermediate
domain: Network security principles
module: 2
lecture-anchor: L08
clos: [CLO-2]
time-estimate: 12 min (5 min reasoning + 7 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-021-solution.md
---

# cs-021 — SYN-Flood Diagnosis and Mitigation Options

> **Simulated scenario.** The retailer, infrastructure, and metrics are fictional.

## Difficulty & Domain

- **Difficulty:** Intermediate · **Domain:** Network security principles · **CLO:** CLO-2
- **Est. time:** 12 minutes · **Anchor:** L08 (DoS, DDoS & Infrastructure Abuse)

## Scenario

A mid-size online retailer's storefront slows at 18:55, degrades to errors by
19:10. Black-Friday rehearsal is in two weeks. You have the edge metrics below
and must (a) confirm the diagnosis, (b) pick tonight's mitigation, and (c)
propose the pre-rehearsal architecture change. The incumbent "DDoS vendor"
salesperson is available by phone; you have budget authority for one emergency
decision.

## Stakeholders

- **Shoppers** — revenue is bleeding per minute.
- **Retail CTO** — wants a decision, not options.
- **Hosting provider** — has scrubbing capacity and an activation SLA.
- **Attacker (presumed)** — unknown motive; competitor? extortion? test?

## Network Context

- Storefront: 4× app servers behind an on-prem LB, 1 Gbps internet uplink.
- The LB does TCP termination; SYN cookies **disabled** (legacy tuning fear).
- No CDN in front; DNS points directly at the uplink IP.
- Health checks: LB→app servers every 5 s, from LB subnet.

## Available Evidence

| Time | SYNs/s to :443 | Completed handshakes/s | Uplink util | LB CPU | Notes |
|---|---|---|---|---|---|
| 18:50 | 400 | 390 | 22% | 35% | baseline |
| 18:55 | 9,000 | 380 | 48% | 61% | alert fired |
| 19:05 | 41,000 | 350 | 88% | 70% | shoppers see timeouts |
| 19:10 | 95,000 | 340 | 97% | 71% | storefront effectively down |
| Source profile | ~90k SYNs/s | spread over ~12,000 IPs | | | mixed flags, random src ports |

## Student Task

1. Confirm/refute "SYN flood" from the metrics, and identify **which resource
   is actually saturating first** — this determines tonight's fix.
2. Choose tonight's mitigation from: enable SYN cookies on the LB · activate
   provider scrubbing (2 h SLA) · rate-limit SYNs at the edge · move DNS to a
   CDN tonight. Justify the choice and name what each rejected option would
   have done.
3. Design the **pre-rehearsal architecture change** (one paragraph): what
   stands in front of the origin, and why that shape ends this attack class.

## How to Approach This (Reasoning Scaffold)

- Two different saturations hide in the numbers: *state* (LB/kernel queues)
  and *bandwidth* (uplink pps). Which one is at 97%?
- SYN cookies trade a little CPU for infinite half-open tolerance — the
  legacy fear is usually about performance, not correctness.
- "Tonight" fixes differ from "two weeks" fixes in reversibility and blast radius.

## CLO Mapping

- **CLO-2** — DoS mechanics and mitigation engineering.

## Safety Notes

- Simulated incident; mitigation of *your own* service is defensive.
