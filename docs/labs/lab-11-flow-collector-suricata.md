---
lab: Lab-11
title: Flow Collector + Suricata Ruleset
week: 11
module: 6
clos: [CLO-9]
lectures: [L21, L22]
duration: 2h (embedded in lecture block)
status: complete
artifact-type: student-lab-handout
instructor-key: teaching/lab-answer-keys/lab-11-answer-key.md
---

# Lab-11 — Flow Collector + Suricata Ruleset

## 1. Lab Overview & CLO Mapping

You will stand up the L21/L22 pipeline in miniature: load a flow dataset,
compute a baseline, then author and tune a Suricata ruleset against two
corpora — a malicious set it must catch and a clean set it must **not** fire
on. This is the graded **Lab Pract-4**. *CLO-9* — deploy and tune NIDS
(signature and anomaly based) and write custom detection rules. Reference
lectures: L21 (monitoring foundations), L22 (IDS/IPS signatures & tuning).

## 2. Learning Objectives

By the end you can: (1) query flow records for top-N, per-host, and
periodicity views; (2) write a defensible baseline statement from data; (3)
author Suricata rules (header + options) for scan and beacon-shaped behaviors;
(4) apply the census → scope → document tuning workflow to drive false
positives down without deleting detection; (5) prove your ruleset with a
clean-corpus regression test.

## 3. Prerequisites

Labs 09–10 submitted; L21/L22 attended; datasets verified.

## 4. Estimated Duration

120 minutes: flow baseline 35 · rule authoring 35 · tuning + clean-corpus 35 ·
write-up 15.

## 5. Required Software & Hardware

- Lab-range VM with Suricata ≥ 7 (pinned), Python 3.11+ (pandas or stdlib for
  flows), Wireshark.
- Datasets: `lab11-flows.csv` (79 records), `lab13-incident.pcap` (malignant
  corpus, reused from Lab-13's staging — instructor provides a benign corpus
  `lab11-clean.pcap` in the range share).

## 6. Setup Instructions

> **Command status:** ✅ verified at authoring time; ⚠️ range steps.

1. ✅ Verify datasets: `sha256sum -c SHA256SUMS` (flows) and range share copy.
2. ✅ Flow baseline (stdlib shape — verified):

```python
import csv, collections
rows = list(csv.DictReader(open("docs/labs/datasets/lab11-flows.csv")))
by_src = collections.Counter((r["src_ip"], r["dst_ip"], r["dst_port"]) for r in rows)
print(by_src.most_common(5))                       # top-5 talker pairs
one_way = [r for r in rows if r["tcp_flags"] == "S"]
print("one-way SYNs:", len(one_way), one_way[:3])  # scan signature
dns = [r for r in rows if r["dst_port"] == "53" and r["src_ip"] == "10.20.0.102"]
print("periodic DNS:", [(int(d["first_switched"])) for d in dns][:8])
```

3. ⚠️ Suricata config: point `HOME_NET` at the lab subnets per the sheet;
   enable eve.json output; test config: `suricata -T -c /etc/suricata/suricata.yaml`.
4. ✅ Run against the malignant corpus (reference shape):

```bash
suricata -r docs/labs/datasets/lab13-incident.pcap -l /tmp/suri \
  -c /etc/suricata/suricata.yaml
# ✅ alerts land in /tmp/suri/eve.json (json lines); count with:
grep -c '"signature_id"' /tmp/suri/eve.json
```

## 7. Authorization & Safety Notes

- **Authorization basis:** rules run against prepared course datasets only; live capture is confined to the instructor-authorized range interfaces, and IPS blocking is disabled for this lab.

