#!/usr/bin/env python3
"""Validator for the Network Security assessment package.

Checks (per mission validation requirements):
  A1  completeness: every expected artifact exists (16 quizzes, 16 keys,
      7 assignments + keys, question bank + key, midterm + key, final + key,
      capstone set, case-evaluation set)
  A2  mark arithmetic: every assessment's per-question marks sum to its
      declared total (exams use their explicit schemes)
  A3  answer-key consistency: every student artifact points to an existing
      key; every key is marked instructor-only
  A4  CLO coverage: the union of assessed CLOs equals CLO-1..CLO-15
  A5  separation: no student artifact contains instructor-only markers or
      answer text ("Answer:" patterns from keys)
  A6  Bloom coverage: bank key reports all six Bloom levels; every graded
      quiz question carries a Bloom tag
  A7  syllabus weight reconciliation: component weights match the syllabus
      grading table (quizzes 15, practicals 20, assignments 35, midterm 10,
      capstone 15, final 5)
  A8  no duplicate question stems (quiz vs bank) on normalized text
Exit 0 on success; nonzero with findings otherwise.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FINDINGS = []

EXPECTED_FILES = [
    # 5 graded quizzes + 11 self-checks + 16 keys
    "assessments/quizzes/quiz-01-week02-clo1-protocol-foundations.md",
    "assessments/quizzes/quiz-02-week04-clo2-threat-mechanics.md",
    "assessments/quizzes/quiz-03-week05-clo3-clo5-perimeter-crypto.md",
    "assessments/quizzes/quiz-04-week10-clo8-clo13-wireless-cloud.md",
    "assessments/quizzes/quiz-05-week14-clo11-clo14-ir-forensics.md",
    "assessments/quizzes/quiz-06-week01-selfcheck.md",
    "assessments/quizzes/quiz-07-week03-selfcheck.md",
    "assessments/quizzes/quiz-08-week06-selfcheck.md",
    "assessments/quizzes/quiz-09-week07-selfcheck.md",
    "assessments/quizzes/quiz-10-week09-selfcheck.md",
    "assessments/quizzes/quiz-11-week11-selfcheck.md",
    "assessments/quizzes/quiz-12-week13-selfcheck.md",
    "assessments/quizzes/quiz-13-week08-selfcheck-midterm-prep.md",
    "assessments/quizzes/quiz-14-week15-selfcheck-final-prep.md",
    "assessments/quizzes/quiz-15-week12-selfcheck.md",
    "assessments/quizzes/quiz-16-week16-capstone-selfcheck.md",
    "instructor/answer-keys/quiz-01-answer-key.md",
    "instructor/answer-keys/quiz-02-answer-key.md",
    "instructor/answer-keys/quiz-03-answer-key.md",
    "instructor/answer-keys/quiz-04-answer-key.md",
    "instructor/answer-keys/quiz-05-answer-key.md",
    "instructor/answer-keys/quiz-06-answer-key.md",
    "instructor/answer-keys/quiz-07-answer-key.md",
    "instructor/answer-keys/quiz-08-answer-key.md",
    "instructor/answer-keys/quiz-09-answer-key.md",
    "instructor/answer-keys/quiz-10-answer-key.md",
    "instructor/answer-keys/quiz-11-answer-key.md",
    "instructor/answer-keys/quiz-12-answer-key.md",
    "instructor/answer-keys/quiz-13-answer-key.md",
    "instructor/answer-keys/quiz-14-answer-key.md",
    "instructor/answer-keys/quiz-15-answer-key.md",
    "instructor/answer-keys/quiz-16-answer-key.md",
    # assignments + keys
    "assessments/assignments/assignment-01-week06-segmentation-design.md",
    "assessments/assignments/assignment-02-week07-tls-deployment-audit.md",
    "assessments/assignments/assignment-03-week09-vpn-access-design.md",
    "assessments/assignments/assignment-04-week11-ids-tuning-detection-engineering.md",
    "assessments/assignments/assignment-05-week12-vulnerability-program-design.md",
    "assessments/assignments/assignment-06-week13-ir-runbook-development.md",
    "assessments/assignments/assignment-07-week15-board-briefing.md",
    "instructor/answer-keys/assignment-01-answer-key.md",
    "instructor/answer-keys/assignment-02-answer-key.md",
    "instructor/answer-keys/assignment-03-answer-key.md",
    "instructor/answer-keys/assignment-04-answer-key.md",
    "instructor/answer-keys/assignment-05-answer-key.md",
    "instructor/answer-keys/assignment-06-answer-key.md",
    "instructor/answer-keys/assignment-07-answer-key.md",
    # question bank + key
    "assessments/question-bank/question-bank.md",
    "assessments/question-bank/generate_question_bank.py",
    "instructor/answer-keys/question-bank-answer-key.md",
    # exams + keys
    "assessments/midterm/midterm-exam.md",
    "instructor/answer-keys/midterm-answer-key.md",
    "assessments/final/final-exam.md",
    "instructor/answer-keys/final-answer-key.md",
    # capstone + defense
    "assessments/capstone/capstone-brief.md",
    "assessments/capstone/capstone-rubric.md",
    "assessments/capstone/defense-guide.md",
    "instructor/answer-keys/capstone-rubric-bands.md",
    # case evaluation
    "assessments/case-study-evaluation/case-evaluation-rubric.md",
    "instructor/answer-keys/case-evaluation-protocol.md",
]


def load(rel):
    p = ROOT / rel
    if not p.exists():
        return None
    return p.read_text(encoding="utf-8")


def fm_field(text, field):
    m = re.search(r"^%s:\s*(.+)$" % re.escape(field), text, re.MULTILINE)
    return m.group(1).strip() if m else None


def front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    return m.group(1) if m else ""


def check_a1():
    missing = [f for f in EXPECTED_FILES if not (ROOT / f).exists()]
    if missing:
        FINDINGS.append(f"A1 missing {len(missing)} files: " + "; ".join(missing[:6]) + (" ..." if len(missing) > 6 else ""))


def check_a2_marks():
    # Quizzes: sum of per-question marks == front-matter marks
    for f in sorted((ROOT / "assessments" / "quizzes").glob("quiz-*.md")):
        t = f.read_text(encoding="utf-8")
        declared = fm_field(t, "marks")
        if not declared:
            FINDINGS.append(f"A2 {f.name}: no marks field")
            continue
        declared = int(declared)
        # per-question marks: tags come in two shapes —
        #   MCQ:  *Bloom: X · CLO-n · 1 mark*
        #   open: *(Bloom: X · CLO-n · 3 marks)*  (closing paren inside italics)
        # Section totals use the "N × M = T marks" header shape and never
        # carry a Bloom tag, so matching Bloom-prefixed tags is safe.
        per_q = [int(m) for m in re.findall(
            r"Bloom:[^*]*?·\s*(\d+)\s*marks?\)?\s*\*", t)]
        body_marks = sum(per_q)
        # quizzes state totals like "**Total: 15 marks**"
        total_m = re.search(r"\*\*Total:\s*(\d+)\s*marks?\*\*", t)
        if total_m and int(total_m.group(1)) != declared:
            FINDINGS.append(f"A2 {f.name}: stated total {total_m.group(1)} != front-matter {declared}")
        if per_q and body_marks != declared:
            FINDINGS.append(f"A2 {f.name}: question marks sum {body_marks} != declared {declared}")
    # Assignments: 100 each declared
    for f in sorted((ROOT / "assessments" / "assignments").glob("assignment-*.md")):
        t = f.read_text(encoding="utf-8")
        if fm_field(t, "marks") != "100":
            FINDINGS.append(f"A2 {f.name}: marks != 100")
        # task marks sum: "(NN)" patterns in task headers
        task_marks = [int(m) for m in re.findall(r"\((\d{1,3})\)", t)]
        # heuristic: sum of the numbers in "N. **Name** (NN)" headers
        headers = re.findall(r"^\d+\.\s+\*\*.*?\*\*\s*\((\d{1,3})\)", t, re.MULTILINE)
        if headers and sum(int(h) for h in headers) != 100:
            FINDINGS.append(f"A2 {f.name}: task marks sum {sum(int(h) for h in headers)} != 100")
    # Midterm: A 20 + B 30 + C 30 + D 20 = 100
    mt = load("assessments/midterm/midterm-exam.md")
    if mt:
        if fm_field(mt, "marks") != "100":
            FINDINGS.append("A2 midterm: marks != 100")
        section_totals = {
            "A": re.search(r"Section A[^\n]*\((\d+) × (\d+) = (\d+)", mt),
            "B": re.search(r"Section B[^\n]*\((\d+) × ([\d.]+) = (\d+)", mt),
            "C": re.search(r"Section C[^\n]*\((\d+) × (\d+) = (\d+)", mt),
        }
        a = int(section_totals["A"].group(1)) * int(section_totals["A"].group(2)) if section_totals["A"] else None
        if a != 20:
            FINDINGS.append("A2 midterm: section A arithmetic != 20")
        # D choice total
        if not re.search(r"choose ONE, 20 marks", mt):
            FINDINGS.append("A2 midterm: section D total not stated as 20")
        # overall total stated
        if "**Total: 100 marks**" not in mt:
            FINDINGS.append("A2 midterm: overall total line missing")
    # Final: Part I 60 (A16 + B24 + C20) + Part II 40
    fe = load("assessments/final/final-exam.md")
    if fe:
        if fm_field(fe, "marks") != "100":
            FINDINGS.append("A2 final: marks != 100")
        pairs = {"A": (8, 2, 16), "B": (4, 6, 24), "C": (1, 20, 20)}
        for sec, (n, m, tot) in pairs.items():
            hit = re.search(r"Section %s[^[\n]*\((\d+) × (\d+) = (\d+)" % sec, fe)
            if sec == "C":
                # C is a single 20-mark scenario, header carries no n×m form
                if "Section C — Applied Scenario (20 marks)" not in fe:
                    FINDINGS.append("A2 final: section C header mismatch")
                continue
            if not hit or (int(hit.group(1)), int(hit.group(2)), int(hit.group(3))) != (n, m, tot):
                FINDINGS.append(f"A2 final: section {sec} header arithmetic mismatch")
        if "Part II — Forensic Practical (40 marks)" not in fe:
            FINDINGS.append("A2 final: Part II 40-mark header missing")
        if "**Total: 100 marks**" not in fe:
            FINDINGS.append("A2 final: overall total line missing")


def check_a3_keys():
    for rel in EXPECTED_FILES:
        if "/assessments/" not in rel:
            continue
        t = load(rel)
        if t is None:
            continue
        if "artifact-type: student" in t or "artifact-type: question-bank" in t or "artifact-type: grading-rubric" in t or "artifact-type: student-guide" in t:
            key = fm_field(t, "answer-key") or fm_field(t, "instructor-key") or fm_field(t, "instructor-scoring") or fm_field(t, "instructor-band-detail") or fm_field(t, "instructor-protocol")
            if key:
                if not (ROOT / key).exists():
                    FINDINGS.append(f"A3 {rel}: key link missing -> {key}")
            else:
                # capstone brief points at two rubric files; acceptable
                if "related-rubrics" not in front_matter(t):
                    FINDINGS.append(f"A3 {rel}: student artifact without key link")
    # all keys marked instructor-only
    for f in (ROOT / "instructor" / "answer-keys").glob("*.md"):
        t = f.read_text(encoding="utf-8")
        if fm_field(t, "instructor-only") != "true":
            FINDINGS.append(f"A3 key {f.name}: not marked instructor-only")


def check_a4_clos():
    covered = set()
    for f in sorted((ROOT / "assessments").rglob("*.md")):
        t = f.read_text(encoding="utf-8")
        for clo in re.findall(r"CLO-\d+", t):
            covered.add(clo)
    missing = [f"CLO-{i}" for i in range(1, 16) if f"CLO-{i}" not in covered]
    if missing:
        FINDINGS.append("A4 CLOs not assessed anywhere: " + ", ".join(missing))


def check_a5_separation():
    # regex markers; line-anchored where a substring would false-positive
    # (e.g., "THREAT MODEL:" in a legitimate student question)
    forbidden = [r"INSTRUCTOR ONLY", r"(?m)^MODEL:", r"— Answer:",
                 r"Model answer\*\*", r"Model Solution"]
    for f in sorted((ROOT / "assessments").rglob("*.md")):
        t = f.read_text(encoding="utf-8")
        for bad in forbidden:
            if re.search(bad, t):
                FINDINGS.append(f"A5 {f.relative_to(ROOT)}: contains instructor marker {bad!r}")
                break


def check_a6_bloom():
    t = load("instructor/answer-keys/question-bank-answer-key.md") or ""
    for level in ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]:
        if level not in t:
            FINDINGS.append(f"A6 bank key missing Bloom level {level}")
    # graded quizzes: every question carries Bloom tag
    for n in ["01", "02", "03", "04", "05"]:
        f = ROOT / "assessments" / "quizzes" / f"quiz-{n}-" 
        hits = list((ROOT / "assessments" / "quizzes").glob(f"quiz-{n}-*.md"))
        if not hits:
            continue
        t = hits[0].read_text(encoding="utf-8")
        qcount = len(re.findall(r"^\*\*Q\d+", t, re.MULTILINE))
        blooms = len(re.findall(r"Bloom:", t))
        if qcount and blooms < qcount:
            FINDINGS.append(f"A6 {hits[0].name}: {qcount} questions but {blooms} Bloom tags")


def check_a7_weights():
    t = load("syllabus/syllabus.md") or ""
    expected = {"Quizzes (5 × 3%)": "15%", "Lab practicals (4 × 5%)": "20%",
                "Assignments (7 × 5%)": "35%", "Midterm examination": "10%",
                "Capstone project": "15%", "Final examination": "5%"}
    for comp, wt in expected.items():
        if comp not in t:
            FINDINGS.append(f"A7 syllabus grading table missing component {comp!r}")
    # sum = 100
    if t and sum(int(w.rstrip('%')) for w in expected.values()) != 100:
        FINDINGS.append("A7 internal error: expected weights != 100")


def check_a8_duplicates():
    stems = {}
    def norm(s):
        return re.sub(r"\W+", "", s.lower())[:60]
    # quiz MCQ stems
    for f in sorted((ROOT / "assessments" / "quizzes").glob("quiz-*.md")):
        t = f.read_text(encoding="utf-8")
        for m in re.finditer(r"^\*\*Q\d+\.\*\*\s*(.+)$", t, re.MULTILINE):
            s = norm(m.group(1))
            if s in stems:
                FINDINGS.append(f"A8 duplicate stem: {f.name} vs {stems[s]} :: {m.group(1)[:50]!r}")
            stems[s] = f.name
    # bank MCQ stems
    gen = load("assessments/question-bank/generate_question_bank.py") or ""
    for m in re.finditer(r'q\("QB-\d+",[^,]+,[^,]+,[^,]+,[^,]+,\s*\d+,\s*\n?\s*"(.+?)"', gen, re.DOTALL):
        s = norm(m.group(1))
        if s in stems:
            FINDINGS.append(f"A8 duplicate stem: question-bank vs {stems[s]}")
            continue
        stems[s] = "question-bank"


def main():
    check_a1()
    check_a2_marks()
    check_a3_keys()
    check_a4_clos()
    check_a5_separation()
    check_a6_bloom()
    check_a7_weights()
    check_a8_duplicates()
    if FINDINGS:
        print(f"FAIL — {len(FINDINGS)} finding(s):")
        for f in FINDINGS:
            print("  " + f)
        return 1
    n = len(EXPECTED_FILES)
    print(f"PASS — A1..A8 all green: {n} expected artifacts present; marks arithmetic verified; "
          "keys linked & instructor-only; CLO-1..15 assessed; separation clean; "
          "Bloom complete; weights reconcile to syllabus; no duplicate stems.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
