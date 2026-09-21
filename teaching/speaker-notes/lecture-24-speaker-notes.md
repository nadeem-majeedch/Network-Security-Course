---
lecture: L24
module: 6
week: 12
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L24 Speaker Notes — Vulnerability Management Cycle

## Delivery Guide
"Scanner output is evidence, not risk" is the sentence to repeat. The live
unauthenticated-vs-credentialed diff (same host, both views) is the proof that
authentication sees config truth. The context-inversion demo (9.8 air-gapped test
box vs 7.5 internet-facing KEV gateway) is the judgment moment — make students
argue it before showing the matrix. Assignment 5 (the full cycle) is due today;
collect before the exit ticket.

## Timing Plan
0–10 detection-vs-prevention bridge · 10–35 lifecycle + inventory (failure modes
per stage) · 35–55 scanning craft (safe-mode live scan) · 55–65 break · 65–90
prioritization math (CVSS → context) · 90–110 scan-cycle lab · 110–120 exit
ticket + **Assignment-5 collection** + Module-7 trailer. **Compression:** the
inventory block can lean on L19/L21 callbacks; the inversion demo cannot be cut.

## Teaching Demonstrations
1. Two-view diff: unauth scan vs credentialed scan of the same lab host — the missing-patch/config gap made visible.
2. Context inversion: score both findings on the board (base → environmental → KEV/EPSS/exposure overlay) — let students commit before the reveal.
3. Exception-memo anatomy: one real-shaped memo (owner, compensating control, expiry, approver) — the artifact that makes SLAs real.

## Expected Student Difficulties
1. Score = risk conflation — the inversion demo is the cure; require the four context inputs in every later ranking.
2. Scan-safety afterthought ("just run it") — the fragile-appliance war story + safe-mode flags establish engineering discipline.
3. Exception-process boredom — reframe: without it, triage is theater; the memo is what auditors actually read.

## Discussion Facilitation
Q4 ("KEV within 72 hours as the whole policy") rewards the critique: KEV is a
*prioritizer*, not a program — inventory, verification, and metrics still required.
Q5 (telemetry as inventory): DHCP/DNS and flows reveal unmanaged hosts — connect to
L03/L21 explicitly.

## Lab Troubleshooting (scan-cycle context)
- Scanner hangs on the vulnerable VM: expected — safe-mode/timing flags per the sheet; don't force.
- Credentialed scan auth fails: vault-issued credentials rotated — re-issue from the instructor set.
- Students scan outside assigned hosts: the authorization talk repeats; lab roster enforcement.

## Accessibility Notes
- Scanner GUIs: CLI alternatives provided for all graded steps.
- Finding tables: structured templates; screen-reader-friendly column order.

## CS & Data Science Applications
- **CS:** scan policy = constrained resource scheduling; credentialed scans are privilege-branching — design questions CS students can engage.
- **DS:** prioritization is multi-criteria ranking (CVSS × EPSS × exposure × criticality) — a transparent scoring-model exercise; invite DS students to critique the weights.

## Links
Plan: `modules/module-06-detection-vulnerability/lectures/lecture-24-vulnerability-management-cycle.md` · Student page: `docs/lectures/lecture-24-vulnerability-management-cycle.md` · Answers: `teaching/answer-keys/answer-key-module-06.md`
