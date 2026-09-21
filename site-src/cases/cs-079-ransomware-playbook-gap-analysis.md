# cs-079 — IR Playbook Gap Analysis for Ransomware

> **Simulated scenario.** The playbook, tabletop injects, and gaps are fictional.

## Difficulty & Domain

- **Difficulty:** Expert · **Domain:** Incident response · **CLO:** CLO-11
- **Est. time:** 15 minutes · **Anchor:** L25 (IR Lifecycle & Preparation)

## Scenario

A logistics company has a ransomware playbook — 40 pages, written 3 years
ago. A tabletop exercise (4 injects, below) exposed that the playbook
*describes phases but cannot be executed*: the gaps are operational, not
conceptual. You must run the gap analysis: playbook statement → what
execution requires → what's missing → the fix — and rank fixes by
first-hour value.

## Stakeholders

- **CISO** — the playbook was the compliance artifact; now it's evidence of over-claiming.
- **IR team (4 people)** — must execute under stress; vague steps cost minutes they don't have.
- **Legal/insurance** — notification and ransom-payment decision paths are theirs.
- **Board** — will read the gap report.

## Network Context

- Estate: 3 sites, EDR on 80% of servers (legacy apps excluded), backups:
  nightly disk-to-disk + weekly offline (tapes, untested restore).
- Communication: corp email + Teams (both on the same AD!). No OOB
  comms plan.
- Playbook (summarized): "Phase 1: Detect. Phase 2: Contain (isolate
  infected systems). Phase 3: Eradicate. Phase 4: Recover. Phase 5:
  Lessons." No role names, no decision criteria, no vendor contacts.

## Available Evidence

**Tabletop injects and failures:**

| Inject | What the playbook said | What broke in execution |
|---|---|---|
| I1 (T+0): "Encryption spreading from file server" | "Isolate infected systems" | *how*? EDR-isolate feature exists but the legacy 20% isn't EDR-covered; nobody knew the switch-port procedure for non-EDR hosts |
| I2 (T+30m): "AD being attacked; disable accounts?" | (nothing specific) | disabling AD = disabling the *isolation tool* (EDR console is AD-authed) — sequencing dilemma with no playbook answer |
| I3 (T+2h): "Backup tapes: restore file server" | "Restore from backup" | tape restore *untested in 3 years*; nobody knew which tapes, which offsite vendor, or the drive's firmware state |
| I4 (T+4h): "Reporter calls; ransom note leaked" | "Contact communications" | no named comms lead, no pre-approved holding statement, no legal escalation path beyond "call legal" (which legal?) |

## Student Task

1. Build the **gap table**: for each inject — playbook statement →
   execution requirement → missing element → fix (concrete artifact:
   runbook step, contact list, decision matrix, tested procedure).
2. Identify the **sequencing dilemma** (I2) as a class: dependencies
   between response actions (AD vs EDR console vs comms) that the
   playbook never mapped — and the standard resolution (break-glass
   accounts, OOB comms).
3. Rank the **fixes by first-hour value** (what saves the most minutes
   at T+0–T+60) and design the **retest plan** (which inject proves
   which fix).

## How to Approach This (Reasoning Scaffold)

- Phase-words vs runbook-verbs: "isolate" is a phase; "EDR-isolate via
  console X, or switch-port shutdown via runbook §4.2" is a verb —
  the gap is verbs.
- Dependency mapping is the hidden discipline: every response tool that
  auths to the domain being attacked is a single point of failure —
  break-glass is the answer class.
- Untested restore = no restore (I3): the backup's restore path needs
  the same evidence standard as any control.

## CLO Mapping

- **CLO-11** — IR-preparation engineering and playbook hardening.

## Safety Notes

- Tabletop framing; no ransomware-operation guidance — this is defense
  readiness.
