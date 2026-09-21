---
artifact-type: instructor-manual
status: complete
instructor-only: true
distribution: never-publish-to-students
---

# Model Answers — Index & Grading Philosophy

## 1. Where model answers live

| Artifact type | Location | Scope |
|---|---|---|
| Formative checks, exit tickets, discussion verdicts, case anchors, per-module misconception banks | `teaching/answer-keys/answer-key-module-01…08.md` | All 32 lectures |
| Capstone defense rubric (L31 dry-run + L32 defense) | `teaching/answer-keys/answer-key-module-08.md` §L31/L32 | Capstone arc |
| Quiz/exam answer keys | `teaching/assessments/` (when authored — see inventory; **not yet written**) | W3/6/9/12/14 quizzes, midterm, final |
| Assignment model answers | To be authored with each assignment in P3/P4 — not yet written | A1–A5 |

**Honesty note (mission rule 9):** quiz, exam, and assignment answer keys do
**not** exist yet; they are tracked as gaps in
`docs-meta/teaching-material-inventory.md`. Nothing in this manual pretends
otherwise.

## 2. Grading philosophy

1. **Method over conclusions.** A wrong answer with correct, cited evidence
   discipline outscores a right answer asserted without evidence — because the
   discipline is what transfers to employment.
2. **Partial-but-documented beats undocumented-complete.** Stated in week 1,
   applied in every lab and the capstone exercise rubric.
3. **Safety marks are real marks.** Every attack-adjacent artifact (L06–L08,
   L17, scans in L24) carries safety marks: authorization boundary respected,
   no out-of-scope actions, evidence handled per policy. Safety violations cap
   the artifact at zero regardless of technical quality.
4. **Precision on the E-A-I distinction** (encryption / authentication /
   authorization / integrity) is graded explicitly wherever crypto appears
   (L13–L16, and any capstone crypto claims).
5. **Confidence language is graded** in analysis artifacts: every finding
   states its evidence and its limits. Absolute language without evidence
   ("the attacker definitely…") loses marks — the L30 report rubric enforces
   this at the highest level.

## 3. Rubric anchors (fast reference)

### Lab report rubric (Modules 1–6)
| Dimension | Weight |
|---|---|
| Evidence discipline (cited fields, reproducible commands, confidence stated) | 40% |
| Mechanism accuracy (protocol-level correctness) | 30% |
| Analysis depth (limitations, alternatives considered) | 20% |
| Safety & policy compliance | 10% |

### Capstone rubric
See `answer-key-module-08.md` §L32 (technical accuracy 30, evidence 25,
judgment 20, communication 15, synthesis 10).

### Feedback turnaround
Formative within one week; labs within two; capstone dry-run feedback before
L32 (same week). Turnaround is a syllabus commitment — calendar it, don't
improvise it.

## 4. Using answer keys without killing discussion

Answer keys include *verdicts and grading pointers*, not scripts. In
discussion, reveal verdicts only after positions are committed (the §1 moves in
`facilitation-and-troubleshooting.md`). If a session's discussion surfaced a
better answer than the key's, update the key — the keys are living documents
with a change note in `docs-meta/teaching-material-inventory.md`.
