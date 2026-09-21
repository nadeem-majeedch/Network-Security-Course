---
case: cs-025
title: Sinkholing and Egress-Blocking Trade-offs
difficulty: intermediate
domain: Network security principles
module: 2
lecture-anchor: L08
clos: [CLO-2]
time-estimate: 12 min (5 min reasoning + 7 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-025-solution.md
---

# cs-025 — Sinkholing and Egress-Blocking Trade-offs

> **Simulated scenario.** The manufacturer, domains, and detections are fictional.

## Difficulty & Domain

- **Difficulty:** Intermediate-Advanced · **Domain:** Network security principles · **CLO:** CLO-2
- **Est. time:** 12 minutes · **Anchor:** L08 (DoS, DDoS & Infrastructure Abuse)

## Scenario

A manufacturer's SOC found beaconing to a known botnet domain from 11 hosts.
The IR lead proposes: (a) sinkhole the domain at the internal resolver and
(b) hard-block egress to the botnet's IPs. The CIO asks: "will we lose
visibility when we do that?" You must answer with the visibility trade-off
made explicit, then design the *detection-preserving* containment.

## Stakeholders

- **SOC** — wants both containment and continued telemetry.
- **CIO** — accountable for the answer "what did we stop seeing?"
- **IT operations** — 11 hosts to reimage across 3 sites.
- **Legal** — botnet nodes on corporate machines; notification posture.

## Network Context

- Internal resolvers: 4, forwarding to upstreams; RPZ (response-policy zone)
  capable.
- Egress: one internet breakout, NGFW with TLS-inspection exempt list (they
  can see most HTTP(S) metadata, not content).
- The botnet: known family with **domain rotation every 6 hours** (DGA-style
  fallback, IPs pooled behind a rotating set).
- The 11 hosts: 7 standard workstations, 2 jump servers, 2 OT-adjacent
  engineering workstations (patching constraints).

## Available Evidence

- Beacon logs: 11 hosts, 5-min interval, jittered; domains rotate 6-hourly
  (17 domains observed over 3 days, all under 3 registrar patterns).
- NGFW: egress to those IPs: TLS ClientHello only (SNI matches domains);
  no payload visibility.
- Threat intel: the family's DGA seed rotates; blocking *observed* domains
  historically misses ~30% of future ones.
- OT workstations cannot be reimaged this month (vendor certification
  freeze).

## Student Task

1. Answer the CIO precisely: **what visibility does sinkholing preserve, what
   does egress-blocking destroy, and what does doing *both* cost?** Be
   specific about which telemetry types die at each choice.
2. Design the **detection-preserving containment**: resolver-side sinkhole +
   firewall posture + the one sensor you keep pointed at the sinkhole.
3. The OT workstations can't be reimaged: give the compensating-control plan
   for 30 days, and state the residual risk in one sentence.

## How to Approach This (Reasoning Scaffold)

- Sinkhole ≠ silence: the *client keeps trying*, and that trying is your
  telemetry — a sinkhole is a sensor if you log the queries.
- Egress-block (deny) also leaves a *deny log* — but kills TLS-phase
  metadata. Compare what each telemetry type tells you about *new* domains
  vs *known* ones.
- The DGA means observed-domain lists age at 6-hour half-life: what must the
  control be *functionally*, not just addressally?

## CLO Mapping

- **CLO-2** — Containment design with explicit visibility trade-offs.

## Safety Notes

- Simulated SOC; sinkholing/blocked-egress are standard defensive controls.
  Never sinkhole domains you don't own without coordination (collateral
  damage risk).
