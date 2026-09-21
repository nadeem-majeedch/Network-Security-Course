---
case: cs-023
title: Botnet C2 Beacon Pattern Recognition
difficulty: intermediate
domain: Network security principles
module: 2
lecture-anchor: L08
clos: [CLO-2]
time-estimate: 12 min (5 min reasoning + 7 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-023-solution.md
---

# cs-023 — Botnet C2 Beacon Pattern Recognition

> **Simulated scenario.** The clinic group, hosts, and flows are fictional.

## Difficulty & Domain

- **Difficulty:** Intermediate · **Domain:** Network security principles · **CLO:** CLO-2
- **Est. time:** 12 minutes · **Anchor:** L08 (DoS, DDoS & Infrastructure Abuse)

## Scenario

A dental-clinic group's IT contractor notices one front-desk PC uploading
"some data" nightly. There's no IDS; the firewall can export flow records,
which you now have for three nights. The clinics handle patient records
(covered by health-privacy rules in their jurisdiction). Decide what the PC
is doing and what tonight's action is.

## Stakeholders

- **Patients** — data confidentiality.
- **Clinic owner** — regulator notification exposure.
- **IT contractor** — first responder; needs tonight's steps.
- **Compliance consultant** — will judge whether a "breach" occurred.

## Network Context

- 3 clinics; flat small networks; central firewall with flow export;
  workstations run AV only (no EDR).
- Outbound web is allowed; no egress categories; DNS via ISP resolvers.
- The PC in question (`front-desk-2`) also runs an old Java-based scheduling app.

## Available Evidence

**Flow records, `front-desk-2` → external, three nights (23:40–00:20 window):**

| Night | Sessions | Bytes up | Remote IP:port | Timing | Notes |
|---|---|---|---|---|---|
| N1 | 14 | 22.4 MB | 45.33.x.x:443 | every ~4 min, 23:41→00:05 | TLS, avg 1.6 MB/session |
| N2 | 14 | 22.9 MB | same IP:443 | every ~4 min, 23:44→00:04 | same shape |
| N3 | 14 | 6.1 MB | **different IP, same /24** | every ~4 min | shorter, partial |
| All | — | — | — | jitter ±30 s | starts ~23:40 nightly |

DNS: the TLS destinations were reached via `cdn-metrics.example-ads.com`
(resolves to both IPs); the hostname is new this month. The PC also
"updates" the scheduling app at 23:30 nightly (vendor endpoint, legit).

## Student Task

1. Classify the traffic: beacons to C2, scheduled legitimate upload, or
   exfiltration-in-progress? Cite which flow features discriminate.
2. The vendor's 23:30 "update" is legitimate. Explain how malware rides
   *adjacent* to legitimate nightly jobs, and what this implies for the
   containment time you choose.
3. Give tonight's containment sequence (host + network) and the one
   evidence-preservation step most teams skip.

## How to Approach This (Reasoning Scaffold)

- Legit nightly jobs are also periodic — periodicity alone doesn't convict.
  What convicts: *remote-IP rotation within a /24, volume unrelated to the
  job's purpose, TLS to a brand-new metrics domain*.
- 22 MB nightly from a front-desk PC with a scheduling app — ask what the
  job's purpose could *plausibly* upload. If nothing fits, the purpose is
  the attacker's.
- Containment choices trade evidence against ongoing harm — pick a time and
  defend it.

## CLO Mapping

- **CLO-2** — Beacon/exfil pattern recognition and first-response choices.

## Safety Notes

- Simulated incident. No reverse-engineering or malware-execution is asked
  for; the response is defensive containment.
