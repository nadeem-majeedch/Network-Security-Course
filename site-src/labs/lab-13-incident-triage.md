# Lab-13 — Incident Triage on a Staged Intrusion

## 1. Lab Overview & CLO Mapping

A staged intrusion dataset ("the week-10 incident") lands on your desk as an
IDS alert + the raw capture. You triage it the L26 way: corroborate
three ways (signature → behavioral → flow), scope the activity, decide
containment on the reversible-first ladder, and produce a handoff note that
survives your absence. *CLO-11* — execute the IR lifecycle on a simulated
intrusion producing defensible artifacts. Reference lectures: L25 (IR
lifecycle & preparation), L26 (detection, triage & containment).

## 2. Learning Objectives

By the end you can: (1) corroborate an alert across independent evidence
sources before acting; (2) scope an incident from evidence (hosts, destinations,
time window) with confidence bounds; (3) sequence containment by reversibility
and document the visibility cost of each step; (4) write a self-contained
handoff note (what/when/source/actions/open questions, timestamped); (5)
calibrate severity against the course rubric and defend the call.

## 3. Prerequisites

Lab-12 submitted; L25/L26 attended; course severity rubric (manual §3, handed
out with the lab).

## 4. Estimated Duration

120 minutes: alert briefing 10 · corroboration hunt 40 · scope & containment
plan 35 · handoff note + debrief 35.

## 5. Required Software & Hardware

- Lab-range VM with Wireshark, Python 3.11+, text editor.
- Datasets: `lab13-incident.pcap` + the "alert ticket" (one-page brief on the
  lab sheet — treat it as *unverified*, that's the exercise).

## 6. Setup Instructions

> **Command status:** ✅ verified at authoring time; ⚠️ reference shape.

1. ✅ Verify: `cd docs/labs/datasets && sha256sum -c SHA256SUMS`
2. ✅ Corroboration starters (verified shapes):

```bash
# IDS-view analog: count SYNs to the server subnet (scan signature)
tshark -r lab13-incident.pcap 'tcp.flags.syn==1 && tcp.flags.ack==0' 2>/dev/null | wc -l
# ⚠️ if tshark unavailable: Wireshark filter + Statistics → Conversations

# Zeek-view analog: beacon cadence from the DNS view (see Lab-12 hunt)
```

3. Copy the dataset to a work directory — originals stay read-only (evidence
   discipline starts at first touch).

## 7. Authorization & Safety Notes

- This is an *analysis* exercise on synthetic evidence — no containment actions
  on live range systems are authorized in this lab; your containment plan is a
  **plan**, executed only in instructor-run demos (the full simulation is
  Lab-16).
- The alert ticket contains assumptions that may be wrong — treating ticket
  narrative as evidence is the exact failure this lab teaches you to avoid.

## 8. Student Tasks

1. **Corroborate:** the ticket claims "C2 beacon from a workstation." Verify
   three ways: (a) IDS-analog — what in the packet stream matches a beacon
   *signature*? (b) behavioral — cadence/entropy from the DNS view (Lab-12
   method); (c) flow-view — volume asymmetry and periodicity. Each view: what
   it adds, what it cannot say.
2. **Scope:** from evidence only: source host(s), external destination(s),
   first/last seen (time window), protocols, confidence per item (high/med/low
   + why). Explicitly mark what the window *cannot* rule out.
3. **Severity:** score with the course rubric (business impact × spread risk ×
   data sensitivity). Write the one-paragraph justification a reviewer could
   audit.
4. **Containment plan (reversible-first ladder):** for each candidate action —
   isolate host at switch (reversible), block destination at egress (reversible),
   disable account (disruptive), reimage (irreversible, out of scope here) —
   state: reversibility, evidence preserved/destroyed, visibility cost, who
   approves. Sequence them and justify the order.
5. **Handoff note:** self-contained, timestamped: what/when/source-of-evidence,
   corroboration results, scope table, actions taken (= none; analysis only)
   and planned, open questions (≥2). Test: could a teammate continue cold?
6. **Debrief:** exchange notes; the instructor reveals the staging ground
   truth; log the delta between your scope and truth (over/under-claims).

## 9. Expected Observations

- Three views agree: periodic ~30 s DNS TXT traffic from 10.20.0.102 to
  TEST-NET destination pattern + scan phase from 10.20.0.66 + small periodic
  POSTs (exfil-shaped). No single view convicts; the *convergence* is the
  finding.
- The ticket is *partially wrong* by design (it overstates one thing and
  misses another — revealed at debrief): corroboration discipline is why.
- Handoff quality visibly differs: notes without timestamps and open questions
  fail the cold-continue test.

## 10. Analysis Questions

1. Which corroboration view did the ticket's author likely skip, and what
   distortion did that produce?
2. Your scope says "10.20.0.102, high confidence" but the window is 30 minutes.
   What containment action does that confidence *not* yet justify, and what
   evidence would?
3. Blocking the C2 destination alerts the attacker (they notice). Weigh that
   against continued observation — which factors decide, and who owns the call?
4. Why does the ladder place reimage last even when it feels decisive? Name
   two evidence classes destroyed by premature reimaging.
5. The incident "ends" when your handoff is accepted. What does the receiving
   analyst's next hour look like given your note (or: what would they have to
   ask you that you failed to write down)?

## 11. Troubleshooting

- Cadence looks noisy → you included the background DNS; group strictly by
  (src,dst,qtype) and re-read the periodic subset.
- Two "beacon" candidates → one is the exfil POST cadence; different protocol,
  different verdict — do not merge them.
- Handoff bloated → the test is cold-continuability, not length; every sentence
  must carry evidence or a question.

## 12. Cleanup Instructions

- Work-copy deletion after export; originals untouched (hashes still verify);
  VM logout.

## 13. Submission Requirements

- Corroboration worksheet (three views, each with evidence excerpts).
- Scope table with confidence bounds + explicit window limits.
- Severity paragraph + rubric-scored call.
- Containment plan (ladder-ordered, approvals named).
- Handoff note (timestamped) + debrief delta log. Due: start of Week 14 session.

## 14. Expected Output & Evidence

| Artifact | Passing evidence |
|---|---|
| Corroboration | three independent views, excerpts cited, agreement stated |
| Scope | hosts/dest/window/confidence — no narrative borrowing from the ticket |
| Containment | reversibility + visibility cost per action; approval owners |
| Handoff | passes the cold-continue test (peer-checked in debrief) |

## 15. Grading Rubric

| Criterion | Weight | Full-credit behavior |
|---|---|---|
| Evidence discipline | 40% | corroboration before conclusions; excerpts cited; bounds stated |
| Mechanism accuracy | 30% | beacon/scan/exfil mechanics + phase vocabulary correct |
| Analysis depth | 20% | trade-off reasoning (Q2/Q3); severity justification |
| Safety & policy | 10% | analysis-only posture; originals preserved |

## 16. Instructor Answer Key

Staging ground truth, corroboration exemplar, severity calibration notes,
handoff exemplar: `the instructor answer-key collection (not published)`
(instructor-only).
