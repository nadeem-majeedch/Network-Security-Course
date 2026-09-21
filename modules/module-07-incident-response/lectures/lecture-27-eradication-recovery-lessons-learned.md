---
lecture: L27
title: Eradication, Recovery & Lessons Learned
module: 7
week: 14
hours: 2
clos: [CLO-11]
difficulty: advanced
status: complete
artifact-type: teaching-plan
---

# L27 — Eradication, Recovery & Lessons Learned

## 1. Overview & Prerequisites

- **Prerequisites:** L26 (triage/scope/containment — the incident continues today), L25 (lifecycle, evidence discipline).
- **Position:** completes the response arc. The tabletop (graded in-class, feeds Assignment 6's second half and the capstone IR exercise) forces students to run eradication→recovery→review decisions under time pressure. Quiz 5 (W14) samples L25–L28.
- **Faculty prep:** prepare the tabletop inject pack (6 timed injects continuing the L26 incident); prepare the "false eradication" vignette (persistence survives reimaging); ready the post-incident report skeleton.
- **Common misconceptions:** "reimage = eradicated"; "recovery = turn it back on"; "lessons learned = blame allocation"; "the incident ends at containment."

## 2. Learning Objectives

By the end of this lecture, students can:

1. Plan eradication per finding: remove persistence, rotate credentials/keys, patch the entry vector, and *verify* absence (not assume it) (Create/Evaluate).
2. Sequence recovery safely: clean-build validation, staged restoration, enhanced monitoring during re-entry, and success criteria (Create).
3. Distinguish eradication failure modes: missed persistence (firmware/credential/classic autostart classes), re-infection via unchanged entry vector (Analyze).
4. Lead a post-incident review that produces control changes, not blame: root-cause framing, action items with owners/dates, and the loop back to preparation (L25) (Evaluate/Create).
5. Produce the incident report: executive summary + technical detail + metrics (MTTD/MTTR), written for both audiences (CLO-15) (Create).

## 3. Detailed Concepts

### 3.1 Eradication: hunting what let it in and what kept it in
- Entry-vector closure: the phishing mail → mailbox purge, the exposed service → firewall fix (L10/L11 artifacts), the missing patch → remediation (L24 SLA).
- Persistence enumeration: autostarts/scheduled tasks, service implants, credential stores (pass-the-hash era → rotate *account* material, not just passwords: Kerberos tickets, OAuth tokens, API keys — the cloud-era extension), firmware/UEFI-level persistence for the "assume breach" humility check.
- Verification mindset: absence of evidence ≠ evidence of absence — define the verification scan set (L22 rules + L23 hunts + L24 scans) that says "clean *enough*," with residual-risk statement.

### 3.2 Recovery engineering
- Clean-build vs in-place clean: trade-offs (speed vs assurance); gold-image discipline (L24 hardening baseline returns).
- Staged restoration order: identity infrastructure first (AD/IdP), then core services, then user data — with *enhanced monitoring* thresholds active during re-entry window (L21 pipelines tuned hot).
- Success criteria (pre-agreed): N days of clean telemetry, no beacon-pattern recurrence, credential-rotation complete — written *before* reconnection, not negotiated during.

### 3.3 Eradication failure vignettes
- The reimage that wasn't: persistence in a task called by the storage array's own agent; second compromise 9 days later.
- The unchanged door: credentials rotated, but the phishing path (unfixed mail rule + no MFA on that account) re-admits the actor.
- Lesson: eradication checklists are per-vector; the post-incident review drives their updates.

### 3.4 Post-incident review that changes things
- Blameless framing: assume everyone acted reasonably on the information they had; examine systems/decisions, not people.
- Root-cause ladder: symptom → contributing conditions → root causes (usually: preparation gaps — L25's thesis).
- Action-item discipline: owner, date, verification method; tracked to closure (the "lessons learned report that changes controls" is a deliverable pattern — cs-084).
- Metrics for the report: MTTD/MTTA/MTTR, scope counts, evidence quality notes, cost-avoidance framing where honest (no inflated claims — Mission rule 5 ethos).

### 3.5 The incident report (dual-audience craft)
- Executive summary: what happened, business impact, what we did, what changes now — no jargon, no blame.
- Technical appendix: timeline with citations (L26), scope statement, evidence index, IOC list, verification results.
- IOC handling: shareable vs internal (legal/privacy review), industry-sharing programs (responsible-sharing framing from the ethics policy).

## 4. Teaching Sequence (120 Minutes)

| Time | Segment | Instructor moves |
|---|---|---|
| 0–10 | Recap: L26 incident state | Read one team's handoff doc aloud — "we resume *their* incident" |
| 10–30 | Core: eradication planning | Persistence taxonomy; verification-scan set design; the reimage vignette |
| 30–50 | Core: recovery engineering | Staged restoration diagram; success-criteria drafting exercise (fast round) |
| 50–60 | Break | — |
| 60–100 | **Tabletop exercise** (injects every ~6 min) | Teams of 4 run injects: re-infection, exec demand to reconnect early, media inquiry, regulator question, evidence-custody gap, budget ask |
| 100–110 | Review + root-cause ladder | Teams extract 3 action items from their inject decisions |
| 110–120 | Wrap + formative | Exit ticket; **Quiz 5** administration (10 min, end-of-slot); Assignment-6 full collection; L28 trailer: "hunting: find them before they fire" |

## 5. Technical Examples

```
# Eradication verification set (design artifact for the tabletop):
# 1. Re-image host from gold image (L24 baseline) — but ALSO:
# 2. Re-scan with L22 ruleset (sid 1000001/1000002) against 72h of fresh telemetry
# 3. Re-run L23 hunts: DNS entropy + SMB sweep + beacon cadence — host AND segment
# 4. Re-scan with L24 credentialed policy — confirm entry-vector patch in place
# 5. Credential rotation ledger: user passwords + tickets + API keys + service
#    accounts, with timestamps — checked against first-compromise time.
# Teaching point: "clean" is defined by this checklist, agreed BEFORE reconnection.

# Recovery monitoring uplift (re-entry window):
#   Pipeline (L21): raise beacon-candidate threshold sensitivity for 14 days;
#   add host to daily Zeek profile diff; alert on ANY new external destination.
```
Expected teaching points: verification is multi-tool and time-boxed; monitoring uplift is pre-planned; the ledger turns "we rotated credentials" into evidence.

## 6. Discussion Questions

1. Your reimage passed every scan, and the beacon returned in 9 days. Enumerate three hiding places your checklist missed.
2. The CEO wants the plant floor reconnected tonight. What do your pre-agreed success criteria allow you to say — and what's your escalation path?
3. Which is harder: eradicating the malware or closing the entry vector? Why does the answer differ by attacker class?
4. Blameless review: how do you handle the one admin who disabled logging on the affected segment? (Policy, not personality.)
5. What belongs in the IOC list you share externally vs internally — and who reviews that decision?

## 7. Student Activity

**Tabletop exercise (40 min, teams of 4):** six timed injects continuing the L26 incident, each requiring a decision + one-line rationale on the decision log. Injects: (1) beacon recurs on a "clean" host mid-recovery; (2) exec demands early reconnection; (3) media call; (4) regulator asks for evidence custody proof; (5) responder finds evidence gap in acquisition log; (6) post-incident budget ask. Deliverable: decision log + 3 root-cause action items — feeds Assignment 6 and cs-084.

## 8. Problem-Solving Case

**Primary case — cs-084 "Lessons-learned report that changes controls" (advanced):**
Using the class incident's full record (L25 playbook, L26 triage/scope/containment docs, today's tabletop decisions), students write the post-incident report: executive summary (≤ 1 page, no jargon), technical appendix (timeline + evidence index + IOCs), metrics table (MTTD/MTTA/MTTR), and exactly five action items (owner, date, verification) mapped to lifecycle phases. Constraint: at least two action items must change *preparation* (L25), not just detection.
**Linked cases:** cs-083 (eradication sequencing and validation).
*(Model solutions: instructor answer-key set, Module 7.)*

## 9. Formative Assessment

1. List four persistence classes your eradication checklist must cover.
2. What makes recovery "staged," and which system returns first — why?
3. Write one success criterion that is verifiable (not "it seems fine").
4. In blameless review, where does the line sit between system failure and individual action?
5. What two metrics does your report lead with for the executive audience?
*(Answer key: instructor set, Module 7.)*

## 10. Summary & Key Takeaways

- Eradication = entry vector + persistence + credentials, closed with a *pre-agreed* verification set.
- Recovery is staged, monitored, and criteria-gated — re-entry is a security decision, not an IT task.
- The review exists to change controls; the report serves two audiences with one evidence base.

## 11. References

- NIST SP 800-61 Rev. 2 — eradication/recovery/post-incident guidance.
- NIST SP 800-86 — verification and evidence integration.
- MITRE ATT&CK — persistence technique taxonomy (T1547-class) for the eradication checklist.
- SANS IR Handbook — post-incident review patterns.

## 12. CLO Mapping

| CLO | Where in this lecture | Assessed via |
|---|---|---|
| CLO-11 | §3.1–3.5 eradication/recovery/review; tabletop §7 | Assignment 6 (today), Quiz 5 (today), Capstone IR, Final |