- Rules run against prepared corpora only — never point Suricata's live
  capture at campus networks. IPS (inline drop) mode is **off** for this lab:
  we detect, we do not block (that's a change-control decision, L26).
- Your rules are graded artifacts: comment every rule with intent + author
  (the Lab-06 hygiene carries forward).

## 8. Student Tasks

1. **Baseline from flows:** produce the baseline paragraph (≥3 anchors: top
   talker share, one-way SYN count, DNS cadence for 10.20.0.102). What does
   the periodic ~30 s cadence suggest — state it as *hypothesis*.
2. **Author rules:** three Suricata rules: (a) TCP scan tell (one-way SYN
   pattern toward HOME_NET), (b) DNS beacon cadence hint (TXT qtype to
   EXTERNAL_NET with threshold), (c) exfil-shaped HTTP POST volume. Syntax
   card on the sheet; comment each.
3. **Malignant test:** run the ruleset on `lab13-incident.pcap`; record alerts
   per rule (expect all three to fire; note sid and count).
4. **Clean-corpus regression:** run on `lab11-clean.pcap` (range share) — the
   ruleset must be **silent or explicable**. For every firing, apply the
   census → scope → document workflow: narrow the rule (content/threshold/
   flow direction), re-run both corpora, record the exclusion and its expiry.
5. **Tuning report:** before/after alert counts on both corpora; the precision
   story in two numbers (alerts on clean corpus before vs after).

## 9. Expected Observations

- The flows CSV contains a planted scan (15 one-way SYNs, one source) and a
  24-flow periodic DNS beacon at ~30 s — the baseline paragraph must *notice
  both* without being told.
- Rule (b) will initially fire on benign periodic DNS too — that's the tuning
  lesson; scope it (e.g., TXT-only + threshold + EXTERNAL_NET) rather than
  delete.
- eve.json is JSON-lines: field paths matter; the `signature_id` you chose
  shows in every alert.

## 10. Analysis Questions

1. Your baseline missed the beacon until you grouped by (src,dst,port) — what
   does that say about aggregation level in pipeline design (L21)?
2. Threshold + qtype narrowing: what false negatives does each introduce?
   When would you accept them?
3. The clean-corpus test is your ruleset's unit test. What belongs in CI for a
   real detection team (name the two corpora every rule should face)?
4. IPS vs IDS: given your rule (b)'s residual false-positive rate, would you
   run it inline blocking? Justify with the visibility/outage cost frame.
5. If the attacker lengthened beacon period to 6 h and rotated destinations,
   which of your three rules survives, and what detection class replaces it
   (anomaly/baseline, L23 forward-look)?

## 11. Troubleshooting

- `suricata -T` fails → YAML indentation or undefined variable (HOME_NET);
  test mode names the line.
- Zero alerts on malignant corpus → rule direction (`flow:established,to_server`),
  ports, or HOME_NET scope; check eve.json is from *this* run (clear the dir).
- Clean corpus fires you can't scope → inspect the matched packets' exact
  fields (`eve.json` payload fields) before narrowing; blind `-` deletions are
  what the workflow forbids.

## 12. Cleanup Instructions

- Export ruleset + eve samples; clear `/tmp/suri`; VM logout. No AP/cloud
  state involved.

## 13. Submission Requirements

- Baseline paragraph + flow-analysis script/commands.
- Ruleset file (3 commented rules) + before/after tuning report.
- Clean-corpus regression evidence (both runs' alert counts).
- Analysis answers (5). Due: end of session (Pract-4 grading).

## 14. Expected Output & Evidence

| Artifact | Passing evidence |
|---|---|
| Baseline | ≥3 quantitative anchors; beacon/scan noticed as hypotheses |
| Ruleset | all rules fire on malignant corpus; intent comments present |
| Tuning | clean-corpus count drops with documented scoped exclusions |
| Regression | re-run shown after each exclusion |

## 15. Grading Rubric

| Criterion | Weight | Full-credit behavior |
|---|---|---|
| Evidence discipline | 40% | alert counts cited per run; exclusions documented with expiry |
| Mechanism accuracy | 30% | rule syntax/semantics; scan & beacon mechanics |
| Analysis depth | 20% | FN trade-offs; CI framing; evasion resilience |
| Safety & policy | 10% | corpus-only runs; IDS-not-IPS posture; rule hygiene |

## 16. Instructor Answer Key

Reference ruleset, expected alert counts per corpus, tuning exemplars:
`teaching/lab-answer-keys/lab-11-answer-key.md` (instructor-only).
