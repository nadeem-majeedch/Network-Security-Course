#!/usr/bin/env python3
"""Calendar validation for the Network Security Course (C1-C9).

Re-parses the finalized course front matter INDEPENDENTLY of the generator
and checks every generated calendar view against it, so a stale, hand-edited,
or misaligned calendar fails.

Usage: python docs-meta/validate_calendar.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STUDENT = ROOT / "site-src" / "course" / "calendar-generated.md"
PRINTABLE = ROOT / "docs-meta" / "calendar-printable.html"
INSTRUCTOR = ROOT / "docs-meta" / "calendar-instructor.md"
CONFIG = ROOT / "docs-meta" / "calendar-config.json"
GENERATOR = ROOT / "docs-meta" / "generate_calendar.py"

FINDINGS: list[str] = []


def check(cond, ok, fail):
    if cond:
        print(f"  PASS  {ok}")
    else:
        FINDINGS.append(fail)
        print(f"  FAIL  {fail}")
    return bool(cond)


def section(t):
    print(f"\n[{t}]")


FM_RE = re.compile(r"\A---\n(.*?)\n---", re.S)


def read_fm(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    fm = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line and not line.startswith((" ", "#")):
                k, _, v = line.partition(":")
                fm[k.strip()] = v.strip()
    if "title" not in fm or not fm.get("title"):
        h1 = re.search(r"^# (.+)$", FM_RE.sub("", text), re.M)
        if h1:
            fm["title"] = h1.group(1).strip()
    return fm


def plist(v):
    return re.findall(r"[A-Za-z]+-?\d+", v or "")


def parse_sources():
    """Independent re-parse of the finalized content."""
    lectures = {}
    for p in sorted((ROOT / "modules").glob("module-*/lectures/lecture-*.md")):
        fm = read_fm(p)
        n = int(re.search(r"\d+", fm["lecture"]).group())
        lectures[n] = {"week": int(fm["week"]), "title": fm["title"],
                       "clos": plist(fm.get("clos", ""))}
    labs = {}
    for p in sorted((ROOT / "docs" / "labs").glob("lab-*.md")):
        fm = read_fm(p)
        n = int(re.search(r"\d+", fm["lab"]).group())
        labs[n] = {"week": int(fm["week"]), "title": fm["title"]}
    quizzes = []
    for p in sorted((ROOT / "assessments" / "quizzes").glob("quiz-*.md")):
        fm = read_fm(p)
        quizzes.append((int(fm["week"]), fm.get("type", "self-check")))
    assigns = {}
    for p in sorted((ROOT / "assessments" / "assignments").glob("assignment-*.md")):
        assigns[int(read_fm(p)["week"])] = p.name
    midterm = int(read_fm(ROOT / "assessments" / "midterm" / "midterm-exam.md")["week"])
    final = int(read_fm(ROOT / "assessments" / "final" / "final-exam.md")["week"])
    return lectures, labs, quizzes, assigns, midterm, final


# --------------------------------------------------------------- C1 weeks
def c1(student):
    section("C1 - exactly 16 weeks, ordered")
    weeks = [int(m) for m in re.findall(r"^## Week (\d+)", student, re.M)]
    check(weeks == list(range(1, 17)),
          "student view has exactly Weeks 1..16 in order",
          f"student view weeks wrong: {weeks}")


# --------------------------------------------------------------- C2 lectures
def c2(student, lectures):
    section("C2 - exactly 32 lectures, no gaps or duplicates")
    ids = re.findall(r"\*\*(L\d{2})\*\*", student)
    nums = sorted(int(x[1:]) for x in set(ids))
    check(len(ids) == 32 and nums == list(range(1, 33)),
          "32 lecture anchors L01..L32, each exactly once",
          f"lecture anchors wrong: {len(ids)} found, nums={nums}")
    # Titles and weeks must match finalized front matter (staleness check).
    stale = []
    for n in range(1, 33):
        block = re.search(
            rf"\*\*L{n:02d}\*\* \| \[([^\]]+)\]", student)
        if not block or block.group(1) != lectures[n]["title"]:
            stale.append(n)
    check(not stale,
          "every calendar lecture title matches finalized front matter",
          f"stale/mismatched lecture titles for L: {stale}")


# --------------------------------------------------------------- C3 labs
def c3(student, labs):
    section("C3 - lab alignment with docs/labs front matter")
    ok = True
    for n, lab in labs.items():
        pat = rf"\[{lab_id(n)}\]"
        week_block = re.search(rf"## Week {lab['week']}\n(.*?)(?=\n## Week |\Z)",
                               student, re.S)
        if not week_block or not re.search(pat, week_block.group(1)):
            ok = False
            FINDINGS.append(f"Lab-{n:02d} not in its week-{lab['week']} row")
            print(f"  FAIL  Lab-{n:02d} missing from Week {lab['week']}")
    if ok:
        print(f"  PASS  all {len(labs)} labs appear in their front-matter weeks")


def lab_id(n):
    return f"Lab-{n:02d}"


# --------------------------------------------------------------- C4 assessments
def c4(student, quizzes, assigns, midterm, final):
    section("C4 - assessment alignment")
    ok = True
    graded = [w for w, t in quizzes if t == "graded"]
    for i, w in enumerate(sorted(graded), 1):
        wb = re.search(rf"## Week {w}\n(.*?)(?=\n## Week |\Z)", student, re.S)
        if not wb or f"Quiz {i}" not in wb.group(1):
            ok = False
            FINDINGS.append(f"Quiz {i} (week {w}) missing/misplaced")
    for w in sorted(assigns):
        wb = re.search(rf"## Week {w}\n(.*?)(?=\n## Week |\Z)", student, re.S)
        if not wb or "Assignment" not in wb.group(1):
            ok = False
            FINDINGS.append(f"assignment for week {w} missing")
    for label, w in (("Midterm", midterm), ("Final", final)):
        wb = re.search(rf"## Week {w}\n(.*?)(?=\n## Week |\Z)", student, re.S)
        if not wb or label not in wb.group(1):
            ok = False
            FINDINGS.append(f"{label} not in week {w}")
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    for sid, spec in cfg["case_sets"].items():
        for w in spec["weeks"]:
            wb = re.search(rf"## Week {w}\n(.*?)(?=\n## Week |\Z)", student, re.S)
            if not wb or f"Case Set {sid}" not in wb.group(1):
                ok = False
                FINDINGS.append(f"Case Set {sid} not in week {w}")
    cap_w = len(re.findall(r"Capstone", student))
    check(ok and cap_w >= 8,
          "quizzes, assignments, exams, case sets, capstone window all aligned",
          f"assessment misalignment: {FINDINGS[-4:] if not ok else ''}")
    check("Quiz 5" in student and "Quiz 1" in student,
          "graded quizzes numbered 1..N in chronological order",
          "quiz numbering broken")


# --------------------------------------------------------------- C5 links
def c5(student, instructor):
    section("C5 - calendar link verification")
    broken = []
    links = re.findall(r"\]\(([^)#]+)\)", student)
    for t in links:
        if t.startswith(("http", "mailto:")):
            continue
        if not (STUDENT.parent / t).resolve().exists():
            broken.append(f"student:{t}")
    for t in re.findall(r"\]\((\.\./docs/labs/[^)#]+)\)", instructor):
        if not (INSTRUCTOR.parent / t).resolve().exists():
            broken.append(f"instructor:{t}")
    check(not broken, "all calendar links resolve to real files",
          f"broken links: {broken[:6]}")
    lab_links = set(re.findall(r"\]\(\.\./labs/([^)#]+)\)", student))
    real = {p.name for p in (ROOT / "site-src" / "labs").glob("lab-*.md")}
    check(lab_links - {"index.md"} <= real,
          "lab links point at canonical lab filenames (no guesses)",
          f"non-canonical lab links: {sorted(lab_links - real - {'index.md'})}")


# --------------------------------------------------------------- C6 printable
def c6(printable, lectures):
    section("C6 - printable HTML")
    if not check(printable.exists(), "printable HTML exists",
                 "calendar-printable.html missing"):
        return
    html = printable.read_text(encoding="utf-8")
    rows = len(re.findall(r"<tr>", html)) - 1  # minus header row
    check(rows == 16, f"16 body rows (found {rows})", f"printable rows = {rows}")
    missing = [f"L{n:02d}" for n in range(1, 33) if f">{f'L{n:02d}'}</span>" not in html
               and f">{f'L{n:02d}'}<" not in html]
    check(not missing, "all 32 lectures present in printable view",
          f"printable missing lectures: {missing}")
    check("Print / Save as PDF" in html and "@media print" in html,
          "print stylesheet + print button present",
          "printability features missing")
    check("viewport" in html, "responsive viewport meta present",
          "viewport meta missing")


# --------------------------------------------------------------- C7 instructor
def c7(instructor, cfg):
    section("C7 - instructor planning view")
    if not check(bool(instructor), "instructor view exists",
                 "calendar-instructor.md missing"):
        return
    rows = re.findall(r"^\| (\d+) \|", instructor, re.M)
    check([int(r) for r in rows] == list(range(1, 17)),
          "16 week rows in instructor view", "instructor rows wrong")
    for lab, pract in cfg["graded_practicals"].items():
        num = lab.split("-")[1]
        wb = re.search(rf"^\| \d+ \|[^|]*\|[^|]*\|[^|]*\| \[[^\]]*\]\(\.\./docs/labs/lab-{num}-[^)]+\)\s*\*\*Pract-{pract}", instructor, re.M)
        check(bool(wb), f"{lab} flagged as Pract-{pract}",
              f"practical flag missing for {lab}")
    check("instructor/answer-keys/" in instructor,
          "notes reference key locations (repo doc, not site)",
          "expected planning notes missing")


# --------------------------------------------------------------- C8 freshness
def c8():
    section("C8 - generation instructions & freshness")
    gen_newer = (GENERATOR.stat().st_mtime > STUDENT.stat().st_mtime)
    check(not gen_newer, "generated outputs are newer than the generator",
          "generator changed after last generation - regenerate the calendar")
    cfg_newer = CONFIG.stat().st_mtime > STUDENT.stat().st_mtime
    check(not cfg_newer, "generated outputs are newer than the config",
          "config changed after last generation - regenerate the calendar")
    check("generate_calendar.py" in GENERATOR.read_text(encoding="utf-8"),
          "generation instructions embedded in generator docstring",
          "docstring missing")
    instr = (ROOT / "docs-meta" / "calendar-instructions.md")
    check(instr.exists(),
          "docs-meta/calendar-instructions.md documents generation steps",
          "calendar-instructions.md missing")


def c9(cfg, labs, syllabus_text):
    """C9 - graded-practical set must agree with the syllabus and lab weeks."""
    section("C9 - graded-practical cross-artifact agreement")
    ok = True
    for lab, pract in cfg["graded_practicals"].items():
        num = int(lab.split("-")[1])
        lw = labs[num]["week"]
        m = re.search(rf"Pract-{pract} \(W(\d+)\)", syllabus_text)
        if not m:
            ok = False
            FINDINGS.append(f"Pract-{pract} not found in syllabus")
            continue
        if int(m.group(1)) != lw:
            ok = False
            FINDINGS.append(f"{lab} (Pract-{pract}) week {lw} != syllabus W{m.group(1)}")
    # every graded practical lab must carry its Pract-N in its handout
    for lab, pract in cfg["graded_practicals"].items():
        num = int(lab.split("-")[1])
        handouts = list((ROOT / "docs" / "labs").glob(f"lab-{num:02d}-*.md"))
        if not handouts or f"Pract-{pract}" not in handouts[0].read_text(encoding="utf-8"):
            ok = False
            FINDINGS.append(f"{lab} handout missing Pract-{pract} marker")
    check(ok, "config/syllabus/handout practical numbering agree",
          f"practical cross-check failed: {FINDINGS[-4:]}")


def main():
    if not STUDENT.exists():
        print("FAIL: calendar-generated.md missing - run generate_calendar.py")
        sys.exit(1)
    lectures, labs, quizzes, assigns, midterm, final = parse_sources()
    student = STUDENT.read_text(encoding="utf-8")
    printable = PRINTABLE if PRINTABLE.exists() else None
    instructor = INSTRUCTOR if INSTRUCTOR.exists() else None
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    c1(student)
    c2(student, lectures)
    c3(student, labs)
    c4(student, quizzes, assigns, midterm, final)
    c5(student, instructor.read_text(encoding="utf-8") if instructor else "")
    c6(printable, lectures)
    c7(instructor.read_text(encoding="utf-8") if instructor else "", cfg)
    c8()
    c9(cfg, labs, (ROOT / "syllabus" / "syllabus.md").read_text(encoding="utf-8"))
    print("\n" + "=" * 50)
    if FINDINGS:
        print(f"FAIL: {len(FINDINGS)} finding(s)")
        for f in FINDINGS:
            print(f"  - {f}")
        sys.exit(1)
    print("OK: calendar validation passed (C1-C9)")


if __name__ == "__main__":
    main()
