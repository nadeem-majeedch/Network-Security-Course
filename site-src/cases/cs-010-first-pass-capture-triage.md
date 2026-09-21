# cs-010 — First-Pass Triage of an Unfamiliar Capture

> **Simulated scenario.** The capture summary, hosts, and findings are fictional.

## Difficulty & Domain

- **Difficulty:** Beginner · **Domain:** TCP/IP protocol analysis · **CLO:** CLO-1
- **Est. time:** 10 minutes · **Anchor:** L04 (Applied Packet Analysis & Web Protocols)

## Scenario

A colleague hands you a 10-minute capture from an office access-layer switch
(SPAN port) saying "something felt slow this morning, here's a capture, tell
me if anything's wrong." No other context. You have 5 minutes and a
protocol-summary sheet (below). Your job is a **triage verdict** with
priorities — not a full analysis.

## Stakeholders

- **Colleague** — wants a quick verdict on whether "slowness" is security-relevant.
- **IT manager** — decides whether to open an incident ticket.
- **You** — must defend whatever you prioritize with only the evidence given.

## Network Context

- Office VLAN, 60 users, normal business apps: web, mail, VoIP, file shares.
- Baseline profile: ~70% of bytes are HTTPS to a small set of SaaS destinations;
  DNS < 2% of packets; VoIP to two known session-border controllers.

## Available Evidence

Protocol summary of the 10-minute capture:

| Metric | Observed | Baseline |
|---|---|---|
| Total bytes | 6.1 GB | ~2 GB per 10 min |
| HTTPS share | 55% | 70% |
| HTTP (plaintext) share | 18% | 3% |
| DNS packets | 41% of packet count | <2% |
| Distinct DNS query names | 1,412 | ~180 |
| Longest DNS name length | 189 chars | 31 chars |
| NTP | 0.1% | 0.1% |
| VoIP (SIP/RTP to SBCs) | 2% | 8% |
| Top talker | one workstation, 2.9 GB | (none dominant) |

## Student Task

1. Rank the **three anomalies** that most deserve analyst attention, ordered,
   each with the observation that triggered it.
2. For your #1: name the two most likely explanations and state the single
   next evidence item that would discriminate between them.
3. Give your verdict: security incident, misconfiguration, or "insufficient
   evidence" — with your top reason.

## How to Approach This (Reasoning Scaffold)

- Triangulate anomalies: an outlier is stronger if two metrics move together.
- 41% of *packets* vs 6% of *bytes* is not a contradiction — think packet sizes.
- Very long DNS names at volume is a pattern worth memorizing for the whole course.

## CLO Mapping

- **CLO-1** — Triage reasoning over protocol summaries.

## Safety Notes

- Simulated capture summary; analysis is paper-only.
