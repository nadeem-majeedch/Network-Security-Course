---
case: cs-008
title: Rogue DHCP Server Effects on a Client Subnet
difficulty: beginner
domain: DNS and DHCP security
module: 1
lecture-anchor: L03
clos: [CLO-1]
time-estimate: 10 min (5 min reasoning + 5 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-008-solution.md
---

# cs-008 — Rogue DHCP Server Effects on a Client Subnet

> **Simulated scenario.** The campus, hosts, and evidence are fictional.

## Difficulty & Domain

- **Difficulty:** Beginner · **Domain:** DNS and DHCP security · **CLO:** CLO-1
- **Est. time:** 10 minutes · **Anchor:** L03 (Protocol Deep Dive II)

## Scenario

Monday 08:40, a computer-lab manager reports that lab PCs "have internet but
can't reach the library catalog or print servers." Some laptops work fine. A
student mentions their roommate "was playing with a Raspberry Pi in the lab
over the weekend." You are given the evidence below.

## Stakeholders

- **Lab users** — broken intranet access.
- **Lab manager** — accountable for the room.
- **Campus NOC** — wants the room's switch port disabled or not.
- **The Pi owner** — a student whose intent matters (curiosity vs malice) but
  whose *effect* is identical.

## Network Context

- Lab subnet `172.16.40.0/24`; legitimate DHCP from campus core (`.1`).
- Legit DHCP option 3 (router) = `172.16.40.1`; option 6 (DNS) = campus resolvers.
- All PCs are DHCP clients; no DHCP snooping configured on the lab switch.

## Available Evidence

1. **A working PC (`ipconfig /all` excerpt):** lease from 172.16.40.1, router
   172.16.40.1, DNS campus resolvers — normal.
2. **A broken PC:** lease from **172.16.40.200** (a DHCP server nobody
   recognizes), router = **172.16.40.5**, DNS = **8.8.8.8** and **1.1.1.1**.
3. **Switch port counters:** port 17 (student desks area) shows a new MAC on
   the weekend; the Pi's MAC OUI maps to a single-board vendor.
4. **Working laptops:** they cached valid leases from last week (lease 8 days,
   T1 rebinding not yet reached) — hence "some devices fine."

## Student Task

1. Name the event and explain, packet-level, how the Pi's messages defeated
   the legitimate server for some clients.
2. Explain precisely why "internet works but intranet doesn't" on affected PCs.
3. Order the response: what do you do first, and why is the switch port the
   decisive lever?

## How to Approach This (Reasoning Scaffold)

- DHCP clients take the **first** offer (DORA), not the "best" one — race mechanics.
- The rogue's *option set* is the attack payload: router + DNS choices create
  the specific brokenness pattern you see.
- Containment lever vs forensic step: which one stops new victims in seconds?

## CLO Mapping

- **CLO-1** — DHCP protocol mechanics → threat understanding.

## Safety Notes

- Simulated incident. Real DHCP testing belongs on your own lab segment only.
