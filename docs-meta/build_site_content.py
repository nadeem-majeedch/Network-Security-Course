#!/usr/bin/env python3
"""Build site-src/ for the Network Security Course website.

Copies canonical STUDENT-facing material into the MkDocs source tree with
mechanical link rewriting. Instructor-only trees (instructor/, teaching/)
are NEVER copied — they stay outside docs_dir by construction.

Copies:
  docs/lectures/lecture-*.md      -> site-src/lectures/lecture-NN-*.md
  docs/labs/lab-*.md              -> site-src/labs/lab-NN-*.md
  modules/module-0N-*/case-studies/cs-*.md
                                  -> site-src/cases/cs-NNN-*.md

Link rewrites (applied to ALL site-src/*.md before copying sources):
  ../lectures/lecture-01.md     -> ../../lectures/lecture-01.md      (m0N -> root)
  ../lectures/lecture-NN-*.md   -> ../../lectures/lecture-NN-*.md    (m0N -> root)
  ../labs/lab-*.md              -> ../../labs/lab-*.md               (m0N -> root)
  modules/module-0N.md          -> modules/m0N/index.md              (root pages)
  course/description.md etc.    -> course/description.md (already correct)
  assessment-info.md            -> assessment/index.md
  case-studies.md               -> cases/index.md
  labs.md                       -> labs/index.md
  ../assessment/index.md etc.   -> ../../assessment/index.md         (m0N -> root)

Idempotent: run repeatedly; regeneration = python site-src/build_site_content.py
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site-src"

LECTURES = sorted((ROOT / "docs" / "lectures").glob("lecture-*.md"))
LABS = sorted((ROOT / "docs" / "labs").glob("lab-*.md"))
CASES = sorted((ROOT / "modules").glob("module-*/case-studies/cs-*.md"))
ASSIGNMENTS = sorted((ROOT / "assessments" / "assignments").glob("assignment-*.md"))


def rewrite_root_pages(text: str) -> str:
    """Rewrite links written before the final nav layout (root-level pages)."""
    # Legacy flat pages -> new locations
    text = text.replace("](assessment-info.md)", "](assessment/index.md)")
    text = text.replace("](case-studies.md)", "](cases/index.md)")
    text = text.replace("](labs.md)", "](labs/index.md)")
    # Module pages renamed to m0N/index.md
    text = re.sub(
        r"\]\(modules/module-0(\d)\.md\)", r"](modules/m0\1/index.md)", text
    )
    return text


def rewrite_from_course_dir(text: str) -> str:
    """Rewrite links inside course/*.md (legacy root-relative forms)."""
    text = text.replace("](/assessment-info.md)", "](/../assessment/index.md)")
    text = text.replace("](/assessment-info.md)", "](/../assessment/index.md)")
    text = text.replace("](/case-studies.md)", "](/../cases/index.md)")
    text = text.replace("](/labs.md)", "](/../labs/index.md)")
    text = text.replace("](/course/description.md)", "](/description.md)")
    text = text.replace("](/course/clos.md)", "](/clos.md)")
    text = text.replace("](/course/calendar.md)", "](/calendar.md)")
    text = text.replace("](/assessment/index.md)", "](/../assessment/index.md)")
    text = text.replace("](/lectures/index.md)", "](/../lectures/index.md)")
    return text


def rewrite_from_module_dir(text: str) -> str:
    """Rewrite links inside modules/m0N/index.md (one directory deeper)."""
    text = text.replace("](../lectures/", "](../../lectures/")
    text = text.replace("](../labs/", "](../../labs/")
    text = text.replace("](../assessment/", "](../../assessment/")
    text = text.replace("](../cases/", "](../../cases/")
    text = text.replace("](../case-studies.md)", "](../../cases/index.md)")
    return text


INSTRUCTOR_KEY_RE = re.compile(
    r"(?:teaching/(?:answer-keys|lab-answer-keys|case-solutions|speaker-notes)"
    r"|instructor/answer-keys)/[A-Za-z0-9._/-]+"
)


def sanitize_for_publication(text: str) -> str:
    """Remove instructor-key PATH DISCLOSURES from student pages.

    These pages contain no answer content; they reference the repository's
    internal answer-key locations. The public site replaces those references
    with a neutral pointer, so no internal path is published.
    """
    return INSTRUCTOR_KEY_RE.sub(
        "the instructor answer-key collection (not published)", text
    )


def strip_yaml_front_matter(text: str) -> str:
    """Remove YAML front matter (MkDocs handles metadata itself)."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:].lstrip("\n")
    return text


def main() -> None:
    copied = {"lectures": 0, "labs": 0, "cases": 0, "assignments": 0}

    # 1) Rewrite links in hand-written site-src pages first.
    for md in SITE.rglob("*.md"):
        if md.name == "build_site_content.py":
            continue
        text = md.read_text(encoding="utf-8")
        new = rewrite_root_pages(text)
        posix = md.as_posix()
        if "/course/" in posix:
            new = rewrite_from_course_dir(new)
        if "/modules/m0" in posix and md.name == "index.md":
            new = rewrite_from_module_dir(new)
        if new != text:
            md.write_text(new, encoding="utf-8")

    # 2) Copy canonical student lecture pages (strip front matter; keep titles).
    out_dir = SITE / "lectures"
    out_dir.mkdir(exist_ok=True)
    for src in LECTURES:
        text = sanitize_for_publication(
            strip_yaml_front_matter(src.read_text(encoding="utf-8"))
        )
        (out_dir / src.name).write_text(text, encoding="utf-8")
        copied["lectures"] += 1

    # 3) Copy lab handouts.
    out_dir = SITE / "labs"
    out_dir.mkdir(exist_ok=True)
    for src in LABS:
        text = sanitize_for_publication(
            strip_yaml_front_matter(src.read_text(encoding="utf-8"))
        )
        (out_dir / src.name).write_text(text, encoding="utf-8")
        copied["labs"] += 1

    # 4) Copy case studies (student files only; solutions live in teaching/).
    out_dir = SITE / "cases"
    out_dir.mkdir(exist_ok=True)
    for src in CASES:
        text = sanitize_for_publication(
            strip_yaml_front_matter(src.read_text(encoding="utf-8"))
        )
        (out_dir / src.name).write_text(text, encoding="utf-8")
        copied["cases"] += 1

    # 5) Copy assignment briefs (student side; answer keys stay in instructor/).
    out_dir = SITE / "assessment" / "assignments"
    out_dir.mkdir(parents=True, exist_ok=True)
    for src in ASSIGNMENTS:
        text = sanitize_for_publication(
            strip_yaml_front_matter(src.read_text(encoding="utf-8"))
        )
        (out_dir / src.name).write_text(text, encoding="utf-8")
        copied["assignments"] += 1

    # 6) Generate the full case list (all 100 cases, tier-grouped).
    tiers = [
        ("Beginner", "cs-001–020", 1, 20),
        ("Intermediate", "cs-021–045", 21, 45),
        ("Advanced", "cs-046–075", 46, 75),
        ("Expert", "cs-076–100", 76, 100),
    ]
    case_titles = {}
    for src in CASES:
        m = re.search(r"^# (.+)$", strip_yaml_front_matter(
            src.read_text(encoding="utf-8")), re.M)
        case_titles[src.name] = m.group(1).strip() if m else src.stem
    lines = ["---", "status: complete", "artifact-type: generated-index",
             "instructor-only: false", "---", "", "# Full Case List", "",
             "> Generated by `docs-meta/build_site_content.py` — all 100",
             "student case pages, grouped by tier. All scenarios are",
             "simulated fiction.", ""]
    for label, rng, lo, hi in tiers:
        lines += [f"## {label} ({rng})", ""]
        for src in CASES:
            n = int(src.name[3:6])
            if lo <= n <= hi:
                lines.append(f"- [{case_titles[src.name]}]({src.name})")
        lines.append("")
    (SITE / "cases" / "all-cases.md").write_text(
        "\n".join(lines), encoding="utf-8")

    print(
        f"site-src build OK: {copied['lectures']} lectures, "
        f"{copied['labs']} labs, {copied['cases']} cases, "
        f"{copied['assignments']} assignments copied "
        f"(+ cases/all-cases.md generated)"
    )


if __name__ == "__main__":
    main()
