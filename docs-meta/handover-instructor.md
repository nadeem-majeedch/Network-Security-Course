---
artifact-type: instructor-handover-guide
status: complete
instructor-only: false
handover-date: 2026-09-21
---

# Instructor Handover Guide

Everything an adopting instructor needs to review, set up, and deliver the
course. Read together with `final-validation-report.md` (what was verified)
and `known-limitations.md` (what still needs human attention).

## 1. Review the package in this order (half a day)

| Step | What | Where | Time |
|---|---|---|---|
| 1 | Course shape | `syllabus/syllabus.md` (CLOs, calendar, grading) | 30 min |
| 2 | Sample a full week | Teaching plan + student page + speaker notes + slides for L05–L06 | 45 min |
| 3 | Sample a lab | `docs/labs/lab-06-*.md` + its key in `teaching/lab-answer-keys/` | 30 min |
| 4 | Run two cases live | `modules/module-02-*/case-studies/cs-011-*.md` + solution | 30 min |
| 5 | Skim the exams | `assessments/midterm/`, `assessments/final/` (+ keys) | 30 min |
| 6 | Build the site locally (commands in the root `README.md`) | — | 20 min |
| 7 | Skim validation & audit reports | `docs-meta/final-validation-report.md`, `final-course-audit.md` | 20 min |

## 2. Semester setup (one sitting)

1. **Set the calendar:** edit `docs-meta/calendar-config.json` —
   `semester.start_date` (Monday of week 1), lecture days, holiday
   `overrides`. Run `python docs-meta/generate_calendar.py`. This refreshes
   the student calendar page, the printable HTML, the instructor planning
   view, and emits `calendar.ics`.
2. **Verify the graded practicals** match your section plan: Pract-1–4 =
   Labs 06/07/10/11 (weeks 6/7/10/11) — enforced by validator check C9.
3. **Pick the case rotations** for graded Sets A/B/C and record them in
   `assessments/case-study-evaluation/` per the protocol (prevents
   cross-section leakage).
4. **Provision the lab range** — the one genuinely outstanding build item
   (`known-limitations.md` §2). Then execute each lab once before delivery
   and update the per-step ✅/⚠️ status markers in the handouts.

## 3. Delivery workflow per week

- Teaching plan (`modules/module-0N-*/lectures/`) is the master script:
  timing, demos, expected difficulties, case anchor.
- Slides (`teaching/slides/lecture-NN-*.md`) render with Marp:
  `npx @marp-team/marp-cli <deck>.md -o out.html` (rendering toolchain not
  included in this repo — see `teaching/slides/README.md`).
- Speaker notes pair 1:1 with decks; the misconception bank and
  facilitation guides live in `teaching/instructor-manual/`.
- Quizzes/self-checks release per the calendar; keys are in
  `instructor/answer-keys/`. **Never** copy key material into anything
  student-facing — the CI leak-scan gate blocks the site build if you do.

## 4. Answer-key map (instructor-only trees)

| Keys | Location |
|---|---|
| Quizzes, assignments, exams | `instructor/answer-keys/` |
| Module exit tickets / formative | `teaching/answer-keys/` |
| Labs (incl. Pract rubrics) | `teaching/lab-answer-keys/` |
| Case model solutions | `teaching/case-solutions/` |
| Capstone rubric bands | `instructor/answer-keys/capstone-rubric-bands.md` |

## 5. Publication to GitHub Pages (manual, verified-by-human)

1. Review the built site once locally (`mkdocs build --strict`, then
   `mkdocs serve` and click through Home → Modules → a lecture → a lab → a
   case).
2. On GitHub: **Settings → Pages → Build & deployment → Source: GitHub
   Actions**.
3. Commit and push to `main` (this session made no commits, by instruction).
4. Watch the *Deploy site to GitHub Pages* workflow run to green.
5. **Verify the live URL yourself** — `https://nadeem-majeedch.github.io/Network-Security-Course/`
   — and confirm: home loads, search works, a lecture page renders its
   diagrams, and `/about/qa-report/` is present. Deployment has **not** been
   exercised end-to-end yet; the first real run is yours to verify.

## 6. If something looks wrong

- Re-run the validators (commands in the root `README.md`) — they localize
  most issues to a file and check.
- Check `docs-meta/findings-register.md` for known-issue history, and
  `docs-meta/known-limitations.md` for open items.
- The calendar and site regenerate from sources: fix the source, rerun the
  generator — never edit generated outputs by hand.
