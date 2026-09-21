# cs-088 — Data Science Infrastructure: Scoping a GPU Cluster Intrusion

> **Simulated scenario.** The cluster, intrusion, and telemetry are fictional.

## Difficulty & Domain

- **Difficulty:** Expert · **Domain:** Data Science infrastructure security · **CLO:** CLO-11, CLO-12
- **Est. time:** 15 minutes · **Anchor:** L26 (Detection, Triage & Containment)

## Scenario

A research-lab GPU cluster runs training jobs for 30 data scientists.
Monitoring caught cryptomining on one GPU node. The PI wants the
cluster *cleaned quietly* ("just reimage that node, don't scare the
funders"); the security team suspects the intrusion is wider —
training data and model checkpoints are the real crown jewels, and
the cluster shares credentials with the data lake. Scope it honestly:
what is compromised, what is at risk, and what does containment cost
the research mission?

## Stakeholders

- **PI (research lead)** — mission continuity; funder optics.
- **Security (you)** — honest scope; data-lake exposure is the fear.
- **30 data scientists** — jobs interrupted; credentials on nodes.
- **Funder/compliance** — dataset governance commitments.

## Network Context

- GPU nodes: SSH-accessible, shared user accounts for convenience
  ("lab" account), home dirs on NFS.
- Data lake: S3-style object store, credentials cached in home dirs
  (`~/.aws`, dataset tokens) — read-mostly, one write path for
  results.
- Scheduler: jobs run as the shared account; no per-job isolation.
- Telemetry: scheduler logs, NFS server logs, object-store access
  logs (90-day), no EDR on GPU nodes.

## Available Evidence

| T | Event |
|---|---|
| Day 0 02:10 | SSH brute-force on lab account from off-campus IP (firewall) |
| Day 0 02:40 | lab-account login succeeds (auth log) |
| Day 0 03:00 | cryptomining process on gpu-07 (monitoring) |
| Day 0 03:05–now | gpu-07 to mining-pool endpoints (flow, sustained) |
| Day 0 03:20 | `~/.aws` read on gpu-07 via NFS — *indistinguishable from researcher activity* (NFS logs) |
| Ongoing | object-store logs: no anomalous large reads *yet* |

## Student Task

1. State the **scope hypothesis**: which assets are compromised vs
   exposed, with the evidence for each (and the uncomfortable
   "cannot-determine" items).
2. Answer the **PI's request**: is "reimage gpu-07 quietly" acceptable
   — and what *specifically* does it leave unresolved?
3. Design the **containment that preserves research**: sequence
   actions so the cluster stays partially productive (which nodes,
   which accounts, what gets rotated first).
4. Answer the **credential-blast-radius question**: what does the
   `~/.aws` read mean given it's indistinguishable from normal use —
   and what control would have made it distinguishable?

## How to Approach This (Reasoning Scaffold)

- Shared-account + shared-credential design converts one node
  compromise into an *identity* problem — the blast radius is the
  credential's, not the node's.
- "Quiet cleanup" fails when credentials may be stolen: reimages
  don't revoke tokens.
- Indistinguishability is a telemetry failure, not an unknown — the
  fix is attribution (per-job identity), not more alerts.

## CLO Mapping

- **CLO-11** — Scoping and containment in research infrastructure.
- **CLO-12** — Reasoning about ambiguous evidence.

## Safety Notes

- Simulated; cryptomining discussed as detection evidence, no
  mining deployment steps.
