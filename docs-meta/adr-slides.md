---
artifact-type: adr
adr-id: ADR-003
title: Slide Format & Presentation Resource Conventions
status: accepted
date: presentation-resources session
context-decision: presentation layer format
supersedes: none
---

# ADR-003 — Slide Format & Presentation Resource Conventions

## Status

Accepted (this session). Consistent with ADR-001's defensive framing and
the §7 directory conventions.

## Context

The repository had **no existing slide format** (verified: no Marp,
reveal.js, or Slidev conventions anywhere in the tree; the
teaching-material inventory recorded "slide decks pending"). The course
needed 32 lecture decks + review/case decks that stay maintainable as
plain-text, version-controlled content alongside the existing Markdown
layers.

## Decision

1. **Marp** for slide decks. Rationale: slides are plain Markdown with a
   front-matter directive block — diffable, reviewable, no binary assets;
   one HTML comment per slide; the deck renders to HTML/PDF/PPTX via
   `marp-cli` when needed. The deck *source* is always renderable by a
   human reading the file.
2. **Mermaid fenced blocks** for diagrams (flowcharts, sequence diagrams)
   and **ASCII box diagrams** where topology precision matters (existing
   repository convention — student lecture pages already use both).
   Mermaid renders in GitHub and in Marp via the `mermaid` integration;
   until then, the ASCII variant inside the same block is the
   ground-truth visual.
3. **Directory layout** (extends §7.1):
   - `teaching/slides/lecture-NN-<slug>.md` — one deck per lecture,
     numbering mirrors the canonical lecture files.
   - `teaching/slides/review-midterm.md`, `review-final.md`,
     `case-studies-showcase.md` — the three special decks.
   - `teaching/slides/diagrams/` — shared diagram assets referenced by
     multiple decks (one diagram, one definition).
   - `teaching/slides/README.md` — the render guide (dependencies,
     commands, tested-vs-untested labeling).
4. **Accessibility conventions** (enforced by validator): every deck has
   a title slide with objectives, ≤6 bullets per content slide, every
   diagram has a text description line, color is never the sole carrier
   of meaning (labels accompany all color coding).
5. **Density rule:** a lecture deck is 16–24 slides for a 2-hour block
   (~4–6 min per content slide); the speaker-notes section of each deck
   (or its paired notes file) carries timings.

## Alternatives considered

- **PowerPoint/PPTX authoring:** not diffable, not reviewable in PRs,
  binary churn — rejected for a course repository.
- **reveal.js HTML:** heavier maintenance; slides-as-HTML are hostile to
  review — rejected.
- **Pure ASCII-only decks:** would work but loses cheap Mermaid rendering
  on GitHub where students preview — rejected as the sole form.

## Consequences

- Rendering Marp/Mermaid to actual HTML/PDF requires Node + marp-cli —
  **not executed in this environment**; documented as untested in
  `teaching/slides/README.md` with the exact commands.
- Slide outlines serve dual duty: projector content + structured
  teaching plan; speaker notes live with the deck.

## Compliance

`docs-meta/validate_slides.py` enforces: 32 decks + 3 special decks,
Marp front matter present, objectives slide, notes/timings present,
diagram references resolve to existing assets, slide-density ceiling.
