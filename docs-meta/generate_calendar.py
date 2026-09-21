#!/usr/bin/env python3
"""Generate the Network Security Course one-click semester calendar.

Reads the FINALIZED course content (front matter only — never re-states it)
and emits three synchronized views:

  site-src/course/calendar-generated.md   student view (site page, links out)
  docs-meta/calendar-printable.html       printable one-page-per-week HTML
  docs-meta/calendar-instructor.md        instructor planning view (repo doc)
  docs-meta/calendar.ics                  calendar-subscription file (only if
                                          semester.start_date is set)

Sources of truth (read live at generation time):
  modules/*/lectures/lecture-*.md          L01..L32: number, title, week, CLOs
  docs/labs/lab-*.md                       Lab-01..16: week, CLOs, lecture links
  assessments/quizzes/quiz-*.md            graded + self-check weeks
  assessments/assignments/assignment-*.md  A1..A7: week, due, CLOs
  assessments/midterm|final/*.md           exam weeks and coverage
  assessments/capstone/capstone-brief.md   capstone weeks (9..16)
  assessments/case-study-evaluation/...    case-set windows
  docs-meta/calendar-config.json           start date, day pattern, themes

Usage:
  python docs-meta/generate_calendar.py [--config docs-meta/calendar-config.json]

Validation: docs-meta/validate_calendar.py (C1-C8).
"""
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "docs-meta" / "calendar-config.json"

OUT_STUDENT = ROOT / "site-src" / "course" / "calendar-generated.md"
OUT_PRINT = ROOT / "docs-meta" / "calendar-printable.html"
OUT_INSTRUCTOR = ROOT / "docs-meta" / "calendar-instructor.md"
OUT_ICS = ROOT / "docs-meta" / "calendar.ics"

WEEKS = 16

# ----------------------------------------------------------------- parsing
FM_RE = re.compile(r"\A---\n(.*?)\n---", re.S)


def read_fm(path: Path) -> dict:
    """Extract simple `key: value` front matter (no nested structures)."""
    text = path.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    fm = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line and not line.startswith((" ", "#")):
                k, _, v = line.partition(":")
                fm[k.strip()] = v.strip()
    # Title falls back to the first H1.
    if "title" not in fm or not fm.get("title"):
        h1 = re.search(r"^# (.+)$", FM_RE.sub("", text), re.M)
        if h1:
            fm["title"] = h1.group(1).strip()
    return fm


def parse_list(value: str) -> list[str]:
    return re.findall(r"[A-Za-z]+-?\d+", value or "")


def load_all():
    lectures = {}
    for p in sorted((ROOT / "modules").glob("module-*/lectures/lecture-*.md")):
        fm = read_fm(p)
        num = int(re.search(r"\d+", fm["lecture"]).group())
        lectures[num] = {
            "id": fm["lecture"],
            "title": fm.get("title", ""),
            "week": int(fm.get("week", 0)),
            "clos": parse_list(fm.get("clos", "")),
        }

    labs = {}
    for p in sorted((ROOT / "docs" / "labs").glob("lab-*.md")):
        fm = read_fm(p)
        num = int(re.search(r"\d+", fm["lab"]).group())
        labs[num] = {
            "id": fm["lab"],
            "title": fm.get("title", ""),
            "week": int(fm.get("week", 0)),
            "clos": parse_list(fm.get("clos", "")),
            "lectures": parse_list(fm.get("lectures", "")),
        }

    quizzes = {"graded": [], "selfcheck": {}}
    for p in sorted((ROOT / "assessments" / "quizzes").glob("quiz-*.md")):
        fm = read_fm(p)
        week = int(fm.get("week", 0))
        if fm.get("type") == "graded":
            quizzes["graded"].append(week)
        else:
            quizzes["selfcheck"][week] = quizzes["selfcheck"].get(week, 0) + 1
    quizzes["graded"].sort()
    quizzes["graded_num"] = {w: i + 1 for i, w in enumerate(quizzes["graded"])}

    assignments = []
    for p in sorted((ROOT / "assessments" / "assignments").glob("assignment-*.md")):
        fm = read_fm(p)
        assignments.append({
            "num": len(assignments) + 1,
            "file": p.name,
            "week": int(fm.get("week", 0)),
            "due": fm.get("due", f"end of week {fm.get('week', '?')}"),
            "clos": parse_list(fm.get("clos", "")),
        })

    midterm = read_fm(ROOT / "assessments" / "midterm" / "midterm-exam.md")
    final = read_fm(ROOT / "assessments" / "final" / "final-exam.md")
    return lectures, labs, quizzes, assignments, midterm, final


