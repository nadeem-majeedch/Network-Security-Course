---
lecture: L09
title: Defense in Depth & Network Segmentation
module: 3
week: 5
hours: 2
clos: [CLO-3]
difficulty: intermediate
status: complete
artifact-type: student-lecture-material
instructor-plan: modules/module-03-secure-architecture/lectures/lecture-09-defense-in-depth-segmentation.md
---

# L09 — Defense in Depth & Network Segmentation

## 1. Learning Objectives

By the end of this session you can: (1) explain defense in depth as independent *control classes* — not layered products; (2) design trust zones from data-flow analysis using the 5-step method; (3) distinguish VLANs (traffic engineering) from security zones (policy enforcement); (4) compare DMZ patterns by what a compromised host reaches; (5) summarize zero-trust tenets and name their network-level operationalizations.

## 2. Key Definitions

| Term | Definition |
|---|---|
| Defense in depth | Independent control classes across attack stages (prevent/detect/respond/recover) |
| Trust zone | Set of assets sharing trust level + policy, enforced at a policy point |
| VLAN | Layer-2 broadcast-domain tool — *not* a policy boundary by itself |
| DMZ | Zone for internet-facing services, isolated from internal zones |
| Microsegmentation | Per-workload policy (east-west), not just per-zone (north-south) |
| Zero trust | No implicit trust by network location; per-session authN/authZ (NIST SP 800-207) |
| PDP / PEP | Policy Decision Point (decides) / Policy Enforcement Point (enforces) |
| Default deny | Everything not explicitly allowed is denied — the segmentation baseline |

## 3. Detailed Explanations

### 3.1 Defense in depth, precisely
Depth means **independent** controls across the attack timeline: *prevent* (filters, crypto), *detect* (monitoring, IDS), *respond* (IR playbooks), *recover* (backups, HA). "Independent" is the operative word: two controls sharing one failure mode (same console, same trust anchor, same admin credential) are effectively **one** control. Depth is also priced: controls are chosen against your L05 threat model, not bought by layer count.

### 3.2 The 5-step segmentation method (use it everywhere)
1. **Inventory** assets + data classifications (your L01 worksheet).
2. **Map required flows** — who talks to what, on which ports. *Flows drive rules; org charts do not.*
3. **Define zones** by trust + function: edge / DMZ / corporate / servers / management / out-of-band.
4. **Set inter-zone default-deny**, with explicit allow-pairs — each documented with owner and justification.
5. **Choose enforcement points**: router ACLs, firewalls, hypervisor/SDN policy, 802.1X (L12).

### 3.3 VLANs vs zones vs physical separation
A **VLAN** isolates broadcast domains — useful for traffic engineering and a *prerequisite* for zone enforcement, but no inspection or policy lives in it. A **security zone** is a policy construct enforced by a firewall/ACL/SG. **Physical separation** (air-gap) is for the truly critical (OT, backups) — with its own risks (sneakernet malware, maintenance access). Confusing VLAN with zone is the most common design error students make; the exam will test it.

### 3.4 DMZ patterns — compared by blast radius
- **Single firewall, three legs:** web/app/mail in the DMZ leg. Compromised DMZ host → reaches internal zones only across explicit rules.
- **Dual firewall (back-to-back):** outer and inner policy points; an inner misconfiguration is caught by the outer — and vice versa.
- **Reverse proxy fronting:** no direct app exposure at all; the proxy *is* the surface.
Ask of each: *what does a pwned webserver reach?* The answer defines the pattern's value. Management interfaces never live in the DMZ — admin access rides a separate management zone with MFA.

### 3.5 Zero trust: direction, not destination
NIST SP 800-207 tenets: no implicit trust by network location; per-session authentication and authorization; policy from identity + device posture + context; **PDP/PEP separation**; least privilege; assume breach. Network-level operationalizations: **microsegmentation** (per-workload policy), **identity-aware access** (ZTNA replaces VPN-for-everything — L16), **egress control** (L12). Migration reality: zones and zero trust coexist for years; start with crown-jewel microsegments.

## 4. Network Diagram: flat vs segmented

