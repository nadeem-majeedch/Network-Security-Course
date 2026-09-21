---
case: cs-076
solution-for: modules/module-06-detection-vulnerability/case-studies/cs-076-cvss-base-vs-environmental-debate.md
difficulty: expert
module: 6
lecture-anchor: L24
clos: [CLO-10]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-076 Solution — CVSS Governance (INSTRUCTOR ONLY)

## Model Solution

**Arbitration — the technical split:**

| Adjustment claimed | Verdict | Why |
|---|---|---|
| "Requires authentication" → lower score | **Abuse — rejected** | the base vector *already contains* `PR:L` — the 9.1 prices "attacker with a low-privilege account"; re-arguing authentication is **double-counting** a metric the vector carries. This is the arithmetic tell. |
| "MFA on the SSO in front" | **Legitimate — environmental** | maps to CVSS environmental metrics genuinely outside base scope: it raises the *exploitation* bar beyond PR:L's assumption (MFR/MAR-class reasoning; in v3.1 terms, a defensible Modified-AC/CR-style adjustment — the spec's environmental group exists for exactly this). Condition: **evidence** (MFA actually enforced on this tool's path, tested — the cs-075 standard). |
| "Internal-only, no internet" | **Partially legitimate** | AV was already `N` (network — *any* network reach counts); "no internet" narrows *remoteness of attacker population*, which is deployment context the base deliberately abstracts. Legitimate as an environmental note feeding the SLA band decision; **not** license to rewrite the vector's AV. |
| "Inventory data isn't crown-jewel" → lower C | **Legitimate but weakest** | Modified-CIR is spec-valid; but "not crown-jewel" must be *asset-class evidence* (data classification record), not owner assertion — and a command-injection typically carries **I:H** (integrity) which the C-argument ignores: the vector's I:H survives their narrative untouched. |

**Net verdict:** a *governed* environmental re-score is defensible
toward roughly **5–6**, **not** 4.2 — the app owner's number shopped
the double-count plus an unpriced I:H. But the base camp is *also*
wrong in kind: 9.1's SLA (7 days) applied to base scores everywhere
treats a **severity** number as a **risk** number — the standard
*expects* environmental scoring for deployment context; refusing it
wholesale is the other abuse.

**The base-score contract (the literacy payload):** a CVSS base score
claims *intrinsic severity under stated worst-case-ish assumptions*
(exploitability primitives, scope, impact ceilings) — constant across
environments, so organizations can communicate and compare. It does
**not** claim "this is the risk to *your* deployment"; that's what the
temporal and environmental groups exist for. The ops camp's error:
treating base as finished risk arithmetic. The app-owner error:
treating it as negotiable rhetoric rather than a metric system with
rules.

**Governance rule (the deliverable):**

1. **Locked:** base-vector metrics are immutable post-publication;
   adjustments happen *only* in the environmental group, documented
   metric-by-metric — no wholesale re-scoring.
2. **No double-counting:** any environmental adjustment must reference
   a metric *not already encoded in the base vector*; reviewers check
   the vector first (the PR:L tell becomes a checklist item).
3. **Evidence standard:** each adjusted metric cites testable evidence
   (MFA-enforced-and-tested, segmentation re-verified, data-class
   record) — assertions score as if absent (cs-075's tested-vs-
   documented rule).
4. **Re-review triggers:** any evidence change (MFA removed, exposure
   path added, tool repurposed) auto-reverts to base-score SLA until
   re-adjudicated — deferrals carry tripwires, always.
5. **Audit artifact:** the adjustment record (per-metric rationale +
   evidence link + approver + date) ships with the finding — the
   debated 4.2-vs-9.1 conversation becomes a one-page artifact an
   auditor can read without a meeting.

## Alternative Solutions

- **"Base scores only, no environment ever":** operationally simple,
  standard-noncompliant, and *wastes* the context that makes
  prioritization rational (cs-075's whole formula depends on it) —
  rejected with the spec citation.
- **"Owner scores their own risk":** the score-shopping endgame —
  conflicts of interest need the two-party rule (adjuster ≠ owner) in
  the governance.
- **CVSS v4 framing:** v4's threat/environmental restructure improves
  exactly this class of debate — name it as the roadmap; the governance
  rule above is version-agnostic by design.

## Tradeoffs

- Governance friction (evidence + two-party) vs tuning speed: each
  adjustment costs an afternoon — the price of score credibility.
- MFA-as-discount depth: *how much* MFA lowers exploitability is a
  judgment — cap the per-metric adjustment (spec ranges) and document
  the rationale; caps prevent the 4.2-class dives.
- Base-SLA bands tied to adjusted scores: compliance wants stable
  bands; environmental adjustment moves findings across bands — the
  rule's re-review trigger is what keeps bands honest.

## Common Mistakes

- Missing the double-count (reading the vector resolves the case —
  skipping it loses the arbitration).
- "Environmental scoring = score shopping" (the standard *invites* it,
  governed).
- No evidence standard (discounts become assertions).
- One-off verdicts without the rule (the debate re-happens quarterly).

## Instructor Prompts

- "Read the vector aloud: which metric already answers the app owner's
  authentication argument?"
- "What evidence would move *your* ruling — name the test."
- "Why does the rule need re-review triggers to survive contact with
  reality?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Vector-reading arbitration; both-camps critique |
| Technical accuracy | 25% | CVSS metric semantics (PR:L, AV:N, environmental group) |
| Alternatives considered | 20% | Base-only/owner-scored rejections |
| Communication | 15% | 5-bullet governance rule |

**Timing:** reveal at 5:00 + 10; the vector-reading moment is the
literacy payoff.

## CLO Mapping

- **CLO-10** — Scoring-standard fluency and governance.