def build_weeks(lectures, labs, quizzes, assignments, midterm, final, cfg):
    """One record per week: the single reconciled schedule."""
    weeks = {w: {"lectures": [], "items": [], "clos": set()} for w in range(1, WEEKS + 1)}
    for n in sorted(lectures):
        lec = lectures[n]
        weeks[lec["week"]]["lectures"].append(n)
        weeks[lec["week"]]["clos"].update(lec["clos"])
    for n in sorted(labs):
        lab = labs[n]
        weeks[lab["week"]]["items"].append(("lab", lab["id"], lab["title"], lab["clos"]))
        weeks[lab["week"]]["clos"].update(lab["clos"])
    for w in sorted(quizzes["graded_num"]):
        weeks[w]["items"].append(("quiz", f"Quiz {quizzes['graded_num'][w]}", "Graded quiz, in-class, 20 min", []))
    for w, count in quizzes["selfcheck"].items():
        weeks[w]["items"].append(("selfcheck", "Self-check", "Ungraded weekly self-check quiz", []))
    for a in assignments:
        weeks[a["week"]]["items"].append(("assignment", f"Assignment {a['num']}", f"Released; {a['due']}", a["clos"]))
    mw = int(midterm["week"])
    weeks[mw]["items"].append(("exam", "Midterm", "Written exam, modules 1-4", parse_list(midterm.get("clos", ""))))
    fw = int(final["week"])
    weeks[fw]["items"].append(("exam", "Final", "Written synthesis + forensic practical", parse_list(final.get("clos", ""))))
    for w in range(9, 17):
        weeks[w]["items"].append(("capstone", "Capstone", "Capstone window (brief W9 - defense W16)", []))
    for set_id, spec in cfg["case_sets"].items():
        for w in spec["weeks"]:
            weeks[w]["items"].append(("caseset", f"Case Set {set_id}", spec["tier_mix"], spec["clos"]))
    return weeks


# ----------------------------------------------------------------- dates
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def week_dates(cfg):
    """Real dates per week when start_date is configured; else None."""
    start = cfg["semester"].get("start_date", "").strip()
    if not start:
        return None
    day0 = datetime.strptime(start, "%Y-%m-%d").date()
    if day0.weekday() != 0:
        print(f"NOTE: {start} is a {DAYS[day0.weekday()]}, not a Monday - week 1 starts on this day anyway.")
    pattern = cfg["semester"].get("lecture_days", ["Monday", "Wednesday"])
    idx = [DAYS.index(d) for d in pattern]
    lab_idx = DAYS.index(cfg["semester"]["lab_day"]) if cfg["semester"].get("lab_day") else idx[-1]
    overrides = {int(k): v for k, v in cfg["semester"].get("overrides", {}).items()}
    out = {}
    for w in range(1, WEEKS + 1):
        monday = day0 + timedelta(weeks=w - 1)
        if w in overrides:
            monday = datetime.strptime(overrides[w], "%Y-%m-%d").date()
            if monday.weekday() != 0:
                print(f"NOTE: override for week {w} is a {DAYS[monday.weekday()]}.")
        lec = [(monday + timedelta(days=i)) for i in sorted(idx)]
        lab = monday + timedelta(days=lab_idx)
        out[w] = {"lectures": lec, "lab": lab}
    return out


def fmt(d):
    return d.strftime("%a %d %b %Y") if d else ""


# ----------------------------------------------------------------- student view
_lecture_slug_cache = {}
_lab_slug_cache = {}


def lecture_slug(num: int) -> str:
    """Resolve the canonical lecture filename stem for LNN (never guess)."""
    if not _lecture_slug_cache:
        for p in (ROOT / "modules").glob("module-*/lectures/lecture-*.md"):
            m = re.match(r"lecture-(\d+)-", p.stem)
            _lecture_slug_cache[int(m.group(1))] = p.stem
    return _lecture_slug_cache[num]


