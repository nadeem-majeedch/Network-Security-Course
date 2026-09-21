# L23 — Zeek & Anomaly Detection

## 1. Learning Objectives

By the end of this session you can: (1) explain Zeek's model (protocol analyzers → structured logs + scriptable events) and how it complements signatures; (2) read and cross-reference core Zeek logs by UID; (3) build behavioral baselines (per-host profiles, DNS distributions, cadences); (4) detect tunneled/abusive patterns — DNS tunneling, SMB sweeps, beacons — from log arithmetic; (5) sketch a Zeek notice policy and place it in the pipeline.

## 2. Key Definitions

| Term | Definition |
|---|---|
| Zeek | Protocol-aware network sensor producing structured logs + scriptable event engine |
| conn.log | Every connection: endpoints, duration, bytes, state codes, history flags |
| dns.log | Query name, qtype, TTLs, rcode — the tunnel/DGA hunting ground |
| UID | Connection identifier joining conn.log with protocol logs |
| Baseline | Documented "normal" per host/service/time — the anomaly reference |
| Entropy | Randomness measure of names — high entropy suggests encoding/DGA |
| NXDOMAIN ratio | Failed-answer share — DGA/beaconing signal |
| Notice | Zeek script-raised alert (notice.log) — the pipeline's Zeek-side alert stream |

## 3. Detailed Explanations

### 3.1 Zeek's model in one picture
libpcap feed → event engine → **protocol analyzers** → structured logs (conn, dns, http, ssl, files, notice…) + script events. The philosophical difference from L22: Zeek asks *"what is this protocol conversation doing?"* while signatures ask *"does this byte pattern match?"* — complementary by design. Logs are queryable tables (JSON for SIEM ingestion), which is why Zeek is the hunting substrate (L28).

### 3.2 Core log fluency (the hands-on skill)
- **conn.log:** every connection — duration, bytes, **state codes** (SF=established+finished, S0=SYN-no-reply, REJ=rejected), history flags — the backbone for lateral movement and beacon analysis.
- **dns.log:** query name, qtype, TTL, rcode — NXDOMAIN ratios, name entropy, TXT-heavy patterns (tunnel bait).
- **http.log / ssl.log:** URIs, user-agents, SNI, fingerprints — UA anomalies (curl from workstations), referrer chains.
- **files.log:** mime types, sizes, extractable payloads — document-flow hooks (L29).
- **notice.log:** script-raised alerts.
**UID joins:** the same connection appears across logs — follow one user's hour through conn→dns→http, and you've run the triage workflow in miniature (L26 preview).

### 3.3 Baselining with Zeek logs
Per-host **service profile** (what does each host normally speak to?), **DNS distribution** (per-resolver rates, NXDOMAIN ratios, entropy histograms), **cadence profiles** (regularity scoring on conn.log timestamps — the beacon math). Baseline hygiene: re-baseline after change windows; document exclusions (scanners, backup windows); baselines are *living artifacts* that L28 hunt hypotheses cite.

### 3.4 Tunnel and abuse signatures (the arithmetic)
- **DNS tunneling:** long, high-entropy qnames; TXT/NULL qtype abuse; beacon-like cadence to one authoritative NS. Detector sketch: `entropy(qname)` + qtype distribution + per-client volume. Sobering math: exfil-over-DNS is *slow* (bytes per query) — which is itself a detection insight (throughput estimate from query counts).
- **SMB lateral sweep:** many conn.log entries to 445/tcp across many hosts from one origin in a short window (history-flag pattern).
- **Beaconing:** near-constant inter-arrival + small bytes + external destination — the three-variable test, computable from conn.log.

