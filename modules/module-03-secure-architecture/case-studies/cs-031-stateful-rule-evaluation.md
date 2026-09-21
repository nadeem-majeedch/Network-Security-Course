---
case: cs-031
title: Stateful Rule Evaluation Against a Policy Spec
difficulty: intermediate
domain: Firewall and ACL design
module: 3
lecture-anchor: L10
clos: [CLO-4]
time-estimate: 12 min (5 min reasoning + 7 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-031-solution.md
---

# cs-031 — Stateful Rule Evaluation Against a Policy Spec

> **Simulated scenario.** The firewall, rulebase, and test traffic are fictional.

## Difficulty & Domain

- **Difficulty:** Intermediate · **Domain:** Firewall and ACL design · **CLO:** CLO-4
- **Est. time:** 12 minutes · **Anchor:** L10 (Firewalls — Concepts & Placement)

## Scenario

You audit a proposed rulebase against its policy spec. The firewall is
**stateful, top-down first-match**. Six test flows are provided; for each you
must predict **ALLOW/DENY** and name the rule that decided it. Two of the six
reveal classic rulebase defects — find them.

## Stakeholders

- **Firewall team** — wants defects found before change control.
- **App owners** — expect their flows to work after go-live.
- **Auditor** — wants the spec-to-config traceability you're producing.

## Network Context

- Zones: `INT` (workstations), `SRV` (servers), `DMZ`, `WAN` (internet).
- Firewall is stateful: replies to allowed flows auto-permit.
- Rules evaluated top-down, first match wins; implicit deny at bottom.

## Available Evidence

**Policy spec (the intent):**

1. Workstations may reach the patch server (TCP 443) in SRV.
2. Workstations may browse the web (HTTP/HTTPS) via the DMZ proxy only.
3. No workstation may reach the DB server directly (TCP 5432).
4. DMZ proxy may fetch from WAN (HTTP/HTTPS).
5. Admin subnet (part of INT, 10.9.9.0/24) may SSH to any SRV host.

**Rulebase as submitted (top-down):**

| # | Src | Dest | Svc | Action | Comment |
|---|---|---|---|---|---|
| 1 | INT | SRV | **any** | ALLOW | "patching etc." |
| 2 | INT | DMZ-proxy | 80,443 | ALLOW | web via proxy |
| 3 | INT | SRV | 5432 | DENY | spec item 3 |
| 4 | 10.9.9.0/24 | SRV | 22 | ALLOW | admin SSH |
| 5 | DMZ | WAN | 80,443 | ALLOW | proxy egress |
| 6 | INT | WAN | any | ALLOW | "fallback" |

**Test flows:**

| Flow | Src → Dest | Svc |
|---|---|---|
| F1 | workstation → patch server (SRV) | TCP 443 |
| F2 | workstation → DB server (SRV) | TCP 5432 |
| F3 | workstation → internet site (direct) | TCP 443 |
| F4 | workstation → internet site (direct) | TCP 22 |
| F5 | admin host (10.9.9.5) → SRV host | TCP 22 |
| F6 | DMZ proxy → WAN | TCP 443 |

## Student Task

1. For each flow: **ALLOW/DENY** + the deciding rule number.
2. Identify the **two rulebase defects** (hint: one makes spec item 3
   unenforceable; one makes the spec's *scope* meaningless). Name the
   defect class (shadowing / over-permission / ordering error / etc.).
3. Rewrite the minimal rulebase that enforces the spec exactly — 6 lines
   max, with the same rule-number ordering discipline.

## How to Approach This (Reasoning Scaffold)

- First-match evaluation means rule 1 decides *everything* from INT to SRV —
  read rules 2–6 with that in mind.
- Ask of every broad rule: "which narrower rule can never fire because of
  this?" That's shadowing.
- The spec says "via the proxy only" — a scope statement, not just a port list.

## CLO Mapping

- **CLO-4** — Stateful policy evaluation and rulebase defect detection.

## Safety Notes

- Paper audit of a fictional rulebase.
