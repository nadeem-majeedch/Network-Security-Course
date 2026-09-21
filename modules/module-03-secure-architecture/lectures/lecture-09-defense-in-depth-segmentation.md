---
lecture: L09
title: Defense in Depth & Network Segmentation
module: 3
week: 5
hours: 2
clos: [CLO-3]
difficulty: intermediate
status: complete
artifact-type: teaching-plan
---

# L09 — Defense in Depth & Network Segmentation (Teaching Plan)

## 1. Overview & Prerequisites

- **Prerequisites:** L04 (protocol/triage fluency), L08 (why flat networks lose availability battles; where attacker noise comes from). L01 trust-zone inventory reused as design input.
- **Position:** Module 3 opens the defender's architecture arc. Everything here (zones, VLANs, zero trust) is instantiated by L10–L12 controls and reappears in cloud labs (L19–L20) and the capstone design.
- **Faculty prep:** bring two full-bleed topology diagrams (flat office vs segmented campus); prepare the segmentation requirements card deck for the design exercise; queue NIST SP 800-207 zero-trust tenets slide.
- **Common misconceptions:** "VLAN = security boundary"; "one firewall at the edge is defense in depth"; "zero trust means never trust anything, so nothing works."

## 2. Learning Objectives

By the end of this lecture, students can:

1. Explain defense in depth as layered *control classes*, not layered products, and justify layer choices for a given threat (Understand/Evaluate).
2. Design trust zones from data-flow analysis: identify flows, classify assets, assign zones with tiers (Create).
3. Differentiate VLANs (traffic engineering) from security zones (policy enforcement points) and from physical segmentation (Analyze).
4. Sketch DMZ patterns (single/dual firewall, reverse proxy fronting) and state the failure mode each contains (Analyze).
5. Summarize zero-trust tenets (NIST SP 800-207): per-session authentication/authorization, policy decision/enforcement points, and why microsegmentation operationalizes them (Understand).

## 3. Detailed Concepts

### 3.1 Defense in depth, precisely
- Layers: prevention (filters, crypto), detection (IDS/monitoring), response (IR), recovery (backups/HA) — mapped against attack stages (recon → C2 → exfil).
- Redundant, *independent* controls: two controls sharing one failure mode (e.g., same admin console, same trust anchor) are one control.
- Cost/threat matching: controls priced against the model from L05 (minimum-cut reasoning returns).

### 3.2 Segmentation method (the repeatable 5 steps)
1. Inventory assets + data classifications (L01 worksheet).
2. Map required flows (who talks to what, on which ports) — flows drive rules, not org charts.
3. Define zones by trust + function: edge/DMZ/corporate/servers/management/OoC (out-of-band).
4. Set inter-zone default-deny with explicit allow-pairs; document each allow with owner + justification.
5. Plan enforcement points: router ACLs, firewalls, hypervisor/SDN policy, 802.1X (L12).

### 3.3 VLANs vs zones vs physical separation
- VLAN: L2 broadcast-domain tool; no inspection, no policy — a *prerequisite* for zone enforcement, not a boundary itself.
- Security zone: set of assets sharing trust + policy; enforced by a policy point (firewall/ACL/SG).
- Physical/air-gap: for truly critical OT/backup networks; costs and reality (sneakernet risks, maintenance access).

### 3.4 DMZ patterns
- Single-firewall 3-leg vs dual-firewall back-to-back vs reverse-proxy/fronting (no direct app exposure).
- Failure-mode analysis: what does a compromised web server reach in each? (Back-to-back: internal DB only via explicit allow; proxy: nothing but the proxy contract.)
- Management plane discipline: admin interfaces in a management zone, MFA at entry — never in the DMZ.

### 3.5 Zero trust as direction, not destination
- Tenets: no implicit trust by network location; per-session authN/authZ; policy from identity + device posture + context; PDP/PEP separation; least privilege; assume breach.
- Network-level operationalizations: microsegmentation (per-workload policy), identity-aware proxies (replaces VPN-for-everything, bridges to L16), egress control (L12).
- Migration reality: coexistence with classic zones; start with crown-jewel microsegments.

## 4. Teaching Sequence (120 Minutes)

