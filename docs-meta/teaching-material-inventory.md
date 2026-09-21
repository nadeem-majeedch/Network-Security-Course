---
artifact-type: teaching-material-inventory
status: complete
instructor-only: false
last-updated: session 4 (teaching materials + instructor manual)
---

# Teaching Materials Inventory

Record of the teaching-material layer built this session, its validation
results, and the remaining gaps. This document is the honest status ledger for
`docs/lectures/`, `teaching/instructor-manual/`, `teaching/speaker-notes/`,
and `teaching/answer-keys/`.

## 1. What exists now (73 files this session)

### Student-facing lecture material — `docs/lectures/` (33 files)
| Artifact | Count | Status |
|---|---|---|
| Student lecture pages `lecture-01…32-*.md` | 32 | complete — each carries the 12 mandated elements: detailed explanations, key definitions, network diagram, protocol examples, configuration concepts, security implications, realistic organizational scenario, common misconceptions, classroom activities, problem-solving questions, exit ticket, references, CLO mapping (13 numbered sections + "Why This Lecture Exists") |
| Index `README.md` | 1 | complete — module-grouped table linking every page |

### Instructor-only material — `teaching/` (40 files)
| Artifact | Count | Status |
|---|---|---|
| Speaker notes `speaker-notes/lecture-01…32-speaker-notes.md` | 32 | complete — delivery guide, timing plan (with compression guidance), teaching demonstrations, expected student difficulties, discussion facilitation, lab troubleshooting, accessibility notes, CS/DS applications, links |
| Answer keys `answer-keys/answer-key-module-01…08.md` | 8 | complete — per-lecture formative-check model answers, exit-ticket answers, discussion facilitation verdicts, case-study grading anchors, module misconception banks; Module 8 additionally anchors the capstone defense rubric |
| Instructor manual `instructor-manual/` | 7 | complete — README index, global delivery guide (session anatomy, semester rhythm, assessment logistics), demonstrations/difficulties + course-wide misconception bank, facilitation & lab-troubleshooting compendium, model-answers index + grading philosophy + rubric anchors, accessibility guidance (baseline + accommodations menu), CS/DS track maps |

### Validation tooling — `docs-meta/validate_teaching_materials.py`
18 executable checks (T1–T9), exit code 0 required.

## 2. Validation — actual observed results (not asserted)

Final run: **18/18 checks PASS, exit code 0** (`python docs-meta/validate_teaching_materials.py`):

| Check | Requirement | Observed |
|---|---|---|
| T1a–c | All 32 lectures have substantive notes | 32 notes, L01–L32, no gaps, no duplicate numbering ✅ |
| T2a–b | Notes substantive | All 9 delivery sections present in every note; ≥40 body lines each ✅ |
| T3a–b | Answer keys complete | 8 keys; each covers its module's 4 lectures with formative checks, exit tickets, misconception sections ✅ |
| T4a–b | Manual covers all mandated elements | All 7 files present; all 11 required elements (delivery guide, timing, speaker notes, demos, difficulties, misconception bank, facilitation, lab troubleshooting, model answers, accessibility, CS/DS) located ✅ |
| T5a–b | Instructor/student separation | Every `teaching/` file carries `instructor-only: true`; zero instructor-only markers in `docs/lectures/` or `syllabus/` ✅ |
| T6a–c | Student pages complete | 32 pages, L01–L32, `status: complete`, `artifact-type: student-lecture-material`, plan links resolve, all 13 required sections present ✅ |
| T7 | No placeholder-only pages marked complete | Zero TODO/TBD/FIXME/PLACEHOLDER markers in any complete page ✅ |
| T8a–b | References + CLO mapping | ≥3 reference lines and CLO-\d+ mapping in every student page ✅ |
| T9 | Note links resolve | Every `modules/…`, `docs/…`, `teaching/…` path in note Links sections exists ✅ |

**First-run failures and triage (2 real content gaps, fixed same session):**
1. `T3b: answer-key-module-02.md missing misconception section` — the Module 2
   key lacked its misconception bank. Fixed: bank added (4 entries: tool-vs-
   mechanism, sniffing visibility, DDoS response layer, recon legality).
2. `T6c: L02 section heading deviation` — L02's scenario section was headed
   "Organizational Scenario" instead of the template's "Realistic Organizational
   Scenario". Fixed: heading aligned to template.

Prior gates re-verified after these fixes: `validate_plan.py` PASS (exit 0),
`validate_teaching_plans.py` PASS (exit 0). All three validators green.

## 3. Relationship to repo conventions

The mission for this session named a `docs/lectures/` + `teaching/` layout;
the repo's §7.1 conventions (in `course-requirements.md`) place student pages
under `docs/` and instructor material under a separate tree — this layout
satisfies both: `docs/lectures/` is student-facing (Pages-included),
`teaching/` is instructor-only (Pages-excluded, enforced as gate V5/T5).
Cross-links (`instructor-plan:` front-matter on every student page; Links
sections on every note) bind the three layers per lecture.

## 4. Remaining gaps (honest ledger — nothing here is claimed complete)

| Gap | Phase | Notes |
|---|---|---|
| 16 lab packages (worksheets, datasets, solution walkthroughs) | P3 | Referenced by plans and notes; not yet authored |
| Quizzes ×5, midterm, final (+ answer keys) | P3/P4 | Not yet authored |
| Assignments A1–A5 (+ model answers) | P3/P4 | Not yet authored |
| Case-study files cs-001–cs-100 (full writeups) | P3 | Tracker exists; case files pending |
| Capstone project pack (team charter, datasets, rubric pack) | P5 | Rubric anchor exists in Module 8 key; pack pending |
| GitHub Pages build + CI workflows (with `teaching/` exclusion) | P1/P6 | Not yet authored |
| Slide decks / visual assets | P6 | Diagrams exist as text/ASCII; image assets pending |

## 5. Change log — session 4

- Created 32 student lecture pages + README index (`docs/lectures/`).
- Created 32 speaker notes (`teaching/speaker-notes/`).
- Created 8 module answer keys (`teaching/answer-keys/`).
- Created 7-file instructor manual (`teaching/instructor-manual/`).
- Created `docs-meta/validate_teaching_materials.py` (18 checks).
- Fixed 2 validator-detected gaps (Module 2 misconception bank; L02 heading).
- No commits, no pushes (repo still has zero commits; all files untracked).
