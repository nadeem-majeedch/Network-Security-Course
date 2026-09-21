---
status: complete
artifact-type: instructor-resources-page
instructor-only: false
---

# Instructor Resources

This page describes the instructor support package and where it lives.
**None of the instructor answer-key material is published on this website** —
the repository keeps it in separate instructor-only trees, and the site build excludes them entirely.

## What exists in the repository

| Package | Location (repo) | Contents |
|---|---|---|
| Teaching plans | Instructor repository tree | 32 instructor teaching plans with timing, demos, expected difficulties |
| Speaker notes | Instructor repository tree | Per-lecture delivery notes paired with slide decks |
| Instructor manual | Instructor repository tree | Delivery guide, misconception bank, lab troubleshooting, accessibility guidance |
| Slide decks | Instructor repository tree | 36 Marp decks (32 lectures + reviews + case showcase) + 10 diagram assets |
| Answer keys | Held in instructor-only repository trees (paths withheld from the public site) | Validated answers for quizzes, exams, assignments, labs, cases |
| Question bank | Instructor repository tree | 50-question CLO/Bloom-mapped bank + generator |
| Validators | Repository tooling | Executable consistency checks for plans, labs, cases, assessments, slides |

## Access policy

- Adopting instructors: request repository access from the course maintainer.
- Answer keys are never rendered on the public site; the CI leak-scan gate
  blocks any build that would expose them (see the repository's
  `docs-meta/website-qa.md` for the enforcement details).
- Students: you will not find keys here — by design. Ask your instructor
  for practice material instead.
