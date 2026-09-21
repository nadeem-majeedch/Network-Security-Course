---
case: cs-079
solution-for: modules/module-07-incident-response/case-studies/cs-079-ransomware-playbook-gap-analysis.md
difficulty: expert
module: 7
lecture-anchor: L25
clos: [CLO-11]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-079 Solution — Ransomware Playbook Gaps (INSTRUCTOR ONLY)

## Model Solution

**Gap table:**

| Inject | Playbook statement | Execution requirement | Missing element | Fix (concrete artifact) |
|---|---|---|---|---|
| I1 | "Isolate infected systems" | per-host isolation *procedure* covering EDR and non-EDR | switch-port shutdown runbook for the legacy 20%; per-host isolation decision criteria | **Runbook §4.2**: "EDR-covered → console isolate; non-EDR → switch port list (per-site port maps, printed) + port-disable; verify with flow monitor" |
| I2 | (silence) | *dependency mapping*: AD-authed response tools vs AD containment | break-glass accounts; OOB comms; decision matrix for AD-vs-tool sequencing | **Break-glass kit**: 2 local-admin EDR-console accounts (offline-stored, MFA-token), OOB channel (pre-paid phones/mesh app), decision matrix: "AD disablement ONLY after EDR isolation capability confirmed via break-glass auth" |
| I3 | "Restore from backup" | *tested, located, inventoried* restore path | tape inventory (which, where), vendor contacts, drive state, **a tested procedure** | **Restore card**: quarterly *partial* restore test (one file set from one tape), tape registry (IDs, offsite vendor + contract #, rotation), drive maintenance record; tabletop I3 re-run after first live test |
| I4 | "Contact communications" | *named humans + pre-approved language* | comms lead name/deputy, holding statement, legal escalation path, insurer notification duty (policy #) | **Contact card** (laminated, printed): comms lead + deputy, outside counsel, insurer + policy #, regulator duty summary; **pre-approved holding statement** reviewed by counsel *now*, not at T+4h |

**The sequencing dilemma (I2) as a class:** the case's structural lesson
is the **response-tool dependency map** — every capability that
authenticates to the resource under attack (EDR console, backup
console, comms, even the playbook itself if it lives on the wiki behind
SSO) is a single point of failure at exactly the wrong moment. Standard
resolutions: (a) **break-glass identities** — local, non-AD, MFA-token,
offline-stored, alarmed on use; (b) **OOB comms** — the response must
not depend on the compromised estate's email/Teams (this org's Teams
and AD share fate — the inject's hidden trap); (c) **dependency order
decided *now***: the matrix ("if AD is being attacked, isolate FIRST
via break-glass EDR auth, THEN discuss AD disablement") removes the
T+30m argument from the incident.

**Fixes ranked by first-hour value:**

| Rank | Fix | Minutes saved at T+0–60 |
|---|---|---|
| 1 | Break-glass kit + dependency matrix (I2-class) | without it, every other tool may be unreachable *at once* — this is the meta-fix |
| 2 | Isolation runbook + printed port maps (I1) | the literal first verb of the incident; ambiguity here burns the opening minutes |
| 3 | Contact card + holding statement (I4) | comms chaos consumes senior attention mid-technical-work |
| 4 | Restore card + first quarterly test (I3) | not needed until recovery hours — but the *test* is a months-lead item; start it this week |

**Retest plan:** re-run the tabletop with the same injects after fixes
ship — each inject now *proves* one fix (I1→runbook used unprompted;
I2→break-glass exercised; I3→partial restore test referenced; I4→
statement drafted in <15 min). The retest is the evidence that converts
the gap report into a closed compliance story.

## Alternative Solutions

- **Buy IR retainer + IR platform:** valuable (forensics capacity,
  playbooks-as-code) but the tabletop failures are *internal decision
  and dependency* gaps no vendor attendance fixes at T+30m — buy it,
  and still fix the kit.
- **Move everything to EDR (deprecate legacy 20%):** correct long-term;
  the port-map runbook is still required until that project lands —
  roadmap + bridge, not either/or.
- **Cloud-offsite backups only (drop tapes):** ransomware-targets-cloud
  risk needs *immutability/offline* anyway — the tape path (tested!) or
  immutable-object tier are the honest choices; dropping untested
  restore *paths* without a replacement is the failure mode.

## Tradeoffs

- Break-glass security vs availability: two accounts, alarmed, offline
  MFA — the controls that make break-glass safe *are* the design;
  unmonitored break-glass is the backdoor class.
- Printed artifacts (port maps, contact cards) vs digital-only: the
  incident may take digital access away — print the two cards, version
  them, re-print quarterly.
- Tabletop frequency vs fatigue: two full runs/year + inject-of-the-
  month at staff meetings keeps verbs sharp without theater.

## Common Mistakes

- Rewriting the playbook to be *longer* (phases with more adjectives) —
  the fix is verbs, maps, and cards, not prose.
- Fixing I3 by "testing restore" someday (the test is the fix; schedule
  it).
- Break-glass without alarms/scoping (backdoor creation).
- No retest (gap reports without re-evidence decay back to prose).

## Instructor Prompts

- "Which fix makes the other three *usable* under attack?"
- "What does the dependency map catch beyond EDR/AD?"
- "Why is the holding statement written *before* the incident a
  security control?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Verbs-not-phases framing; dependency-class insight |
| Technical accuracy | 25% | Break-glass/OOB/restore-test mechanics |
| Alternatives considered | 20% | Retainer/EDR-everywhere tradeoffs |
| Communication | 15% | Gap table + ranked fixes + retest |

**Timing:** reveal at 5:00 + 10; "phases vs verbs" is the opening line.

## CLO Mapping

- **CLO-11** — IR-preparation engineering and playbook hardening.
