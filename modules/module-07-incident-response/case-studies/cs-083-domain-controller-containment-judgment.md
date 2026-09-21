---
case: cs-083
title: Isolating a Domain Controller at 2 a.m. — Kill vs Survive
difficulty: expert
domain: Incident response
module: 7
lecture-anchor: L26
clos: [CLO-11, CLO-12]
time-estimate: 15 min (5 min reasoning + 10 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-083-solution.md
---

# cs-083 — Isolating a Domain Controller at 2 a.m.: Kill or Survive?

> **Simulated scenario.** The intrusion, topology, and decisions are fictional.

## Difficulty & Domain

- **Difficulty:** Expert · **Domain:** Incident response · **CLO:** CLO-11, CLO-12
- **Est. time:** 15 minutes · **Anchor:** L26 (Detection, Triage & Containment)

## Scenario

03:10. Your NDR flagged abnormal LDAP and DCSync-style read patterns
between a member server and DC01 — one of two domain controllers.
DC01 shows signs of attacker access (new admin account, new GPO).
DC02 is clean so far. If you contain DC01 hard (isolate/offline), auth
load falls entirely on DC02 and some branch sites will feel it; if
you leave it, the attacker keeps a foothold in the directory itself.
Containment here is a *judgment* case, not a checklist case.

## Stakeholders

- **SOC (you)** — the 2 a.m. decision is yours.
- **Directory/AD owner** — on-call; would rather you didn't touch DCs.
- **Branch offices** — auth outages if DC02 staggers.
- **CISO** — asleep; wants to be woken for exactly this class.

## Network Context

- Two DCs; DC01 primary FSMO holder; ~6,000 employees, 12 branch sites.
- Member server SRV-FIN-02 suspected compromised (source of DCSync
  pattern).
- NDR + Windows event streaming; no packet capture on the DC VLAN.
- Backups: AD system-state nightly (last 01:00, pre-incident).

## Available Evidence

| T | Event |
|---|---|
| 22:40 | SRV-FIN-02 executes a credential-access tool (EDR) |
| 23:20 | DC01: new admin account "svc_backup2" created |
| 23:35 | DC01: new GPO linked at domain root (unreviewed script) |
| 01:05–03:05 | NDR: repeated DCSync-pattern reads DC01 ← SRV-FIN-02 |
| 03:10 | (now) DC02 shows *no* anomalous directory reads |

## Student Task

1. Decide the **containment posture for DC01**: (a) full isolate now,
   (b) partial containment (block its outbound + attacker account),
   (c) leave and monitor. Justify against the cost of each wrong.
2. Specify the **attacker-access revocation set** (the minimum
   directory actions that close the foothold without rebuilding).
3. Answer: **why is DC02's clean status load-bearing** for your
   decision — and what would you check to trust it?
4. Name the **wake-the-CISO threshold**: what fact would have made
   this call not yours to make?

## How to Approach This (Reasoning Scaffold)

- Redundancy is what makes containment affordable: two DCs means you
  can survive losing one — check the *claim* of cleanliness before
  leaning on it.
- Directory footholds compound: an admin account + GPO is execution
  infrastructure, not just access — the GPO alone can redeploy the
  attacker at next boot cycle.
- Partial containment is a real middle option: cut the attacker's
  path while keeping the DC serving — but only if the attacker's
  *current* path actually runs through what you're blocking.

## CLO Mapping

- **CLO-11** — High-stakes containment judgment.
- **CLO-12** — Evidence-weighted decision under uncertainty.

## Safety Notes

- Simulated; conceptual DCSync framing only, no tooling detail.
