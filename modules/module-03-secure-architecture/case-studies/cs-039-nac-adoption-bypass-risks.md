---
case: cs-039
title: 802.1X/NAC Adoption Plan and Bypass Risks
difficulty: intermediate
domain: Enterprise architecture
module: 3
lecture-anchor: L12
clos: [CLO-3]
time-estimate: 12 min (5 min reasoning + 7 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-039-solution.md
---

# cs-039 — 802.1X/NAC Adoption Plan and Bypass Risks

> **Simulated scenario.** The hospital, device fleet, and constraints are fictional.

## Difficulty & Domain

- **Difficulty:** Intermediate-Advanced · **Domain:** Enterprise architecture · **CLO:** CLO-3
- **Est. time:** 12 minutes · **Anchor:** L12 (NAT, Proxies, Egress & NAC)

## Scenario

A regional hospital plans 802.1X/NAC. The device inventory is the problem:
managed PCs (fine), 1,400 medical devices (infusion pumps, imaging, monitors)
with unknown 802.1X support, guest devices, and building controls. You must
design the **adoption plan** (phases + failure policy per device class) and
name the **bypass risks** honestly — including the "one open port" problem
and MAB's security cost.

## Stakeholders

- **CISO** — audit wants network access control.
- **Clinical engineering** — patient-safety devices must never lose network
  (imaging archives, pumps reporting).
- **Help desk** — will own every "no network" event.
- **Vendors** — some devices do 802.1X, some do MAC auth (MAB) only, some
  nothing.

## Network Context

- 40 access switches; NAC engine planned; RADIUS/AD exists.
- Device classes: managed Windows (802.1X EAP-TLS ready), medical fleet
  (1,400: 30% EAP-capable, 50% MAB-only, 20% unknown), guests (open SSID
  separate), BMS/doors (MAB + static config).
- Clinical constraint: **no re-auth disruption** for life-critical devices;
  DHCP renewals okay, mid-session port bounces are not.

## Student Task

1. Design the **auth policy per device class** (method, VLAN/role result,
   failure mode — reject vs quarant VLAN vs allow-limited) and the
   **port-level enforcement** choice per class.
2. Plan the **three-phase adoption** (assessment/monitor/enforce) with the
   medical-fleet special handling (no-bounce constraint) and the exit
   criteria per phase.
3. Give the **top-3 bypass risks** of the resulting design, each with the
   compensating control (think: MAB spoofing, the never-authenticating
   port, and hub/handheld bridging).

## How to Approach This (Reasoning Scaffold)

- 802.1X for *who*, MAB for *what*, and the difference in security value
  (MACs are trivially spoofable — MAB is inventory discipline, not auth).
- The enforcement point matters as much as the method: DHCP-only steering
  (v4) is bypassable; RADIUS-change-of-authorization + port roles are not.
- Patient-safety constraints push medical devices to *monitor-first,
  restricted-allow* — quarantine for life-critical devices is a clinical
  hazard, not a security win.

## CLO Mapping

- **CLO-3** — NAC architecture under real-world device constraints.

## Safety Notes

- Design exercise; hospital-safety framing (fail-safe for patients) is
  part of the answer's quality.
