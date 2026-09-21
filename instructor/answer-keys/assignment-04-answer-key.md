---
assignment: assignment-04
type: answer-key
instructor-only: true
distribution: never-publish-to-students
clos: [CLO-9, CLO-12]
marks: 100
status: complete
---

# Answer Key — Assignment 4 (IDS Tuning & Detection Engineering)

> **INSTRUCTOR ONLY.** The Lab-11 dataset embeds: (a) heavy benign scanner
> traffic (the FP driver), (b) periodic software-update fetches (benign,
> high volume), (c) one unannounced scripted behavior — periodic
> small-outbound beaconing with regular jitter from one internal host to
> a fixed external IP (the detection target).

## Expected analysis core

### 1. Alert economics (25)
Top-band tables show: scanner-triggered class ≈ dominant volume × ~0% TP;
update-fetch class ≈ high volume × 0% TP (policy, not security); beacon
class ≈ tiny volume × high TP. Pain ranking must be *computed*
(volume × minutes), then corrected for trust damage — students who rank
purely by reclaimed minutes and pick the update-class auto-close as their
only interesting change are missing the second-order point (cs-070).

### 2. Tuning proposal (25)
Expected pair: (1) **suppress scanner-to-scanned noise** by scanning-host
IP scope (not rule deletion — the rule must stay for external scanners);
(2) **scope the update-fetch class** to the update servers' IP/process
context. Both must show: FP driver named, scoping exact, accepted risk
stated, and the **replay proof** (before/after alert diff on the dataset;
zero suppressed TPs demonstrated by class).

### 3. New detection (25)
The unannounced behavior is **C2-style beaconing**: regular-interval,
low-volume outbound to a fixed external IP. Expected rule shape
(either syntax acceptable):
- Suricata: flow:established,to_server; threshold on **bytes_in <
  threshold** + **count/seconds interval** matching the beacon period;
  dest IP scoped or, better, frequency- rather than IP-based.
- Zeek: notice on per (src, dst) connection-interval regularity
  (coefficient of variation below threshold over N connections).

Full marks: behavioral rationale (periodicity + low volume + fixed
destination = beacon profile), FP profile (legit polling apps — name
them: monitoring agents, update checks), exposed knobs (interval, volume,
consecutive count).

### 4. Escalation criteria (15)
Page on: N consecutive matched intervals + destination not on allow-list;
queue on: single match. Measurable numbers required — "high severity"
alone caps at 8/15.

### 5. Reflection (15→10)
Expected honest limits: dataset has no *user* context (no identity logs);
one week cannot capture slow beacons (low-and-slow evades the window);
no encrypted-payload inspection (the beacon's *content* is opaque —
detection is purely behavioral); lab noise ≠ production noise (FP rates
will shift).

## Common failure patterns to annotate

- Tuning = deleting rules (loses TP coverage; caps at 60% per the brief).
- Detection = signature for the lab's dest IP (overfits; the beacon's
  *behavior* is the target, not the IP — cap at 15/25).
- Escalation criteria unmeasurable ("analyst judgment").
