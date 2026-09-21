---
case: cs-082
title: Ransomware Pre-Encryption — Wait or Act? (Solution)
difficulty: expert
module: 7
lecture-anchor: L26
clos: [CLO-11, CLO-12]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-082 — Solution: Ransomware Pre-Encryption, Wait or Act?

> **INSTRUCTOR ONLY.** Model solution for cs-082.

## Model Solution

### 1. Act or wait — decide

**Act now.** The error asymmetry decides it: acting on a false
positive costs a maintenance-window reboot of one server; waiting on a
true positive costs an 8 TB production share and 400 users' workday.
With staging egress + task creation + mass rename inside 4 minutes,
the pre-encryption hypothesis is strong — and this window is the only
cheap one.

### 2. Containment sequence (next 10 minutes)

| # | Action | Class |
|---|---|---|
| 1 | EDR isolate FS01 (network containment, host stays up for forensics) | **Reversible** |
| 2 | Block the staging domain at proxy + DNS | **Reversible** |
| 3 | Snapshot/preserve: copy the scheduled task + service definitions before any cleanup | **Reversible** (adds evidence) |
| 4 | Pull the workstation's switch port / isolate the source workstation | **Reversible** |
| 5 | Suspend the new scheduled task + service (not delete) | **Reversible** |
| 6 | Verify last backup integrity + take an ad-hoc backup of critical shares *from a clean point* | **Reversible** |

No host rebuild, no share restore — those are **irreversible-class**
moves for after scoping.

### 3. Telemetry gaps

- **Gap 1:** no NDR/Zeek on the server VLAN — SMB staging from the
  workstation was only visible as a flow spike, not parsed.
- **Gap 2:** identity telemetry did not alert on the *workstation→
  server* credential use (service account anomalous use undetected).
- **Fix:** east-west NDR/Zeek + a detection on service-account use
  outside its host. Either alone would have moved detection ~20 min
  earlier; together, they remove the ambiguity entirely.

### 4. Executive one-liner

> "We caught an attempted ransomware event mid-staging and contained
> the server within 4 minutes; no files are encrypted, backups are
> verified, and I need two hours with the server offline to confirm
> scope."

## Alternative Solutions

- **Wait 10 min for rename-pattern confirmation:** defensible if EDR
  confidence were low; rejected here — the egress + task signals make
  the prior strong, and the cost asymmetry punishes waiting.
- **Power off immediately instead of isolate:** kills execution but
  destroys volatile evidence and complicates forensics; isolate is
  strictly better when EDR supports it.

## Tradeoffs

- Speed vs scope certainty: acting at 21:48 maximizes the chance the
  share survives but accepts a possible false positive.
- Isolation vs shutdown: evidence preservation vs certainty of kill.

## Common Mistakes

- Waiting for "more alerts" — pre-encryption windows close in minutes.
- Deleting the task/service (destroys evidence) instead of suspending.
- Forgetting the *source workstation* — the initial access is still
  live elsewhere on the network.

## Instructor Prompts

- "What is the cost of being wrong in each direction — and which one
  is career-ending?"
- "Why suspend rather than delete the persistence artifacts?"
- "Which telemetry gap was closest to preventing the whole incident?"

## Rubric (10 pts)

| Criterion | Pts |
|---|---|
| Decision with explicit error-asymmetry reasoning | 3 |
| Containment sequence ≥5 steps, correct classes, evidence-safe | 3 |
| Both telemetry gaps + the one control identified | 2 |
| Executive one-liner (event, action, need) | 2 |

## Safety Notes

- Simulated; no ransomware artifacts, IOCs from real campaigns, or
  destructive content included.
