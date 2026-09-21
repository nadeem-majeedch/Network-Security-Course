---
lab: Lab-13
status: complete
artifact-type: lab-answer-key
instructor-only: true
distribution: never-publish-to-students
---

# Answer Key — Lab-13 (Incident Triage on a Staged Intrusion)

## Staging ground truth (seed 413 corpus)
Three phases over ~12 min of simulated time: (1) **recon** — 5 one-way SYNs
from 10.20.0.66 → 10.20.30.10 ports 22/80/443/445/3389; (2) **beacon** —
10.20.0.102 → resolver TXT queries to `*.cdn-metrics.example` at 30 s cadence
(24 queries, TEST-NET 203.0.113.7 pattern); (3) **exfil-shaped** — 10.20.0.102
→ 198.51.100.9:80, 6 small periodic POSTs (~120 s cadence, 64-byte bodies).

## Alert-ticket design (instructor note)
The ticket deliberately: (a) overstates "workstation-wide compromise" (only
one host shows beacon evidence in-window), (b) omits the scan phase entirely,
(c) names the wrong protocol for the exfil (says FTP; it's HTTP POST). The
debrief reveals all three — corroboration discipline is the counter to each.

## Expected corroboration (grading anchor)
- IDS-analog: SYN sweep matches scan signatures; beacon matches DNS-TXT-
  external signatures (Lab-11 rule (b) would fire here — cross-lab continuity
  worth noting in class).
- Behavioral: 30 s cadence + 26-char base32 labels + TXT concentration
  (Lab-12's four-signal arithmetic).
- Flow-view: periodic small one-way flows; exfil POSTs' ~120 s periodicity.
- Convergence → finding; any single view → hypothesis only.

## Expected scope table (full-credit shape)
| Item | Value | Confidence | Why |
|---|---|---|---|
| Source host (beacon/exfil) | 10.20.0.102 | high (3 views) | multi-view convergence |
| Scan source | 10.20.0.66 | high in-window | direct frames |
| Destinations | resolver-external pattern + 198.51.100.9 | medium | qname pattern, no payload |
| Window | [first,last] frame ± skew | high | measured |
| Un-scoped | prior compromise, other hosts | n/a | window cannot rule out |

## Containment plan (grading anchor)
Ladder order: isolate 10.20.0.102 at switch (reversible, preserves volatile
state, visibility cost low) → block 198.51.100.9 + qname pattern at egress
(reversible, visibility cost = loses new-C2 view) → disable user session on
.102 (disruptive, approver: IT ops) → reimage (irreversible — out of scope
this lab; approver: IC + asset owner). Full credit names *who approves each*
and the evidence-preservation consequence (volatile capture before isolation).

## Severity calibration
Course rubric (impact × spread × sensitivity): beaconing + exfil-shaped
post = P1/P2 boundary; defensible either with justification — the paragraph,
not the number, is graded. Common inflation: treating the *scan* as the
incident (it's recon context).

## Grading notes
- Handoff note: cold-continue test in debrief is the pass/fail moment; notes
  missing timestamps or open questions fail it.
- Over/under-claim delta log required (honest scope misses score fine;
  un-logged misses don't).
- Q3 (blocking alerts the attacker): reward explicit trade-off framing +
  owner (IC/risk owner decides, analyst presents options — L26's ethics case).

## Command status
✅ Dataset + corroboration starter shapes executed; ⚠️ tshark line is a
documentation shape (Wireshark CLI) where the GUI equivalent is accepted.
