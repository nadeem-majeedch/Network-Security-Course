---
assignment: assignment-06
week: 13
type: graded
clos: [CLO-11, CLO-12]
lectures: [L25, L26, L27]
lab: Lab-13
marks: 100
weight: 5%
due: end of week 13
status: complete
artifact-type: student-assignment
answer-key: instructor/answer-keys/assignment-06-answer-key.md
---

# Assignment 6 — Incident Runbook Development & Tabletop (Week 13)

> **Weight:** 5% · **Due:** end of week 13 · **CLO-11, CLO-12**
> **Deliverable:** one runbook (4–6 pages) + tabletop record. Teams of 2–3.

## Scenario (simulated)

Choose **one** runbook to develop for the course range organization:
(a) ransomware pre-encryption staging (the cs-082 pattern), (b) credential
phishing with MFA-fatigue approval (the cs-100 pattern), or (c) cloud
egress anomaly on a VPC workload (the cs-065 pattern).

## Tasks

1. **Trigger & scope** (15): detection sources that fire (name the
   telemetry), triage corroboration steps (which second/third sources),
   and the decision point that declares an incident.
2. **Decision points with pre-decided answers** (30): the 3–5 judgment
   calls (contain now vs observe; credential rotation scope; comms
   timing) — each with the **pre-decided answer, its condition set, and
   the reversibility class** of every action. This is the graded core:
   the runbook exists so stress doesn't improvise policy.
3. **Action sequence** (20): numbered steps with owner roles, evidence-
   preservation notes, and rollback for every reversible action.
4. **Escalation & comms** (15): who is called when (criteria, not names),
   and the pre-approved holding statement (facts + labeled unknowns +
   next-update commitment — the cs-099 standard).
5. **Tabletop execution** (20): run the runbook against the matching
   course case (cs-082/cs-100/cs-065) with your team; record where the
   runbook held, where it forced judgment, and the two amendments you'd
   make. Tabletop record (≤300 words) is the deliverable — a runbook
   never exercised caps at 70%.

## Constraints

- Defensive framing only; no offensive tooling content anywhere.
- "Pre-decided answer" means a *condition set*, not a shrug — "contain if
  EDR + flow corroborate staging within 10 min" is the register.

## Submission

PDF/repo Markdown + tabletop record. Rubric: instructor materials.
