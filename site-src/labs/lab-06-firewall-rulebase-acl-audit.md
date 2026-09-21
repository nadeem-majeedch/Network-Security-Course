# Lab-06 — Firewall Rulebase Build & ACL Audit (pfSense)

## 1. Lab Overview & CLO Mapping

You will implement Lab-05's design on a live lab firewall: build pfSense rules
for two zones, then *audit* a supplied broken rulebase for shadowing, orphaned
allows, and any/any residue. This is the graded **Lab Pract-1**. *CLO-4* —
configure and verify firewall/ACL policy sets and audit an existing rule base.
Reference lectures: L10 (concepts & placement), L11 (rulebase engineering).

## 2. Learning Objectives

By the end you can: (1) translate policy tables into ordered pfSense rules with
documented intent; (2) verify first-match behavior empirically (hit counters,
test connections); (3) audit a rulebase for shadowed, redundant, and orphaned
rules using hit-count data; (4) apply direction-awareness (`in`/`out`,
source/destination) without trial-and-error; (5) produce a change record with
rollback.

## 3. Prerequisites

Lab-05 submitted (your egress table is the input); L10/L11 attended.

## 4. Estimated Duration

120 minutes: build 45 · verify 25 · audit the broken rulebase 35 · change
record 15.

## 5. Required Software & Hardware

- Lab range: pfSense VM (pinned version on the lab sheet), two test VMs
  (user-zone, server-zone), an "audit" pfSense config export (supplied).
- Browser for the pfSense GUI; SSH/console optional.

## 6. Setup Instructions

> **Command status:** ✅ verified at authoring time; ⚠️ reference shape.

1. ⚠️ Snapshot your pfSense VM (`take-snapshot lab06-start`) — every change gets a rollback point.
2. ⚠️ Confirm test VMs: user-zone 10.20.10.50, server-zone 10.20.30.10; ping across (baseline reachability per the range map).
3. ⚠️ pfSense: Firewall → Rules. Create aliases first (`Firewall → Aliases`):
   `NET_CORP 10.20.10.0/24`, `NET_SERVERS 10.20.30.0/24`, `PORT_WEB 80,443`.
4. Build rules per your Lab-05 egress/policy table (example shape):

| # | Action | Proto | Source | Dest | Port | Intent |
|---|---|---|---|---|---|---|
| 10 | Pass | TCP | NET_CORP | NET_SERVERS | PORT_WEB | corp→web tier only |
| 20 | Block | Any | NET_CORP | NET_SERVERS | Any | default-deny with log |

5. ✅ Verification helpers (run on the test VMs — these are range-internal):

```bash
# from user-zone VM: expected pass/block outcomes per your rules
curl -m 3 http://10.20.30.10/ ; echo "exit=$?"        # ✅ tested shape: exit 7/28 = refused/timeout when blocked
ping -c 1 10.20.30.10                                  # ICMP is its own rule — check yours
```

## 7. Authorization & Safety Notes

- **Authorization basis:** only the course-owned pfSense and range VMs listed on the lab sheet may be configured or tested; anything outside that boundary is prohibited.

- Only range VMs; the pfSense you configure is course-owned. Rule changes go
  through the change-record template (below) — unsnapshotted rulebase surgery
  that breaks another student's path is the classic range incident.
- No rule may target anything off the range.

## 8. Student Tasks

1. **Build:** implement ≥8 rules implementing Lab-05's policy for corp→servers
   and corp→egress (via the range proxy). Every rule gets a description that
   states *intent and author* (rulebase hygiene, L11).
2. **Verify first-match:** create a deliberately shadowed pair (broad pass
   above specific block) on a scratch alias, observe the hit counter, then
   *fix* it — screenshot before/after.
3. **Audit the supplied broken rulebase** (config export on the lab sheet).
   Deliver a findings table: rule # · problem class (shadowed / orphaned /
   any-any / direction error / missing log) · evidence (hit count, test result) · fix.
4. **Direction drill:** apply one rule on the wrong interface direction
   deliberately, test, record the symptom, correct it. (Top real-world ACL error —
   say why in your notes.)
5. **Change record:** one-page record for your build: intent, rules added,
   test path (which connections verified which rule), rollback = snapshot id.

## 9. Expected Observations

- Hit counters increment on the *first matching* rule only — the empirical
  proof of first-match-wins.
- Wrong-direction rules produce silent drops with zero hits on the rule you
  meant to test — the symptom is traffic dying with no counter movement.
- The broken rulebase contains ≥1 any/any (usually mid-table), ≥2 shadowed
  specifics, ≥1 orphan (hits=0 since creation), ≥1 missing-log deny.

## 10. Analysis Questions

1. First-match semantics make rule order load-bearing — what does that imply
   about how a rulebase rots as rules are appended over years?
2. Stateful firewall: why did you not need explicit "return" rules for corp→web,
   and when would you (stateless ACL on a router — which of your Lab-05 zones
   might still use them)?
3. Your audit found an orphaned permit with zero hits. Why is deletion still a
   *decision* (what do you check first) rather than reflexive cleanup?
4. Which is riskier: an unlogged permit or an unlogged deny — argue both, then
   commit with reasoning.
5. How does your change record map to the change-control discipline from L11
   (intent, test path, rollback)? What did the snapshot save you from?

## 11. Troubleshooting

- Locked out of pfSense GUI → you applied a rule blocking the management
  subnet; use console (option 8) or revert the snapshot — then *say so* in the
  change record.
- Rule "doesn't work" → checklist: direction? interface? aliases spelled right?
  floating vs interface tab? gateway/return route? Check counters before
  editing — zero hits means it never matched.
- Test VM curl hangs (28) vs refused (7) → timeout = dropped (firewall), refused
  = reached but service closed (not a firewall problem).

## 12. Cleanup Instructions

- Revert to `lab06-start` snapshot **after** instructor sign-off; export your
  final config XML for submission first. Delete scratch aliases/rules.

## 13. Submission Requirements

- Final pfSense config export (XML) + screenshot set: build, shadow-demo
  before/after, audit findings.
- Audit findings table (broken rulebase) with evidence per row.
- Change record (intent/tests/rollback).
- Analysis answers (5). Due: end of session (Pract-1 grading) — late = practical
  resit rules apply.

## 14. Expected Output & Evidence

| Artifact | Passing evidence |
|---|---|
| Config export | ≥8 intent-documented rules implementing Lab-05 |
| Shadow demo | before/after counters proving first-match |
| Audit table | ≥5 findings, each with evidence class + fix |
| Change record | test path maps connections→rules; rollback named |

## 15. Grading Rubric

| Criterion | Weight | Full-credit behavior |
|---|---|---|
| Evidence discipline | 40% | counters/screenshots for every claim; change record complete |
| Mechanism accuracy | 30% | first-match, direction, statefulness all correct |
| Analysis depth | 20% | rot/audit reasoning (Q1–Q3) |
| Safety & policy | 10% | snapshots used; range-only; lockout incident reported honestly |

## 16. Instructor Answer Key

Audit answer table for the broken rulebase, verification walk-through, common
failure list: `the instructor answer-key collection (not published)` (instructor-only).
