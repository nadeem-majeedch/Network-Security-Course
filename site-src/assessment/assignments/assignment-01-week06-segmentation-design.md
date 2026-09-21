# Assignment 1 — Segmentation Design Document (Week 6)

> **Weight:** 5% of course grade · **Due:** end of week 6 · **CLO-3**
> **Deliverable:** a design document (6–10 pages) + one network diagram.
> Teams: solo or pairs.

## Scenario (simulated)

A 400-staff professional-services firm runs a flat `10.10.0.0/16`. Assets:
ERP (on-prem), file/print, VoIP, 60 CCTV cameras with vendor cloud access,
a guest Wi-Fi, a small data-science cluster (GPU nodes, dataset storage),
and a building-management system with a vendor remote-access contract.
The CIO wants a segmentation proposal that survives operations: phased,
reversible, evidence-first. (Same design ethos as cs-026, larger estate,
new verticals — do not reuse that solution.)

## Tasks

1. **Zone model** (25): define 5–8 zones with names, subnets/VLANs, and
   default posture. Justify each boundary by *sensitivity + behavior*, not
   org structure. Include the DS cluster and BMS explicitly.
2. **Flow matrix** (25): an initiation matrix (≤15 rows) — zone → zone,
   ports, justification. Everything unlisted is denied. Mark the three
   flows most likely to break and how you'd detect breakage in week one.
3. **Phased rollout** (25): two phases; phase 1 = observe-only with the
   evidence you'd gather (name the telemetry: NetFlow/Zeek, firewall logs)
   and how the real matrix gets built; phase 2 = enforcement by zone risk
   with rollback criteria per step.
4. **Diagram** (15): one diagram showing zones, enforcement points
   (firewall/L3 boundaries), and telemetry tap points.
5. **Tradeoff memo** (10): ≤300 words — what you deliberately did *not*
   segment, the risk accepted, and the pairing control.

## Constraints

- Cite the tradeoffs using course vocabulary (default-deny, east-west,
  blast radius) — vendor marketing language is penalized.
- The BMS vendor remote-access path must appear in your matrix with its
  risk noted — it is this assignment's trap.

## Submission

PDF (or repo Markdown) + diagram source. Rubric: see the grading scheme
distributed with feedback (instructor materials).
