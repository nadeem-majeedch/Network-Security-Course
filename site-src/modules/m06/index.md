---
status: complete
artifact-type: module-overview-page
module: 6
instructor-only: false
---

# Module 6 — Detection, Monitoring & Vulnerability Management

**Lectures:** L21–L24 (Weeks 11–12) · **CLOs:** CLO-8, CLO-9, CLO-10 · **Cases:** cs-068–078

*Descriptive orientation. Detection engineering uses prepared traffic and the
lab sensor; vulnerability scanning targets lab systems you are explicitly
authorized to scan.*

## What this module covers

Prevention fails eventually; detection is what bounds the damage. You build
the monitoring foundations (logs, flows, PCAP), engineer and tune IDS/IPS
signatures, add behavioral analytics with Zeek, and close the loop with a
disciplined vulnerability management cycle.

## Lectures

| # | Lecture | Core idea |
|---|---|---|
| L21 | [Monitoring Foundations](../../lectures/lecture-21-monitoring-foundations.md) | Telemetry types, sensor placement, log pipelines, coverage mapping |
| L22 | [IDS/IPS — Signatures & Tuning](../../lectures/lecture-22-ids-ips-signatures-tuning.md) | Signature anatomy, false-positive economics, tuning workflow |
| L23 | [Zeek & Anomaly Detection](../../lectures/lecture-23-zeek-anomaly-detection.md) | Zeek logs, conn/HTTP/DNS analytics, baselining behavior |
| L24 | [Vulnerability Management Cycle](../../lectures/lecture-24-vulnerability-management-cycle.md) | Scan → CVSS + context → remediation → verification |

## Labs

[Lab-11](../../labs/lab-11-flow-collector-suricata.md) (flow collector + Suricata
ruleset) and [Lab-12](../../labs/lab-12-zeek-vulnerability-hardening-cycle.md) (Zeek analysis +
vulnerability scan cycle) — lab targets only, documented authorization basis in
each handout.

## Case studies (advanced tier)

cs-068–078: coverage-mapping tradeoffs, alert-tuning backlog prioritization,
anomaly triage from Zeek logs, scan prioritization on patch windows, CVSS
base-vs-environmental debate, remediation SLA design, program metrics review.
See the [case studies guide](../../cases/index.md).

## Skills checkpoints

- Choose sensor placement for a stated detection goal and name the visibility gaps it leaves.
- Read a Suricata rule and predict what traffic it fires on.
- Tune a noisy rule without losing the true positive it was written for.
- Prioritize a scan result set using CVSS + environmental context, and defend the order.
