---
case: cs-097
title: Multi-Source Timeline Correlation — Logs, Flows, and PCAP
difficulty: expert
domain: Network forensics
module: 8
lecture-anchor: L30
clos: [CLO-14, CLO-15]
time-estimate: 25 min (5 min reasoning + 20 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-097-solution.md
---

# cs-097 — Multi-Source Timeline Correlation: Logs, Flows, and PCAP

> **Simulated scenario.** The intrusion, estate, and telemetry are fictional.

## Difficulty & Domain

- **Difficulty:** Expert · **Domain:** Network forensics · **CLO:** CLO-14, CLO-15
- **Est. time:** 25 minutes · **Anchor:** L30 (Advanced Forensics & Reporting)

## Scenario

The final capstone forensics case: an intrusion into Meridian's
analytics platform produced three partial telemetry sets from three
teams, each with a different clock, granularity, and blind spot:
**host logs** (per-second, app-level), **flow records** (5-min
aggregates, network-level), and a **full PCAP** of one critical
30-minute window. Legal needs a single defensible timeline.
The discipline: correlation across granularity and clock skew, with
confidence labels — and a report shaped for an audience that was
not in the room (the cs-087 single-estate version, now across three
*incompatible* sources).

## Stakeholders

- **IR/forensics (you)** — timeline author.
- **Legal** — defensibility: provenance + confidence per entry.
- **NetOps** — owns flow data; resists "your data is wrong" claims.
- **Platform team** — owns host logs; alarmed by what they show.

## Network Context

- Sources: (1) app host logs, NTP-synced (±50 ms); (2) NetFlow v9,
  5-min aggregation, router clock +3.5 min skew; (3) PCAP, sensor
  clock −40 s skew, 30-min capture window only.
- The event: unauthorized data export from the analytics platform
  over ~6 hours; the PCAP covers the *peak* window only.
- Export size: 2.1 GB total; PCAP window shows 640 MB of it.

## Available Evidence

| T (approx) | Host log (NTP) | Flow (router +3:30) | PCAP (sensor −40 s) |
|---|---|---|---|
| ~13:00 | export job created by svc_analytics | — | — |
| ~14:10 | auth anomaly: svc_analytics from new host | 14:13 flow pair to new external | — |
| ~15:45–16:15 | export peak (800 MB logged) | 15:48–16:18 egress spikes (810 MB) | 15:44:20–16:14:40 full session, 640 MB |
| ~17:30 | log source goes quiet (agent stopped) | flows continue to 18:05 | — |
| ~18:05 | — | final egress burst (290 MB) | — |

## Student Task

1. Build the **normalized timeline**: align the three clocks (state
   each skew and how you derived it), reconcile the 800 vs 810 MB
   and the 2.1 vs 640 MB accounting, and tag each entry with its
   sources and confidence.
2. Answer the **agent-stop question**: the host agent goes quiet at
   ~17:30 while flows continue to 18:05 — what are the three
   candidate explanations, which does the evidence favor, and what
   *cannot* be concluded about 17:30–18:05?
3. Make the **volume accounting**: 2.1 GB total claimed, 810 MB
   peak-window (host) vs 810 MB (flow) vs 640 MB (PCAP) — produce
   the reconciliation table and state what the PCAP *adds* beyond
   volume (the three things only packet data proves).
4. Draft the **legal-ready finding**: one paragraph, provenance
   citations, confidence labels, explicit unknowns — the format
   survives cross-examination.

## How to Approach This (Reasoning Scaffold)

- Clock skew is derived, not assumed: find an event visible in two
  sources (the 15:45 peak) and measure the offset — 3:30 and 40 s
  are *derivations* you must show.
- Granularity differences are not contradictions: 5-min flow
  buckets can't timestamp to the second; the timeline records
  *each source at its native resolution* — precision is per-source,
  never inflated.
- The PCAP's value is not volume: it's content proof (what
  protocol, what data shape, whether encryption, session
  boundaries) — the three things logs can never show.

## CLO Mapping

- **CLO-14** — Forensic evidence handling and reporting.
- **CLO-15** — Capstone synthesis across telemetry domains.

## Safety Notes

- Simulated; forensic methodology only.
