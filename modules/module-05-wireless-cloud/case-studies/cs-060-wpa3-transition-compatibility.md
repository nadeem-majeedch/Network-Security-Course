---
case: cs-060
title: WPA3 Transition Compatibility Triage
difficulty: advanced
domain: Wireless network security
module: 5
lecture-anchor: L18
clos: [CLO-8]
time-estimate: 15 min (5 min reasoning + 10 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-060-solution.md
---

# cs-060 — WPA3 Transition Compatibility Triage

> **Simulated scenario.** The campus, fleet, and failures are fictional.

## Difficulty & Domain

- **Difficulty:** Advanced · **Domain:** Wireless network security · **CLO:** CLO-8
- **Est. time:** 15 minutes · **Anchor** L18 (Enterprise Wireless & Rogue Defense)

## Scenario

A university enables WPA3 on its Enterprise SSID in transition mode. Within
a week, three device cohorts misbehave (below). You must triage each
cohort's failure *mechanically* (SAE transition quirks, PMF requirements,
driver issues), decide per-cohort fixes, and design the WPA3-only endgame
with the transition mode's residual risk stated honestly (downgrade
attack surface).

## Stakeholders

- **Students/staff** — devices must just work.
- **Network team** — enabled WPA3 "for security"; now debugging.
- **Security** — wants WPA3-only eventually; wants the transition risk
  named.
- **Help desk** — collecting the tickets (the evidence).

## Network Context

- Enterprise SSID: was WPA2-Enterprise (EAP-TLS); now
  **WPA3-Enterprise transition mode** (WPA3-capable clients use SAE-
  style/PMF-enforced paths; legacy fall back to WPA2).
  *Note for accuracy:* enterprise WPA3 = 192-bit option exists; the
  transition mechanics that bite are PMF and management-frame handling,
  plus driver maturity.
- Cohorts: (A) 2022+ laptops — fine; (B) older tablets/phones (2017–19) —
  intermittent association; (C) a lab of USB Wi-Fi dongles — hard fail.

## Available Evidence

**Help-desk cluster (2 weeks):**

| Cohort | Symptom | Count | Clue |
|---|---|---|---|
| A | none | ~1,800 | — |
| B | associates, drops every ~10 min; "Wi-Fi has no internet" | ~120 devices | 2017–19 tablet fleet; vendor driver 2019 |
| C | cannot associate at all | 40 dongles | chipset 2015; driver refuses PMF |

Controller logs: cohort-B drops correlate with **PMF-protected
management-frame retransmissions** (SAE/PMF path); cohort-C never sends
the PMF-capable association.

## Student Task

1. Explain each cohort's failure **mechanically**: what WPA3/transition
   mode changes on the air (PMF enforcement, management-frame protection,
   SAE for personal — clarify what applies to *Enterprise* transition) and
   where each driver stack breaks.
2. Decide per-cohort: fix, accommodate, or replace — with the concrete
   action (driver update path? separate legacy SSID? decommission vote?)
   and the security cost of each accommodation.
3. Design the **WPA3-only endgame**: the retirement criteria for
   transition mode, the honest statement of transition mode's residual
   risk (what downgrade exposure remains, and why "transition mode" is
   not WPA3's security), and the campus policy that gets there.

## How to Approach This (Reasoning Scaffold)

- Transition mode = *both* security modes advertised; legacy clients
  self-select down. The compatibility bugs live at the seams: PMF
  (required-ish in WPA3, optional in WPA2) and driver maturity.
- Per-cohort: the *vendor driver* is the artifact — fix via update where
  the vendor lives, segment where it doesn't, replace where neither
  exists.
- The endgame's honesty: while transition mode runs, an attacker can
  *downgrade* clients (the mode exists precisely to permit legacy) —
  the risk statement must say this plainly.

## CLO Mapping

- **CLO-8** — WPA3 migration mechanics and fleet triage.

## Safety Notes

- Design exercise; no deauth/downgrade testing guidance against
  production networks.
