---
case: cs-004
title: IP Fragmentation Anomaly in a Routed Capture
difficulty: beginner
domain: TCP/IP protocol analysis
module: 1
lecture-anchor: L02
clos: [CLO-1]
time-estimate: 10 min (5 min reasoning + 5 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-004-solution.md
---

# cs-004 — IP Fragmentation Anomaly in a Routed Capture

> **Simulated scenario.** The network, hosts, and numbers below are fictional
> teaching data.

## Difficulty & Domain

- **Difficulty:** Beginner · **Domain:** TCP/IP protocol analysis · **CLO:** CLO-1
- **Est. time:** 10 minutes · **Anchor:** L02 (Protocol Deep Dive I)

## Scenario

You support a university CS department network. The firewall team forwards you
a capture snippet from the department border. Off-campus traffic to an internal
file server has been unusually slow this week; on-campus traffic is normal.
The capture covers one internal client (10.3.1.20) fetching a large file from
an external partner site (203.0.113.77), both directions included.

## Stakeholders

- **Students/researchers** — slow downloads hurt coursework and research.
- **Network team** — owns the border MTU story.
- **Partner site** — availability of their service affects your users.
- **Firewall team** — wants a verdict before touching rules.

## Network Context

- Border links: campus core 1500 MTU; the department uplink is PPPoE (MTU 1492).
- Internal file server and clients sit behind the border router.
- Partner path beyond campus is standard internet MTU 1500.

## Available Evidence

Key packets from the capture (MSS = TCP maximum segment size; MF = more-fragments flag):

| # | Dir | Source→Dest | Proto | Info |
|---|---|---|---|---|
| 1 | out | 10.3.1.20 → 203.0.113.77 | TCP | SYN, MSS 1460, DF not set |
| 2 | in | 203.0.113.77 → 10.3.1.20 | TCP | SYN-ACK, MSS 1460 |
| 3 | out | 10.3.1.20 → 203.0.113.77 | TCP | ACK, request file |
| 4 | in | 203.0.113.77 → 10.3.1.20 | TCP | 1460 B data segment, DF=1 |
| 5 | in | 203.0.113.77 → 10.3.1.20 | TCP | same segment retransmitted ×6 over 45 s |
| 6 | — | 10.3.1.20 → 203.0.113.77 | ICMP | none seen: no type 3 code 4 anywhere in capture |
| 7 | in | 203.0.113.77 → 10.3.1.20 | TCP | 512 B data segment — finally ACKed |
| 8 | in | 203.0.113.77 → 10.3.1.20 | TCP | file completes in small 512 B increments |

## Student Task

1. Explain what IP fragmentation is and why PPPoE's MTU matters here.
2. Explain what PMTUD is supposed to do, and why it fails silently through
   this firewall.
3. Propose **two candidate fixes** with their tradeoffs (e.g., MSS clamping
   vs raising PMTUD/ICMP handling).

## How to Approach This (Reasoning Scaffold)

- Trace one downstream packet's size budget: 20B IP + 20B TCP + payload ≤ 1492.
- The capture shows frag only on the *inbound* leg — ask what device on that
  path cannot send ICMP "frag needed" to the server.
- "ICMP is noise" is the default folklore; test that belief here.

## CLO Mapping

- **CLO-1** — Protocol mechanics to diagnose availability/correctness problems.

## Safety Notes

- Simulated capture; no real network was involved.
- Real-world equivalent: diagnosis only, on links you administer.
