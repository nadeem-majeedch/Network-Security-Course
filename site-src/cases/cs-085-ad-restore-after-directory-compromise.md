# cs-085 — Restoring AD After Directory Compromise: The Rebuild Order Problem

> **Simulated scenario.** The compromise, estate, and recovery plan are fictional.

## Difficulty & Domain

- **Difficulty:** Expert · **Domain:** Multi-stage security incidents · **CLO:** CLO-11, CLO-14
- **Est. time:** 15 minutes · **Anchor:** L27 (Eradication, Recovery & Lessons Learned)

## Scenario

After a 3-week dwell-time incident (cs-083's estate, worse outcome:
the attacker held DA for ~2 weeks before detection), the directory
itself is untrusted. Both DCs are presumed compromised; the attacker
created accounts, modified a GPO, and dumped the KRBTGT key. You own
the recovery-order plan. The trap: restoring in the wrong order
*re-imports the compromise* — a restored DC that replicates from a
compromised peer re-taints itself, and a KRBTGT reset done before the
DCs are clean just gets re-dumped.

## Stakeholders

- **IR lead (you)** — owns the recovery sequence.
- **Directory team** — executes; worried about a broken forest.
- **HR/Finance** — 6,000 users' productivity hangs on auth.
- **Auditors** — will ask what was trusted, when, and why.

## Network Context

- Single forest, single domain, 2 DCs (both presumed compromised),
  6,000 users, 12 branch sites.
- Backups: nightly system-state, last known-good 40 days ago
  (pre-dwell); newer backups exist but span the dwell window.
- Attacker artifacts: 2 rogue accounts, 1 rogue GPO, KRBTGT dump
  (evidenced by DCSync patterns), possible Golden-Ticket capability.
- No clean management workstation currently exists.

## Available Evidence

| Artifact | State |
|---|---|
| DC01, DC02 | both show rogue artifacts; neither individually "cleaner" |
| System-state backup | 40 days old (clean), 39 newer (span dwell) |
| Rogue accounts/GPO | identified, disabled/unlinked, archived |
| KRBTGT | dumped; current password age > dwell window |
| Management workstation | previously domain-joined; presumed tainted |

## Student Task

1. Produce the **recovery-order sequence** — what is rebuilt/reset
   first through last, with the dependency that each step's output is
   trusted only because of the step before it. (Hint: build a clean
   *path*, not a clean *moment*.)
2. Answer the **KRBTGT timing question**: why is resetting it before
   the DCs are rebuilt wasted effort, and what is the correct double-
   reset window in this plan?
3. Decide the **backup-generation question**: restore from the 40-day
   clean backup (data loss + re-create 40 days of changes) vs a newer
   dwell-spanning backup with artifact scrubbing? Take a position and
   name what each choice costs.
4. Identify the **re-tainting vectors** — the three ways your
   carefully rebuilt directory gets re-compromised during recovery
   itself (management workstation, replication, admin credentials).

## How to Approach This (Reasoning Scaffold)

- Trust must flow along the rebuild path: clean build → clean OS →
  clean directory → clean credentials. Every shortcut that pulls
  tainted state forward (replication from a compromised peer, a
  domain-joined admin workstation) breaks the chain.
- KRBTGT is a *credential*, not a host state: resetting it only
  matters when the hosts holding its history are gone — otherwise
  the attacker re-dumps it from the still-compromised DC.
- The 40-day restore is not the only cost: newer backups carry
  unknown-unknown scrubbing burden. Quantify both.

## CLO Mapping

- **CLO-11** — Recovery sequencing under deep compromise.
- **CLO-14** — Evidence/trust-chain preservation during rebuild.

## Safety Notes

- Simulated; Golden-Ticket discussed conceptually only (what it
  enables, not how to forge).
