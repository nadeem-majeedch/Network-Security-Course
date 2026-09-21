---
case: cs-080
solution-for: modules/module-07-incident-response/case-studies/cs-080-roles-and-escalation-design-for-a-small-ir-team.md
difficulty: expert
module: 7
lecture-anchor: L25
clos: [CLO-11]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-080 Solution — IR Roles & Escalation (INSTRUCTOR ONLY)

## Model Solution

**Role matrix (4 internal + 3 external):**

| Role | Primary | Alternate | The 3 a.m. rule |
|---|---|---|---|
| **IC (Incident Commander)** — declares, sequences, owns decisions | SOC-1 | sysadmin | **"Whoever answers is IC until relieved."** Written on the on-call card; relief = explicit verbal handoff + scribe note. No title-waiting. |
| **Investigator** — evidence, scope, forensics | SOC-2 | network engineer | IC may hold simultaneously at Sev-1 (declare + investigate) — split only when help arrives |
| **Executor** — containment actions (isolate, block, patch) | network engineer | sysadmin | dual-control for *irreversible* actions (fleet wipe, mass cred reset) — IC + executor |
| **Scribe/Liaison** — timeline, comms relay to externals | (any, assigned by IC per shift) | — | the *first* scribe note ("T+0, what I know, who's IC") is the artifact that survives shift changes |
| **Legal (external)** | outside counsel (retainer) | GC | engaged at Sev-2+; privilege-route all written analysis through counsel once engaged |
| **Comms (external)** | comms lead (named) | deputy | drafted holding statements per class (cs-079's artifact) |
| **Exec sponsor** | CISO | COO | decision authority for business-impact calls (shut the line? pay? notify?) — *their* role is decisions, not direction |

**Escalation ladder (observable triggers):**

| Level | Trigger (observable) | Notified | Clock rule |
|---|---|---|---|
| **Sev-1** (event) | single-host indicator, no spread, no data movement | the 4 (next shift informed at handoff) | none |
| **Sev-2** (incident) | *any* of: multi-host spread, credential abuse confirmed, data staged (not moved), business function degraded | + IC formal, + legal informed (privilege), + exec sponsor *aware* | **T-72 assessment:** if exfil *cannot be excluded*, counsel starts the notification-clock evaluation memo — the clock debate is had *now*, not at hour 60 |
| **Sev-3** (major) | confirmed exfil of regulated data, ransomware-class event, regulator-notifiable condition met | + exec (engaged, not just aware), + comms lead activated, + regulator-clock: counsel owns countdown, daily memo | 72 h clock *starts on reasonable belief* — the memo records the belief's basis and time |
| **Sev-4** (crisis) | business-stopping (payments down), public exposure | + board, + insurer (policy #), + full comms posture | everything above, plus insurer's IR-panel activation |

*Ladder discipline:* levels escalate on **conditions**, never on mood;
and the *T-72 rule* is the compliance payload — the condition ("exfil
cannot be excluded") is deliberately conservative because the clock is
a regulator's, not ours.

**Exercise plan (2/year):**

| Drill | Tests | The failure it exposes |
|---|---|---|
| D1: "Declare it" (inject: ambiguous single-host malware w/ noise) | the declare rule; IC-until-relieved | title-waiting (the 3-hour stall reborn) — measured by *time-to-declaration* |
| D2: "External roles activate" (inject: confirmed exfil Friday 6 p.m.) | legal/comms/exec activation; T-72 memo | contact-card rot (numbers changed), exec improvisation |
| **D3: exec-in-the-room (the skipped one)** | exec sponsor *physically in the drill*, making the shutdown-the-line call under incomplete info | exposes exec role ambiguity *before* the real event: execs who've never decided under drill pressure either over-ride the IC or freeze — the drill makes their decision lane real |

## Alternative Solutions

- **Hire a dedicated IR lead:** the right move at this maturity (and
  the design should say so) — but the 3 a.m. rule exists because the
  *next* incident predates the hire.
- **MSSP/retainer-as-IR:** adds capacity; *their* escalation still
  needs your ladder (they can't declare your Sev-3 or start your
  regulator memo) — retainer plugs into the matrix, doesn't replace it.
- **Severity-by-asset-value only:** simpler but misses the *behavioral*
  triggers (spread, staging) that make early escalation possible —
  conditions beat classifications.

## Tradeoffs

- IC-until-relieved vs IC-by-title: claiming rule risks IC churn
  mid-incident — the scribe's handoff note and a *relief checklist*
  (what's decided, what's pending) make churn survivable.
- Conservative T-72 trigger (believe-exfil → start evaluation) vs false
  alarms: evaluation ≠ notification — the counsel memo separates
  "assessing" from "clock-running," which is exactly the nuance to
  rehearse in D2.
- 4-person dual-hatting vs role purity: small teams *must* dual-hat;
  the matrix's job is making the dual-hat explicit so handoffs
  unbundle it cleanly.

## Common Mistakes

- Role matrices without the claiming rule (3-hour stall reborn).
- Adjective severity ("serious incident") — mood escalations.
- External roles as *names in a drawer* — no drills, no holding
  statements, contact rot.
- Regulator clock treated as counsel's private math — the trigger
  condition must be written and drilled (D2).

## Instructor Prompts

- "Walk 3 a.m.: phone rings, SOC-1 answers — quote their first three
  actions under your design."
- "What does the T-72 memo contain at hour one — and why does writing
  it *early* protect the company?"
- "What did the exec-in-the-room drill expose last time you ran one?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Claiming-rule design; observable triggers; T-72 condition |
| Technical accuracy | 25% | Role/escalation mechanics; privilege routing |
| Alternatives considered | 20% | Hire/retainer tradeoffs |
| Communication | 15% | Matrix + ladder + drill table |

**Timing:** reveal at 5:00 + 10; the 3 a.m. walk is the debrief opener.

## CLO Mapping

- **CLO-11** — IR organizational design under staffing constraints.
