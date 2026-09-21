---
lab: Lab-14
status: complete
artifact-type: lab-answer-key
instructor-only: true
distribution: never-publish-to-students
---

# Answer Key — Lab-14 (IR Tabletop + Guided Threat Hunt)

## Tabletop script anchor ("Meridian returns")
Backstory: Lab-05's fix held 3 weeks. Inject sequence:
1. **T0:** DNS anomaly on backup server + "slow file server" ticket.
2. **T+25 min (inject 1 — "kill it now"):** executive orders immediate
   reimage of the backup server. Correct handling: options with risk
   (evidence destruction, re-compromise if credentials unrotated), decision
   on record by IC/risk owner — *not* silent compliance, not refusal theater.
3. **T+40 min (inject 2 — "is this public yet?"):** comms question; correct:
   facts known/unknown, legal gates external comms, single spokesperson.
4. **Close:** eradication order (credentials first: service accounts with
   external reach → domain-tier keys conceptually (KRBTGT rotation framing),
   then backup-server rebuild, then app tiers), go/no-go gates (persistence
   hunt clean, credentials rotated, monitoring heightened), lessons-learned.

## Eradication order reference (grading anchor)
1. Rotate adversary-facing credentials (service accounts w/ external reach).
2. Identity infrastructure before dependent services (DNS/DHCP before tiers).
3. Rebuild affected hosts from known-good images *after* credential rotation.
4. Restore with stepwise verification (dependency-ordered, tested).
Teams restoring "everything at once" re-compromise on paper — the debrief
demonstrates via H1/H2 evidence (a surviving scheduled task analog).

## Hunt expected results (grading anchor)
- **H1 (other beacons):** grouping DNS by src → only 10.20.0.102 shows the
  30 s cadence in-window → *confirmed in-window, inconclusive beyond it*.
- **H2 (scan host's reach):** flows by src=10.20.0.66 → only 10.20.30.10
  touched → confirmed in-window; verdict vocabulary graded.
- **Student H3+ (open):** grade the H→query→verdict chain, not the finding.
- Detection delta: expected "add" = backup-server DNS anomaly rule (from the
  scenario); "tune" = Lab-11 (b) threshold for 30 s cadence family.

## Lessons-learned quality bar
Blameless (systemic language), each finding → owned action + date +
verification at next exercise. "Humans blamed, no changes" fails; "the
process allowed unmonitored backup-server DNS" → action "ship resolver logs
to SIEM (owner: netops, date, verify: pipeline check)" passes.

## Analysis-question model answers (pointers)
1. Written plan vs improvised: the inject-1 handling — runbooks with
   preconditions (contact roster, pre-authorized options) beat memory under
   pressure (L25's clinic).
2. Process vs detection fixes: log-shipping = process+detection hybrid;
   ownership/verification is what makes either real.
3. Inconclusive follow-up: targeted capture window on the suspect path +
   revisit trigger (next anomaly); "found nothing" lacks the *scope statement*.
4. Metrics: time-to-tune (delta delivered) or coverage (new technique covered).
5. Gates vs theater: a gate that ran the persistence hunt *catches the
   re-compromise*; the gate that "checked the box" is theater — teams name
   which of theirs was which.

## Grading notes
- Scribe log completeness under the injects is the tabletop's core grade.
- Role pressure stays in-scenario; debrief separates performance from person.
- ✅ zeek/flow shapes executed at authoring; tabletop cards are print assets.

## Command status
✅ Analysis shapes verified; scenario/injects are instructor print assets.
