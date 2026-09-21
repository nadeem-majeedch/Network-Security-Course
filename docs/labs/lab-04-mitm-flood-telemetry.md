---
lab: Lab-04
title: MITM & Flood Telemetry Analysis
week: 4
module: 2
clos: [CLO-2]
lectures: [L07, L08]
duration: 2h (embedded in lecture block)
status: complete
artifact-type: student-lab-handout
instructor-key: teaching/lab-answer-keys/lab-04-answer-key.md
---

# Lab-04 — MITM & Flood Telemetry Analysis

## 1. Lab Overview & CLO Mapping

L07/L08 covered session and availability attacks; this lab reads their
*telemetry* from evidence: a SYN wave that never completes, amplify-shaped UDP
pairs, and downgrade-exposed web traffic. You compute the arithmetic (amplification
factors, connection-table pressure) that makes these attacks cheap. *CLO-2* —
classify threats and map them to exploited positions. Reference lectures:
L07 (sniffing/MITM/session), L08 (DoS/DDoS).

## 2. Learning Objectives

By the end you can: (1) identify an incomplete-connection flood from flow/frame
evidence and quantify its rate; (2) compute an amplification factor from request/
response sizes and explain what enables reflection; (3) read cleartext-vs-TLS
session differences and state what an unencrypted first hop exposes; (4) match
each observed pattern to its layer-appropriate mitigation; (5) bound your
conclusions to the evidence window.

## 3. Prerequisites

Lab-03 submitted; L07/L08 attended; datasets verified.

## 4. Estimated Duration

120 minutes: verification 5 · flood analysis 35 · amplification math 30 ·
MITM/web exposure 25 · write-up 25.

## 5. Required Software & Hardware

- Lab-range VM with Wireshark ≥ 4.0, Python 3.11+.
- Datasets: `lab04-mitm-flood.pcap` (202 packets), `lab02-normal-traffic.pcap`
  (comparison baseline).

## 6. Setup Instructions

> **Command status:** ✅ verified at authoring time; ⚠️ reference shape.

1. ✅ Verify: `cd docs/labs/datasets && sha256sum -c SHA256SUMS`
2. ⚠️ Open `lab04-mitm-flood.pcap`. Starter filters:

```
tcp.flags.syn == 1 && tcp.flags.ack == 0 && !tcp.flags.fin    # SYNs
tcp.flags.syn == 1 && tcp.flags.ack == 0 && tcp.dstport == 443
udp && data.len > 800                                          # big replies
udp.srcport == 53                                              # DNS-source UDP
```

3. ⚠️ Rate math (spreadsheet or Python): packets per second = count / window
   observed; state the window you measured, never assume.

## 7. Authorization & Safety Notes

- **Authorization basis:** all analysis is confined to the instructor-authorized lab range and the pinned course datasets; anything outside that boundary is prohibited.

- Evidence analysis only. Do not generate floods or spoofed traffic on the range
  or any network — instructor demos handle active technique; your job is
  detection and arithmetic.
- All external IPs in the datasets are documentation ranges (TEST-NET) — no
  real systems are contacted by this evidence.

## 8. Student Tasks

1. **SYN wave:** count SYNs to 10.20.30.10:443, measure the window (first/last
   frame time), compute SYNs/sec, count completed handshakes (expect 0).
   Which side is spoofed, and what in the frame pattern supports that?
2. **Backlog arithmetic:** assume a listen backlog of 128 and 60 s half-open
   timeout. At your measured rate, how long to exhaust it? What does the
   *server* experience, and what does a legitimate user see?
3. **Amplification math:** for the UDP pairs, compute response/request size
   ratio; state the query type (255 = ANY) and why that qtype is toxic. Who is
   the real target of each pair — the resolver or the victim? Why does this
   require source spoofing, and why can't TCP be reflected this way?
4. **Web exposure:** using `lab02-normal-traffic.pcap` as the baseline, list
   every cleartext-visible field in the HTTP conversation (host, path, user
   agent, body). What *metadata* would still be visible if the same session
   used TLS (SNI, IPs, sizes, timing)?
5. **Mitigation mapping:** for each pattern, name the layer-appropriate control
   (SYN cookies/backlog tuning/upstream filtering vs BCP 38/Response Rate
   Limiting/ANY-rate limits vs TLS-everywhere + HSTS) and where it must sit.
6. Write two findings (evidence → assessment → recommendation), each bounded by
   its measurement window.

## 9. Expected Observations

- 120 SYNs to :443 from rotating 198.51.100.x sources, no SYN/ACKs back —
  spoofed-source one-way traffic.
- 40 pairs: ~34-byte ANY queries; ~950+ byte responses; request from spoofed
  sources, reply *to* 10.20.0.101 — reflection with amplification ≈ 28×.
- Baseline HTTP: full header visibility; the contrast defines "what TLS fixes".

## 10. Analysis Questions

1. Why do spoofed SYNs have no completions? What would an attacker need to see
   replies (and why would that reveal them)?
2. SYN cookies trade what for what? Name one thing the server no longer
   remembers during a cookie-mode SYN flood.
3. Response Rate Limiting (RRL) on an authoritative resolver trades false
   negatives for protection — explain the trade-off in your own words.
4. BCP 38 (ingress/egress filtering) is "the" structural fix — at whose border
   must it be deployed to actually stop reflection, and why does global
   adoption lag?
5. Your measured amplification is ~28× from a synthetic dataset. What is the
   danger of publishing that number without its measurement context?

## 11. Troubleshooting

- "SYNs/sec differs from my neighbor's" → different measurement windows; both
  can be right — report the window.
- UDP replies look truncated → snaplen limits; the dataset is complete, check
  you opened the right file.
- Confusing query vs reply direction → resolver is 10.20.30.53; follow the
  source/dest of the 53/53 pair carefully (reflection makes it non-obvious).

## 12. Cleanup Instructions

- Export annotated copies; remove scratch; VM logout; originals read-only.

## 13. Submission Requirements

- `lab04-annotated.pcapng` with the two patterns marked.
- Rate + backlog worksheet (measured window stated).
- Amplification table (query bytes, response bytes, ratio).
- Mitigation mapping table (pattern → control → placement).
- Two findings + analysis answers (5). Due: start of Week 5 session.

## 14. Expected Output & Evidence

| Artifact | Passing evidence |
|---|---|
| Annotated capture | both patterns bookmarked with counts labeled |
| Worksheets | every rate/ratio carries its measurement window |
| Mapping | layer-correct controls (SYN cookies ≠ L7 rate limit) |
| Findings | bounded claims; no invented totals |

## 15. Grading Rubric

| Criterion | Weight | Full-credit behavior |
|---|---|---|
| Evidence discipline | 40% | measured windows stated; arithmetic shown |
| Mechanism accuracy | 30% | spoofing/reflection/backlog mechanics correct |
| Analysis depth | 20% | trade-off nuance (cookies, RRL, BCP 38 adoption) |
| Safety & policy | 10% | analysis-only posture stated and kept |

## 16. Instructor Answer Key

Model answers, worked arithmetic, common errors:
`teaching/lab-answer-keys/lab-04-answer-key.md` (instructor-only).
