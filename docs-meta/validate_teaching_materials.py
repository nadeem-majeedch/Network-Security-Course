#!/usr/bin/env python3
"""Teaching-material validation for the Network Security Course.

Validates the mission's four requirements:
  T1  all 32 lectures have speaker notes (L01..L32, no gaps/duplicates)
  T2  speaker notes are substantive (all 9 delivery sections, length floor)
  T3  eight module answer keys exist, cover their lectures, carry model-answer sections
  T4  instructor manual covers all mandated elements
  T5  instructor/student separation (teaching/ flagged; student trees clean)
  T6  32 student pages with required structure + plan links resolve
  T7  no placeholder-only pages marked complete
  T8  references + CLO mapping substantive in every student page
  T9  speaker-note Links sections point at real files

Exit code 0 = all checks pass. Results are printed as PASS/FAIL lines.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTES = ROOT / "teaching" / "speaker-notes"
KEYS = ROOT / "teaching" / "answer-keys"
MANUAL = ROOT / "teaching" / "instructor-manual"
STUDENT = ROOT / "docs" / "lectures"

failures: list[str] = []
passes: list[str] = []


def check(cid: str, desc: str, ok: bool, detail: str = "") -> None:
    (passes if ok else failures).append(f"{cid} {desc}" + (f" — {detail}" if detail else ""))
    print(f"{'PASS' if ok else 'FAIL'}  {cid}  {desc}" + (f" — {detail}" if detail else ""))


def fm(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    out: dict = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                out[k.strip()] = v.strip()
    return out


def body(text: str) -> str:
    m = re.match(r"^---\n.*?\n---\n", text, re.S)
    return text[m.end():] if m else text


LECTURE_IDS = [f"L{n:02d}" for n in range(1, 33)]
NOTE_SECTIONS = [
    "Delivery Guide", "Timing Plan", "Teaching Demonstrations",
    "Expected Student Difficulties", "Discussion Facilitation",
    "Lab Troubleshooting", "Accessibility Notes",
    "CS & Data Science Applications", "Links",
]
STUDENT_SECTIONS = [
    "Detailed Explanations", "Key Definitions", "Network Diagram",
    "Protocol Examples", "Configuration Concepts", "Security Implications",
    "Realistic Organizational Scenario", "Common Misconceptions",
    "Classroom Activities", "Problem-Solving Questions", "Exit Ticket",
    "References", "CLO Mapping",
]
MODULE_LECTURES = {
    1: ["L01", "L02", "L03", "L04"], 2: ["L05", "L06", "L07", "L08"],
    3: ["L09", "L10", "L11", "L12"], 4: ["L13", "L14", "L15", "L16"],
    5: ["L17", "L18", "L19", "L20"], 6: ["L21", "L22", "L23", "L24"],
    7: ["L25", "L26", "L27", "L28"], 8: ["L29", "L30", "L31", "L32"],
}

# T1: speaker notes exist, complete, unique
notes: dict[str, Path] = {}
for p in NOTES.glob("lecture-*.md"):
    t = p.read_text(encoding="utf-8")
    lid = fm(t).get("lecture", "")
    if lid:
        notes[lid] = p
check("T1a", "32 speaker notes present", len(notes) == 32, f"found {len(notes)}")
missing = [i for i in LECTURE_IDS if i not in notes]
check("T1b", "no gaps in L01..L32", not missing, f"missing {missing}" if missing else "")
dupes = []
for p in NOTES.glob("lecture-*.md"):
    t = p.read_text(encoding="utf-8")
    if list(fm(t).get("lecture", "")) and p.name != notes.get(fm(t).get("lecture", ""), p).name:
        dupes.append(p.name)
check("T1c", "no duplicate lecture numbering", not dupes, f"{dupes}" if dupes else "")

# T2: substantive notes
bad_secs, bad_len = [], []
for lid in LECTURE_IDS:
    p = notes.get(lid)
    if not p:
        continue
    t = p.read_text(encoding="utf-8")
    b = body(t)
    if len(b.splitlines()) < 40:
        bad_len.append(lid)
    absent = [s for s in NOTE_SECTIONS if not re.search(rf"^##\s+{re.escape(s)}", b, re.M)]
    if absent:
        bad_secs.append(f"{lid}:{','.join(absent)}")
check("T2a", "all 9 delivery sections in every note", not bad_secs, f"{bad_secs}" if bad_secs else "")
check("T2b", "length floor (>=40 body lines) in every note", not bad_len, f"{bad_len}" if bad_len else "")

# T3: answer keys
keys_found = sorted(KEYS.glob("answer-key-module-*.md"))
check("T3a", "8 module answer keys present", len(keys_found) == 8, f"found {len(keys_found)}")
key_issues = []
for p in keys_found:
    t = p.read_text(encoding="utf-8")
    mmod = re.search(r"module:\s*(\d+)", t)
    if not mmod:
        key_issues.append(f"{p.name}: no module id")
        continue
    mod = int(mmod.group(1))
    for lid in MODULE_LECTURES[mod]:
        if lid not in t:
            key_issues.append(f"{p.name}: missing {lid}")
    for sec in ["Formative checks", "Exit ticket", "isconception"]:
        if not re.search(sec, t):
            key_issues.append(f"{p.name}: missing section ~{sec}")
check("T3b", "keys cover their 4 lectures + model-answer sections", not key_issues, f"{key_issues}" if key_issues else "")

# T4: instructor manual coverage
manual_texts = {p.name: p.read_text(encoding="utf-8") for p in MANUAL.glob("*.md")}
all_manual = "\n".join(manual_texts.values())
required_manual_files = ["README.md", "delivery-guide.md", "demonstrations-and-difficulties.md",
                         "facilitation-and-troubleshooting.md", "model-answers-index.md",
                         "accessibility.md", "cs-ds-applications.md"]
missing_mf = [f for f in required_manual_files if f not in manual_texts]
check("T4a", "all 7 manual files present", not missing_mf, f"missing {missing_mf}" if missing_mf else "")
manual_topics = {
    "delivery guide": r"Delivery Guide|delivery guide",
    "suggested timing": r"[Tt]iming",
    "speaker notes index": r"speaker-notes",
    "demonstrations": r"[Dd]emonstration",
    "student difficulties": r"[Dd]ifficult",
    "misconception bank": r"[Mm]isconception [Bb]ank",
    "discussion facilitation": r"[Ff]acilitation",
    "lab troubleshooting": r"[Tt]roubleshooting",
    "model answers": r"[Mm]odel [Aa]nswer",
    "accessibility": r"[Aa]ccessibility",
    "CS/DS applications": r"Data Science|Data-Science",
}
missing_topics = [k for k, pat in manual_topics.items() if not re.search(pat, all_manual)]
check("T4b", "all 11 mandated manual elements covered", not missing_topics, f"missing {missing_topics}" if missing_topics else "")

# T5: separation
unflagged = []
for p in list(NOTES.glob("*.md")) + list(KEYS.glob("*.md")) + list(MANUAL.glob("*.md")):
    if "instructor-only: true" not in p.read_text(encoding="utf-8"):
        unflagged.append(str(p.relative_to(ROOT)))
check("T5a", "every teaching/ file flagged instructor-only", not unflagged, f"{unflagged}" if unflagged else "")
leak = []
for p in STUDENT.glob("*.md"):
    t = p.read_text(encoding="utf-8")
    if re.search(r"instructor-only|INSTRUCTOR ONLY", t):
        leak.append(str(p.relative_to(ROOT)))
for p in (ROOT / "syllabus").glob("*.md"):
    if re.search(r"INSTRUCTOR ONLY", p.read_text(encoding="utf-8")):
        leak.append(str(p.relative_to(ROOT)))
check("T5b", "student trees contain no instructor-only material", not leak, f"{leak}" if leak else "")

# T6: student pages structure + plan links
students: dict[str, Path] = {}
for p in STUDENT.glob("lecture-*.md"):
    t = p.read_text(encoding="utf-8")
    lid = fm(t).get("lecture", "")
    if lid:
        students[lid] = p
check("T6a", "32 student pages present", len(students) == 32, f"found {len(students)}")
miss_s = [i for i in LECTURE_IDS if i not in students]
check("T6b", "student pages L01..L32 complete", not miss_s, f"missing {miss_s}" if miss_s else "")
struct_issues = []
for lid in LECTURE_IDS:
    p = students.get(lid)
    if not p:
        continue
    t = p.read_text(encoding="utf-8")
    f = fm(t)
    if f.get("status") != "complete":
        struct_issues.append(f"{lid}: status != complete")
    if f.get("artifact-type") != "student-lecture-material":
        struct_issues.append(f"{lid}: wrong artifact-type")
    plan = f.get("instructor-plan", "")
    if not plan or not (ROOT / plan).exists():
        struct_issues.append(f"{lid}: plan link unresolved ({plan or 'none'})")
    b = body(t)
    absent = [s for s in STUDENT_SECTIONS if not re.search(rf"^##\s+\d+\.\s+.*{re.escape(s)}", b, re.M)]
    if absent:
        struct_issues.append(f"{lid}: sections {absent}")
check("T6c", "front-matter, plan links, 13 required sections in every student page", not struct_issues,
      f"{struct_issues[:6]}{'…' if len(struct_issues) > 6 else ''}" if struct_issues else "")

# T7: placeholders in complete pages
placeholder_pat = re.compile(r"\b(TODO|TBD|FIXME|PLACEHOLDER|LOREM)\b", re.I)
ph = []
for lid, p in students.items():
    t = p.read_text(encoding="utf-8")
    if fm(t).get("status") == "complete":
        hits = placeholder_pat.findall(body(t))
        if hits:
            ph.append(f"{lid}: {len(hits)}")
check("T7a", "no placeholder markers in pages marked complete", not ph, f"{ph}" if ph else "")

# T8: references + CLO mapping substantive
ref_bad, clo_bad = [], []
for lid, p in students.items():
    b = body(p.read_text(encoding="utf-8"))
    m = re.search(r"^##\s+\d+\.\s+References(.*?)(?=^##\s+\d+\.)", b, re.S | re.M)
    if not m or len([ln for ln in m.group(1).splitlines() if ln.strip()]) < 3:
        ref_bad.append(lid)
    m2 = re.search(r"^##\s+\d+\.\s+CLO Mapping(.*?)(?=^##\s+\d+\.|\Z)", b, re.S | re.M)
    if not m2 or not re.search(r"CLO-\d+", m2.group(1)):
        clo_bad.append(lid)
check("T8a", "references substantive (>=3 lines) everywhere", not ref_bad, f"{ref_bad}" if ref_bad else "")
check("T8b", "CLO mapping present everywhere", not clo_bad, f"{clo_bad}" if clo_bad else "")

# T9: speaker-note links resolve
link_bad = []
for lid in LECTURE_IDS:
    p = notes.get(lid)
    if not p:
        continue
    b = body(p.read_text(encoding="utf-8"))
    m = re.search(r"^##\s+Links(.*?)$", b, re.S | re.M)
    if m:
        for path in re.findall(r"`((?:modules|docs|teaching)/[^`]+\.(?:md|py))`", m.group(1)):
            if not (ROOT / path).exists():
                link_bad.append(f"{lid}: {path}")
check("T9a", "speaker-note Links resolve to real files", not link_bad, f"{link_bad}" if link_bad else "")

print(f"\n{'=' * 60}")
print(f"TOTAL: {len(passes) + len(failures)} checks — {len(passes)} passed, {len(failures)} failed")
sys.exit(1 if failures else 0)
