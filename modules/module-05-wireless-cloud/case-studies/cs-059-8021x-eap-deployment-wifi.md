---
case: cs-059
title: 802.1X/EAP Deployment for Enterprise Wi-Fi
difficulty: advanced
domain: Wireless network security
module: 5
lecture-anchor: L18
clos: [CLO-8]
time-estimate: 15 min (5 min reasoning + 10 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-059-solution.md
---

# cs-059 — 802.1X/EAP Deployment for Enterprise Wi-Fi

> **Simulated scenario.** The company, fleet, and rollout pains are fictional.

## Difficulty & Domain

- **Difficulty:** Advanced · **Domain:** Wireless network security · **CLO:** CLO-8
- **Est. time:** 15 minutes · **Anchor:** L18 (Enterprise Wireless & Rogue Defense)

## Scenario

A 500-person company moves corporate Wi-Fi from WPA2-PSK to 802.1X. You
design the EAP method choice (EAP-TLS vs PEAP-MSCHAPv2), the certificate
provisioning path, the RADIUS architecture, and the rollout that avoids
the classic day-one outage (auth server down = nobody on Wi-Fi). Include
the BYOD/device-classes story and the fallback design that isn't a
backdoor.

## Stakeholders

- **Employees** — 500 devices, zero tolerance for "can't connect."
- **IT (4 people)** — RADIUS/cert ops added to their plate.
- **Security** — credential-theft resistance is the point (PEAP's
  MSCHAPv2 weakness is the decision driver).
- **Fleet quirks** — printers (30), scanners (10), conference-room
  systems (8): not 802.1X-native.

## Network Context

- Current: WPA2-PSK (shared), one SSID, flat VLAN.
- AD + PKI (internal CA) exist; MDM covers 480 of 500 laptops.
- Controllers support dynamic VLAN/role assignment via RADIUS attributes.
- Legacy devices can do WPA2-PSK only.

## Student Task

1. Make the **EAP method decision**: EAP-TLS vs PEAP-MSCHAPv2 — the
   security mechanics that decide it (credential exposure vs cert
   provisioning cost), and your call for *this* fleet (MDM coverage is
   the deciding fact). One paragraph.
2. Design the **architecture**: RADIUS topology (redundancy!), certificate
   lifecycle via MDM (enrollment/renewal/revocation), dynamic VLAN/role
   mapping (which roles/VLANs exist), and the **legacy-device pattern**
   that isn't a shared PSK.
3. Plan the **rollout with the day-one-outage fix**: phased SSID overlap
   (new SSID alongside), per-group migration, the failure-mode design
   (what happens when RADIUS dies — and why "allow PSK fallback" is the
   backdoor you must design around), and the rollback triggers.

## How to Approach This (Reasoning Scaffold)

- PEAP-MSCHAPv2 tunnels the password but MSCHAPv2's crypto (MD4/DES-era)
  makes offline attacks on leaked handshakes feasible — EAP-TLS removes
  the password from the equation entirely; MDM at 96% coverage makes
  cert provisioning *free*.
- The RADIUS pair must be *redundant and boring* — the outage design is
  the graded core.
- Legacy devices: per-device PSKs (iPSK) on a segregated SSID/VLAN —
  identity-ish without 802.1X; not a shared secret.

## CLO Mapping

- **CLO-8** — Enterprise 802.1X architecture and rollout engineering.

## Safety Notes

- Design exercise; no live credential handling.
