---
artifact-type: findings-register
status: complete
instructor-only: false
audit-date: 2026-09-21
related: final-course-audit.md, validation-summary.md
---

# Findings Register

> **Handover update:** F-01, F-02, F-03, F-04 (partial), F-05, F-10
> RESOLVED; F-09 RETRACTED (audit false positive — see entry). Post-fix
> regression: all nine validators green. Open items feed
> `known-limitations.md`.

Severity scale: **CRITICAL** (breaks learning, leaks keys, fabricates
results) → **HIGH** (material inconsistency affecting grading/outcomes) →
**MEDIUM** (operational/quality gap with real impact) → **LOW** (minor gap,
easy fix) → **INFORMATIONAL** (documented observation, no action required
or already mitigated by design).

Findings marked *fix now* have a concrete one-session remediation.

---

## F-01 · HIGH · Conflicting graded-practical sets (Pract-1–4)

- **Evidence (executed):**
  - `site-src/labs/index.md` line 49: "Labs 02, 06, 12, 16" as the four
    heavier practicals.
  - `syllabus/syllabus.md` §7 CLO matrix: `Pract-1 (W6), Pract-2 (W7),
    Pract-3 (W10), Pract-4 (W11)` → Labs 06/07/10/11.
  - `site-src/course/calendar.md`: Assignment rows put Pract-1–4 in W6/W7
    (A2 weeks) and W10/W11 — consistent with the syllabus, not labs.md.
  - `docs-meta/assessment-coverage.md` line 48: "(+ Pract-4)" on **week 11**.
  - `docs-meta/calendar-config.json`: `"graded_practicals": {"Lab-06": 1,
    "Lab-07": 2, "Lab-10": 3, "Lab-16": 4}` → generated calendar
    (`calendar-instructor.md`) flags Lab-16 as Pract-4.
  - Student-facing exam page (`site-src/assessment/exams.md`) implies the
    final's practical is separate from lab practicals — consistent with
    both readings, resolving nothing.
- **Three sets in play:** {02,06,12,16} vs {06,07,10,11} vs {06,07,10,16}.
- **Affected files:** `site-src/labs/index.md`, `syllabus/syllabus.md`,
  `site-src/course/calendar.md`, `docs-meta/assessment-coverage.md`,
  `docs-meta/calendar-config.json`, `docs-meta/calendar-instructor.md`,
  `docs-meta/calendar-printable.html`, `site-src/course/calendar-generated.md`.
- **Impact:** students cannot know which four labs carry 20% of the grade;
  the config-driven calendar (the "single source of truth" introduced for
  the calendar) silently contradicts the syllabus. Risk of grading disputes;
  undermines an otherwise verified marks-arithmetic chain.
- **Remediation (fix now):** choose one set (syllabus W6/W7/W10/W11 = Labs
  06/07/10/11 is the most internally consistent with the calendar's
  assignment columns), then update `calendar-config.json`, `labs/index.md`,
  regenerate calendar views, and re-run validators. Add a cross-artifact
  check to `validate_calendar.py` (compare config vs syllabus Pract weeks).
- **Status:** RESOLVED (handover). Canonical set confirmed as Labs 06/07/10/11
  (the lab handouts themselves declare Pract-1–4 on exactly those labs).
  Fixed: `calendar-config.json`, `site-src/labs/index.md`,
  `site-src/assessment/index.md`; calendar views regenerated; new validator
  check **C9** cross-verifies config ↔ syllabus ↔ handout numbering (would
  have failed pre-fix; verified failing-config detection by construction).

## F-02 · MEDIUM · Validator output-path collision

- **Evidence (executed):** `validate_teaching_plans.py` line 28 writes
  `ROOT / "coverage-report.md"` (i.e. `docs-meta/coverage-report.md`),
  overwriting any other content at that path. **Observed live TWICE during
  this audit:** once during evidence gathering (in-progress audit report
  replaced by the teaching-plan report), and again during the closing
  regression loop after the audit report had been restored.
- **Affected files:** `docs-meta/validate_teaching_plans.py`,
  `docs-meta/coverage-report.md` (this audit now owns the path; the
  teaching-plan report is preserved inside validation-summary.md §9).
- **Impact:** silent data loss; ambiguous meaning of a canonical-looking
  path; future audits/CI writing both reports will clobber one another.
- **Remediation (fix now):** rename the teaching-plan output to
  `docs-meta/teaching-plans-coverage.md` (one-line change + docstring) and
  re-run to regenerate.
- **Status:** RESOLVED (handover). Validator now writes
  `teaching-plans-coverage.md`; verified by re-run output.

