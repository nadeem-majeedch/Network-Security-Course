---
case: cs-001
title: Asset and Trust-Zone Inventory of a Small-Office LAN
difficulty: beginner
domain: Network security principles
module: 1
lecture-anchor: L01
clos: [CLO-1]
time-estimate: 10 min (5 min reasoning + 5 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-001-solution.md
---

# cs-001 — Asset and Trust-Zone Inventory of a Small-Office LAN

> **Simulated scenario.** The organization, hosts, addresses, and evidence below
> are fictional teaching material, not a real incident.

## Difficulty & Domain

- **Difficulty:** Beginner · **Domain:** Network security principles · **CLO:** CLO-1
- **Est. time:** 10 minutes · **Anchor:** L01 (Security Mindset & the Network Threat Landscape)

## Scenario

A 12-person accounting firm occupies one floor. You are asked to produce a
security baseline before they buy any security product. Today the network is
one flat LAN behind an ISP-managed router: one office Wi-Fi network (WPA2-PSK,
password shared with everyone since 2021), one unmanaged 24-port switch, three
network printers, one NAS holding all client tax documents, ten laptops, a
smart TV in reception, and a door-access controller the installer put "on the
network so it can be updated." Guests routinely get the office Wi-Fi password.

## Stakeholders

- **Managing partner** — owns the client tax documents (legal/privacy exposure).
- **Office manager** — administers the router and Wi-Fi informally.
- **Clients** — their PII lives on the NAS.
- **Building security vendor** — operates the door-access controller remotely.

## Network Context

- Subnet `192.168.10.0/24`, ISP router at `.1`, flat L2, no VLANs.
- DHCP lease table shows 18 active leases for 12 employees.
- The ISP router offers no VLAN support; it supports basic port forwarding.

## Available Evidence

1. A hand-drawn topology sketch (single switch, single SSID).
2. Wi-Fi settings: WPA2-PSK, SSID "ACCT-OFFICE", password unchanged since 2021.
3. DHCP lease table excerpt: `nas .10, printer-1..3 .20-.22, doorctl .30,
   reception-tv .31, laptop-lp01 .45, plus 5 unknown Android/iOS leases`.
4. Vendor invoice: door controller "remote support enabled, port 80."

## Student Task

1. Build an asset inventory table: asset, owner, data sensitivity (high/med/low).
2. Assign every asset to a trust zone (define your own zones).
3. Identify the **three riskiest trust-zone misplacements** in the current flat
   network and say why each one matters in order.

## How to Approach This (Reasoning Scaffold)

- First classify *data*, then place *assets* — the sensitivity of what a device
  touches drives its zone, not the device type.
- Ask of each pair of assets: "if A is compromised, what does the attacker
  reach from it?"
- Do not stop at "flat network bad" — name the specific exposures.
- You will not have time for perfection; an ordered, justified top-3 is the goal.

## CLO Mapping

- **CLO-1** — Apply CIA/risk/threat vocabulary to classify assets and exposures.

## Safety Notes

- Paper exercise on a simulated environment: no scanning, no connection to any
  real network. Identical skills later apply only to systems you are authorized to assess.
