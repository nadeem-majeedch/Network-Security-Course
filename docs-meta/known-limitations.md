---
artifact-type: known-limitations
status: complete
instructor-only: false
handover-date: 2026-09-21
related: findings-register.md (full history), final-validation-report.md
---

# Known Limitations (Handover State)

What this package honestly does **not** include or prove, and what the
adopting instructor should do about each. Fixed findings are not repeated
here — see `findings-register.md`.

## 1. Unproven execution (highest awareness value)

| # | Limitation | Impact | Owner action |
|---|---|---|---|
| L-1 | **Deployment never exercised end-to-end.** The Pages workflow is structurally valid and its build job's steps ran locally, but no push has been made, so `deploy-pages` has never run. | First real deploy is the first real test. | Follow handover-instructor.md §5; verify the live URL personally; keep the local build as fallback. |
| L-2 | **Slides never rendered.** 35 Marp decks + 10 Mermaid diagrams are structurally validated only; no Node toolchain existed. | First render may show overflow/spacing issues invisible to structure checks. | Render L01 first (`npx @marp-team/marp-cli`), then batch; record results in `teaching/slides/README.md`. |
| L-3 | **Labs never executed in a live range.** Handouts are concept-verified with per-step ✅/⚠️ markers; the range itself is unprovisioned (the roadmap's last remaining authored-layer item). | First delivery of each lab will surface environment friction. | Provision the range; run each lab once before delivery; update handout markers; record deviations in `lab-inventory.md`. |

## 2. Open findings from the audit (low severity)

| # | Finding | Impact | Owner action |
|---|---|---|---|
| L-4 | **F-04 residual:** GitHub Actions pinned at major tags (`@v4/@v5`), not SHAs. | Supply-chain exposure to tag retargeting; low practical risk for a course repo. | Pin SHAs before production adoption or enable Dependabot. |
| L-5 | **F-11:** technical accuracy spot-verified (5 claim clusters, all correct), not exhaustively re-reviewed across all 32 lectures. | Residual risk of a subtle protocol claim error. | Schedule a second-pass review, M1–M4 first (densest protocol content). |
| L-6 | **F-12:** accessibility verified at code level only (lang, skip-link, aria, one-H1, anchors). No WCAG conformance claim. | Standard claims supportable; conformance claims not. | Run axe/Lighthouse on the built site; keyboard-only walkthrough; record results. |
| L-7 | **F-13:** reference URLs not liveness-checked (editions verified current). | Possible dead links in reference shelves. | Scripted HEAD-check of external links; fix 404s. |
| L-8 | **F-14:** validators never negative-tested in this audit (each historically caught real bugs, but detection wasn't re-proven this session). | Unknown false-negative rate. | Optional self-test harness: inject one defect per check class, assert failure. |

## 3. Structural notes (no action required)

- **Speaker notes carry no CLO tags by design** — plans and student pages
  hold the mapping; notes hold delivery craft (audit F-06).
- **Assignments map to a single primary CLO each** by design; cross-CLO
  coverage arrives via quizzes/exams/cases (matrix shows all 15 CLOs
  assessed ≥3 ways).
- **`calendar.ics` is intentionally absent** — it emits only when
  `semester.start_date` is configured (verified working in the audit's
  round-trip test).
- **Generated outputs must not be hand-edited** (`calendar-generated.md`,
  `all-cases.md`, copied pages): fix sources, rerun generators. Validators
  detect staleness (C8) and hand-edits (C2 title check).

## 4. Out of scope entirely

- LMS integration, university-specific policy documents, enrollment data,
  real student statistics (recorded post-marking only), live threat
  intelligence feeds. Nothing in the repo claims otherwise.
