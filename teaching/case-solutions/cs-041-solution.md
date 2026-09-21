---
case: cs-041
solution-for: modules/module-04-crypto-protocols/case-studies/cs-041-key-management-lapse-rca.md
difficulty: intermediate
module: 4
lecture-anchor: L13
clos: [CLO-5]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-041 Solution — Key-Management Lapse RCA (INSTRUCTOR ONLY)

## Model Solution

**Root-cause chain — three failure classes:**

| Failure class | Where it shows | Missing control |
|---|---|---|
| **1. Secret without a system of record** (KEK lives in a file + wiki, not a KMS) | events 1, 3, 5 | KMS-managed KEK with API-only access; secrets are *services*, not files |
| **2. Lifecycle gaps at decommission/migration** (no revocation, no inventory of copies) | events 2, 3 | key-material inventory + decommission checklist incl. cryptographic secrets; "copies exist" tracked |
| **3. No restore *testing*** (the process that would have caught every earlier step) | whole cascade | scheduled restore drills from cold tier — the drill would have surfaced the KEK's fragility *before* the loss |

(Single-cause answers — "the cleanup job deleted it" — miss that three
independent controls were absent; any one would have saved the archives.)

**Compliance answer — what was actually lost:**

- **Availability: lost, material.** Last month's cold-tier archives are
  undecryptable (KEK unrecoverable): a real, reportable backup-coverage gap.
- **Confidentiality: *probably* not breached — but unprovable, and that's
  the finding.** Exposure candidates: (a) the wiki copy — the KEK existed
  in a *wiki* for 14 months, visible to whoever had wiki access (insider/
  account-compromise exposure window); (b) the old host — wiped "later,"
  so a window where the disk (and KEK) existed outside control; (c) no
  evidence of external access in the cascade, so the honest statement is:
  *"no evidence of exposure; two uncontrolled copies existed for months;
  exposure cannot be excluded"* — and the audit answer changes from
  "encrypted backups" to "encrypted backups with a key-custody incident,
  investigations attached."

**Minimum viable key management (5-person team):**

1. **KMS/HSM-backed KEKs** — key material never leaves the KMS; apps call
   wrap/unwrap APIs (no file copies, ever).
2. **Envelope encryption** — per-archive DEKs wrapped by KEK; KEK rotation
   = re-wrap DEKs, archives untouched (this kills the "rotate what?"
   confusion from event 4).
3. **Escrow with dual control** — KMS provider escrow / second-region
   replicated key with 2-person access for break-glass.
4. **Break-glass procedure** — documented, tested, alarmed (any
   break-glass use pages two people).
5. **Restore drills** — monthly: restore one archive *from cold tier* end-
   to-end; drill failure = sev-2, not a note.
6. **Copy inventory** — one page listing every place key material has ever
   existed; each entry has an owner and a destruction date.

**The one practice that prevents the loss outright: scheduled restore
drills.** Everything else reduces risk; the drill *detects* the single-copy
fragility while it's still recoverable — it converts silent key rot into a
loud operational failure months early. (KMS adoption is the structural
prevent; the drill is the detection that saves you when structure lags.)

## Alternative Solutions

- **"Use the KMS" as the whole answer:** necessary but incomplete — events
  3–4 show *process* rot that a KMS alone doesn't catch (drills + inventory
  remain).
- **Cloud-managed backup service end-to-end:** vendors the problem away
  (and the key custody with it); legitimate for this team size — but the
  restore-drill practice survives any vendor choice.
- **Manual rotation runbook instead of KMS re-wrap:** adds exactly the kind
  of human-key-handling that caused events 2–4.

## Tradeoffs

- KMS cost/complexity vs file-based simplicity for a 5-person team: the
  event *is* the cost of file-based; KMS spend is the cheaper risk.
- Escrow's dual-control friction vs single-admin speed: escrow exists for
  the day speed doesn't matter (disaster).
- Drill frequency (monthly) vs storage egress cost: drill one archive, not
  the library — proportionality keeps the practice alive.

## Common Mistakes

- Root cause = the cleanup job (single-cause RCA fails the exercise).
- "Confidentiality unaffected" without naming the wiki/old-host windows.
- MVP design without restore drills (the prevent-detect pairing broken).
- No break-glass path — which turns the *next* incident into this one.

## Instructor Prompts

- "Point at the exact event where the archives became unrecoverable — and
  the earlier event where it became *inevitable*."
- "What would your audit answer have been one week ago?"
- "Why is 'we gitignored it' not a control?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Three-class RCA; C-vs-A loss separation |
| Technical accuracy | 25% | Envelope/re-wrap/escrow mechanics correct |
| Alternatives considered | 20% | KMS-only/vendor options weighed |
| Communication | 15% | Chain table + 6-bullet MVP |

**Timing:** reveal at 5:00 + 2; the "inevitable vs unrecoverable" prompt
teaches RCA depth.

## CLO Mapping

- **CLO-5** — Key-lifecycle failures and minimal-controls design.
