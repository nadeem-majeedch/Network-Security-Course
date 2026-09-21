---
lab: Lab-15
title: Forensic Timeline & Findings Report
week: 15
module: 8
clos: [CLO-14, CLO-15]
lectures: [L29, L30]
duration: 2h (embedded in lecture block)
status: complete
artifact-type: student-lab-handout
instructor-key: teaching/lab-answer-keys/lab-15-answer-key.md
---

# Lab-15 — Forensic Timeline & Findings Report

## 1. Lab Overview & CLO Mapping

The capstone's forensic rehearsal: treat a case from first touch — acquire
with hashes, build a clock-normalized timeline from the corpus, extract IOCs
with context, and write the two-audience report (exec summary that decides;
analyst section a peer can reproduce). *CLO-14* (network forensics with chain-
of-custody discipline) + *CLO-15* (communicate to technical and executive
audiences). Reference lectures: L29 (forensic fundamentals), L30 (advanced
forensics & reporting).

## 2. Learning Objectives

By the end you can: (1) handle evidence with hashing and custody records from
first touch; (2) normalize multi-source timestamps (clock skew) before
ordering events; (3) construct a defensible timeline with confidence per
event; (4) extract and scope IOCs (exact values, context, confidence, expiry);
(5) write a report whose exec summary stands alone and whose claims are
exhibit-linked.

## 3. Prerequisites

Labs 11–14 submitted; L29/L30 attended; Lab-13's triage results (this case is
the same corpus, now as *evidence*, not as a live hunt).

## 4. Estimated Duration

120 minutes: acquisition & custody 15 · timeline build 40 · IOCs 20 · report
40 · exchange 5.

## 5. Required Software & Hardware

