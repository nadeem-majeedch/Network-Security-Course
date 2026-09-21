---
case: cs-018
title: Internal MITM — Evidence and Defensive Fixes
difficulty: beginner
domain: ARP and local network threats
module: 2
lecture-anchor: L07
clos: [CLO-2]
time-estimate: 12 min (5 min reasoning + 7 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-018-solution.md
---

# cs-018 — Internal MITM: Evidence and Defensive Fixes

> **Simulated scenario.** The bank branch, hosts, and captures are fictional.

## Difficulty & Domain

- **Difficulty:** Beginner · **Domain:** ARP and local network threats · **CLO:** CLO-2
- **Est. time:** 12 minutes · **Anchor:** L07 (Sniffing, MITM & Session Attacks)

## Scenario

A bank branch's teller application uses an internal HTTPS service
(`teller.internal.bank.example`) behind a self-signed internal certificate.
Tellers report that "twice this month, the app demanded a certificate
exception." A 90-second SPAN capture taken during the second event shows the
traffic below. Compliance wants to know whether customer data could have been
read, and the network team wants the fix list.

## Stakeholders

- **Tellers** — potential credential exposure.
- **Bank security** — incident classification (fraud vs malfunction).
- **Compliance** — regulator notification threshold question.
- **Application team** — owns the self-signed cert choice.

## Network Context

- Branch LAN `10.40.0.0/24`; teller app server `.25`; gateway `.1`.
- The teller app's certificate is self-signed by the app server (no internal PKI).
- Endpoints: teller Windows PCs with the app in a kiosk browser.
- No 802.1X; one unmanaged switch in the break room (against policy).

## Available Evidence

**90-second SPAN capture during event #2:**

| Phase | Observation |
|---|---|
| 0:00–0:20 | teller-PC `.31` ARPs normally; gateway `.1` MAC = `00:1b:44:11:3a:07` everywhere |
| 0:21 | `.1` → `00:1b:44:11:3a:07` reply; `.25` → `00:1b:44:11:3a:07` reply (normal) |
| 0:35 | **untrusted reply:** `.1` → MAC `00:0c:29:7e:19:c2` (new device), 3× in 10 s |
| 0:36–1:10 | `.31`'s TLS ClientHellos to `.25:443` now also appear on the **break-room switch uplink** (they shouldn't — `.25` hangs off the core) |
| 1:05 | `.31` receives a **certificate-not-valid** warning; teller clicks through? (no — the app blocks: kiosk browser policy) |
| 1:10–1:30 | ARP replies revert to `00:1b:44:11:3a:07`; spurious MAC stops transmitting |
| Extra | spurious MAC's device type from DHCP fingerprint: "Linux 5.15, laptop" |

## Student Task

1. Reconstruct the **attack sequence** (what tool-behavior does this match?)
   and state what the attacker achieved and *failed* to achieve.
2. Answer compliance's question precisely: **what customer data was exposed,
   if any**, distinguishing what TLS protected from what it couldn't.
3. Give the fix list split into **must-do-now** (this week) and
   **must-do-this-quarter**, each with the failure mode it eliminates.

## How to Approach This (Reasoning Scaffold)

- The self-signed certificate is the *reason* tellers see warnings — and also
  the reason the kiosk policy could block. Two-edged: weak trust config,
  strong last line.
- The ClientHello appearing on the wrong uplink is the on-path proof —
  topology + capture geography beats ARP logs alone.
- TLS protects content, not *reachability*: name what an on-path attacker
  still had (SNI, timing, the ability to drop/block).

## CLO Mapping

- **CLO-2** — MITM mechanics, TLS boundary analysis, layered fixes.

## Safety Notes

- Simulated bank environment; TLS-interception *attack* concepts are taught
  only to inform defense. No interception tooling instructions are provided
  or permitted in coursework.
