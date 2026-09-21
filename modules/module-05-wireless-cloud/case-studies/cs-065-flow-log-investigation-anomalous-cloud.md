---
case: cs-065
title: Flow-Log Investigation of Anomalous Cloud Traffic
difficulty: advanced
domain: Cloud network security
module: 5
lecture-anchor: L20
clos: [CLO-13]
time-estimate: 15 min (5 min reasoning + 10 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-065-solution.md
---

# cs-065 — Flow-Log Investigation of Anomalous Cloud Traffic

> **Simulated scenario.** The cloud estate, flow records, and anomaly are fictional.

## Difficulty & Domain

- **Difficulty:** Advanced · **Domain:** Cloud network security · **CLO:** CLO-13
- **Est. time:** 15 minutes · **Anchor:** L20 (Cloud & Hybrid Assurance)

## Scenario

A cost-anomaly alert led a SaaS company to its flow logs: one compute node
in the data-processing subnet moved 700 GB out over 6 hours, doubling the
month's egress bill. The data-science platform team says "that's the
nightly model-retraining sync." The security team says "prove it." You
have flow records and context; adjudicate.

## Stakeholders

- **DS platform team** — owns the nightly sync; defensive about "false alarm."
- **Security** — adjudicates with evidence, not team reputation.
- **Finance** — wants the anomaly explained or contained.
- **Data governance** — dataset custody if it *is* exfil.

## Network Context

- Subnets: `ds-compute` (GPU nodes), `data-lake` (private endpoints only),
  `corp` (users), `shared` (NAT egress for approved classes).
- Normal nightly sync: ds-compute → data-lake over *private endpoint*,
  60–80 GB, 22:00–01:00, pull-heavy (ingress to ds-compute).
- The anomaly node: ds-compute-07, egress *from* the node → **internet via
  shared NAT** — a path the DS fleet isn't documented to use.

## Available Evidence

**Flow-log summary, ds-compute-07 (6-h window):**

| Period | Direction | Peer | Bytes | Notes |
|---|---|---|---|---|
| 22:00–01:00 | in | data-lake endpoint | 74 GB | matches documented sync profile |
| 01:40–07:30 | **out** | shared-NAT → external IP 185.x.x.x:443 | **700 GB** | steady ~26 MB/s, small flows interleaved with 2 big ones |
| 01:40–07:30 | out | shared-NAT → 4 CDN-ish IPs | 12 GB | chunked |
| 03:10 | out | shared-NAT → unknown IP :53 (DNS) | trivial | — but the node has no documented external DNS use |

Context: node image updated 5 days ago ("new python base image");
credentials: node uses workload identity with read access to the
data-lake *and* (historically granted) a bucket-writer role.

## Student Task

1. **Adjudicate**: benign sync, or exfiltration? Cite the discriminating
   flow features (direction, peer class, timing, the :53 detail). Give
   your verdict with confidence level and what evidence would raise it.
2. Explain the **"it's just the nightly sync" trap**: why the 74 GB
   legitimate ingress makes the 700 GB egress *more* suspicious, not
   less (what does a sync profile predict about egress?).
3. Give the **containment + fix plan** (tonight/this week): what to do to
   the node, the path, and the credential grant — and the *detection*
   that would have fired at 01:45.

## How to Approach This (Reasoning Scaffold)

- The documented sync predicts the *shape*: ingress-heavy, private-peer,
  bounded window. Egress-heavy + internet-peer + post-window = the
  shape's negation, not its continuation.
- The :53 external query from a node with no documented DNS use is small
  and huge at once (C2/bootstrap-class signal).
- Workload identity with an unused bucket-writer role is the classic
  over-grant that turns a node compromise into data loss.

## CLO Mapping

- **CLO-13** — Cloud flow forensics and adjudication.

## Safety Notes

- Simulated flows; investigation framing only.
