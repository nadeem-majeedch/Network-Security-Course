---
artifact-type: final-course-audit
status: complete
instructor-only: false
audit-date: 2026-09-21
method: evidence-based (every verdict backed by an executed check or explicitly marked unverified/not-run)
---

# Final Course Audit — Network Security Course

Independent QA audit of the complete course package. Executed commands and
raw outputs: `docs-meta/validation-summary.md`. Per-finding detail (severity,
evidence, impact, remediation): `docs-meta/findings-register.md`. Which audit
areas were verified vs. not: `docs-meta/coverage-report.md`.

**Verdict snapshot: 1 HIGH, 5 MEDIUM, 4 LOW, 8 INFORMATIONAL findings.
No CRITICAL defects. The package is structurally complete and validated;
the defects are consistency, operations, and shipping issues, not missing
content.**

## Verdicts by review area

| # | Area | Verdict | Basis |
|---|---|---|---|
| 1 | Course structure | **Verified, PASS** | All 9 validators exit 0; counts: 32/32 lecture plans & student pages, 32 speaker notes, 16/16 labs & keys, 100/100 cases & solutions, 16/16 quiz units & keys, 7/7 assignments & keys, exams + capstone pack, 35 decks + 10 diagrams, 7-file instructor manual (structure table in validation-summary §1) |
| 2 | Syllabus | **Verified, 1 MEDIUM** | Present and complete (calendar, weights, policies); graded-practical set conflicts with two other artifacts (F-01) |
| 3 | CLO mapping | **Verified, PASS with notes** | Matrix computed over 9 artifact classes: all 15 CLOs taught (plans), practiced (labs), and assessed (≥3 assessment types); notes: CLO-5 no dedicated lab (MEDIUM-low, F-05); speaker notes intentionally carry no CLO tags (INFO, F-06) |
| 4 | 32 lecture plans | **Verified, PASS** | validate_plan + validate_teaching_plans green (structure + syllabus alignment); spot-checks of L14/L15/L30 confirmed accurate prerequisites, positions, CLO mapping |
| 5 | Teaching notes | **Verified, PASS** | 32/32 speaker notes; validate_teaching_materials 18/18 (timings, misconceptions, accessibility, CS/DS apps) |
| 6 | Instructor manual | **Verified, PASS** | 7 files cover delivery guide, demonstrations/difficulties, facilitation/troubleshooting, model-answers index, accessibility, CS/DS applications |
| 7 | Practical labs | **Verified, 1 MEDIUM** | 16 handouts, all with authorization language; commands conceptually verified only — none executed in a live range (F-08); 2/16 handouts carry tested/untested labels (F-09); graded-practical conflicts (F-01) |
| 8 | Case studies | **Verified, PASS** | validate_cases: 100 cases, tiers 20/25/30/25, all elements, separation; all 100 `instructor-solution:` links resolve |
| 9 | Assessment package | **Verified, 1 HIGH** | validate_assessments A1–A8 green (arithmetic, keys, Bloom, weights); **but the graded-practical set is stated three different ways across five artifacts (F-01)** |
| 10 | Slides & speaker notes | **Verified, 1 MEDIUM** | validate_slides green; rendering untested — no Marp toolchain in environment (F-07) |
| 11 | Website | **Verified, 1 MEDIUM** | Strict build clean, 183 HTML pages, leak scan clean, W1–W8 green; public QA-report page carries a stale page count (F-03) |
| 12 | GitHub Pages workflow | **Verified, 1 MEDIUM** | YAML valid, permissions correct, official actions; **unpinned dependency versions (F-04)**; end-to-end deploy untested by policy (F-10) |
| 13 | Internal links | **Verified, PASS** | 461 markdown links checked repo-wide (excl. `site/`, venv): **0 broken**; site nav reachability green |
| 14 | Technical accuracy | **Spot-verified, PASS** | Probed claims correct: TLS 1.2=2-RTT/1.3=1-RTT, 0-RTT replayability, TCP FIN/RST teardown semantics, IPsec AH-vs-ESP + NAT incompatibility, SYN backlog mechanics; full technical review NOT performed (F-11) |
| 15 | Ethics & safety | **Verified, PASS** | Pattern-based scan of student-facing trees found no operational tool invocations (aircrack/hydra/mimikatz/masscan/reverse shells); all 16 labs contain authorization language; simulated-fiction labeling enforced by validators |
| 16 | Accessibility | **Partially verified** | Site: `lang`, skip-link, aria-labels verified in built HTML; one-H1-per-page + anchors validated. **No screen-reader or contrast-tool run** (F-12); no WCAG conformance claim possible |
| 17 | References | **Verified, PASS with note** | All 32 student pages carry reference sections; standards cited are current editions (RFC 9293, SP 800-207, TLS 1.3). URLs NOT fetched/live-checked (F-13) |
| 18 | CS & DS relevance | **Verified, PASS** | 30 files across lectures/cases reference DS environments (GPU clusters, notebooks, pipelines); instructor manual has a dedicated CS/DS applications guide |
| 19 | Assessment coverage | **Verified, 1 HIGH** | A1–A8 green (CLO-1..15 ≥3 assessment types; marks arithmetic verified; Bloom complete); undermined by the F-01 practical-set conflict |
| 20 | Semester calendar | **Verified, PASS with note** | C1–C8 green (16 weeks, 32 lectures, alignment vs independent re-parse, links); config-vs-syllabus conflict feeds F-01; calendar validator itself untested against a broken calendar (F-14) |

## Headline findings (full detail in findings-register.md)

- **F-01 (HIGH) — Conflicting graded-practical sets.** Site labs page: Labs
  02/06/12/16 · syllabus + static calendar + coverage report: Pract-1–4 =
  W6/W7/W10/W11 (Labs 06/07/10/11) · calendar config + generated views:
  Labs 06/07/10/16. Three different sets, three different Pract→Lab
  assignments. Affects grading fairness and the 20% weight integrity.
- **F-02 (MEDIUM) — Validator output-path collision.**
  `validate_teaching_plans.py` writes `docs-meta/coverage-report.md`,
  clobbering any audit coverage report of the same name (observed live
  **twice** during this audit: during evidence gathering and again in the
  closing regression loop after restoration — reproduced, not
  hypothetical).
- **F-03/F-04 (MEDIUM) — Ship-shape issues.** Stale page count on the
  public QA page; workflow dependencies unpinned (`pip install` floats,
  actions @ major tags).
- **F-05…F-09 (MEDIUM/LOW)** — CLO-5 has no dedicated lab; labs lack a
  systematic tested/untested label; no top-level README/.gitignore (LOW);
  slide rendering untested (documented).
- **No CRITICAL findings**: nothing broken for a student, no answer-key
  leakage, no broken links, no marks-arithmetic errors, no fabricated
  results detected.

## What was NOT audited (honest scope)

See coverage-report.md §3 for the full list: live lab execution, Marp
rendering, deployed-site behavior (no push), screen-reader/contrast runs,
external URL liveness, full technical review of all 32 lectures, quiz
answers verified beyond quiz-01/midterm/final spot-checks, validator
self-testing (negative cases).
