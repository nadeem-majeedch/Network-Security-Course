---
case: cs-034
solution-for: modules/module-03-secure-architecture/case-studies/cs-034-acl-audit-shadowed-rules.md
difficulty: intermediate
module: 3
lecture-anchor: L11
clos: [CLO-4]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-034 Solution — ACL Audit (INSTRUCTOR ONLY)

## Model Solution

**Classification:**

| # | Rule | Class | Reason |
|---|---|---|---|
| 1 | permit tcp any host 10.4.1.10 eq 22 | **keep** | host-scoped SSH; 12.4k hits |
| 2 | permit tcp 10.9.9.0/24 any eq 22 | **keep** | admin SSH (any dest); 41k hits |
| 3 | permit tcp any 10.4.0.0/16 eq 22 | **shadowed**? — careful: rule 1 is *narrower* but different (one host); 3 is *broader* than 1 but not fully covered by 1 → not shadowed by 1; **over-broad/dead** | 0 hits and grants SSH to the whole cluster — remove (the 0-hit + broadness pair is the finding) |
| 4 | permit ip 10.9.9.0/24 10.4.0.0/16 | **keep** (redundant-adjacent with 2? no — 2 is dest-*any*, 4 is subnet-pair: overlapping but distinct semantics) | admin→HPC any-protocol; 3.3k hits; candidate for narrowing, not removal |
| 5 | permit tcp any 10.5.0.0/16 eq 443 | **keep** | 1.2M hits |
| 6 | permit tcp 10.9.9.0/24 host 10.5.2.7 eq 443 | **redundant** | fully covered by 5 (same proto/ports, narrower src/dest ⊂ 5); 0 hits *because* 5 fires first — the hit-counter trap |
| 7 | permit udp any any eq 53 | **over-broad → narrow** | 8.9M hits (it's DNS, everyone needs it) but "any any" permits *replies to anyone* — keep function, scope to resolvers |
| 8 | permit ip any 10.4.0.0/16 | **over-broad (dangerous)** | 210 hits; any-protocol to HPC from anywhere on campus — this is how rule 3's intent died; replace with specific flows |
| 9 | permit icmp any any | **over-broad → narrow** | 95k hits; scope to diagnostic types (echo/echo-reply/unreachable) |
| 10 | permit ip any any | **the headline defect** | 4.1M hits — everything below is decoration; make it **deny** (or delete and let implicit deny work) |
| 11 | deny ip any any log | **semantically dead, operationally vital** | 0 hits *because* rule 10 fires first; after fixing 10, this becomes the logging workhorse |

**Hit-counter trap (two parts):**

- **Looks load-bearing, structurally unreachable:** rule 10's 4.1M hits make
  it look essential — it *is* (it matches everything), but that's the defect:
  it's a permit-any-any in disguise; its hits belong to *all other intents*.
- **Looks dead but matters:** rule 11 (0 hits) is the explicit-deny/log
  anchor; and rule 6's 0 hits mean "rule 5 shadows me," not "nobody needs
  me" — the semantic lesson: **0 hits has three different meanings**
  (dead, shadowed, or pre-empted-but-intended).

**Cleaned ACL (top-down):**

| # | Rule | Rationale |
|---|---|---|
| 1 | permit tcp any host 10.4.1.10 eq 22 | unchanged |
| 2 | permit tcp 10.9.9.0/24 any eq 22 | unchanged |
| 3 | permit ip 10.9.9.0/24 10.4.0.0/16 | admin→HPC (kept, watch for narrowing later) |
| 4 | permit udp <campus-resolvers> any eq 53 | DNS scoped |
| 5 | permit udp any host <resolver> eq 53 | replies/queries to resolvers |
| 6 | permit tcp any 10.5.0.0/16 eq 443 | unchanged |
| 7 | permit icmp any any echo / echo-reply / unreachable | diagnostic subset |
| 8 | **deny ip any any log** | now reachable; logging anchor |

(Rules 3/6/8/10/11 of the original deleted as dead/shadowed/over-broad; rule
10's permit-any-any replaced by the deny.)

**Safe-cutover argument:**

- **Stage 1:** fix rule 10 → deny+log (the *only* behavior change; watch the
  log-deny for 7 days — every logged flow is a conversation you're about to
  break; hand the list to NOC, add survivor rules deliberately).
- **Stage 2:** remove 0-hit dead/over-broad rules (3, 8) one change-ticket
  each; keep the log-deny as the tripwire.
- **Rollback trigger:** any *business-justified* flow in the deny log that
  lacks an owner within 24 h → restore immediately, add properly, re-clean.

## Alternative Solutions

- **Delete rule 11 entirely and rely on implicit deny:** loses the logging
  anchor — worse, not cleaner.
- **Clean everything in one change:** fails the NOC's risk posture; staging
  is the point of the safe-cutover argument.
- **Keep rule 8 "because research needs flexibility":** the 210 hits *are*
  researchers' ungoverned flows; replace with governed rules *after* the
  deny-log tells you what they actually do.

## Tradeoffs

- Explicit denies (audit-visible) vs rulebase length: keep one deny+log;
  no blanket explicit-deny-per-service noise.
- Scope-tightening speed vs researcher friction: the 7-day deny-log window
  converts "security says no" into "here's the governed rule for what you do."

## Common Mistakes

- Classifying by hits alone (rule 10 vs rule 11 inversion).
- Missing that rule 6 is *shadowed*, not dead — "why would anyone write it?"
  is exactly the 8-year-accumulation question.
- Cleaning without the log-deny tripwire (changes become archaeology).
- Scoping DNS/ICMP rules so narrowly they break lookups/pmtud (the pendulum
  swing failure).

## Instructor Prompts

- "Which single rule *caused* the rest of the mess, and when?"
- "Give the three meanings of 0 hits."
- "What does the NOC need to see before stage 2?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Reachability tracing; 0-hits triple meaning |
| Technical accuracy | 25% | Cleaned ACL enforces intent; stateless return-path respected |
| Alternatives considered | 20% | Staging/rollback design |
| Communication | 15% | Classification + cleaned table |

**Timing:** reveal at 5:00 + 2; the rule-10 reveal is the case's punchline.

## CLO Mapping

- **CLO-4** — ACL defect classification and safe remediation.
