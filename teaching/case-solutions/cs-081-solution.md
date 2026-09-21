---
case: cs-081
title: Phishing-Driven Intrusion — First-Hour Triage (Solution)
difficulty: expert
module: 7
lecture-anchor: L26
clos: [CLO-11, CLO-12]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-081 — Solution: Phishing-Driven Intrusion, First-Hour Triage

> **INSTRUCTOR ONLY.** Model solution for the graded formative case cs-081.

## Model Solution

### 1. Corroboration checks (CLO-12)

| Check | Sources | What it establishes |
|---|---|---|
| A | EDR (dump + task) ↔ VPN logs (session active) | Attacker is *live*: session active AND host-level tooling running → mid-operation, not dormant |
| B | Proxy log (webmail UA/IP) ↔ VPN login (same residential IP) | Same actor across both footholds → one intrusion, not two |
| C | FW allow-flow (SMB/LDAP sweep) ↔ payroll access (2 sessions) | Lateral + data-access both happened; payroll export = data-movement hypothesis |

### 2. Containment sequence (CLO-11, reversible-before-irreversible)

| # | Action | Class | Severs |
|---|---|---|---|
| 1 | Kill the live VPN session + block the source IP at the edge | **Reversible** | The attacker's *current* control channel |
| 2 | Disable the harvested webmail session (revoke tokens/sessions) | **Reversible** | Cookie-based webmail foothold |
| 3 | Isolate the accountant's host (network containment) | **Reversible** | Local execution + persistence host |
| 4 | Block the phishing domain at proxy/DNS | **Reversible** | Re-click / re-harvest path |
| 5 | Reset the accountant's password + review AD sign-ins for the dumped-credential use | **Semi-irreversible** (user friction) | Credential reuse |

**Judgment call — kill vs observe:** kill. Deciding evidence: the
EDR dump alert + scheduled task mean the attacker holds *credentials
and persistence*, so observation buys little intelligence while the
session is actively dumping. If the only telemetry were the VPN login
and no host alerts, observe-first would be defensible. State the
condition that flips the answer.

### 3. First-hour legal brief

- **Exposure hypothesis:** payroll reports exported (2 sessions,
  40 min) — treat as PII exposure until proven otherwise.
- **Evidence state:** preserved (EDR telemetry, VPN/proxy logs, host
  image pending); no destructive actions taken on the host.
- **Pending:** host forensics (scheduled task artifacts), payroll
  access-log export for counsel.

## Alternative Solutions

- **Observe-first** (defensible when host is clean): monitor the VPN
  session to map C2 and data movement before killing — trades risk of
  continued access for richer attribution. Reject here because of the
  dump alert.
- **Isolate host first, VPN second:** protects the endpoint fastest
  but leaves the attacker's *network* path alive to pivot elsewhere.

## Tradeoffs

- Kill-now vs intelligence: alerting the attacker loses visibility
  but caps damage; observe buys time at the cost of active intrusion.
- Speed vs evidence preservation: isolating (not wiping) preserves
  evidence while containing.

## Common Mistakes

- Sequencing irreversible actions first (rebuild, lockout) before the
  cheap reversible ones.
- Treating webmail and VPN as two incidents (they share the phish kit).
- Forgetting the persistence artifact (scheduled task) — killing the
  session does not remove it.

## Instructor Prompts

- "What single piece of evidence flips kill-vs-observe?"
- "Which containment action is the hardest to undo — and why is it
  still in your list?"
- "What does counsel need in hour one that they cannot get from IT?"

## Rubric (10 pts)

| Criterion | Pts |
|---|---|
| 3 corroboration checks correctly mapped | 3 |
| ≥5 containment actions, correct order + reversibility labels | 3 |
| Judgment call argued with deciding evidence | 2 |
| Legal brief complete in triage-ready form | 2 |

## Safety Notes

- Simulated; no exploit content.
