# cs-005 — ICMP Misuse Red Flags (Unusual Types and Volumes)

> **Simulated scenario.** All hosts, addresses, and rates are fictional.

## Difficulty & Domain

- **Difficulty:** Beginner · **Domain:** TCP/IP protocol analysis · **CLO:** CLO-1
- **Est. time:** 10 minutes · **Anchor:** L02 (Protocol Deep Dive I)

## Scenario

A monitoring dashboard at a regional ISP's corporate office flags "ICMP
volume +800% vs 30-day baseline" at 02:10. You are handed a 2-minute slice of
edge-router NetFlow-style records summarizing ICMP activity to and from one
internal subnet. Your job is not to declare an attack but to produce the
red-flag list that decides whether an analyst looks at it tonight.

## Stakeholders

- **NOC analyst (on-call)** — wants a short, decisive red-flag list, not a report.
- **Corporate users** — asleep; their subnet is the noisy one.
- **ISP security manager** — owns the escalation decision.

## Network Context

- `198.51.100.0/24` corporate subnet; edge router to the internet.
- Normal ICMP profile (30-day baseline): mostly type 0 (echo replies), type 3
  (unreachable) from the router itself, type 8 outbound pings from one
  monitoring host `.9` (NMS), ~200 packets/min total.
- ICMP is permitted in/out; no rate limiting configured.

## Available Evidence

NetFlow-style ICMP summary (2-minute slice, 02:10):

| Type/code | Direction | Source | Dest pattern | Pkts/min | Notes |
|---|---|---|---|---|---|
| 8 (echo) | out | .9 (NMS) | internet | 210 | normal NMS polling |
| 0 (reply) | in | internet | .9 | 200 | matches polling |
| 8 | out | **.77, .78, .90** | **random internet IPs** | 1450 | sizes exactly 1400 B, 1/s each |
| 0 | in | random IPs | .77/.78/.90 | 1380 | many "unreachable" payloads inside |
| 3/4 (frag needed) | in | internet | any | 0 | baseline shows occasional |
| 13/14 (timestamp) | in | 2 external IPs | .5, .6 | 8/min | new this week |
| 3/3 (port unreachable) | out | router | internet | 30/min | routine |

## Student Task

1. Classify each row: normal / notable / red-flag, with a one-line reason.
2. What traffic pattern does the .77/.78/.90 row most resemble? Name two
   distinct things an attacker could be doing with it and how you would tell them apart.
3. Recommend: wake the analyst tonight or defer to morning? One sentence of justification.

## How to Approach This (Reasoning Scaffold)

- Volume is a signal, but *shape* (who, where, sizes, periodicity) is the story.
- Exactly-sized packets at steady rates is a signature worth knowing.
- The baseline rows are there to anchor "normal" — use them, don't re-litigate.

## CLO Mapping

- **CLO-1** — Protocol-aware indicator triage.

## Safety Notes

- Simulated flow data. No scanning or testing against real infrastructure.
