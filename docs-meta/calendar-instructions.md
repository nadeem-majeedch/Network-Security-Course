---
artifact-type: calendar-instructions
status: complete
instructor-only: false
---

# Calendar Generation Instructions

The semester calendar is **generated from the finalized course content** —
never hand-edited. One command produces all views; one validator proves
they match the course.

## The one-click command

```bash
python docs-meta/generate_calendar.py
python docs-meta/validate_calendar.py     # must print: OK (C1–C8)
```

Both use only the Python standard library — no extra dependencies.

## Outputs

| View | File | Audience |
|---|---|---|
| Student calendar (site page) | `site-src/course/calendar-generated.md` | Students; published on the website with links into lecture/lab/assessment pages |
| Printable calendar | `docs-meta/calendar-printable.html` | Anyone — open in a browser, "Print / Save as PDF" (responsive, print stylesheet, repeats table headers) |
| Instructor planning view | `docs-meta/calendar-instructor.md` | Instructor: per-week actions, quiz administration, practical rubric weeks, case-set rotation notes (no answer-key content) |
| Calendar subscription file | `docs-meta/calendar.ics` | Import into Outlook/Google/Apple Calendar — **generated only when a start date is configured** |

## Configuring the semester (the only thing you normally edit)

Edit `docs-meta/calendar-config.json`:

```json
"semester": {
  "start_date": "2027-01-11",        // Monday of week 1 (empty = generic Weeks 1–16)
  "lecture_days": ["Monday", "Wednesday"],
  "lab_day": null,                    // or a weekday name for a separate lab slot
  "lecture_start": "09:00",
  "lecture_hours": 2,
  "overrides": { "6": "2027-02-22" }  // move week 6 (holidays) — remaps that week's Monday
}
```

Then rerun the two commands above. With a start date set, the student and
printable views show real dates and `calendar.ics` is emitted (32 events,
one per lecture, with CLOs in the description). Week themes, case-set
windows, graded-practical numbering, and link roots are also configurable
in the same file.

## How the schedule is derived (what the generator reads)

Everything is read live from the finalized content's front matter — the
generator never duplicates it:

| Source | Provides |
|---|---|
| `modules/*/lectures/lecture-*.md` | L01–L32 numbers, titles, weeks, CLOs |
| `docs/labs/lab-*.md` | Lab-01–16 weeks, titles, CLOs |
| `assessments/quizzes/quiz-*.md` | Graded quiz weeks (numbered chronologically) + self-check weeks |
| `assessments/assignments/assignment-*.md` | Assignment weeks and due dates |
| `assessments/midterm/`, `assessments/final/` | Exam weeks and CLO coverage |
| `assessments/case-study-evaluation/` + config | Case-set windows A/B/C |
| `assessments/capstone/capstone-brief.md` | Capstone window (W9–W16) |

Changing a week, title, or CLO in any source file and regenerating updates
all calendar views automatically. `validate_calendar.py` re-parses the
sources independently and fails if any view is stale, hand-edited, missing
a lecture/lab/assessment, or contains a broken link (C1–C8).

## Where the calendar appears on the website

The student view is part of the site build (Course section → "Semester
Calendar"). The printable HTML and ICS are repo artifacts; link them from
an LMS or hand them out — the deploy workflow regenerates the student view
on every push, so the site never drifts from the course content.
