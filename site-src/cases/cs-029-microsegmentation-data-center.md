# cs-029 — Microsegmentation Concept for a Data Center

> **Simulated scenario.** The DC, workloads, and flows are fictional.

## Difficulty & Domain

- **Difficulty:** Intermediate · **Domain:** Network segmentation · **CLO:** CLO-3
- **Est. time:** 12 minutes · **Anchor:** L09 (Defense in Depth & Network Segmentation)

## Scenario

A SaaS company's data center runs 400 VMs on 3 clusters. East-west traffic
is flat-allowed: any VM can reach any VM. A pen test showed
web-app → database-direct and web-app → payroll-server paths that
"shouldn't exist." Leadership approves a microsegmentation project. You must
define the **policy model** (identity-based, not IP-based), the
**enforcement point options**, and the **rollout that doesn't break prod**.

## Stakeholders

- **SRE team** — owns 400 VMs; change fatigue is real.
- **Security** — wants lateral-movement death.
- **Compliance auditors** — PCI scope contains the payment app's cluster.
- **Vendors** — 3 managed service providers have standing access.

## Network Context

- vCenter-based virtualization; distributed switch; NSX-style microseg
  capability exists but is unused; north-south is firewalled already.
- Workload groups: web tier (60), app tier (90), DB tier (40), payment
  cluster (30, PCI), internal tools (80), batch/analytics (100).
- All VMs currently have identical baseline: agents + same local firewall = off.

## Student Task

1. Define the **policy model**: workload *labels/tags* (name ≥6 categories),
   the default policy, and 4 example rules expressed as
   `source-tag → dest-tag, service` (no IPs).
2. Compare **two enforcement points** (distributed hypervisor firewall vs
   central firewall/SDN gateway) for this estate: control granularity,
   failure mode, ops cost. Pick one with justification.
3. Design the **prod-safe rollout**: monitoring-only phase, ring ordering
   (which group first/last), and the PCI cluster's special treatment.

## How to Approach This (Reasoning Scaffold)

- Tag-based policy survives IP changes and autoscaling — that's the entire
  point vs VLAN/ACL thinking.
- Enforcement point choice is about *failure modes*: what happens when the
  policy engine is down or misconfigured?
- Rollout order follows *flow determinism*: appliances/DBs have narrow,
  known flows; desktop-like workloads don't.

## CLO Mapping

- **CLO-3** — Identity-based microsegmentation design.

## Safety Notes

- Design exercise on a fictional estate.
