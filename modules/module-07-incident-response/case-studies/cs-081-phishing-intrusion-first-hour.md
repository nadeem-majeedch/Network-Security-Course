---
case: cs-081
title: Phishing-Driven Intrusion — First-Hour Triage
difficulty: expert
domain: Incident response
module: 7
lecture-anchor: L26
clos: [CLO-11, CLO-12]
time-estimate: 15 min (5 min reasoning + 10 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-081-solution.md
---

# cs-081 — Phishing-Driven Intrusion: First-Hour Triage

> **Simulated scenario.** The intrusion, telemetry, and timeline are fictional.

## Difficulty & Domain

- **Difficulty:** Expert · **Domain:** Incident response · **CLO:** CLO-11, CLO-12
- **Est. time:** 15 minutes · **Anchor:** L26 (Detection, Triage & Containment)

## Scenario

An accountant clicked a credential-phishing link 26 hours ago; the
phisher logged into webmail, then the corporate VPN (no MFA on VPN —
cs-019's pattern), and moved. The EDR raised its *first* high alert 10
minutes ago. You have the first-hour slot: triage evidence, sequence
containment (reversible-before-irreversible), and decide the one
judgment call that defines the hour.

## Stakeholders

- **The accountant** — victim; their host is evidence.
- **SOC (you)** — the hour is yours.
- **Finance systems** — payroll data likely accessed.
- **Legal** — notification exposure if PII moved.

## Network Context

- Telemetry: VPN logs (post-auth), proxy logs, EDR on the accountant's
  host, mail gateway logs, AD sign-in logs.
- No MFA on VPN; MFA on webmail (phisher used the *harvested session
  cookie*, bypassing MFA — the cs-019 lesson live).
- Payroll system: web app, AD-authed, accessible from VPN.

## Available Evidence

**26-hour reconstruction (from logs, now):**

| T (relative) | Event |
|---|---|
| −26:10 | accountant clicks link; phishing page harvests session cookie (webmail) |
| −26:05 | phisher reads webmail via cookie (proxy log: unusual UA from new IP) |
| −25:30 | phisher VPN login (harvested *password* from the same phish kit's credential page) from residential IP |
| −25:00–24:00 | internal scan from VPN session (fw allow-flow records: SMB sweep, 44818?, LDAP) |
| −23:50 | access to payroll web app (2 sessions, 40 min; exported 2 reports) |
| −18:00 | credential-dumping tool executed on accountant's host (**EDR alert — 10 min ago**) |
| −17:55 | EDR: scheduled-task creation on the host (persistence) |
| now | phisher's VPN session *still active*; accountant's host online |

## Student Task

1. **Triage in order**: name the three corroboration checks (EDR ↔
   proxy/VPN ↔ flow) that confirm the intrusion is real and *map the
   phisher's current position* (where are they *right now*?) — the
   cs-026 three-way corroboration discipline.
2. Sequence **containment** (reversible-before-irreversible): at least 5
   actions ordered, each labeled (reversible/irreversible) with what
   each severs — and the *one judgment call*: kill the live VPN session
   now (alerting the attacker) vs observe to map scope (data moving?).
   Take a position with the deciding evidence.
3. Answer the **legal question** in triage-ready form: what would you
   tell counsel *in the first hour* (exposure hypothesis + evidence
   state + what's pending) — not at day 3.

## How to Approach This (Reasoning Scaffold)

- "Where are they now" beats "what did they do": containment targets
  the *live* position first (active VPN session + dumping tool = the
  attacker is mid-operation).
- Reversibility discipline: session kills and port-blocks undo cheaply;
  account lockouts and host rebuilds cost the business — sequence by
  cost-of-being-wrong, not by instinct.
- The credential-dump alert is the escalation *event* — it converts
  "maybe phishing" into "keys to the kingdom moving."

## CLO Mapping

- **CLO-11** — First-hour triage and containment sequencing.
- **CLO-12** — Cross-source corroboration.

## Safety Notes

- Simulated incident; forensic handling framing only.
