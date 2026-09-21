---
lecture: L11
module: 3
week: 6
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L11 Speaker Notes — ACLs & Rulebase Engineering

## Delivery Guide
Audit day: the four fault classes are the method; the planted-fault targets are the
reps. Wildcard masks get their own drill — the /23 and "typo'd /16" examples are
where students stumble. The instructor "red review" (proposing innocent
explanations for findings) teaches precision: a wrong finding is worse than a missed
one in professional audits. Assignment 2 is the audit deliverable — state the rubric
explicitly.

## Timing Plan
0–10 recap (test matrices) · 10–35 ACL mechanics + wildcard drill · 35–55 audit
taxonomy on the two targets · 55–65 break · 65–75 least-privilege refactoring demo ·
75–110 audit sprint · 110–120 exit ticket + Assignment-2 briefing. 
**Compression:** one audit target instead of two if behind; the taxonomy walk is
sacred.

## Teaching Demonstrations
1. Wildcard drill: ten prefixes → masks, timed; include the 0.0.255.255-vs-0.0.0.255 trap.
2. Shadowing proof by test: the planted pair — send the traffic, show which rule's counter moves.
3. Hit-counter archaeology: a 0-match rule with a legitimate purpose (failover path) — precision lesson.

## Expected Student Difficulties
1. Inverse-mask inversion — draw the bit ranges; /23 is the humbling one.
2. "Delete zero-hit rules" enthusiasm — the failover-path example reframes counters as *evidence*, not verdicts.
3. Findings without evidence — require rule id + observed behavior in every finding; opinion is not a finding.

## Discussion Facilitation
Q3 (800 rules, 300 zero-hit): the strongest answers sequence *investigation*
(owner query, change-window test) before deletion. Q5 (dual-stack): the IPv6-twin
rule generalizes — "every control you wrote, wrote for one protocol only."

## Lab Troubleshooting (audit-sprint context)
- ACL syntax rejected: platform version variance — provide the syntax sheet for the range's image.
- Students audit the wrong target: file names labeled with module + lecture; re-point.
- Fixes break the test matrix: that's the rollback-plan lesson — require the plan before applying.

## Accessibility Notes
- ACL listings: text files distributed; config screens described line-by-line.
- Sprint deliverable: structured findings template (table) provided.

## CS & Data Science Applications
- **CS:** ACLs as ordered rule evaluation = interpreter semantics; alias compilation is a source-to-source transform — CS students see their compilers course.
- **DS:** hit-counter analysis over time = usage statistics; propose "rule-decay analysis" as a DS stretch task (which rules trend to zero?).

## Links
Plan: `modules/module-03-secure-architecture/lectures/lecture-11-acls-rulebase-engineering.md` · Student page: `docs/lectures/lecture-11-acls-rulebase-engineering.md` · Answers: `teaching/answer-keys/answer-key-module-03.md`
