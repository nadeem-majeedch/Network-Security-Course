# L28 — SOC Operations & Threat Hunting

## 1. Learning Objectives

By the end of this session you can: (1) describe SOC structure — tiered triage, shift handover, escalation to IR; (2) formulate a hunt hypothesis (behavior → data source → query plan → decision criteria); (3) execute a guided hunt across Zeek/flow/proxy data and log the *negative* result properly; (4) design SOC metrics that measure coverage and quality without gaming; (5) sequence maturity investments.

## 2. Key Definitions

| Term | Definition |
|---|---|
| SOC tier model | T1 triage (runbook) → T2 investigation → T3/IR handoff; detection engineering feeds T1 |
| Disposition | Every alert's outcome: true-positive / false-positive / benign-true — with a reason |
| Hunt hypothesis | Falsifiable statement: attacker does X via Y, leaving evidence Z |
| Hunt log | Hypothesis → queries → results → decision — the evidence artifact either way |
| Negative result | "Hunted for X over Y data, not present" + coverage note — assurance, not waste |
| Coverage map | ATT&CK techniques with/without detections — the honest gap list |
| Watch item | Indicator tracked across shifts without (yet) an incident |
| Anti-metrics | Activity counts (alerts closed, rules written) that reward the wrong behavior |

## 3. Detailed Explanations

