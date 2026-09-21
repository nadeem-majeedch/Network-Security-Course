---
case: cs-063
solution-for: modules/module-05-wireless-cloud/case-studies/cs-063-overly-permissive-cloud-route-nat-exposure.md
difficulty: advanced
module: 5
lecture-anchor: L19
clos: [CLO-13]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-063 Solution — Route/NAT Exposure (INSTRUCTOR ONLY)

## Model Solution

**Path reconstruction (both paths):**

- *Path A — public-bucket path:* compromised CI runner (10.50.10.x) →
  RT-A: 0.0.0.0/0 → NAT-GW-1 → internet → public-read bucket
  (`analytics-exports`) → 40 GB returns through NAT → out. The bucket's
  public-read policy made this trivial; the *egress design* made it
  silent (no egress policy, no per-destination visibility).
- *Path B — intra-VPC path:* same runner → **local route** (every VPC
  has 10.50.0.0/16 → local) → dataset host 10.50.40.15 directly —
  no NAT, no firewall boundary existed between nonprod and data subnets
  (SGs default egress-allow; inbound on the data host evidently allowed
  nonprod sources or was unprotected on the dataset service port).
- *Why "separate subnet" was zero separation:* subnets are addressing
  conveniences; separation is produced by **routes** (the local route
  connects everything in the VPC by default), **security groups** (which
  weren't scoped), and **egress policy** (default-allow). RT-B even
  shared NAT-GW-1 — the "data" class *piggybacked the nonprod egress
  path by design* ("for dataset downloads"), completing the merge: same
  VPC, same egress, same blast radius. The label said data; the packets
  said peers.

**Findings (ranked):**

| Rank | Finding | Mechanism |
|---|---|---|
| 1 | **Shared NAT-GW across classes** | nonprod and data share one egress identity and path — class distinction dies at the NAT; exfil is indistinguishable from normal egress |
| 2 | **No intra-VPC isolation (SG/local-route)** | data host reachable from any VPC host; subnet label ≠ boundary |
| 3 | **Default-allow egress everywhere** | 40 GB out with zero egress-policy friction; no destination allow-listing |
| 4 | **Detection on the cloud bill** | the *only* signal was billing — flow logs/NAT metrics existed but no alert tied egress volume+destination-class to expectation |
| 5 | **Bucket public-read policy** | cofactor, not root cause: it enabled Path A's triviality; even fixed, Path B remains without #1–#3 |

**Redesign:**

| Control | Design |
|---|---|
| **Route tables per class** | nonprod RT: 0.0.0.0/0 → **NAT-GW-nonprod**; data RT: **no internet route at all** — only S3/storage **private endpoints** (dataset sync via endpoint, not public path); shared-services RT: own NAT |
| **Egress proxy per class** (where full egress needed) | nonprod egress via explicit proxy with allow-list (patch registries, package repos); data class never gets one |
| **Intra-VPC isolation** | data subnet: SG ingress from *named producer SGs only* (chaining); nonprod→data denied by default; consider a separate VPC/attachment with restricted peering for the data class (account-level fence — the end-state for regulated data) |
| **SG egress discipline** | nonprod: allow-list (no 0.0.0.0/0 all); data: no internet egress at all |
| **Detection that fires next time** | (a) **VPC flow-log alert**: aggregate bytes-to-internet per subnet-class per hour vs baseline — threshold at, say, 3× class median *or* >5 GB/h from nonprod → page; (b) NAT-GW bytes-out metric per gateway with per-class gateways making the baseline *meaningful*; (c) bucket access-log anomaly (public-path reads from nonprod CIDRs = instant alarm). The bill arrives monthly; the class-baseline alert fires at minute 20. |

## Alternative Solutions

- **"Fix the bucket policy, done":** the CTO framing — leaves Path B and
  the shared-NAT class-merge intact; the next incident uses Path B and
  any *internal* destination.
- **Separate VPC for data immediately:** the strongest structural fix;
  costs peering/endpoint ops — right for regulated datasets; acceptable
  as phase 2 with the SG/RT fixes as phase 1.
- **Egress firewall appliance on the NAT path:** adds inspection/DLP on
  the *nonprod* path; valuable, but the data class's answer is *no
  internet route*, not a better-inspected one.

## Tradeoffs

- Private endpoints vs NAT for dataset sync: endpoints = no public path
  at all (the point), cost per endpoint; NAT keeps habits but keeps the
  path — endpoints win for the data class.
- Class-per-NAT vs one NAT + tagging: per-class gateways make baselines
  and blast radius legible; cost is multiple NAT charges — cheap
  insurance at this scale.
- Alert thresholds vs noise: class-baseline medians adapt; static GB
  thresholds page falsely during legitimate syncs — baseline + sudden
  delta, not absolute size.

## Common Mistakes

- Root-causing to the bucket policy (cofactor) and closing.
- "Separate subnets = separated" (the case's central misconception).
- Detection design as "more flow logs" without the class-baseline alert.
- Forgetting the *intra-VPC* path entirely (the half-reconstruction).

## Instructor Prompts

- "What route-table line best symbolizes the design flaw? Why that one?"
- "Which alert would have fired at minute 20, and with what payload?"
- "Where does 'subnet' earn its keep in cloud security — and where does
  it mislead?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Two-path reconstruction; label-vs-boundary framing |
| Technical accuracy | 25% | Route/NAT/SG/endpoint mechanics |
| Alternatives considered | 20% | Bucket-only framing rejected with reasons |
| Communication | 15% | Findings + redesign table + named alert |

**Timing:** reveal at 5:00 + 10; "the label said data; the packets said
peers" is the landing line.

## CLO Mapping

- **CLO-13** — Cloud routing/egress exposure analysis and redesign.
