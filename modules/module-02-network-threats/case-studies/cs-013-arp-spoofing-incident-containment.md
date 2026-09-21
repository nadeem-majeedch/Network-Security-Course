---
case: cs-013
title: ARP-Spoofing Incident — Symptoms and Containment
difficulty: beginner
domain: ARP and local network threats
module: 2
lecture-anchor: L06
clos: [CLO-2]
time-estimate: 10 min (5 min reasoning + 5 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-013-solution.md
---

# cs-013 — ARP-Spoofing Incident: Symptoms and Containment

> **Simulated scenario.** The office, hosts, and alerts are fictional.

## Difficulty & Domain

- **Difficulty:** Beginner (stretch) · **Domain:** ARP and local network threats · **CLO:** CLO-2
- **Est. time:** 10 minutes · **Anchor:** L06 (Layer-2 / LAN Attacks)

## Scenario

A 30-person fintech back office: users report intermittent "certificate
warnings" on internal tools and one shared-drive folder that "sometimes asks
for my password again." The help desk also notes a laptop whose Teams calls
drop for exactly 30–60 seconds then recover. An EDR-less environment: you
have switch logs, an ARP anomaly alert from a free monitoring tool, and user
reports. Management wants to know if they're "being hacked" before tomorrow's
board call.

## Stakeholders

- **Employees** — victims; internal credentials may be exposed.
- **CISO (fractional)** — board answer needed.
- **Help desk** — accumulating tickets, no pattern recognized yet.
- **Compliance officer** — PCI scope includes this office.

## Network Context

- Flat `10.10.0.0/23`, one core switch, no DHCP snooping, no dynamic ARP
  inspection (DAI), all clients on one VLAN.
- Gateway `10.10.0.1`; file server `10.10.0.20`; internal tools on `.30-.35`.
- Managed switches with CAM-table and port logs, centrally collected.

## Available Evidence

1. **Monitoring alert (2 h window):** `10.10.0.77` sent ARP replies binding
   `10.10.0.1` → MAC of .77 at ~2/min, and `10.10.0.20` → same MAC.
2. **Switch CAM log:** .77's MAC moved between three switch ports in 2 hours
   (docked laptop, wireless bridge, then conference-room port).
3. **Help-desk pattern:** cert warnings + share re-auth prompts started ~2 h
   ago, all from wired clients.
4. **.77's owner:** a contractor, present today, with a "network debugging
   tool" installed for a legitimate project.

## Student Task

1. Explain what the attacker (or tool) achieves with **two** bindings
   (gateway + file server) versus one.
2. Explain, mechanically, why users see **certificate warnings** (what's being
   attempted, why it *partially* fails) and **share re-auth prompts**.
3. Give the containment order (3 steps) and the board-ready one-liner.

## How to Approach This (Reasoning Scaffold)

- On-path interception of HTTPS mostly *fails* — but "fails" still produces
  user-visible symptoms. Match symptom → mechanism.
- Two bindings = the attacker wants traffic *in and out* — think return path.
- Containment lever #1 stops the poison; #2 finds what .77 actually captured;
  #3 prevents the next one. Order matters.

## CLO Mapping

- **CLO-2** — L2 attack mechanics → incident interpretation.

## Safety Notes

- Simulated incident. Real ARP-spoofing testing only on your own lab segment
  with authorization; production containment is a defensive activity.
