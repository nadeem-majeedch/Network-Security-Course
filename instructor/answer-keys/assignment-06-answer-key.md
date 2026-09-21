---
assignment: assignment-06
type: answer-key
instructor-only: true
distribution: never-publish-to-students
clos: [CLO-11, CLO-12]
marks: 100
status: complete
---

# Answer Key — Assignment 6 (IR Runbook Development)

> **INSTRUCTOR ONLY.** Three scenario options share one grading spine;
> scenario-specific expectations below.

## Grading anchors (all options)

### 1. Trigger & scope (15)
Named telemetry per detection (EDR behavioral + flow + Zeek/proxy per
option) = 8; corroboration steps that *name the sources* (three-way
discipline) = 7. Single-source triggers with "investigate further" cap
at 10.

### 2. Decision points (30) — the graded core
Each decision needs: **condition set → pre-decided answer → reversibility
class**. The three canonical calls:
- **Contain vs observe:** contain when corroboration ≥2 sources (or
  single-source with stated error-asymmetry — the cs-082 logic);
  observe only when host is clean and identity not yet stolen.
- **Credential rotation scope:** the credential is the blast radius, not
  the host (cs-088) — rotate estate-wide for shared/service accounts,
  per-user for unique identities; irreversible-class user friction noted.
- **Comms timing:** holding statement at declaration, *before* facts
  complete; the "awareness vs certainty" distinction (cs-090) must
  appear for options (a)/(c)'s data-exposure angle.

Runbooks with decisions but no condition sets cap at 18/30; with no
reversibility labels cap at 15.

### 3. Action sequence (20)
Numbered, role-owned, evidence-preserving (suspend-not-delete; isolate-
not-wipe) (12); rollback per reversible action (8). Missing evidence-
preservation notes cap at 14.

### 4. Escalation & comms (15)
Criteria-based escalation (time-boxed, severity-triggered) (8); holding
statement in the cs-099 structure — facts + labeled unknowns + next-update
commitment, no invented certainty (7).

### 5. Tabletop execution (20)
The record must show **specific failure/repair moments** ("runbook said
X; we discovered the flow logs needed querying first — amending step 3")
= 15+; generic "it went well" records cap at 10. Unexercised runbook
= hard 70% cap per the brief.

## Scenario-specific expectations

- **(a) Ransomware staging:** staging-egress block + host isolation +
  task/service suspension (not deletion); backup-generation check
  (cs-084) must appear in eradication/recovery steps.
- **(b) MFA-fatigue phishing:** session/token revocation *in addition to*
  password reset (the cs-100 lesson — password reset alone misses the
  live session); number-changing/push-hardening in post-incident.
- **(c) Cloud egress:** attribution-before-block discipline (cs-065:
  verify agent/update benign-ness first); containment via subnet/NACL/
  egress construct without touching the instance; VPC flow logs as the
  attribution source.

## Common failure patterns

- Runbooks that narrate IR theory instead of pre-deciding decisions
  (theory lives in lectures; the runbook's value is decisions).
- Holding statements that promise certainty ("no data was accessed").
- Rollback omitted — the reversibility discipline asserted in decisions
  but absent from the sequence.
