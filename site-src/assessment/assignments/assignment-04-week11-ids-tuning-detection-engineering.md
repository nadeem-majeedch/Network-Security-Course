# Assignment 4 — IDS Tuning & Detection Engineering (Week 11)

> **Weight:** 5% · **Due:** end of week 11 · **CLO-9, CLO-12**
> **Deliverable:** tuning analysis (4–6 pages) + one written detection
> rule with rationale. Uses the course dataset (`docs/labs/datasets/`).

## Scenario (simulated)

Your SOC ingests Suricata alerts and Zeek logs from the course range
(Lab-11 dataset: 1 week of traffic, known benign patterns seeded + one
unannounced scripted behavior). Alert volume: ~3,000/day. Your budget:
2 tuning changes and 1 new detection.

## Tasks

1. **Alert economics** (25): quantify the alert classes — volume × triage
   minutes × estimated true-positive rate (build the table from the
   dataset). Rank the pain with numbers, not adjectives.
2. **Tuning proposal** (25): your 2 changes with, for each: the FP driver,
   the exact scoping (what narrows, what stays), the risk you're accepting,
   and the **regression-safety proof** (how you demonstrate no lost TPs —
   replay on the dataset before/after).
3. **New detection** (25): write one detection rule (Suricata-style
   syntax or Zeek script pseudocode) for the unannounced behavior you
   found. Include: the behavioral rationale (what technique it maps to),
   expected FP profile, and the tuning knobs you'd expose.
4. **Escalation criteria** (15): the conditions under which an alert from
   your new rule pages a human (vs queues) — measurable thresholds only.
5. **Reflection** (10): ≤200 words — what the *dataset could not show*
   about production alerting (telemetry limits of the lab).

## Constraints

- All analysis on course datasets only (authorized, simulated).
- The regression-safety proof is the discipline being graded — a tuning
  change without a replay plan caps at 60%.

## Submission

PDF/repo Markdown + the rule file. Rubric: instructor materials.
