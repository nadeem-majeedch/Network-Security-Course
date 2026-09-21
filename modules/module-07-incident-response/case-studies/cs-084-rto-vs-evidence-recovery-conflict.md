---
case: cs-084
title: RTO vs Evidence — The Recovery-Speed Conflict
difficulty: expert
domain: Multi-stage security incidents
module: 7
lecture-anchor: L27
clos: [CLO-11, CLO-14]
time-estimate: 15 min (5 min reasoning + 10 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-084-solution.md
---

# cs-084 — RTO vs Evidence: The Recovery-Speed Conflict

> **Simulated scenario.** The incident, systems, and business pressures are fictional.

## Difficulty & Domain

- **Difficulty:** Expert · **Domain:** Multi-stage security incidents · **CLO:** CLO-11, CLO-14
- **Est. time:** 15 minutes · **Anchor:** L27 (Eradication, Recovery & Lessons Learned)

## Scenario

Three days after containment of a ransomware precursor (cs-082's
firm, next chapter), the business wants its 8 TB file share back.
Finance says every hour of downtime costs ≈ $18k. The eradication
team has not yet confirmed the persistence mechanism on the *source*
workstation was the only one. Restoring the share from last night's
backup takes 4 hours; rebuilding the server from golden image takes
2 days; imaging for forensics adds 6 hours to either path. The CIO
says "restore, we'll investigate in parallel." You must reconcile
recovery speed, evidence integrity, and re-infection risk.

## Stakeholders

- **CIO** — wants the share back; owns the business risk call.
- **Finance** — $18k/hour downtime.
- **IR lead (you)** — owns the "don't restore into a live attacker"
  verdict.
- **Backup team** — restore mechanics, 6-hour RPO, 24-hour RTO
  design point.
- **Users** — 400 staff waiting.

## Network Context

- FS01: file server, isolated since the event; image captured day 1.
- Source workstation W-77: reimaged day 1 (persistence mechanism
  identified; *no confirmation* it was unique).
- Backups: nightly offline, verified; last pre-incident backup 18:00
  day 0; nightly backups *continued* during isolation (server was
  network-contained, not powered off).
- Egress proxy: the staging domain remains blocked.

## Available Evidence

- EDR timeline: task + service + rename activity, all attributed to
  W-77's session; no other source visible in flow records.
- Persistence artifacts found: 1 scheduled task, 1 service (both on
  W-77, both suspended day 1).
- AD audit: no new accounts/GPOs since the event (cs-083's checks
  clean on this smaller estate).
- Backup integrity: nightly restore-verify reports PASS through the
  isolation window.

## Student Task

1. Choose a **recovery path**: (a) restore share to FS01 as-is,
   (b) rebuild FS01 from golden image + restore data, (c) rebuild +
   restore to *new* hostname/segment, (d) restore now + rebuild
   later. Justify with the three conflicting objectives (speed,
   evidence, re-infection risk) made explicit.
2. Define the **go/no-go criteria** that must be true before the
   restore executes (the L27 recovery board list, applied here).
3. Answer the **backup-during-incident question**: nightly backups
   ran during isolation — which backup generations are safe to keep,
   which must be quarantined, and why?
4. Propose the **compromise schedule** if the CIO overrules: what is
   the fastest defensible path, and what risk do you explicitly
   accept in writing?

## How to Approach This (Reasoning Scaffold)

- "Restore in parallel" is safe only if the *data* is clean and the
  *destination* is clean — separate those two questions.
- Backups taken *after* compromise but *during* containment may be
  clean (server was isolated) — but generation matters: the 18:00
  day-0 backup predates the event; later ones are suspect only if
  the server was reachable.
- Rebuilding into the same name/segment restores the attacker's
  knowledge of the environment along with the server.

## CLO Mapping

- **CLO-11** — Recovery-path decision under business pressure.
- **CLO-14** — Evidence preservation vs operational restore.

## Safety Notes

- Simulated; no ransomware artifacts.
