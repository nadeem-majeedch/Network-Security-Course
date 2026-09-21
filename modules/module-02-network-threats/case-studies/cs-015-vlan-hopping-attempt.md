---
case: cs-015
title: VLAN-Hopping Attempt Analysis
difficulty: beginner
domain: Network segmentation
module: 2
lecture-anchor: L06
clos: [CLO-2]
time-estimate: 10 min (5 min reasoning + 5 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-015-solution.md
---

# cs-015 — VLAN-Hopping Attempt Analysis

> **Simulated scenario.** The campus, switches, and logs are fictional.

## Difficulty & Domain

- **Difficulty:** Beginner (stretch) · **Domain:** Network segmentation · **CLO:** CLO-2
- **Est. time:** 10 minutes · **Anchor:** L06 (Layer-2 / LAN Attacks)

## Scenario

A university's lab network had a "strange afternoon": an analytics workstation
in the student VLAN briefly appeared to reach a server VLAN it should never
see. The network team pulled the access-switch config and a switch-port log
snippet. You are asked to explain what was attempted, why it *mostly* failed,
and what config lines would have made it fully fail.

## Stakeholders

- **Students** — some may be experimenting beyond authorization.
- **Server owners** — assume VLANs guarantee isolation.
- **Network team** — owns switch hygiene.
- **CISO** — wants to know if segmentation claims are still true.

## Network Context

- Access switch: user ports VLAN 40 (students), trunk uplink to core.
- Server VLANs 100–110 live across the core.
- Switch defaults: DTP mode `dynamic auto` on user ports; native VLAN 1
  unchanged; VTP domain configured; no port security.
- Server VLANs contain research file servers + lab databases.

## Available Evidence

1. **Port log, workstation A (VLAN 40):** ~400 frames/minute for 3 minutes
   tagged **VLAN 100**, then silence; nothing else anomalous from A.
2. **A's switch port config (excerpt):** `switchport mode dynamic auto`,
   `switchport trunk native vlan 1` (global default), no `switchport access vlan`
   pinned, DTP enabled.
3. **Core-side:** no corresponding session established from A to any server;
   some switch CPU spike during the 3 minutes.
4. Student A (interviewed): "I was testing whether VLANs actually isolate —
   I read about 'double tagging' online and tried a tool."

## Student Task

1. Explain **double-tagging** (VLAN hopping) mechanically — which frame fields
   the attacker controls and what each device does with them.
2. State precisely why this attempt "mostly failed" on this network, and the
   one design decision that would have made double-tagging *useless* here.
3. List the four switch-config changes (exact commands optional) that close
   this attack class on user ports, and name the attack variant each one targets.

## How to Approach This (Reasoning Scaffold)

- Trace one crafted frame hop-by-hop: ingress switch strips one tag, forward
  decision uses the *remaining* tag — who must be on the native VLAN for this to work?
- "Mostly failed" — what did the CPU spike mean, and what would success have
  required?
- The switch-config fixes map onto two named attack variants: double-tagging
  and trunk-negotiation (DTP) abuse. Sort your four changes across the two.

## CLO Mapping

- **CLO-2** — L2 segmentation attack mechanics and hardening.

## Safety Notes

- Simulated campus. Real VLAN testing without authorization is a policy and
  legal violation — this case exists to teach the *defense*.
