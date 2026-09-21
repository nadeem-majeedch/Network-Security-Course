# cs-090 — The Disclosure Decision: Notify Now or Finish the Investigation?

> **Simulated scenario.** The incident, regulators, and timelines are fictional; no jurisdiction's law is quoted as authoritative.

## Difficulty & Domain

- **Difficulty:** Expert · **Domain:** Risk management (IR × legal × governance) · **CLO:** CLO-14, CLO-15
- **Est. time:** 20 minutes · **Anchor:** L27 (Eradication, Recovery & Lessons Learned)

## Scenario

Day 9 of an incident. The attacker had access to a customer-support
file store for 11 days before detection. Your forensics are 70%
done: 2 of 5 storage buckets confirmed accessed; the other 3 are
"suspect but unproven." The regulator's window is 72 hours from
*awareness* (day 0) — you are already past it, and the delay has a
reason (initial triage misjudged severity). Legal is split: notify
now with incomplete facts, or finish forensics (5 more days) and
notify accurately but late. You advise the disclosure decision.

## Stakeholders

- **DPO/Counsel** — owns the notification; needs your factual input.
- **Regulator** — will treat timeliness and accuracy separately.
- **Customers** — 40,000 individuals; want truth fast.
- **Board** — wants both accuracy *and* timeliness; someone will be
  disappointed.

## Network Context

- 5 buckets, customer-support data (tickets, some ID documents).
- Access pattern: attacker used a support console account; bucket-
  level access logs exist for all 5 (retention: 90 days).
- Forensics: 2 buckets fully reconstructed; 3 pending log parsing.
- The 72-hour clock: awareness = day 0 (EDR alert); triage
  misjudged it as low-severity until day 3; escalation then.

## Available Evidence

| Item | State |
|---|---|
| Buckets 1–2 | confirmed accessed (log-verified reads of ticket data) |
| Buckets 3–5 | suspect: attacker's account *could* reach them; no access-log evidence of reads yet |
| Attacker account | created day −11 via stolen creds; MFA-less console |
| Log parsing backlog | 5 days to complete buckets 3–5 |

## Student Task

1. Frame the **legal-clock reality**: is "still investigating" a
   defense for the missed window? What is notified *now* regardless:
   the incident, or only confirmed findings? (Reason from the
   principle — awareness triggers the clock; accuracy can follow in
   phases — not from quoted statutes.)
2. Choose a **notification strategy**: (a) single late-accurate notice,
   (b) immediate phased notice (incident + confirmed buckets now,
   updates as forensics complete), (c) wait 5 days. Take a position;
   name what each costs customers, regulator, and the board.
3. Draft the **day-9 phased notice skeleton** (what is stated as
   fact, what as unknown, what as next-update commitment) — 5 bullet
   points max.
4. Answer the **post-mortem question**: which internal failure
   (severity misjudgment) does the review fix, and how — one
   concrete control.

## How to Approach This (Reasoning Scaffold)

- The clock runs on *awareness*, not on *certainty*: waiting for
  perfect forensics converts a timeliness problem into a timeliness
  *and* accuracy problem.
- Phased notification is the standard resolution of the accuracy-
  timeliness tension: say what you know, label the unknowns,
  commit to updates.
- The 3 unproven buckets are *risk statements*, not facts — the
  notice's honesty depends on keeping that distinction intact.

## CLO Mapping

- **CLO-14** — Post-incident obligations and learning.
- **CLO-15** — Governance synthesis under real-world constraints.

## Safety Notes

- Simulated; principles-based, no legal advice.
