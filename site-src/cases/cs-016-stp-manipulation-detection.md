# cs-016 — STP Manipulation Detection

> **Simulated scenario.** The office, switches, and logs are fictional.

## Difficulty & Domain

- **Difficulty:** Beginner · **Domain:** ARP and local network threats · **CLO:** CLO-2
- **Est. time:** 10 minutes · **Anchor:** L06 (Layer-2 / LAN Attacks)

## Scenario

A marketing office's network has three "mystery outages" this quarter: each
time, the whole floor loses connectivity for ~30 seconds, then recovers. Each
outage coincided with a new employee's first day. You have the switch syslog
and a packet snippet from the outage window.

## Stakeholders

- **Employees** — repeated outages hurt a launch-week team.
- **Network manager** — needs the root cause, not another reboot.
- **Facilities/IT procurement** — brought "cute little switches" for new desks.
- **Security** — whether this is attack or accident changes the response.

## Network Context

- Floor = 2 access switches + 1 core, RSTP enabled, root bridge = core
  (priority default 32768 on all three — a config weakness).
- New-hire desks get whatever equipment employees bring from home.

## Available Evidence

1. **Syslog (core, outage window):**
   - `Topology change: root bridge changed to MAC 00:1a:2b:xx (port Gi0/2)`
   - `New root: priority 0, MAC 00:1a:2b:xx`
   - 30 s later: `Topology change: root reverted to core (priority 32768)`
2. **Packet snippet:** BPDU frames from a new MAC, priority 0, with hello
   interval advertisements; BPDU guard: not configured anywhere.
3. **Facilities email:** "we bought a 5-port desktop switch for each new desk."
4. The new MAC belongs to a desktop switch in a new hire's desk cluster.

## Student Task

1. Explain **root-bridge election mechanics** and what a "priority 0" BPDU
   does to a network that elected its root by default.
2. Distinguish: was this **malicious** or **accidental**? List the evidence
   for each and state your verdict with the deciding fact.
3. Give the three-config fix and say which outage *type* each prevents
   (malicious, accidental, or both).

## How to Approach This (Reasoning Scaffold)

- STP's root election trusts *any* BPDU with a better (lower) bridge ID —
  ask who gets to speak BPDUs on your access layer.
- The 30-second recovery window matches RSTP reconvergence, not a device crash.
- "New employee's first day" is a correlation — what hardware appears on day one?

## CLO Mapping

- **CLO-2** — Control-protocol abuse mechanics and hardening.

## Safety Notes

- Simulated network. Real STP experiments belong in your own lab only.
