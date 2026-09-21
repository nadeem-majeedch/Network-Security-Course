---
case: cs-027
title: DMZ Design Review for a Public Web Service
difficulty: intermediate
domain: Network segmentation
module: 3
lecture-anchor: L09
clos: [CLO-3]
time-estimate: 12 min (5 min reasoning + 7 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-027-solution.md
---

# cs-027 — DMZ Design Review for a Public Web Service

> **Simulated scenario.** The agency, architecture, and findings are fictional.

## Difficulty & Domain

- **Difficulty:** Intermediate · **Domain:** Network segmentation · **CLO:** CLO-3
- **Est. time:** 12 minutes · **Anchor:** L09 (Defense in Depth & Network Segmentation)

## Scenario

A government agency is launching a public benefits portal. Before go-live,
you are the reviewing architect. The proposed design (below) has *real*
findings — your job is to rank them by exploitability × impact, and produce
the go/no-go conditions. "No findings" would be a failure of imagination;
"all findings are blockers" would be a failure of proportion.

## Stakeholders

- **Agency CISO** — owns go/no-go.
- **Delivery vendor** — built the design; defensive about rework.
- **Citizens** — PII in the application tier.
- **Auditors** — will compare design vs implemented config later.

## Network Context (proposed design)

```
Internet ──> Firewall A ──> [DMZ: web servers, 10.1.0.0/24]
                                │ (any port, any protocol)
                                ▼
                        [APP tier: 10.2.0.0/24] ──> [DB: 10.3.0.0/24]
                        (no firewall between app and DB)
Firewall B sits between DMZ and INTERNAL-CORP (10.0.0.0/16)
  rule: "allow 10.2.0.0/24 -> 10.0.0.0/16 any"  (for "patching and monitoring")
```

Additional facts: web servers are domain-joined to the corp AD; the DB
service account is a **domain account**; TLS terminates at the web tier;
monitoring agents use SMB to reach collectors inside corp; backups of the
app run from the corp backup server **pulling SMB from the DMZ**.

## Student Task

1. List the **five most significant findings** with (a) the attack path each
   enables, (b) exploitability (low/med/high), (c) blast radius.
2. Rank them and mark the **top 2 as go-live blockers** with your justification.
3. Rewrite the design in one paragraph: the minimum set of changes that
   converts the blockers into acceptable residuals *without* delaying
   go-live more than two weeks.

## How to Approach This (Reasoning Scaffold)

- Trace the kill chain an attacker gets *for free* from each finding —
  findings are interesting only as paths.
- Domain-joined DMZ + domain service account + any-to-corp rule = the classic
  DMZ-to-AD collapse. Follow the credentials.
- Proportionality: blockers are paths to PII or to corp-wide compromise —
  everything else is a finding with a date, not a veto.

## CLO Mapping

- **CLO-3** — DMZ architecture review and risk-ranked findings.

## Safety Notes

- Paper review of a fictional design; no testing against real agency systems.
