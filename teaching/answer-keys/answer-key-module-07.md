---
module: 7
lectures: [L25, L26, L27, L28]
status: complete
artifact-type: answer-key
instructor-only: true
distribution: never-publish-to-students
---

# Answer Key — Module 7: Incident Response, SOC Operations & Threat Intelligence

> **INSTRUCTOR ONLY — contains model answers to graded formative assessments.**
> Links: Plans `modules/module-07-incident-response/lectures/` · Student pages `docs/lectures/lecture-25…28` · Notes `teaching/speaker-notes/lecture-25…28-speaker-notes.md`

## L25 — IR Lifecycle & Preparation

### Formative checks (plan §11)
1. IR phases (PICERL-style): Preparation → Identification → Containment → Eradication → Recovery → Lessons Learned. Preparation is the answer to "most important" — everything downstream depends on readiness assets.
2. Preparation artifacts: contact roster (with out-of-band), severity rubric, evidence-handling procedure, runbooks per scenario, pre-authorized legal counsel — any four with one sentence each.
3. Severity dimensions: business impact × spread/propagation risk × data sensitivity; P1 = business-stopping or propagating — the rubric *is* the graded artifact, so consistency with it matters.
4. Runbook anatomy: trigger conditions, roles, first-three-actions, escalation paths, communication templates, evidence checkpoints — runbooks are checklists under stress, not essays.
5. Communication plan: internal (who informs whom, when), external (customers/regulators — legal gates the clock), and the *single spokesperson* rule.

### Exit ticket
- The 2 a.m. test: if your plan needs the org chart, it fails — contact roster with backup names is the portable artifact; "call the manager who's on leave" is the failure mode to name.
- First containment decision with incomplete data: contain laterally (segment suspected hosts) while preserving evidence — reversible-first logic from L26 applies here.

### Discussion facilitation
- Q4 (regulator notification clock): the answer is *legal counsel pre-engaged with a decision tree* — improvising timelines during an incident is the failure; reward students who name the pre-work.

## L26 — Detection, Triage & Containment

### Formative checks
1. Triage questions: What is the alert actually saying (evidence, not narrative)? Is it corroborated? What's the blast radius? What's the reversibility of next actions? — the four in order.
2. Three-way corroboration: IDS alert (signature says beacon) + Zeek (cadence/entropy says beacon) + flows (asymmetric periodic volume says beacon) — each adds a fact; single-source action is the graded error.
3. Containment ladder: isolate (network quarantine, reversible) → block (egress/domain, reversible-ish) → remove/disable (account/host, more disruptive) → each step documented with visibility cost noted.
4. Evidence preservation: capture volatile state (connections, processes) *before* power actions; hash images; chain of custody from first touch — "reboot to fix" destroys the case.
5. Handoff documentation: what/when/source, evidence locations, actions taken with times, open questions — a handoff that requires a call to interpret has failed.

### Exit ticket
- Executive pressure case: present evidence + options with risk estimates, let the risk owner decide *on record* — the analyst's job is truthful framing, not silent compliance or heroic refusal; the documented decision is what survives review.
- Containment kills visibility: every block shrinks the observation window — sequence reversible-observational steps before hard blocks, and say why.

### Guided-exercise grading (4-phase block)
- Phase gates: triage (corroboration cited), scope (hosts named from evidence), containment (ladder order), record (handoff complete). Partial-but-documented beats undocumented-complete — stated in the rubric, enforce it.
- Common exercise failures: acting on the alert narrative without corroboration; irreversible action in phase 1; handoff notes with no timestamps.

## L27 — Eradication, Recovery & Lessons Learned

### Formative checks
1. Eradication vs containment: eradication removes the adversary's presence *and access paths* (artifacts, persistence, credentials) after scoping is confident — premature eradication on an incompletely-scoped incident reopens it.
2. Persistence mechanisms (conceptual): autostart entries, scheduled tasks, service creation, credential theft enabling re-entry (e.g., golden-ticket concepts) — for each: the *evidence* it leaves and the *hunt* that finds it.
3. Restoration order: identity infrastructure before dependent services (DNS/DHCP before app tiers, credentials rotated before reconnection) — dependency-ordered, verified stepwise; "restore everything at once" fails.
4. Recovery criteria: go/no-go checklist — no unexplained anomalies, persistence hunt clean on restored hosts, credentials rotated, monitoring heightened — the *checklist* decides, not optimism.
5. Lessons-learned quality: blameless (systemic language), actionable (each finding → owned action with date), scheduled (measured at next exercise) — "humans blamed, no changes" fails.

### Exit ticket
- The re-compromise loop: restored hosts phoning home means an access path survived — credential rotation and persistence hunting are the two hypotheses to test first, in that order for credential-centric incidents.
- Credential rotation priority: adversary-facing secrets first (KRBTGT-concept domain keys, service accounts with external reach), then the long tail — "rotate everything" without order fails the knowledge check.

### Discussion facilitation
- Q5 (blameless resistance): reframe with the systemic-language sentence stems; the counterexample (post-blame reporting suppression) makes the case better than policy language.

## L28 — SOC Operations, Maturity & Threat Intelligence

### Formative checks
1. SOC roles: tiered analysts (triage → investigation), detection engineering, threat intel, hunt, shift lead — and the *escalation contract* between them.
2. Maturity model honesty: tiers describe process consistency, not tool budgets; the self-assessment must cite evidence per level — maturity without evidence is marketing (the lecture's core claim).
3. TI lifecycle: requirements (what decisions intel must support) → collection → processing → analysis → dissemination → feedback — skipping *requirements* produces hoarding.
4. Source scoring: reliability × recency × relevance (the Admiral-grade-inspired rubric taught); undisseminated intel = inventory, not capability.
5. Metrics: MTTD, dwell time, coverage per ATT&CK technique, time-to-tune — each metric paired with the decision it changes; unpaired metrics are theater.

### Exit ticket
- Intel-to-detection path: report → extraction (IoCs/behaviors) → scoring → detection rule/tuning → feedback to source — a path with *feedback* is the full-credit answer.
- One-analyst SOC: requirements-driven collection, weekly packaged dissemination, measured coverage — process discipline beats headcount; the metrics wall makes it visible.

### Case study anchors (cs-073–cs-084) — grading pointers
- **cs-073–cs-076 (L25/L26):** timeline reconstruction answers must cite evidence per claim; severity calls must reference the rubric, not vibes.
- **cs-077–cs-080 (L27):** recovery plans need dependency-ordered restoration + verification criteria; "restore from backup" alone fails.
- **cs-081–cs-084 (L28):** intel writeups need scoring + dissemination format matched to audience; undifferentiated dumps fail.

## Common misconceptions (module-level)
1. "IR is a tech problem" — communications, legal, and decision-record discipline decide outcomes as often as packets do (L25/L26).
2. "Containment ends the incident" — eradication, recovery, and lessons-learned are where incidents actually end (L27).
3. "More maturity tiers = better SOC" — outcome metrics (MTTD, dwell, coverage) are the evidence; tiers are description, not achievement (L28).
4. "Threat intel = IoC feeds" — requirements-driven analysis and dissemination produce decisions; raw feeds produce noise (L28).