### 3.1 SOC operations reality
- **Tiers:** T1 validates alerts against runbooks (L26's method, compressed); T2 investigates/scopes; T3 + IR take over per the L25 authority matrix. **Detection engineering** is a distinct function feeding T1 — your L22/L23 artifacts are its products.
- **Queue hygiene:** every alert dispositioned *with a reason*; dispositions feed tuning (L22) and the coverage map.
- **Handover discipline:** shift notes as evidence artifacts — open incidents, watch items, pending detections. The **watch item** concept: indicators you track without (yet) an incident.

### 3.2 The hunt method (the graded craft)
Hypothesis-first loop: **hypothesis** (attacker does X via Y leaving Z evidence) → **data** (which telemetry? L21 tiers) → **query plan** (specific, executable) → **decision criteria** (what confirms/refutes) → **log** results either way. Entry points: **intel-driven** (a new TTP report, a KEV addition — L24 link), **gap-driven** (coverage map shows a technique with no detection → hunt where sensors are blind → often ends in a new detection, looping to L22). The **negative result is a product**: "hunted for X across 7 days of Y; not present; coverage note filed" — this is how hunts compound into assurance.

### 3.3 Pivoting craft (hands-on core)
- Indicator → context: external IP → which internal hosts talked (flow/conn) → protocol/timing (L23 cadence math) → identities (auth/proxy logs) → asset owner (L24 inventory).
- Behavior → candidates: beacon cadence (L23's three-variable test), staging patterns, new-service appearances (L23 baselines).
- Discipline: every pivot recorded in the hunt log (query + result + next step) — the capstone hunting deliverable uses exactly this format.

### 3.4 SOC metrics that mean something
- **Detection:** technique-coverage % (ATT&CK-mapped), precision (from dispositions), time-to-detect for *injected* test events (purple-team validation — honest numbers).
- **Response:** MTTA (alert → human), MTTR by severity, incident recurrence (L27 link).
- **Anti-metrics to avoid:** alerts-closed/day, rule counts, dashboard counts — they reward activity, not outcomes.
- Cadence: weekly ops review (queue health), monthly program review (coverage/metrics) — feeding budget asks (L27 action items).

### 3.5 Maturity as investment sequencing
Stages: log-everything-but-blind → tuned-detection core (L21–L23) → documented hunts/coverage (today) → automation/SOAR-class response → analytics-assisted triage (validated like any L22 rule). Investment rule: **each stage's value depends on the previous stage's quality** — automating an untuned pipeline automates chaos.

## 4. Network Diagram: hunt loop + coverage

```
 Intel / coverage gap
        ▼
 [Hypothesis] → [Data (L21 tiers)] → [Query plan] → [Run] → [Decision]
        ▲                                                   │
        │            ┌── positive ──► escalate (L26 triage) ┘
        └── refine ◄─┴── negative ──► coverage note + data request
 Detection backlog ←──────────┘ (new rules → L22)
```

## 5. Protocol Examples

- **Hypothesis A (intel-driven):** "Users tunnel via DoH to bypass proxy policy." Data: dns + proxy logs, 7 days. Query: DoH-provider query counts per client/hour vs proxy-volume collapse. Criteria: >90% DNS via DoH + proxy collapse = confirmed.
- **Hypothesis B (gap-driven):** "Low-and-slow staging: nightly small SMB bursts." `zeek-cut ts id.orig_h id.resp_h id.orig_b < conn.log | awk '$4>1000 && $4<5000' | sort | uniq -c | sort -rn | head` — criteria: same src→dst, nightly cadence, growing bytes.
- **Hunt-log entry (the graded artifact):** `H-2026-09-14-A | Hypothesis… | Data… | Queries… | Result: negative | Coverage note: T1071.004 partial (no payload visibility) | Follow-up: ticket DET-142`.

## 6. Configuration Concepts (concept level)

- Disposition taxonomy configured in the SIEM; watch-item register per shift.
- Coverage map maintained in ATT&CK Navigator; review monthly.
- Hunt-log template (as above) — versioned with the detection backlog.

## 7. Security Implications

- Hunting is hypothesis-driven *falsification* over known telemetry — products are findings **and** coverage assurance.
- SOC health = queue discipline + honest metrics + maturity built on tuned detection.
- Modules 1–7 converge here: protocols → attacks → architecture → detection → response → hunting.

## 8. Realistic Organizational Scenario

**The beaconing hunt (running case).** Intel bulletin (provided): a campaign beaconing via HTTPS to rotating CDN-fronted domains, ~15-minute cadence, small POST bodies. You translate the TTP into observable properties (cadence + POST pattern + domain novelty), write the query plan across proxy and conn logs, execute on the 7-day dataset (planted: one host, 15-min POST cadence), and produce the escalation package for L26 triage: evidence citations, scope-lite, and the L22 detection proposal with expected FPs. Full case: **cs-086**; the guided hunt (hypotheses A + B) is the in-session lab; Quiz 5 closes the session.

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "Hunting is random grep" | It's hypothesis-driven falsification with logged method. |
| "The SOC's job ends at closing tickets" | Dispositions feed tuning; coverage maps drive the program. |
| "More alerts = better detection" | Precision and coverage are the metrics; volume is cost. |
| "A negative hunt failed" | It's assurance — *if* logged with a coverage note. |
| "Maturity = buying more tools" | Each stage depends on the previous stage's quality. |

## 10. Classroom Activities

1. **Guided hunt lab (teams of 3):** execute hypotheses A and B on the 7-day dataset; maintain hunt logs; one positive (planted), one documented negative with coverage note.
2. **Disposition drill:** five alerts → dispositions with reasons; compute the session's precision.
3. **Metric redesign:** replace one anti-metric with an outcome metric; defend the change.

## 11. Problem-Solving Questions

1. Why is "we hunt when we're bored" not a hunting program — and what makes the loop compound?
2. Your best hunt returns negative across 90 days: what are the three possible conclusions, and how do you distinguish them?
3. Which SOC metric is most gameable, and what pairing prevents gaming?
4. Where does automation help T1 most — and where does it actively harm (think L22 FP dynamics)?
5. Your coverage map shows T1567 (exfil) detections rely solely on proxy logs: what's the hunt — and the data request — that closes the gap?

## 12. Exit Ticket

1. Name the five elements of a hunt hypothesis (framework form).
2. What makes a negative hunt result valuable rather than wasted effort?
3. Order the pivot: external IP → host → identity → owner — which dataset answers each hop?
4. Give one outcome metric and one activity metric — and why the second corrupts incentives.
5. What distinguishes a watch item from an incident?

*(Answers: `the instructor answer-key collection (not published)`.)*

## 13. References

- SANS PEAK Framework — hunt operations methodology.
- MITRE ATT&CK + ATT&CK Navigator — coverage mapping; D3FEND — countermeasures.
- NIST SP 800-61 — SOC/IR interface.
- Zeek/nfdump/proxy documentation — the pivot toolset.

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-12 | §3.2–3.4 hunt method + metrics | Assignment 6 (W13), Quiz 5 (W14), Capstone, Lab-14 |
