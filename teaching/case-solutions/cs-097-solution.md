---
case: cs-097
title: Multi-Source Timeline Correlation (Solution)
difficulty: expert
module: 8
lecture-anchor: L30
clos: [CLO-14, CLO-15]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-097 — Solution: Multi-Source Timeline Correlation

> **INSTRUCTOR ONLY.** Model solution for cs-097.

## Model Solution

### 1. Normalized timeline (clocks derived, precision per-source)

**Skew derivations:** the 15:45 export peak appears in all three
sources: host 15:45, flow bucket 15:48 (router **+3:30**), PCAP
session start 15:44:20 vs host first-write 15:45:00 (sensor
**−40 s**). Both offsets *derived from a common event*, stated in
the report.

| T (normalized, host-clock) | Event | Sources | Confidence |
|---|---|---|---|
| 13:00 | export job created by svc_analytics | host | Supported |
| 14:10 | auth anomaly: svc_analytics from new host | host | Supported |
| 14:13* | first flow pair to new external (*flow clock normalized) | flow | Supported |
| 15:45:00–16:15:00 | export peak: 800 MB (host bytes-written) | host | Corroborated |
| 15:45–16:18 | egress 810 MB in two 5-min buckets | flow | Corroborated |
| 15:44:20–16:14:40 | PCAP: single TLS session, 640 MB, one external IP | PCAP | Corroborated |
| 17:30 | host agent stops | host | Supported |
| 17:30–18:05 | egress continues, 590 MB across 7 buckets | flow | Supported (host-blind) |
| 18:05 | final burst 290 MB | flow | Supported |

**Volume reconciliation:** 800 MB (host, bytes written by the job)
vs 810 MB (flow, wire bytes incl. TLS overhead) — consistent within
~1%. 2.1 GB total (host job total) vs observed network totals:
peak-window 810 MB + post-agent-stop 590 MB ≈ 1.4 GB *observed
egress*; the remaining ~0.7 GB occurred before the PCAP/peak window
and outside flow scrutiny — **explicit unknown**, with the host log
(2.1 GB written 13:00→17:30) as the bounding claim.

### 2. The agent-stop question (17:30–18:05)

Three candidates:
1. **Attacker stopped the agent** (anti-forensics) then continued
   via a network path — favored: flows continue *unchanged* in
   pattern after agent stop; a legitimate process wouldn't
   correlate with the egress.
2. **Crash/rotation** — possible, but the stop coincides with the
   investigation becoming active (day 2) and the flow continuity
   argues *deliberate* silencing.
3. **Log pipeline failure** — possible; but the flow side
   (independent) shows activity continuing — pipeline failure
   explains log silence, not the egress.

**Cannot conclude:** what *process* moved the 590 MB post-stop;
whether the export continued from the same job or a second
mechanism. Host-blind window: the 590 MB is *network-attributed,
host-unattributed* — say exactly that.

### 3. Volume accounting table + what only PCAP proves

| Metric | Host | Flow | PCAP | Reconciliation |
|---|---|---|---|---|
| Peak-window volume | 800 MB | 810 MB | 640 MB | host≈flow (TLS overhead); PCAP window (30 min) < host window (30 min but offset) → 640 of 800 captured |
| Total | 2.1 GB | ≥1.4 GB observed | 640 MB | 0.7 GB pre-peak: host-attributed only |

**Only packet data proves:** (1) **protocol** — single long-lived
TLS session, not many short ones (shapes the "automated export"
conclusion); (2) **content shape** — payload size/interval
pattern matches bulk file transfer, not beaconing (rules out
alternative explanations); (3) **session boundaries** — exactly
one session, one destination, start/stop to the second (the
flow's 5-min buckets cannot show this, and the defense will ask).

### 4. Legal-ready finding

> "Between 13:00 and 18:05 on [date], the service account
> svc_analytics exported 2.1 GB (±5%, host-measured) from the
> analytics platform to a single external IP. This conclusion
> rests on three independent sources: host application logs
> (NTP-synced), network flow records (router clock, +3:30 skew,
> normalized), and a 30-minute packet capture of the peak window
> (−40 s skew, normalized), which together corroborate the
> volume, destination, and single-session transfer pattern
> (corroborated). The initiating authentication anomaly is
> host-evidenced (supported). Activity between 17:30 and 18:05
> (590 MB) is network-attributed but host-unattributed, as the
> host agent ceased at 17:30 (supported — suspected deliberate).
> Approximately 0.7 GB of transfer predates the peak capture
> window and is host-attributed only. No evidence of a second
> destination was found in any source."

Every clause: source + confidence + boundary. Unknowns stated as
unknowns, not smoothed over.

## Alternative Solutions

- **Reconcile by discarding the flow data** ("PCAP + host is
  enough"): loses the 17:30–18:05 window entirely and the
  total-volume corroboration — the flow data is the *only* source
  spanning the full event.
- **Report un-normalized times** with a caveat: faster, but the
  3:30 skew makes the timeline read as cause-following-effect
  errors — normalization is the report's credibility.

## Tradeoffs

- Per-source precision vs a single clean timeline: honest
  per-source resolution beats falsely uniform timestamps.
- Peak-PCAP-only vs trying to capture more: what's captured is
  what exists — the report's boundary is the capture boundary,
  stated plainly.

## Common Mistakes

- Asserting a single derived skew without showing the common
  event used.
- Treating 640 vs 810 MB as contradiction (it's window math).
- Attributing post-stop egress to a process (host-blind — say
  so).
- Reporting 2.1 GB as network-verified (only 1.4 GB is).

## Instructor Prompts

- "Which single event did you use to derive both skews — and
  could a defense challenge it?"
- "Why is 'network-attributed, host-unattributed' the honest
  formulation for 17:30–18:05?"
- "What would upgrading the finding from 'supported' to
  'corroborated' require for the first two entries?"

## Rubric (10 pts)

| Criterion | Pts |
|---|---|
| Skew derivations shown + normalized timeline with per-source precision | 3 |
| Agent-stop: 3 candidates, favored, explicit unknowns | 2 |
| Volume reconciliation table + 3 PCAP-only proofs | 3 |
| Legal finding: provenance, confidence, boundaries | 2 |

## Safety Notes

- Simulated; no real incident or IOCs.
