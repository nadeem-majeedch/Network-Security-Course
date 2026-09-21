#!/usr/bin/env python3
"""Site validation for the Network Security Course website (W1-W8).

Checks MkDocs config, navigation completeness, internal links, the Pages
workflow, instructor-content separation, and (if site/ exists) the built
output. Mirrors the CI gates so failures surface locally first.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_SRC = ROOT / "site-src"
BUILT = ROOT / "site"

FINDINGS: list[str] = []


def check(cond: bool, msg_ok: str, msg_fail: str) -> bool:
    if cond:
        print(f"  PASS  {msg_ok}")
    else:
        FINDINGS.append(msg_fail)
        print(f"  FAIL  {msg_fail}")
    return cond


FENCE_RE = re.compile(r"```.*?```|~~~.*?~~~", re.S)


def load_mkdocs_simple(path: Path) -> dict:
    """Parse mkdocs.yml ignoring mkdocs-specific !!python/name tags."""
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"!!python/name:[^\s]+", '"__tagged__"', text)
    import yaml  # available inside the mkdocs venv
    return yaml.safe_load(text)


def flatten_nav(nav) -> list[str]:
    out = []
    if isinstance(nav, str):
        return [nav]
    if isinstance(nav, dict):
        for v in nav.values():
            out.extend(flatten_nav(v))
        return out
    for item in nav:
        out.extend(flatten_nav(item))
    return out


def section(title: str) -> None:
    print(f"\n[{title}]")


# ---------------------------------------------------------------- W1 config
section("W1 - mkdocs.yml configuration")
cfg_path = ROOT / "mkdocs.yml"
cfg = load_mkdocs_simple(cfg_path) if cfg_path.exists() else {}
check(cfg.get("docs_dir") == "site-src",
      "docs_dir is site-src (student tree only)",
      "docs_dir missing or not site-src")
check(cfg.get("strict") is True, "strict mode enabled",
      "strict mode not enabled")
check(cfg.get("theme", {}).get("name") == "material", "Material theme",
      "theme is not material")
plugins = cfg.get("plugins") or []
plugin_names = [p if isinstance(p, str) else list(p.keys())[0] for p in plugins]
check("search" in plugin_names, "search plugin enabled", "search plugin missing")
check(bool(cfg.get("site_url", "").startswith("https://nadeem-majeedch.github.io/")),
      "site_url points at the Pages origin", "site_url wrong/missing")
check(bool(cfg.get("repo_url", "").endswith("Network-Security-Course")),
      "repo_url points at the course repository", "repo_url wrong/missing")

# ---------------------------------------------------------------- W2 nav
section("W2 - navigation completeness")
nav_pages = flatten_nav(cfg.get("nav", [])) if cfg else []
missing = [p for p in nav_pages if not (SITE_SRC / p).exists()]
check(bool(nav_pages) and not missing,
      f"all {len(nav_pages)} nav pages exist in site-src",
      f"nav pages missing from site-src: {missing[:5]}")
if nav_pages:
    all_md = {p.relative_to(SITE_SRC).as_posix().replace("\\", "/")
              for p in SITE_SRC.rglob("*.md")}
    link_re = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)")

    def resolve_targets(page: Path) -> set[str]:
        """Internal md links on one page -> site-src-relative POSIX paths."""
        text = FENCE_RE.sub("", page.read_text(encoding="utf-8"))
        out = set()
        for m in link_re.finditer(text):
            t = m.group(1)
            if t.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (page.parent / t).resolve()
            if resolved.exists() and resolved.suffix == ".md":
                out.add(resolved.relative_to(SITE_SRC).as_posix()
                        .replace("\\", "/"))
        return out

    # BFS from nav entry pages over internal links.
    seen: set[str] = set()
    queue = [p for p in nav_pages]
    while queue:
        rel = queue.pop(0)
        if rel in seen:
            continue
        seen.add(rel)
        page = SITE_SRC / rel
        if page.exists():
            queue.extend(sorted(resolve_targets(page) - seen))
    orphans = sorted(all_md - seen)
    check(not orphans,
          f"all {len(all_md)} pages reachable from nav via internal links",
          f"unreachable (orphan) pages: {orphans[:10]}")

# ---------------------------------------------------------------- W3 content
section("W3 - expected site content present")
lect = sorted((SITE_SRC / "lectures").glob("lecture-*.md")) if (SITE_SRC / "lectures").exists() else []
labs = sorted((SITE_SRC / "labs").glob("lab-*.md")) if (SITE_SRC / "labs").exists() else []
cases = sorted((SITE_SRC / "cases").glob("cs-*.md")) if (SITE_SRC / "cases").exists() else []
asg = sorted((SITE_SRC / "assessment" / "assignments").glob("assignment-*.md")) if (SITE_SRC / "assessment" / "assignments").exists() else []
mods = sorted((SITE_SRC / "modules").glob("m0*/index.md")) if (SITE_SRC / "modules").exists() else []
check(len(lect) == 32, "32 lecture pages in site", f"{len(lect)} lecture pages")
check(len(labs) == 16, "16 lab handouts in site", f"{len(labs)} lab handouts")
check(len(cases) == 100, "100 case-study pages in site", f"{len(cases)} case pages")
check(len(asg) == 7, "7 assignment briefs in site", f"{len(asg)} assignment briefs")
check(len(mods) == 8, "8 module pages in site", f"{len(mods)} module pages")

# ---------------------------------------------------------------- W4 links
section("W4 - internal link integrity (site-src)")
broken: list[str] = []
link_re = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)")
for md in SITE_SRC.rglob("*.md"):
    text = md.read_text(encoding="utf-8")
    for m in link_re.finditer(text):
        target = m.group(1)
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        resolved = (md.parent / target).resolve()
        if not resolved.exists():
            broken.append(f"{md.relative_to(SITE_SRC)} -> {target}")
check(not broken, "all internal md links resolve",
      f"broken internal links: {broken[:8]}")

# ---------------------------------------------------------------- W5 secrets
section("W5 - instructor-only separation")
src_blob = "\n".join(
    p.read_text(encoding="utf-8") for p in SITE_SRC.rglob("*.md")
)
markers = ["instructor-only: true", "never-publish-to-students",
           "INSTRUCTOR ONLY", "Model Solution", "MODEL SOLUTION"]
leaks = [m for m in markers if m in src_blob]
check(not leaks, "no instructor-only markers in site-src markdown",
      f"instructor markers found in site-src: {leaks}")
path_leaks = re.findall(
    r"teaching/(?:answer-keys|lab-answer-keys|case-solutions|speaker-notes)"
    r"|instructor/answer-keys", src_blob)
check(not path_leaks,
      "no instructor-tree path references in site-src markdown",
      f"instructor paths referenced in site-src: {len(path_leaks)}x")
forbidden_dirs = [d for d in ("instructor", "teaching")
                  if (SITE_SRC / d).exists()]
check(not forbidden_dirs,
      "no instructor/teaching directories inside docs_dir",
      f"forbidden dirs in site-src: {forbidden_dirs}")

# ---------------------------------------------------------------- W6 workflow
section("W6 - GitHub Pages workflow")
wf_path = ROOT / ".github" / "workflows" / "deploy-pages.yml"
if check(wf_path.exists(), "deploy-pages.yml exists", "workflow file missing"):
    wf_text = wf_path.read_text(encoding="utf-8")
    for needle, ok, fail in [
        ("permissions:", "permissions block present", "permissions missing"),
        ("pages: write", "pages: write granted", "pages: write missing"),
        ("id-token: write", "id-token: write granted", "id-token missing"),
        ("actions/upload-pages-artifact", "artifact upload step",
         "upload-pages-artifact step missing"),
        ("actions/deploy-pages", "official deploy step",
         "deploy-pages step missing"),
        ("mkdocs build --strict", "strict build step",
         "strict build step missing"),
        ("python docs-meta/build_site_content.py", "content copy step",
         "content copy step missing"),
    ]:
        check(needle in wf_text, ok, fail)
    workflows = [p.name for p in (ROOT / ".github" / "workflows").glob("*.yml")]
    check(workflows == ["deploy-pages.yml"],
          "single Pages workflow (no duplicates)", f"workflows: {workflows}")

# ---------------------------------------------------------------- W7 built
section("W7 - built output gate (site/)")
if BUILT.exists():
    leak_re = re.compile(
        r"instructor-only: true|never-publish-to-students|INSTRUCTOR ONLY"
        r"|answer key \u2014|teaching/(?:speaker-notes|answer-keys|lab-answer-keys"
        r"|case-solutions)|instructor/answer-keys", re.I)
    hits = []
    for f in BUILT.rglob("*"):
        if f.is_file() and f.suffix in (".html", ".json", ".xml"):
            if leak_re.search(f.read_text(encoding="utf-8", errors="ignore")):
                hits.append(f.relative_to(BUILT).as_posix())
    check(not hits, "leak scan clean on built output",
          f"leak markers in built output: {hits[:5]}")
    html_count = len(list(BUILT.rglob("index.html")))
    check(html_count >= 165,
          f"{html_count} pages built (expected >= 165)",
          f"only {html_count} pages built")
else:
    print("  SKIP  site/ not built yet - run: mkdocs build --strict")

# ---------------------------------------------------------------- W8 a11y
section("W8 - accessibility basics")
FENCE_RE = re.compile(r"```.*?```|~~~.*?~~~", re.S)
bad_h1 = []
for md in SITE_SRC.rglob("*.md"):
    body = FENCE_RE.sub("", md.read_text(encoding="utf-8"))
    h1s = [ln for ln in body.splitlines() if ln.startswith("# ")]
    if len(h1s) != 1:
        bad_h1.append(md.relative_to(SITE_SRC).as_posix())
check(not bad_h1, "exactly one H1 per page",
      f"pages without exactly one H1: {bad_h1[:8]}")
has_permalink = "permalink: true" in cfg_path.read_text(encoding="utf-8")
check(has_permalink, "heading anchors enabled (toc.permalink)",
      "toc.permalink not enabled")

print(f"\n{'=' * 50}")
if FINDINGS:
    print(f"FAIL: {len(FINDINGS)} finding(s)")
    for f in FINDINGS:
        print(f"  - {f}")
    sys.exit(1)
print("OK: all site validation checks passed")
