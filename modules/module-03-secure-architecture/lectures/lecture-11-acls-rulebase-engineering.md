---
lecture: L11
title: ACLs & Rulebase Engineering
module: 3
week: 6
hours: 2
clos: [CLO-4]
difficulty: intermediate
status: complete
artifact-type: teaching-plan
---

# L11 — ACLs & Rulebase Engineering (Teaching Plan)

## 1. Overview & Prerequisites

- **Prerequisites:** L10 (first-match semantics, rulebase concepts, policy spec build).
- **Position:** audit-grade rule engineering. Students leave able to find planted faults in any rulebase — the exact skill Assignment 2 grades and the capstone hardening phase uses.
- **Faculty prep:** prepare two audit targets — a router ACL set with 4 planted faults, and a firewall rulebase export with shadowing/redundancy — plus the audit checklist card.
- **Common misconceptions:** "more rules = more secure"; "implicit deny means I don't need explicit denies"; "ACLs on routers make firewalls redundant."

## 2. Learning Objectives

By the end of this lecture, students can:

1. Read and write router/switch ACLs (standard vs extended) with correct wildcard-mask semantics (Apply).
2. Explain ACL evaluation order, implicit deny, and direction/in-interface binding (Understand).
3. Audit a rulebase for shadowed, redundant, overly permissive, and orphaned rules using a checklist (Evaluate).
4. Apply least-privilege decomposition: object groups/aliases, service decomposition, time-based rules (Apply).
5. Document rules with justification + owner + review date so the rulebase survives staff turnover (Create).

## 3. Detailed Concepts

### 3.1 ACL mechanics on routers/switches
- Standard (source-only) vs extended (proto/src/dst/port); wildcard masks (inverse masks: 0.0.0.255 vs prefix math) — the classic source of accidental any.
- Evaluation: top-down first match, implicit deny at the end; one ACL per direction per interface; placement guidance (extended near source, standard near destination — and why this is a traffic-path decision).
- Statelessness: return traffic needs explicit entries (or *established*-style keywords where available) — the difference from L10 stateful design.

### 3.2 The four rulebase faults (audit taxonomy)
- **Shadowed:** an earlier rule matches first; later rule dead (allow-shadowed-by-deny = the dangerous direction).
- **Redundant:** later rule identical/subsumed — no effect, pure noise.
- **Overly permissive:** ANY source/dest/service where a pair suffices; "temporary" opens with no expiry.
- **Orphaned:** references removed hosts/services; suggests stale design.
- Audit method: per-rule interrogation — why does this exist, who owns it, what breaks if we delete it, does it ever match (hit counters)?

### 3.3 Least-privilege decomposition craft
- Object/alias discipline: named groups (`WEB_SERVERS`, `HR_SUBNET`, `DNS_RESOLVERS`) — rules read like policy, not like addressing plans.
- Service decomposition: split "web = 80+443" when rules differ; explicit vs ranges (`1000-2000` invites abuse).
- Time-based and scheduled rules for maintenance windows; expiry metadata for temporary rules.
- IPv4+IPv6 twins: every v4 rule needs a v6 counterpart or an explicit v6 deny (dual-stack audit blind spot).

### 3.4 Documentation & change control
- Rule metadata: owner, ticket/ticket-link, justification, creation date, review date.
- Change process: request → impact analysis (what matches today) → staged rule (log-only mode where supported) → enforce → verify → document.
- Rulebase as evidence: exports under version control; diff review in PRs (convention ties to repo §7 governance).

### 3.5 From audit findings to fixes
- Findings taxonomy → remediation: tighten (narrow scope), delete (orphan/redundant), reorder (fix shadowing), split (decompose services).
- Verification: hit counters, test traffic matrix, then re-audit; regression risk analysis before deletion (who *might* match this rule?).

## 4. Teaching Sequence (120 Minutes)

| Time | Segment | Instructor moves |
|---|---|---|
| 0–10 | Recap: L10 test matrices | One pair's matrix reviewed; transition: "you built it — now audit your neighbor's" |
| 10–35 | Core: ACL mechanics | Wildcard-mask drill on boards; implicit-deny trap demo; direction binding quiz |
| 35–55 | Core: audit taxonomy | Walk the 2 audit targets live; class tags each fault; checklist card distributed |
| 55–65 | Break | — |
| 65–75 | Core: least privilege + documentation | Alias refactoring demo: 30-line rulebase → 12 readable rules |
| 75–110 | Student activity: audit sprint | Teams of 3 audit the planted-fault targets; produce findings table + fixes (Lab-06 second half, cs-034..036 prep) |
| 110–120 | Wrap + formative | Exit ticket; Assignment-2 (rulebase audit deliverable) briefing; L12 trailer: NAT/proxies/egress |

