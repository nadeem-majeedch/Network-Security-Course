---
case: cs-014
title: MAC-Flooding Signs on a Switch Access Layer
difficulty: beginner
domain: ARP and local network threats
module: 2
lecture-anchor: L06
clos: [CLO-2]
time-estimate: 10 min (5 min reasoning + 5 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-014-solution.md
---

# cs-014 — MAC-Flooding Signs on a Switch Access Layer

> **Simulated scenario.** The hotel, switches, and logs are fictional.

## Difficulty & Domain

- **Difficulty:** Beginner (stretch) · **Domain:** ARP and local network threats · **CLO:** CLO-2
- **Est. time:** 10 minutes · **Anchor:** L06 (Layer-2 / LAN Attacks)

## Scenario

A 200-room hotel's guest Wi-Fi and wired business-center share one access
switch stack. The AV contractor complains their streaming box "lost the
presentation feed" during a conference; the network manager pulls switch
health data and finds the two symptoms below. Some guests also reported
"seeing other people's pop-ups." The hotel manager wants to know: broken
switch, or something worse?

## Stakeholders

- **Hotel guests** — privacy (pop-up sightings) and connectivity.
- **AV contractor** — wants the network blamed or fixed.
- **Network manager** — owns the switch stack; needs a defensible verdict.
- **Hotel brand** — privacy incident on shared infrastructure.

## Network Context

- One access switch stack; guest wired ports in business center; Wi-Fi bridged
  into the same VLAN (a design flaw worth noting).
- Switch CAM capacity per stack member: 8,192 entries; normally ~1,100 used.
- Port security: **not configured** on guest ports.

## Available Evidence

1. **CAM utilization trace (conference hours):** 09:00 = 1,100; 10:15 = 3,900;
   10:40 = 8,180 (≥99%); 10:42 = "unknown-unicast flooding enabled" syslog;
   11:30 = 8,190 sustained.
2. **One port (#12, business center) contributed 7,000+ new MACs in 25 min.**
3. **During 10:40–11:30:** multiple guests' devices received traffic not
   addressed to them (guests' "pop-up" reports = unicast flooding delivering
   other guests' frames).
4. After the conference, CAM utilization returns to ~1,100.

## Student Task

1. Name the technique and explain **mechanically** how filling the CAM table
   causes guests to see others' traffic — including why it stops when the
   table drains.
2. Explain why **HTTPS guests** were largely protected while **HTTP guests**
   were not, and what the "pop-ups" tell you about the attacker's *intent*.
3. Give the two-switch-config defenses (exact feature names) and the policy
   fix for the bridged Wi-Fi design flaw.

## How to Approach This (Reasoning Scaffold)

- A switch is a *learning* device: ask what a table full of **fake** entries
  does to frames for **real, absent** MACs.
- Unicast flooding = frames out every port = passive sniffing opportunity.
- "Pop-ups" on other guests' screens means *rendered content* was delivered —
  what does that imply about what the flooder was sending?

## CLO Mapping

- **CLO-2** — Switch learning mechanics → L2 attack analysis.

## Safety Notes

- Simulated hotel network. MAC-flooding experiments belong only in your own
  lab; production response is defensive.
