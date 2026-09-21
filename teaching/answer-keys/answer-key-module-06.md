---
module: 6
lectures: [L21, L22, L23, L24]
status: complete
artifact-type: answer-key
instructor-only: true
distribution: never-publish-to-students
---

# Answer Key — Module 6: Detection, Monitoring & Vulnerability Management

> **INSTRUCTOR ONLY — contains model answers to graded formative assessments.**
> Links: Plans `modules/module-06-detection-vulnerability/lectures/` · Student pages `docs/lectures/lecture-21…24` · Notes `teaching/speaker-notes/lecture-21…24-speaker-notes.md`

## L21 — Monitoring Foundations

### Formative checks (plan §11)
1. Telemetry family trade-offs: full PCAP (complete, expensive, privacy-heavy) → packet metadata (cheap, less context) → flow records (aggregated, great for baselines, no payload) → logs (app truth, inconsistent formats). "One best source" answers fail — the answer is a tiered mix.
2. Collection architecture: source → sensor/tap → parser/normalizer → storage (hot/cold) → analysis; every stage adds latency/cost — the design question is what to keep where.
3. Baseline: normal-by-hour profile of traffic volumes, top talkers, protocol mix, cadence — the *absence of a baseline* is why alerts can't be prioritized.
4. Sampling trade-off: sampled flow saves money, distorts volume/low-and-slow detection — for teaching: state whether data is sampled before computing anything.
5. Privacy/legality: monitoring policies define scope, retention, access — "we log everything forever" is both a storage and a legal problem.

### Exit ticket
- Flow records answer "who talked to whom, when, how much" — they cannot answer "what was said"; pairing flows with selective PCAP/log capture is the designed answer.
- The first telemetry to enable on a flat network: flow export (switch/router) + DHCP/DNS logs — cheapest inventory and visibility wins.

### Discussion facilitation
- Q4 (cost-vs-coverage): reward tiered answers (full capture only at critical segments, metadata everywhere) over binary choices.

## L22 — IDS/IPS: Signatures & Tuning

### Formative checks
1. NIDS vs HIDS: network sensor sees wire traffic (misses encrypted payloads without inspection, host-local events); host-based sees the endpoint (misses network-only context). Placement answer: both, scoped.
2. Signature vs anomaly: known-bad patterns (precise, brittle, evadable) vs deviations from baseline (novel, noisy, needs a baseline). Detection engineering = both, with different false-positive profiles.
3. False positive/negative: FP = alert without attack (cost: analyst time); FN = attack without alert (cost: breach). Tuning trades between them — and *suppression without review* manufactures FNs.
4. Tuning workflow: alert census → classify (true, noisy-true, false) → scope exclusions (narrow the rule, not the data) → document expiry → re-measure. The "narrow the rule" discipline is the graded core.
5. Inline vs passive: IPS blocks (latency risk, blocking errors are outages) vs IDS detects (no prevention). Placement: IPS at high-value boundaries only, IDS elsewhere.

### Exit ticket
- "Delete the noisy rule" vs "scope it": scoping preserves detection value while removing noise; deletion must be justified by total obsolescence — the documentation difference is the answer.
- Signature evasions: fragmentation, encoding variations, timing splits — cite at least two with the mitigation (stream reassembly, normalized decoding).

### Lab troubleshooting (ruleset lab context)
- Rule never fires: check HOME_NET/EXTERNAL_NET variables first, then direction (`flow:established,to_server`), then the exact content bytes (hex vs ASCII).
- Fires on everything: content match too generic or missing depth/offset — show the byte-window discipline.

## L23 — Zeek & Anomaly Detection

### Formative checks
1. Zeek vs signature IDS: Zeek produces *structured behavioral logs* (conn, dns, http, ssl, files) you query; it's an analysis platform, not primarily an alerter — "Zeek is just another Snort" is the misconception to catch.
2. conn.log essentials: UID joins related logs; durations, bytes, state codes — the UID join across logs is the triage superpower (L26 reuses it).
3. DNS tunneling signatures: long unique subdomains, high entropy labels, TXT/NULL qtype concentration, regular query cadence — the arithmetic (entropy + cadence) is the detection, not a single magic field.
4. Baseline in Zeek: per-host/per-subnet profiles from conn/dns distributions; anomalies = deviation from *own* profile, not global average — NAT-aware grouping expected.
5. HTTP anomalies: odd user agents, unusual methods, rare content types, beacon-like periodicity — two cited signals with reasoning earn full credit.

### Exit ticket
- Anomaly detection's weakness: no baseline, no detection — and attackers can blend into baseline; that's why anomaly complements, never replaces, signatures.
- Why flows first: Zeek/flow telemetry gives cheap breadth; targeted PCAP gives depth — the funnel order is the designed answer.

### Lab troubleshooting (hunt worksheet context)
- Zeek logs empty: wrong interface or missing `LogAscii::use_utc` confusions are common; check the pinned lab config first.
- Entropy script errors: students hand-roll instead of using the provided tooling — redirect to the sheet's functions; correctness of *method* is graded.

## L24 — Vulnerability Management Cycle

### Formative checks
1. Cycle stages: inventory → scan (authenticated) → prioritize → remediate → verify → report; skipping *verify* is the most common real-world failure — closed ≠ fixed.
2. Authenticated scanning value: sees local patch state, config issues, installed software — unauthenticated scans under-report; the diff between the two is the demo payoff.
3. Prioritization stack: base CVSS is *not* risk alone — add KEV/exploitation evidence, EPSS probability, asset criticality, exposure — context inverts the queue (the 9.8-on-test-box vs 7.5-on-internet-gateway case).
4. SLA design: severity × exposure × criticality → time targets; exceptions need owner, compensating control, expiry, approver — no-expiry exceptions are the audit finding.
5. Scanner limitations: false positives/negatives exist; scanners can't see what credentials don't reach, and aggressive scans can harm fragile systems — safe-mode discipline.

### Exit ticket
- The question "scanner says 9.8, do we panic?" — the answer is the four context inputs (exploitation evidence, exposure, criticality, compensations) *before* queue position; panic answers fail.
- Rate limiting/safe-mode: production scans are change-controlled events — timing windows, read-only intent, fragile-system exclusions.

### Case study anchors (cs-063–cs-072) — grading pointers
- **cs-063–cs-066 (L21/L23):** analysis must cite the specific fields/signals (flow asymmetry, DNS entropy, cadence) — conclusions without cited evidence lose half credit.
- **cs-067–cs-069 (L22):** rule/tuning answers need the census → scope → document workflow; "turn it off" fails.
- **cs-070–cs-072 (L24):** prioritization must apply the context stack; base-CVSS-only ordering fails.

## Common misconceptions (module-level)
1. "More alerts = better security" — signal quality beats volume; untuned stacks manufacture fatigue (L22).
2. "AI/ML replaces baselining" — models need the same clean data and still need labeled review; no magic (L21/L23).
3. "Scan = secure" — scanning is measurement; remediation and verification are the program (L24).
4. "Flow data is enough" — flows can't see payloads; tiered telemetry is the design answer (L21).
