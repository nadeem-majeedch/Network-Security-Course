---
status: complete
artifact-type: module-overview-page
module: 2
instructor-only: false
---

# Module 2 — Network Threats & Attack Mechanics

**Lectures:** L05–L08 (Weeks 3–4) · **CLOs:** CLO-2 · **Cases:** cs-011–020

*Descriptive orientation. All offensive mechanics here are taught and studied
in the isolated lab range only — see each page's authorization frame.*

## What this module covers

With protocol fluency from Module 1, you now study how attackers abuse those
protocols — and just as importantly, what evidence each abuse leaves behind.
The framing throughout is defensive: understand the mechanics well enough to
detect, prioritize, and harden.

## Lectures

| # | Lecture | Core idea |
|---|---|---|
| L05 | [Threat Modeling & Attacker Anatomy](../../lectures/lecture-05-threat-modeling-attacker-anatomy.md) | STRIDE, attack trees, adversary capability tiers |
| L06 | [Layer-2 & LAN Attacks](../../lectures/lecture-06-layer2-lan-attacks.md) | ARP spoofing, DHCP starvation/rogue, CAM overflow, STP abuse |
| L07 | [Sniffing, MITM & Session Attacks](../../lectures/lecture-07-sniffing-mitm-session-attacks.md) | Capture positioning, TCP hijacking, downgrade tactics |
| L08 | [DoS/DDoS & Infrastructure Abuse](../../lectures/lecture-08-dos-ddos-infrastructure-abuse.md) | Volumetric vs application-layer DoS, amplification, reflection |

## Labs

[Lab-03](../../labs/lab-03-l2-attack-evidence-analysis.md) (L2 attack evidence
analysis) and [Lab-04](../../labs/lab-04-mitm-flood-telemetry.md) (MITM & flood
telemetry) work from prepared, staged evidence — you analyze attack artifacts,
you do not generate them against shared infrastructure.

## Case studies (beginner tier)

cs-011 attack tree · cs-012 ATT&CK mapping · cs-013 CAM-table overflow triage ·
cs-014 DHCP exhaustion diagnosis · cs-015 SSL-strip observation · cs-016 DNS
spoof vs cache poisoning · cs-017 amplification inventory · cs-018 SYN-cookie
capacity math · cs-019 RST attack evidence · cs-020 mitm evidence chain.
See the [case studies guide](../../cases/index.md) for the classroom protocol.

## Skills checkpoints

- Build an attack tree for a stated abuse case and prune infeasible branches.
- Identify ARP/DHCP anomalies from packet evidence and name the compensating control.
- Classify a DoS event as volumetric, protocol, or application layer with reasoning.
- Describe the detection telemetry each attack type produces (flows, logs, captures).
