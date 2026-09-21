---
case: cs-085
title: Restoring AD After Directory Compromise (Solution)
difficulty: expert
module: 7
lecture-anchor: L27
clos: [CLO-11, CLO-14]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-085 — Solution: AD Restore After Directory Compromise

> **INSTRUCTOR ONLY.** Model solution for cs-085.

## Model Solution

### 1. Recovery-order sequence (trust flows along the path)

| # | Step | Why here |
|---|---|---|
| 1 | **Build a clean management workstation** (fresh OS, no domain join, patched) | Every later step needs trusted admin tooling — this is the root of trust |
| 2 | **Build 2 new DCs from clean media** in a *parallel* environment (new names, isolated L2/L3, no replication from old DCs) | Clean directory infrastructure cannot coexist with replication from tainted peers |
| 3 | **Restore AD data from the 40-day clean backup** onto the new DCs (authoritative restore of objects) | Data comes from a pre-dwell source, not a scrubbed-compromise snapshot |
| 4 | **Re-create the 40 days of changes** from reliable sources (HR, app exports, diff of old-DC exports reviewed for rogue objects) | Cost of the clean-backup choice, paid deliberately |
| 5 | **Reset KRBTGT twice** (once now, once ~12 h later) on the *new* directory | Breaks Golden-Ticket capability only now that no DC holding the old key history remains |
| 6 | **Reset all privileged credentials** (DA, schema, service accounts) — passwords were in the dumped ntds.dit | The dump outlives the hosts it came from |
| 7 | **Migrate systems/members** to the new DCs; decommission old DCs (preserve as evidence, offline) | Clean path extends outward; old state is quarantined, not re-merged |

### 2. KRBTGT timing

Resetting KRBTGT while any compromised DC still runs is wasted: the
attacker can re-dump it and mint new tickets. The correct window is
**after step 3's directory is trusted**: first reset when the new DCs
are authoritative, second reset after the old DCs are offline (or ~12
h later) to cover tickets issued during the transition. Two resets,
both *after* clean infrastructure exists — not a reset at incident
start for theater.

### 3. Backup-generation choice

- **40-day clean restore (chosen):** known-clean provenance; costs
  40 days of directory changes to re-create (HR-driven, ~3–5 days of
  team effort) plus user-visible churn. Auditable — every object's
  provenance is one sentence.
- **Newer scrubbed restore:** saves re-creation but requires proving
  a *negative* across 39 generations ("no rogue artifacts anywhere")
  — weeks of review, weaker audit story, residual unknowns.

**Position:** take the 40-day restore; directory data re-creation is
bounded and verifiable, scrubbing 39 generations is neither.

### 4. Re-tainting vectors

1. **Management workstation** — a domain-joined or previously
   compromised admin host passes tainted credentials/tools into every
   clean step; hence step 1.
2. **Replication** — any new DC replicating from an old one imports
   the compromise wholesale; hence parallel build with no
   replication from old estate.
3. **Admin credentials** — privileged passwords from the dumped
   database are burned and must not touch the new directory until
   reset; reusing them "temporarily" re-taints the clean build.

## Alternative Solutions

- **Forest functional-level migration / new forest:** the maximal
  version of the same logic — costs migration effort; right answer
  at larger scale or with structural AD debt.
- **Scrub-and-keep newer backups:** viable only with strong
  evidence the dwell was short and artifacts fully enumerated;
  rejected here given 2-week DA hold.

## Tradeoffs

- Clean provenance vs data loss: 40 days of re-creation buys a
  defensible audit story and zero unknowns.
- Speed vs chain-of-trust: every skipped trust step saves hours now
  and re-opens the incident later.

## Common Mistakes

- Resetting KRBTGT first "to be safe" (theater — attacker re-dumps).
- Rebuilding DCs with the same names and letting them replicate.
- Forgetting that *privileged credentials* are compromised material,
  not just hosts.
- Doing the rebuild from the existing management workstation.

## Instructor Prompts

- "What is the root of trust in this plan, and what makes it clean?"
- "Why does the double KRBTGT reset exist — what does the second one
  cover?"
- "If the 40-day backup were corrupt, what is your fallback?"

## Rubric (10 pts)

| Criterion | Pts |
|---|---|
| Recovery order correct with dependency reasoning | 3 |
| KRBTGT timing (both resets, correct window) | 2 |
| Backup choice argued with both cost sides | 2 |
| All three re-tainting vectors identified | 3 |

## Safety Notes

- Simulated; Golden-Ticket referenced conceptually (impact, not
  forgery steps).
