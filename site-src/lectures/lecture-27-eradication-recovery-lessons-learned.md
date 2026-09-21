# L27 — Eradication, Recovery & Lessons Learned

## 1. Learning Objectives

By the end of this session you can: (1) plan eradication per finding — persistence classes, credential rotation, entry-vector closure — with *verification*, not assumptions; (2) sequence recovery safely with pre-agreed success criteria; (3) recognize eradication failure modes; (4) lead a blameless post-incident review that produces control changes; (5) structure the dual-audience incident report (CLO-15).

## 2. Key Definitions

| Term | Definition |
|---|---|
| Eradication | Removing attacker access *and* the conditions that allowed it |
| Persistence | Mechanisms maintaining access (autostarts, services, implants, credentials, firmware) |
| Entry vector | The path that admitted the attacker (phish, exposed service, missing patch) |
| Success criteria | Pre-agreed, verifiable conditions for reconnecting systems |
| Staged recovery | Ordered restoration (identity → core services → data) with enhanced monitoring |
| Blameless review | Examine systems/decisions, not people — to produce honest findings |
| Root-cause ladder | Symptom → contributing conditions → root causes (usually preparation gaps) |
| MTTR / MTTD | Mean time to respond / to detect — the report's core metrics |

## 3. Detailed Explanations

### 3.1 Eradication: close the door *and* evict the guest
Three threads, all required:
- **Entry-vector closure:** purge the phishing mail, firewall the exposed service (L10/L11 artifacts), patch the missing CVE (L24 SLA).
- **Persistence enumeration:** autostarts/scheduled tasks, service implants, credential stores — rotate *account material*, not just passwords (Kerberos tickets, OAuth tokens, API keys — the cloud-era extension); firmware/UEFI persistence exists, so humility matters.
- **Verification — not assumption:** define the scan set that says "clean *enough*": L22 rules against 72 h of fresh telemetry, L23 hunts (entropy, sweeps, cadence) on host *and* segment, L24 credentialed rescan confirming the patch, and a **credential-rotation ledger** checked against first-compromise time.

### 3.2 Recovery engineering
**Clean-build vs in-place clean:** speed vs assurance — gold-image discipline (L24's hardening baseline) decides. **Staged restoration:** identity infrastructure first (AD/IdP), then core services, then user data — with **enhanced monitoring** during the re-entry window (L21 pipelines tuned hot, 14 days). **Success criteria are pre-agreed:** N days of clean telemetry, no beacon-pattern recurrence, rotation ledger complete — written *before* reconnection, not negotiated during the executive call.

### 3.3 Eradication failure vignettes (why checklists exist)
- **The reimage that wasn't:** persistence in a task invoked by the storage array's own agent — second compromise 9 days later.
- **The unchanged door:** credentials rotated, but the phishing path (unfixed mail rule, no MFA on that account) re-admitted the actor.
Lesson: eradication checklists are per-vector, and the post-incident review updates them.

### 3.4 The blameless review that changes things
Assume everyone acted reasonably on the information they had; examine systems and decisions. The **root-cause ladder**: symptom → contributing conditions → root causes (usually preparation gaps — L25's thesis). **Action-item discipline:** owner, date, verification method, tracked to closure. Metrics for the report: MTTD/MTTA/MTTR, scope counts, evidence-quality notes — honest numbers only.

### 3.5 The incident report (dual audiences, one evidence base)
**Executive summary (≤1 page):** what happened, business impact, what we did, what changes — no jargon. **Technical appendix:** timeline with citations (L26), scope statement, evidence index, IOCs, verification results. Recommendations mapped to controls with owners. (L30 develops this format fully; today you produce the review + action items.)

## 4. Network Diagram: eradication → recovery flow

```
 [Containment done (L26)]
      │
      ├─► Entry vector closed?   (mail rule / firewall / patch — verified)
      ├─► Persistence swept?     (autostart, services, credentials ledger)
      ├─► Verification set run?  (rules + hunts + rescan — "clean enough")
      ▼
 [Pre-agreed success criteria met?] ──no──► hold (document why)
      │ yes
      ▼
 [Staged recovery: identity → core → data]  + enhanced monitoring (14d)
      ▼
 [Blameless review → action items (owner/date/verification)] → back to L25 prep
```

## 5. Protocol Examples

- Verification set (design artifact): re-image from gold image **plus** L22 ruleset against fresh telemetry; L23 hunts on host *and* segment; L24 credentialed rescan; credential ledger timestamps vs first-compromise time.
- Recovery monitoring uplift: beacon-candidate thresholds tightened for 14 days; daily profile diffs; alert on *any* new external destination.

## 6. Configuration Concepts (concept level)

- Gold-image pipeline with the L24 hardening baseline baked in.
- Re-entry monitoring profile (temporary, auto-expiring).
- Action-item tracker with owner/date/verification fields.

## 7. Security Implications

- "Reimage = clean" is the most expensive assumption in IR — verification is a defined artifact.
- Recovery is a security decision gated by pre-agreed criteria, not an IT task.
- Blameless reviews produce the control changes that make the next incident smaller.

## 8. Realistic Organizational Scenario

**The tabletop (the session's core exercise).** Continuing the L26 incident, six timed injects: (1) beacon recurs on a "clean" host mid-recovery; (2) exec demands early reconnection; (3) media call; (4) regulator asks for custody proof; (5) acquisition-log gap found; (6) budget ask. Each requires a decision + rationale on the decision log. Your deliverables feed Assignment 6 and **case cs-084** — the lessons-learned report that changes controls (at least two action items must touch *preparation*).

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "Reimage = eradicated" | Persistence hides in agents, firmware, and *credentials* — verify with a defined set. |
| "Recovery = turn it back on" | Staged, monitored, criteria-gated — or you re-earn the incident. |
| "Lessons learned = blame allocation" | Blame kills honesty; systems/decisions get examined. |
| "The incident ends at containment" | Eradication, recovery, and review are where recurrence is prevented. |
| "One review meeting is enough" | Action items with owners and dates, tracked to closure. |

## 10. Classroom Activities

1. **Tabletop exercise (40 min, teams of 4):** six injects with decision log (see §8).
2. **Success-criteria drafting:** write two verifiable criteria for reconnecting a plant-floor segment.
3. **Root-cause ladder drill:** symptom ("malware returned") → contributing conditions → root causes.

## 11. Problem-Solving Questions

1. Your reimage passed every scan and the beacon returned in 9 days — enumerate three hiding places your checklist missed.
2. The CEO wants the plant floor reconnected tonight: what do your pre-agreed criteria allow you to say, and what's your escalation path?
3. Which is harder — eradicating the malware or closing the entry vector — and why does it differ by attacker class?
4. In blameless review, where does the line sit between system failure and individual action?
5. What two metrics lead your report for the executive audience, and why those?

## 12. Exit Ticket

1. List four persistence classes your eradication checklist must cover.
2. What makes recovery "staged," and which system returns first — why?
3. Write one verifiable success criterion (not "it seems fine").
4. What does the credential-rotation ledger prove, and against what timestamp?
5. Name the review's three required outputs.

*(Answers: `the instructor answer-key collection (not published)`.)*

## 13. References

- NIST SP 800-61 Rev. 2 — eradication/recovery/post-incident guidance.
- NIST SP 800-86 — verification and evidence integration.
- MITRE ATT&CK — persistence techniques (T1547-class) for checklist coverage.
- SANS IR Handbook — post-incident review patterns.

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-11 | §3 eradication/recovery/review; tabletop | Assignment 6 (W13), Quiz 5 (W14), Capstone IR, Final |