def lab_slug(num: str) -> str:
    """Resolve the canonical lab filename stem for Lab-NN (never guess)."""
    if not _lab_slug_cache:
        for p in (ROOT / "docs" / "labs").glob("lab-*.md"):
            _lab_slug_cache[re.search(r"lab-(\d+)", p.name).group(1)] = p.stem
    return _lab_slug_cache.get(num, f"lab-{num}")


def student_view(weeks, lectures, cfg, dates):
    themes = cfg["week_theme"]
    L = []
    L.append("---")
    L.append("status: complete")
    L.append("artifact-type: generated-calendar")
    L.append("instructor-only: false")
    L.append("---")
    L.append("")
    L.append("# Semester Calendar (generated)")
    L.append("")
    sem = cfg["semester"]
    if dates:
        L.append(f"**Semester begins {fmt(dates[1]['lectures'][0])}** - lectures "
                 f"{sem['lecture_days'][0]}/{sem['lecture_days'][1]} {sem['lecture_start']} "
                 f"({sem['lecture_hours']} h each). Dates below update automatically: set "
                 f"`semester.start_date` in `docs-meta/calendar-config.json` and regenerate.")
    else:
        L.append("Two lectures per week (2 hours each), one embedded lab per week. "
                 "Set `semester.start_date` in `docs-meta/calendar-config.json` and regenerate "
                 "to replace relative weeks with real dates.")
    L.append("")
    L.append("> Generated by `docs-meta/generate_calendar.py` from the finalized course "
             "content - do not edit this page by hand; edit the sources or the config.")
    L.append("")
    for w in range(1, WEEKS + 1):
        rec = weeks[w]
        d = dates[w] if dates else None
        head = f"## Week {w}"
        if d:
            a, b = d["lectures"][0], d["lectures"][1]
            head += f" - {a.strftime('%d %b')} & {b.strftime('%d %b %Y')}"
        L.append(head)
        theme = themes.get(str(w), "")
        if theme:
            L.append(f"*{theme}*")
        L.append("")
        L.append("| Session | Lecture | CLOs | Lab & assessment | CLOs |")
        L.append("|---|---|---|---|---|")
        lec_a, lec_b = rec["lectures"][:2]
        lab_items = [i for i in rec["items"] if i[0] == "lab"]
        other = [i for i in rec["items"] if i[0] != "lab"]
        lab_clos = ""
        lab_cell = ""
        if lab_items:
            lab = lab_items[0]
            lab_clos = ", ".join(lab[3])
            lab_cell = f"[{lab[1]}](../labs/{lab_slug(lab[1].split('-')[1])}.md) - {lab[2]}"
            if len(lab_items) > 1:
                lab_cell += f" (+{len(lab_items)-1} more)"
        for slot, n in [(0, lec_a), (1, lec_b)]:
            lec = lectures[n]
            when = ""
            if d:
                when = d["lectures"][slot].strftime("%a:")
            L.append(f"| {when} **{lec['id']}** | [{lec['title']}](../lectures/{lecture_slug(n)}.md) | {', '.join(lec['clos'])} | {lab_cell if slot == 0 else ''} | {lab_clos if slot == 0 else ''} |")
        L.append("| | | | | |")
        for kind, label, desc, clos in other:
            anchors = {
                "quiz": ("../assessment/quizzes.md", "Graded quiz (15 marks, 20 min)"),
                "selfcheck": ("../assessment/quizzes.md", desc),
                "assignment": ("../assessment/assignments.md", desc),
                "exam": ("../assessment/exams.md", desc),
                "capstone": ("../assessment/capstone.md", desc),
                "caseset": ("../cases/index.md", desc),
            }
            href, base_desc = anchors[kind]
            extra = f" - {base_desc}" if desc == base_desc else (f" - {desc}" if desc else "")
            L.append(f"| | {label} | | [{label}]({href}){extra} | {', '.join(clos) if clos else ''} |")
        L.append("")
    L.append("## Legend")
    L.append("")
    L.append("- **L01-L32**: 2-hour lectures; each embeds its week's lab and case-study session - see the [lectures index](../lectures/index.md).")
    L.append("- **Labs** link into the [lab workbook](../labs/index.md) (objectives, setup, authorization notes, submission checklist).")
    L.append("- **Quizzes/self-checks**: see [Quizzes & Self-Checks](../assessment/quizzes.md); **assignments**: [Assignments](../assessment/assignments.md); **exams**: [Examinations](../assessment/exams.md).")
    L.append("- **Case sets A-C** are the graded case rotations - [how case evaluation works](../assessment/index.md); practice with [all 100 cases](../cases/all-cases.md).")
    L.append("- **Capstone** runs weeks 9-16: [capstone project](../assessment/capstone.md).")
    L.append("")
    return "\n".join(L) + "\n"


