# L31 — Capstone Workshop & IR Simulation

## 1. Learning Objectives

By the end of this session you can: (1) present and defend your capstone architecture against structured peer review; (2) critique another team's design with a rubric (requirement coverage, least privilege, failure modes, detection gaps); (3) execute a live IR simulation — triage → scope → contain → document — using *your own* monitoring design; (4) integrate review and simulation feedback into the final deliverable with a change log; (5) brief under pressure using the L30 discipline.

## 2. Key Definitions

| Term | Definition |
|---|---|
| Design review | Structured interrogation of artifacts against a rubric — not a demo |
| Rubric dimensions | Requirement coverage / least privilege / failure modes / detection gaps / operational realism |
| Calibrated inject | Simulation incident shaped to what *your* design should detect |
| Decision log | Timestamped decisions with rationale and authority citations (L25) |
| Change log | Recorded deliverable changes: what, why (finding), verification |
| Defense pack | Prepared answers to the hardest panel questions, artifact-cited |
| Integration loop | Review findings + simulation gaps → deliverable revisions → re-verification |

## 3. Detailed Explanations

### 3.1 The capstone deliverable set (recap)
(1) **Architecture & policy document** — zones, rulebases, egress, cloud segment; (2) **monitoring & detection design** — pipeline, placement, ≥2 custom detections, hunt log (L21–L23); (3) **IR playbook set** (L25 format); (4) **forensic/reporting artifact** from today's simulation (L30 format); (5) **the defense briefing**. The rubric maps each to CLOs (requirements §5). Today: review + simulation; L32: defense + final.

### 3.2 Design review method (the peer-panel format)
Slot structure (10 min): 4-min presentation (architecture → policy → detection coverage), 4-min structured questions from the rubric, 2-min action items. The question bank: *"What does a compromised DMZ host reach?"* (L09); *"Show your shadowing audit"* (L11); *"Which ATT&CK techniques have no detection?"* (L22/L28); *"What happens when the IdP is down?"* (L16/L25); *"Your egress design vs the exfil scenario?"* (L12/L20). Feedback discipline: findings as questions with evidence ("your guest VLAN has no egress policy — what stops tunneling?"), action items with owners.

### 3.3 The IR simulation (live, time-boxed)
Each team's capstone network hosts a planted incident — **calibrated to their design** (beacon + credential reuse + small exfil attempt): teams whose monitoring is good *see more*. The run (~20 min per team): inject 1 (alert) → L26 triage → inject 2 (scope-expanding evidence) → containment council per their authority matrix → inject 3 (exec pressure: "just turn it off") → incident-state doc produced live (L26/§3.5 standard). **Grading lens:** process quality — citations, trade-off reasoning, authority use, honest unknowns — *not* "winning." A team that correctly documents what it cannot know scores well.

### 3.4 The integration loop
Review findings → architecture/policy changes, each justified in a change log (governance habit from the repo's own docs-meta, applied to capstones). Simulation gaps → new detections (L22) or data requests (L21 coverage notes); playbook gaps → revisions (L25 anatomy checklist). End-of-session huddle: each team lists its top-3 changes before L32.

## 4. Network Diagram: the quality loop

```
 [Draft deliverables (W15)] ──► [Design reviews] ──► [action items]
        ▲                                                   │
        │                                                   ▼
 [Final deliverables (L32)] ◄── [change log] ◄── [IR simulation + gaps]
        │                                              │
        └──────────► [L32 defense] ◄── defense pack ◄──┘
```

## 5. Protocol Examples

- Review rubric card (condensed): `R1 requirements→artifact map | R2 sample 3 rules for least privilege | R3 IdP/NAT/scanner failure modes | R4 pick 2 ATT&CK tactics → detection coverage | R5 who is paged, exceptions process`.
- Change-log entry: `CHANGE-04 | Added egress allow-list to GUEST zone | Source: review R2 | Justification: exfil-path closure | Verified: retest matrix updated`.
- Simulation inject 1: Suricata sid 1000001 fires on WEB-03 → the course's recurring fictional C2 (continuity is deliberate) → expected path: L26 triage → their flow collector → quarantine VLAN per their playbook → incident-state doc in-window.

## 6. Configuration Concepts (concept level)

- Review schedule: 4 slots × 10 min, panel = instructor + 2 peers per slot.
- Simulation arming: injects per team, no cross-team visibility; ground rules stated.
- Dry-run plan for the defense: presenter roles, question-owner map.

## 7. Security Implications

- Artifacts, not opinions, carry design arguments — reviews interrogate evidence.
- Simulation injects calibrated to your design make visibility itself a rubric finding: "we saw nothing" is about the design.
- The integration loop is professional life: feedback → change → verification → defense.

## 8. Realistic Organizational Scenario

**Your own capstone is the scenario.** The simulation mirrors real SOC life: your detections fire (or don't), your playbook runs (or reveals gaps), your authority matrix answers the exec-pressure inject (or exposes that you never wrote one). The review questions you fail today are the interview questions you'll answer better tomorrow. Preparation for the defense is **case cs-098** (defense pack: change log, ten hardest questions with artifact-cited answers, 8-minute outline, dry-run plan); the inject-handling under pressure is **cs-099**.

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "The capstone is a big lab report" | It's an integration: architecture + detection + response + forensics + communication. |
| "Design review = show the diagram" | Diagrams aren't arguments; cited trade-offs are. |
| "The simulation is graded on winning" | Process quality — citations, trade-offs, honest unknowns — is the rubric. |
| "Feedback means redoing everything" | The change log scopes revisions; verification proves them. |
| "We present; the panel judges" | You review two other teams too — critiquing is half the learning. |

## 10. Classroom Activities

1. **Design reviews (4 slots):** present once, review twice, log action items both ways.
2. **IR simulation (staggered 20-min windows):** run your playbook against calibrated injects; produce the incident-state doc live.
3. **Integration huddle:** top-3 changes list; assign owners; verify retest plan.

## 11. Problem-Solving Questions

1. Why is "we saw nothing during the simulation" a rubric finding for the *design*, not the team's luck?
2. Your panel found a shadowed rule in your production-design rulebase: what does that say about your L11 audit process, and what's the fix beyond the fix?
3. During the exec-pressure inject, your authority matrix said "no": rehearse the 30-second answer.
4. Which deliverable benefited most today — and which needs the most work before L32?
5. How would you run this review format in a real organization (name the meeting it replaces)?

## 12. Exit Ticket

1. Name the four review rubric dimensions beyond requirement coverage.
2. In the simulation, which deliverable does the incident-state doc become?
3. What makes an inject "calibrated to the team's design" — and why does that matter for fairness?
4. Give one change-log field and why it exists.
5. What's the difference between defending a design and defending a diagram?

*(Answers: `the instructor answer-key collection (not published)`.)*

## 13. References

- Course-internal formats: L25 playbook anatomy; L26 incident-state template; L30 report structure.
- NIST SP 800-61 — simulation alignment to lifecycle phases.
- MITRE ATT&CK Navigator — detection-coverage presentation.
- CIS Controls v8 — requirement-traceability anchors.

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-11 | §3.3 simulation execution | Capstone IR exercise, Final |
| CLO-15 | §3.2 review + briefing under pressure | Capstone defense (L32) |
