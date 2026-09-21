# L21 — Monitoring Foundations

## 1. Learning Objectives

By the end of this session you can: (1) distinguish full packets, flow records, and logs by fidelity, volume, and cost; (2) explain NetFlow/IPFIX record structure and what analyses flows enable vs cannot do; (3) design a log pipeline (sources → collection → parsing → storage → detection) with retention tiers; (4) justify sensor placement against specific threat scenarios; (5) define SIEM concepts and the human triage loop around them.

## 2. Key Definitions

| Term | Definition |
|---|---|
| PCAP | Full packet capture — payloads, retransmits, handshakes; storage- and privacy-heavy |
| Flow record (NetFlow/IPFIX) | Connection metadata: 5-tuple + bytes/packets/flags/timestamps (~1:1000 of PCAP volume) |
| Sampled flow | Records only a fraction of flows — thresholds must account for it |
| Log pipeline | Sources → collection → normalization → storage → detection |
| Normalization | Parsing events into a common schema (timestamp, host, user, action) |
| Hot/warm/cold storage | Searchable recent / archived tiers — cost engineering |
| SIEM | Aggregation + correlation + alerting platform — plus the *process* around it |
| Alert precision | True alerts ÷ total alerts — the quality metric that fights fatigue |
| Sensor placement | Where your tap/SPAN feeds analysis — a scenario-driven design decision |

## 3. Detailed Explanations

### 3.1 Telemetry families and their trade-offs
- **PCAP:** maximum fidelity — payloads, TLS handshakes, retransmission behavior. Costs: storage, privacy duties. Used for deep dives and forensic reconstruction (L29), not always-on everywhere.
- **Flow records:** who/when/how-much for every connection at ~1:1000 the volume. Enables baselining, volumetric detection, lateral-movement mapping, beacon cadence. Blind to payloads — and that's fine (L14: metadata carries detection).
- **Logs/events:** application truth — auth successes/failures, DNS queries, proxy URLs. Quality varies wildly; **parsing debt** (unparsed, inconsistent fields) is the classic SIEM failure.
The design answer is **tiered**: flows everywhere; logs from crown jewels; targeted PCAP at choke points.

