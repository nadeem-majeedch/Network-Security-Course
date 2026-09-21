---
lab: Lab-06
status: complete
artifact-type: lab-answer-key
instructor-only: true
distribution: never-publish-to-students
---

# Answer Key — Lab-06 (Firewall Rulebase Build & ACL Audit)

## Build reference (≥8 rules)
Aliases first; rules ordered specific→general with intent+author descriptions;
explicit log on the final deny; ICMP handled by its own named rule (not
implicit); egress via proxy object where the range provides one. Verification
path must map *each rule to a test connection* (curl exit 7/28 distinctions
refused-vs-dropped; ping for the ICMP rule).

## Broken-rulebase audit answer table (the graded core)
| Rule # (audit config) | Problem class | Evidence | Fix |
|---|---|---|---|
| 5 | any/any permit mid-table | shadows 12/18; hits enormous | delete or scope to admin subnet |
| 9 | shadowed specific permit | hit counter 0 while rule 5 catches all | reorder above 5 or delete |
| 12 | orphaned permit (port 8080) | hits=0 since creation; no service owner | confirm-with-owner → delete |
| 15 | direction error (out on LAN) | intended path dead; counter 0 | move to in/interface pair |
| 17 | unlogged deny | silent blackholes, no diagnostics | add log |
| 21 | any/any on egress | post-incident finding | replace with proxy allow-list |

(Team sheets carry the exact rule IDs from the supplied export — key the
numbers to the export version pinned that semester; the *classes* are stable.)

## Analysis-question model answers
1. **Rot:** first-match + append-only growth → broad permits accrete above
   specifics; nobody deletes (no owner/hits data) → shadowing accumulates;
   audits need hit-count data + intent fields to fight it.
2. **Statefulness:** return traffic auto-matched on the state table; stateless
   router ACLs (Lab-05's OT/DMZ edges if implemented there) still need
   established/return handling — the concept students must not blur.
3. **Orphan deletion is a decision:** check creation date, owner intent, season
   patterns (month-end jobs), then delete in a change window with rollback —
   not reflexive.
4. **Unlogged permit vs deny:** permit = undetected misuse path; deny =
   undiagnosed outage; commit either way with reasoning — the *reasoning* is
   graded, not the side.
5. **Change record:** maps to L11's intent/test/rollback; the snapshot is the
   rollback — students who skipped it and locked themselves out report it
   honestly (reward the honesty; it's the incident-report habit).

## Grading notes
- Screenshots must show *counters*, not just rule tables — first-match claims
  need empirical counters.
- Lockout self-reports: full safety marks if reported in the change record;
  silently reverted = loss of marks (integrity of the record).
- Common build errors: direction/interface confusion (see §4 drill), alias
  typos, ICMP forgotten.

## Command status
⚠️ pfSense GUI steps are range steps (not executable in authoring env); the
curl exit-code semantics (7 refused / 28 timeout) are POSIX-documented shapes.
✅ Nothing here depends on the generated datasets.
