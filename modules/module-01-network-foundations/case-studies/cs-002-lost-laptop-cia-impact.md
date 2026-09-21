---
case: cs-002
title: Classifying a Lost-Laptop Incident by CIA Impact
difficulty: beginner
domain: Network security principles
module: 1
lecture-anchor: L01
clos: [CLO-1]
time-estimate: 10 min (5 min reasoning + 5 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-002-solution.md
---

# cs-002 — Classifying a Lost-Laptop Incident by CIA Impact

> **Simulated scenario.** All people, systems, and data described are fictional.

## Difficulty & Domain

- **Difficulty:** Beginner · **Domain:** Network security principles · **CLO:** CLO-1
- **Est. time:** 10 minutes · **Anchor:** L01 (Security Mindset & the Network Threat Landscape)

## Scenario

A field nurse leaves a laptop in a taxi. The laptop is used for remote
consultation: it holds a cached copy of her last 30 patient reports, an
always-on VPN client, and a browser session that was not logged out of the
hospital's records portal. The laptop has full-disk encryption, but the
smartcard that unlocks it was left clipped to the same bag. IT cannot tell
whether the bag was stolen or just forgotten.

## Stakeholders

- **Patients** — confidentiality of 30 clinical reports.
- **The nurse** — may face disciplinary action; also the victim.
- **Hospital privacy officer** — regulator-notification decision.
- **IT security** — containment decision (revoke session, rotate credentials).
- **Health regulator** — statutory breach-notification thresholds.

## Network Context

- Remote access is via always-on VPN to the hospital network.
- The records portal session cookie is valid for 12 hours or until logout.
- No network-level lockout exists for stale sessions; VPN cert remains valid
  until its scheduled expiry (up to 24 h).

## Available Evidence

1. Asset record: laptop model, encrypted (FIPS 140-validated FDE), smartcard required.
2. Nurse's statement: card was in the same bag; last portal use 40 min before loss.
3. Portal config: session cookie lifetime 12 h; no re-auth on new device IP.
4. VPN config: device certificate valid 24 h; no remote-wipe enrollment.

## Student Task

1. Assess the incident against **each CIA element** separately (C, I, A) and
   justify each rating (none / low / high impact) — do not lump them together.
2. List the **next three containment actions in order**, saying what each one
   actually limits.
3. State which single fact from the evidence most changes the impact rating,
   and in which direction.

## How to Approach This (Reasoning Scaffold)

- The encryption story and the smartcard story are separate — evaluate them
  independently before combining.
- "Availability" applies to the hospital's systems too, not just the laptop.
- Containment actions differ in what they protect: credentials ≠ data ≠ device.

## CLO Mapping

- **CLO-1** — Distinguish and apply confidentiality, integrity, and availability.

## Safety Notes

- Simulated healthcare scenario; no real patient data or systems are involved.
