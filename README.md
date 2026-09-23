# Network Security Course

A complete, university-level **Network Security** course for
**BS Computer Science / BS Data Science** students (7th semester):
**16 weeks · 32 lectures × 2 h (64 contact hours) · 8 modules · 16 labs ·
100 case studies · full assessment layer · capstone with oral defense ·
MkDocs Material website with one-click GitHub Pages deployment.**

Every security control in the course is grounded in the protocol it
protects. All scenarios are simulated and labeled as such; all practical
work targets an isolated, authorized lab range; instructor answer-key
material is kept in separate trees and never published to the site.

## Repository map

| Path | Contents |
|---|---|
| `syllabus/` | Full syllabus: CLOs, calendar, grading, policies |
| `modules/module-0N-*/lectures/` | 32 instructor teaching plans |
| `modules/module-0N-*/case-studies/` | 100 student case studies (solutions in `teaching/case-solutions/`) |
| `docs/lectures/` | 32 student lecture pages |
| `docs/labs/` | 16 lab handouts (+ dataset generator in `docs/labs/setup/`) |
| `assessments/` | Quizzes, assignments, exams, capstone, question bank, case-evaluation rubric |
| `teaching/` | Speaker notes, instructor manual, slides (Marp), answer keys (instructor-only) |
| `instructor/answer-keys/` | Quiz/assignment/exam answer keys (instructor-only) |
| `site-src/` + `mkdocs.yml` | Student-facing website source (MkDocs Material) |
| `.github/workflows/deploy-pages.yml` | GitHub Pages deployment (build + leak-scan gate) |
| `docs-meta/` | Governance: inventories, ADRs, validators, calendar tooling, audits |

## Quickstart

### Run the quality gates

```bash
python -m pip install mkdocs-material mkdocs-minify-plugin   # or: python -m venv .venv-mkdocs
python docs-meta/validate_plan.py && python docs-meta/validate_teaching_plans.py
python docs-meta/validate_teaching_materials.py && python docs-meta/validate_labs.py
python docs-meta/validate_cases.py && python docs-meta/validate_assessments.py
python docs-meta/validate_slides.py && python docs-meta/validate_site.py
python docs-meta/validate_calendar.py
```

All nine must exit 0. `validate_site.py` additionally requires a built `site/`.

### Build the website locally

```bash
python docs-meta/build_site_content.py    # copy student content into site-src/
python docs-meta/generate_calendar.py     # regenerate semester calendar views
mkdocs build --strict                     # zero warnings expected
mkdocs serve                              # preview at http://127.0.0.1:8000
```

### Configure the semester calendar

Edit `docs-meta/calendar-config.json` (`semester.start_date`, lecture days,
holiday overrides), then rerun `generate_calendar.py`. With a start date
set, a `calendar.ics` (32 events) is emitted. Details:
`docs-meta/calendar-instructions.md`.

### Publish to GitHub Pages

1. Repository **Settings → Pages → Source: GitHub Actions**.
2. Push to `main` (or run the *Deploy site to GitHub Pages* workflow
   manually). The workflow builds strictly, leak-scans the output, and
   deploys via the official Pages action.
3. First deployment must be verified by a human — see
   `docs-meta/handover-instructor.md` for the checklist.

## Quality system

- **Nine validators** cover structure, teaching plans, materials, labs, cases,
  assessments, slides, the site, the calendar, and cross-artifact
  consistency — all currently green (see `docs-meta/final-validation-report.md`).
- **Independent QA audit** with evidence: `docs-meta/final-course-audit.md`
  and `findings-register.md` (fixed findings marked RESOLVED; open items in
  `known-limitations.md`).
- Instructor separation is enforced by construction (key trees live outside
  `docs_dir`) and verified by a leak-scan gate in CI.

## License & use

Course materials for teaching use. All incidents, organizations, and
telemetry in examples, labs, and cases are **simulated fiction**. Techniques
are taught defensively and practiced only in the authorized lab range..
