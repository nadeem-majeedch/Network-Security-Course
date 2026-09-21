---
case: cs-099
title: IR Simulation — Injects Under Time Pressure (Solution)
difficulty: expert
module: 8
lecture-anchor: L31
clos: [CLO-11, CLO-15]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-099 — Solution: Injects Under Time Pressure

> **INSTRUCTOR ONLY.** Model solution for cs-099.

## Model Solution

### Inject-by-inject decisions

**Inject 1 (0:10 — mass rename on FS-mirror-01):**
- **Decision:** open the incident; EDR isolate FS-mirror-01.
- **Corroboration:** single-source (EDR), acting on *error
  asymmetry* (cs-082): act-wrong costs a mirror reboot; wait-wrong
  costs the share. Basis stated, not assumed.
- **Reversibility:** Reversible (network containment, host stays
  up). **Fallback:** if false positive, un-isolate and file the
  tuning task.

**Inject 2 (0:30 — staging egress, same host):**
- **Decision:** containment stands; block domain at proxy+DNS;
  preserve artifacts (suspend, don't delete).
- **Corroboration:** two-source now (EDR + SIEM/proxy) — the
  three-way rule is satisfied for "real incident"; *not yet* for
  "ransomware pre-encryption" specifically.
- **Reversibility:** all reversible. **Fallback:** domain block
  false-positives → unblock with change record.

**Inject 3 (0:50 — VP demands customer-data answer):**
- **Decision:** no data-loss claim, no all-clear — the facts don't
  support either.
- **Line (exact words):** *"We contained a suspected ransomware
  event on one file server 40 minutes ago. No customer data
  systems are involved in what we've seen so far, but the review
  isn't finished — I won't guess. You can tell the customer: we
  detected it fast, contained it, and will confirm scope by [T+
  2h]."*
- **Corroboration basis:** absence of evidence on customer systems
  (no SIEM hits) is *not* clearance — the line keeps "so far"
  attached.
- **Reversibility:** communication is irreversible once said —
  which is why the line contains no invented certainty.
- **Fallback:** if staging is later traced into customer data,
  the update goes to the same VP *before* the customer — the
  commitment made the first update obligation explicit.

**Inject 4 (1:10 — svc_ops interactive on DB-mirror-02):**
- **Decision:** contain DB-mirror-02; disable svc_ops interactive
  use estate-wide (service accounts never log in interactively);
  heighten monitoring on all other service accounts.
- **Corroboration:** two-source (SIEM identity + the pattern's
  deviation from baseline); the *estate-wide* disable is
  proportionate to a credential whose blast radius is estate-wide
  (cs-088's account-vs-host logic).
- **Reversibility:** reversible (account restrictions; sessions
  killable). **Fallback:** if a legitimate admin used svc_ops
  interactively (break-glass), the change record shows it — and
  break-glass misuse is itself a finding.

**Inject 5 (1:30 — legal: when does the clock run?):**
- **Decision:** state the trigger framework, not a date — and
  escalate to counsel as the owner.
- **Line (exact words):** *"Awareness started when the first
  credible alert fired — [0:10 today]. Whether this meets the
  notification bar is a legal determination, not mine: I've asked
  counsel to assess now, and the timeline I give them will show
  detection at 0:10, containment at 0:35, and the customer-data
  review completing by [T+2h]."*
- **Corroboration basis:** the awareness timestamp is
  corroborated (EDR alert + SIEM entry); the *bar* is
  counsel's call (cs-090's separation of technical and legal
  determinations).
- **Reversibility:** the framework statement is safe; a specific
  "we notify at X" guess is not.

### Exercise-level question: worst decision-quality tradeoff

**Inject 3.** The VP inject forces communication *before*
corroboration can mature — the only inject where the required
output (an executive statement) is irreversible and the evidence
base is deliberately incomplete. It reveals the estate's real
preparedness gap: **there is no pre-approved holding statement**.
Everything else had a technical playbook; this had only discipline.
Fix (cs-086 conversion): a pre-approved incident holding-statement
template, owned by comms, with the "facts + labeled unknowns +
commitment" structure — tabletop-verified next quarter.

## Alternative Solutions

- **Inject 1: wait one cycle for corroboration** — defensible
  only if the share were non-production; with production data and
  the asymmetry stated, isolation is the better-scored decision.
- **Inject 4: contain only DB-mirror-02** (not estate-wide
  disable): narrower blast radius management; rejected because
  svc_ops's estate-wide credential means the attacker holds the
  key regardless — the cs-088 principle (contain the credential,
  not just the host).

## Tradeoffs

- Speed vs corroboration maturity: the exercise rewards *stating
  the basis* over waiting for it — the structure is the skill.
- Executive candor vs reassurance: "I won't guess" reads badly in
  the moment and ages best in the debrief.

## Common Mistakes

- Treating inject 3 as a technical question (it's a comms
  decision with a technical input).
- Estate-wide account action skipped for "wait and see" — the
  credential is the asset, not the host.
- Guessing at the legal clock (a specific wrong date is worse
  than a correct framework).
- Silent assumptions under time pressure — scored as none.

## Instructor Prompts

- "Which decision, if it proved wrong tomorrow, would you defend
  unchanged — and why is the written basis what saves it?"
- "What would a *pre-approved* holding statement have changed in
  inject 3?"
- "Why is the estate-wide svc_ops disable proportionate rather
  than panic?"

## Rubric (10 pts)

| Criterion | Pts |
|---|---|
| 5 decisions with corroboration basis stated | 3 |
| Reversibility labels + fallbacks per decision | 2 |
| Communication lines exact-worded (no invented certainty) | 3 |
| Worst-tradeoff analysis + preparedness insight | 2 |

## Safety Notes

- Simulated exercise; synthetic telemetry; no production systems.
