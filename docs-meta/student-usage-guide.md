---
artifact-type: student-usage-guide
status: complete
instructor-only: false
handover-date: 2026-09-21
---

# Student Usage Guide

How to work through the course week by week, and where everything lives.

## The website

- **Home** — course overview and quick links.
- **Course** — description, CLOs, **Semester Calendar** (dates update from
  the instructor's configuration), syllabus.
- **Modules** — eight orientation pages; start here each module to see the
  arc: lectures, labs, case themes, and the skills you must demonstrate.
- **Lectures** — all 32 student pages: concepts, diagrams, protocol
  examples, activities, the week's case, exit ticket, references, CLO map.
- **Lab Workbook** — all 16 handouts: setup, **authorization notes**, tasks,
  expected observations, troubleshooting, cleanup, submission checklist.
- **Case Studies** — the 100-case collection with the full list and the
  five-step classroom protocol.
- **Assessment** — quizzes/self-checks, assignments, exams, capstone: what
  is graded, when, and how.
- **Search** (magnifier icon) indexes everything student-facing.

## Your weekly rhythm

1. **Before class:** skim the week's two lecture pages (5–10 min each).
2. **In class:** the lectures embed the week's lab and a case study —
   the case gets ~5 minutes of reasoning on the projector before any
   reveal. Do the reasoning, don't wait for the answer.
3. **After class:** finish the lab submission checklist; run the week's
   self-check quiz when one is scheduled.
4. **Assignments:** release weeks are on the calendar; each is a
   design-and-justify artifact, not a report.

## The lab environment

- Tools: Wireshark/tshark, Suricata, Zeek, pfSense VMs, container targets,
  and an instructor-provisioned cloud sandbox. Specs are in each handout.
- Lab handouts mark each command **✅ verified against the course datasets**
  or **⚠️ untested in the authoring environment** — if a ⚠️ step fails,
  that's expected friction: document it and ask; don't skip it silently.
- **Authorization frame:** everything targets the isolated lab range or
  prepared captures. Running course techniques against any system you don't
  own — including campus networks — is a disciplinary matter, full stop.

## Calendar on your phone

Ask your instructor for the semester's `calendar.ics` (generated from
`docs-meta/calendar-config.json`) and import it into Google/Outlook/Apple
Calendar — 32 lecture events with CLOs in the descriptions.

## Integrity

- Labs and case sessions are collaborative; assignments, quizzes, and exams
  are individual; the capstone is team-reported but individually defended.
- Cite tools, datasets, and any AI assistance in submission headers.
- Lab evidence must come from your own range work — fabricated captures fail.

## If you're stuck

The misconception tables on lecture pages and the troubleshooting sections
in lab handouts answer most questions before office hours do.
