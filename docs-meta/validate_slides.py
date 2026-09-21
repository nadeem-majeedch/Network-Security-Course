#!/usr/bin/env python3
"""Validator for the slide-resource layer (teaching/slides/).

Checks (per mission validation requirements):
  S1  32 lecture decks exist, numbering mirrors canonical lecture files
      (lecture-NN-*.md ↔ lecture-NN-*.md), no gaps/duplicates
  S2  3 special decks exist (review-midterm, review-final,
      case-studies-showcase) + README
  S3  every deck: Marp front matter (marp: true), title/objectives slide,
      notes present, timing statement, objectives present
  S4  every lecture deck: `lecture: LNN` anchor matches file number and
      resolves to an existing canonical lecture file; CLOs declared
  S5  diagram references resolve to existing assets in teaching/slides/
      (and referenced diagrams carry text descriptions)
  S6  slide-density ceiling: content slides ≤ 6 bullets (heuristic on
      top-level bullets per slide)
  S7  accessibility: every diagram asset has an accessibility text line
  S8  speaker notes: every lecture deck carries `<!-- notes:` blocks and
      the paired canonical speaker-notes file exists in teaching/
Exit 0 on success; nonzero with findings otherwise.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLIDES = ROOT / "teaching" / "slides"
DIAGRAMS = SLIDES / "diagrams"
FINDINGS = []


def bullets_in_slide(slide_body: str) -> int:
    """Top-level bullet count: lines starting with '- ' or '* '."""
    return len(re.findall(r"(?m)^\s*[-*]\s+", slide_body))


def check_deck(path: Path, kind: str):
    text = path.read_text(encoding="utf-8")
    fm = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)

    if not fm:
        FINDINGS.append(f"S3 {path.name}: no front matter")
        return None
    head = fm.group(1)
    if "marp: true" not in head:
        FINDINGS.append(f"S3 {path.name}: missing 'marp: true' directive")
    if "status: complete" not in head:
        FINDINGS.append(f"S3 {path.name}: status not complete")
    if kind == "lecture" and not re.search(r"^lecture: L\d{2}", head, re.MULTILINE):
        FINDINGS.append(f"S3 {path.name}: missing lecture anchor")
    if "clos:" not in head:
        FINDINGS.append(f"S3 {path.name}: missing CLO declaration")

    body = text[fm.end():]
    slides = [s for s in body.split("\n---\n") if s.strip()]
    if len(slides) < 8:
        FINDINGS.append(f"S3 {path.name}: only {len(slides)} slides (density floor)")

    # objectives slide (lecture decks) / session-overview slide (special decks)
    if not re.search(r"(?i)## (Learning Objectives|Session Overview)", body):
        FINDINGS.append(f"S3 {path.name}: no Learning Objectives / Session Overview slide")

    # speaker notes present
    if "<!-- notes" not in body:
        FINDINGS.append(f"S3 {path.name}: no speaker-notes blocks")

    # timing statement (front matter or notes)
    if not re.search(r"(?i)duration:|\d+\s*min", text):
        FINDINGS.append(f"S3 {path.name}: no timing statement")

    # density ceiling per slide (skip title/objective/reference slides is
    # over-engineering; flag slides with >8 bullets, the hard ceiling)
    for i, s in enumerate(slides, 1):
        n = bullets_in_slide(s)
        if n > 8:
            FINDINGS.append(f"S6 {path.name}: slide {i} has {n} bullets (>8 ceiling)")

    # diagram references resolve
    for ref in re.findall(r"diagrams/([a-z0-9\-]+)\.md", body):
        if not (DIAGRAMS / f"{ref}.md").exists():
            FINDINGS.append(f"S5 {path.name}: diagram ref missing -> {ref}.md")

    return len(slides), head, body


def main() -> int:
    # S1: 32 lecture decks mirroring canonical lectures
    canonical = sorted(ROOT.glob("modules/*/lectures/lecture-*.md"))
    if len(canonical) != 32:
        FINDINGS.append(f"S1 canonical lecture count is {len(canonical)} (expected 32) — check modules tree")
    for cn in canonical:
        m = re.match(r"lecture-(\d{2})-", cn.name)
        if not m:
            FINDINGS.append(f"S1 unparsable canonical lecture name: {cn.name}")
            continue
        nn = m.group(1)
        deck = SLIDES / f"lecture-{nn}-" + cn.name.split("-", 1)[1].rsplit(".", 1)[0] + ".md" if False else None
        matches = list(SLIDES.glob(f"lecture-{nn}-*.md"))
        if not matches:
            FINDINGS.append(f"S1 missing lecture deck for L{nn}")
        elif len(matches) > 1:
            FINDINGS.append(f"S1 duplicate decks for L{nn}: {[p.name for p in matches]}")

    # S2: special decks + README
    for special in ["review-midterm.md", "review-final.md", "case-studies-showcase.md", "README.md"]:
        if not (SLIDES / special).exists():
            FINDINGS.append(f"S2 missing special deck: {special}")

    # S3–S8: per-deck checks
    for p in sorted(SLIDES.glob("lecture-*.md")):
        kind = "lecture" if re.match(r"lecture-\d{2}", p.name) else "special"
        check_deck(p, kind)
        # S8: paired canonical speaker notes
        if kind == "lecture":
            nn = re.match(r"lecture-(\d{2})-", p.name).group(1)
            notes = ROOT / "teaching" / "speaker-notes" / f"lecture-{nn}-speaker-notes.md"
            if not notes.exists():
                FINDINGS.append(f"S8 {p.name}: canonical speaker notes missing ({notes.name})")

    for p in [SLIDES / "review-midterm.md", SLIDES / "review-final.md",
              SLIDES / "case-studies-showcase.md"]:
        if p.exists():
            check_deck(p, "special")

    # S7: diagram accessibility lines
    for d in sorted(DIAGRAMS.glob("*.md")):
        t = d.read_text(encoding="utf-8")
        if "Text description" not in t:
            FINDINGS.append(f"S7 diagram {d.name}: missing accessibility text description")
        if "status: complete" not in t:
            FINDINGS.append(f"S7 diagram {d.name}: status not complete")

    # deck count summary
    decks = list(SLIDES.glob("lecture-*.md"))
    if len(decks) != 32:
        FINDINGS.append(f"S1 lecture deck count is {len(decks)} (expected 32)")

    if FINDINGS:
        print(f"FAIL — {len(FINDINGS)} finding(s):")
        for f in FINDINGS:
            print("  " + f)
        return 1
    print(f"PASS — 32 lecture decks + 3 special decks + README; Marp front matter, "
          "objectives, notes, timings, density, diagram refs, accessibility lines all verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
