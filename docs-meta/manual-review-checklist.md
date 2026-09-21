---
artifact-type: manual-review-checklist
status: complete
instructor-only: false
handover-date: 2026-09-21
---

# Manual Review Checklist

The things automation cannot prove, for the human reviewer. Print or copy
into your review notes; each item has a sign-off line. Nothing here has
been pre-checked by a human — all prior verification was automated.

## A. Academic review (adopting instructor)

| # | Item | Notes | ✓ / ✗ |
|---|---|---|---|
| A1 | Syllabus CLOs match your program's outcomes; adjust numbering if your board requires it | | |
| A2 | Grading weights (15/20/35/10/15/5) acceptable to your department | | |
| A3 | Read L01, L07, L14, L24 teaching plans end-to-end — depth and timing feel right for *your* students | | |
| A4 | Read two case studies + solutions (one beginner, one expert) — run one aloud | | |
| A5 | Skim all 16 lab handouts for tool availability in YOUR lab (versions, images, licensing) | | |
| A6 | Review midterm + final against your exam norms (duration, marks, integrity rules) | | |
| A7 | Confirm capstone brief's four organization profiles suit your cohort | | |
| A8 | Verify prerequisite chain against your program's actual prerequisites | | |
| A9 | Technical spot-review of one module you know deeply (protocol claims, terminology) | | |

Sign-off: ______________  Date: ________

## B. Safety & compliance review

| # | Item | Notes | ✓ / ✗ |
|---|---|---|---|
| B1 | Lab authorization frame matches your institution's policy (who authorizes the range, in writing) | | |
| B2 | Range isolation plan reviewed (no bridging to production/campus networks) | | |
| B3 | Simulated-fiction labeling adequate per your legal/comms office | | |
| B4 | Answer-key trees (`instructor/`, `teaching/`) access-restricted before any student repo access | | |
| B5 | Cloud sandbox accounts provisioned by the institution, not personal | | |

Sign-off: ______________  Date: ________

## C. Pre-publication review (before enabling Pages)

| # | Item | Notes | ✓ / ✗ |
|---|---|---|---|
| C1 | All nine validators exit 0 on your machine (commands in root README) | | |
| C2 | `mkdocs build --strict` zero warnings; `mkdocs serve` click-through: Home → Module → Lecture → Lab → Case → Assessment | | |
| C3 | Search finds a known phrase from a lecture and a lab | | |
| C4 | Leak spot-check: search the built `site/` for one answer you know; it must not appear | | |
| C5 | Calendar page shows your semester dates (set `start_date` first) | | |
| C6 | Settings → Pages → Source: GitHub Actions selected | | |
| C7 | Workflow runs green on push; **verify the live URL and at least five interior pages personally** | | |
| C8 | Re-check after first deploy: leak scan concept — spot-open `/search/?q=answer+key` style queries on the live site | | |

Sign-off: ______________  Date: ________

## D. First-semester delivery review

| # | Item | Notes | ✓ / ✗ |
|---|---|---|---|
| D1 | Execute each lab once before its delivery week; update ✅/⚠️ markers | | |
| D2 | Render each week's slide deck before class (Marp); fix overflow | | |
| D3 | After Quiz 1: review item statistics; note any miskeyed item in the key's calibration section | | |
| D4 | After Pract-1 (W6): confirm rubric produces the intended mark distribution | | |
| D5 | Log any content correction as a change note in `content-inventory.md` | | |

Sign-off: ______________  Date: ________
