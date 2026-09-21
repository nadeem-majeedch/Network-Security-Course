---
artifact-type: final-validation-report
status: complete
instructor-only: false
handover-date: 2026-09-21
scope: post-fix handover regression (all commands executed in this session)
---

# Final Validation Report (Handover)

Every result below is from a command executed during the handover session,
after the audit fixes. Raw per-check evidence: `validation-summary.md`
(audit session) and the validator outputs quoted here.

## 1. Handover requirements — confirmed with actual counts

| Requirement | Result | Evidence (executed) |
|---|---|---|
| 32 lectures | **CONFIRMED** | `ls modules/*/lectures/lecture-*.md \| wc -l` → 32; student pages → 32; slides → 32; speaker notes → 32 |
| 64 total hours | **CONFIRMED** | 32 × 2 h front-matter `hours: 2` on all plans; calendar = 16 weeks × 2 lectures (validator C1/C2) |
| Eight modules | **CONFIRMED** | 8 `modules/module-0N-*/` trees; 8 site module pages; validators green |
| Lecture notes & instructor resources | **CONFIRMED** | 32 speaker notes paired 1:1; instructor manual 7 files (delivery, demos/difficulties, facilitation/troubleshooting, model-answers index, accessibility, CS/DS); answer keys 8 module + 16 lab + 16 quiz + 7 assignment + exam keys |
| Practical labs | **CONFIRMED** | 16 handouts; 16 answer keys; per-step ✅/⚠️ status legend on 16/16; dataset generator present; validate_labs 13/13 |
| 100+ progressive case studies | **CONFIRMED** | 100 cases + 100 solutions; tiers 20/25/30/25; all solution links resolve (validate_cases 8/8) |
| Assessments | **CONFIRMED** | 16 quiz units + keys, 7 assignments + keys, midterm (100 marks) + final (100 marks) + keys, capstone brief/rubric/defense-guide, 50-question bank; validate_assessments A1–A8 green |
| Slides & speaker notes | **CONFIRMED (structure)** | 35 decks + 10 diagrams; validate_slides green. **Rendering NOT RUN** (no Node in environment) |
| Website & deploy workflow | **CONFIRMED (build)** | `mkdocs build --strict` exit 0; 183 HTML pages; leak scan CLEAN; workflow YAML validated, deps pinned. **Deployment NOT RUN** (no push by instruction) |
| Semester calendar | **CONFIRMED** | 3 generated views; C1–C9 green incl. new practical cross-check; ICS logic verified in audit (32 events, correct span); ICS file NOT emitted now (start_date intentionally empty) |
| Documentation & references | **CONFIRMED** | README + .gitignore created; 32/32 student pages have reference sections; governance docs complete (inventory, ADRs, audits, instructions) |

## 2. Validators — executed post-fix (all green)

```
validate_plan.py               exit 0  all plan-level checks PASSED
validate_teaching_plans.py     exit 0  report -> teaching-plans-coverage.md (renamed this session)
validate_teaching_materials.py exit 0  18/18
validate_labs.py               exit 0  13/13
validate_cases.py              exit 0  100/100, tiers 20/25/30/25, separation clean
validate_assessments.py        exit 0  A1..A8 (59 artifacts, marks arithmetic, keys, CLOs, Bloom, weights)
validate_slides.py             exit 0  32+3 decks + README; structure all verified
validate_site.py               exit 0  W1-W8 (post-fix tree)
validate_calendar.py           exit 0  C1-C9 (C9 = new graded-practical cross-artifact check, PASS)
```

## 3. Build & safety gates — executed post-fix

```
mkdocs build --strict     exit 0, zero warnings, 183 HTML pages
leak scan on site/        CLEAN (7 instructor-marker patterns, incl. search index)
```

## 4. Fixes applied this session (verified by re-run)

| Finding | Fix | Verification |
|---|---|---|
| F-01 HIGH | Graded practicals unified to Labs 06/07/10/11 (config, labs page, assessment page); calendar regenerated | New validator check C9 PASSes; pre-fix config would FAIL it |
| F-02 | Teaching-plan validator output renamed to `teaching-plans-coverage.md` | Re-run shows new path; no more collision |
| F-03 | Internal ledger counts refreshed; floor-check formulation adopted | Ledger states 183 + floor check; public page never carried counts |
| F-04 (partial) | Workflow Python deps pinned (`mkdocs-material==9.7.7`, `mkdocs-minify-plugin==0.8.0`) | grep on workflow; action SHAs remain major-tag (documented) |
| F-05 | Lab-07 `clos:` → `[CLO-5, CLO-6]` | validate_labs green post-change |
| F-09 | **RETRACTED** — labs already carry a per-step ✅/⚠️ status system; audit grep was too narrow | Re-check: 16/16 legends, 16/16 with step markers; no content changed |
| F-10 | `README.md` + `.gitignore` created | Files present at repo root |

## 5. NOT RUN (explicit — do not assume otherwise)

- **GitHub Pages deployment** — no commit/push made (by instruction); the
  workflow's deploy job has never executed. Publication is a manual,
  human-verified step (handover-instructor.md §5).
- **Marp/Mermaid slide rendering** — no Node/npm toolchain in this
  environment.
- **Live lab execution** — no lab range/VMs provisioned here; handout
  commands are concept-verified with per-step status markers, not executed.
- **Screen-reader / contrast / keyboard accessibility audit** — code-level
  checks only (lang, skip-link, aria, one-H1, anchors).
- **External reference URL liveness** — editions verified current; URLs not
  fetched.
- **Exhaustive second technical review of all 32 lectures** — spot-checks
  passed; full pass still recommended (see known-limitations).

## 6. Verdict

The package is **handover-ready for instructor review**: complete,
internally consistent (all nine validators + build + leak scan green after
fixes), with one corrected HIGH finding and an audited, honest record of
what remains manual.
