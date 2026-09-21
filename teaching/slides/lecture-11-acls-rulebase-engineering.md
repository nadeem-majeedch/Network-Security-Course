---
marp: true
theme: default
paginate: true
lecture: L11
week: 6
clos: [CLO-4]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# ACLs & Rulebase Engineering

**Network Security · Lecture 11 · Week 6**

*Rules age like milk. Engineering keeps them edible.*

<!-- notes: OPEN (2 min). Hook: "A rulebase written once and reviewed
never is the attacker's favorite document." -->

---

## Learning Objectives

1. **Write** ordered ACLs with first-match semantics — correctly
2. **Audit** a rulebase for shadowed, redundant, and orphaned rules
3. **Distinguish** implicit vs explicit deny and their logging value
4. **Engineer** change control so the rulebase stays true
5. **Reconcile** flow logs against rules to find the fiction

<!-- notes: (1 min) Objective 2 is the Pract-1 practical (week 6);
objective 5 is the audit skill the midterm C1 section grades. -->

---

## ACL Mechanics: Order Is the Policy

```
 1. permit tcp host 10.99.0.10 10.99.0.0/24 eq 22   ← jump host FIRST
 2. deny   tcp any 10.99.0.0/24 eq 22 log           ← everyone else
 3. permit tcp any 10.99.0.0/24 established         ← returns
    (implicit deny all)
```

- First match wins — a broad permit above a specific deny **erases** it
- The implicit deny is always last: unmatched = dropped

![bg right:34% fit](diagrams/04-acl-stateful-flow.md)

<!-- notes: (6 min) The two-rule ordering trap is the single most
tested ACL fact on this course (quiz 3 C8, midterm C1, QB-040). Walk
the diagram 04 flow alongside. -->

---

## Rule Anatomy: What Good Looks Like

- Specific: `src, dst, port, protocol` all named — `any` is a debt
- Documented: `! change 4471: ticket-2213, owner: neteng`
- Logged when denied: the SIEM feeds on deny lines

<!-- notes: (4 min) "any is a debt" is the phrase for the quiz. The
comment discipline is what makes rulebases auditable years later
(cs-034's audit case assumes it). -->

---

## Shadowed, Redundant, Orphaned

| Defect | Meaning | Cost |
|---|---|---|
| Shadowed | unreachable (an earlier rule covers it) | false sense of control |
| Redundant | duplicate of another rule | noise, audit bloat |
| Orphaned | matches nothing (asset gone) | unmanaged surface |

- Audit tooling exists; the *method* is flow-log reconciliation

<!-- notes: (5 min) cs-034's audit case IS this table. The three
defects are quiz/exam material; the method line is the practical. -->

---

## Implicit vs Explicit Deny

- Implicit deny: silent, universal — free but invisible in logs
- Explicit deny with `log`: visible, classifiable, SIEM-able
- Design: explicit+log for the *interesting* denies, implicit for the
  rest

<!-- notes: (4 min) The design judgment (what deserves a log line) is
operational maturity. Quiz-3/quiz-8 both test the distinction's
concept. -->

---

## Rulebase Hygiene Cycle

1. Reconcile: flows vs rules → the fiction list
2. Remove/repair: orphans, shadows, over-broad `any`
3. Re-verify: replay before/after (the regression-safety rule)
4. Document: change record with owner + ticket

<!-- notes: (5 min) The cycle is Pract-1's skeleton. The replay step
is the same regression discipline as alert tuning (L22) — say so;
students transfer it. -->

---

## Change Control: Who May Add Rules

- Emergency-change path exists (fires happen) — with post-review
- Standing approval matrix: who may permit what, to where
- The alternative: rulebase sprawl → shadow IT → the 2 a.m. audit

<!-- notes: (4 min) Governance per course register: process as control.
cs-086's conversion rule (owned, dated, verifiable) applies to rulebase
changes verbatim. -->

---

## Egress ACLs: The Flip Side

- Inbound = who touches you; **egress = who you become**
- Allow-list: updates, DNS, specific SaaS; deny+log the rest
- C2/exfil containment value (L08's continuity, cs-035's case)

<!-- notes: (5 min) Egress is the highest-leverage, least-glamorous
ACL. QB-013 + cs-035 carry the depth. The "who you become" phrasing
sticks. -->

---

## CS/DS Example: The Cluster Egress ACL

```
 permit tcp 10.50.0.0/24 → pkg-mirror 443
 permit tcp 10.50.0.0/24 → lake-api 443
 deny   ip  10.50.0.0/24 → any log
```

- Three rules; the cryptomining cs-088 would have died here

<!-- notes: (3 min) The three-line allow-list is the DS estate's
highest-value artifact — show it as small and achievable, not heroic. -->

---

## Activity: Fix the Broken Rulebase (7 min)

Given 8 rules with 4 defects (shadow, orphan, broad permit, missing
log): find, classify, fix, justify order.

<!-- notes: (7 min) Pract-1's warm-up. Debrief: one defect per type.
The "justify order" requirement rehearses first-match discipline. -->

---

## Case Study: cs-036 (5 min)

- Management-subnet inbound ACL — design the admin plane's rules

<!-- notes: (5 min) The case applies today's mechanics to the highest-
value zone. cs-031's stateful evaluation case is the backup. -->

---

## Formative Check

- Oral: given rules 1-permit-any-80, 2-permit-10.1.1.5-443 — what's
wrong?

<!-- notes: (2 min) Exit oral: rule 1's `any` source makes rule 2's
*destination* fine but ordering fine — the trap is a broad permit that
shadows a future deny. Expect discussion; that's the learning. -->

---

## References & Next

- NIST SP 800-41; vendor ACL syntax guides
- Diagrams: `diagrams/04-acl-stateful-flow.md`
- **Next (L12):** NAT, proxies, egress & NAC — the edge's supporting
  cast
