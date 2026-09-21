---
case: cs-026
solution-for: modules/module-03-secure-architecture/case-studies/cs-026-flat-network-segmentation-proposal.md
difficulty: intermediate
module: 3
lecture-anchor: L09
clos: [CLO-3]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-026 Solution — Segmentation Proposal (INSTRUCTOR ONLY)

## Model Solution

**Zone model (7 zones, default-deny between):**

| Zone | VLAN (new) | Members | Default posture |
|---|---|---|---|
| CORE-SERVERS | 100 | ERP, PBX | deny-in except listed flows |
| SCANNERS | 110 | warehouse scanners | egress ERP:5010 + vendor-update only |
| VOICE | 120 | phones | egress PBX (SIP/RTP) + NTP |
| WORKSTATIONS | 130 | employee PCs | egress proxy/ERP client flows; no peer-to-peer |
| OT-BMS | 140 | building controls | egress vendor cloud + facilities workstation only; no lateral |
| PRINT | 150 | printers | ingress from WORKSTATIONS (IPP/9100) |
| GUEST | 160 | guest Wi-Fi | internet only (unchanged) |

**Flow matrix (allow-list; everything else denied):**

| From | To | Ports | Notes |
|---|---|---|---|
| WORKSTATIONS | CORE-SERVERS | ERP client (e.g., 443/1500) | user apps |
| SCANNERS | CORE-SERVERS | TCP 5010 | scanner→ERP only |
| SCANNERS | Internet (vendor) | 443, monthly window | or proxy via allow-list |
| VOICE | CORE-SERVERS (PBX) | SIP 5060 + RTP range | trunk stays at firewall |
| FACILITIES-WS (subset of WORKSTATIONS) | OT-BMS | BMS protocol | 1 host only |
| OT-BMS | Internet (vendor) | 443 | pinned domains |
| WORKSTATIONS | PRINT | IPP/9100 | |
| All | Internet | via proxy | existing |

**Two-phase rollout (the graded core):**

*Phase 1 — observe (6–8 weeks, zero enforcement):*
- Implement VLANs and *log* inter-zone flows (core-switch flow export /
  firewall deny-with-log rules in monitor-only mode). Build the **real**
  matrix from data; reconcile against the proposal above; publish diffs to
  app owners ("we saw your scanner fleet also talk to X — expected?").
- Collect ≥ one full business cycle (month-end batch jobs, weekly vendor
  windows) before declaring the matrix stable.

*Phase 2 — enforce (by zone risk):*
- Enforce in order: **OT-BMS → SCANNERS → VOICE → PRINT → WORKSTATIONS**
  (appliance zones first: deterministic flows, easy rollback; workstation
  zone last: most variable).
- Rollback = per-zone enforcement toggle (policy, not cable pulls). Ticket
  triage: first 48 h staffed for misdirected flows.

**The two flows most likely forgotten:**

1. **Facilities workstation → BMS** — everyone segments BMS as "isolated"
   and then the facilities team can't do their job; the miss usually surfaces
   as *violence against the project* (BMS vendor escalates) or a hidden
   4G router plugged into the BMS rack. Consequence: safety-relevant systems
   go unmanaged on a shadow network.
2. **Scanner fleet's vendor-update window** — monthly, easy to miss in a
   2-week observation window; enforcement day = 200 scanners brick their
   update check, vendor blames network, project loses credibility.
   Consequence: enforcement rollback, "segmentation doesn't work" folklore.

## Alternative Solutions

- **Microsegmentation/host-firewall-first:** valid for the server tier;
  as the *only* phase-1 move it misses the appliance zones (no host
  firewalls on scanners/BMS). Combine: host-firewall pilots on ERP/PBX.
- **Three phases (add "pilot one zone")** — better change management,
  longer timeline; credit if the pilot zone is SCANNERS with a rollback drill.
- **NGFW-based zones instead of core-router ACLs:** gives app-aware policy
  and better logs; costs refresh capex — acceptable if budgeted, not
  assumed.

## Tradeoffs

- Observation duration vs project momentum: one full cycle is the minimum
  defensible; month-end batch is the trap that catches short windows.
- Zone count: 7 is manageable; 12 fragments the matrix and the help desk's
  mental model.
- Default-deny day-one vs phased: phased is the assignment; note that
  GUEST/PRINT enforcement is cheap quick wins that build credibility.

## Common Mistakes

- Matrix built from the inventory *only* (it's a hypothesis, not data).
- Forgetting return-flow semantics when writing inter-zone rules (stateful
  firewall handles replies; core-router ACLs may not).
- Enforcing WORKSTATIONS first (maximum ticket blast radius).
- No rollback mechanism named.

## Instructor Prompts

- "Which zone would you pilot enforcement on, and why that one?"
- "What data proves your matrix is *complete*? (You can't prove a negative —
  how long until 'close enough'?)"
- "Which single flow, if denied silently, would take longest to diagnose?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Observe-then-enforce sequencing; zone risk ordering |
| Technical accuracy | 25% | Flow matrix + stateful/ACL semantics correct |
| Alternatives considered | 20% | Microsegmentation/NGFW options weighed |
| Communication | 15% | Matrix + phase table readable as a proposal |

**Timing:** reveal at 5:00 + 2; the "prove the matrix is complete" prompt is
the epistemology lesson of the case.

## CLO Mapping

- **CLO-3** — Defense-in-depth segmentation design with operational realism.
