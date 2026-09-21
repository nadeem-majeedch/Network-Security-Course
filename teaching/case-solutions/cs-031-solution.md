---
case: cs-031
solution-for: modules/module-03-secure-architecture/case-studies/cs-031-stateful-rule-evaluation.md
difficulty: intermediate
module: 3
lecture-anchor: L10
clos: [CLO-4]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-031 Solution — Stateful Rulebase Audit (INSTRUCTOR ONLY)

## Model Solution

**Flow verdicts (as submitted):**

| Flow | Verdict | Deciding rule |
|---|---|---|
| F1 workstation → patch server 443 | **ALLOW** | #1 (`INT→SRV any`) |
| F2 workstation → DB 5432 | **ALLOW** ⚠️ | #1 — rule 3 never fires (shadowed) |
| F3 workstation → direct internet 443 | **ALLOW** ⚠️ | #6 fallback — bypasses proxy intent |
| F4 workstation → direct internet 22 | **ALLOW** ⚠️ | #6 fallback (`any`) |
| F5 admin → SRV 22 | **ALLOW** | #1 (not #4 — also shadowed) |
| F6 DMZ proxy → WAN 443 | **ALLOW** | #5 (correct) |

**The two defects:**

1. **Shadowing (ordering error):** rule #1 (`INT→SRV any`) makes rule #3
   (deny DB) and rule #4 (admin SSH) unreachable — **spec item 3 is
   unenforceable**. Broad-before-narrow is the classic first-match defect.
2. **Over-permission / scope violation:** rule #6 (`INT→WAN any`) destroys
   the spec's "via the proxy **only**" scope — workstations can reach any
   internet service directly on any port (F3, F4). The spec's *intent* was a
   chokepoint, not just a port list.

**Minimal corrected rulebase (same discipline):**

| # | Src | Dest | Svc | Action | Maps to spec |
|---|---|---|---|---|---|
| 1 | INT | SRV | 443 (patch server host only) | ALLOW | item 1 — narrowed to the host, not the zone |
| 2 | 10.9.9.0/24 | SRV | 22 | ALLOW | item 5 — *before* the deny |
| 3 | INT | SRV | 5432 | DENY | item 3 — now reachable, explicit (belt for braces; default deny covers) |
| 4 | INT | DMZ-proxy | 80,443 | ALLOW | item 2 |
| 5 | DMZ | WAN | 80,443 | ALLOW | item 4 |
| — | *implicit* | | | DENY | everything else — rule 6 deleted |

Notes: #2 must precede #3's deny logic conceptually (first-match), and the
explicit deny (#3) is retained as auditor-visible evidence even though
implicit deny would cover it. Rule 1's narrowing from zone to host is the
*least-privilege* repair of "patching etc." — the comment is not a spec.

## Alternative Solutions

- **Delete rule 3, rely on implicit deny:** defensible and cleaner; the
  explicit-deny variant is kept for audit visibility — both earn credit if
  the shadowing fix is correct.
- **Proxy-enforcement via DNS/pac-file instead of firewall scope:** a good
  *additional* control (clients can still direct-connect unless the firewall
  denies) — must be paired with the rule fix, not replace it.

## Tradeoffs

- Explicit denies (readability/audit value) vs rulebase bloat: for high-value
  denials, explicit is worth it; blanket explicit-deny-everything is noise.
- Host-scoped rule 1 vs zone-scoped: host-scope is least-privilege but grows
  with each new SRV service — manage via service objects/groups, not raw IPs.

## Common Mistakes

- Marking F2 DENY because "rule 3 exists" — first-match says otherwise; the
  whole point of the case.
- Fixing only the ordering and leaving rule 6 (scope leak survives).
- Rewriting with 12 rules — the spec needs 6; verbosity hides defects.
- Forgetting statefulness notes (replies auto-allowed — no reverse rules needed).

## Instructor Prompts

- "Which rule would you keep as an explicit deny, and what does the auditor
  gain?"
- "Rule 1's comment says 'patching etc.' — what does 'etc.' cost the next
  auditor?"
- "How would you *test* the corrected rulebase before change control?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | First-match tracing per flow; both defects named by class |
| Technical accuracy | 25% | Verdicts correct; corrected base enforces exactly |
| Alternatives considered | 20% | Implicit-vs-explicit deny weighed |
| Communication | 15% | Verdict table + 6-line rewrite |

**Timing:** reveal at 5:00 + 2; the F2 verdict is the reveal moment — expect
audible groans.

## CLO Mapping

- **CLO-4** — Stateful policy evaluation and rulebase defect detection.
