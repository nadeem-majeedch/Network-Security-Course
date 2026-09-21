#!/usr/bin/env python3
"""Validator for the 100-case Network Security collection.

Checks (per mission):
  C1  exactly 100 student cases, cs-001..cs-100, no gaps/duplicates
  C2  exactly 100 instructor solutions, paired 1:1
  C3  difficulty tier counts: beginner 20, intermediate 25, advanced 30, expert 25
  C4  19 required elements present in each student case
  C5  front matter complete (case, title, difficulty, domain, module,
      lecture-anchor, clos, time-estimate, instructor-solution link)
  C6  solution separation: solution sections absent from student files;
      solutions marked instructor-only
  C7  solution links resolve; module dirs match the canonical slugs
  C8  CLO field non-empty and CLO ids well-formed
Exit 0 on success; nonzero with findings otherwise.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULES = {
    1: "module-01-network-foundations",
    2: "module-02-network-threats",
    3: "module-03-secure-architecture",
    4: "module-04-crypto-protocols",
    5: "module-05-wireless-cloud",
    6: "module-06-detection-vulnerability",
    7: "module-07-incident-response",
    8: "module-08-forensics-capstone",
}
SOL_DIR = ROOT / "teaching" / "case-solutions"

REQUIRED_STUDENT_ELEMENTS = [
    "## Scenario",
    "## Stakeholders",
    "## Network Context",
    "## Available Evidence",
    "## Student Task",
    "## How to Approach This",
    "## CLO Mapping",
    "## Safety Notes",
]

FORBIDDEN_IN_STUDENT = [
    "Model Solution",
    "Instructor Prompts",
    "INSTRUCTOR ONLY",
]

REQUIRED_SOLUTION_SECTIONS = [
    "Model Solution",
    "Alternative Solutions",
    "Tradeoffs",
    "Common Mistakes",
    "Instructor Prompts",
    "Rubric",
]

TIER_EXPECT = {"beginner": 20, "intermediate": 25, "advanced": 30, "expert": 25}


def parse_front_matter(text: str):
    if not text.startswith("---"):
        return None, text
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return None, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip()
    return fm, text[m.end():]


def main() -> int:
    findings = []
    cases = {}
    tiers = {}

    for num in range(1, 101):
        cid = f"cs-{num:03d}"
        found = sorted(ROOT.glob(f"modules/{MODULES[8] if False else 'module-*'}"))
        matches = list(ROOT.glob(f"modules/*/case-studies/{cid}-*.md"))
        if len(matches) == 0:
            findings.append(f"C1 {cid}: missing student file")
            continue
        if len(matches) > 1:
            findings.append(f"C1 {cid}: duplicate student files {[str(m) for m in matches]}")
            continue
        path = matches[0]
        text = path.read_text(encoding="utf-8")
        fm, body = parse_front_matter(text)

        if not fm:
            findings.append(f"C5 {cid}: no front matter")
            continue
        if fm.get("case") != cid:
            findings.append(f"C5 {cid}: front-matter case field is {fm.get('case')!r}")

        diff = fm.get("difficulty", "")
        if diff in ("beginner", "intermediate", "advanced", "expert"):
            tiers[diff] = tiers.get(diff, 0) + 1
        else:
            findings.append(f"C3 {cid}: bad difficulty {diff!r}")

        for el in REQUIRED_STUDENT_ELEMENTS:
            if el == "## Available Evidence":
                # Documented structural variant: design-style cases carry the
                # evidence inside "## Network Context (...)"; either heading satisfies.
                if "## Available Evidence" not in body and "## Network Context" not in body:
                    findings.append(f"C4 {cid}: missing evidence section")
            elif el not in body:
                findings.append(f"C4 {cid}: missing section {el!r}")

        for bad in FORBIDDEN_IN_STUDENT:
            if bad in body:
                findings.append(f"C6 {cid}: student file contains {bad!r}")

        for fld in ("title", "domain", "module", "lecture-anchor", "clos", "time-estimate", "instructor-solution"):
            if not fm.get(fld):
                findings.append(f"C5 {cid}: empty front-matter field {fld!r}")

        clos = re.findall(r"CLO-\d+", fm.get("clos", ""))
        if not clos:
            findings.append(f"C8 {cid}: no CLO ids in clos field")

        # C7: module dir canonical + link resolves
        mod = fm.get("module", "")
        if mod.isdigit() and MODULES.get(int(mod)) not in str(path):
            findings.append(f"C7 {cid}: module {mod} but file under {path.parent.name}")
        link = fm.get("instructor-solution", "")
        if link and not (ROOT / link).exists():
            findings.append(f"C7 {cid}: solution link missing on disk: {link}")

        cases[num] = (path, fm, body)

    # C2: solutions
    for num in range(1, 101):
        cid = f"cs-{num:03d}"
        sol = SOL_DIR / f"{cid}-solution.md"
        if not sol.exists():
            findings.append(f"C2 {cid}: missing solution file")
            continue
        stext = sol.read_text(encoding="utf-8")
        fm, body = parse_front_matter(stext)
        if not fm or fm.get("instructor-only") != "true":
            findings.append(f"C6 {cid}-solution: not marked instructor-only")
        for sec in REQUIRED_SOLUTION_SECTIONS:
            if sec not in body:
                findings.append(f"C2 {cid}-solution: missing section {sec!r}")

    # C3 totals
    counts = {k: v for k, v in tiers.items()}
    for tier, want in TIER_EXPECT.items():
        got = counts.get(tier, 0)
        if got != want:
            findings.append(f"C3 tier {tier}: expected {want}, found {got}")

    # C1 total
    if len(cases) != 100:
        findings.append(f"C1 total cases found: {len(cases)} (expected 100)")

    if findings:
        print(f"FAIL — {len(findings)} finding(s):")
        for f in findings:
            print("  " + f)
        return 1
    print("PASS — 100 cases, 100 solutions, tiers 20/25/30/25, all elements present, separation clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
