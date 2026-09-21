---
marp: true
theme: default
paginate: true
lecture: L23
week: 12
clos: [CLO-9, CLO-12]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# Zeek & Anomaly Detection

**Network Security · Lecture 23 · Week 12**

*The network narrates its behavior — Zeek takes the minutes.*

<!-- notes: OPEN (2 min). Hook: "Signatures match crimes. Zeek writes
the testimony." -->

---

## Learning Objectives

1. **Explain** Zeek's protocol-analysis logging model vs signature
  matching
2. **Navigate** the core log set (conn, dns, http, ssl, files)
3. **Detect** beaconing and DNS-tunneling patterns from Zeek/flow data
4. **Correlate** Zeek logs with IDS alerts and flows (the three-way
  rule)
5. **Write** a simple behavioral detection (Lab-11/12 continuity)

<!-- notes: (1 min) Objective 3 is cs-073's case + QB-029/043; the
detection students write in assignment 4 lives in this lecture. -->

---

## Zeek's Model: Behavior → Structured Logs

- Parses protocols into typed logs — not signatures
- `conn.log` = every conversation; `dns/http/ssl` = protocol detail
- Scripting framework: site-specific detections (your rules live here)

![bg right:35% fit](diagrams/07-ids-ips-workflow.md)

<!-- notes: (5 min) Diagram 07 re-shown: Zeek as the sensor layer.
Quiz-11 Q3's answer ("rich protocol-level logging") is this slide. -->

---

## The Beacon Pattern (Statistical View)

```
 regular intervals: 60s ±3s over hours
 small, uniform volumes: ~2 KB
 fixed external destination
```

- Regularity (low interval variance) + uniformity + persistence =
  C2 profile
- Legit polling (monitoring agents, updates) is the FP class —
  allow-list by behavior/publisher

<!-- notes: (6 min) cs-023's case + assignment-4's detection target.
The statistical framing is the DS-student hook: this is distribution
analysis on timestamps. QB-043's classification question reads this. -->

---

## DNS Tunneling: The Exfil Channel

- High-entropy subdomain churn: `data.heavy-random.c2-domain.com`
- Long queries, TXT records, unusual query *rates* per client
- Detection: entropy + uniqueness per client (QB-029's answer)

<!-- notes: (6 min) cs-073's detection-design case. The lecturer's
demo: two entropy distributions side by side — normal vs tunneled. The
fix stack: resolver control + egress DNS allow-list (L12 continuity). -->

---

## Correlation: Zeek in the Three-Way

- IDS alert (signature fired) ↔ Zeek log (behavior context) ↔ flow
  (volume/timing)
- The triage answer usually lives *between* sources
- Zeek's conn.log anchors every conversation's timeline slot

<!-- notes: (4 min) The three-way rule (L21) with Zeek's seat named.
cs-072's log-correlation case is the worked instance. -->

---

## Anomaly Detection in Practice

- Per-asset-class baselines (L21) + Zeek behavior logs = anomaly
  inputs
- Alert on *deviation with context*: "this server never RDPs out"
- Season the FP profile: migrations, updates, new services

<!-- notes: (5 min) The honest-FP discipline continues: anomalies need
context or they're just noise with extra steps. cs-067/cs-070
continuity. -->

---

## CS/DS Example: Cluster Job Patterns as Baseline

- Training jobs have rhythm: dataset pulls, long GPU compute, sparse
  egress
- cs-088's mining broke the rhythm — volume + destination + timing
- The baseline *was* the detector; telemetry made it visible

<!-- notes: (4 min) DS framing: their own job patterns are the
baseline — anomaly detection on a fleet they live in. The cs-088
callback lands the stakes. -->

---

## Activity: Name That Traffic (6 min)

Three Zeek/flow excerpts: (a) 60s±2s 2KB to one IP for 8h; (b) 400
unique high-entropy subdomains in 10 min; (c) nightly 5 GB to the
backup server. Classify; which needs a rule, which needs a baseline
entry?

<!-- notes: (6 min) Answers: (a) beacon — rule; (b) tunnel — rule;
(c) backup — baseline entry (expected behavior, not a threat). The
(c) nuance — expected patterns deserve baselines, not alarms — is the
maturity beat. -->

---

## Case Study: cs-073 (5 min)

- DNS-tunneling detection design — from pattern to rule

<!-- notes: (5 min) If used in the teaching slot, run cs-072 here
(rotation per case-index). -->

---

## Formative Check

- Oral: three signals that distinguish C2 beaconing from legit
  polling.

<!-- notes: (2 min) Exit oral: interval regularity, volume uniformity,
destination novelty/allow-list state. -->

---

## References & Next

- Zeek documentation (log reference)
- Diagrams: `diagrams/07-ids-ips-workflow.md`
- **Next (L24):** vulnerability management — finding weaknesses before
  they're used
