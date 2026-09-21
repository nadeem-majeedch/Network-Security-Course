---
artifact-type: instructor-manual
status: complete
instructor-only: true
distribution: never-publish-to-students
---

# Delivery Guide — Global

## 1. Course delivery philosophy

Three commitments shape every session:

1. **Mechanism before mitigation.** Students who can't explain *why* an attack
   works can't evaluate a defense. Every lecture establishes mechanism first;
   controls are taught as responses to named mechanisms. This is why Module 1
   spends four weeks on protocol anatomy before Module 2 weaponizes it.
2. **Analysis under constraint.** Every graded artifact (baseline paragraph,
   rulebase, forensic timeline, triage note) is graded on *method and evidence
   discipline*, not conclusions alone. Partial-but-documented beats
   undocumented-complete — state this in week 1 and enforce it all semester.
3. **Trust boundaries as the through-line.** From L02 (ARP trust) to L32 (the
   synthesis question), the course is one argument: *trust is a design
   decision, and every control relocates or hardens a boundary.* Say this
   explicitly in L01 and again in L32; students should recognize it themselves
   by Module 6.

## 2. Session anatomy & timing (120 minutes)

Standard block used by all 32 plans (speaker notes carry the per-lecture variant):

| Segment | Typical span | Notes |
|---|---|---|
| Hook / retrieval quiz | 0–10 | Retrieves the *prior* lecture's mechanism — spaced retrieval, graded lightly |
| Core concept block 1 | 10–35 | Mechanism + live demonstration |
| Core concept block 2 | 35–55 | Design/defense implications, worked examples |
| Break | 55–65 | Non-negotiable; 2-hour blocks without a break lose the back half |
| Working block (lab/worksheet/case) | 65–105 | The graded spine — protect this time when compressing |
| Synthesis + exit ticket | 105–120 | Exit ticket (5 min) + next-session setup |

**Compression rule** (also stated in every speaker note): when behind, cut
*lecture exposition*, never the working block and never the graded artifact.
Every plan's speaker notes name the graded spine explicitly.

## 3. Semester rhythm

- **Quizzes:** Weeks 3, 6, 9, 12, 14 (five quizzes, per NSC-REQ-001 grading plan).
  Quizzes are cumulative-in-mechanism: each references prior modules' mechanisms.
- **Assignments:** A1 rulebase engineering (due W7), A2 risk report (W8), A3
  architecture design (W10), A4 detection rules (W11), A5 vulnerability cycle
  (W12) — due dates are stated in syllabus; re-check against `syllabus/syllabus.md`
  before announcing.
- **Capstone arc:** teams form W13, dry-run W15 (L31), defense W16 (L32). Teams
  of 4 with assigned role rotation (lead analyst, evidence custodian, comms,
  detection) — roles rotate once mid-arc.
- **Module boundaries** are natural checkpoints for returning formative
  feedback; return Module N answers before Module N+2 begins.

## 4. Demonstrations & lab range discipline

- All live attack demonstrations run **only** inside the isolated lab range.
  The instructor states the authorization boundary aloud at every attack-adjacent
  demo (L06, L07, L08, L17) — this models the professional norm and satisfies the
  course's ethics gate.
- Demos are rehearsed the week before; each has a fallback (recorded output) so
  a failed live demo costs minutes, not the mechanism.
- Console output is captured to text files and distributed — the transcript is
  the accessible artifact (see `accessibility.md`).

## 5. Assessment logistics

- **Formative (exit tickets, checks):** feedback within one week; they exist to
  surface misconceptions while they're still correctable — the misconception
  bank (`demonstrations-and-difficulties.md` §3) is updated from real exit-ticket
  data each run of the course.
- **Lab reports:** graded on evidence discipline (cited fields, confidence
  statements, reproducible commands) per the rubric in `model-answers-index.md`.
- **Late policy & academic integrity:** per institutional policy; capstone teams
  sign a contribution statement at L32 submission.
- **Never** publish: `teaching/` tree, answer keys, exam files. The Pages
  workflow must exclude `teaching/` — this is a gate (V5) in the plan validator.

## 6. First-session checklist (L01)

1. Syllabus walkthrough: grading weights, ethics/authorization policy (have
   students sign the lab rules sheet in week 1 — no signature, no range access).
2. State the three delivery commitments (§1) — the through-line sentence
   verbatim: "trust is a design decision."
3. Tooling check: Wireshark, tcpdump, Python, the range VM — the L01 exit
   ticket includes a tooling smoke test; failures get a fixed help session
   before L02.
4. Set the capstone expectation early: teams and case selection begin W13;
   the L01 preview prevents the W13 scramble.
