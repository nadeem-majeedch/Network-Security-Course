---
case: cs-054
title: WPA2-PSK Wireless Audit of a Campus Floor
difficulty: advanced
domain: Wireless network security
module: 5
lecture-anchor: L17
clos: [CLO-8]
time-estimate: 15 min (5 min reasoning + 10 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-054-solution.md
---

# cs-054 — WPA2-PSK Wireless Audit of a Campus Floor

> **Simulated scenario.** The institute, SSIDs, and survey data are fictional.

## Difficulty & Domain

- **Difficulty:** Advanced-Advanced · **Domain:** Wireless network security · **CLO:** CLO-8
- **Est. time:** 15 minutes · **Anchor:** L17 (Wireless Fundamentals & Threats)

## Scenario

A research institute's floor runs WPA2-PSK with a shared password ("posted
on the wall for guests, rotated yearly"). You're given a *simulated* survey
(air monitor data + config) and must audit: PSK exposure mechanics,
row-level findings, migration options to WPA2/WPA3-Enterprise, and the
upgrade sequencing that doesn't strand the 30 IoT sensors also on that
SSID.

## Stakeholders

- **Researchers** — laptops, lab instruments on Wi-Fi.
- **Visitors** — get the wall-posted password.
- **IoT fleet (30 sensors)** — vendor firmware: PSK-only, no 802.1X.
- **Institute director** — audit response due.

## Network Context

- One SSID `CAMPUS-PSK`, WPA2-PSK (CCMP), passphrase 12 chars, on the wall
  since 2023.
- 4 APs, floor-wide; no rogue-AP detection; 2.4+5 GHz.
- Devices: 40 laptops (Enterprise-ready), 30 IoT sensors (PSK-only), guests.
- No VLAN mapping by role (all one subnet).

## Available Evidence

**Simulated survey:**

| Item | Reading | Note |
|---|---|---|
| SSID/Security | WPA2-PSK, CCMP, PMF off | — |
| Passphrase | 12 chars, word+year pattern | wall-posted |
| PMF | disabled | — |
| AP count | 4, channel plan clean | — |
| Client census | 40 laptops, 30 sensors, ~10 guest phones | same PSK |
|assoc flood test (simulated)| APs throttle at ~200 assoc/s | known behavior |
| WPS | enabled on 2 APs | vendor default missed |

## Student Task

1. Explain the **PSK exposure mechanics** concretely: what the wall-posted
   password lets a visitor compute (PTK derivation per-client, the 4-way
   handshake capture), why PSK rotation is the only retroactive control,
   and why "nobody malicious has it" is not a control.
2. Produce the **findings table** ranked: wall-posted PSK, WPS on 2 APs,
   PMF off, single flat subnet for all roles — each with risk mechanism +
   finding class (config hygiene vs architectural).
3. Design the **migration**: Enterprise for laptops/guests *plus* a
   survival path for the PSK-only sensors (segmented IoT SSID with what
   controls?), with phase ordering and the one policy that prevents
   wall-posting culture from re-emerging.

## How to Approach This (Reasoning Scaffold)

- PSK math: the passphrase *is* the PMK source for everyone — one secret
  covers all clients; capture one handshake = offline-guessable, and the
  wall makes the guessing unnecessary.
- PMF (802.11w) matters for deauth-class disruption; WPS is an old but
  *live* weakness where enabled.
- The sensor fleet forces the honest two-SSID design: Enterprise where
  possible, hardened-PSK-IoT where not — say what hardening means.

## CLO Mapping

- **CLO-8** — Wireless security mechanics and migration planning.

## Safety Notes

- Simulated survey data only; real wireless auditing requires written
  authorization and never includes deauth/disassociation testing against
  production networks.
