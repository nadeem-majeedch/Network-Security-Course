# cs-080 — Roles and Escalation Design for a Small IR Team

> **Simulated scenario.** The team, incident classes, and escalation drills are fictional.

## Difficulty & Domain

- **Difficulty:** Expert · **Domain:** Incident response · **CLO:** CLO-11
- **Est. time:** 15 minutes · **Anchor:** L25 (IR Lifecycle & Preparation)

## Scenario

A 1,000-employee fintech has **4 IR-capable people** (2 SOC analysts, 1
sysadmin, 1 network engineer) and no formal role/escalation design. A
minor incident last quarter stalled 3 hours because "everyone waited to
see who declared it." Design the **role matrix + escalation ladder** for
a 4-person team: who declares, who leads, who executes, who talks —
including the roles *nobody on the team holds* (legal, comms, exec) and
how those get exercised without hiring.

## Stakeholders

- **The 4** — already over-extended; roles must be lightweight.
- **CISO** — owns the design; needs 3-a.m. usability.
- **Exec team** — will be pulled in; needs their role defined so they
  don't improvise.
- **Regulator** — notification clocks make escalation latency a
  *compliance* number.

## Network Context

- Incident classes to design for: (a) malware on one host, (b) creds
  compromise + lateral movement, (c) ransomware-class event, (d) data
  exposure (exfil confirmed), (e) vendor/cloud incident affecting them.
- 24/7 coverage: none (business hours team; on-call = the 4, rotating).
- Regulator clock: 72 h notification for qualifying breaches.

## Student Task

1. Design the **role matrix**: the minimal IR role set (declare/investi-
   gate/contain/comms-liaison/scribe) mapped to the 4 people + named
   external roles (legal, comms, exec sponsor) — with the
   *primary/alternate* pattern and the rule that makes it work at 3
   a.m. (whoever answers is IC until relieved — say it explicitly).
2. Build the **escalation ladder**: severity levels (define 3–4 levels
   with *observable triggers*, not adjectives), who's notified at each,
   and the regulator-clock rule (T-72 countdown starts when *what*
   condition is met?).
3. Design the **exercise plan** (2 drills/year) that tests the ladder:
   which injects exercise "declare," which exercise "external-role
   activation," and the one drill that most orgs skip (the exec-in-the-
   room drill) — with the failure it exposes.

## How to Approach This (Reasoning Scaffold)

- Small teams need *role-claiming rules*, not org charts: "IC until
  relieved" plus a written handoff beats an unstaffed title.
- Severity levels must key on *observable conditions* (spread, data
  movement, business function) — adjective-severity ("bad") escalates
  by mood.
- The regulator clock is an *external* constraint: the condition that
  starts it (reasonable belief of qualifying breach) must be written
  down or the 72 h burns in debate.

## CLO Mapping

- **CLO-11** — IR organizational design under staffing constraints.

## Safety Notes

- Design exercise; tabletop framing.
