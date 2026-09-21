# cs-066 — Sensor Placement Plan for an Enterprise Edge

> **Simulated scenario.** The enterprise, chokepoints, and constraints are fictional.

## Difficulty & Domain

- **Difficulty:** Advanced · **Domain:** Network monitoring and log analysis · **CLO:** CLO-12
- **Est. time:** 15 minutes · **Anchor:** L21 (Network Monitoring Foundations)

## Scenario

A company (HQ + 2 data centers + 30 branches + cloud VPC) has budget for
**8 network sensors** (Zeek/Suricata-capable). You must design the
placement plan: which chokepoints, what visibility each buys, and the
traffic-volume math that decides where the 8 go — with the blind spots
named honestly (unmonitorable = TLS-inspected? cloud? branch local?).

## Stakeholders

- **SOC** — wants detection coverage per sensor-hour.
- **Network team** — owns SPAN/tap capacity; oversubscription kills sensors.
- **Compliance** — wants "traffic is monitored" claims survivable in audit.
- **Budget holder** — 8 sensors, not 12.

## Network Context

**Candidate chokepoints (with traffic volumes):**

| # | Chokepoint | Peak Gbps | Traffic classes | Notes |
|---|---|---|---|---|
| A | DC-1 core (east-west + north-south) | 40 | server-to-server, user-to-DC | the crown jewels live here |
| B | DC-2 core | 25 | same, smaller | replication + DR |
| C | HQ internet edge | 6 | user egress, inbound VPN | one breakout |
| D | Branch aggregation (all 30 branches) | 9 | branch user egress via DC | branches backhaul |
| E | Cloud VPC egress (shared NAT) | 3 | cloud workload egress | cs-065's lesson |
| F | HQ-to-DC WAN links (2×) | 12 | user-to-DC traffic | duplicates some C/A visibility |
| G | OOB/management plane | 0.1 | admin access | small volume, huge value |

Sensor capacity: ~2 Gbps sustained analysis per sensor (tuned), SPAN
ports available at A/B/C/D; E via flow-log mirroring (no SPAN in cloud —
agent/mirror options exist but cost); F via optical taps.

## Student Task

1. Produce the **placement plan** (8 sensors): which chokepoints get
   sensors, how many per chokepoint (load math!), and what each
   placement *detects* (name 3 detection scenarios per placement).
2. Do the **volume math** for your A-placement decision: does DC-1's 40
   Gbps fit 2 sensors? If not, what *filtering/reduction* strategy do
   you apply (which traffic classes to exclude) — and what does each
   exclusion cost in blindness?
3. List the **residual blind spots** honestly (what the 8 sensors do not
   see) and the compensating telemetry for each (logs? cloud flow? EDR?).

## How to Approach This (Reasoning Scaffold)

- Detection value = threat density × visibility, not Gbps — but Gbps
  decides *feasibility*; the math gates the plan.
- East-west at DC cores is where breaches live longest; branch traffic
  backhauls through DC (D may duplicate A's view — check).
- The G chokepoint is 0.1% of traffic and the highest *value per byte* —
  admin-plane visibility is the classic under-buy.

## CLO Mapping

- **CLO-12** — Monitoring architecture and coverage engineering.

## Safety Notes

- Design exercise; packet capture within your own authorized estate.
