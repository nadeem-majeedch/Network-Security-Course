---
lecture: L10
title: Firewalls: Concepts & Placement
module: 3
week: 6
hours: 2
clos: [CLO-3, CLO-4]
difficulty: intermediate
status: complete
artifact-type: teaching-plan
---

# L10 — Firewalls: Concepts & Placement (Teaching Plan)

## 1. Overview & Prerequisites

- **Prerequisites:** L09 (zones, default-deny, enforcement points). L03/L04 (TCP state — required to understand stateful inspection).
- **Position:** turns L09's zone map into enforcement devices. Rulebase *craft* continues in L11; today is concepts + placement + first working policy.
- **Faculty prep:** snapshot clean pfSense VMs for the lab; pre-stage the policy spec cards; verify interface/VLAN wiring on the lab range.
- **Common misconceptions:** "NGFW replaces network design"; "stateful means it inspects content"; "default-allow outbound is safe because it's *our* users."

## 2. Learning Objectives

By the end of this lecture, students can:

1. Distinguish packet-filter, stateful, and next-generation (NGFW) inspection, and state what each can/cannot see (Analyze).
2. Explain state tables and why return traffic is auto-allowed in stateful firewalls (Understand).
3. Design rule ordering per first-match semantics and explain shadowing consequences (Apply).
4. Select firewall placement for a given zone design (edge, internal segmentation, host-based) and justify HA choices (Evaluate).
5. Implement a policy spec as a working rulebase on pfSense with logging on denies (Apply).

## 3. Detailed Concepts

### 3.1 Inspection generations
- Packet filter: per-packet 5-tuple ACLs; no connection context; asymmetric routes break return paths.
- Stateful: connection table; first-packet decision + automatic return traffic; TCP state machine awareness (SYN/SYN-ACK tracking, half-open limits — L08 link).
- NGFW adds: application identification (regardless of port), user identity integration, TLS inspection options (with cost/complexity), threat feeds. Key teaching: NGFW is still a policy point — garbage policy in, garbage protection out.
- Host-based firewalls: the last policy point; zone designs should assume both network + host enforcement.

