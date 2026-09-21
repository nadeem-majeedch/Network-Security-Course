---
lab: Lab-16
title: Capstone IR Simulation
week: 16
module: 8
clos: [CLO-11, CLO-14, CLO-15]
lectures: [L31, L32]
duration: 2h (embedded in lecture block)
status: complete
artifact-type: student-lab-handout
instructor-key: teaching/lab-answer-keys/lab-16-answer-key.md
---

# Lab-16 — Capstone IR Simulation

## 1. Lab Overview & CLO Mapping

The course's integration assessment: your team runs a full IR cycle on a
multi-phase staged intrusion (evidence bundle + injected updates), from
triage through containment plan, eradication sequence, recovery gates, and the
defense briefing — then defends decisions in Q&A. *CLO-11* (execute the IR
lifecycle on a simulated intrusion) + *CLO-14* (forensic artifacts) +
*CLO-15* (briefing to decision-makers). This lab feeds the **L32 capstone
defense and final examination**. Reference lectures: L31 (capstone workshop),
L32 (defense & synthesis).

## 2. Learning Objectives

By the end you can: (1) run the complete IR lifecycle as a team with role
discipline under time pressure; (2) integrate the course's three analysis
layers (signature/behavioral/flow) into one investigation; (3) produce
defensible artifacts at every phase (triage record, containment log,
eradication/recovery sequence, IOC list, briefing); (4) brief executives and
answer hostile questions with evidence-anchored calm; (5) synthesize the
course's trust-boundary thread in a closing defense statement.

## 3. Prerequisites

All labs 01–15 submitted; capstone draft (L31 workshop output) in hand;
role assignments made (rotation per syllabus: lead analyst, evidence
custodian, comms, detection — rotated once since W13).

## 4. Estimated Duration

120 minutes, hard-clocked: briefing 10 · investigation 55 · recovery sequence
+ briefing prep 25 · briefings + Q&A 25 · debrief 5. The hard clock is a
design feature — grade rewards the *record*, per manual §2.

## 5. Required Software & Hardware

- Lab-range VM with the full toolset (Wireshark, Zeek, Python, editor).
- Capstone evidence bundle (instructor-issued at session start; includes a
  fresh staged dataset + log extracts + inject cards).
- Timing cards, severity rubric, containment-ladder card (from L26/L31).

## 6. Setup Instructions

> **Command status:** ✅ verified shapes; ⚠️ session steps.

1. ⚠️ Roles confirmed and *recorded* on the team sheet (contribution
   statement follows at submission — syllabus policy).
2. ✅ Evidence bundle handling (same discipline as Lab-15, now under time
   pressure):

```bash
mkdir capstone-case && cd capstone-case
sha256sum <bundle-files> > evidence.sha256 && sha256sum -c evidence.sha256  # ✅ before work
cp <bundle.pcap> work.pcap        # analysis on the copy, always
```

3. ⚠️ Injects: the instructor will hand 2–3 update cards mid-exercise — the
   IC acknowledges each on record and re-scopes.

## 7. Authorization & Safety Notes

- **Authorization basis:** all work happens on synthetic evidence inside the block; containment and eradication remain plans and logs — live actions are analysis commands on your copy only.

- Everything happens on synthetic evidence inside the block; containment and
  eradication remain *plans and logs* — the only live actions are analysis
  commands on your copy. This boundary is stated in your briefing (it is part
  of what a real IR lead would say).
- Time pressure never suspends custody discipline — that trade is exactly
  what the grading probes (real IRs fail here, not in the technical reading).

## 8. Student Tasks

1. **Triage & scope (timed):** corroborate the initial alert three ways;
   scope hosts/destinations/window with confidence; severity call on the
   rubric; log decisions (who/when/what).
2. **Containment plan:** ladder-ordered with reversibility + visibility cost +
   approvers; explicitly handle the injected "executive pressure" card
   (options with risk, decision on record).
3. **Eradication & recovery sequence:** dependency-ordered restoration
   (identity → core services → tiers), credential-rotation priorities, go/
   no-go gates with named checks (persistence-hunt clean, credentials rotated,
   monitoring heightened).
4. **IOC & detection output:** contextual IOC table (context, confidence,
   expiry, destination) + one detection rule the incident *adds* to the
   course corpus (L28's detection-delta habit at capstone scale).
5. **Briefing (8 min):** exec summary (decide-able) + technical walkthrough
   (exhibit-linked) + synthesized closing: the trust-boundary thread across
   ≥3 modules applied to this case.
6. **Q&A defense:** questions draw from the course-wide misconception bank
   (manual §3) — answer from evidence; "the evidence doesn't show that" is a
   full-credit sentence.

## 9. Expected Observations

- The bundle contains a re-compromise tell (a host phoning home after its
  "clean" state) — teams with a real go/no-go gate catch it; teams that
  rubber-stamp recovery ship the incident (debrief reveals).
- Inject pressure produces the course's most reliable tell: notes that stop
  being timestamped. The scribe role exists for exactly this.
- Briefings that narrate ("we did X then Y") score below briefings that decide
  ("we recommend Z because evidence E").

## 10. Analysis Questions

1. Which single artifact from Labs 01–15 proved most valuable in this
   simulation, and what does that say about what you should build first in a
   real role?
2. Where did your team's clock-skew/normalization discipline matter (or cost
   you)? One concrete event it changed.
3. The misconception-bank questions were answerable from course material —
   which one came closest to catching your team asserting something the
   evidence didn't show?
4. Your closing synthesis named ≥3 modules' controls for this case. Which
   *one* control, if present pre-incident, collapses the most of this
   scenario — and why is that always a costed judgment, not a slogan?
5. What would your team do differently in the first 15 minutes if this
   happened tomorrow — name one practice, one artifact, one decision rule.

## 11. Troubleshooting

- Falling behind the clock → triage the *record*, not the completion: a
  documented partial state scores above an undocumented complete one (rubric
  says so; believe it).
- Team conflict mid-exercise → IC re-assigns roles on record; the debrief
  handles process, not blame.
- Q&A freeze → return to exhibits: name the frame/log line; if none exists,
  say so and mark it an open question — composure under "I don't know, here's
  how we'd find out" is the professional skill.

## 12. Cleanup Instructions

- Bundle + work copies archived to the team's course folder (feeds the L32
  defense); custody and team sheets submitted; range VMs logged out.

## 13. Submission Requirements

- Team sheet (roles, rotation, contribution statement signed).
- Complete artifact set: triage/scope, severity, containment log, eradication/
  recovery sequence, IOC table, detection addition, briefing deck (or notes),
  Q&A log, custody records.
- Analysis answers (5). Due: end of session — feeds L32 defense and final.

## 14. Expected Output & Evidence

| Artifact | Passing evidence |
|---|---|
| Triage/scope | three-view corroboration; confidence bounds; timestamped |
| Containment/recovery | ladder order + go/no-go gates that actually gate |
| IOC + detection | contextual IOCs; one evidence-justified new rule |
| Briefing + Q&A | decide-able summary; evidence-anchored answers |

## 15. Grading Rubric

Aligned to the capstone defense rubric (answer-key-module-08 §L32):
technical accuracy 30% · evidence discipline 25% · judgment & trade-offs 20% ·
communication 15% · course synthesis 10%. Safety/policy violations cap at
zero per manual §2.

## 16. Instructor Answer Key

Staging ground truth, inject scripts, expected decision points, Q&A bank,
defense logistics: `teaching/lab-answer-keys/lab-16-answer-key.md`
(instructor-only).
