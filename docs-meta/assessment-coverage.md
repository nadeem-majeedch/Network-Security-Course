---
artifact-type: assessment-coverage
status: complete
components: 59
last-updated: assessment-package session
---

# Assessment Package — Coverage Report

> Generated artifacts validated by `docs-meta/validate_assessments.py`
> (A1–A8, exit 0). This report records what exists and what it assesses;
> **no class statistics are pre-filled** — post-marking numbers are
> recorded in the answer keys' calibration sections only after delivery.

## 1. Component inventory (59 files)

| Layer | Student artifacts | Instructor keys | Count |
|---|---|---|---|
| Graded quizzes (Q01–Q05, weeks 2/4/5/10/14) | `assessments/quizzes/quiz-01…05-*.md` | `instructor/answer-keys/quiz-01…05-answer-key.md` | 10 |
| Self-check quizzes (Q06–Q16, weeks 1/3/6/7/8/9/11/12/13/15/16) | `assessments/quizzes/quiz-06…16-*.md` | keys 06–16 | 22 |
| Assignments (7, weeks 6/7/9/11/12/13/15) | `assessments/assignments/assignment-01…07-*.md` | keys 01–07 | 14 |
| Question bank (50 questions) | `question-bank.md` + generator script | `question-bank-answer-key.md` | 3 |
| Midterm (week 8, 100 marks) | `assessments/midterm/midterm-exam.md` | `midterm-answer-key.md` | 2 |
| Final (week 16, 100 marks, written + forensic practical) | `assessments/final/final-exam.md` | `final-answer-key.md` | 2 |
| Capstone (brief, rubric, defense guide) | 3 files | `capstone-rubric-bands.md` | 4 |
| Case-study evaluation (rubric + protocol) | `case-evaluation-rubric.md` | `case-evaluation-protocol.md` | 2 |
| **Total** | | | **59** |

## 2. Weekly assessment units (16 = 5 graded + 11 self-check)

Every week 1–16 carries an assessment unit; graded units follow the
syllabus calendar (weeks 2/4/5/10/14), self-checks fill the remaining
weeks and warm up the graded items that follow them (Q10→Quiz 4, Q13→
midterm, Q14→final, Q16→defense).

| Week | Unit | Type | CLO | Marks |
|---|---|---|---|---|
| 1 | Q06 | self-check | CLO-1 | 10 |
| 2 | **Q01** | **graded** | CLO-1 | 15 |
| 3 | Q07 | self-check | CLO-2 | 10 |
| 4 | **Q02** | **graded** | CLO-2 | 15 |
| 5 | **Q03** | **graded** | CLO-3, CLO-5 | 15 |
| 6 | Q08 + Assignment 1 | self-check + assignment | CLO-3, CLO-4 | 10 + 100 |
| 7 | Q09 + Assignment 2 | self-check + assignment | CLO-5/6/7 | 10 + 100 |
| 8 | Q13 + **Midterm** | self-check + **exam** | CLO-1..7 | 10 + 100 |
| 9 | Q10 + Assignment 3 | self-check + assignment | CLO-8/13, CLO-5/7 | 10 + 100 |
| 10 | **Q04** | **graded** | CLO-8, CLO-13 | 15 |
| 11 | Q11 + Assignment 4 (+ Pract-4) | self-check + assignment | CLO-9/10/12 | 10 + 100 |
| 12 | Q15 + Assignment 5 | self-check + assignment | CLO-9/10 | 10 + 100 |
| 13 | Q12 + Assignment 6 | self-check + assignment | CLO-11/12 | 10 + 100 |
| 14 | **Q05** | **graded** | CLO-11, CLO-14 | 15 |
| 15 | Q14 + Assignment 7 | self-check + assignment | CLO-8..15 | 10 + 100 |
| 16 | Q16 + **Final** + capstone defense | self-check + **exam** + defense | CLO-11/14/15 | 10 + 100 + rubric |

## 3. CLO coverage (assessed where)

