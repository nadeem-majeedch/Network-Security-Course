# Lab-05 — Segmentation & Proxy Egress Design

## 1. Lab Overview & CLO Mapping

Modules 1–2 gave you the attacker's map; this lab is your first design
deliverable: segment the course's fictional company (**Meridian Lab Supplies**
— 180 staff, warehouse OT, e-commerce site, and a flat network that suffered a
lateral-movement incident) and design its egress policy through an explicit
proxy. *CLO-3* — design segmented, defense-in-depth architectures satisfying
stated requirements and trade-offs. Reference lectures: L09 (defense in depth,
zero trust), L12 (NAT, proxies, egress, NAC).

## 2. Learning Objectives

By the end you can: (1) partition a flat network into zones with documented
trust levels and enforcement points; (2) design an egress allow-list and
justify every allow by business function; (3) specify DHCP-snooping/DAI and
802.1X placements from Lab-03's lessons; (4) articulate residual risks a design
accepts; (5) present the design as a defensible diagram + policy tables.

## 3. Prerequisites

Labs 01–04 submitted; L09/L12 attended; Lab-03 findings (they seed this design).

## 4. Estimated Duration

120 minutes: requirements walkthrough 15 · zone design 40 · egress policy 35 ·
peer review 20 · final edits 10.

## 5. Required Software & Hardware

- Diagram tool (draw.io) or paper + scan; no range infrastructure needed.
- Lab-03 findings and Lab-01 baseline as inputs.

## 6. Setup Instructions

> **Command status:** design lab — no commands; ✅/⚠️ n/a.

1. Read the Meridian brief (below) and list every stated constraint.
2. Open the flat-network starting diagram (on the lab sheet): one /16, three
   switches, no VLANs, default-gateway-only egress.

**Meridian brief (constraints you must satisfy):** e-commerce web tier must be
internet-reachable; warehouse scanners use legacy software on a flat LAN;
corporate staff need SaaS + web; finance PCs handle card data (PCI scope);
printers/IoT are unmanaged; management of switches/servers must not be
reachable from user space; egress currently default-allow (post-incident
finding: C2 beaconed out for 3 weeks undetected).

## 7. Authorization & Safety Notes

- **Authorization basis:** a design exercise only — no live systems; but designs must include their own authorization/verification hooks to be acceptable.

- Paper/design exercise — no live systems. Still binding: designs must include
  the *authorization/verification* hooks (who tests the egress allow-list, how)
  or they are fiction.

## 8. Student Tasks

1. **Zone design:** define ≥5 zones (internet, DMZ, corporate, OT/warehouse,
   management; servers optional), assign the brief's assets, and draw
   enforcement points (firewall/ACL/NAC) on every inter-zone path. For each
   boundary: what is inspected, what is blocked by default?
2. **Egress policy through an explicit proxy:** draft an allow-list table —
   business function, destinations (categories/FQDNs), protocol/ports, which
   zone may use it, logging level. Default-deny everything else; state where
   DNS goes (internal resolvers + DoT optional) and why.
3. **L2 hygiene:** from Lab-03 evidence, specify DHCP-snooping/DAI, port
   security, and 802.1X/MAB placements (which ports, which trust).
4. **Residual risk:** name ≥3 risks the design still accepts (e.g., OT legacy
   software needing flat access) and their compensating monitoring.
5. **Verification hook:** define how each control would be *tested* (one test
   per control) — this becomes Lab-06's audit mindset.
6. Peer review: exchange designs; attack one another's egress tables ("what
   business function breaks?", "what tunnels through 443?").

## 9. Expected Observations

- The default-allow egress is what let the beacon run 3 weeks — your allow-list
  plus proxy logging is the direct answer; **egress logs feed detection** (L21).
- Scanners' legacy constraint is best answered by a constrained OT zone with
  protocol-specific allows, not by keeping the flat LAN.
- Management reachability is the classic forgotten boundary — jump-host
  patterns only, no user-VLAN routes.

## 10. Analysis Questions

1. Which zone trusts which, and what single sentence defines each trust
   boundary's policy?
2. The proxy adds inspection and policy — what does it *cost* (latency, privacy,
   TLS-inspection limits, bypass temptation)? Name two failure modes of an
   explicit proxy design.
3. Justify: why is "block everything except 443" not a sufficient egress policy
   by itself?
4. Where does microsegmentation (per-workload policy) beat VLAN zoning on this
   estate, and where would it be overkill?
5. The incident's beacon cadence was visible in DNS logs that nobody shipped
   anywhere. Which pipeline decision (L21 forward-look) would have caught it,
   and where does your design state that?

## 11. Troubleshooting

- Design bloat (10+ zones) → merge by trust level; a zone nobody can articulate
  a policy for is not a zone.
- Egress table with "allow all HTTPS" rows → split by business function; the
  FQDN/category column is where the value lives.
- Peer review gone personal → review the table, not the author; findings as
  questions ("what breaks?"), per manual §1 moves.

## 12. Cleanup Instructions

- Archive your design (PDF + editable source) to your course folder; nothing on
  shared desktops. No range state to clean.

## 13. Submission Requirements

- Zone diagram (PDF) with enforcement points and trust labels.
- Egress allow-list table + default-deny statement.
- L2-hygiene placement table; residual-risk list (≥3) with monitoring hooks.
- Verification-hook tests (one per control).
- Peer-review notes (what you attacked, what changed).
- Due: start of Week 6 session (feeds Assignment 1).

## 14. Expected Output & Evidence

| Artifact | Passing evidence |
|---|---|
| Diagram | ≥5 zones, every inter-zone path has a named enforcement point |
| Egress table | every allow has business justification; default-deny explicit |
| Hygiene table | ports/trust directions named (snooping trust ≠ access port) |
| Residual risks | honest accepted risks with monitoring, not "none" |

## 15. Grading Rubric

| Criterion | Weight | Full-credit behavior |
|---|---|---|
| Evidence discipline | 40% | design decisions traceable to brief constraints + Lab-03 findings |
| Mechanism accuracy | 30% | controls placed at correct layers/points |
| Analysis depth | 20% | trade-offs + residual risks articulated |
| Safety & policy | 10% | verification hooks present; authorization mindset |

## 16. Instructor Answer Key

Reference design, egress-table exemplar, review guidance:
`the instructor answer-key collection (not published)` (instructor-only).
