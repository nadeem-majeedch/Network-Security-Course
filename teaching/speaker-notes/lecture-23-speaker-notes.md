---
lecture: L23
module: 6
week: 12
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L23 Speaker Notes — Zeek & Anomaly Detection

## Delivery Guide
Zeek reads like querying, not pattern matching — sell that framing first. The UID
join demo (one connection, three logs) is the triage superpower moment; L26 will
reuse it. The DNS-tunnel hunt is the highlight: the planted tunnel *falls out of
arithmetic* (length, entropy, qtype, cadence) — let students compute, don't show
the answer. Assignment 6 preview (W13) closes the session.

## Timing Plan
0–10 signature-vs-behavior debate · 10–35 Zeek model + core logs (UID join live) ·
35–55 baselining (per-host profile + DNS histogram) · 55–65 break · 65–90 tunnel/
abuse signatures (class finds the tunnel) · 90–110 three-part worksheet · 110–120
exit ticket + Assignment-6 preview. **Compression:** http/ssl log detail to one
slide; conn+dns are the load-bearing logs.

## Teaching Demonstrations
1. UID join live: grep one uid across conn/dns/http — the same conversation, three views.
2. DNS-tunnel hunt: length/label counts → entropy per client → TXT concentration → cadence — computed in class, step by step.
3. Notice-policy sketch: the script fragment (thresholds + NOTICE) — pseudocode is fine; integration to notice.log → SIEM is the point.

## Expected Student Difficulties
1. "Zeek is another Snort" — the model comparison slide (behavior vs bytes) resets it.
2. Entropy as magic — walk the calculation once on a short qname set; it's just statistics.
3. Baseline exclusions feel like cheating — documented exclusions with expiry are *the* professional form.

## Discussion Facilitation
Q2 (backup-tool entropy FP) is the tuning-in-Zeek moment: narrow the rule, not the
data; document the exclusion. Q5 (cloud visibility): connect to L20's CNI flow
telemetry — same idea, different stack.

## Lab Troubleshooting (worksheet context)
- zeek-cut missing fields: log schema versions differ — use the pinned Zeek version on range images.
- Students "find" the tunnel by accident (too fast): require the *method* on paper, not just the answer.
- conn.log state codes unfamiliar: provide the state-code reference card.

## Accessibility Notes
- Log excerpts: text-first; reads narrated field-by-field.
- Entropy math: worked example distributed with plain-language steps.

## CS & Data Science Applications
- **DS:** this is the flagship DS lecture: entropy, distributions, cadence/periodicity, and labeled baselines — every detection here is applied statistics on logs. DS students should co-teach the entropy step.
- **CS:** Zeek scripts are event-driven programming — policy as code with state; connects to their systems-event instincts.

## Links
Plan: `modules/module-06-detection-vulnerability/lectures/lecture-23-zeek-anomaly-detection.md` · Student page: `docs/lectures/lecture-23-zeek-anomaly-detection.md` · Answers: `teaching/answer-keys/answer-key-module-06.md`
