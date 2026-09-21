# L11 — ACLs & Rulebase Engineering

## 1. Learning Objectives

By the end of this session you can: (1) read and write router/switch ACLs with correct wildcard-mask semantics; (2) explain evaluation order, implicit deny, and direction binding; (3) audit a rulebase for the four fault classes; (4) apply least-privilege decomposition (aliases, service splitting, expiries); (5) document rules so the rulebase survives staff turnover.

## 2. Key Definitions

| Term | Definition |
|---|---|
| ACL | Access Control List — ordered permit/deny rules evaluated top-down, first match |
| Wildcard mask | Inverse mask (0 = must match, 1 = don't care): /24 = 0.0.0.255 |
| Implicit deny | The invisible "deny all" at every ACL's end |
| Shadowed rule | Unreachable rule (earlier rule matches first) |
| Redundant rule | Later duplicate/subset of an earlier rule — pure noise |
| Orphaned rule | References removed hosts/services — stale design evidence |
| Hit counter | Per-rule match count — the "is this rule alive?" signal |
| Least privilege | Minimum access required for function — enforced via aliases + decomposition |

## 3. Detailed Explanations

### 3.1 ACL mechanics on routers and switches
- **Standard ACLs** match source only; **extended** match protocol + source + destination + ports.
- **Wildcard masks** are inverse masks — `0.0.0.255` means "first three octets must match." The classic typo: `0.0.255.255` where `0.0.0.255` was intended — a /16-sized hole instead of /24.
- Evaluation: top-down, first match wins, **implicit deny at the end**. One ACL per direction per interface; extended ACLs belong near the *source*, standard near the *destination* (a traffic-path decision).
- **Statelessness:** unlike L10's stateful firewall, return traffic needs explicit entries (or established-style keywords where available).

### 3.2 The four fault classes (your audit taxonomy)
1. **Shadowed** — an earlier rule matches first; the later rule is dead. *Allow-shadowed-by-deny* is the dangerous direction: the deny you believe protects you never fires.
2. **Redundant** — identical/subsumed later rules: no effect, pure noise that hides real policy.
3. **Over-permissive** — any/any sources or services; "temporary" opens without expiry.
4. **Orphaned** — rules for decommissioned hosts/services: evidence of process decay.
Audit method per rule: *why does it exist, who owns it, what breaks if deleted, does it ever match (hit counters)?*

### 3.3 Least-privilege decomposition craft
Named **aliases/objects** (`WEB_SERVERS`, `DNS_RESOLVERS`) make rules read like policy. **Service decomposition**: split "web = 80+443" when the rules differ; explicit ports over ranges (`1000-2000` invites abuse). **Time-based rules** for maintenance windows; **expiry metadata** on temporary rules. And the dual-stack rule every audit misses: every IPv4 rule needs an IPv6 twin or an explicit IPv6 deny (RFC 7123 logic).

### 3.4 Documentation and change control
Rule metadata: owner, ticket link, justification, creation date, review date. Change flow: request → impact analysis (what matches today?) → staged rule (log-only where supported) → enforce → verify → document. Rulebase exports live under version control; changes are reviewed as diffs — the same governance habit as code.

### 3.5 From findings to fixes
Findings → remediation: **tighten** (narrow scope), **delete** (orphan/redundant), **reorder** (fix shadowing), **split** (decompose services). Verify with hit counters and a traffic test matrix, then re-audit. Deletion needs regression reasoning: *who might match this rule that doesn't show in counters?*

## 4. Network Diagram: where the ACL binds and why direction matters

```
 Traffic: CORP(10.1.0.0/16) ──► SERVERS(10.2.0.0/24)
                │
        [interface vlan20, ACL 110 IN]   ← extended ACL near the SOURCE leg
                │  rule 1 permit tcp 10.1.0.0/16 host 10.2.0.10 eq 443
                │  rule 2 deny   tcp 10.1.5.0/24 host 10.2.0.10 eq 443  ← SHADOWED
                │  rule 3 permit ip  10.1.0.0/16 10.2.0.0/24            ← too broad
                │  ... implicit deny
```

## 5. Protocol Examples

- Wildcard math drill: 10.1.5.0/24 → `10.1.5.0 0.0.0.255`; a /23 → `0.0.1.255`; a single host → `0.0.0.0` (or `host`).
- Hit-counter read: `show access-lists 110` — rules with 0 matches over 90 days are orphan *candidates*, not automatic deletes (see §11 Q5).

## 6. Configuration Concepts (Cisco-style, concept level)

```
 ip access-list extended WEB-ACCESS
  10 permit tcp 10.1.0.0 0.0.255.255 host 10.2.0.10 eq 443
  20 deny   tcp 10.1.5.0 0.0.0.255 host 10.2.0.10 eq 443   ! dead: shadowed
  30 permit udp any host 10.2.0.53 eq 53                    ! resolver only
  100 deny ip any any log                                   ! explicit + logged
 interface vlan20
  ip access-group WEB-ACCESS in
```

## 7. Security Implications

- ACLs are stateless, order-sensitive, and trap-prone — wildcard and direction errors are where breaches live.
- Auditing is a *repeatable method* (four fault classes + hit counters + metadata), vendor-independent.
- Undocumented rulebases are institutional risk: the knowledge walks out with the admin.

## 8. Realistic Organizational Scenario

**The inherited 400-line rulebase (running case).** A new firewall admin inherits an undocumented export; a pen test just reached an internal DB from the guest network. The export shows an allow-shadowed-by-allow ordering flaw plus an any/any rule marked "legacy printing." You classify every contributing fault, produce a corrected rulebase *with a rollback plan* that doesn't break the printer fleet on day one. Full case: **cs-034**; the planted-fault audit is Lab-06 part 2 and Assignment 2.

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "More rules = more secure" | Every rule is a liability surface; least privilege means *fewer, tighter* rules. |
| "Implicit deny covers me" | Silent implicit deny gives no evidence; explicit logged denies give intent. |
| "Zero-hit rules are safe to delete tomorrow" | Backup windows, failover paths, and rare maintenance may not hit in 90 days. |
| "ACLs make firewalls redundant" | They complement: ACLs near the source, stateful policy at choke points. |
| "IPv6 doesn't need ACLs" | Dual-stack audits are where attackers live (RFC 7123). |

## 10. Classroom Activities

1. **Audit sprint (teams of 3):** two planted-fault targets (router ACL set + firewall export) → findings table (rule id, fault class, evidence, risk, fix), then apply + re-test on the range.
2. **Wildcard speed round:** ten prefixes → masks, timed.
3. **Alias refactoring demo→do:** 30-line rulebase → 12 readable rules with objects.

## 11. Problem-Solving Questions

1. Why is allow-shadowed-by-deny more dangerous than the reverse? Construct the incident.
2. When is "standard ACL near destination" wrong? Give the traffic-path scenario.
3. 300 of 800 rules have zero hits in 90 days — why can't you delete them all tomorrow?
4. You inherit an undocumented rulebase: what are your first three actions?
5. What breaks if IPv6 has no ACL at all on an internet-facing interface?

## 12. Exit Ticket

1. Write the wildcard mask for 10.1.5.0/24 — and for a /23.
2. Where is the implicit deny, and how do you make it visible?
3. Name the four fault classes and one detection signal for each.
4. Why do named aliases improve *security*, not just readability?
5. Give two reasons a zero-hit rule may still be needed.

*(Answers: `the instructor answer-key collection (not published)`.)*

## 13. References

- Cisco ACL configuration guides and wildcard-mask reference (current).
- NIST SP 800-41 Rev. 1 — rulebase policy guidance.
- RFC 7123 — Securing IPv4/IPv6 dual-stack networks.
- CIS Benchmarks — router/switch ACL sections.
- SANS firewall rulebase audit methodology (whitepaper series).

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-4 | §3 mechanics + audit method; sprint §10 | Pract-1 (W6), Assignment 2, Lab-06 |
