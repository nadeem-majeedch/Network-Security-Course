---
assessment: case-evaluation
type: rubric-and-protocol
clos: [CLO-2, CLO-12, CLO-14]
cases-referenced: 100
status: complete
artifact-type: student-visible-rubric
instructor-protocol: instructor/answer-keys/case-evaluation-protocol.md
---

# Case-Study Evaluation Protocol & Rubric

> The course's 100 case studies (`docs-meta/case-index.md`) are used in
> two modes: **classroom mode** (projector, 5-minute reasoning, solution
> reveal — ungraded) and **evaluation mode** (graded case sets, below).

## Graded case sets (three per student per term)

| Set | Window | Tier mix | CLO focus |
|---|---|---|---|
| **Case Set A** | weeks 4–5 | beginner ×2 + intermediate ×1 | CLO-1, CLO-2 |
| **Case Set B** | week 8 (with midterm) | intermediate ×2 + advanced ×1 | CLO-2, CLO-3, CLO-6 |
| **Case Set C** | week 13 | advanced ×2 + expert ×1 | CLO-10, CLO-12, CLO-14 |

- Each set: 3 cases, 25 minutes in-lecture, closed-book reasoning then
  individual written answers.
- Cases rotate from the bank; the instructor selects per section and
  records the selection in the instructor protocol file (prevents
  cross-section leakage).
- **Set assignment weight:** counted inside Assignment marks
  (Case sets are part of the 7-assignment pool per the syllabus
  CLO matrix).

## The shared 20-point rubric (per case)

| # | Criterion | Pts | Strong answer looks like |
|---|---|---|---|
| 1 | **Problem decomposition** | 4 | Correctly separates the scenario's sub-problems (e.g., "identify attack" vs "contain" vs "verify") before answering |
| 2 | **Evidence use** | 4 | Cites the *specific* evidence items that drive each claim; ignores distractor evidence |
| 3 | **Mechanism accuracy** | 5 | Protocol/security mechanisms named correctly (no "the hacker uses DNS" vagueness) |
| 4 | **Solution quality** | 5 | Defensible action/design with reversibility or tradeoff reasoning; matches the case's scoring intent |
| 5 | **Communication** | 2 | Answer structured (claim → evidence → conclusion); ≤ the case's stated scope |
| 6 | **Tradeoff/honesty** | — | Bonus +1: names what their solution does *not* fix or an alternative they rejected and why |

*Rubric alignment note: criteria 1–6 mirror the case-solution files'
section structure (reasoning scaffold → evidence → mechanism → model
solution → tradeoffs), so instructors grade against the same skeleton
students practiced with.*

## Marking anchors

- **18–20:** the model solution's reasoning, independently reconstructed;
  distractors correctly ignored.
- **14–17:** correct mechanism + defensible solution; minor evidence
  misses.
- **10–13:** right answer, wrong/missing mechanism (the most common
  failure mode — penalized here specifically).
- **<10:** action without evidence basis; unsafe or incoherent proposal.

## Academic integrity

- Written under in-lecture conditions; the *reasoning* is the assessed
  artifact — identical conclusions with different evidence use score
  differently.
- Cases rotate termly; solutions stay in the instructor tree (leak scan
  is part of the CI gate per the roadmap).
