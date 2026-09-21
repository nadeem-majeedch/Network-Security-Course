# cs-028 — VLAN Plan for Corporate, Guest, and IoT Traffic

> **Simulated scenario.** The firm, devices, and constraints are fictional.

## Difficulty & Domain

- **Difficulty:** Intermediate · **Domain:** Network segmentation · **CLO:** CLO-3
- **Est. time:** 12 minutes · **Anchor:** L09 (Defense in Depth & Network Segmentation)

## Scenario

A 120-person architecture firm moves to a new office. You design the VLAN
plan from scratch (a luxury!). Devices: employee laptops+desktops, guest
Wi-Fi, printers, video-conference room systems, smart TVs in meeting rooms,
door-access panels, HVAC controller, IP cameras, one NAS with client
drawings, and a "smart coffee machine" the office manager bought. The
building landlord demands door panels stay reachable by *their* maintenance
vendor. Design zones + policy, and specifically decide what to do about the
coffee machine and the landlord requirement.

## Stakeholders

- **Partners** — client drawing confidentiality (the NAS is crown jewels).
- **Office manager** — bought the coffee machine; needs a face-saving answer.
- **Landlord** — contractual demand for vendor access to door panels.
- **Employees** — casting to TVs and printers must "just work."

## Network Context

- New L3 switch stack + one firewall; Wi-Fi: 3 SSIDs possible (corp WPA2-Ent,
  guest open, IoT PSK).
- Door panels: vendor connects via cloud app; panels also have local
  config port; landlord demands "network access for maintenance."
- HVAC: vendor cloud + local thermostat protocol to one controller.
- Casting/room systems: mDNS-heavy.

## Student Task

1. Produce the **VLAN/SSID plan** (zone table: VLAN, members, SSID mapping,
   inter-zone policy one-liner each).
2. Decide the **coffee machine** with a defensible policy (2 options minimum)
   and the **landlord requirement** with a concrete technical arrangement —
   not "we'll negotiate."
3. Name the **mDNS/casting** problem the design must solve and give the
   standard solution(s), with the tradeoff each carries.

## How to Approach This (Reasoning Scaffold)

- Consumer IoT (TVs, coffee) behaves like *untrusted guests with vendor
  cloud phones-home*: isolate by default, allow egress, deny lateral.
- Contractual access ≠ network-wide trust: translate "vendor can maintain"
  into a scoped, auditable path.
- mDNS is multicast — it does not cross VLANs by default; that's either your
  bug or your feature depending on the zone design.

## CLO Mapping

- **CLO-3** — Zone design for mixed trust in a greenfield office.

## Safety Notes

- Design exercise; building-controls safety constraints respected (door/HVAC
  must fail safe and remain administrable in emergencies).