### 3.2 Stateful mechanics
- Connection table entry: 5-tuple + state + timers; established/related handling (FTP's data channel as the classic ALG example — and why ALGs are also a liability).
- Asymmetric routing kills state: traffic out path A, return path B → drops; design consequence: firewall placement must respect routing symmetry.
- TCP sequencing of policy: deny by default; allow-pairs only (source zone, dest zone, service, log).

### 3.3 Rulebase semantics and ordering
- First-match wins → specific before general; most-matched rules near top (performance); cleanup deny with logging at bottom.
- Shadowed rules (unreachable due to earlier match), redundant rules, overly permissive ANY/ANY — the audit checklist that L11 operationalizes.
- Logging: log denies by default; log allows for high-value zones; log volume engineering (what to send to the SIEM — L21).

### 3.4 Placement patterns
- Edge: ingress/egress gate; handles the internet attack surface (L08 flood relevance: connection limits here).
- Internal segmentation firewalls: between zones from L09 (CORP↔SERVERS, GUEST→internet only).
- Host-based: per-server policy for east-west least privilege (microsegmentation's classic form).
- HA pairs: stateful failover (session sync), split-brain risks, maintenance windows; active/standby vs active/active trade-offs.

### 3.5 Egress policy — the most neglected rulebase
- Outbound default-allow = free exfiltration path for any compromised host (L07/L23 link).
- Starter egress policy: allow DNS to internal resolvers only, block direct-to-IP 443 where feasible, allow per-category destinations; logging feeds detection.

## 4. Teaching Sequence (120 Minutes)

| Time | Segment | Instructor moves |
|---|---|---|
| 0–10 | Recap: zone maps on the board | One team's L09 design reused as the day's target |
| 10–35 | Core: inspection generations | Packet-filter vs stateful demo: connection table live in pfSense states view |
| 35–55 | Core: rulebase semantics | Build 5 rules live; deliberately add a shadowing error; class finds it |
| 55–65 | Break | — |
| 65–85 | Core: placement + HA | Topology walk: where does each zone's enforcement live; state-sync failure vignette |
| 85–110 | Student activity: policy build | Pairs implement the policy spec card on pfSense (Lab-06 first half) |
| 110–120 | Wrap + formative | Exit ticket; Assignment-2 preview (rulebase audit); L11 trailer: "now we audit what we built" |

## 5. Technical Examples

```
# pfSense working session (lab range, from clean snapshot)
# Interfaces: WAN (em0), CORP (em1 vlan10), SERVERS (em1 vlan20), GUEST (em2)
# Policy spec card sample:
#  1. CORP -> SERVERS: HTTPS/22 to jump host only
#  2. SERVERS -> any: deny except DNS to internal resolver + approved update mirrors
#  3. GUEST -> CORP/SERVERS: deny (log)
#  4. any -> MGMT: deny (log)

# Verify stateful behavior from CORP client:
ssh 10.0.20.10            # allowed to jump host
# Diagnostics → States: find the entry; note interface pair + state; then
# confirm return traffic needs NO explicit reverse rule (state does it).

# First-match shadowing demonstration (diagnostic view):
#   rule1: allow CORP->SERVERS tcp/443
#   rule2: deny  CORP->SERVERS tcp/443 to db01   # never reached: shadowed!
```
Expected teaching points: states view proves stateful return handling; the shadowed rule shows why audit order matters (L11's whole premise).

## 6. Discussion Questions

1. Why does asymmetric routing break stateful firewalls but not packet filters? What design rule prevents it?
2. When is TLS inspection worth its costs? Name two technical and one legal/privacy consideration.
3. Your egress policy is default-allow. Using Module 2 knowledge, describe the attack path this enables end-to-end.
4. What exactly does session sync replicate between HA nodes, and what happens to long-lived connections during failover?
5. Which rules deserve logging on *allow* rather than deny, and why?

## 7. Student Activity

**Policy build (25 min, pairs):** implement the spec card in pfSense on the range: create aliases, write ordered rules, test each with curl/ssh/nc from the right client VM, and capture one deny-log line as evidence. Deliverable: screenshot-free written test matrix (rule → test command → expected → observed).

## 8. Problem-Solving Case

**Primary case — cs-030 "Firewall placement review for a branch office" (intermediate):**
A branch runs one edge firewall; its VoIP and guest VLANs ride the same WAN uplink; the server room hosts a legacy app reachable by port-forward from the internet. An internal audit requires segmentation without buying new hardware. Students must (a) propose placement for an internal segmentation firewall (or VLAN-ACL interim), (b) redesign the port-forward (reverse proxy or VPN-only), (c) write the top-8 rulebase, and (d) identify which rules need state tracking that the legacy app's protocol breaks (asymmetric/FTP-style ALG discussion).
**Linked cases:** cs-031 (stateful rule evaluation), cs-032 (NGFW app-control policy), cs-033 (HA failover verification).
*(Model solutions: instructor answer-key set, Module 3.)*

## 9. Formative Assessment

1. Name the three inspection generations and one capability unique to each.
2. Why is no reverse rule needed for return traffic in stateful firewalls?
3. What makes a rule "shadowed," and why is it a security problem, not just untidiness?
4. Where does SYN-cookie-style connection limiting belong — edge, internal, or host — and why?
5. Write (pseudocode) a default-deny egress rulebase skeleton for a server zone.
*(Answer key: instructor set, Module 3.)*

## 10. Summary & Key Takeaways

- State is the firewall's superpower: connection context + automatic return handling.
- Placement is a design decision driven by zones and routing symmetry, not product brochures.
- Egress default-deny is the highest-leverage, most-skipped rulebase in the building.

## 11. References

- NIST SP 800-41 Rev. 1 — Guidelines on Firewalls and Firewall Policy.
- pfSense documentation — rules, states, HA (CARP/pfsync) sections (current edition).
- RFC 6092 — simple security in IPv6 (default-deny ingress rationale).
- RFC 959/2428 — FTP active/passive modes (ALG liability example).
- CIS Benchmarks — pfSense/fortigate-class device hardening baselines (for L24 bridge).

## 12. CLO Mapping

| CLO | Where in this lecture | Assessed via |
|---|---|---|
| CLO-3 | §3.4 placement design; case §8 placement review | Assignment 1 (feedback loop), Capstone design |
| CLO-4 | §3.2–3.3 rulebase semantics; activity §5/§7 build | Pract-1 (W6), Assignment 2, Lab-06 |
