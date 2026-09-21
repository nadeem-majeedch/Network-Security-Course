---
case: cs-011
solution-for: modules/module-02-network-threats/case-studies/cs-011-attack-tree-two-tier-web-app.md
difficulty: beginner
module: 2
lecture-anchor: L05
clos: [CLO-2]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-011 Solution — Attack Tree (INSTRUCTOR ONLY)

## Model Solution

**Reference tree (goal: read customer DB):**

```
READ DATABASE
├─ OR 1: Compromise admin panel (via /admin through proxy)
│   ├─ leaf: credential guess/phish of 4 staff (no MFA)
│   └─ leaf: panel vulnerability (unpatched app code)
├─ OR 2: Compromise app server
│   ├─ leaf: exploit app vuln via proxy path (unvalidated input)
│   └─ leaf: steal app→DB creds from app config
├─ OR 3: Compromise proxy
│   ├─ leaf: proxy CVE (monthly patching window gap)
│   └─ leaf: TLS misconfig → traffic manipulation
└─ OR 4: Attack DB directly
    ├─ leaf: internet-exposed 5432 (misconfig) — NOT currently open
    └─ leaf: compromise backup path (app service account restores dump)
```

**AND/OR correctness:** nearly all nodes are OR (any suffices). A rare AND
example students may add: "phish staff AND harvest session cookie" or
"compromise app AND extract DB creds" — any AND that correctly models steps
that must *all* happen earns credit.

**Most likely opportunistic path: OR-1, leaf 1** — 4 password-only accounts on
an internet-reachable panel is the cheapest path; everything else requires a
vulnerability the attacker must first find. Likelihood logic: exposed weak auth
> unknown vuln discovery.

**Implied priority list (the CTO's actual deliverable):** 1) MFA on admin
panel, 2) restrict/rename `/admin`, 3) app-pen-test before patch-cycle trust,
4) decouple backup restore rights from the app service account.

## Alternative Solutions

- Rooting the tree at "compromise app server" instead of the DB goal —
  acceptable if the tree then continues to DB access; weaker because it
  bakes in one path.
- Adding insider/physical branches — good breadth; fine as long as network
  branches are correct.

## Tradeoffs

- Tree depth vs class time: shallow trees miss preconditions; deep trees
  become unreadable. 3 levels is the teaching sweet spot.
- Likelihood-based vs impact-based prioritization: they reorder the same tree —
  worth one debrief minute.

## Common Mistakes

- Nodes as product names ("install WAF") instead of attacker sub-goals.
- AND/OR confusion (making everything AND because "attackers need luck").
- Forgetting the backup-restore path — the sneaky branch that rewards good trees.
- Declaring the DB unreachable so branch 4 "impossible" — service accounts and
  misconfig make it merely *currently closed*.

## Instructor Prompts

- "Which single control kills the most branches at once?" (MFA on /admin.)
- "Where would you put detection, if you can't prevent a branch?"
- "Which branch survives 'we patched everything last night'?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Correct OR/AND semantics; likelihood-based path choice |
| Technical accuracy | 25% | Branches match the actual architecture |
| Alternatives considered | 20% | ≥1 extra branch (backup/insider) or alternative root |
| Communication | 15% | Tree readable; one-sentence justification |

**Timing:** reveal at 5:00; debrief "which control kills most branches."

## CLO Mapping

- **CLO-2** — Attack-tree construction and prioritization.
