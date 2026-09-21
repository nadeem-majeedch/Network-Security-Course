---
artifact-type: audit-coverage-report
status: complete
instructor-only: false
audit-date: 2026-09-21
---

# Audit Coverage Report — What Was Verified, What Was Not

> **F-02 demonstrated twice during this audit:** this file was overwritten
> by `validate_teaching_plans.py` (which writes to this exact path) both
> during evidence gathering and again during the closing regression loop.
> Restored both times; the remediation in findings-register.md stands as
> necessary, not hypothetical. The teaching-plan report's verdict is
> preserved verbatim in `validation-summary.md` §9.

Distinguishes **EXECUTED** (command run, output observed in this audit),
**HISTORICAL** (green result from a validator whose run this audit
re-confirmed), **UNVERIFIED** (claimed elsewhere, not re-proven here), and
**NOT-RUN** (impossible or out of scope in this environment).

## 1. Executed in this audit (with observed results)

| Check | Method | Observed result |
|---|---|---|
| 9 validators | `python docs-meta/validate_*.py` ×9 (venv Python) | all exit 0: plan PASS, teaching plans 14/14, materials 18/18, labs 13/13, cases 8/8 (100/100, tiers 20/25/30/25), assessments A1–A8, slides S1–S8, site W1–W8, calendar C1–C8 |
| Strict site build | `mkdocs build --strict` (twice) | 0 warnings, exit 0 |
| Leak scan on output | grep over `site/` for 7 instructor-marker patterns | CLEAN |
| Built page count | `find site -name index.html \| wc -l` | 183 |
| Structure counts | 14 file-glob counts (plans, pages, notes, keys, labs, cases, solutions, quizzes, assignments, slides, diagrams, manual, qbank, exams) | all match claimed values (validation-summary §1) |
| CLO coverage matrix | independent script over 9 artifact classes × CLO-1..15 | all 15 CLOs in plans/pages/labs/quizzes/cases/slides/exams; zeros only in assignments (single-CLO anchoring by design) + speaker notes (F-06); CLO-5 zero in labs (F-05) |
| Repo-wide md links | script over all *.md excluding site/ + venv: 461 link targets resolved | 0 broken |
| Case→solution links | script: 100 `instructor-solution:` references checked | 100 resolve |
| Answer-key flags | script: all `instructor/answer-keys/*.md` front matter | 100% `instructor-only: true` |
| Answer-key completeness (spot) | manual read: quiz-01 key (8/8 Qs, section totals 5+3+3+4=15), midterm key (20+30+30+20=100, band descriptors present), final key structure | consistent |
| Workflow anatomy | grep: permissions, pages:write, id-token:write, upload/deploy steps, strict build, calendar step, single workflow | all present |
| Safety pattern scan | grep over student-facing trees for operational tool invocations (aircrack/hydra/mimikatz/masscan/reverse shells/…), filtered for negation contexts | 0 hits |
| Lab authorization language | grep "authoriz" per lab handout | 16/16 contain it |
| Technical spot-checks | read TLS (L14), TCP (L03), IPsec (L15), SYN backlog (L03/quiz key), cs-018 evidence table | claims correct: TLS 1.2=2-RTT/1.3=1-RTT/0-RTT replayable; FIN/ACK vs RST; AH integrity-only + NAT-incompatible; half-open backlog fills |
| Cross-artifact consistency probes | graded-practical sets (6 artifacts), qa-page counts, workflow deps, syllabus vs config | **F-01 conflict confirmed; F-03 stale count confirmed; F-04 unpinned deps confirmed; F-02 collision observed twice** |
| Accessibility (code level) | grep built HTML: `lang`, skip-link, aria-labels | present (Material supplies the full ARIA set) |
| DS/CS relevance | grep lectures+cases for DS-environment terms | 30 files; dedicated instructor-manual guide exists |
| References presence | per-student-page reference-section grep | 32/32 |
| Lab tested/untested labels | grep docs/labs | only 2/16 (→ F-09) |

## 2. Re-confirmed historical (validator) claims — trusted, not re-implemented

- Marks arithmetic across 16 quizzes + 2 exams + 7 assignments
  (validate_assessments A2/A7 re-run green this audit; the arithmetic was
  not independently recomputed question-by-question here beyond the spot
  reads).
- Question-bank generation determinism (generator re-run not performed;
  bank files present and A6-checked).
- C1–C8 calendar freshness checks passed at audit time.

## 3. NOT-RUN / UNVERIFIED (explicit scope limits)

| Item | Why not run | Residual risk |
|---|---|---|
| Live lab execution (16 handouts' commands) | no lab range/VMs in environment | untested instructions (F-08); first delivery will surface friction |
| Slide rendering (Marp/Mermaid) | no Node/npm toolchain | visual defects invisible to structure checks (F-07) |
| Deployed-site behavior | no push allowed; no network deploy | workflow's deploy job unproven end-to-end (F-15) |
| Screen-reader / contrast / keyboard audit | no browser or assistive toolchain here | conformance claims not supportable (F-12) |
| External URL liveness (references) | bulk network fetching out of scope for this audit | dead links possible (F-13) |
| Full technical review of all 32 lectures | effort-bounded audit; spot-check strategy chosen | subtle claim errors may exist (F-11) |
| Negative-case validator self-tests | out of audit budget | false-negative rate unknown (F-14) |
| LMS integration, university-specific policy compliance | no LMS/policy artifacts exist in repo | out of scope entirely |

## 4. Area-by-area coverage map

| Audit area | Coverage level |
|---|---|
| 1 structure | EXECUTED (counts + validators) |
| 2 syllabus | EXECUTED (read + conflict probe) |
| 3 CLO mapping | EXECUTED (independent matrix) |
| 4 lecture plans | HISTORICAL (validators) + spot reads |
| 5 teaching notes | HISTORICAL + presence counts |
| 6 instructor manual | EXECUTED (file inventory) |
| 7 labs | HISTORICAL + authorization/safety greps; commands NOT-RUN |
| 8 case studies | HISTORICAL + 100 link checks |
| 9 assessment package | HISTORICAL + key spot reads + F-01 finding |
| 10 slides/notes | HISTORICAL; rendering NOT-RUN |
| 11 website | EXECUTED (build, leak scan, counts) |
| 12 workflow | EXECUTED (anatomy); deploy NOT-RUN |
| 13 internal links | EXECUTED (461 links, 0 broken) |
| 14 technical accuracy | SPOT-VERIFIED (5 claim clusters); full review NOT-RUN |
| 15 ethics/safety | EXECUTED (pattern scans + labeling checks) |
| 16 accessibility | PARTIAL (code-level only) |
| 17 references | PARTIAL (presence + currency of editions; URLs not fetched) |
| 18 CS/DS relevance | EXECUTED (density + dedicated guide) |
| 19 assessment coverage | EXECUTED (matrix + A-checks + F-01) |
| 20 calendar | HISTORICAL (C1–C8 re-run) + config conflict probe |
