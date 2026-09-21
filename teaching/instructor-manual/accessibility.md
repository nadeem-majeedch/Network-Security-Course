---
artifact-type: instructor-manual
status: complete
instructor-only: true
distribution: never-publish-to-students
---

# Accessibility Guidance

## 1. Universal design baseline (built into the course already)

The course materials were designed with these defaults — verify them each
semester rather than retrofitting:

- **All console output exists as text files.** Every demonstration's captured
  output is distributed as text — no student depends on reading a projector
  in real time.
- **Every diagram has a text equivalent.** Architecture/DFD diagrams in
  student pages carry text-outline equivalents; when sketching live, narrate
  the structure aloud.
- **Timed sequences are published, not improvised.** Students can prepare for
  the pace of drills because speaker-note timing plans are mirrored in student
  pages' activity descriptions.
- **High-contrast reference cards** for syntax-heavy content (ACL keywords,
  IDS rule syntax, Zeek fields) — black-on-white, no color-only encoding.
- **No assessment depends on color perception** (attack/detection datasets are
  distinguishable by labels and values, not hue).
- **Captures, not sound-dependent evidence:** no audio-only artifacts in any
  graded path.

## 2. Accommodations menu (map requests to these)

| Accommodation type | Course adaptation |
|---|---|
| Extended time | Guided-exercise and quizzes: extended clock (institutional percentage); the *hard-clock design feature* of drills is preserved in debrief structure but grading rewards the record, not the finish |
| Alternative formats | Materials are Markdown-first — convertible to Braille/large-print/EPUB without re-authoring; request 2-week lead |
| Note-taking support | All teaching sequences and slide-equivalents published in student pages; peer-notes not load-bearing |
| Lab environment | Adjustable-height stations in the security lab; software alternatives to any physical-console task; paired-work rotation |
| Screen-reader use | Markdown structure (headers, tables, alt-text lines) verified per release; console-output files are plain text with field-by-field narration available |
| Anxiety/access to recordings | Live demos recorded (with lab-range authorization notice) and posted to the student-facing area for review |
| Communication preference | Written questions accepted in lieu of spoken during drills; verbal responses never the only channel |

## 3. Per-activity adaptations (the moments that need care)

- **Rapid-response drills (L25 contact sheet, L26 guided exercise):** written
  scenario cards distributed simultaneously with spoken briefs; roles can be
  assigned to match processing-time strengths; the record is graded, not the
  speech.
- **Live attack demonstrations (L06–L08, L17):** projected content is also on
  the distributed transcript; the authorization statement is spoken *and*
  shown.
- **Capstone defense (L32):** presentation mode is student choice — live
  talk, narrated slides, or pre-recorded video plus live Q&A; Q&A questions
  are given in writing as well as spoken.
- **Team roles (capstone arc):** role rotation is deliberate — evidence
  custodian and comms roles allow different working styles to score equally.

## 4. Instructor habits that carry most of the load

1. Narrate what you type during live demos (screen-reader users and everyone
   else benefit).
2. Face the class when speaking; don't narrate toward the projector.
3. Publish materials *before* session, not after — preparation time is an
   equity issue.
4. Ask, don't assume: the accommodation a student requested in week 1 may not
   be the one they need in week 12 — re-offer the menu at module boundaries.

## 5. Institutional interface

Follow institutional disability-services processes for formal accommodations;
this menu is the course-side implementation map. The course's own gates: the
L01 tooling smoke test doubles as an early-needs check — help session offered
before L02 for any student whose setup needs adjustment.
