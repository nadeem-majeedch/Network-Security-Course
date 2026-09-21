---
case: cs-089
title: Tainted Update — Trusted-Channel Compromise (Solution)
difficulty: expert
module: 7
lecture-anchor: L26
clos: [CLO-11, CLO-12, CLO-15]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-089 — Solution: Tainted Update via Trusted Channel

> **INSTRUCTOR ONLY.** Model solution for cs-089.

## Model Solution

### 1. Scope stratification

| Tier | Population | Status | Evidence |
|---|---|---|---|
| 1 | 3 servers | **Affected** | anomalous agent children + C2 cadence + svc_ops interactive + internal spread |
| 2 | All hosts in the tainted-build window (~4,750) | **Suspect — verified clean-so-far** | no anomalous agent behavior on endpoints (EDR); absence is weaker for *unsigned* stage-2 but meaningful for process-level tells |
| 3 | Pilot ring (50) | **Likely clean** | received build *before* window; check manifests to confirm ring dates |

**Stages reached (tier 1):** delivery → execution → C2 →
credential use (svc_ops) → internal spread (backup + build servers
— the latter is *build infrastructure*: worst-case extension of the
supply chain into your own pipelines).

**Cannot determine (say so):** what stage-2 did on the 2 internal
servers (no EDR alerts there — coverage gap?), whether stage-2
persistence survives the agent's replacement, and whether endpoints
in tier 2 got a *dormant* stage-2 (absence of behavior ≠ absence of
implant). Each unknown gets a verification task, not a shrug.

### 2. Vendor-trust question

**Verifiable locally:** (a) pull the agent binary + update manifests
from a tier-1 host — hash against vendor's published tainted/clean
list; (b) confirm *your* ring dates vs their window; (c) EDR
timeline of the agent children (day −19…−17) vs their claimed
mechanism; (d) the svc_ops interactive session (your AD logs) — the
vendor can't spin that.
**Take on faith (for now):** "builds outside the window are clean"
and the *mechanism* of taint. **Demand from vendor:** the exact
tainted build hashes, the IOC/behavior list, whether stage-2
persistence exists outside the agent, and their own telemetry of
your update fetches (timestamped, auditable).

### 3. Containment for trusted-channel compromise

The delivery mechanism is the attacker → **the channel is the first
containment target**, before hosts:

| # | Action | Rationale |
|---|---|---|
| 1 | **Halt auto-updates fleet-wide** (block the channel); pin the last known-clean build | Stops *future* taint; buying time for vendor's clean build costs nothing |
| 2 | Network-contain the 3 servers (evidence-preserving) + block the 6 C2 domains | Live stage-2 sessions die; hosts stay up for forensics |
| 3 | Disable svc_ops interactive use (service accounts never log in interactively) + rotate it | Kills the credential pivot |
| 4 | Isolate the 2 internal spread targets — especially the **build server** (treat as compromised pipeline) | Prevents self-propagation via your own builds |
| 5 | Tier-2 hosts: heightened monitoring, don't reimage 4,700 machines on suspicion | Proportionality — containment matches evidence |
| 6 | When vendor's clean build + hashes arrive: staged redeploy *with* EDR watch on agent children | Replacing the agent is eradication's delivery vehicle — use the same channel deliberately |

### 4. CEO status (three sentences, durable)

> "We are affected on three servers out of 4,750 systems and have
> contained all known attacker access as of this morning. We halted
> the software's update channel, are verifying every system that
> received it, and expect full verification within [N] days. I need
> legal engaged on disclosure timing and authority to keep the
> update freeze until the vendor's verified-clean build ships."

Every sentence survives new facts: scope *may widen* (says "known
attacker access"), the freeze is a *decision with a reason*, and the
asks are concrete.

## Alternative Solutions

- **Fleet-wide reimage:** burns weeks and destroys evidence; justified
  only if stage-2 persistence proves unrecoverable.
- **Trust the vendor's window, contain only it:** faster, but your
  tier-2 "clean" is behavioral, not provenance-based — keep both
  evidence streams running.

## Tradeoffs

- Update freeze vs patch posture: the freeze blocks *all* fixes from
  that vendor — time-box it and pair with compensating monitoring.
- Disclosure speed vs certainty: legal needs the three-sentence
  frame, not final numbers; premature certainty is the bigger
  disclosure risk.

## Common Mistakes

- Scoping by *symptom* (3 hosts) instead of by *channel* (the whole
  tainted ring) — under-containment.
- Reinstalling the vendor's "clean" build without verifying hashes
  locally.
- Treating build-server compromise as ordinary server news — your
  own pipeline is now a supply-chain risk to *your* software.
- A CEO status full of hedges that becomes false in a week.

## Instructor Prompts

- "Which containment action would you take even with zero vendor
  cooperation?"
- "Why is the build server the scariest internal target?"
- "What makes the three-sentence status survive Monday's new facts?"

## Rubric (10 pts)

| Criterion | Pts |
|---|---|
| Scope stratification with stages + cannot-determine set | 3 |
| Vendor verification split (local vs faith) + asks | 2 |
| Trusted-channel containment sequence (channel first, svc_ops, build server) | 3 |
| CEO status: accurate, durable, actionable | 2 |

## Safety Notes

- Simulated; fictional vendor/incident; no exploit detail.
