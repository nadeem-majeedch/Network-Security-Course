---
artifact-type: instructor-manual-index
status: complete
instructor-only: true
distribution: never-publish-to-students
---

# Instructor Manual — Network Security (NS-401)

## How this manual is organized

| File | Contents |
|---|---|
| `delivery-guide.md` | Global delivery guide, session anatomy, suggested-timing philosophy, semester rhythm, assessment logistics |
| `demonstrations-and-difficulties.md` | Consolidated teaching-demonstration index, expected student difficulties by module, **misconception bank** (32-lecture scope) |
| `facilitation-and-troubleshooting.md` | Discussion facilitation playbook, lab troubleshooting compendium, escalation rules |
| `model-answers-index.md` | Where model answers live (per-module answer keys), grading philosophy, rubric anchors |
| `accessibility.md` | Accessibility guidance: universal design, accommodations menu, per-activity adaptations |
| `cs-ds-applications.md` | CS-track and Data-Science-track application maps for every module |

## Where per-lecture detail lives

The manual is the **global layer**. Per-lecture specifics live in:

- **Timing plans, demos, difficulties, facilitation, troubleshooting, accessibility, CS/DS notes** → `teaching/speaker-notes/lecture-NN-speaker-notes.md` (all 32 lectures)
- **Model answers** → `teaching/answer-keys/answer-key-module-01…08.md`
- **Full lesson structure** → `modules/module-0N-*/lectures/lecture-NN-*.md` (teaching plans)
- **Student-facing pages** → `docs/lectures/lecture-NN-*.md` (never contains answers)

## Coverage map — mission requirements → locations

| Instructor-manual requirement | Primary location | Per-lecture detail |
|---|---|---|
| Lecture delivery guide | `delivery-guide.md` | Speaker notes §Delivery Guide |
| Suggested timing | `delivery-guide.md` §2 | Speaker notes §Timing Plan |
| Speaker notes | (this set) | `teaching/speaker-notes/` (32 files) |
| Teaching demonstrations | `demonstrations-and-difficulties.md` §1 | Speaker notes §Teaching Demonstrations |
| Expected student difficulties | `demonstrations-and-difficulties.md` §2 | Speaker notes §Expected Student Difficulties |
| Misconception bank | `demonstrations-and-difficulties.md` §3 | Answer keys §misconceptions |
| Discussion facilitation | `facilitation-and-troubleshooting.md` §1 | Speaker notes §Discussion Facilitation |
| Lab troubleshooting | `facilitation-and-troubleshooting.md` §2 | Speaker notes §Lab Troubleshooting |
| Model answers | `model-answers-index.md` | `teaching/answer-keys/` (8 files) |
| Accessibility guidance | `accessibility.md` | Speaker notes §Accessibility Notes |
| CS & Data Science applications | `cs-ds-applications.md` | Speaker notes §CS & Data Science Applications |

## Distribution rule

Everything under `teaching/` is **instructor-only**. The GitHub Pages build and
any student-facing export must exclude this tree (enforced by the Pages workflow
plan; see `docs-meta/course-requirements.md` §7 and the roadmap's P1 gate).
Student-facing material lives in `docs/lectures/` and `syllabus/` only.
