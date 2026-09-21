#!/usr/bin/env python3
"""Plan-level validation for the Network Security Course governance documents.

Checks (Mission validation requirements):
  V1  exactly 32 planned lectures (L01..L32, no gaps/duplicates)
  V2  exactly 8 modules
  V3  total contact hours = 64 (32 x 2)
  V4  CLO coverage: CLO-1..CLO-15 each taught and assessed
  V5  student/instructor separation conventions defined (instructor/ tree + Pages exclusion)
  V6  >= 100 case studies planned (documented requirement + tracker plan)
  V7  16-week schedule and 16 labs present
  V8  assessment plan references quizzes 1-5, assignments 1-7, midterm, final, capstone

Usage: python3 docs-meta/validate_plan.py
Exit code 0 = all checks pass, 1 = at least one failure.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ARCH = ROOT / "course-architecture.md"
REQ = ROOT / "course-requirements.md"
ROAD = ROOT / "implementation-roadmap.md"

failures = []


def check(name, condition, observed):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {name}: observed = {observed}")
    if not condition:
        failures.append(name)


def section(text, heading_pattern):
    """Return the text under a markdown heading until the next heading of the
    same or higher level (level = number of leading '#')."""
    m = re.search(heading_pattern, text, re.M)
    if not m:
        return ""
    start = m.start()
    level = len(re.match(r"^(#+) ", text[start:]).group(1))
    nxt = re.search(r"^#{1,%d} " % level, text[m.end():], re.M)
    end = m.end() + nxt.start() if nxt else len(text)
    return text[start:end]


def main():
    arch = ARCH.read_text(encoding="utf-8")
    req = REQ.read_text(encoding="utf-8")
    road = ROAD.read_text(encoding="utf-8")

    # V1: exactly 32 lectures L01..L32 from the master lecture map (sections 3.x)
    master = section(arch, r"^## 3\. Master Lecture Map")
    lec_rows = re.findall(r"^\| L(\d{2}) \|", master, re.M)
    lec_nums = [int(n) for n in lec_rows]
    check("V1a lecture rows found in master map", len(lec_nums) == 32, len(lec_nums))
    check("V1b lecture ids are exactly 01..32", sorted(lec_nums) == list(range(1, 33)), sorted(set(lec_nums)))
    check("V1c no duplicate lecture ids", len(lec_nums) == len(set(lec_nums)), f"{len(lec_nums)} vs {len(set(lec_nums))}")

    # V2: exactly 8 modules
    module_heads = re.findall(r"^### Module (\d) ", arch, re.M)
    check("V2 module sections", sorted(map(int, module_heads)) == list(range(1, 9)), module_heads)

    # V3: hours = lectures x 2 (per-lecture duration stated in requirements)
    check("V3a requirements state 2 hours per lecture", "| Lecture length | 2 hours each |" in req, "found" if "| Lecture length | 2 hours each |" in req else "missing")
    hours = len(lec_nums) * 2
    check("V3b computed contact hours = 64", hours == 64, hours)

    # V4: CLO coverage matrix has CLO-1..CLO-15 all covered
    clo_sec = section(arch, r"^## 4\. CLO ")
    clo_rows = re.findall(r"^\| CLO-(\d+) \|", clo_sec, re.M)
    clo_covered = re.findall(r"^\| CLO-(\d+) \|.*\|\s*✅\s*\|", clo_sec, re.M)
    check("V4a all 15 CLOs present in matrix", sorted(map(int, clo_rows)) == list(range(1, 16)), sorted(set(map(int, clo_rows))))
    check("V4b all 15 CLOs marked covered", sorted(map(int, clo_covered)) == list(range(1, 16)), sorted(set(map(int, clo_covered))))

    # V5: separation conventions defined
    check("V5a instructor-only tree defined in requirements", "instructor/" in req and "INSTRUCTOR-ONLY" in req.upper(), "found")
    check("V5b Pages exclusion rule stated", "excludes `instructor/`" in arch or "excluded" in req, "found")
    check("V5c answer-key pairing rule stated", "answer-keys" in req, "found")

    # V6: >= 100 case studies planned
    check("V6a requirement states >= 100 case studies", ("**≥ 100**" in req or "Minimum 100" in req), "found")
    check("V6b architecture references the case-study tracker", "case-study-tracker.md" in arch, "found")
    tracker_exists = (ROOT / "case-study-tracker.md").exists() or (ROOT.parent / "docs-meta" / "case-study-tracker.md").exists()
    check("V6c tracker file exists (P1 deliverable)", tracker_exists, tracker_exists)

    # V7: weekly schedule = 16 weeks, 16 labs
    sched = section(arch, r"^## 5\. Weekly Schedule")
    week_rows = re.findall(r"^\| (\d+) \|", sched, re.M)
    check("V7a 16 weekly rows in schedule", sorted(map(int, week_rows)) == list(range(1, 17)), sorted(set(map(int, week_rows))))
    labs = set(re.findall(r"Lab-(\d{2})", sched))
    check("V7b labs 01..16 all scheduled", sorted(map(int, labs)) == list(range(1, 17)), sorted(labs))

    # V8: assessment plan completeness
    check("V8a quizzes 1-5 referenced", set(map(int, re.findall(r"Quiz (\d)", arch))) == {1, 2, 3, 4, 5}, sorted(set(re.findall(r"Quiz (\d)", arch))))
    check("V8b assignments 1-7 referenced", set(map(int, re.findall(r"Assignment (\d)", arch))) == {1, 2, 3, 4, 5, 6, 7}, sorted(set(re.findall(r"Assignment (\d)", arch))))
    check("V8c midterm + final + capstone present", all(s in arch for s in ("Midterm", "Final", "Capstone")), "found")

    # Scope coverage: all 16 mandated topic areas mapped in architecture section 8
    scope = section(arch, r"^## 8\. Compliance Check")
    topic_rows = re.findall(r"^\| ([A-Z][^|]+)\|.*?(?:L\d|M\d)", scope, re.M)
    check("Scope: 16 mandated topic areas mapped", len(topic_rows) == 16, len(topic_rows))

    print()
    if failures:
        print(f"RESULT: {len(failures)} check(s) FAILED -> {failures}")
        return 1
    print("RESULT: all plan-level checks PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
