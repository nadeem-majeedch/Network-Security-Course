---
artifact-type: instructor-manual
status: complete
instructor-only: true
distribution: never-publish-to-students
---

# CS & Data Science Applications — Track Maps

The course serves two degree programs in one room. Every module has named
application points for each track; the per-lecture versions are in speaker
notes §CS & Data Science Applications. Use these to make both cohorts see
their discipline *in* the material — the point is relevance, not parallel
syllabi.

## Module 1 — Foundations & Analysis
- **CS:** protocol parsing is systems programming (byte-order, state machines,
  socket APIs); L04's reassembly edge cases are distributed-systems problems in
  miniature.
- **DS:** packet/flow data as the first time-series dataset of the course;
  sessionization (5-tuple grouping) is the feature-engineering warm-up.

## Module 2 — Threats
- **CS:** attacks as API/protocol misuse — input-validation and state-handling
  failures they'll be paid to prevent as developers.
- **DS:** attack telemetry (scan patterns, beacon cadence) as labeling
  problems; L05's ATT&CK mapping is a taxonomy exercise.

## Module 3 — Secure Architecture
- **CS:** rulebases are declarative programs with first-match semantics —
  compiler-course instincts apply (ordering, shadowing = dead code).
- **DS:** rulebase hit-count data as usage analytics driving hygiene decisions.

## Module 4 — Crypto & Protocols
- **CS:** nonce/IV handling is API-contract discipline; the GCM misuse cases
  are concurrency bugs at heart.
- **DS:** entropy as a computed feature (L23 forward-look); random-vs-random
  distinction (PRNG vs CSPRNG) matters in any synthetic-data work.

## Module 5 — Wireless & Cloud
- **CS:** IaC is software engineering — versioning, review, CI for network
  config; NetworkPolicy additive semantics are a merge-semantics puzzle.
- **DS:** VPC flow logs at cloud scale = the course's biggest data; sampling
  effects (L19/L21) are statistical pitfalls they must name before the data
  fools them.

## Module 6 — Detection & Vulnerability Management
- **CS:** detection rules as tested, versioned code — the clean-corpus test is
  a unit test; the repo's own CI discipline is the worked example.
- **DS:** **the flagship DS module** — baselines, precision/recall, entropy
  features, cadence/periodicity, CVSS×EPSS multi-criteria ranking; invite DS
  students to lead baseline reads (L21) and entropy steps (L23) and to critique
  prioritization weights (L24).

## Module 7 — IR, SOC & Threat Intel
- **CS:** runbooks as idempotent human-in-the-loop state machines; rollback
  design under uncertainty.
- **DS:** MTTD/dwell-time distributions, coverage-as-recall, rubric-based
  ordinal scoring of intel — DS students own metric definitions in the capstone.

## Module 8 — Forensics & Capstone
- **CS:** timeline reconstruction is event-sourcing debugged backwards;
  clock-skew normalization is a data-cleaning problem with stakes.
- **DS:** report writing is communicating analytical uncertainty — confidence
  language, exhibit-linked claims; the capstone report is their portfolio piece
  for DS roles as much as analyst roles.

## One shared frame to state aloud (L01 and L32)

The course's analysis pipeline — **collect → normalize → baseline → detect →
investigate → report** — is a data lifecycle. CS students built its tooling
instincts; DS students built its statistics instincts; security needs both.
The capstone deliberately grades synthesis across both.