## 5. Technical Examples

```
# Router ACL with planted faults (audit target A, Cisco-style syntax)
access-list 110 permit tcp 10.1.0.0 0.0.255.255 host 10.2.0.10 eq 443
access-list 110 deny   tcp 10.1.5.0 0.0.0.255 host 10.2.0.10 eq 443   ! shadowed
access-list 110 permit ip 10.1.0.0 0.0.255.255 10.2.0.0 0.0.0.255     ! overly permissive
access-list 110 permit tcp any host 203.0.113.9 eq 25                 ! orphaned? (host decommissioned)
access-list 110 permit tcp 10.1.0.0 0.0.255.255 host 10.2.0.10 eq 443 ! redundant
! implicit deny at end

# Reading the table like an auditor:
show access-lists 110        ! hit counters reveal dead rules
show ip interface vlan20     ! which direction binds which ACL
```
Expected teaching points: hit counters expose orphans; shadow detection requires reading order, not counters; wildcard `0.0.255.255` may be broader than intended (typo audit).

```
# Firewall export (target B) audit checklist card applied:
# [ ] every rule has owner+justification  [ ] no any/any  [ ] v6 twin exists
# [ ] shadow check in order  [ ] hit-count check  [ ] temp rules have expiry
```

## 6. Discussion Questions

1. Why is an allow-shadowed-by-deny more dangerous than the reverse? Construct the incident.
2. When is "standard ACL near destination" wrong? Give the traffic-path scenario.
3. Your rulebase has 800 rules; 300 have zero hits in 90 days. Why can't you delete them all tomorrow?
4. How do you audit a rulebase you inherited with no documentation? First three actions?
5. Dual-stack: what breaks if v6 has no ACL at all on an internet-facing interface?

## 7. Student Activity

**Audit sprint (35 min, teams of 3):** each team audits one target (A or B) with the checklist: findings table (rule id, fault class, evidence, risk, proposed fix), then applies fixes on the range and re-tests traffic. Deliverable feeds Assignment 2. Instructor "red review": tries to find one *false finding* per team (rules that look wrong but are correct) — precision matters in audits.

## 8. Problem-Solving Case

**Primary case — cs-034 "ACL audit: finding shadowed and redundant rules" (intermediate):**
A new firewall admin inherited a 400-line rulebase; a pen-test just reached an internal DB from the guest network. Provided: full rule export, hit counters, and the pen-test path. Students must find the enabling path (allow-shadowed-by-allow ordering flaw plus an any/any for "legacy printing"), classify every contributing fault, and produce a corrected rulebase *with a rollback plan* that doesn't break the legacy printer fleet on day one.
**Linked cases:** cs-035 (least-privilege egress ACL authoring), cs-036 (management-subnet inbound hardening).
*(Model solutions: instructor answer-key set, Module 3.)*

## 9. Formative Assessment

1. Write the wildcard mask for 10.1.5.0/24 — and for a /23.
2. Where is the implicit deny and how do you make it visible/logged?
3. Name the four audit fault classes and one detection signal for each.
4. Why do named aliases improve security (not just readability)?
5. Give two reasons a zero-hit rule may still be needed.
*(Answer key: instructor set, Module 3.)*

## 10. Summary & Key Takeaways

- ACLs are stateless, order-sensitive, and trap-prone — wildcard math and direction binding are where errors live.
- Auditing is a *method* (four fault classes + hit counters + metadata), repeatable on any vendor's export.
- Least privilege is a craft: aliases, decomposition, expiries, and v6 twins turn a rulebase into policy.

## 11. References

- Cisco — Access Control Lists (ACL) configuration and wildcard-mask guides (current docs).
- NIST SP 800-41 Rev. 1 — rulebase policy guidance.
- SANS firewall rulebase audit whitepaper series (checklist methodology).
- CIS Benchmarks — router/switch ACL sections.
- RFC 7123 — Securing IPv4/IPv6 dual-stack networks (v6-twin audit rationale).

## 12. CLO Mapping

| CLO | Where in this lecture | Assessed via |
|---|---|---|
| CLO-4 | §3.1–3.5 mechanics + audit method; audit sprint §7 | Pract-1 (W6), Assignment 2, Lab-06 |
