---
case: cs-050
title: Site-to-Site IPsec Design Between Two Sites
difficulty: advanced
domain: VPN and secure remote access
module: 4
lecture-anchor: L15
clos: [CLO-7]
time-estimate: 12 min (5 min reasoning + 7 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-050-solution.md
---

# cs-050 — Site-to-Site IPsec Design Between Two Sites

> **Simulated scenario.** The manufacturer, sites, and requirements are fictional.

## Difficulty & Domain

- **Difficulty:** Advanced · **Domain:** VPN and secure remote access · **CLO:** CLO-7
- **Est. time:** 12 minutes · **Anchor:** L15 (IPsec & Legacy VPN Architecture)

## Scenario

A manufacturer must link a factory site (OT/ICS networks) with an R&D site
(simulation clusters). Requirements: engineering traffic only, deterministic
performance for simulation sync, no OT→R&D reachability, and failover if
one of two ISP links drops. Design the IPsec architecture: topology, phase
1/2 parameters, routing/failover, and the OT-isolation guarantee.

## Stakeholders

- **Plant OT team** — deterministic, minimal, auditable.
- **R&D leads** — throughput for simulation sync (large files, nightly).
- **Security** — one-way-ish flow discipline; OT never initiates to R&D.
- **IT operations** — two ISPs, one pair of firewalls; failover must be automatic.

## Network Context

- Factory: OT VLANs (PLCs, historians) + small IT office; firewall FW-A.
- R&D: simulation cluster + office; firewall FW-B.
- Links: ISP-1 (10 Gbps, primary), ISP-2 (100 Mbps, backup) at both sites.
- Traffic classes: (1) R&D↔factory *engineering jump hosts only* (small,
  interactive), (2) simulation-sync (nightly, 200 GB), (3) historian
  read-only replica pull to R&D (allowed one-way).

## Student Task

1. Produce the **architecture table**: tunnels (how many, per link),
   phase-1 and phase-2 parameters (version, crypto, DH, lifetimes, DPD,
   PFS), and routing/failover design (which mechanism, why not another).
2. Enforce the **OT-isolation guarantee**: which selector design + which
   firewall zones make "OT cannot initiate to R&D" structurally true, and
   the one rule that permits the historian replica without breaking it.
3. Address **deterministic performance**: QoS/DSCP over IPsec realities
   (what survives ESP), MTU/MSS specifics for the double-encapsulation
   path, and the sync-window design.

## How to Approach This (Reasoning Scaffold)

- Selector design is the isolation mechanism: narrow phase-2 selectors
  (hosts, not subnets) make the guarantee structural, not procedural.
- Failover: policy-based vs route-based — route-based + dynamic routing is
  the answer for automatic failover; say why policy-based fails here.
- MTU arithmetic: two encapsulations (ESP + underlying tunnels) — compute
  the numbers, don't gesture.

## CLO Mapping

- **CLO-7** — Site-to-site IPsec architecture engineering.

## Safety Notes

- Design exercise; OT/ICS constraints honored (determinism, auditability).
