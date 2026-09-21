---
case: cs-088
title: Data Science Infrastructure — GPU Cluster Intrusion (Solution)
difficulty: expert
module: 7
lecture-anchor: L26
clos: [CLO-11, CLO-12]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-088 — Solution: GPU Cluster Intrusion Scoping

> **INSTRUCTOR ONLY.** Model solution for cs-088.

## Model Solution

### 1. Scope hypothesis

| Asset | Status | Evidence |
|---|---|---|
| gpu-07 | **Compromised** | brute-force success + mining + NFS credential read |
| lab account (all 32 nodes) | **Credential compromise — presumptive** | password known to attacker; any node reachable with it |
| Data lake via cached tokens | **Exposed — cannot yet confirm abuse** | `~/.aws` read happened; object-store logs show no anomalous reads *yet* |
| Training data (read path) | At risk via tokens; no confirmed access | object-store logs clean so far |
| Other nodes | Unknown — brute-force likely tried cluster-wide | FW shows the attack; per-node auth logs must be checked |
| Model checkpoints (write path) | Untouched | no anomalous writes |

Cannot-determine items: whether the token was copied off-node
(1 file read is visible; exfil of its contents is not), and whether
other nodes were accessed pre-monitoring.

### 2. The PI's request — verdict

**Not acceptable.** Reimaging gpu-07 removes the mining process but
leaves: (a) the lab-account password known to the attacker on every
node, (b) any *other* footholds on other nodes, (c) cached tokens
still valid against the data lake, (d) the original entry path
(brute-force exposure) open. "Quiet" cleanup without credential
rotation guarantees re-entry — and *that*, not the incident, is the
funder-facing story if datasets are later taken.

### 3. Containment preserving research (sequenced)

| # | Action | Research impact |
|---|---|---|
| 1 | Network-contain gpu-07 (keep powered for forensics) | One node lost |
| 2 | **Rotate the lab-account credential cluster-wide** + expire active sessions | Brief job interruption; the real fix |
| 3 | **Revoke/rotate the exposed object-store tokens** | Token-scoped; jobs re-auth |
| 4 | Rate-limit + restrict SSH source (VPNs only) on all nodes | Transparent to on-campus |
| 5 | Audit object-store logs against all *other* lab tokens for the dwell window | Read-only, zero downtime |
| 6 | Check per-node auth logs for other lab-account logins | Zero downtime |
| 7 | Phased node rebuilds via scheduler drain (rolling) | Cluster stays ≥90% utilized |

### 4. Credential blast radius

The `~/.aws` read means the token was *available to the attacker* —
treat as compromised regardless of later abuse. Because NFS logs
can't distinguish researcher from attacker reads, absence of
anomalous object-store activity is weak reassurance: the attacker
would read with the same identity. **The control that makes it
distinguishable: per-job/per-user identity** — short-lived,
job-scoped credentials (workload identity / per-session tokens)
instead of long-lived cached keys, so every data-lake read carries
an attributable identity. Secondary: EDR on nodes (the read would
correlate with the mining session, not a researcher's job).

## Alternative Solutions

- **Full cluster shutdown** (max safety): defensible if funder/
  compliance demands certainty; costs 30 researchers' weeks — the
  phased plan reaches the same credential-security end state
  without the total stop.
- **Rotate only gpu-07's exposure:** inadequate — the credential is
  cluster-wide by design.

## Tradeoffs

- Mission continuity vs certainty: phased containment keeps research
  alive but accepts days of residual unknowns; shutdown buys
  certainty at total mission cost.
- Per-job identity vs convenience: the durable fix has real
  engineering cost — this incident is its business case.

## Common Mistakes

- Treating a node compromise as only a node problem (credentials
  outlive nodes).
- Accepting "no anomalous reads" as clearance when identity is
  shared (absence of anomaly ≠ absence of access).
- Rotating credentials *after* rebuilding nodes — order matters.

## Instructor Prompts

- "What is the actual blast radius — the node or the account?"
- "Which containment step, if skipped, guarantees re-entry?"
- "What telemetry redesign makes the next incident scoping trivial
  instead of agonizing?"

## Rubric (10 pts)

| Criterion | Pts |
|---|---|
| Scope hypothesis with compromised/exposed/cannot-determine split | 3 |
| Quiet-cleanup verdict with unresolved-list | 2 |
| Containment sequence preserving research (credential rotation early) | 3 |
| Blast-radius answer + attribution control | 2 |

## Safety Notes

- Simulated; no mining tools, no real datasets.
