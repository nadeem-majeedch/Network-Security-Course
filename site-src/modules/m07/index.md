---
status: complete
artifact-type: module-overview-page
module: 7
instructor-only: false
---

# Module 7 — Incident Response & SOC Operations

**Lectures:** L25–L28 (Weeks 13–14) · **CLOs:** CLO-11, CLO-12 · **Cases:** cs-079–090

*Descriptive orientation. IR practice runs on staged incidents in the lab
range; no real systems are ever targeted.*

## What this module covers

Detection means someone now has to act, under pressure, with partial
information. You learn the full IR lifecycle — preparation, detection &
triage, containment, eradication, recovery, lessons learned — plus the SOC
context it happens in: roles, escalation, maturity, and threat hunting.

## Lectures

| # | Lecture | Core idea |
|---|---|---|
| L25 | [IR Lifecycle & Preparation](../../lectures/lecture-25-ir-lifecycle-preparation.md) | Phases, playbooks, runbook preconditions, roles & escalation |
| L26 | [Detection, Triage & Containment](../../lectures/lecture-26-detection-triage-containment.md) | Evidence corroboration, reversibility-first containment |
| L27 | [Eradication, Recovery & Lessons Learned](../../lectures/lecture-27-eradication-recovery-lessons-learned.md) | Persistence hunting, safe restoration order, go/no-go recovery |
| L28 | [SOC Operations & Threat Hunting](../../lectures/lecture-28-soc-operations-threat-hunting.md) | SOC tiers, maturity by outcomes, hunt hypotheses from intelligence |

## Labs

[Lab-13](../../labs/lab-13-incident-triage.md) (incident triage
on a staged intrusion) and [Lab-14](../../labs/lab-14-tabletop-threat-hunt.md)
(tabletop + guided threat hunt) — the tabletop is discussion-based; the hunt
works from prepared telemetry.

## Case studies (advanced → expert)

cs-079–090: ransomware playbook gap analysis, IR team design, first-hour
phishing intrusion, pre-encryption decision pressure, DC containment judgment,
RTO-vs-evidence conflict, AD restore, lessons-learned that stick, forensic
timeline from five sources, DS-cluster intrusion scoping, supply-chain update
compromise, disclosure decision. See the [case studies guide](../../cases/index.md).

## Skills checkpoints

- Derive runbook preconditions from failure modes rather than memorized phase lists.
- Triage an alert by corroborating three independent telemetry sources.
- Order containment actions reversible-first and defend the ordering.
- Lead a structured tabletop and extract testable improvements from it.
