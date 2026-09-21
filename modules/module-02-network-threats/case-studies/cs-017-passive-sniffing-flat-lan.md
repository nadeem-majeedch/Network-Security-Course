---
case: cs-017
title: Passive-Sniffing Exposure Assessment on a Flat LAN
difficulty: beginner
domain: Network segmentation
module: 2
lecture-anchor: L07
clos: [CLO-2]
time-estimate: 10 min (5 min reasoning + 5 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-017-solution.md
---

# cs-017 — Passive-Sniffing Exposure Assessment on a Flat LAN

> **Simulated scenario.** The co-op, protocols, and census are fictional.

## Difficulty & Domain

- **Difficulty:** Beginner · **Domain:** Network segmentation · **CLO:** CLO-2
- **Est. time:** 10 minutes · **Anchor:** L07 (Sniffing, MITM & Session Attacks)

## Scenario

A 40-person software co-op runs one flat switched LAN. A co-founder read that
"anyone on the network can read everything" and wants a straight answer: what
can a rogue laptop plugged into any office port actually *see*? You are given
a protocol census of the office's traffic mix. Your deliverable: an exposure
table with percentages of traffic by exposure class, and the top-3 fixes.

## Stakeholders

- **Co-founder** — wants the myth quantified or debunked.
- **Employees** — their credentials and files are the exposure.
- **Clients** — source code repos and client data move on this LAN.

## Network Context

- Flat switched LAN; a switched network delivers unicast only to the
  destination port (unlike hubs), but broadcasts/multicasts and any flooding
  reach everyone.
- No 802.1X; no NAC; conference-room hub (yes, a literal hub) still in use
  for presentations.
- Remote work: SSH to a code repo server inside the LAN; Git over HTTPS to
  an external SaaS; internal wiki over HTTP (a legacy choice).

## Available Evidence

Protocol census (2-week sample, share of bytes):

| Traffic | Share | Transport/security |
|---|---|---|
| Git over HTTPS to SaaS | 30% | TLS 1.3 |
| Internal wiki | 12% | **HTTP plaintext** |
| SSH to internal repo server | 10% | SSH-2 |
| SMB file shares | 15% | SMB3 signed+encrypted (new servers) / SMB1 (legacy NAS) |
| VoIP (RTP) | 8% | SRTP to SBC, internal leg plaintext RTP |
| Internal DNS | 3% | plaintext UDP/53 |
| Backup job to NAS | 12% | proprietary, unknown encryption |
| Everything else (web, mail SaaS) | 10% | TLS |

## Student Task

1. Build an **exposure table**: for a passive sniffer on any port, classify
   each traffic class as *content-readable*, *metadata-only*, or
   *content-protected*, with the % of bytes in each class and a one-line reason.
2. Name the two **census rows that break the co-founder's "switches make
   sniffing impossible" belief** and explain the mechanism (hint: one is a hub).
3. Give the **top-3 fixes by bytes-protected-per-effort**, ordered, with the
   % of exposed bytes each one closes.

## How to Approach This (Reasoning Scaffold)

- "Switched = safe" is true only for *delivered* unicast; ask what else
  reaches every port (broadcast/multicast/flooding/hub legs).
- Encryption status is per-traffic-class, not per-network — the census *is*
  the security posture.
- Rank fixes by "bytes re-classified per unit of work," not by elegance.

## CLO Mapping

- **CLO-2** — Sniffing exposure quantification and control ranking.

## Safety Notes

- Simulated census; passive analysis concepts taught for defense. Real
  sniffing only on networks you own or are authorized to assess.
