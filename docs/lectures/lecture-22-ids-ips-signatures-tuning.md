---
lecture: L22
title: IDS/IPS — Signatures & Tuning
module: 6
week: 11
hours: 2
clos: [CLO-9]
difficulty: advanced
status: complete
artifact-type: student-lecture-material
instructor-plan: modules/module-06-detection-vulnerability/lectures/lecture-22-ids-ips-signatures-tuning.md
---

# L22 — IDS/IPS — Signatures & Tuning

## 1. Learning Objectives

By the end of this session you can: (1) compare signature vs anomaly detection and state each one's blind spots; (2) describe IDS/IPS deployment modes and their availability trade-offs; (3) write syntactically correct Suricata rules (header + protocol-aware options + sid/rev); (4) tune a ruleset: measure false positives against a clean baseline and scope exclusions correctly; (5) explain evasion pressures and the layering answer.

## 2. Key Definitions

| Term | Definition |
|---|---|
| Signature detection | Known-bad pattern matching — precise, explainable, brittle to variation |
| Anomaly detection | Deviation from learned baselines — catches novelty, FP-rich, poisonable |
| IDS vs IPS | Passive detection vs inline blocking (with availability risk) |
| SPAN / tap | Mirror feed for passive sensors |
| Rule header | action, protocol, src, port → dst, port |
| Rule options | content/pcre, flow, protocol fields (http.uri, tls.sni), threshold, sid/rev |
| Threshold/suppression | Alert-volume controls; suppress the *instance*, never the *rule* |
| False positive (FP) | Alert on benign traffic — the tuning currency |
| Evasion | Techniques that hide traffic from matching (fragmentation, encoding, TLS, timing) |

## 3. Detailed Explanations

### 3.1 Detection paradigms — layered by design
**Signatures** are precise and explainable ("this byte pattern = this malware") but brittle: novel variants slip through. **Anomaly detection** catches deviation from baselines but explains poorly and false-positives richly; it feeds hunting (L23/L28) more than blocking. **Stateful protocol analysis** (Zeek — L23) checks protocol conformance and behavior. Reality: no single mode wins; layer them so each covers the others' blind spots.

### 3.2 Architecture and deployment
**Passive IDS** on a SPAN/tap: detects, zero availability risk — the starting posture (L21 placement applies). **Inline IPS** blocks — but a bad rule can now cause an outage; change control and bypass hardware are prerequisites; deploy at the highest-value choke points only. Sensor hygiene: NIC tuning (ring buffers, RSS), ruleset update cadence, and honest hardware budgeting (line-rate 10G inspection is real money — scope it).

### 3.3 Suricata rule anatomy (the craft)
Header: `alert http $HOME_NET any -> $EXTERNAL_NET any`. Options, in the order that matters:
- `flow:established,to_server;` — state anchoring.
- Protocol-aware fields over raw content: `http.method`, `http.uri`, `dns.query`, `tls.sni`, `ja3.hash` — they match *semantics*, not bytes, and survive encoding games.
- `content` with **anchoring** (`startswith`/`endswith`) — mid-string matches are FP factories.
- `threshold:type limit, track by_src, count 1, seconds 60;` — first-line volume control.
- `metadata` (created_at, attack_target) + `classtype` + **local sids ≥ 1000000** with `rev` — version-controlled like code (repo conventions).
Rule-writing method: define the *behavior* ("what would we never see from normal traffic?") → pick protocol fields → anchor content → test against **both** malicious and clean corpora.

### 3.4 Tuning and FP management (the professional skill)
Baseline first: run the ruleset against *clean* traffic for a week — the FP census. Triage classes: true-positive (tune scope), FP-but-interesting (narrow or suppress + document), noise (disable with justification). **Exclusion hygiene:** suppress the instance (specific src/dst), never the rule wholesale; every exclusion documented with expiry. Metrics: alerts/day pre/post, precision, per-rule top-FPs. The tuning log is a deliverable — L26's triage feeds it.

### 3.5 Evasion pressures and the layering answer
Classic evasions: fragmentation/reassembly games, URI-encoding mismatches, session splicing, TLS (payload invisible), low-and-slow timing. Defender answers: normalization at the sensor, protocol-aware parsers (Zeek), behavioral analytics for the encrypted remainder — and the honest acceptance that *any single sensor is evadable*, which is why L05's model maps detections across stages.

## 4. Network Diagram: sensor placement + alert flow