def slugify_removed():
    raise NotImplementedError


# ----------------------------------------------------------------- printable
def printable_view(weeks, lectures, cfg, dates):
    themes = cfg["week_theme"]
    css = """
    :root { --ink:#1a2433; --muted:#5b6b7f; --line:#d7dee8; --brand:#283593; --chip:#e8eaf6; }
    * { box-sizing:border-box; }
    body { font-family:'Segoe UI',-apple-system,system-ui,sans-serif; color:var(--ink); margin:0; padding:24px; background:#f5f7fa; }
    .toolbar { max-width:900px; margin:0 auto 16px; display:flex; gap:8px; align-items:center; }
    .toolbar button { border:1px solid var(--line); background:#fff; padding:6px 14px; border-radius:6px; cursor:pointer; font-size:14px; }
    .wrap { max-width:900px; margin:0 auto; background:#fff; border:1px solid var(--line); border-radius:10px; padding:28px 32px; }
    h1 { font-size:22px; margin:0 0 4px; color:var(--brand); }
    .meta { color:var(--muted); font-size:13px; margin-bottom:18px; }
    table { width:100%; border-collapse:collapse; font-size:13px; }
    th { background:var(--chip); text-align:left; padding:8px 10px; border:1px solid var(--line); }
    td { padding:8px 10px; border:1px solid var(--line); vertical-align:top; }
    tr { page-break-inside:avoid; }
    .wk { font-weight:700; white-space:nowrap; }
    .theme { color:var(--muted); font-style:italic; font-size:12px; }
    .dates { color:var(--muted); font-size:12px; white-space:nowrap; }
    .lec { font-weight:600; }
    .tag { display:inline-block; padding:1px 7px; border-radius:10px; font-size:11px; margin:1px 2px 1px 0; background:var(--chip); color:var(--brand); white-space:nowrap; }
    .tag.exam { background:#fdecea; color:#b71c1c; font-weight:700; }
    .tag.quiz { background:#fff8e1; color:#8d6e00; font-weight:600; }
    .tag.due { background:#e8f5e9; color:#1b5e20; }
    @media print {
      body { background:#fff; padding:0; font-size:12px; }
      .toolbar { display:none; }
      .wrap { border:none; max-width:none; padding:0; }
      thead { display:table-header-group; }
    }
    """
    rows = []
    for w in range(1, WEEKS + 1):
        rec = weeks[w]
        d = dates[w] if dates else None
        datestr = (f"{d['lectures'][0].strftime('%d %b')} - {d['lectures'][1].strftime('%d %b %Y')}" if d else "")
        lec_cells = []
        for n in rec["lectures"][:2]:
            lec = lectures[n]
            lec_cells.append(f"<span class='lec'>{lec['id']}</span> {lec['title']}"
                             f"<br><span class='theme'>{', '.join(lec['clos'])}</span>")
        lab_cell, assess = [], []
        for kind, label, desc, clos in rec["items"]:
            if kind == "lab":
                lab_cell.append(f"<span class='tag'>{label}</span> {desc}")
            elif kind == "exam":
                assess.append(f"<span class='tag exam'>{label.upper()}</span> {desc}")
            elif kind == "quiz":
                assess.append(f"<span class='tag quiz'>{label}</span> {desc}")
            elif kind == "assignment":
                assess.append(f"<span class='tag due'>{label} released</span> {desc}")
            elif kind == "selfcheck":
                assess.append(f"<span class='tag'>{label}</span>")
            else:
                assess.append(f"<span class='tag'>{label}</span> {desc}")
        rows.append(
            "<tr>"
            f"<td class='wk'>W{w}<br><span class='dates'>{datestr}</span></td>"
            f"<td>{lec_cells[0]}</td><td>{lec_cells[1]}</td>"
            f"<td>{'<br>'.join(lab_cell)}</td>"
            f"<td>{'<br>'.join(assess) or '&mdash;'}</td>"
            "</tr>")
    sem = cfg["semester"]
    gen_date = datetime.now().strftime("%d %b %Y")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Semester Calendar - {sem['course']} ({sem['code']})</title>
