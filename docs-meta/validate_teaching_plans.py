#!/usr/bin/env python3
"""Session-2 validation: syllabus + 32 lecture teaching plans.

Mission validation requirements:
  T1  exactly 32 lecture-plan files, ids L01..L32, no gaps/duplicates
  T2  no duplicate lecture numbering; weeks 1..16 with exactly 2 lectures each
  T3  weekly assignment matches the architecture schedule (section 5)
  T4  CLO coverage: union of front-matter CLOs == CLO-1..CLO-15, and per-lecture
      CLOs match the architecture master-map column
  T5  prerequisite progression: every prerequisite lecture id < the lecture's id
  T6  every plan contains the 12 required sections
  T7  plan titles match the architecture master map
  T8  syllabus exists: 16 calendar rows, 15 CLO rows, CLO matrix present
  T9  mission topic coverage: mandated topics located in designated lectures

Generates: docs-meta/teaching-plans-coverage.md (observed results).
Usage: python3 docs-meta/validate_teaching_plans.py   (exit 0 = all pass)
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent          # docs-meta
REPO = ROOT.parent
ARCH = ROOT / "course-architecture.md"
SYLL = REPO / "syllabus" / "syllabus.md"
REPORT = ROOT / "teaching-plans-coverage.md"
MODULES = REPO / "modules"

REQUIRED_SECTIONS = [
    "## 1. Overview & Prerequisites",
    "## 2. Learning Objectives",
    "## 3. Detailed Concepts",
    "## 4. Teaching Sequence (120 Minutes)",
    "## 5. Technical Examples",
    "## 6. Discussion Questions",
    "## 7. Student Activity",
    "## 8. Problem-Solving Case",
    "## 9. Formative Assessment",
    "## 10. Summary & Key Takeaways",
    "## 11. References",
    "## 12. CLO Mapping",
]

# Mission topic -> (lecture ids where the topic must appear, keywords)
TOPIC_KEYWORDS = {
    "Network security foundations": (["L01"], ["CIA", "risk"]),
    "CIA triad, threats, vulnerabilities, risk": (["L01"], ["vulnerab", "threat"]),
    "TCP/IP and OSI security considerations": (["L02"], ["OSI"]),
    "IPv4": (["L02"], ["IPv4"]),
    "IPv6": (["L02"], ["IPv6"]),
    "DNS": (["L03"], ["DNS"]),
    "DHCP": (["L03"], ["DHCP"]),
    "ARP": (["L02"], ["ARP"]),
    "Routing": (["L02", "L03"], ["routing"]),
    "Network services": (["L03"], ["DHCP", "DNS"]),
    "Reconnaissance and threat modeling": (["L05"], ["reconnaissance", "threat model|attack tree"]),
    "Spoofing": (["L06", "L07"], ["spoof"]),
    "Sniffing": (["L07"], ["sniff"]),
    "Denial of service": (["L08"], ["DoS|denial", "flood"]),
    "Firewalls": (["L10"], ["firewall"]),
    "ACLs": (["L11"], ["ACL"]),
    "NAT": (["L12"], ["NAT"]),
    "Proxies": (["L12"], ["proxy"]),
    "Segmentation": (["L09"], ["segmentation"]),
    "Zero trust": (["L09"], ["zero trust"]),
    "Symmetric/asymmetric cryptography": (["L13"], ["symmetric", "asymmetric"]),
    "TLS": (["L14"], ["TLS"]),
    "Certificates": (["L13", "L14"], ["certificate"]),
    "VPNs": (["L15", "L16"], ["VPN"]),
    "IPsec": (["L15"], ["IPsec"]),
    "Secure remote access": (["L16"], ["remote access|remote-access"]),
    "Wireless and enterprise network security": (["L17", "L18"], ["802.11", "802.1X|Enterprise"]),
    "IDS/IPS": (["L22"], ["IDS|IPS|Suricata"]),
    "Network monitoring": (["L21"], ["monitoring|flow"]),
    "Vulnerability assessment": (["L24"], ["scan", "CVSS"]),
    "Network hardening": (["L24"], ["hardening|CIS"]),
    "Cloud networking": (["L19", "L20"], ["VPC|cloud"]),
    "Container networking security": (["L20"], ["container", "NetworkPolicy"]),
    "Incident response": (["L25"], ["incident response|IR lifecycle"]),
    "Network forensics": (["L29", "L30"], ["forensic"]),
    "Threat intelligence": (["L28"], ["intel|intelligence"]),
    "Advanced network defense": (["L28"], ["hunt|SOC"]),
    "Capstone architecture and security assessment": (["L31", "L32"], ["capstone|defense"]),
}

failures = []


def check(name, cond, observed):
    print(f"[{'PASS' if cond else 'FAIL'}] {name}: {observed}")
    if not cond:
        failures.append(name)


def norm(s):
    return re.sub(r"\s+", " ", s).strip().lower()


def section(text, pattern):
    m = re.search(pattern, text, re.M)
    if not m:
        return ""
    level = len(re.match(r"^(#+) ", text[m.start():]).group(1))
    nxt = re.search(r"^#{1,%d} " % level, text[m.end():], re.M)
    return text[m.start(): m.end() + nxt.start()] if nxt else text[m.start():]


def parse_front_matter(text):
    fm = {}
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return fm
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def main():
    arch = ARCH.read_text(encoding="utf-8")

    # --- Architecture reference data -------------------------------------
    master = section(arch, r"^## 3\. Master Lecture Map")
    arch_titles, arch_clos = {}, {}
    for row in re.findall(r"^\| L(\d{2}) \| (\d+) \| ([^|]+) \|[^|]*\|[^|]*\|([^|]*)\|", master, re.M):
        lid = f"L{row[0]}"
        arch_titles[lid] = norm(row[2])
        arch_clos[lid] = {int(c) for c in re.findall(r"\d+", row[3])}
    sched = section(arch, r"^## 5\. Weekly Schedule")
    arch_weeks = {}
    for w, ls in re.findall(r"^\| (\d+) \| ([^|]+) \|", sched, re.M):
        ids = re.findall(r"L(\d{2})", ls)
        if ids:
            arch_weeks[int(w)] = [f"L{i}" for i in ids]

    # --- T1: collect plan files -------------------------------------------
    plans = {}
    files = sorted(MODULES.glob("module-*/lectures/lecture-*.md"))
    for f in files:
        fm = parse_front_matter(f.read_text(encoding="utf-8"))
        lid = fm.get("lecture", "")
        plans[lid] = {"path": f, "fm": fm, "text": f.read_text(encoding="utf-8")}
    ids = sorted(plans)
    check("T1a 32 lecture-plan files", len(files) == 32, len(files))
    check("T1b ids exactly L01..L32", [f"L{i:02d}" for i in range(1, 33)] == ids, ids)

    # --- T2: duplicates + weeks -------------------------------------------
    weeks = {}
    for lid, p in plans.items():
        weeks.setdefault(int(p["fm"].get("week", 0)), []).append(lid)
    week_counts = {w: len(v) for w, v in sorted(weeks.items())}
    check("T2a weeks 1..16, two lectures each",
          sorted(week_counts) == list(range(1, 17)) and all(c == 2 for c in week_counts.values()),
          week_counts)

    # --- T3: weeks match architecture schedule ----------------------------
    mismatches = [w for w in arch_weeks if sorted(arch_weeks[w]) != sorted(weeks.get(w, []))]
    check("T3 week->lectures matches architecture", not mismatches,
          f"mismatched weeks: {mismatches or 'none'}")

    # --- T4: CLO coverage ---------------------------------------------------
    clo_map = {}
    per_lecture_bad = []
    for lid, p in plans.items():
        got = {int(c) for c in re.findall(r"CLO-(\d+)", p["fm"].get("clos", ""))}
        clo_map.setdefault(lid, got)
        if got != arch_clos.get(lid):
            per_lecture_bad.append(f"{lid}: plan={sorted(got)} arch={sorted(arch_clos.get(lid, set()))}")
    union = set().union(*clo_map.values()) if clo_map else set()
    check("T4a CLO-1..15 all covered", union == set(range(1, 16)), sorted(union))
    check("T4b per-lecture CLOs match architecture", not per_lecture_bad, per_lecture_bad or "all match")

    # --- T5: prerequisite progression ---------------------------------------
    prereq_bad = []
    for lid, p in plans.items():
        raw = p["fm"].get("prerequisites", "")
        refs = re.findall(r"L(\d{2})", raw)
        cur = int(lid[1:])
        for r in refs:
            if int(r) >= cur:
                prereq_bad.append(f"{lid} requires L{r} (not earlier)")
    check("T5 prerequisite progression (earlier lectures only)", not prereq_bad, prereq_bad or "all forward-safe")

    # --- T6: required sections ------------------------------------------------
    missing_sections = {}
    for lid, p in plans.items():
        miss = [s for s in REQUIRED_SECTIONS if s not in p["text"]]
        if miss:
            missing_sections[lid] = miss
    check("T6 all 12 required sections present in every plan", not missing_sections,
          missing_sections or "all complete")

    # --- T7: titles match architecture --------------------------------------
    title_bad = [lid for lid, p in plans.items()
                 if norm(p["fm"].get("title", "")) != arch_titles.get(lid)]
    check("T7 titles match architecture master map", not title_bad, title_bad or "all match")

    # --- T8: syllabus ----------------------------------------------------------
    sy = SYLL.read_text(encoding="utf-8") if SYLL.exists() else ""
    check("T8a syllabus exists", bool(sy), "present" if sy else "MISSING")
    cal = section(sy, r"^## 7\. Sixteen-Week Teaching Calendar") if sy else ""
    rows = [r for r in re.findall(r"^\| (\d+) \|", cal, re.M)]
    check("T8b syllabus calendar = 16 weeks", sorted(map(int, rows)) == list(range(1, 17)), len(rows))
    clo_sec = section(sy, r"^## 4\. Course Learning Outcomes") if sy else ""
    n_clo = len(re.findall(r"^\| \*\*CLO-(\d+)\*\* |^\| CLO-(\d+) \|", clo_sec, re.M)) or \
        len(re.findall(r"CLO-\d+", clo_sec)) // 2
    check("T8c syllabus defines 15 CLOs", n_clo >= 15, f"~{n_clo}")
    check("T8d CLO coverage matrix present", "## 5. CLO → Lectures, Labs, and Assessments" in sy, "found")

    # --- T9: mission topic coverage --------------------------------------------
    topic_bad = {}
    for topic, (lecture_ids, kws) in TOPIC_KEYWORDS.items():
        found = False
        for lid in lecture_ids:
            if lid not in plans:
                continue
            blob = norm(plans[lid]["text"])
            if any(re.search(k, blob, re.I) for k in kws):
                found = True
                break
        if not found:
            topic_bad[topic] = lecture_ids
    check("T9 mission topics located in lectures", not topic_bad,
          topic_bad or f"all {len(TOPIC_KEYWORDS)} topics covered")

    # --- coverage matrix for the report -----------------------------------------
    clo_to_lectures = {}
    for lid, g in clo_map.items():
        for c in sorted(g):
            clo_to_lectures.setdefault(c, []).append(lid)

    print()
    if failures:
        print(f"RESULT: {len(failures)} check(s) FAILED -> {failures}")
        write_report(plans, clo_to_lectures, weeks, per_lecture_bad, prereq_bad,
                     missing_sections, title_bad, topic_bad, failures)
        return 1
    print("RESULT: all teaching-plan checks PASSED")
    write_report(plans, clo_to_lectures, weeks, [], [], {}, [], {}, failures)
    return 0


def write_report(plans, clo_to_lectures, weeks, per_lecture_bad, prereq_bad,
                 missing_sections, title_bad, topic_bad, failures):
    weeks = {w: sorted(v) if isinstance(v, (list, tuple, set)) else [v]
             for w, v in weeks.items()}
    lines = [
        "# Teaching-Plan Coverage Report",
        "",
        "**Generated by:** `docs-meta/validate_teaching_plans.py` (automated; observed results, not asserted)",
        "**Scope:** `syllabus/syllabus.md` + 32 lecture teaching plans in `modules/`",
        "",
        "## Verdict",
        "",
        f"**{'ALL CHECKS PASSED' if not failures else 'FAILURES: ' + ', '.join(failures)}**",
        "",
        "## Lecture / Week Inventory",
        "",
        "| Week | Lectures |",
        "|---|---|",
    ]
    for w in sorted(weeks):
        lines.append(f"| {w} | {', '.join(weeks[w])} |")
    lines += ["", "## CLO → Teaching Plans", "", "| CLO | Lectures |", "|---|---|"]
    for c in sorted(clo_to_lectures):
        lines.append(f"| CLO-{c} | {', '.join(sorted(clo_to_lectures[c]))} |")
    lines += [
        "",
        "## Findings",
        "",
        f"- Per-lecture CLO mismatches vs architecture: {per_lecture_bad or 'none'}",
        f"- Prerequisite-progression violations: {prereq_bad or 'none'}",
        f"- Plans missing required sections: {missing_sections or 'none'}",
        f"- Title mismatches vs architecture: {title_bad or 'none'}",
        f"- Mission topics not located: {topic_bad or 'none'}",
        "",
        "## Interpretation (honest scope)",
        "",
        "- Validated: planning + teaching-plan layer (syllabus, 32 instructor teaching plans).",
        "- Still pending (documented in content-inventory.md §3): student-facing full lecture",
        "  content, labs 01–16, quizzes/assignments/exams, case-study files cs-001..100,",
        "  instructor manual/speaker notes, CI workflows, GitHub Pages site.",
        "- No artifact here is marked complete beyond its actual type: these are teaching",
        "  plans (`artifact-type: teaching-plan`), not final student-facing lecture content.",
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"coverage report written -> {REPORT}")


if __name__ == "__main__":
    sys.exit(main())
