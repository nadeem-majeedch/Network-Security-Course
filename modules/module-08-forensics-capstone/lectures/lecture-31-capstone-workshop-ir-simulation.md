---
lecture: L31
title: Capstone Workshop & IR Simulation
module: 8
week: 16
hours: 2
clos: [CLO-11, CLO-15]
difficulty: expert
status: complete
artifact-type: teaching-plan
---

# L31 — Capstone Workshop & IR Simulation

## 1. Overview & Prerequisites

- **Prerequisites:** L30 (reporting standard), L27 (IR execution — the simulation reuses its authority matrix and checklists), plus the full architecture/detection stack (L09–L23). Capstone draft was due W15.
- **Position:** the capstone's working session: design reviews sharpen each team's architecture, then the live IR simulation stress-tests their monitoring and response under time pressure. Everything today rehearses L32's defense (CLO-15).
- **Faculty prep:** schedule 4 design-review slots (10 min each) with a review panel (instructor + 2 peers per slot); arm the IR simulation range (injects per capstone scenario pack); prepare the peer-review rubric cards.
- **Common misconceptions:** "the capstone is a big lab report"; "design review = show the diagram"; "the IR simulation is graded on winning."

## 2. Learning Objectives

By the end of this lecture, students can:

1. Present and defend a network security architecture against structured peer review: trust zones, policy table, detection coverage, and trade-offs (CLO-3/15 synthesis) (Evaluate/Create).
2. Critique another team's design using a rubric: requirement coverage, least privilege, failure modes, detection gaps (Evaluate).
3. Execute a live IR simulation: triage → scope → contain → report under time constraints, using their own team's monitoring design (CLO-11) (Apply/Create).
4. Integrate review and simulation feedback into the final capstone deliverable (due L32) (Create).
5. Demonstrate the briefing discipline from L30 under pressure (CLO-15) (Create).

## 3. Detailed Concepts

### 3.1 The capstone deliverable set (recap + today's path)
- Deliverables: (1) architecture & policy document (zones, rulebases, egress, cloud segment where applicable); (2) monitoring & detection design (pipeline, sensor placement, ≥ 2 custom detections, hunt log — L21–L23 artifacts); (3) IR playbook set (L25 format); (4) forensic/reporting artifact from the simulation; (5) the defense briefing (L30/§3.5 standard).
- Today = review + simulation; L32 = defense + final integration. The rubric maps each deliverable to CLOs (requirements §5).

### 3.2 Design review method (the peer-panel format)
- Slot structure (10 min): 4-min presentation (architecture → policy → detection coverage), 4-min structured questions (panel uses rubric cards: requirement coverage / least privilege / failure modes / detection gaps / operational realism), 2-min action items.
- The question bank (what panels should probe): "what does a compromised DMZ host reach?" (L09), "show your first-match shadowing audit" (L11), "which ATT&CK techniques have no detection?" (L22/L28), "what happens when the IdP is down?" (L16/L25), "your egress design vs the exfil scenario?" (L12/L20).
- Feedback discipline: findings as questions with evidence ("your guest VLAN has no egress policy — what stops tunneling?"), action items with owners.

### 3.3 The IR simulation (live, time-boxed)
- Setup: each team's capstone network hosts a planted incident (beacon + credential reuse + small exfil attempt — calibrated to their own monitoring design; teams that built detection *see more*).
- The run (30 min): inject 1 (alert) → team triages per L26 method → inject 2 (scope-expanding evidence) → containment decision council (authority matrix from their playbook) → inject 3 (exec pressure: "just turn it off") → incident-state doc produced live (L26/§3.5 standard).
- Grading lens: process quality (citations, trade-off reasoning, authority use), not "winning" — a team that correctly documents what they *cannot* know scores well.
- The simulation is also the source of the team's forensic artifact (deliverable 4): their incident-state doc + L30-style report.

### 3.4 Feedback integration loop
- From reviews: architecture/policy changes go into the final document with a change log (each change justified — the governance habit from docs-meta applied to capstones).
- From simulation: detection gaps → new rules (L22) or data requests (L21 coverage note); playbook gaps → revisions (L25 anatomy checklist).
- Integration checkpoint: end-of-session 5-minute team huddle listing their top-3 changes before L32.

## 4. Teaching Sequence (120 Minutes)

