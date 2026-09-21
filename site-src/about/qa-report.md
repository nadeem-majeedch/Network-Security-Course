---
status: complete
artifact-type: qa-report-page
instructor-only: false
---

# Site QA Report

> Summary of the executable QA performed on this website. The detailed,
> engineering-facing ledger is `docs-meta/website-qa.md` in the repository.

## What is checked automatically

Every build runs two gates **before** deployment:

1. **Strict MkDocs build** — `mkdocs build --strict`. Any broken internal
   link, missing nav page, or invalid config fails the workflow; nothing
   broken is ever uploaded.
2. **Leak scan** — the built `site/` output is scanned for instructor-only
   front-matter markers, answer-key banners, and internal instructor-tree
   path references in page bodies. The exact patterns live in the
   deployment workflow; any hit fails the build.

## Design-level separation

Separation is enforced by construction, not just by scanning:

- MkDocs `docs_dir` is `site-src/` — a dedicated student-facing tree.
- The instructor-only repository trees are **outside** `site-src/` and
  outside every copy operation; they are never in the build input.
  Their internal paths are likewise never published: student pages that
  reference them are rewritten at build time to a neutral pointer.
- The only files copied into the site are canonical **student** materials:
  32 lecture pages, 16 lab handouts, 100 case-study pages (the student
  side only — model solutions remain in the instructor-only collection),
  and 7 assignment briefs.

## Known limitations (honest ledger)

- Mermaid diagrams render client-side via Material for MkDocs; extremely
  old browsers without ES6 support may not render them (text fallbacks
  appear in the surrounding prose).
- Search indexes student material only — instructor trees are not in the
  build, so their content is correctly absent from search results.
- The deploy workflow has not been exercised end-to-end until the first
  push to GitHub (no push has been made from this environment); the
  workflow file follows the official `actions/deploy-pages` pattern and
  the build gate is validated locally.
