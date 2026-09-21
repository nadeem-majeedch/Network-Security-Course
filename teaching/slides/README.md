---
artifact-type: slides-readme
status: complete
decks: 35
diagrams: 10
---

# Slide Decks & Presentation Resources

35 decks: 32 lecture decks (`lecture-01…32`), midterm review, final
review, and the case-studies showcase. Shared diagrams live in
`diagrams/` (one diagram, one definition — decks reference, never
duplicate).

## Rendering (UNTESTED in this environment)

Slide sources are plain Markdown (Marp-flavored). To render:

```bash
# Dependencies: Node.js ≥18, then:
npm install -g @marp-team/marp-cli      # UNTESTED here — no network/npm in this environment

# Per-deck HTML (works from the repo root):
marp teaching/slides/lecture-01-security-mindset-threat-landscape.md -o out/l01.html

# All decks to PDF:
marp teaching/slides/*.md --pdf -o out/

# Mermaid diagrams: Marp needs the mermaid plugin, e.g.:
marp --plugin @marp-team/mermaid-plugin ...   # UNTESTED — plugin name/API to verify
```

**Tested vs untested, honestly labeled:**
- *Tested:* nothing here was rendered in the authoring environment —
  no Node/npm available. The deck sources are however plain Markdown
  and were validated structurally (`docs-meta/validate_slides.py`:
  front matter, objectives, notes, timings, density, diagram refs).
- *Untested:* every `marp` command above, Mermaid's rendering fidelity,
  and PPTX export. First render should be smoke-tested on deck L01
  before batching.

Mermaid blocks: GitHub renders them natively (student preview path);
ASCII variants inside the same block preserve meaning when rendering
is unavailable.

## Conventions (per ADR-003)

- Front matter: `marp: true`, theme, pagination, lecture anchor
  (`lecture: LNN`, `clos: [...]`), `status: complete`.
- Slide 2 = objectives (3–5, measurable); last slide = references +
  next-lecture pointer.
- ≤6 bullets per content slide; diagrams carry a one-line text
  description (accessibility).
- Speaker notes: HTML comments `<!-- notes ... -->` between slides —
  timings per section sum to 110 min (2-hour block minus break).
- CS/DS examples: at least one per deck, drawn from the course's
  data-science infrastructure framing (GPU clusters, notebooks, data
  lakes).

## Deck index

See `docs-meta/slide-resources.md` for the full deck↔lecture↔diagram
map and validation results.