- Lab-range VM with Wireshark, Python 3.11+, Zeek (optional reconsumption).
- Dataset: `docs/labs/datasets/lab15-forensics.pcap` + `SHA256SUMS` + the case
  brief (context: "Meridian, day after the Lab-13 alert — what actually
  happened, and what do we tell whom?").

## 6. Setup Instructions

> **Command status:** ✅ verified at authoring time; ⚠️ reference shape.

1. ✅ Acquisition with integrity (the discipline *is* the exercise):

```bash
mkdir case-work && cp docs/labs/datasets/lab15-forensics.pcap case-work/
cd case-work
sha256sum lab15-forensics.pcap > evidence.sha256        # ✅ record at acquisition
sha256sum -c evidence.sha256                            # ✅ verify before AND after analysis
```

2. ✅ Custody record template (fill per touch — verified content shape):

```
Exhibit: lab15-forensics.pcap
Acquired: <UTC timestamp> by <analyst> from <source path>
SHA-256: <value from evidence.sha256>
Purpose of access: <what/why>            (one line per access, append-only)
```

3. ✅ Timeline helpers (verified shapes):

```python
# skew-aware event list: read packet timestamps (UTC assumed) and label sources
# Wireshark alternative: File → Export Packet Dissections → as CSV, then sort
```

## 7. Authorization & Safety Notes

- **Authorization basis:** analysis on the hash-verified copy only; originals are sealed; the case brief is the only authorized scope for this exercise.

- Analysis on the **copy**, originals sealed (hash-verified) — the report
  cites exhibits, never edits them.
- IOC handling: your IOC list names destinations that are TEST-NET addresses —
  in a real case these would feed blocking lists with expiry; treat precision
  (context + confidence + expiry per IOC) as a graded behavior.
- Report language: findings state what evidence shows; no attribution
  storytelling beyond evidence (L30's honesty discipline is graded).

## 8. Student Tasks

1. **Acquire:** complete the custody record; both hash checks pass (record
   times).
2. **Timeline:** build ≥10 events from the corpus: scan phase, beacon phase,
   exfil-shaped phase, background context. Normalize timestamps; per event:
   time (UTC) · source exhibit+frame · interpretation · confidence (H/M/L).
3. **Clock-skew drill:** the case brief states the capturing sensor ran +90 s
   fast vs the DNS server's clock. Recompute the beacon phase's true window
   and show the delta — one sentence on why uncorrected skew produces
   impossible narratives.
4. **IOC extraction:** table of IOCs: value (exact IP/qname-pattern/UA) · type
   · context (what it did) · confidence · suggested expiry/condition · where
   it would go (egress blocklist? DNS RPZ? detection rule?).
5. **Report:** two sections. *Exec summary (≤150 words):* what happened,
   impact, decisions needed, containment status — no jargon. *Analyst
   section:* method, exhibits, timeline (the table), IOCs, limitations
   (window, skew, no host telemetry), recommendations (prioritized).
6. **Peer exhibit test:** swap reports; the reviewer must reproduce one claim
   from its exhibit reference alone. Log what failed.

## 9. Expected Observations

- The corpus's three phases sort cleanly once timestamps are ordered — the
  scan (early, fast), beacon (periodic throughout), exfil-shaped POSTs
  (low-volume, periodic).
- Skew correction shifts the beacon window measurably; teams that skip it
  produce overlapping "impossible" event orders — visible at exchange.
- IOC precision differs sharply across teams (bare IPs vs contextual IOCs) —
  precision is the graded skill.

## 10. Analysis Questions

1. Why hash at acquisition *and* after analysis? What does the second check
   prove that the first does not?
2. Your timeline has 10 events from one exhibit. What other sources would a
   real case add (host logs, NetFlow, DHCP/DNS server logs), and which of
   your confidence labels would improve first?
3. Which of your IOCs would you *not* push to a blocklist, and why (context/
   collateral risk)? What does that say about IOC automation limits?
4. The exec summary must support a decision. Which decision did you write it
   for, and what would change it if the missing host telemetry arrived?
5. Attribution: what can you *honestly* say about who/what? Write the one
   sentence you would defend under cross-examination — and one you wouldn't.

## 11. Troubleshooting

- Hash mismatch mid-lab → you analyzed the original, or copied again over a
  changed file; re-acquire and log the incident in custody (honest handling
  scores; hiding it doesn't).
- Timeline interleaves background noise → filter to the case actors first
  (Lab-13's scope table), then order events.
- Exec summary drifts technical → the decision test: could a CFO read it and
  answer "what do we do?" Cut every acronym.

## 12. Cleanup Instructions

- Seal: case-work → course folder archive; originals never leave datasets/;
  custody records submitted with the case.

## 13. Submission Requirements

- Custody record (complete, append-only) + both hash checks.
- Timeline table (≥10 events, normalized, confidence-labeled) + skew note.
- IOC table (context, confidence, expiry, destination system per IOC).
- Two-section report (exec ≤150 words + analyst) with exhibit links.
- Peer-test log + analysis answers (5). Due: start of Week 16 session
  (capstone draft feed).

## 14. Expected Output & Evidence

| Artifact | Passing evidence |
|---|---|
| Custody | append-only; both checks recorded with times |
| Timeline | frame-level citations; skew-corrected; confidence per event |
| IOCs | no bare values — every one has context+confidence+destination |
| Report | exec standalone-decidable; analyst reproducible (peer-tested) |

## 15. Grading Rubric

| Criterion | Weight | Full-credit behavior |
|---|---|---|
| Evidence discipline | 40% | custody complete; every claim exhibit-linked |
| Mechanism accuracy | 30% | skew handling, phase mechanics, IOC precision |
| Analysis depth | 20% | limits + automation/collateral nuance (Q3/Q5) |
| Safety & policy | 10% | copy-only analysis; honest incident logging |

## 16. Instructor Answer Key

Ground-truth event table, skew arithmetic, IOC exemplar, report exemplar:
`teaching/lab-answer-keys/lab-15-answer-key.md` (instructor-only).
