---
assignment: assignment-01
type: answer-key
instructor-only: true
distribution: never-publish-to-students
clos: [CLO-3]
marks: 100
status: complete
---

# Answer Key — Assignment 1 (Segmentation Design)

> **INSTRUCTOR ONLY.** Grading anchors and the traps that distinguish
> grade bands. This is a design assignment — model answers define the
> *shape* of a strong submission; student answers will differ legitimately.

## Grading anchors (100 points)

### 1. Zone model (25)
- **Strong (21–25):** 5–8 zones by sensitivity+behavior; DS cluster split
  (compute vs dataset storage) or explicitly justified as one; BMS isolated
  with its vendor path *inside* the zone definition; guest fully isolated;
  default-deny posture stated per zone.
- **Adequate (15–20):** correct zones but boundaries copied from org chart;
  BMS present but vendor path unexamined.
- **Weak (<15):** flat-with-VLANs proposal or zones without postures.

### 2. Flow matrix (25)
- **Strong (21–25):** ≤15 rows, initiation direction correct, unlisted =
  denied stated; names breakage detection per top-3 risk (e.g., scanner→ERP
  batch window, DNS, NTP); **vendor remote-access path appears with a
  documented exception flow** (jump host/brokered, time-boxed, logged).
- **Adequate (15–20):** matrix correct but detection-by-breakage hand-waved.
- **Common fails:** matrix lists *allowed* rather than *initiation*;
  forgot DNS/NTP (flows that make or break segmentation projects).

### 3. Phased rollout (25)
- **Strong (21–25):** phase 1 = observe (NetFlow/Zeek tap points named),
  real matrix built from data; phase 2 = enforce by zone risk, **per-step
  rollback criteria** (metric + threshold + action).
- **Adequate (15–20):** two phases but enforcement-first or rollback vague.
- **Weak:** big-bang cut-over.

### 4. Diagram (15)
- Zones, enforcement points, telemetry taps all present and consistent
  with the matrix (cross-check 3 random rows against the diagram —
  inconsistency caps at 10/15).

### 5. Tradeoff memo (10)
- Honest deferral + accepted risk + pairing control. The expected answer
  shape: "did not segment printers/some low-value zone — accepted risk X,
  paired with Y." Pure risk-free claims cap at 5/10.

## The trap (graded explicitly)

**BMS vendor remote access.** Submissions that either ignore it or
"block it" without an operational path (the vendor contract requires
access) miss the point. Strong submissions broker it: vendor → jump/broker
host → BMS, time-boxed, logged, alerted. This is worth up to 5 of the 25
matrix points — enough to drop a band.

## Common misconceptions to annotate

- "Segmentation = VLANs" (VLANs are a mechanism, not the policy).
- "Firewall at the edge is enough" (east-west is the assignment's point).
- "DS cluster is just another server zone" (dataset exfiltration risk and
  per-job identity deserve a mention for full marks).