### 3.5 A first notice policy + pipeline integration
Script sketch: track DNS queries per client; if `|qname| > 60 && entropy > 3.5 && volume > N/min` → `NOTICE`. Notices land in notice.log → forwarded to the SIEM (L21 pipeline) → triage (L26) → tuning feedback (L22's discipline, new detector class).

## 4. Network Diagram: logs → joins → detections

```
 pcap ──► Zeek ──► conn.log ──┐
                  dns.log  ───┤── UID join ──► per-host profile / baseline
                  http.log ───┤                     │
                  notice.log──┘                     ▼
                                        anomaly / tunnel / beacon detections
                                              → SIEM → triage (L26) → tuning (L22)
```

## 5. Protocol Examples

- Process a capture: `zeek -r sample.pcap local` → logs in `./`; inspect with `zeek-cut ts id.orig_h id.resp_h id.resp_p < conn.log | head`.
- UID join: `grep <uid> conn.log dns.log http.log` — one conversation, three views.
- Tunnel hunt: qname length/label counts sorted descending; entropy per client; TXT-qtype concentration — the planted tunnel in the lab dataset falls out of arithmetic.

## 6. Configuration Concepts (concept level)

- Zeek node.cfg for the range sensor; log rotation into the pipeline; JSON output for SIEM.
- Local script policy: threshold constants documented; notice-to-SIEM mapping.
- Baseline jobs: daily per-host profile diffs; entropy histograms per resolver.

## 7. Security Implications

- Zeek turns wire traffic into queryable metadata — the behavioral half of detection engineering.
- Baselines are living profiles; tunnels and beacons fall out of arithmetic you can now compute.
- Notices + signatures + flows = layered detection feeding one triage pipeline (L26).

## 8. Realistic Organizational Scenario

**The research-subnet suspicion (running case).** A hunch: data leaves a research subnet via DNS. Provided: 24 h of dns.log + conn.log. You compute qname length/entropy distributions, identify the outlier client, confirm cadence + authoritative-NS concentration, estimate exfil throughput from query counts × payload bytes, design the standing detection (entropy + qtype + volume thresholds) with its FP profile, and write the handoff note for L26 triage citing the three proving logs. Full case: **cs-073**; the three-part worksheet (profile, tunnel find, notice sketch) is the in-session lab.

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "Zeek is another Snort" | Different model: protocol conformance + behavior, not byte signatures. |
| "Anomaly detection is automatic AI magic" | It's baselines you build, maintain, and defend — with documented exclusions. |
| "Baselines are one-time" | Change windows, new apps, and drift require re-baselining. |
| "High entropy = malicious" | CDNs and some apps use random-looking names — context beats thresholds. |
| "More logs always help" | Unparsed logs are cost without signal; schema discipline first. |

## 10. Classroom Activities

1. **Zeek analysis lab (pairs, three parts):** (1) service profile for a given host; (2) locate the planted DNS tunnel (qname stats + qtype + client volume) and the SMB sweep (conn.log pattern + window); (3) sketch a notice policy for one of them.
2. **UID-join race:** first pair to follow one connection across three logs wins.
3. **Baseline defense:** instructor challenges a class baseline exclusion; teams justify or revise.

## 11. Problem-Solving Questions

1. Why does protocol-conformance detection catch things content signatures miss — and vice versa? One attack per blind spot.
2. Your DNS entropy alert fires on a legit backup tool's long TXT records — tune like a professional: what changes, what stays?
3. What makes a baseline "living"? Name three re-baselining triggers.
4. Why is the UID join the triage superpower? Which L26 question does it answer fastest?
5. Where do Zeek notices lose fidelity that Suricata content rules keep — and what compensates?

## 12. Exit Ticket

1. Name three Zeek logs and one unique field each exposes.
2. Which conn.log state code indicates a rejected connection attempt?
3. Give the three-variable beacon test and where each variable lives.
4. Which two query-pattern properties most strongly suggest DNS tunneling?
5. What must be true about the CNI/stack before Zeek-equivalent visibility works in cloud (L20 tie-in)?

*(Answers: `the instructor answer-key collection (not published)`.)*

## 13. References

- Zeek documentation — log reference, script language, zeek-cut (current).
- DNS tunneling/DGA detection literature (entropy-based methods).
- NIST SP 800-94 — IDPS layering context; MITRE ATT&CK T1071.004 (DNS).
- Corelight/SELKS sensor deployment references.

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-9 | §3 analytics + notice policy | Pract-4, Lab-12, Assignment 4 (feedback) |
| CLO-12 | §3.3–3.4 baselines + pipeline integration | Assignment 6 (W13), Capstone, Lab-11/14 |
