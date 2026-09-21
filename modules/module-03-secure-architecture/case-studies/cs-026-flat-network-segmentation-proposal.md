---
case: cs-026
title: Segmentation Proposal for a Flat Corporate Network
difficulty: intermediate
domain: Network segmentation
module: 3
lecture-anchor: L09
clos: [CLO-3]
time-estimate: 12 min (5 min reasoning + 7 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-026-solution.md
---

# cs-026 — Segmentation Proposal for a Flat Corporate Network

> **Simulated scenario.** The company, subnets, and applications are fictional.

## Difficulty & Domain

- **Difficulty:** Intermediate · **Domain:** Network segmentation · **CLO:** CLO-3
- **Est. time:** 12 minutes · **Anchor:** L09 (Defense in Depth & Network Segmentation)

## Scenario

A 300-person logistics company runs one flat `10.0.0.0/16` VLAN. After a
near-miss (a laptop got infected, nothing spread, luck), the CIO wants a
segmentation proposal *that survives contact with operations*: it must ship
in two phases with zero workflow breakage promises violated. You have the
application inventory below. Design it.

## Stakeholders

- **CIO** — wants phased, reversible, defensible.
- **Help desk** — will absorb every misdirected flow as a ticket.
- **App owners** — warehouse scanner fleet, ERP, VoIP, building controls.
- **Auditors** — will read the proposal as the new compliance boundary.

## Network Context (application inventory)

| App / asset | Subnet today | Talks to | Sensitivity |
|---|---|---|---|
| ERP (self-hosted) | 10.0.8.5 | all employees' PCs, batch integration from warehouse scanners | High |
| Warehouse scanners (200) | 10.0.20.x | ERP only (TCP 5010), vendor update server monthly | Med |
| VoIP phones (250) | 10.0.30.x | PBX (10.0.8.9), SIP trunk via firewall | Low–Med |
| Employee PCs | 10.0.1–3.x | everything, internet via proxy | Med |
| Building controls (BMS) | 10.0.40.x | vendor cloud + one facilities workstation | High (safety) |
| Guest Wi-Fi | 10.0.50.x | internet only (already isolated) | Low |
| Printers | 10.0.60.x | all PCs | Low |

Existing infra: L3 core switch (VLAN-capable, inter-VLAN routing), one edge
firewall, no host firewalls managed centrally.

## Student Task

1. Propose a **zone model** (names, VLANs, default posture) and the
   **flow matrix** (which zone may initiate to which, on what ports) — at
   most 8 rows in the matrix; everything not listed is denied.
2. Sequence the rollout in **two phases**: what moves first, what evidence
   you gather *before* enforcement (and how — this is the graded core).
3. Name the **two flows most likely to be forgotten** in such projects (use
   the inventory) and the operational consequence of each miss.

## How to Approach This (Reasoning Scaffold)

- Zones follow *sensitivity + behavior*, not org charts — scanners and BMS
  behave like appliances, not like PCs.
- The winning proposals enforce nothing in phase 1: they *observe* (flow
  data/switch NetFlow) and build the real matrix, then enforce deltas.
- Default-deny is the goal; phase it by zone risk, not by alphabetical order.

## CLO Mapping

- **CLO-3** — Defense-in-depth segmentation design with operational realism.

## Safety Notes

- Design exercise; no live systems touched.
