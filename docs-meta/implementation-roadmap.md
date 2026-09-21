# Implementation Roadmap — Network Security Course

**Document ID:** NSC-ROAD-001 · **Status:** Approved baseline · **Version:** 1.0
**Purpose:** Stage-by-stage plan to build, validate, and publish the full course.
**Cadence rule:** a phase is *complete* only when its exit criteria AND the relevant
validation gates (Requirements §9) pass with recorded observed results.

---

## 1. Phase Overview

| Phase | Scope | Key outputs | Gate focus | Status |
|---|---|---|---|---|
| **P0 — Baseline & Governance** | Repo inspection, planning docs | This doc set | V1–V4 (plan-level) | ✅ Complete (2026-09-20) |
| P1 — Scaffolding | Repo skeleton, templates, CI, Pages shell | Directory tree, workflow files, trackers | V5 scaffolding test | ◐ Started — tracker complete; skeleton/templates/CI pending |
| P2 — Module 1–2 content | L01–L08, labs 1–4, quizzes 1–2, case set A | 8 lectures, 4 labs, ≥ 25 cases | V1 partial, V3, V7, V8 | ◐ Teaching plans + student pages + speaker notes L01–L08 complete (validated); labs/quizzes/case files pending |
| P3 — Module 3–4 content | L09–L16, labs 5–8, quiz 3, assignments 1–3, midterm, case set B | 8 lectures, 4 labs, ≥ 25 cases | V1 partial, V4 (mid) | ◐ Teaching plans + student pages + speaker notes + answer key L09–L16 complete (validated); labs/quizzes/exams/case files pending |
| P4 — Module 5–6 content | L17–L24, labs 9–12, quiz 4, assignments 4–5, case set C | 8 lectures, 4 labs, ≥ 25 cases | V4 (mid) | ◐ Teaching plans + student pages + speaker notes + answer key L17–L24 complete (validated); labs/quizzes/case files pending |
| P5 — Module 7–8 content | L25–L32, labs 13–16, quiz 5, assignments 6–7, final, capstone spec, case set D | 8 lectures, 4 labs, ≥ 25 cases | V1, V2, V3 full pass | ◐ Teaching plans + student pages + speaker notes + answer keys L25–L32 complete (validated); labs/quizzes/final/capstone pack/case files pending |
| P6 — Instructor materials | Instructor manual, all speaker notes, all answer keys | Separated instructor tree | V5, V8 | ⬜ Not started |
| P7 — Publication & QA | Site build, final audit, semester dry-run | Published GitHub Pages site | V5–V8 full pass | ⬜ Not started |

## 2. Phase Details

### P1 — Scaffolding (est. effort: small)
- Create full directory skeleton per Requirements §7.1 for all 8 modules.
- Author templates: `lecture-template.md`, `lab-template.md`, `case-template.md`,
  `quiz-template.md`, `answer-key-template.md` (each with the standard front matter).
- Add `.github/workflows/ci.yml` (link check + gate scripts) and `pages.yml`
  (build `site/`, exclude `instructor/`).
- Create `docs-meta/case-study-tracker.md` with 100+ planned rows (id, module, slug,
  difficulty, status). *(Done early, 2026-09-20: 100 planned rows recorded; gate V6c passes.)*
- **Exit:** CI runs green on an empty-but-structured repo; tracker shows 100+ planned ids.

### P2 — Foundations & Threats (Modules 1–2)
- L01–L08 full lecture content per Quality Standard (Requirements §10).
- Labs 01–04 with tested command transcripts (stored under `instructor/lab-verification/`).
- Quizzes 1–2 + answer keys; case set A (≥ 25 cases: module minimums 10 + 15).
- **Exit:** Gates V1 (partial, 8 lectures), V3, V7, V8 recorded in content-inventory.

### P3 — Architecture & Cryptography (Modules 3–4)
- L09–L16 content; labs 05–08; quiz 3; assignments 1–3; midterm exam + key;
  case set B (≥ 25 cases).
- **Exit:** Gates V1 (16 lectures), V4 interim matrix recorded.

### P4 — Wireless/Cloud & Detection/VulnMgmt (Modules 5–6)
- L17–L24 content; labs 09–12; quiz 4; assignments 4–5; case set C (≥ 25 cases).
- **Exit:** Gates V1 (24 lectures), V4 interim matrix recorded.

