---
case: cs-063
title: Overly Permissive Cloud Route/NAT Exposure
difficulty: advanced
domain: Cloud network security
module: 5
lecture-anchor: L19
clos: [CLO-13]
time-estimate: 15 min (5 min reasoning + 10 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-063-solution.md
---

# cs-063 — Overly Permissive Cloud Route/NAT Exposure

> **Simulated scenario.** The VPC, route tables, and incident are fictional.
> Constructs described provider-neutrally.

## Difficulty & Domain

- **Difficulty:** Advanced · **Domain:** Cloud network security · **CLO:** CLO-13
- **Est. time:** 15 minutes · **Anchor:** L19 (Cloud Networking I — VPC Design & Controls)

## Scenario

A data-analytics startup's VPC leaked analytics datasets to a public
bucket *not* through storage permissions but **through the network
path**: a permissive route table + shared NAT design let a compromised
nonprod instance reach, enumerate, and exfiltrate from a "separated"
data subnet. You reconstruct the path, explain why "separate subnet"
was never separation, and redesign routing/egress so the classes are
structurally distinct.

## Stakeholders

- **Startup CTO** — "the bucket was misconfigured" (wrong framing).
- **Security** — the network path was the enabler; controls exist.
- **Data governance** — dataset custody questions.
- **SRE** — nonprod egress convenience must survive the redesign.

## Network Context

```
VPC 10.50.0.0/16
├── nonprod subnets 10.50.10.0/24, 10.50.11.0/24  → RT-A: 0.0.0.0/0 → NAT-GW-1
├── data subnets    10.50.40.0/24                → RT-B: local + 0.0.0.0/0 → NAT-GW-1 (!)
│                                                   (added "for dataset downloads")
├── shared-services 10.50.20.0/24               → RT-A
SGs: everything egress "all" (default); data subnet hosts reachable
     from nonprod because... they're all one VPC with local routes.
Bucket: analytics-exports (public-read via policy error — the noted
     "misconfiguration"), accessed *by name* from nonprod over the NAT
     path (internet egress) OR directly intra-VPC.
```

**Incident:** compromised nonprod CI runner (supply-chain) → enumerated
the bucket via public path *and* the internal dataset host on
10.50.40.15 → 40 GB out through NAT-GW-1 → noticed on the cloud bill.

## Student Task

1. **Reconstruct the exfiltration paths** (two paths — name both) and
   explain why "separate subnet" provided *zero* separation: identify
   which design elements (local routes, shared NAT, default-allow egress)
   made the data subnet an illusion.
2. Rank the **findings** (route/NAT design, egress posture, monitoring
   that found it on the *bill*, the bucket policy's role — is it the
   root cause or a cofactor?).
3. Produce the **redesign**: route tables per class, NAT separation (or
   egress-proxy per class), the data subnet's "no internet, only
   endpoints" pattern, and the *detection* that catches 40 GB next time
   (which metric, what threshold, which alert).

## How to Approach This (Reasoning Scaffold)

- In a VPC, "separation" comes from routes+SGs+egress policy — *never*
  from subnet labels. Walk what a packet actually needs.
- The bill as your IDS is the monitoring finding: flow logs existed?
  NAT metrics existed? Name the detection that should have fired.
- The bucket policy is a cofactor (it made enumeration easy); the
  *path* is the structural finding — fix both, but grade the network
  one.

## CLO Mapping

- **CLO-13** — Cloud routing/egress exposure analysis and redesign.

## Safety Notes

- Simulated incident; standard cloud forensics framing.
