---
case: cs-056
title: WEP Legacy Device Retirement Plan
difficulty: advanced
domain: Wireless network security
module: 5
lecture-anchor: L17
clos: [CLO-8]
time-estimate: 15 min (5 min reasoning + 10 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-056-solution.md
---

# cs-056 — WEP Legacy Device Retirement Plan

> **Simulated scenario.** The warehouse, device fleet, and vendor answers are fictional.

## Difficulty & Domain

- **Difficulty:** Advanced-Advanced · **Domain:** Wireless network security · **CLO:** CLO-8
- **Est. time:** 15 minutes · **Anchor:** L17 (Wireless Fundamentals & Threats)

## Scenario

A distribution warehouse runs 12 handheld barcode scanners on **WEP** —
vendor firmware from 2009, "works fine." A security scan flagged it; the
ops manager resists ("these devices cost $2k each and the vendor is
gone"). You must produce the retirement plan: WEP's actual risk mechanics
stated precisely, interim containment for a fleet that can't upgrade
*yet*, and the replacement/retirement path with the business case.

## Stakeholders

- **Ops manager** — uptime is sacred; scanners are workflow-critical.
- **Security** — WEP is broken *in minutes*; audit finding open.
- **Procurement** — replacement capex decision.
- **IT (1 person)** — will run whatever interim exists.

## Network Context

- Scanners: 802.11b/g, WEP-40 (vendor firmware), talk to a warehouse
  inventory server (WPA2-capable).
- WAP: enterprise AP with multiple SSIDs — WEP SSID exists *alongside* the
  modern corp SSID on the same APs.
- Warehouse has truck yards, neighboring businesses within radio range.
- Inventory server holds customer order data (moderate sensitivity).

## Student Task

1. State **WEP's break mechanics precisely** (why minutes: IV space,
   FCS/CRC flaw, keystream reuse) and the *actual* risk path here:
   what does an attacker do after cracking WEP in this warehouse, and
   what data is truly exposed?
2. Design **interim containment** (before replacement ships): the
   segmentation + monitoring + AP-config changes that buy months
   honestly — and the one thing interim controls *cannot* fix.
3. Produce the **retirement path**: replacement options (new scanners vs
   bridge/gateway devices vs wired-only for fixed stations), the business
   case arithmetic (loss exposure vs capex), and the decommission
   checklist (the WEP SSID's death).

## How to Approach This (Reasoning Scaffold)

- WEP isn't "old encryption" — it's a broken cipher suite (RC4 + 24-bit
  IV + unauthenticated CRC); cracking is a traffic-volume game.
- The risk path matters more than the cipher: attacker→scanner→inventory
  server; what does that path yield?
- Interim containment buys *detection latency and reach limits* — name
  what it can't buy (the cipher).

## CLO Mapping

- **CLO-8** — Legacy wireless risk and retirement engineering.

## Safety Notes

- Design exercise; WEP-cracking tool specifics are not provided —
  defense planning only.
