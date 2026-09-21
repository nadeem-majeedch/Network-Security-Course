# cs-041 — Key-Management Lapse Root-Cause Analysis

> **Simulated scenario.** The company, pipeline, and incident are fictional.

## Difficulty & Domain

- **Difficulty:** Intermediate · **Domain:** VPN and secure remote access · **CLO:** CLO-5
- **Est. time:** 12 minutes · **Anchor:** L13 (Cryptographic Foundations)

## Scenario

A SaaS company's nightly encrypted-backup restore *fails*: the restore
service can't decrypt last month's archive. Digging in, the team finds a
cascade (below). No attacker is involved — this is a **key-management
lapse** with confidentiality *and* availability consequences. You run the
root-cause analysis and design the fixes.

## Stakeholders

- **SRE** — owns backups; already know restore is broken.
- **Compliance** — encrypted backups were the audit answer; the answer is now wrong.
- **Data owners** — one month of archives may be unrecoverable.
- **The 5-person platform team** — no dedicated security engineer.

## Network Context

- Backup flow: app servers → backup service (client-side encrypt with KEK)
  → object storage.
- Keys: one **static KEK** in a config file (gitignored, but...) used for
  all archives; DEKs per archive generated locally.
- Rotation: none ("nothing ever rotated it").

## Available Evidence

**The cascade (in order):**

1. 14 months ago: KEK generated, placed in config file on the backup
   service; gitignored; a copy in the on-call wiki "for emergencies."
2. 8 months ago: server migrated; KEK file copied to new host. Old host
   decommisioned **without key material revocation** (disk wiped later).
3. 3 months ago: wiki migrated; the KEK page was lost in migration —
   nobody noticed (config file still worked).
4. Last month: engineer rotated *the config system's* master secret,
   believing it was the KEK; re-encrypted the *config file wrapper* only.
   DEK-wrapping KEK unchanged — restores still worked. Confusion began.
5. This week: storage lifecycle policy archived cold-tier objects and the
   **config file was deleted** by a cleanup job; the wiki copy is gone;
   KEK unrecoverable. Last month's archives: undecryptable.

## Student Task

1. Produce the **root-cause chain** (not a single cause): the 3 distinct
   failure classes visible in the cascade, each with the control that was
   missing.
2. Answer compliance's question precisely: **what was actually lost** —
   confidentiality exposure, availability exposure, or both? Justify from
   the evidence (old host's disk, wiki copy, rotation confusion).
3. Design the **minimum viable key management** for a 5-person team
   (KMS/envelope, rotation, escrow, break-glass) — 6 bullets max — and name
   the one practice that would have prevented the loss outright.

## How to Approach This (Reasoning Scaffold)

- Root cause ≠ the cleanup job: ask why *one copy* of a critical secret
  could delete the ability to read backups (secrets have no backup?).
- Distinguish exposure (confidentiality) from loss (availability) per event:
  the old host, the wiki, the rotation confusion each differ.
- MVP key management for tiny teams exists: KMS + envelope + escrow +
  break-glass is a *day-one* design, not enterprise luxury.

## CLO Mapping

- **CLO-5** — Key-lifecycle failures and minimal-controls design.

## Safety Notes

- Simulated incident; no real key material anywhere.
