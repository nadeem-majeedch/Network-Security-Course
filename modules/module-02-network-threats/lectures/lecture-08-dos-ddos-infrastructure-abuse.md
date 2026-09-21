---
lecture: L08
title: DoS/DDoS & Infrastructure Abuse
module: 2
week: 4
hours: 2
clos: [CLO-2]
difficulty: beginner-intermediate
status: complete
artifact-type: teaching-plan
---

# L08 — DoS/DDoS & Infrastructure Abuse (Teaching Plan)

## 1. Overview & Prerequisites

- **Prerequisites:** L05 (modeling), L03 (TCP/UDP mechanics — SYN backlog, spoofable UDP), L07 (vantage reasoning).
- **Position:** closes Module 2 with the availability leg of CIA at scale; introduces flow-level telemetry reading that L21 formalizes. Motivates egress filtering (L12) and anycast/CDN design (L20).
- **Faculty prep:** prepare the simulated-flood telemetry pack (flow records + firewall counters + NetFlow graphs from the lab range's rate-limited stress test *against the range only*).
- **Common misconceptions:** "more bandwidth stops DDoS"; "SYN cookies are a firewall feature"; "botnets are only Windows bot armies."

## 2. Learning Objectives

By the end of this lecture, students can:

1. Distinguish DoS from DDoS and classify floods by layer (volumetric L3/4, protocol, application L7) (Understand/Analyze).
2. Explain reflection/amplification mechanics (spoofed source → response amplification) and compute amplification factor from service tables (Analyze).
3. Describe SYN-flood mechanics (half-open backlog exhaustion) and the SYN-cookie mitigation decision (Analyze).
4. Characterize botnet architecture (C2 models: centralized, P2P, domain-generation) and the network signature of each (Analyze).
5. Design a layered mitigation order-of-operations: upstream scrubbing → edge rate-limiting → application controls, with correct placement reasoning (Evaluate).

## 3. Detailed Concepts

### 3.1 Flood taxonomy
- Volumetric: saturate bandwidth (UDP floods, ICMP floods, amplification).
- Protocol: exhaust connection/state tables (SYN flood, ACK/SYN-ACK floods, fragmentation games).
- Application: look legitimate, exhaust expensive work (HTTP GET floods, slowloris, regex DoS, API hammering).
- Detection distinction: volumetric = obvious in traffic graphs; L7 = requires per-request analysis and rate baselining.

### 3.2 Reflection & amplification
- Attacker sends spoofed-source requests to reflector services (DNS/53, NTP/123 monlist-historic, memcached/11211, SSDP/1900, CoAP/5683); responses go to the victim.
- Amplification factor: response/request size (DNS ~28–54× depending on query, NTP monlist ~200×+ historic, memcached up to 10,000×+).
- The enabling flaw: UDP + spoofable sources; the structural fix: BCP 38 ingress filtering (source validation) — network operators' duty, students' L12 lab.

### 3.3 SYN flood & state exhaustion
- Mechanism: SYN, no ACK → half-open backlog fills → legitimate SYNs dropped.
- Mitigations: backlog tuning (partial), SYN cookies (stateless encoding of connection state into ISN), upstream filtering, RST rate triggers.
- Where each fits: cookies buy time at the edge; scrubbing handles volume; app-layer proxies shed L7 floods.

### 3.4 Botnets & C2 models
- Centralized C2 (IRC/HTTP-era): single point to find/take down → fast response possible.
- P2P: resilient, harder to sinkhole; signatures: peer-list exchange patterns.
- DGA (domain generation algorithms): domains generated algorithmically; defense: DGA detection (entropy, NXDOMAIN ratios — L23), passive DNS.
- Rentable botnets: DDoS-for-hire changes defender math — attacks are cheap and frequent; capacity + response playbooks matter more than motive analysis.

### 3.5 Mitigation architecture & order of operations
1. Upstream/ISP scrubbing or CDN/anycast absorption (buy capacity).
2. Edge ACLs/rate-limits (cheap, coarse) — drop known-bad sources/protocols at the border, not on the server.
3. Host/app controls: connection limits, request-rate shaping, queues, graceful degradation (design for load shedding).
- DNS-side: TTL management, anycast, registrar lock; sinkholing C2 domains (dual-use: defense vs abuse — governance note).
- Monitoring: flow-based thresholds (L21), per-protocol counters, and *both* directions (egress floods = compromised insiders/hosts — detection gold).

## 4. Teaching Sequence (120 Minutes)

| Time | Segment | Instructor moves |
|---|---|---|
| 0–10 | Warm-up: classify 5 flood scenarios | Teams classify layer/type in 30 s each |
| 10–35 | Core: taxonomy + SYN flood mechanics | Whiteboard backlog; SYN-cookie encoding intuition; where each mitigation lives |
| 35–55 | Core: reflection/amplification | Compute amplification factors from a service table; BCP 38 duty discussion |
| 55–65 | Break | — |
| 65–85 | Core: botnets/C2 | Map C2 models to network signatures; DGA intuition with domain-list sample |
| 85–110 | Student activity: telemetry analysis | Teams read the flood telemetry pack: classify attack, find mitigation trigger points (cs-021..025 prep) |
| 110–120 | Wrap + formative | Exit ticket; Quiz 2 announced (in-session); Module-3 trailer: "now we build what would have stopped all of this" |

## 5. Technical Examples

```
# Reading flood telemetry (lab-range flow records, no live attack)
# flow-tools / nfdump style:
nfdump -r flood1.nfcap -o 'fmt:%sa %sp %da %dp %pr %fl %pkt %byt' -A srcip -s record/bytes | head
# Teaching point: one source prefix, thousands of flows, symmetric small packets
# = volumetric UDP; compare with many sources → one dest:port = distributed.

# Rate-limit shape (router config excerpt shown as design artifact, not live)
class-map match-any FLOOD
 match protocol udp
policy-map EDGE
 class FLOOD
  police cir 100m conform-action transmit exceed-action drop

# SYN-cookie trigger concept (shown as behavior plot, not live attack):
# backlog utilization graph crosses threshold → cookie mode engaged →
# legitimate-client success rate recovers; students annotate the three phases.
```
Expected teaching points: mitigation placement (upstream vs edge vs host) is the design skill; graphs tell layer, tables tell sources.

## 6. Discussion Questions

1. Why does buying more bandwidth fail as a strategy, and when is CDN/anycast absorption the right buy?
2. BCP 38 requires *source networks* to filter egress. Why has global deployment been slow, and what changes it?
3. SYN cookies encode state in the ISN. Which TCP options are lost, and what breaks as a result?
4. You see a huge inbound NTP flood. Walk through your first three response actions and who you call first.
5. Egress-side volumetric spikes from your own campus — what does that indicate, and which lecture's control catches it?

## 7. Student Activity

**Telemetry triage (25 min, teams of 3):** from the flood telemetry pack, each team produces: attack classification (layer/type), source characterization (spoofed vs real: TTL/value reasoning), top mitigation with placement justification, and a monitoring recommendation that would have triggered 10 minutes earlier. Teams present; instructor highlights placement errors (e.g., rate-limiting the web server that the CDN should be absorbing for).

## 8. Problem-Solving Case

**Primary case — cs-021 "SYN-flood diagnosis and mitigation options" (beginner-intermediate):**
An online registration service goes unresponsive during enrollment week. Telemetry shows ~50k half-open connections to port 443, steady SYN rate from thousands of sources, low bandwidth usage. Students must (a) classify (protocol flood, not volumetric), (b) explain why the app server's backlog exhausted, (c) choose the correct mitigation order (edge SYN cookies/filtering upstream, *not* adding app capacity), and (d) write the monitoring rule that distinguishes this from a flash crowd.
**Linked cases:** cs-022 (reflection/amplification response plan), cs-023 (botnet C2 beacon patterns), cs-024 (app-layer flood rate-limit design), cs-025 (sinkholing trade-offs).
*(Model solutions: instructor answer-key set, Module 2.)*

## 9. Formative Assessment

1. Classify: "10 Gbps of UDP/123 responses to one IP" — layer, type, enabling flaw.
2. What makes an amplification attack possible with UDP but not TCP (normally)?
3. Which two counters tell you a SYN flood (not a flash crowd) is underway?
4. Why are DGA domains harder to block-list than static C2 domains?
5. Order: edge rate-limit, upstream scrubbing, app-tier load shedding — and justify the order for a volumetric attack.
*(Answer key: instructor set, Module 2.)*

## 10. Summary & Key Takeaways

- Availability attacks exploit state and bandwidth asymmetries; classify by layer to choose mitigations.
- Amplification is a source-validation failure (BCP 38) more than a victim misconfiguration.
- Response is an architecture: capacity at the edge, filters at the border, graceful degradation in the app — and egress monitoring to find your own compromised hosts.

## 11. References

- RFC 4987 — TCP SYN flooding attacks and common mitigations.
- BCP 38 / RFC 2827 — network ingress filtering (source validation); RFC 3411-era NTP reflection analyses (US-CERT alerts).
- CIRCL/US-CERT amplification-factor tables — DNS, NTP, memcached, SSDP.
- MITRE ATT&CK — T1498 Network Denial of Service and sub-techniques.
- Kurose & Ross — congestion/control context for flood behavior.

## 12. CLO Mapping

| CLO | Where in this lecture | Assessed via |
|---|---|---|
| CLO-2 | §3.1–3.5 classification + mitigation placement; telemetry triage | Quiz 2 (today), Lab-04, Case set A |
