---
lecture: L10
title: Firewalls: Concepts & Placement
module: 3
week: 6
hours: 2
clos: [CLO-3, CLO-4]
difficulty: intermediate
status: complete
artifact-type: student-lecture-material
instructor-plan: modules/module-03-secure-architecture/lectures/lecture-10-firewalls-concepts-placement.md
---

# L10 — Firewalls: Concepts & Placement

## 1. Learning Objectives

By the end of this session you can: (1) distinguish packet-filter, stateful, and NGFW inspection and state what each can/cannot see; (2) explain state tables and why return traffic needs no reverse rule; (3) apply first-match rule ordering and recognize shadowing; (4) select firewall placement for a zone design and justify HA; (5) implement a policy spec as a working rulebase with logged denies.

## 2. Key Definitions

| Term | Definition |
|---|---|
| Packet filter | Per-packet 5-tuple decision; no connection context |
| Stateful firewall | Tracks connections; auto-allows return traffic of established sessions |
| State table | Live connection entries: 5-tuple + state + timers |
| NGFW | Adds application identification, user identity, threat feeds — still a policy point |
| ALG | Application Layer Gateway — protocol helper (e.g., FTP); also a liability |
| Shadowed rule | Unreachable rule (an earlier rule matches first) |
| HA pair | Active/standby firewalls with state synchronization |
| Egress filtering | Policy controlling traffic *leaving* a zone — the most-skilled, most-skipped rulebase |

## 3. Detailed Explanations

### 3.1 Three inspection generations
- **Packet filter:** fast, stateless; every packet judged alone. Asymmetric routes break return paths; FTP-style multi-channel protocols need helpers.
- **Stateful:** the first packet of a connection is evaluated against policy; if allowed, an entry in the **state table** authorizes the return traffic automatically. The firewall understands the TCP state machine (SYN → SYN/ACK → ESTABLISHED), which is also why SYN-flood limits (L08) live here.
- **NGFW:** adds application identification regardless of port, user identity, and threat feeds — powerful, but it is *still a policy point*: garbage policy in, garbage protection out.

### 3.2 Stateful mechanics — the table is the superpower
A state entry records the 5-tuple, direction, state, and timers. Consequences you must be able to reason from: (1) **no reverse rule needed** for return traffic of allowed sessions; (2) **asymmetric routing kills state** — if traffic leaves via firewall A and returns via firewall B, the state is missing and packets drop; (3) long-lived sessions (SSH, backups) need timer awareness or they die mid-transfer.

### 3.3 Rulebase semantics and ordering
Rules evaluate **top-down, first match wins**: specific before general; most-matched rules near the top (performance); explicit, logged cleanup-deny at the bottom. The audit faults you will hunt in L11: **shadowed** rules (dead because an earlier rule matches), **redundant** rules, **any/any** over-permissiveness, orphaned rules for decommissioned hosts. Logging: log denies by default; log allows for high-value zones; send both to the pipeline (L21).

### 3.4 Placement patterns
- **Edge:** ingress/egress gate — the internet-facing attack surface; connection limits (L08) live here.
- **Internal segmentation:** between L09 zones (CORP↔SERVERS, GUEST→internet-only).
- **Host-based:** the last policy point; east-west least privilege at per-server granularity.
- **HA pairs:** stateful failover requires *state synchronization*; split-brain (both active, desynced) is the classic failure; maintenance windows and failover testing are part of the design, not an afterthought.

### 3.5 Egress policy — the highest-leverage rulebase
Outbound default-allow = a free exfiltration path for any compromised host (L07). A starter server-zone egress policy: allow DNS to internal resolvers only; allow approved update mirrors; deny + log everything else. Those deny logs become high-value detection events (L21–L22).

## 4. Network Diagram: placement in the zone design

```
 Internet ──► [EDGE FW: ingress/egress, conn limits, L8 filters]
                     |
              [CORE routing]
             /        |         \
      [FW: CORP]  [FW: SERVERS]  [FW: GUEST]──► internet only
             \        |
              [MGMT zone: OOB, MFA]     host firewalls: every server
```

