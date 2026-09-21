---
case: cs-057
title: Evil-Twin AP Detection and Response
difficulty: advanced
domain: Wireless network security
module: 5
lecture-anchor: L18
clos: [CLO-8]
time-estimate: 15 min (5 min reasoning + 10 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-057-solution.md
---

# cs-057 — Evil-Twin AP Detection and Response

> **Simulated scenario.** The hotel, detections, and responses are fictional.

## Difficulty & Domain

- **Difficulty:** Advanced-Advanced · **Domain:** Wireless network security · **CLO:** CLO-8
- **Est. time:** 15 minutes · **Anchor:** L18 (Enterprise Wireless & Rogue Defense)

## Scenario

A hotel's guest Wi-Fi (`HOTEL-GUEST`) was impersonated for one weekend by
an evil twin in the lobby. Now detected and closed, you must run the
response: assess what guests lost, decide the notification duty, harden
detection, and write the client-side guidance that actually protects
future guests — with the legal/PR line between "we were attacked" and
"our network was the platform."

## Stakeholders

- **Guests** — some connected to the twin; credentials/sessions exposed.
- **Hotel management** — brand, liability, PR.
- **Hotel security vendor** — runs the Wi-Fi; defensive about detection gap.
- **Local law enforcement** — possible fraud reports.

## Network Context

- Twin: same SSID, open (matching the hotel's open+portal design), hosted
  on a portable device in the lobby, *phishing* the hotel's captive portal
  page to collect "room + surname" and any passwords typed.
- Hotel WIPS: not deployed (gap). Detection came from a guest complaint
  ("the Wi-Fi asked for my password twice").
- Guest traffic on the real network: TLS-dominant; portal is HTTP (page
  itself unauthenticated — that's how the clone worked).

## Available Evidence

**Weekend timeline (simulated):**

| Time | Observation |
|---|---|
| Fri 18:00 | twin SSID appears, stronger RSSI near lobby seating |
| Fri–Sun | portal clone live; "room number + surname" phishing + generic login forms |
| Sat | 2 guest complaints dismissed as "phone issues" |
| Sun 20:00 | guest complaint escalates; vendor investigates; twin found & removed |
| Evidence | twin device: consumer hotspot-style hardware, cache of portal clones; unknown operator (checked out Sunday? — unknown) |

Estimates: 40–90 guests associated over the weekend; portal clones
captured an unknown subset; hotel has no per-association logs for the twin
(of course), but does have *real*-network association logs to estimate the
denominator.

## Student Task

1. Reconstruct the **attack economics and mechanics**: what the twin
   operator invested vs plausibly gained, *which* guest actions exposed
   them (portal phishing vs TLS traffic), and the honest statement about
   what guests on the twin *lost*.
2. Write the **notification duty analysis**: does the hotel notify guests,
   and *which* guests? What evidence bounds the affected set, what does
   the notice say, and what does it NOT say (avoid over-claiming)?
3. Produce the **hardening plan**: WIPS deployment scope, portal
   authentication fix, client-guidance content (3 bullets that work), and
   the incident-response improvement (the "twice asked for password"
   signal that was missed).

## How to Approach This (Reasoning Scaffold)

- The twin's *payoff* was the phishing portal, not TLS-breaking — guests
  doing HTTPS with validated certs were safe; guests typing passwords into
  the clone were not. Scope the harm precisely.
- The notification set is bounded by *who associated with the twin* —
  which the hotel cannot enumerate; state the honest bound (all
  weekend guests? lobby-anchored guests?) and the over/under-claim
  tradeoff.
- The missed signal ("asked twice") is a *process* finding — the detection
  plan must make guest reports a sensor.

## CLO Mapping

- **CLO-8** — Rogue-AP incident response and control design.

## Safety Notes

- Defense analysis only; no twin-building guidance.
