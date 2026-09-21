---
lecture: L28
title: SOC Operations & Threat Hunting
module: 7
week: 14
hours: 2
clos: [CLO-12]
difficulty: advanced
status: complete
artifact-type: teaching-plan
---

# L28 — SOC Operations & Threat Hunting

## 1. Overview & Prerequisites

- **Prerequisites:** L23 (Zeek hunts/baselines), L26–L27 (what happens *after* a hunt finds something), L21 (pipeline/telemetry tiers).
- **Position:** closes Module 7 by flipping the model: from alert-driven reaction to hypothesis-driven hunting, wrapped in the SOC operating context (processes, metrics, maturity). The guided hunt is the direct rehearsal for the capstone's monitoring/hunting deliverable and Assignment 6's hunt extension.
- **Faculty prep:** prepare the hunt dataset (7 days of range Zeek + flow + proxy logs, with two planted low-and-slow behaviors distinct from L26's loud incident); prepare the PEAK/pyramid-bridge framework handout; ready Quiz-5 logistics (administered end-of-slot per calendar).
- **Common misconceptions:** "hunting is random grep"; "the SOC's job ends at closing tickets"; "more alerts = better detection"; "maturity = buying more tools."

## 2. Learning Objectives

By the end of this lecture, students can:

1. Describe SOC operating structure: tiered triage roles, shift/handover discipline, escalation to IR (L25 links), and the alert-queue lifecycle (Understand).
2. Formulate a hunt hypothesis from threat intel or ATT&CK gap analysis: behavior → data source → query plan → decision criteria (Create).
3. Execute a guided hunt across Zeek/flow/proxy data: pivot method, evidence logging, and the documented negative result (hunting's other product) (Apply/Analyze).
4. Design SOC metrics that measure coverage and quality (precision, MTTD/MTTA/MTTR, technique-coverage map) without gaming them (Evaluate/Create).
5. Relate SOC maturity models to concrete investment decisions (detections → automation → analytics) (Evaluate).

## 3. Detailed Concepts

### 3.1 SOC operations reality
- Tier model: T1 triage (runbook-driven validation — L26 method), T2 investigation (scoping/correlation), T3/IR handoff (L25 authority); detection engineering as a distinct function feeding T1 (L22/L23 artifacts are its products).
- Handover discipline: shift notes as evidence artifacts (open incidents, watch items, pending detections); the "watch item" concept — indicators you're tracking without an incident.
- Queue hygiene: every alert dispositioned (true/false/benign-true) *with a reason*; dispositions feed tuning (L22) and coverage maps.

### 3.2 Hunt method (the graded craft)
- Hypothesis-first loop (PEAK-style framing): **hypothesis** (attacker does X via Y leaving Z evidence) → **data** (which telemetry? L21 tiers) → **query plan** (specific, executable) → **decision criteria** (what confirms/refutes) → **log** results either way.
- Intel-driven entry points: a new TTP report (e.g., DNS-over-HTTPS abuse pattern), a KEV-addition (L24 link — "are we exposed?"), an industry peer's sharing-list indicator.
- Gap-driven entry points: ATT&CK coverage map (which techniques have *no* detection?) → hunt where sensors are blind → often ends in a new detection (loop to L22).
- The negative result is a product: "hunted for X across 7 days of Y telemetry; not present; coverage note filed" — this is how hunts compound into assurance.

### 3.3 Pivoting craft (hands-on core)
- From indicator → context: external IP → which internal hosts talked (flow/conn) → what protocol/timing (L23 cadence math) → which identities (auth/proxy logs) → asset owner (L24 inventory).
- From behavior → candidates: beacon cadence query (L23 three-variable test), staging patterns (east-west burst then egress), new-service appearances (L23 baselines).
- Discipline: every pivot recorded in the hunt log (query + result + next step) — the hunt log is the evidence artifact (and the capstone deliverable's model).

### 3.4 SOC metrics that mean something
- Detection: technique-coverage percentage (ATT&CK-mapped), detection precision (from dispositions), time-to-detect for *injected* test events (purple-team validation — honest numbers).
- Response: MTTA (alert → human), MTTR by severity, incident recurrence rate (L27 link).
- Anti-metrics (what to avoid gaming): alerts-closed/day, rules-count, dashboard-count — measure outcomes, not activity.
- Reporting cadence: weekly ops review (queue health), monthly program review (coverage/metrics), feeding budget asks (L27 action items).

### 3.5 Maturity as investment sequencing
- Stages: log-everything-but-blind → tuned-detection core (L21–L23 work) → documented hunts/coverage (today) → automation/soar-class response → analytics/ML-assisted triage (with the same skepticism you apply to any claim — validate like L22 rules).
- Investment rule: each stage's value depends on the previous one's quality — automating an untuned pipeline automates chaos.

## 4. Teaching Sequence (120 Minutes)

| Time | Segment | Instructor moves |
|---|---|---|
| 0–10 | Recap: tabletop decisions | One inject re-run as a triage decision (quick) |
| 10–30 | Core: SOC structure + queue lifecycle | Tier diagram; disposition taxonomy; handover-note anatomy |
| 30–55 | Core: hunt method | PEAK-style loop on one worked hypothesis (intel → query → criteria); negative-result framing |
| 55–65 | Break | — |
| 65–100 | **Guided hunt lab** (teams of 3) | Two hypotheses on the 7-day dataset: (A) DNS-over-HTTPS abuse pattern, (B) low-and-slow staging; hunt logs required |
| 100–110 | Hunt debrief | Teams report findings *or* negative results with coverage notes |
| 110–120 | Wrap + formative | Exit ticket; **Quiz 5** (10 min); Module-8 trailer: "forensics: proving what happened" |

## 5. Technical Examples

```
# Hypothesis A (intel-driven): "Users tunnel via DoH to bypass proxy policy."
# Data: proxy + dns logs (L21 tiers), 7 days.
# Query plan: dns.log → count external DoH-provider queries per client/hour;
#   correlate with proxy-log absence for those clients (bypass signature).
# Decision criteria: >90% of client's DNS via DoH + proxy volume collapse = confirmed.

# Hypothesis B (gap-driven): "Low-and-slow staging: nightly small SMB bursts."
# Data: conn.log + flow (7d). Query plan (L23 style):
zeek-cut ts id.orig_h id.resp_h id.orig_b id.resp_b < conn.log |
  awk '$4 > 1000 && $4 < 5000 {print $1, $2, $3}' | sort | uniq -c | sort -rn | head
# Decision criteria: same src→dst pair, nightly cadence, growing byte counts.

# Hunt log entry (the graded artifact):
#   H-2026-09-14-A | Hypothesis: ... | Data: ... | Queries: <saved>
#   Result: negative | Coverage note: T1071.004 partial (no payload visibility)
#   Follow-up: request proxy TLS-fingerprint telemetry (ticket DET-142)
```
Expected teaching points: hypotheses are falsifiable statements, not vibes; negative results carry coverage notes that drive the next data request; the hunt log mirrors L26's documentation discipline.

## 6. Discussion Questions

1. Why is "we hunt when we're bored" not a hunting program? What makes the loop compound?
2. Your best hunt keeps returning negative across 90 days. What are the three possible conclusions, and how do you distinguish them?
3. Which SOC metric is most gameable, and what pairing prevents the gaming?
4. Where does automation help T1 most — and where does it actively harm (think L22 FP dynamics)?
5. Your ATT&CK coverage map shows T1567 (exfil) detections rely solely on proxy logs. What's the hunt — and the data request — that closes the gap?

## 7. Student Activity

**Guided hunt lab (35 min, teams of 3):** execute both hypotheses (A: DoH bypass; B: nightly staging) on the 7-day dataset; maintain the hunt log (hypothesis → queries → results → decision). One hypothesis yields a positive (planted), one yields a documented negative with a coverage note. Deliverable: two hunt-log entries — the template for the capstone hunting deliverable.

## 8. Problem-Solving Case

**Primary case — cs-086 "Beaconing hunt across proxy and DNS logs" (advanced):**
Intel bulletin (provided): a campaign beaconing via HTTPS to rotating CDN-fronted domains, ~15-minute cadence, small POST bodies. Students design and run the hunt: (a) translate the TTP into observable properties (cadence + POST pattern + new-domain novelty), (b) write the query plan across proxy + conn logs, (c) execute on the dataset (planted: one host, 15-min POST cadence), (d) produce the escalation package for L26 triage: evidence citations, scope-lite (one host), and the detection proposal for L22 (rule idea + expected FPs).
**Linked cases:** cs-085 (hunt-hypothesis design), cs-087 (SOC metric review), cs-088 (insider exfil detection), cs-089 (SIEM use-case tuning), cs-090 (tabletop inject series).
*(Model solutions: instructor answer-key set, Module 7.)*

## 9. Formative Assessment

1. Name the five elements of a hunt hypothesis (framework-form).
2. What makes a negative hunt result valuable rather than wasted effort?
3. Order the pivot: external IP → host → identity → owner — which dataset answers each hop?
4. Give one outcome metric and one activity metric — and why the second one corrupts incentives.
5. What distinguishes a watch item from an incident?
*(Answer key: instructor set, Module 7.)*

## 10. Summary & Key Takeaways

- Hunting is hypothesis-driven falsification over known telemetry; its products are findings *and* coverage assurance.
- SOC health = queue discipline + honest metrics + escalating maturity built on tuned detection.
- Everything from Modules 1–7 converges here: protocols → attacks → architecture → detection → response → hunting.

## 11. References

- PEAK Framework (SANS) — hunt operations methodology; Tahi/TaPlatform hunting guides (practitioner refs).
- MITRE ATT&CK + ATT&CK Navigator — coverage-map practice; D3FEND — countermeasure mapping.
- NIST SP 800-61 — SOC/IR interface; CIDNE-style handover patterns (practitioner literature).
- SQERT/ops-metrics literature — MTTA/MTTR definitions (used consistently with L26–L27).

## 12. CLO Mapping

| CLO | Where in this lecture | Assessed via |
|---|---|---|
| CLO-12 | §3.1–3.5 hunt method + SOC metrics; guided hunt | Assignment 6 (today), Quiz 5 (today), Capstone, Lab-14 |
