---
artifact-type: website-qa-ledger
status: complete
last-updated: website session
validator: docs-meta/validate_site.py (W1–W8)
---

# Website QA Ledger

Engineering-facing record for the GitHub Pages site. The public summary
lives at `site-src/about/qa-report.md` (rendered at `/about/qa-report/`).

## 1. What was inspected before building

- Repository had **no prior site, no mkdocs config, and no workflows**
  (verified: no `mkdocs.yml`, no `.github/workflows/`, no site tree).
- Existing valuable content preserved untouched: `docs/lectures/` (32),
  `docs/labs/` (16), `modules/*/case-studies/` (100), `syllabus/`,
  `teaching/`, `instructor/`, `assessments/` — the site **copies** student
  material out of these trees; it never edits them.

## 2. Architecture

| Layer | Location | Role |
|---|---|---|
| MkDocs config | `mkdocs.yml` | Material theme; `docs_dir: site-src`; strict mode; search; toc permalinks; light/dark accessible palette |
| Site source | `site-src/` | Hand-written student pages + copied canonical student material |
| Copy generator | `docs-meta/build_site_content.py` | Copies 32 lectures + 16 labs + 100 cases + 7 assignments into `site-src/`, rewrites links, strips instructor-key path references, generates `cases/all-cases.md` |
| Instructor trees | `instructor/`, `teaching/` | **Outside `docs_dir`** — never in the build input |
| Deploy workflow | `.github/workflows/deploy-pages.yml` | build job (copy → `mkdocs build --strict` → leak-scan → upload) + deploy job (`actions/deploy-pages@v4`) |
| Validator | `docs-meta/validate_site.py` | W1–W8 checks, mirrors CI gates locally |

Publication model: separation is enforced **by construction** (instructor
trees never enter `docs_dir`) and **by scan** (built output grepped for
instructor markers; any hit fails the workflow before upload).

## 3. Validation results (actual)

**Strict build:** `mkdocs build --strict` → 0 warnings, exit 0.
**Leak scan on `site/`:** clean. **Output:** 183 HTML pages at handover (validator floor-checks ≥165 rather than pinning a rotting count),
including 32 lecture pages, 16 lab handouts, 101 case pages (100 + generated
full list), 7 assignment briefs, 8 module pages.

**`validate_site.py` W1–W8:** all pass —

- W1 config (docs_dir, strict, material, search, site_url, repo_url)
- W2 all nav pages exist; **BFS reachability** from nav over internal links
  covers all pages (no orphans)
- W3 content counts (32/16/100/7/8)
- W4 all internal md links resolve (checked exhaustively)
- W5 no instructor markers, no instructor-tree paths, no forbidden dirs in
  `docs_dir`
- W6 workflow present with permissions (pages:write, id-token:write),
  upload + deploy steps, strict build, single workflow file
- W7 leak scan clean on built output; page-count floor check (≥165) green
- W8 exactly one H1 per page (code fences excluded); heading anchors enabled

**YAML validity:** workflow parsed with PyYAML (jobs/permissions verified).
`mkdocs.yml` loads under MkDocs' own loader; plain `yaml.safe_load` cannot
resolve `!!python/name:` tags by design (documented, not a defect).

**Regression:** all eight course validators green under the venv Python —
plan, teaching plans (14), teaching materials (18), labs (13), cases (8),
assessments (A1–A8), slides (S1–S8), site (W1–W8).

## 4. Findings found and fixed during QA (honest record)

| # | Finding | Resolution |
|---|---|---|
| 1 | `mkdocs.yml` missing `docs_dir` (would have built `docs/` — the wrong tree, exposing raw course material) | Added `docs_dir: site-src` before first build |
| 2 | First strict build: **55 warnings** — depth-wrong links in labs/modules/cases/course pages, one stale lab-10 filename, two resources links | All fixed page-by-page; build script made idempotent (course-dir rewrite passes) |
| 3 | Leak scan: student pages contained 170 instructor-key **path references** (e.g. exit-ticket answer pointers) — no answer content, but internal tree disclosure | `build_site_content.py` now rewrites them to a neutral pointer at copy time; source trees unchanged |
| 4 | Leak scan: public instructor-resources page listed literal key-tree paths | Reworded to "instructor-only repository trees (paths withheld)" |
| 5 | Leak scan: QA report quoted the scan's own marker strings (self-referential) | Reworded; gate stays simple and fail-closed |
| 6 | `build_site_content.py` initially lived inside `docs_dir` and was copied into the built output | Moved to `docs-meta/`; rebuilt clean |
| 7 | Validator bugs (caught by its own first run): nav parser iterated strings char-by-char; H1 check counted `#` shell comments inside code fences; W2 checked nav listing instead of real reachability | Parser fixed for str/dict recursion; fence-stripping added; W2 upgraded to BFS walk from nav over internal links |
| 8 | 100 case pages + 7 assignment briefs were not linked anywhere on the site (orphaned content) | Generated `cases/all-cases.md` (tier-grouped, from case H1s); assignments listed on the Assignments page; nav gained a Modules section index |

## 5. Limitations & untested steps (documented, not hidden)

- **Deployment is untested end-to-end**: no push has been made from this
  environment (per the no-commit/no-push rule), so the workflow has not run
  on GitHub. It follows the official `actions/deploy-pages` pattern and the
  build job's exact commands were executed locally (copy → strict build →
  leak scan → output inspection).
- The repository owner must enable **Settings → Pages → Source: GitHub
  Actions** before the first deployment succeeds.
- Mermaid diagrams render client-side via Material; the seven site pages
  that embed diagrams are configuration-tested, not visually eyeballed in
  every browser.
- A local venv (`.venv-mkdocs/`, MkDocs 1.6.1 + Material 9.7.7) was created
  for validation; it is gitignored-by-convention tooling, not a deliverable.

## 6. How to rebuild locally

```bash
python docs-meta/build_site_content.py     # copy + sanitize + generate
python -m pip install mkdocs-material mkdocs-minify-plugin
python -m mkdocs build --strict            # fails on any warning
python docs-meta/validate_site.py          # W1–W8
grep -rniE "instructor-only: true|never-publish-to-students|INSTRUCTOR ONLY" site/   # expect no output
```

## 7. Calendar integration (calendar session)

- `site-src/course/calendar-generated.md` is generated by
  `docs-meta/generate_calendar.py` from finalized course front matter and is
  nav-linked under Course → "Semester Calendar"; the static calendar page
  cross-links to it.
- The deploy workflow regenerates the calendar on every push before the
  strict build, so the published calendar cannot drift from course content.
- `validate_calendar.py` C1–C8 re-parses sources independently and checks
  week/lecture/lab/assessment alignment, link integrity, and freshness.
- Instructor planning view intentionally lives in `docs-meta/` (outside
  `docs_dir`) and links nowhere into the answer-key trees; verified by the
  leak scan after integration.