## F-03 · MEDIUM · Stale page count on the public QA page

- **Evidence (executed):** `docs-meta/website-qa.md` stated "182 HTML
  pages"; the current strict build produces **183** (count executed after
  the calendar page joined the nav). *Evidence correction (handover):* the
  public `site-src/about/qa-report.md` never hard-coded a count — the audit
  initially attributed the stale number to both files; re-grep showed it
  only in the internal ledger.
- **Impact:** internal ledger drift only (public page unaffected — see
  correction above); small credibility cost within the project's own
  honest-ledger standard.
- **Remediation:** counts replaced with a floor-checked formulation;
  ledger refreshed at handover.
- **Status:** RESOLVED (handover).

## F-04 · MEDIUM · Unpinned dependencies in the deploy workflow

- **Evidence (executed):** `.github/workflows/deploy-pages.yml` line 40:
  `pip install mkdocs-material mkdocs-minify-plugin` (floating versions);
  actions referenced at major tags (`@v4`, `@v3`, `@v5`). Local validation
  ran MkDocs 1.6.1 / Material 9.7.7 — CI may install anything newer.
- **Impact:** a future breaking release (Material has had them) fails the
  deploy or silently changes rendering; reproducibility gap between local
  validation and CI.
- **Remediation (fix now):** pin exact versions
  (`mkdocs-material==9.7.7 mkdocs-minify-plugin==0.8.0`) and/or add a
  `requirements.txt` + Dependabot; pin actions to full SHAs for supply-chain
  hygiene.
- **Status:** PARTIALLY RESOLVED (handover). Python deps pinned to the
  locally validated versions in the workflow. Action SHAs not pinned
  (major tags remain) — acceptable residual risk, revisit before
  production adoption.

## F-05 · MEDIUM (low) · CLO-5 has no dedicated lab

- **Evidence (executed):** CLO matrix (validation-summary §4): CLO-5
  (crypto fundamentals) appears in 0 of 16 lab handouts; Lab-07 maps only
  CLO-6. Substance check: Lab-07 does include cipher/algorithm audit
  content, so the *skill* is practiced — the *mapping* is absent.
- **Impact:** audit trail gap: "taught and assessed" for CLO-5 holds, but
  "practiced in a lab" is not formally evidenced.
- **Remediation (fix now):** either add `CLO-5` to Lab-07's `clos:` (the
  content already supports it) or add a short CLO-5-tagged task; re-run
  validate_labs.
- **Status:** RESOLVED (handover). Lab-07 `clos:` now `[CLO-5, CLO-6]`
  (cipher-suite/algorithm audit content substantiates CLO-5);
  validate_labs green after change.

## F-07 · MEDIUM (documented) · Slide rendering never exercised

- **Evidence (executed):** No Node/npm in the environment; no Marp render
  attempted. validate_slides verifies structure (front matter, objectives,
  notes, timings, density, diagram refs) — not visual output. The 10 shared
  diagrams are Mermaid+ASCII; Mermaid renders only in Marp/browser context.
- **Affected files:** `teaching/slides/**` (36 decks + 10 diagrams).
- **Impact:** first real render may reveal overflow/spacing issues that
  structural checks cannot see; diagrams unrendered.
- **Remediation:** on any machine with Node: `npx @marp-team/marp-cli
  teaching/slides/lecture-01-*.md -o /tmp/l01.html` and eyeball; batch
  render; record results in slide-resources.md. (One session.)
- **Status:** OPEN (documented in teaching/slides/README.md).

## F-08 · MEDIUM (inherent) · Lab instructions never executed live

- **Evidence (executed):** No lab VM/range exists in this environment; all
  16 handouts' commands were reviewed conceptually and for internal
  consistency (validate_labs 13/13) but **none were run**. Only 2/16
  handouts carry explicit tested/untested labels (also F-09).
- **Impact:** first delivery of each lab may hit environment friction
  (paths, package versions, image availability) — the normal state for
  untested instructions, but it must be visible to the instructor.