```
 SPAN (edge) ──► [Suricata sensor] ──eve.json──► SIEM (L21 pipeline)
 SPAN (core) ──► [Zeek sensor] ──logs──► SIEM ──► triage (L26)
 Inline (choke): [IPS] ── blocks ── bypass hardware on failure
 Ruleset: ET/community + local rules (sid≥1000000, version-controlled)
```

## 5. Protocol Examples

```
 alert http $HOME_NET any -> $EXTERNAL_NET any (
   msg:"NSLAB Suspicious periodic HTTP GET";
   flow:established,to_server;
   http.method; content:"GET";
   http.uri; content:"/gate.php"; startswith; nocase;
   threshold:type limit, track by_src, count 1, seconds 60;
   classtype:trojan-activity; sid:1000001; rev:1;)

 alert tls $HOME_NET any -> $EXTERNAL_NET any (
   msg:"NSLAB External TLS to non-corporate SNI";
   flow:established,to_server;
   tls.sni; content:".xyz"; endswith; nocase;
   sid:1000002; rev:1;)
```
Test loop: `suricata -r beacon.pcap -l out/ && grep 1000001 out/eve.json` — then the discipline step: run against `clean.pcap`, count FPs, tune.

## 6. Configuration Concepts (concept level)

- Sensor: HOME_NET/EXTERNAL_NET variables; EVE JSON output to the pipeline; rule management (et-open + local).
- Inline: AF-packet/bridged mode, bypass pair wiring, rule-deployment change control.
- Suppression files with expiry comments — exclusions are configuration with an owner.

## 7. Security Implications

- Signatures catch the known; anomalies catch the novel; neither is sufficient alone.
- Tuning is measured, documented work — not "turn off the noisy rules."
- Every rule is versioned, tested against both corpora, and documented — detection as code.

## 8. Realistic Organizational Scenario

**The C2 detection set (running case).** Malware analysis (provided write-up, no live samples): infected hosts contact `cdn-updates[.]xyz` over HTTPS every 75±5 s (~900-byte responses), first contact via HTTP `GET /gate.php`. Your deliverable: the pre-encryption HTTP rule, the SNI-anchored TLS rule, the flow-side cadence alert as an independent cross-check (L21), a tuning plan against a clean week, and the **detection note** (modeled behavior, data dependencies, expected FPs) that L26's triage will rely on. Full case: **cs-069**; the ruleset lab is the in-session exercise (Assignment 4).

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "IDS finds attacks" | IDS finds *patterns*; judgment, context, and triage find attacks. |
| "More rules = more security" | Untuned rules bury signal; precision beats count. |
| "Inline IPS is better by default" | It adds availability risk; passive first, selective inline with controls. |
| "Signatures catch APTs" | APTs use novel tooling; behavior/analytics and hunting carry that load. |
| "Suppressing a rule fixes noise" | It blinds you; suppress the instance, document, expire. |

## 10. Classroom Activities

1. **Ruleset lab (pairs):** write two rules for assigned patterns (one HTTP-anchored, one metadata-anchored); test against malicious corpus (must fire) and clean corpus (must not); add one threshold with written justification.
2. **FP census drill:** untuned vs tuned alert diff — classify every delta into the triage classes.
3. **Evasion brainstorm:** for each evasion class, name the sensor feature that counters it.

## 11. Problem-Solving Questions

1. Why can't a signature catch a novel exploit — and what *does* (name two layers)?
2. Your rule fires 4,000×/day on a backup server: give three distinct correct responses and pick one with reasons.
3. What change-control process must exist before the first inline rule goes live?
4. How do you test a rule's false-*negative* risk, not just its FP rate?
5. JA3 alerts are powerful against commodity malware and brittle against what — and what keeps them useful?

## 12. Exit Ticket

1. Write the header line for a rule alerting on outbound DNS from a server subnet.
2. Which option anchors `content` to the start of a URI, and why does it matter?
3. What's wrong with suppressing rule 1000002 entirely because one host FP'd?
4. Name two evasion classes and the sensor-side counter for each.
5. What belongs in a rule's metadata, and why do future responders care?

*(Answers: `teaching/answer-keys/answer-key-module-06.md`.)*

## 13. References

- Suricata documentation — rule syntax and EVE JSON (current version).
- Emerging Threats ruleset documentation.
- NIST SP 800-94 — Guide to Intrusion Detection and Prevention Systems.
- Ptacek & Newsham — "Insertion, Evasion, and Denial of Service…" (the classic evasion paper).
- MITRE ATT&CK + D3FEND — detection/countermeasure mapping for detection notes.

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-9 | §3.3–3.4 rule craft + tuning | Assignment 4 (W11), Pract-4 (W11), Lab-11/12 |