## 5. Protocol Examples

- Stateful return: CORP client → SERVERS:22 allowed by rule; the reply packets match the *state entry*, not a rule — verify in the firewall's states view.
- First-match trap: rule 1 `allow CORP→SERVERS tcp/443`, rule 2 `deny CORP→SERVERS tcp/443 to db01` — rule 2 never fires; db01 is reachable. Shadowing in one glance.

## 6. Configuration Concepts (concept level)

- Aliases first: `WEB_SERVERS`, `JUMP_HOST`, `DNS_RESOLVERS` — rules read like policy (L11 formalizes).
- Rule anatomy: action, source zone/object, dest zone/object, service, log flag, description-with-owner.
- pfSense/ equivalents: interfaces per zone, rule order review, states table for verification, HA sync settings.

## 7. Security Implications

- The state table is both the superpower and the dependency: asymmetry and timer errors become outages.
- Placement is a *design* decision driven by zones and routing symmetry — not product brochures.
- Egress default-deny converts your firewall into a detection sensor for compromised hosts.

## 8. Realistic Organizational Scenario

**The branch office (running case).** One edge firewall; VoIP and guest VLANs share the WAN uplink; the server room hosts a legacy app exposed by a port-forward from the internet. Audit requires segmentation without new hardware. Your design: internal segmentation firewall (or VLAN-ACL interim), replace the port-forward (reverse proxy or VPN-only), write the top-8 rulebase, and identify which rules need state the legacy protocol breaks. Full case: **cs-030**; the build itself is Lab-06.

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "Stateful = inspects content" | It inspects *connection state*; content inspection is DPI/NGFW/WAF territory. |
| "NGFW replaces network design" | NGFW is one enforcement point; zones, placement, and egress still decide outcomes. |
| "Default-allow outbound is safe" | It is the standard exfiltration path — server zones get allow-lists. |
| "Deny rules are unnecessary (implicit deny)" | Explicit logged denies create evidence and intent; implicit deny is silent. |
| "HA means zero-downtime always" | State-sync failures and split-brain are real; test failover, don't assume it. |

## 10. Classroom Activities

1. **Policy build (pairs, lab range):** implement your spec card on pfSense — aliases, ordered rules, test matrix (rule → command → expected → observed).
2. **Shadow hunt:** instructor-planted shadowed rule in a rulebase; first team to cite it wins.
3. **States-view verification:** generate allowed traffic, find the state entry, note interface pair and timers.

## 11. Problem-Solving Questions

1. Why does asymmetric routing break stateful firewalls but not packet filters? Which design rule prevents it?
2. When is TLS inspection worth its costs? Name two technical and one governance consideration.
3. Your egress is default-allow. Describe the end-to-end attack path this enables using Module-2 knowledge.
4. What exactly does session sync replicate, and what happens to long-lived connections during failover?
5. Which rules deserve allow-logging rather than deny-logging, and why?

## 12. Exit Ticket

1. Name the three inspection generations and one unique capability of each.
2. Why is no reverse rule needed for return traffic in stateful firewalls?
3. What makes a rule shadowed, and why is it a *security* problem?
4. Where does SYN-flood connection limiting belong — edge, internal, or host — and why?
5. Write (pseudocode) a default-deny egress skeleton for a server zone.

*(Answers: `teaching/answer-keys/answer-key-module-03.md`.)*

## 13. References

- NIST SP 800-41 Rev. 1 — Guidelines on Firewalls and Firewall Policy.
- pfSense documentation — rules, states, HA (current edition).
- RFC 6092 — simple security in IPv6 (default-deny ingress rationale).
- RFC 959/2428 — FTP modes (the ALG-liability example).
- CIS Benchmarks — firewall device hardening baselines.

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-3 | §3.4 placement design; case reasoning | Assignment 1, Capstone design |
| CLO-4 | §3.2–3.3 rulebase semantics; lab build | Pract-1 (W6), Assignment 2, Lab-06 |