<style>{css}</style>
</head>
<body>
<div class="toolbar">
  <button onclick="window.print()">Print / Save as PDF</button>
  <span class="meta">Generated {gen_date} from the finalized course content.</span>
</div>
<div class="wrap">
<h1>{sem['course']} ({sem['code']}) &mdash; 16-Week Semester Calendar</h1>
<div class="meta">{sem['audience']} &middot; 32 lectures &times; 2 h &middot; 16 labs &middot; 100 case studies &middot; capstone with oral defense</div>
<table>
<thead><tr><th>Week</th><th>Lecture A</th><th>Lecture B</th><th>Lab</th><th>Assessment &amp; due items</th></tr></thead>
<tbody>
{chr(10).join(rows)}
</tbody>
</table>
<p class="theme">All scenarios in this course are simulated for education; practical work runs only on the isolated, authorized lab range. Generated by docs-meta/generate_calendar.py &mdash; regenerate after editing calendar-config.json or course content.</p>
</div>
</body>
</html>
"""


# ----------------------------------------------------------------- instructor
def instructor_view(weeks, lectures, labs, assignments, cfg, dates):
    themes = cfg["week_theme"]
    graded_practicals = cfg["graded_practicals"]
    L = []
    L.append("---")
    L.append("artifact-type: instructor-planning-view")
    L.append("instructor-only: false")
    L.append("status: complete")
    L.append("---")
    L.append("")
    L.append("# Instructor Planning Calendar")
    L.append("")
    L.append("> Generated by `docs-meta/generate_calendar.py` alongside the student view "
             "(`site-src/course/calendar-generated.md`) and the printable HTML "
             "(`docs-meta/calendar-printable.html`). Edit sources/config, then regenerate; "
             "never edit the outputs by hand. Contains no answer-key material, so it may "
             "remain in-repo, but treat the working column as planning-sensitive.")
    L.append("")
    if dates:
        sem = cfg["semester"]
        L.append(f"**Semester start:** {fmt(dates[1]['lectures'][0])} - pattern "
                 f"{sem['lecture_days'][0]}/{sem['lecture_days'][1]} at {sem['lecture_start']}.")
        L.append("")
    L.append("| Wk | Dates | Theme | Lectures (CLOs) | In-class lab | Assessment actions for the week |")
    L.append("|---|---|---|---|---|---|")
    for w in range(1, WEEKS + 1):
        rec = weeks[w]
        d = dates[w] if dates else None
        ds = f"{d['lectures'][0].strftime('%d %b')}-{d['lectures'][1].strftime('%d %b')}" if d else "-"
        lec_txt = "; ".join(
            f"{lectures[n]['id']} ({', '.join(lectures[n]['clos'])})" for n in rec["lectures"][:2])
        lab_txt = "-"
        practical_txt = ""
        for kind, label, desc, clos in rec["items"]:
            if kind == "lab":
                num = label.split("-")[1]
                lab_txt = f"[{label}](../docs/labs/{lab_slug(num)}.md)"
                if label in graded_practicals:
                    practical_txt = f" **Pract-{graded_practicals[label]} rubric due**"
        actions = []
        for kind, label, desc, clos in rec["items"]:
            if kind == "quiz":
                actions.append(f"Administer {label} (15 marks); key in instructor/answer-keys/")
            elif kind == "selfcheck":
                actions.append(f"Distribute {label.lower()} (ungraded)")
            elif kind == "assignment":
                actions.append(f"Release {label.lower()}; due {desc.split('; ')[-1]}")
            elif kind == "exam":
                actions.append(f"Administer {label.upper()}; print copies; seating + integrity briefing")
            elif kind == "capstone":
                if w == 9:
                    actions.append("Issue capstone brief; form teams")
                elif w == 15:
                    actions.append("Collect capstone drafts; run peer-review swap")
                elif w == 16:
                    actions.append("Run oral defenses; submit final reports")
            elif kind == "caseset":
                actions.append(f"Run {label} ({desc}); select rotating cases in instructor protocol")
        L.append(f"| {w} | {ds} | {themes.get(str(w), '')} | {lec_txt} | {lab_txt}{practical_txt} | {'<br>'.join(actions) or '-'} |")
    L.append("")
    L.append("## Planning notes")
    L.append("")
    L.append("- **Case Set windows:** " + "; ".join(
        f"Set {k} in weeks {','.join(map(str, v['weeks']))} ({v['tier_mix']})"
        for k, v in cfg["case_sets"].items()) + ".")
    L.append("- **Graded lab practicals (20%):** " + ", ".join(
        f"{k} = Pract-{v}" for k, v in sorted(graded_practicals.items(), key=lambda x: x[1])) + ".")
    L.append("- Assignment due dates follow the briefs' `due:` front matter (all 'end of week N').")
    L.append("- All answer keys and rubric band anchors live in the instructor-only trees; "
             "this view intentionally links nothing into them.")
    L.append("")
    return "\n".join(L) + "\n"


_lab_slug_cache = {}


def lab_slug(num: str) -> str:
    """Resolve the canonical lab filename slug for Lab-NN."""
    if not _lab_slug_cache:
        for p in (ROOT / "docs" / "labs").glob("lab-*.md"):
            _lab_slug_cache[re.search(r"lab-(\d+)", p.name).group(1)] = p.stem
    return _lab_slug_cache.get(num, f"lab-{num}")


# ----------------------------------------------------------------- ICS
def ics_view(weeks, lectures, cfg, dates):
    if not dates:
        return None
    sem = cfg["semester"]
    hh, mm = map(int, sem["lecture_start"].split(":"))
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0",
             "PRODID:-//Network Security Course//Semester Calendar//EN",
             "CALSCALE:GREGORIAN", "METHOD:PUBLISH", "X-WR-CALNAME:Network Security - Semester"]
    def esc(s):
        return s.replace("\\", "\\\\").replace(",", "\\,").replace(";", "\\;")
    for w in range(1, WEEKS + 1):
        d = dates[w]
        for slot, n in enumerate(lectures_sorted(weeks, w)[:2]):
            lec = lectures[n]
            day = d["lectures"][slot]
            start = datetime.combine(day, datetime.min.time()).replace(hour=hh, minute=mm)
            end = start + timedelta(hours=sem["lecture_hours"])
            lines += ["BEGIN:VEVENT",
                      f"UID:nsc-{sem['code'].lower()}-w{w}-l{n:02d}@course.local",
                      f"DTSTAMP:{datetime.now().strftime('%Y%m%dT%H%M%SZ')}",
                      f"DTSTART:{start.strftime('%Y%m%dT%H%M%S')}",
                      f"DTEND:{end.strftime('%Y%m%dT%H%M%S')}",
                      f"SUMMARY:{esc(lec['id'] + ' - ' + lec['title'])}",
                      f"DESCRIPTION:{esc('Week ' + str(w) + ' | CLOs: ' + ', '.join(lec['clos']) + ' | Lab and assessment run inside this lecture block.')}",
                      "END:VEVENT"]
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"


def lectures_sorted(weeks, w):
    return weeks[w]["lectures"]


# ----------------------------------------------------------------- main
def main() -> None:
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    lectures, labs, quizzes, assignments, midterm, final = load_all()
    weeks = build_weeks(lectures, labs, quizzes, assignments, midterm, final, cfg)
    dates = week_dates(cfg)

    OUT_STUDENT.write_text(student_view(weeks, lectures, cfg, dates), encoding="utf-8")
    OUT_PRINT.write_text(printable_view(weeks, lectures, cfg, dates), encoding="utf-8")
    OUT_INSTRUCTOR.write_text(instructor_view(weeks, lectures, labs, assignments, cfg, dates), encoding="utf-8")
    ics = ics_view(weeks, lectures, cfg, dates)
    if ics:
        OUT_ICS.write_text(ics, encoding="utf-8")

    print(f"calendar generated: {OUT_STUDENT.name}, {OUT_PRINT.name}, "
          f"{OUT_INSTRUCTOR.name}" + (f", {OUT_ICS.name}" if ics else " (no ICS: start_date empty)"))


if __name__ == "__main__":
    main()
