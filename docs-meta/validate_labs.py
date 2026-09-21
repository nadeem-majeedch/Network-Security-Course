#!/usr/bin/env python3
"""Lab-layer validation for the Network Security Course.

  B1  16 lab handouts Lab-01..Lab-16, weeks 1..16, no gaps/duplicates
  B2  every handout carries all 16 required sections
  B3  front-matter completeness (lab, week, clos, lectures, duration, key link)
  B4  16 instructor answer keys, substantive, instructor-only flagged
  B5  separation (student handouts clean; keys flagged; key links resolve)
  B6  no placeholder-only handouts marked complete
  B7  CLO mapping matches the syllabus matrix expectations
  B8  lab-to-lecture alignment (weeks -> lectures, files exist)
  B9  datasets present with matching SHA256SUMS
  B10 safety content present in every handout

Exit 0 = all checks pass.
"""
from pathlib import Path
import hashlib
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
LABS = ROOT / "docs" / "labs"
KEYS = ROOT / "teaching" / "lab-answer-keys"
DATASETS = LABS / "datasets"

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


SECTIONS = [
    "Lab Overview & CLO Mapping", "Learning Objectives", "Prerequisites",
    "Estimated Duration", "Required Software & Hardware", "Setup Instructions",
    "Authorization & Safety Notes", "Student Tasks", "Expected Observations",
    "Analysis Questions", "Troubleshooting", "Cleanup Instructions",
    "Submission Requirements", "Expected Output & Evidence", "Grading Rubric",
    "Instructor Answer Key",
]
WEEK_LECTURES = {
    1: ["L01", "L02"], 2: ["L03", "L04"], 3: ["L05", "L06"], 4: ["L07", "L08"],
    5: ["L09", "L12"], 6: ["L10", "L11"], 7: ["L13", "L14"], 8: ["L15", "L16"],
    9: ["L17", "L19"], 10: ["L18", "L20"], 11: ["L21", "L22"], 12: ["L23", "L24"],
    13: ["L25", "L26"], 14: ["L27", "L28"], 15: ["L29", "L30"], 16: ["L31", "L32"],
}
PRIMARY_CLO = {1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 4, 7: 6, 8: 7, 9: 8, 10: 8,
               11: 9, 12: 10, 13: 11, 14: 11, 15: 14, 16: 11}
REQUIRED_EXTRA_CLO = {10: [13], 12: [9], 14: [12], 16: [14, 15]}

# B1: handouts exist, numbered, weeks correct
handouts: dict[int, Path] = {}
for p in LABS.glob("lab-*.md"):
    m = re.match(r"lab-(\d+)-", p.name)
    if m:
        handouts[int(m.group(1))] = p
check("B1a", "16 lab handouts present", len(handouts) == 16, f"found {len(handouts)}")
weeks_bad = []
for n, p in handouts.items():
    w = int(re.search(r"week:\s*(\d+)", p.read_text(encoding="utf-8")).group(1))
    if w != n:
        weeks_bad.append(f"lab-{n:02d}: week {w}")
check("B1b", "weeks 1..16 aligned to file numbers", not weeks_bad, f"{weeks_bad}" if weeks_bad else "")

# B2: all 16 sections present
sec_bad = []
for n, p in sorted(handouts.items()):
    b = body(p.read_text(encoding="utf-8"))
    absent = [s for s in SECTIONS if not re.search(rf"^##\s+\d+\.\s+{re.escape(s)}", b, re.M)]
    if absent:
        sec_bad.append(f"lab-{n:02d}: {absent}")
check("B2", "all 16 required sections in every handout", not sec_bad,
      f"{sec_bad[:4]}{'…' if len(sec_bad) > 4 else ''}" if sec_bad else "")

# B3: front matter completeness
fm_bad = []
for n, p in sorted(handouts.items()):
    f = fm(p.read_text(encoding="utf-8"))
    missing = [k for k in ["lab", "week", "clos", "lectures", "duration", "instructor-key", "status", "artifact-type"] if not f.get(k)]
    if f.get("artifact-type") != "student-lab-handout":
        missing.append("artifact-type")
    if missing:
        fm_bad.append(f"lab-{n:02d}: {missing}")
check("B3", "front matter complete in every handout", not fm_bad, f"{fm_bad}" if fm_bad else "")

# B4: answer keys
keys: dict[int, Path] = {}
for p in KEYS.glob("lab-*-answer-key.md"):
    m = re.match(r"lab-(\d+)-", p.name)
    if m:
        keys[int(m.group(1))] = p
