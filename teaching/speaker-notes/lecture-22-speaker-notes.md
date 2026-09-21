---
lecture: L22
module: 6
week: 11
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L22 Speaker Notes — IDS/IPS — Signatures & Tuning

## Delivery Guide
Rule-writing is a craft skill: model three rules live (beacon, scan, strip-attempt)
with students predicting match counts before each test. The clean-corpus discipline
("must not fire on clean.pcap") is what separates professionals from script
copiers — enforce it in Assignment 4. The FP-census → triage-classes → scoped-
exclusion method is the tuning chapter; the untuned-vs-tuned diff makes its value
visible.

## Timing Plan
0–10 pipeline recap (where alerts land) · 10–35 paradigms + architecture · 35–60
rule anatomy (three live rules) · 60–70 break · 70–90 tuning method (FP census) ·
90–110 ruleset lab (Assignment 4 draft) · 110–120 exit ticket + due-date reminder. 
**Compression:** architecture block to slide + one war story; the three-rule demo
and clean-corpus test are the graded spine.

## Teaching Demonstrations
1. Three rules live: write, run against malicious corpus (fires), run against clean corpus (silent) — both tests shown for each.
2. Untuned-vs-tuned diff: same traffic, two rulesets — alert volume and precision on the board.
3. Anchoring demo: `startswith` vs mid-string content match — FP difference on a legit URI.

## Expected Student Difficulties
1. Syntax errors stall momentum — provide the reference rule card; exact keywords matter.
2. "It fired, done" satisfaction — the clean-corpus test is the correction; make it a gate.
3. Suppression temptation (kill the rule) — the instance-vs-rule exclusion rule, with expiry, is the professional answer.

## Discussion Facilitation
Q2 (4,000 alerts/day on the backup server) has three correct responses — require
all three before choosing; the trade-off articulation is the skill. Q4 (false-
negative testing): elicit the mutated-sample idea — evolve the pattern, does the
rule still catch it?

## Lab Troubleshooting (ruleset context)
- Suricata won't start: YAML indent error in local rules — the config is whitespace-sensitive; check `-T` test mode first.
- Rule never fires: HOME_NET/EXTERNAL_NET scope wrong — check variables before logic.
- EVE output missing fields: protocol not enabled in config (app-layer settings).

## Accessibility Notes
- Rule syntax: text-only, high-contrast; read keyword-by-keyword during demos.
- FP-census tables: structured templates provided.

## CS & Data Science Applications
- **CS:** rules are declarative pattern programs — version control, tests, CI instincts apply (this repo itself is the example).
- **DS:** precision/recall trade-offs in plain view: thresholds are model-tuning; the FP census is a labeled evaluation set — DS students will recognize the workflow instantly.

## Links
Plan: `modules/module-06-detection-vulnerability/lectures/lecture-22-ids-ips-signatures-tuning.md` · Student page: `docs/lectures/lecture-22-ids-ips-signatures-tuning.md` · Answers: `teaching/answer-keys/answer-key-module-06.md`