### P5 — IR/Operations, Forensics & Capstone (Modules 7–8)
- L25–L32 content; labs 13–16; quiz 5; assignments 6–7; final exam + key;
  capstone specification, rubric, and IR simulation script; case set D (≥ 25 cases).
- **Exit:** Gates V1, V2, V3, V6 full pass (32/8/64/100+ observed and recorded).

### P6 — Instructor Materials
- `instructor/instructor-manual.md` covering all 32 lectures (timing, demo cues,
  common misconceptions, discussion prompts).
- Speaker notes for L01–L32 (Gate V8 pairing).
- Answer keys for every graded artifact (Gate V5 scan clean).
- **Exit:** V5, V8 pass with recorded results.

### P7 — Publication & Final QA
- Build and publish GitHub Pages site; verify instructor content absent.
- Full audit: all gates re-run; `content-inventory.md` updated with final observed
  results; statuses moved to `complete` only where evidence exists.
- **Exit:** site live; all gates green; inventory finalized.

## 3. Validation Gate Schedule

| Gate | First enforced | Tooling |
|---|---|---|
| V1 lecture count = 32 | P5 (full), P2–P4 partial | CI script (count `lecture-NN` files) |
| V2 module count = 8 | P5 | CI script (directory check) |
| V3 hours = 64 | P5 | CI script (front-matter sum) |
| V4 CLO coverage | P3 onward | CI script (front-matter aggregation) |
| V5 instructor separation | P1 | CI artifact scan |
| V6 ≥ 100 case studies | P5 | CI script + tracker reconciliation |
| V7 links + lab tooling | P2 onward | Link checker |
| V8 speaker-note pairing | P6 | CI path pairing |

> **Status note (session 8):** V1–V8 all enforced and green via the **seven** local
> validators (plan 20/20, teaching plans 14/14, teaching materials 18/18,
> labs 13/13, cases 8/8, assessments 8/8, **slides 8/8**). Gate V6 met (100
> cases). The presentation layer is complete: 32 lecture decks + midterm/
> final review + case showcase + 10 shared diagram assets (ADR-003, Marp +
> Mermaid; rendering untested — see `teaching/slides/README.md`). Remaining
> authored-layer work: range provisioning automation.
>
> **Status note (website session):** the publication layer is complete.
> MkDocs Material site (`site-src/`, strict-mode, search, responsive nav)
> + single Pages workflow (`.github/workflows/deploy-pages.yml`) with a
> leak-scan gate. Strict build 0 warnings; leak scan clean; 182 pages;
> W1–W8 validator green; see `docs-meta/website-qa.md`. Remaining
> authored-layer work: range provisioning automation. Deployment itself
> awaits the first authorized push (untested end-to-end by policy).
> The one-click semester calendar is also in place: config-driven generator
> (`docs-meta/generate_calendar.py` + `calendar-config.json`) producing the
> student site view, printable HTML, instructor planning view, and .ics;
> validated by `validate_calendar.py` (C1-C8). See
> `docs-meta/calendar-instructions.md`, `slide-resources.md`,
> `assessment-coverage.md`, `lab-inventory.md`, and `case-index.md`.

## 4. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Lab environments drift from written steps | Med | High | Pinned tool versions + tested transcripts (Req §11) |
| Scope creep in offensive content | Med | High | ADR-001 framing; ethics review in P2/P3 exits |
| Instructor/student leak | Low | Critical | Directory isolation + CI leak scan (Gate V5) |
| Case-study quantity shortfall | Med | Med | Tracker-first authoring (P1) with per-phase minimums |
| Pages build includes drafts | Low | Med | CI gate: only `status: complete` publishes |

## 5. Change Control

1. Normative edits (Requirements §4, §7, §9 or Architecture §3, §4, §6) require a
   version bump in **all three** governance docs in the same change set.
2. Lecture reordering or CLO changes must re-run the full gate suite and update the
   observed-results table in `content-inventory.md`.
3. No content may be deleted without a documented reason recorded in the change log
   (Mission rule 3); superseded files are archived under `docs-meta/archive/` instead.