- **Remediation:** provision the lab range (roadmap's remaining item),
  execute Lab-01→16 in order, label each handout, record deviations. Multi-
  session; partially blocked on infrastructure.
- **Status:** OPEN (blocked on range provisioning).

## F-09 · RETRACTED (handover) · Tested/untested labeling in labs

- **Original claim:** only 2/16 handouts carry tested/untested markers.
- **Correction (handover, re-executed):** the labs use a *per-step* status
  system (✅ executed-and-verified / ⚠️ untested, with a "Command status"
  legend) that the audit's word-match missed. Re-check: 16/16 handouts have
  the legend; step-marker coverage per lab recorded in
  validation-summary.md §7b. The audit's grep pattern was too narrow —
  finding withdrawn; no content change required (no labels were added).
- **Status:** RETRACTED — audit false positive.

## F-10 · LOW · No top-level README or .gitignore

- **Evidence (executed):** `ls *.md` at repo root → empty; `.gitignore`
  absent. The project's front door is missing; generated trees (`site/`,
  `.venv-mkdocs/`) have no VCS exclusion.
- **Impact:** discoverability/onboarding (GitHub renders README on the repo
  landing page); risk of committing build artifacts and the local venv.
- **Remediation (fix now):** write README.md (course overview, validator
  and site-build quickstarts, links to syllabus/calendar/site) and a
  .gitignore (`site/`, `.venv*/`, `__pycache__/`, `docs-meta/calendar.ics`).
- **Status:** RESOLVED (handover). Both files created.

## F-11 · LOW (inherent) · Technical accuracy spot-verified, not exhaustively reviewed

- **Evidence (executed):** probed claims verified correct (TLS RTT/0-RTT,
  TCP teardown, IPsec AH/ESP/NAT, SYN backlog); remaining ~28 lectures
  reviewed only by validators (structure) and during authoring, not by a
  second technical pass.
- **Impact:** residual risk of a subtle protocol claim being wrong
  somewhere in 32 lectures × detailed content.
- **Remediation:** scheduled second-pass technical review per module
  (M1–M4 first: highest density of protocol claims). Multi-session.
- **Status:** OPEN (residual risk documented).

## F-12 · LOW · Accessibility verified at code level only

- **Evidence (executed):** built HTML has `lang`, skip-link, aria-labels;
  one-H1-per-page and anchor links validated; palette is Material default
  (WCAG-tested upstream). **Not done:** screen-reader pass, automated
  contrast audit of custom styles (printable CSS colors), keyboard-only
  navigation walkthrough.
- **Impact:** standard claims are supportable; conformance claims (WCAG AA)
  are not.
- **Remediation:** run axe/Lighthouse on the built site; manual keyboard
  pass; record results. One session with a browser toolchain.
- **Status:** OPEN.

## F-13 · LOW · External reference URLs not liveness-checked

- **Evidence (executed):** reference sections exist on all 32 student
  pages; canonical identifiers verified current (RFC 9293, TLS 1.3 / RFC
  8446, SP 800-207, 800-61r2). URLs were not fetched (no network use for
  bulk checks in this audit).
- **Impact:** low; dead links possible in the references shelf.
- **Remediation:** scripted HEAD-request check of `http(s)://` links in
  references.md + lecture reference sections; fix 404s. One session.
- **Status:** OPEN.

## F-14 · LOW · Validators never tested against broken inputs (negative cases)

- **Evidence (executed):** all 9 validators pass on the current tree;
  their detection ability was exercised historically (each found real bugs
  when introduced) but not re-proven by injecting a synthetic defect in
  this audit.
- **Impact:** unknown false-negative rate; a validator could pass while
  silently skipping a check due to a parsing drift.
- **Remediation:** add a self-test harness: copy corpus to temp, inject
  one defect per check class, assert failure. One session.
- **Status:** OPEN.

## F-06 · INFORMATIONAL · Speaker notes carry no CLO tags

- **Evidence (executed):** CLO matrix shows 0 CLO mentions in
  `teaching/speaker-notes/*.md` (by design — notes cover delivery, not
  mapping; validate_teaching_plans enforces CLO presence in the *plans*).
- **Impact:** none; noted so the matrix zeros aren't mistaken for gaps.
- **Status:** NO ACTION (documented rationale).

## F-15 · INFORMATIONAL · Deployment end-to-end untested (by policy)

- **Evidence:** no push made across all sessions (mission rule); workflow
  build-job steps executed individually and locally; deploy job follows
  the official `actions/deploy-pages@v4` pattern.
- **Impact:** first real deployment is still the first real test; owner
  must enable Settings → Pages → GitHub Actions source.
- **Status:** EXPECTED (go-live checklist exists in website-qa.md).

## F-16 · INFORMATIONAL · Coverage-report naming now owned by the audit

- **Evidence:** after F-02's remediation the audit's coverage-report.md is
  stable; until then, the teaching-plan report regenerates on every
  validate_teaching_plans run and would overwrite it again.
- **Status:** RESOLVED-BY-F-02-REMEDIATION (register tracks linkage).
