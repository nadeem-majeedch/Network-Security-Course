---
case: cs-036
title: Inbound ACL Hardening for a Management Subnet
difficulty: intermediate
domain: Firewall and ACL design
module: 3
lecture-anchor: L11
clos: [CLO-4]
time-estimate: 12 min (5 min reasoning + 7 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-036-solution.md
---

# cs-036 — Inbound ACL Hardening for a Management Subnet

> **Simulated scenario.** The DC, jump path, and audit findings are fictional.

## Difficulty & Domain

- **Difficulty:** Intermediate · **Domain:** Firewall and ACL design · **CLO:** CLO-4
- **Est. time:** 12 minutes · **Anchor:** L11 (ACLs & Rulebase Engineering)

## Scenario

A data center's management subnet (iDRAC/iLO/IPMI + switch mgmt + hypervisor
mgmt) is reachable from the operations VLAN with almost no controls — an
external audit flagged it. You must write the **inbound ACL + access-path
design**: who reaches the mgmt subnet, from where, on what ports, with what
session controls — and close the audit's three specific findings.

## Stakeholders

- **Auditor** — findings must close with evidence.
- **Ops engineers** — 24/7 access can't become a ticket queue at 3 a.m.
- **Vendor support** — needs out-of-band reach during incidents.
- **Compliance** — mgmt-plane compromise = game over; the control story must be strong.

## Network Context

- Mgmt subnet `10.90.0.0/24`: 60 BMCs, 8 switch mgmt IPs, 4 hypervisor
  mgmt, 2 storage controllers.
- Today: ops VLAN (all engineers' PCs) → mgmt: any/any.
- Site-to-site VPN exists to DC; 2 remote engineers; vendor support comes
  via "temporarily add an ACL line" today (unlogged, unowned).
- Jump host exists but is bypassed ("it's slower").

## Available Evidence

**Audit findings (the three to close):**

1. F1: "Management plane reachable from broad user VLAN — no network ACL."
2. F2: "No MFA on management interfaces; password-only BMC logins."
3. F3: "Vendor access granted via ad-hoc ACL edits — no lifecycle."

Supporting facts: BMCs support IP-based allowlists (16 entries max each) +
TLS + per-user local accounts; hypervisors support AD auth + MFA gateway;
jump host supports session recording; firewall supports time-based rules.

## Student Task

1. Write the **inbound ACL** (max 8 rules) implementing: ops-jump-host-only
   path, MFA gateway for hypervisor consoles, vendor time-boxed path, BMC
   allowlists — and say which finding each rule group closes.
2. The jump host is bypassed today. Give the **adoption design**: what makes
   the jump path *the* path (technical + procedural), per the "make the
   secure path the fast path" principle.
3. Design the **vendor lifecycle** replacing ad-hoc ACL edits (request →
   grant → expire → evidence), mapping each step to a feature in the
   evidence.

## How to Approach This (Reasoning Scaffold)

- The mgmt plane's threat model is *stolen engineer laptop + worm*, not
  "internet attacker" — the ACL's job is blast-radius containment.
- BMC allowlists (16 IPs) force an architectural decision: *fewer, named
  sources* (jump host IPs) — that constraint is a feature.
- "Secure path must be fast path": measure the current bypass reasons and
  design them away (SSO, session resume, one-URL bookmarks).

## CLO Mapping

- **CLO-4** — Management-plane access engineering with lifecycle controls.

## Safety Notes

- Design exercise; BMC/management hardening is defensive.
