# cs-070 — Alert-Tuning Backlog Prioritization

> **Simulated scenario.** The SOC, alert classes, and constraints are fictional.

## Difficulty & Domain

- **Difficulty:** Advanced · **Domain:** IDS/IPS alerts · **CLO:** CLO-9
- **Est. time:** 15 minutes · **Anchor:** L22 (IDS/IPS — Signatures & Tuning)

## Scenario

A 6-analyst SOC drowns in 4,200 alerts/day (below). The tuning backlog
holds 9 candidate changes; you can execute **3 this sprint**. Prioritize
with an explicit *value framework* — analyst-minutes reclaimed × risk of
missing true positives — and defend leaving the biggest-volume alert
untuned (the trap).

## Stakeholders

- **Analysts** — fatigue is real; triage quality decays after alert #400.
- **SOC manager** — sprint commitment; wants the framework, not vibes.
- **CISO** — "don't tune away our detection" is the standing fear.
- **Detection engineering** — owns the 9 candidates.

## Network Context

Alert classes (daily counts × avg triage minutes × true-positive
estimate):

| Class | /day | min/alert | TP rate | Notes |
|---|---|---|---|---|
| A. EDR "suspicious script" | 900 | 4 | ~1% | top noise source |
| B. Proxy policy violations (streaming) | 1,400 | 2 | ~0% | policy, not security |
| C. IDS scanner false-positives (scanner detected as scanner) | 700 | 3 | ~0% | our own vuln scanner |
| D. Impossible-travel VPN | 40 | 15 | ~8% | noisy but signal-bearing |
| E. Cloud flow anomaly | 25 | 20 | ~15% | new, untrusted |
| F. Malware AV detections | 60 | 10 | ~35% | real but handled |
| G. Data-staging heuristic | 8 | 30 | ~60% | low volume, high value |
| H. SIEM correlation rule w/ broken lookup (fires on ALL users) | 300 | 5 | ~0.3% | *broken*, not noisy |

**The 9 candidates:** (1) auto-close B with weekly digest; (2) baseline
A by host-class (dev vs prod); (3) suppress C by scanner-source IP; (4)
enrich D with HR geo before paging; (5) tune E thresholds after 30-day
baseline; (6) fix H's broken lookup; (7) raise G's threshold; (8) bundle
F into auto-triage playbook; (9) kill a legacy duplicate of A.

## Student Task

1. Define your **value framework** explicitly (the formula) and apply it:
   rank all 9 candidates, pick **your 3**, show the math.
2. Explain the **biggest-volume trap**: why B (1,400/day) is *not* the
   top pick (what does the math actually say about analyst-minutes vs
   risk?), and when it *would* be.
3. Name the **regression-safety rule** your changes must follow (how do
   you prove "we didn't tune away detection"?) — the CISO-facing
   artifact.

## How to Approach This (Reasoning Scaffold)

- Minutes reclaimed is *not* the whole formula: a broken rule (H) fires
  300× on garbage *and* trains analysts to ignore a high-value signal
  class — trust damage compounds.
- Auto-closing a 0%-TP class (B) is nearly free risk-wise — but it's
  also the *least* interesting engineering; the interesting question is
  whether it beats fixing H (trust restoration) and D-enrichment (TP-
  bearing noise).
- Regression safety: before/after replay on historical data — the
  artifact that turns "trust me" into "here's the diff."

## CLO Mapping

- **CLO-9** — Alert-tuning economics and regression discipline.

## Safety Notes

- Design exercise; no real alert data.
