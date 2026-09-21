---
case: cs-096
title: Capstone VI — Hypothesis-Driven Threat Hunt (Solution)
difficulty: expert
module: 8
lecture-anchor: L32
clos: [CLO-15]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-096 — Solution: Hypothesis-Driven Threat Hunt Design

> **INSTRUCTOR ONLY.** Model solution for cs-096.

## Model Solution

### 1. Five hunt hypotheses (estate-grounded)

**H1 — Legacy-workstation dormancy.** *Claim:* if the 30
EDR-less legacy workstations were compromised (the estate's only
unmonitored endpoints), we would see either periodic outbound
patterns from their subnet or anomalies in their identity use.
*Uses near-miss artifacts:* the phish-blocked replay showed the
would-be entry path targets workstations — these 30 are the
reachable ones without EDR.

**H2 — User-VLAN east-west staging.** *Claim:* if lateral
movement/staging occurs on user VLANs (Zeek only watches server
VLANs), endpoint-originated SMB/RDP bursts between workstations
would appear in flow records as workstation→workstation spikes —
currently never queried.

**H3 — Cross-account role abuse (AWS).** *Claim:* if a stolen
role were assumed outside its normal pattern (time, source,
sequence), the CloudTrail identity data would show
assumed-role sessions deviating from the per-role baseline the
team has never built.

**H4 — IdP token anomalies post-ZT.** *Claim:* the ZT phase-2
IdP created a new token plane; if session tokens were replayed or
refresh anomalies existed, IdP logs would show refresh patterns
violating per-app session baselines — the plane's *first-ever*
baseline review.

**H5 — DNS egress residual.** *Claim:* despite proxy+DNS
logging, DNS-tunnel-style patterns to the *small number of
non-corporate resolvers* would survive current detection (cs-073's
technique on this estate's actual resolver config).

### 2. Method per hypothesis

| H | Source | Query/analytic shape | Data-quality prerequisite | Falsification condition |
|---|---|---|---|---|
| H1 | fw/flow (legacy subnet), AD sign-ins | periodicity analysis on outbound; identity-use outlier per host | complete host-IP map for the subnet (CMDB) | no periodicity outliers + identity use within role baseline → closed |
| H2 | edge flow, 90 d | workstation→workstation SMB/RDP volume ranking; top-N manual review | flow records complete for user VLANs | top-N all explained (printers, app clients) → closed |
| H3 | CloudTrail, 90 d | per-role session baseline (time/source/sequence); outlier ranking | role inventory + tagging complete | all assumed-role sessions within constructed baseline → closed |
| H4 | IdP logs, 60 d | refresh-interval distribution per app; replay-shape search (same token, 2 IPs) | IdP logging completeness verified first | no refresh outliers, no replay shapes → closed |
| H5 | DNS logs, 90 d | query-length/entropy per client; non-standard-resolver share | DNS logging covers all egress paths (verify!) | no high-entropy long-query outliers to non-standard resolvers → closed |

### 3. No-findings output (all five come back empty)

The empty hunt still ships: (a) **coverage documentation** —
per-hypothesis: technique, data searched, window, method,
falsification result (auditable "we looked for X, here's how,
absent"); (b) **detection candidates** — the queries themselves
become scheduled (cheap) detections with documented false-positive
profiles from the hunt; (c) **telemetry-gap list** — H1's CMDB
prerequisite and H5's resolver-coverage verification each became
their own findings where incomplete; (d) **baseline artifacts** —
H3/H4 produce the first per-role and per-app baselines, which the
SOC uses for anomaly detection *forever after*. An empty hunt
re-armed the estate.

### 4. SOC handoff rule

- **→ Detection:** hypotheses whose query is cheap, low-FP, and
  meaningfully scheduled (H5's entropy rule, H2's top-N weekly).
- **→ Telemetry request:** hypotheses blocked by data gaps (H1's
  CMDB completeness, H5's resolver coverage) — filed as engineered
  requests, not hunter complaints.
- **→ Quarterly re-hunt:** high-value hypotheses whose data
  quality doesn't yet support scheduling (H3/H4 until baselines
  season).
- **The boundary rule:** hunters stop at validated query +
  documented FP profile; SOC owns tuning/ops. The hunt does *not*
  absorb alert backlog — if the SOC can't resource the handoff,
  the detection *doesn't ship* (worse to have an untuned rule
  than none, per cs-070's alert-tuning economics).

## Alternative Solutions

- **MITRE-coverage-driven hunt** (attack the coverage-map gaps):
  defensible, but the vendor map is unvalidated — this design
  prefers estate-grounded hypotheses and uses the coverage map as
  a secondary input.
- **Intel-driven hunt** (hunt for specific actor TTPs): valuable
  at scale; with 2 hunters/2 weeks, estate-grounded beats
  actor-tracking.

## Tradeoffs

- Estate-grounded vs framework-driven: relevance vs systematic
  coverage — the two approaches alternate quarterly.
- Baseline-building cost vs immediate hunting: H3/H4 pay a
  baseline tax first; the payoff is permanent anomaly detection.

## Common Mistakes

- Hypotheses that can't be falsified ("look for weird stuff").
- Hunting where telemetry is already rich (comfortable, useless).
- Treating empty results as failure (no coverage documentation).
- Handing raw queries to the SOC without FP profiles.

## Instructor Prompts

- "Which hypothesis is strongest *because* of the near-miss
  artifacts?"
- "What makes H3's baseline work a permanent asset rather than a
  one-off?"
- "Why refuse to ship a detection the SOC can't resource?"

## Rubric (10 pts)

| Criterion | Pts |
|---|---|
| 5 falsifiable, estate-grounded hypotheses (1+ from near-misses) | 3 |
| Method per hypothesis: source, shape, prerequisite, falsification | 3 |
| No-findings output designed (coverage/candidates/gaps/baselines) | 2 |
| SOC handoff rule with the boundary drawn | 2 |

## Safety Notes

- Simulated; authorized passive hunting on owned estate.