```
 FLAT (one switch, one policy):            SEGMENTED (zones + policy points):
 Internet ──► everything                    Internet ─► [edge FW] ─► DMZ (web)
   workstations, servers,                             [inner FW] ─► SERVERS (DNS, DB)
   cameras, guest, mgmt...                            [core] ─► CORP (users)
 All east-west traffic trusted.                      GUEST ─► internet only
 One compromise = total reach.                       MGMT ─► OOB, MFA-only
```

## 5. Protocol Examples

- Flow-table to policy: workstation→SMB/NAS (allow), workstation→printer (allow), guest→anything-internal (deny), cameras→NVR only (allow). The zones and the rule pairs *fall out* of the flow table — that is the method working.
- Microsegment example (preview of L20): a Kubernetes NetworkPolicy allowing only `app=api` pods to reach the DB on 5432 — the same default-deny idea, per workload.

## 6. Configuration Concepts (concept level)

- Zone addressing plan: VLAN + subnet per zone (VLAN 10 CORP, 20 SERVERS, 30 GUEST, 40 CCTV, 99 MGMT).
- Inter-zone policy table: source zone, dest zone, service, action, justification, owner.
- Default-deny baseline: explicit cleanup-deny rules (logged) at each policy point.

## 7. Security Implications

- Flat networks give every attacker every path; segmentation is the *structural* answer to L06–L08 position theft and flood blast radius.
- Flow-first design survives reorganizations; org-chart-first design rots.
- Zero trust shifts trust from network location to session context — but PEP quality still decides everything.

## 8. Realistic Organizational Scenario

**The 300-host company (running case).** Everything on two /24s: production servers, user PCs, printers, cameras, and a vendor VPN terminated on the core switch. An assessment found the vendor VPN reaches all servers. Your deliverable (Assignment 1): zones, VLAN/VRF plan, inter-zone policy table, management-plane placement, and a *phased* migration that never breaks payroll — with a change plan per step. Full case: **cs-026**; peer-review attack round included.

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "A VLAN is a security boundary" | VLANs isolate broadcast; policy lives at enforcement points. |
| "One strong edge firewall = defense in depth" | Depth means independent classes across *stages*, not one thick gate. |
| "Zero trust means trust nothing, ever" | It means *verify explicitly per session* — identity, device, context. |
| "Segmentation breaks everything" | Flow-first design preserves required flows; it breaks *assumptions*, not work. |
| "Microsegmentation is only for clouds" | Host firewalls + NAC + SDN deliver it on-prem too. |

## 10. Classroom Activities

1. **Segmentation design sprint (teams of 3):** zones + enforcement points for one requirements card (hospital floor: guest Wi-Fi, nursing workstations, imaging servers, vendor remote support) — zone map, flow table, top-5 policies.
2. **Peer attack round:** another team attacks your design with one Module-2 attack; revise.
3. **VLAN-vs-zone sorting:** ten statements — classify as VLAN fact, zone policy, or neither.

## 11. Problem-Solving Questions

1. Why do flows-first designs beat org-chart-first designs? Give a concrete failure of the latter.
2. Your CFO wants "one big firewall because it's cheaper." Make the minimum-cut argument (L05) that shows where that fails.
3. Which zero-trust tenet is hardest in a university lab, and what's the pragmatic interim control?
4. What does a compromised DMZ webserver reach in each DMZ pattern — and why does that define the pattern?
5. Name the Module-2 attack that defeats VLANs *without touching routing*.

## 12. Exit Ticket

1. State the difference between a VLAN and a security zone in one sentence.
2. List the 5 segmentation steps in order.
3. Which zero-trust component decides policy, and which enforces it (abbreviations fine)?
4. In back-to-back DMZ, what is the *first* rule you write on the inner firewall?
5. Why must management interfaces never live in the DMZ?

*(Answers: `teaching/answer-keys/answer-key-module-03.md`.)*

## 13. References

- NIST SP 800-207 — Zero Trust Architecture.
- NIST SP 800-41 Rev. 1 — firewall policy fundamentals (bridge to L10).
- CIS Controls v8 — Controls 4 (secure configuration) and 12 (network infrastructure management).
- Cisco VLAN design guides (current).
- Shostack — threat-model-to-control mapping (L05 recap).

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-3 | §3 design method; §10 sprint | Assignment 1 (W5), Capstone design, Quiz 3 |