check("B4a", "16 answer keys present", len(keys) == 16, f"found {len(keys)}")
key_bad = []
for n, p in keys.items():
    t = p.read_text(encoding="utf-8")
    if "instructor-only: true" not in t:
        key_bad.append(f"lab-{n:02d}: not flagged instructor-only")
    for pat in ["model answers|expected corroboration|expected decision points|expected scope",
                "Grading notes|grading anchor", "Command status"]:
        if not re.search(pat, t, re.I):
            key_bad.append(f"lab-{n:02d}: missing ~{pat}")
check("B4b", "keys substantive + flagged", not key_bad, f"{key_bad}" if key_bad else "")

# B5: separation + key links resolve
leak = []
for n, p in handouts.items():
    t = p.read_text(encoding="utf-8")
    if re.search(r"INSTRUCTOR ONLY|instructor-only: true", t):
        leak.append(f"lab-{n:02d}")
check("B5a", "handouts contain no instructor-only material", not leak, f"{leak}" if leak else "")
link_bad = []
for n, p in sorted(handouts.items()):
    f = fm(p.read_text(encoding="utf-8"))
    key = f.get("instructor-key", "")
    if not key or not (ROOT / key).exists():
        link_bad.append(f"lab-{n:02d}: {key or 'none'}")
check("B5b", "instructor-key links resolve", not link_bad, f"{link_bad}" if link_bad else "")

# B6: placeholders in complete handouts
ph = []
for n, p in handouts.items():
    t = p.read_text(encoding="utf-8")
    if fm(t).get("status") == "complete":
        hits = re.findall(r"\b(TODO|TBD|FIXME|PLACEHOLDER|LOREM)\b", body(t), re.I)
        if hits:
            ph.append(f"lab-{n:02d}: {len(hits)}")
check("B6", "no placeholder markers in handouts marked complete", not ph, f"{ph}" if ph else "")

# B7: CLO mapping vs syllabus matrix
clo_bad = []
for n, p in sorted(handouts.items()):
    f = fm(p.read_text(encoding="utf-8"))
    clos = [int(c) for c in re.findall(r"CLO-(\d+)", f.get("clos", ""))]
    if PRIMARY_CLO[n] not in clos:
        clo_bad.append(f"lab-{n:02d}: missing primary CLO-{PRIMARY_CLO[n]}")
    for c in REQUIRED_EXTRA_CLO.get(n, []):
        if c not in clos:
            clo_bad.append(f"lab-{n:02d}: missing required CLO-{c}")
check("B7", "CLO mapping matches syllabus matrix", not clo_bad, f"{clo_bad}" if clo_bad else "")

# B8: lab-to-lecture alignment
align_bad = []
for n, p in sorted(handouts.items()):
    f = fm(p.read_text(encoding="utf-8"))
    lectures = [int(x) for x in re.findall(r"L(\d+)", f.get("lectures", ""))]
    exp = [int(x[1:]) for x in WEEK_LECTURES[n]]
    if sorted(lectures) != sorted(exp):
        align_bad.append(f"lab-{n:02d}: lectures {lectures} != week {n} {exp}")
        continue
    for lid in exp:
        plan = list((ROOT / "modules").glob(f"module-*/lectures/lecture-{lid:02d}-*.md"))
        student = list((ROOT / "docs" / "lectures").glob(f"lecture-{lid:02d}-*.md"))
        if not plan or not student:
            align_bad.append(f"lab-{n:02d}: L{lid:02d} plan/student page missing")
check("B8", "every lab maps to its week's lectures with existing files", not align_bad,
      f"{align_bad}" if align_bad else "")

# B9: datasets + checksums
sums = DATASETS / "SHA256SUMS"
if not sums.exists():
    check("B9", "datasets with SHA256SUMS", False, "SHA256SUMS missing")
else:
    bad = []
    for line in sums.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        h, name = line.split(None, 1)
        f = DATASETS / name.strip()
        if not f.exists() or hashlib.sha256(f.read_bytes()).hexdigest() != h:
            bad.append(name.strip())
    check("B9", "datasets present, checksums match", not bad, f"{bad}" if bad else f"{len(sums.read_text(encoding='utf-8').splitlines())} files verified")

# B10: safety content
safety_bad = []
for n, p in sorted(handouts.items()):
    b = body(p.read_text(encoding="utf-8"))
    m = re.search(r"^##\s+7\.\s+Authorization & Safety Notes(.*?)(?=^##\s+\d+\.)", b, re.S | re.M)
    if not m or not re.search(r"authoriz", m.group(1), re.I) or not re.search(r"\bonly\b", m.group(1), re.I):
        safety_bad.append(f"lab-{n:02d}")
check("B10", "authorization/safety content present in every handout", not safety_bad,
      f"{safety_bad}" if safety_bad else "")

print(f"\n{'=' * 60}")
print(f"TOTAL: {len(passes) + len(failures)} checks — {len(passes)} passed, {len(failures)} failed")
sys.exit(1 if failures else 0)