| Time | Segment | Instructor moves |
|---|---|---|
| 0–10 | Recap: Module-2 attacks → defense needs | Map each M2 attack to the layer of defense that blunts it |
| 10–35 | Core: DiD + segmentation method | Walk the 5 steps against the flat-office diagram; flows-first insistence |
| 35–55 | Core: VLAN/zone/DMZ patterns | Failure-mode table filled live; ask "what does pwned-webserver reach?" for each |
| 55–65 | Break | — |
| 65–85 | Core: zero trust | SP 800-207 tenets; microsegment example; VPN-vs-ZTNA contrast preview |
| 85–110 | Student activity: segmentation design | Teams of 3 design zones for the requirements card deck (cs-026..029 prep) |
| 110–120 | Wrap + formative | Exit ticket; Assignment-1 (design doc) briefing; trailer: L10 turns zones into rulebases |

## 5. Technical Examples

- **Zone derivation from flows:** flat office → flows table (workstation→SMB/NAS, workstation→printer, guest→internet only, cameras→NVR only). Zones emerge: GUEST, CORP, SERVERS, CCTV, MGMT; each inter-zone pair gets allow/deny with rationale.
- **VLAN plan excerpt (design artifact):** VLAN 10 CORP /24, VLAN 20 SERVERS /24, VLAN 30 GUEST /24, VLAN 40 CCTV /24, VLAN 99 MGMT — with inter-VLAN routing policy table (source zone, dest zone, ports, action).
- **Microsegment sketch:** Kubernetes NetworkPolicy (preview of L20): `ingress: from podSelector: app=frontend to port 5432` for the DB — the same default-deny idea, per-workload.

## 6. Discussion Questions

1. Why do flows-first designs beat org-chart-first designs? Give a concrete failure of the latter.
2. Your CFO wants "one big firewall because it's cheaper." Construct the minimum-cut argument from L05 that shows where that fails.
3. Which zero-trust tenet is hardest to implement in a university lab environment, and what's the pragmatic interim control?
4. What does a compromised DMZ web server reach in each DMZ pattern — and why does the answer define the pattern's value?
5. VLANs broadcast-isolate. Give the attack from Module 2 that defeats them *without* touching routing.

## 7. Student Activity

**Segmentation design sprint (25 min, teams of 3):** each team draws zones + enforcement points for one requirements card (e.g., "hospital floor: guest Wi-Fi, nursing workstations, imaging servers, vendor remote support"). Deliverable: zone map + flow table + top-5 inter-zone policies with justifications. Peer review: another team attacks the design with one M2 attack of their choice.

## 8. Problem-Solving Case

**Primary case — cs-026 "Segmentation proposal for a flat corporate network" (intermediate):**
A 300-host company runs everything on two /24s: production servers, user PCs, printers, IP cameras, and a vendor VPN terminated on the core switch. An assessment found the vendor VPN can reach all servers. Students produce a segmentation proposal: zones, VLAN/VRF plan, inter-zone policy table, management-plane placement, and a phased migration that never breaks payroll (change-management realism). Graded on justification quality, not diagram beauty.
**Linked cases:** cs-027 (DMZ design review), cs-028 (VLAN plan for corp/guest/IoT), cs-029 (microsegmentation for a data center).
*(Model solutions: instructor answer-key set, Module 3.)*

## 9. Formative Assessment

1. State the difference between a VLAN and a security zone in one sentence.
2. List the 5 segmentation steps in order.
3. Which zero-trust component decides policy, and which enforces it (abbreviations fine)?
4. In back-to-back DMZ, what is the *first* rule you write on the inner firewall?
5. Why must management interfaces never live in the DMZ?
*(Answer key: instructor set, Module 3.)*

## 10. Summary & Key Takeaways

- DiD = independent control classes across attack stages, priced by your threat model.
- Segmentation is a *method* (flows → zones → default-deny → enforcement) you can run on any network.
- Zero trust relocates trust from the network path to per-session identity+context; microsegmentation is its network expression.

## 11. References

- NIST SP 800-207 — Zero Trust Architecture.
- NIST SP 800-41 Rev. 1 — firewall policy fundamentals (bridge to L10).
- CIS Controls v8 — Controls 4 (secure configuration) & 12 (network infrastructure management) context.
- Cisco — VLAN design & best-practice guides (current docs).
- Shostack — threat-model-to-control mapping chapters (recap of L05 method).

## 12. CLO Mapping

| CLO | Where in this lecture | Assessed via |
|---|---|---|
| CLO-3 | §3.1–3.5 design method + design sprint §7 | Assignment 1 (W5), Capstone design, Quiz 3 (partial) |