### 3.2 Flow data in practice
Record anatomy: src/dst IPs, ports, protocol, byte/packet counts, TCP flags, timestamps. Canonical analyses: top-talkers; **new-service detection** (host suddenly speaking SMB?); **beacon periodicity** (regular small flows); **staging patterns** (east-west bursts before egress); scan shapes (L05's signatures in aggregate). Limitations to state honestly: no payload → no content IOCs; **sampling** turns counts into probabilities (thresholds must adapt); aggregation hides low-and-slow.

### 3.3 The log pipeline (engineering, not procurement)
1. **Sources:** inventory what each device emits and at what fidelity (firewall allows+denies, DNS resolver, DHCP, proxy, VPN, AD, cloud flow logs from L19–L20).
2. **Collection:** syslog/agents/API pulls; TLS on transport; buffering for bursts.
3. **Normalization:** extract to schema — the unglamorous 70% of SIEM work; schema discipline pays at correlation time (L26's joins depend on it).
4. **Storage tiers:** hot (searchable, days–weeks), warm, cold/archive (compliance retention).
5. **Detection:** thresholds, correlations, watchlists — later, analytics (L23).

### 3.4 Sensor placement (the design skill)
Inputs: trust boundaries (L09), choke points, encryption boundaries, switching topology (SPAN capability), and — above all — the **scenarios you must detect** (your L05 model). Patterns: edge SPAN (north-south), distribution SPAN (east-west), per-zone sensors, out-of-band management. **Passive vs inline:** IDS (passive) detects with zero availability risk; IPS (inline) blocks but can cause outages — start passive, graduate to selective inline with bypass hardware. Coverage math: a 10G SPAN needs a sensor that can parse it — filter-to-relevant at capture.

### 3.5 SIEM concepts + the human loop
Ingest → normalize → **enrich** (GeoIP, threat intel, asset context) → detect → alert → **triage** (L26's skill): every alert needs an owner, a playbook link, and a disposition path. Metrics: precision, coverage (modeled techniques with detections ÷ modeled), MTTR. Alert fatigue is an *engineering* failure (untuned rules), not a staffing one. Each detection documents its modeled threat, data dependency, and expected false-positive sources.

## 4. Network Diagram: tiered telemetry + pipeline

```
 Edge ──SPAN──► [sensor: PCAP slice + Suricata/Zeek] ──┐
 Core ──SPAN──► [sensor: east-west visibility] ────────┤
 Firewalls/DNS/DHCP/VPN/proxy ──syslog(TLS)────────────┤
 Cloud (L19-20): flow logs ──S3/API pull───────────────┤
                                                       ▼
                                     [normalizer] → [SIEM hot 14d] → [archive 400d]
                                                       → alerts → triage (L26)
```

## 5. Protocol Examples

- nfdump-style reads on a lab dataset: top-10 conversations; one-way SYN storms (scan shape); `bytes < 1000` regular flows → beacon candidates with cadence evidence.
- The pipeline sketch (design artifact): `[fw][dns][dhcp][proxy][vpn][cloud] → rsyslog(TLS) → parser → SIEM(hot) → S3(archive)` — the class's reference architecture for L22–L23 and the capstone.

## 6. Configuration Concepts (concept level)

- Flow export on routers/switches (version 9/IPFIX), collector destination, sampling config.
- Syslog over TLS with buffering; retention tiers by source class.
- Sensor NIC tuning (ring buffers, RSS); capture filters to drop backup/backup-noise traffic.

## 7. Security Implications

- Tier your telemetry by *scenario need*, not by ambition: flows for breadth, logs for truth, PCAP for depth.
- Placement follows scenarios — a sensor at the wrong spot detects nothing, perfectly.
- Parsing discipline and alert quality are the SIEM's real engineering; tools are the easy part.

## 8. Realistic Organizational Scenario

**The dorm-network deviation (running case).** A month of flow data from a university dorm: steady baselines until Tuesday, when volume to one external IP rises 40× in small regular flows, and internal SMB flows jump at 03:00. You hypothesize with evidence (beacon + staging), design discriminating queries, state exactly what flow data *cannot* tell you, and write the escalation note L26's triage will receive. Full case: **cs-067**; the flow-collector + baseline build is the in-session lab.

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "Collect everything" is a strategy | Storage, parsing debt, and fatigue bury signal; tier by scenario. |
| "The firewall log is enough" | It misses east-west, DNS, identity — the pivots investigations need. |
| "Flow data replaces PCAP" | Flows answer who/when/how-much; never *what was said*. |
| "A SIEM is a product you buy" | It's a pipeline + triage process; the tool is one component. |
| "Sampling doesn't matter" | Sampled counts are probabilities; naive thresholds break. |

## 10. Classroom Activities

1. **Telemetry matching game:** five questions → which family answers it (payload? volume? auth event?).
2. **Flow-collector + baseline (pairs):** ingest the hour-one dataset; produce top-talkers, new-external-destinations, one beacon candidate with cadence, and a written baseline paragraph ("normal for this hour looks like…") — the graded artifact.
3. **Placement worksheet:** campus topology + three threat scenarios → place sensors and justify each.

## 11. Problem-Solving Questions

1. Your budget allows flows-everywhere OR PCAP-at-edge + logs-from-crown-jewels — which covers your L05 model scenarios better, and why?
2. Why is "collect everything, figure it out later" an anti-pattern? Name two guaranteed failure modes.
3. What can sampled flow data *never* prove, and which detections must therefore not depend on it?
4. Inline IPS at the core: who signs off on the availability risk, and what bypass design do you require?
5. Which three alerts from today's pipeline go to a human first — and which auto-close?

## 12. Exit Ticket

1. Match: PCAP / flow / logs → one unique capability each.
2. Why does sampling break threshold detection, and what's the mitigation?
3. Draw the 5-stage log pipeline; mark where parsing debt lives.
4. Give two scenario-driven reasons to place a sensor at the distribution layer, not just the edge.
5. Define alert precision and name its most common enemy.

*(Answers: `the instructor answer-key collection (not published)`.)*

## 13. References

- RFC 7011 (IPFIX); RFC 3954 (NetFlow v9).
- nfdump/nfcapd documentation (current).
- NIST SP 800-92 — log management; NIST SP 800-94 — IDPS guidance.
- Zeek documentation — logs overview (L23 preview).
- Bejtlich, *The Practice of Network Security Monitoring* — collection philosophy.

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-12 | §3 telemetry/placement/pipeline design | Assignment 6 (W13), Capstone, Lab-11/14 |