| Time | Segment | Instructor moves |
|---|---|---|
| 0–10 | Setup: rubric cards + review slots | Panel assignments; simulation ground rules (no touching other teams' segments) |
| 10–55 | **Design reviews** (4 × 10 min + transition) | Panel runs the question bank; action items logged per team |
| 55–65 | Break + simulation arming | Instructor arms incidents calibrated to each team's design |
| 65–100 | **IR simulation** (each team 20-min window, staggered) | Injects fire; teams run triage→scope→contain→document; instructor observes with rubric |
| 100–110 | Integration huddle | Teams list top-3 changes from review + simulation |
| 110–120 | Wrap + formative | Exit ticket; L32 defense logistics (schedule, panel, timing); Final-exam window reminder |

## 5. Technical Examples

```
# Review slot question bank (panel rubric card, condensed):
#  R1 Requirement coverage:  map each stated requirement -> artifact section
#  R2 Least privilege:       sample 3 rules -> justify; find one any/any
#  R3 Failure modes:         IdP down / NAT-GW failure / scanner outage
#  R4 Detection gaps:        pick 2 ATT&CK tactics -> which detections cover them?
#  R5 Operational realism:   who is paged? what's the exception process?

# Simulation inject 1 (calibrated to team's design):
#   Suricata sid 1000001 fires on WEB-03 -> cdn-updates[.]xyz (yes, the course's
#   recurring fictional threat — continuity is the point).
# Team's expected path: L26 triage -> scope (their flow collector!) -> quarantine
#   VLAN per their playbook -> incident-state doc (L26 template) within window.

# Integration change-log entry (deliverable-1 appendix):
#   CHANGE-04 | Added egress allow-list to GUEST zone | Source: review R2 finding |
#   Justification: exfil-path closure | Verified: retest matrix updated.
```
Expected teaching points: reviews interrogate *artifacts*, not diagrams; the simulation's injects come from the team's own design (their detection quality determines their visibility); change-log discipline makes the final document defensible.

## 6. Discussion Questions

1. Why is "we saw nothing during the simulation" a rubric finding for the *design*, not the team's luck?
2. Your panel found a shadowed rule in your production-design rulebase. What does that say about your audit process (L11) — and what's the fix beyond the fix?
3. During the exec-pressure inject, your authority matrix said "no." Rehearse the 30-second answer.
4. Which deliverable benefited most from today — and which needs the most work before L32?
5. How would you run this review format in a real security organization (name the meeting it replaces)?

## 7. Student Activity

**Design review panel + IR simulation (90 min combined):** each team presents once, reviews twice (as panel members), and runs its simulation window. Deliverables today: review action-item log (given + received), simulation incident-state doc, and the integration change-log. All three feed the L32 defense directly.

## 8. Problem-Solving Case

**Primary case — cs-098 "Capstone network design defense prep" (expert):**
Preparation case: using your team's review action items, produce the "defense pack": (a) the change-log with justifications, (b) answers to the ten hardest panel questions (written, cited to artifacts), (c) the 8-minute defense outline (what you show, in what order, and the one trade-off you volunteer before being asked), and (d) the dry-run plan (who presents what, who fields which question class).
**Linked cases:** cs-099 (IR simulation inject handling under time pressure).
*(Model solutions: instructor answer-key set, Module 8.)*

## 9. Formative Assessment

1. Name the four review rubric dimensions beyond requirement coverage.
2. In the simulation, which deliverable does the incident-state doc become?
3. What makes an inject "calibrated to the team's design" — and why does that matter for fairness?
4. Give one change-log entry format field and why it exists.
5. What's the difference between defending a design and defending a diagram?
*(Answer key: instructor set, Module 8.)*

## 10. Summary & Key Takeaways

- Review + simulation + integration = the capstone's quality loop; artifacts, not opinions, carry the argument.
- The IR simulation grades process under pressure — citations, trade-offs, and honest unknowns win.
- Everything converges: the course's own formats (playbooks, triage notes, hunt logs, reports) are the capstone's building blocks.

## 11. References

- Course-internal formats: L25 playbook anatomy; L26 triage/incident-state templates; L30 report structure (the capstone's house style).
- NIST SP 800-61 — simulation alignment to lifecycle phases.
- OWASP/CIS — review rubric anchors (requirement traceability, benchmark coverage).
- MITRE ATT&CK Navigator — detection-coverage presentation for the defense.

## 12. CLO Mapping

| CLO | Where in this lecture | Assessed via |
|---|---|---|
| CLO-11 | §3.3 simulation execution (triage→contain→document) | Capstone IR exercise, Final |
| CLO-15 | §3.2 review presentation + §3.5 briefing under pressure | Capstone defense (L32), Assignment 6 (feedback) |