| CLO | Quiz units | Assignments | Exams | Other |
|---|---|---|---|---|
| CLO-1 | Q01, Q06, Q13 | — | Midterm A/B | Case Set A |
| CLO-2 | Q02, Q07, Q13 | Case Set A | Midterm A/C | Case Set B |
| CLO-3 | Q03, Q08, Q13 | Assignment 1 | Midterm A/C/D | Case Set B |
| CLO-4 | Q08 | Assignment 2 | Midterm | — |
| CLO-5 | Q03, Q09, Q13 | Assignment 3 | Midterm B/D | — |
| CLO-6 | Q09 | Assignment 2 | Midterm | Case Set B |
| CLO-7 | Q09 | Assignment 3 | Midterm B/D, Final | — |
| CLO-8 | Q04, Q10, Q14 | — | Final A | — |
| CLO-9 | Q11, Q14, Q15 | Assignment 4 | Final A/C | Case Set C |
| CLO-10 | Q11, Q15 | Assignment 5 | Final B | Case Set C |
| CLO-11 | Q05, Q12, Q14 | Assignment 6 | Final B/C | Capstone D3 |
| CLO-12 | Q11, Q12 | Assignment 4/6 | Final B | Case Set C |
| CLO-13 | Q04, Q10, Q14 | Assignment 7 | Final A/B | — |
| CLO-14 | Q05, Q14 | — | Final P1/P2/P4 | Case Set C, Capstone |
| CLO-15 | Q14, Q16 | Assignment 7 | Final P3 | Capstone D1–D4 |

**All 15 CLOs assessed** through ≥3 distinct assessment types each
(validator A4 confirms the union; this table shows the distribution).

## 4. Question types delivered (mission areas)

| Mission requirement | Where |
|---|---|
| MCQs with validated answers | All quizzes + exams Section A (69 MCQs) + bank (27 MCQs) |
| Short-answer questions | Quizzes Section B, exams Section B |
| Analytical/scenario questions | Quizzes Section C, exam C1, assignment briefs |
| Network diagram interpretation | Q06/Q8, Q07/Q7, Q09/Q8, Q10/Q7, Q11/Q7, Q13/Q7, Q14/Q7, Q16/Q7; QB-042/046/047 |
| Firewall & ACL design | Quiz 3 C8, Midterm C1, QB-040, cs-031/034-aligned cases |
| Packet analysis | Quiz 1 C8, Midterm C2, Final Part II (PCAP-based), QB-041/043 |
| Incident-response tasks | Quiz 5, Assignment 6, Final P2–P4, QB-044 |
| Question bank categorized by CLO/module/difficulty | Bank key summary counts + per-question tags |
| Bloom level per question | All graded quiz questions tagged; bank key carries all six levels |
| Capstone instructions + rubric | `capstone-brief.md`, `capstone-rubric.md`, `defense-guide.md` |

## 5. Mark-arithmetic guarantees (validator A2)

- Graded quizzes: per-question Bloom tags sum exactly to the declared
  total (15 each).
- Assignments: task marks sum to 100 each.
- Midterm: A 10×2=20 + B 4×7.5=30 + C 2×15=30 + D 20 = **100**.
- Final: Part I (A 8×2=16 + B 4×6=24 + C 20) = 60 + Part II 40 = **100**.
- Question bank: 50 questions, 100 marks total (generated — script is
  the source of truth).

## 6. Separation guarantee (validator A3/A5)

- Every student artifact front-matters its key link; every key resolves
  on disk and is marked `instructor-only: true`.
- Student **`.md`** tree scanned for instructor markers (answer lines, model
  solutions, "INSTRUCTOR ONLY") — clean. The one file-tree hit is
  `question-bank/generate_question_bank.py`'s string literal that *writes*
  the instructor key's own banner — tool code, not student content.
- Case-set selection/rotation and the scoring record live only in
  `instructor/answer-keys/case-evaluation-protocol.md`.

## 7. Gaps honestly recorded

- **Lab practicals (4 × 5%, Pract-1–4):** the *graded practical*
  assessment forms live in the lab answer keys' rubric sections
  (`teaching/lab-answer-keys/`) — delivered with the lab layer, not
  duplicated here. The validator counts them via the syllabus weight
  reconciliation (A7).
- **Question-bank randomization:** the bank is deterministic; online
  delivery should shuffle options (noted in the midterm key's grading
  note).
- **Class statistics:** intentionally absent — recorded post-marking in
  the keys' calibration sections only.
