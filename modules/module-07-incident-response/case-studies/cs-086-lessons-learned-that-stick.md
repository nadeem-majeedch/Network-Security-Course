---
case: cs-086
title: Post-Incident Review That Produces Change
difficulty: expert
domain: Incident response
module: 7
lecture-anchor: L27
clos: [CLO-14]
time-estimate: 15 min (5 min reasoning + 10 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-086-solution.md
---

# cs-086 — Post-Incident Review That Produces Change

> **Simulated scenario.** The incident and its aftermath are fictional.

## Difficulty & Domain

- **Difficulty:** Expert · **Domain:** Incident response · **CLO:** CLO-14
- **Est. time:** 15 minutes · **Anchor:** L27 (Eradication, Recovery & Lessons Learned)

## Scenario

Twelve days after the ransomware precursor incident (cs-082/c-084's
firm), the review meeting has been scheduled three times and
cancelled twice. When it finally runs, it produces 14 "action items"
— all phrased as "review X", "consider Y", no owners, no dates. Two
quarters later, none have closed. You have been asked to redesign the
review so it produces change: blameless in form but accountable in
output.

## Stakeholders

- **IR lead (you)** — redesigning the process.
- **Incident participants** — fear blame; some hid mistakes.
- **Engineering managers** — own the systems that need changing.
- **Compliance** — needs evidence the review happened and mattered.

## Network Context

- The incident record: timeline, alerts, containment actions, RTO
  actual (19 h vs 24 h target), backup spot-check results.
- 14 legacy action items, zero closed.
- No standing forum between incidents.

## Available Evidence

- The review doc: 14 vague items, no owners, no dates, no success
  criteria.
- Participant interviews: two engineers admitted (privately) they
  disabled a noisy alert weeks before the incident — never surfaced
  in review.
- MTTD for the incident: 26 h; MTTR 19 h.

## Student Task

1. Redesign the **review format**: agenda, roles, inputs, outputs —
   such that output items are *owned, dated, and verifiable*, and the
   format is blameless enough that the disabled-alert behavior would
   actually surface.
2. Write the **conversion rule**: how a vague item ("review external
   access") becomes an owned, dated, verifiable one. Show it applied
   to two of the 14.
3. Design the **follow-through mechanism** that survives busy
   calendars (who reviews open items, when, what happens on chronic
   non-closure).
4. Answer: **what should compliance receive** as evidence that this
   review was real and effective?

## How to Approach This (Reasoning Scaffold)

- Blamelessness is not comfort — it is *information policy*: people
  surface facts only when facts are safe. The disabled alert is the
  test case: the review design must make that admission useful, not
  punishable.
- An action item is a contract: owner + date + observable done-state.
  Anything less is a wish.
- Follow-through is a system property, not personal virtue — design
  the forum, not the reminder.

## CLO Mapping

- **CLO-14** — Post-incident learning converted to control change.

## Safety Notes

- Simulated; no real-incident references.
