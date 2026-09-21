# Lab-14 — IR Tabletop + Guided Threat Hunt

## 1. Lab Overview & CLO Mapping

Two IR disciplines in one block: a **tabletop** (L25/L27 judgment under
pressure — decisions, communications, lessons-learned) and a **guided threat
hunt** (L28's hunting over the course datasets — hypothesis-driven, evidence-
recorded). *CLO-11* (IR lifecycle execution) + *CLO-12* (monitoring/detection
design decisions). Reference lectures: L27 (eradication/recovery/lessons),
L28 (SOC operations & hunting).

## 2. Learning Objectives

By the end you can: (1) execute a tabletop scenario with role discipline and
on-record decisions; (2) build eradication/recovery sequences that respect
dependency order and credential-hygiene reality; (3) run lessons-learned that
are blameless and actionable; (4) form, test, and record hunt hypotheses over
flow/log evidence; (5) distinguish hunt findings (new detections) from alert
response.

## 3. Prerequisites

Lab-13 submitted (its incident is the tabletop's backstory); L27/L28 attended;
Lab-11/12 outputs (baseline + rules) are hunt inputs.

## 4. Estimated Duration

120 minutes: tabletop 55 · hunt 45 · lessons + write-up 20.

## 5. Required Software & Hardware

- Tabletop: printed scenario cards + role cards (lab sheet); timer.
- Hunt: lab-range VM, datasets `lab11-flows.csv` + `lab13-incident.pcap`
  (processed through Zeek per Lab-12) + your Lab-11 ruleset as a *candidate*
  detection set.

## 6. Setup Instructions

> **Command status:** ✅ verified shapes; ⚠️ environment steps.

1. ⚠️ Tabletop roles assigned by the instructor: incident commander, tech lead,
   comms lead, scribe, executive (injected pressure). Cards handed at start —
   no pre-reading (that's the design).
2. ✅ Hunt workspace: process the corpus if not already done:

```bash
zeek -r docs/labs/datasets/lab13-incident.pcap LogAscii::use_utc=T   # ✅ verified shape
```

3. ✅ Hunt queries build on Lab-11's flow shapes (verified):

```python
# hypothesis worksheet: state H, then query; record result per H
# H1: "another host beacons like .102 did" → group DNS by src, test cadence
# H2: "the scan host touched other subnets" → group flows by src==attacker
```

## 7. Authorization & Safety Notes

- **Authorization basis:** a no-live-systems exercise — tabletop decisions and dataset-only hunt queries; detection pilots on live paths require change control.

- Tabletop: no live systems are touched by design — decisions and
  communications are the deliverable. Role pressure stays in-scenario
  (debrief separates person from performance).
- Hunt: analysis of course datasets only; hunt *queries* never go live against
  anything (detection pilots are a change-controlled process — say it).

## 8. Student Tasks

**Tabletop (55 min, timed):**
1. Scenario "Meridian returns": three weeks after Lab-05's fix, a backup
   server re-appears in DNS anomalies *and* a helpdesk ticket mentions a
   "slow" file server. Play it: triage call, severity, containment choice,
   eradication order (which credentials rotate first?), recovery go/no-go
   gates, comms (internal now; legal gates external).
2. Scribe records every decision + owner + time; the executive injects two
   pressure moments (per the card: "kill it now" and "is this public yet?").
3. Lessons-learned (20 min): blameless format — systemic language ("the
   process allowed…"), each finding → owned action + date + verification.

**Guided hunt (45 min):**
4. Write ≥3 hypotheses on the worksheet (H1/H2 above + one of your own from
   the baseline). For each: state it, run the query, record result, verdict
   (confirmed/refuted/inconclusive), and *what detection would catch it
   permanently*.
5. Detection delta: compare your hunt-derived detections to your Lab-11
   ruleset — name one rule to add and one to tune, with the evidence.

## 9. Expected Observations

- The tabletop's hard step is eradication order: credentials before host
   rebuilds, identity infra before app tiers — teams that "restore everything
   at once" re-compromise on paper (the debrief shows it).
- Pressure moments expose the comms/decision split: the correct answer is
   present options with evidence, decide on record — not silent compliance.
- Hunt H2 confirms the scan host reached only the server subnet *in this
   window* — inconclusive beyond it; the verdict vocabulary matters.

## 10. Analysis Questions

1. Which tabletop decision would have failed under a *written* plan vs
   improvised? What does that say about runbook preconditions (L25)?
2. Your lessons-learned produced three actions. Which are process fixes vs
   detection fixes, and who verifies each at the next exercise?
3. Hunt verdict "inconclusive" is a legitimate result. What is the follow-up
   plan for an inconclusive high-value hypothesis — and what does "we found
   nothing" fail to say?
4. How does the hunt's detection-delta feed the metrics wall (L28: coverage,
   time-to-tune)? Name the metric your delta changes.
5. If the backup server's anomaly had been *real* re-compromise, which of your
   go/no-go gates would have stopped recovery — and which was theater?

## 11. Troubleshooting

- Tabletop stalls → re-read the scenario card's inject; the IC must decide
  with incomplete data — that's the job; log the uncertainty.
- Hunt queries return everything → your grouping key is too coarse (same
  lesson as Lab-11 Q1); group by (src,dst,qtype/ports).
- Lessons drift to blame → enforce the sentence stem ("the process allowed…");
  the scribe rewrites personal phrasing.

## 12. Cleanup Instructions

- Scenario/role cards returned (reused across sections); worksheets exported;
  datasets untouched.

## 13. Submission Requirements

- Scribe log (decisions · owners · times) + lessons-learned table (finding →
  action → owner → date → verification).
- Hunt worksheet (≥3 hypotheses with queries, results, verdicts).
- Detection-delta note (add/tune with evidence).
- Analysis answers (5). Due: start of Week 15 session (feeds Assignment 6/7).

## 14. Expected Output & Evidence

| Artifact | Passing evidence |
|---|---|
| Scribe log | timestamped decisions incl. the pressure moments |
| Lessons table | blameless, actionable, owned, dated |
| Hunt worksheet | H stated before query; verdicts use the vocabulary |
| Detection delta | evidence-linked add/tune recommendations |

## 15. Grading Rubric

| Criterion | Weight | Full-credit behavior |
|---|---|---|
| Evidence discipline | 40% | recorded decisions; hunt H→query→verdict chains |
| Mechanism accuracy | 30% | eradication order, credential hygiene, hunt method |
| Analysis depth | 20% | gates vs theater (Q5); metrics linkage (Q4) |
| Safety & policy | 10% | role discipline; analysis-only hunting |

## 16. Instructor Answer Key

Scenario script + injects, eradication order reference, hunt expected
results, grading notes: `the instructor answer-key collection (not published)`
(instructor-only).
