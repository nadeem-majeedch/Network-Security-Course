---
case: cs-083
title: Isolating a Domain Controller at 2 a.m. (Solution)
difficulty: expert
module: 7
lecture-anchor: L26
clos: [CLO-11, CLO-12]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-083 — Solution: DC Containment, Kill vs Survive

> **INSTRUCTOR ONLY.** Model solution for cs-083.

## Model Solution

### 1. Containment posture: (b) partial containment — with teeth

Full isolation of a production DC is a business outage; leaving it is
a directory foothold. The middle path closes the attacker's *specific*
access while the DC keeps serving:

- Disable the rogue admin account **svc_backup2** (created 23:20).
- Unlink and quarantine the rogue GPO (keep a copy as evidence).
- Block SRV-FIN-02 → DC01 (and → DC02) at the firewall/NDR level —
  the suspected source stops talking to *any* DC.
- Escalate DC01's Kerberos/event telemetry to watch for *new* access
  attempts from other sources.

This is not "leave and monitor": the attacker's demonstrated channels
are all closed; what remains is generic DC operation.

**Cost-of-wrong analysis:**

| Posture | Wrong cost |
|---|---|
| Full isolate | Branch auth pain; if wrong (attacker already evicted), outage for nothing |
| Partial | If wrong (attacker has *another* path), foothold persists — but every known path closed |
| Leave | If wrong, directory-level persistence compounds; worst tail risk |

### 2. Revocation set (minimum directory actions)

1. Disable svc_backup2 (not delete — evidence).
2. Unlink + archive the rogue GPO.
3. Reset the KRBTGT account **twice** (standard post-compromise step;
   scheduled with directory team for the recovery window, not 3 a.m.
   improvisation).
4. Audit admin-group membership + new account creation back to 22:00.

### 3. Why DC02's cleanliness is load-bearing

Partial containment *relies on* DC02 being trustworthy — if the
attacker has DC02 too, you've contained one of two compromised DCs.
Checks before leaning on it: (a) NDR shows no DCSync-pattern reads
into DC02 from any source; (b) no new accounts/GPOs on DC02 since
22:00; (c) replication metadata shows only expected partners. If any
check fails, posture escalates to full isolation of both.

### 4. Wake-the-CISO threshold

Any of: evidence of a *second* compromised DC; attacker access to
backup infrastructure; confirmed data exfiltration at directory
scale; or a business decision to force password reset of all 6,000
users (cost/PR call, not technical). The technical containment itself
was within on-call authority.

## Alternative Solutions

- **Full isolate DC01 now:** maximally safe, maximal pain; right
  answer if DC02's cleanliness checks failed.
- **Leave + monitor only:** rejected — a rogue GPO is an active
  redeployment mechanism, not passive access.

## Tradeoffs

- Availability vs directory integrity: partial containment keeps auth
  alive but accepts residual risk on unknown paths.
- 3 a.m. KRBTGT reset vs scheduled: doing it immediately is safer
  crypto-wise but risks collateral outage at peak-off-hours staffing.

## Common Mistakes

- Treating the DC like any server — directory footholds change the
  calculus (GPO = execution at scale).
- Skipping the source-host containment (SRV-FIN-02 is the actual
  entry; the DC is the *destination*).
- Trusting "DC02 is clean" without checking the claim.

## Instructor Prompts

- "What fact would move you from partial to full isolation in the
  next hour?"
- "Why is the GPO more dangerous than the admin account?"
- "Who owns the KRBTGT reset decision, and why not you alone?"

## Rubric (10 pts)

| Criterion | Pts |
|---|---|
| Posture chosen with cost-of-wrong analysis | 3 |
| Revocation set complete (account, GPO, KRBTGT noted, audit) | 3 |
| DC02 trust argument with concrete checks | 2 |
| Escalation threshold articulated | 2 |

## Safety Notes

- Simulated; no exploit steps, tooling, or real-incident IOCs.
