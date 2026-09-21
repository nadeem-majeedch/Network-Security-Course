---
case: cs-034
title: ACL Audit — Finding Shadowed and Redundant Rules
difficulty: intermediate
domain: Firewall and ACL design
module: 3
lecture-anchor: L11
clos: [CLO-4]
time-estimate: 12 min (5 min reasoning + 7 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-034-solution.md
---

# cs-034 — ACL Audit: Shadowed and Redundant Rules

> **Simulated scenario.** The router ACL, hit counters, and network are fictional.

## Difficulty & Domain

- **Difficulty:** Intermediate · **Domain:** Firewall and ACL design · **CLO:** CLO-4
- **Est. time:** 12 minutes · **Anchor:** L11 (ACLs & Rulebase Engineering)

## Scenario

A campus edge router's inbound ACL has grown for eight years. You are given
the ACL with 90-day hit counters and must classify each rule:
**keep / shadowed (unreachable) / redundant (duplicate) / dead (never hits) /
over-broad** — then produce the cleaned ACL with a hit-rate-safety argument.

## Stakeholders

- **Campus NOC** — fears breaking something ("every rule is load-bearing until proven otherwise").
- **Auditor** — wants dead/over-broad rules gone.
- **Researchers** — their flows must survive the cleanup.

## Network Context

- ACL applied inbound on the edge toward campus; campus research subnets:
  `10.4.0.0/16` (HPC cluster), `10.5.0.0/16` (general), admin `10.9.9.0/24`.
- ACL is stateless (router ACL) — return traffic relies on the reflexive
  handling upstream; cleanups must respect *both* directions' entries.

## Available Evidence

**ACL excerpt (with 90-day hit counters):**

| # | Rule | Hits/90d |
|---|---|---|
| 1 | permit tcp any host 10.4.1.10 eq 22 | 12,400 |
| 2 | permit tcp 10.9.9.0/24 any eq 22 | 41,000 |
| 3 | permit tcp any 10.4.0.0/16 eq 22 | **0** |
| 4 | permit ip 10.9.9.0/24 10.4.0.0/16 | 3,300 |
| 5 | permit tcp any 10.5.0.0/16 eq 443 | 1.2M |
| 6 | permit tcp 10.9.9.0/24 host 10.5.2.7 eq 443 | **0** |
| 7 | permit udp any any eq 53 | 8.9M |
| 8 | permit ip any 10.4.0.0/16 | 210 |
| 9 | permit icmp any any | 95,000 |
| 10 | permit ip any any | 4.1M |
| 11 | deny ip any any log | 0 |

## Student Task

1. Classify each rule (keep/shadowed/redundant/dead/over-broad) with a
   one-line reason — attention to *ordering* is the whole exercise.
2. Explain the **hit-counter trap**: which rule looks load-bearing but is
   structurally unreachable, and which looks dead but is *semantically*
   important to keep (or explicitly re-add)?
3. Produce the cleaned ACL and the **safe-cutover argument**: what you
   monitor, and the rollback trigger, that lets the NOC say yes.

## How to Approach This (Reasoning Scaffold)

- Trace *reachability*, not popularity: a rule with 4.1M hits may make later
  rules unreachable; a 0-hit rule may be an explicit deny that *defines* policy.
- "permit ip any any" above a deny = the deny is decoration — find which.
- Safe cutovers are *staged*: remove one class of dead rules at a time with
  the log-deny watching.

## CLO Mapping

- **CLO-4** — ACL defect classification and safe remediation.

## Safety Notes

- Paper audit; apply to real ACLs only through change control.
