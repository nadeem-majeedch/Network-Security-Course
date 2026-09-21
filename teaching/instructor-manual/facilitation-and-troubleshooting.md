---
artifact-type: instructor-manual
status: complete
instructor-only: true
distribution: never-publish-to-students
---

# Discussion Facilitation & Lab Troubleshooting

## 1. Discussion facilitation playbook

### General method (all 32 lectures)
Every teaching plan carries 4–5 discussion questions with facilitation notes in
the speaker notes. The standard moves:

1. **Commit before reveal.** Ask for a written or thumbs position *before*
   discussing (the calibration demos in L24/L27 are built on this).
2. **Both-sides extraction.** For trade-off questions, extract the cost of the
   popular answer before accepting it — this is where senior judgment forms.
3. **Consequence chain.** "And then what happens?" — run the answer one step
   past comfort; the second-order effect is usually the teaching point.
4. **Silence tolerance.** Ten seconds of silence after a hard question is
   working time, not failure; resist answering your own question.
5. **On-record discipline.** Verdicts (severity calls, go/no-go, triage
   decisions) are recorded on the board with names — modeling the IR
   decision-record norm from L25/L26.

### High-stakes discussions (prepare for these)
- **L07 ethics gate** (who may scan whom): hold the authorization line firmly;
  curiosity is welcome, out-of-lab application is not. State the course policy
  and the institutional policy in one breath.
- **L26 executive-pressure case:** role-play with a volunteer; keep the
  debrief analytical, not personal.
- **L27 blameless resistance:** use systemic-language sentence stems ("the
  process allowed…"); the suppression counterexample does the persuasion.
- **L30 attribution honesty:** students want named villains; the evidence-
  language discipline ("infrastructure cluster consistent with…") is the
  professional skill being built.

## 2. Lab troubleshooting compendium

Per-lecture troubleshooting lives in speaker notes §Lab Troubleshooting. The
course-wide patterns and escalation rules:

### Universal first checks (in order)
1. **Pinned environment?** All lab images/tool versions are pinned on the lab
   sheets — version drift is the #1 cause of "works for the instructor".
2. **Wrong direction/scope?** Interface direction (ACLs), HOME_NET scope
   (rules), trust direction (switch ports) — direction errors dominate.
3. **State before logic?** VPN phase 1 before phase 2; TCP handshake before
   payload analysis; capture completeness before conclusions.

### Lab-range rules
- Students work **only** on assigned attack/lab targets (roster-enforced).
- Out-of-scope scanning or probing = session end + incident per course policy;
  the L01 rules sheet signed in week 1 is the reference.
- Instructor keeps a maintenance window weekly for range repairs — publish it;
  broken-lab frustration converts to missed assignments otherwise.

### Escalation rules (student → TA → instructor)
- **Student self-service (10 min):** pinned-command check, restart the lab VM,
  re-read the lab sheet's troubleshooting box.
- **TA triage (next 15 min):** the universal first checks above; log the fix
  in the range issue log (this log feeds lab-sheet improvements).
- **Instructor:** anything reproducible-but-unexplained, anything touching the
  range's shared infrastructure (routing, DHCP, storage), anything with a
  safety question attached.

### Data integrity in labs
- Graded artifacts (PCAPs, logs, scans) are **read-only** from the student's
  first command: analysis on copies, originals hashed at issue. This mirrors
  the L29 evidence discipline and is enforced in lab grading.

## 3. When demonstrations fail

- Every demo in the speaker notes carries a **fallback** (pre-captured output
  or recording). The rule: a failed live demo costs ≤ 3 minutes, then switch
  to fallback and continue — never debug live past the 3-minute mark.
- If the *range* is down at session start: every lecture has a dataset-only
  variant of its working block (the datasets are downloadable and the analysis
  tooling runs locally) — the mechanism lesson survives infrastructure.
