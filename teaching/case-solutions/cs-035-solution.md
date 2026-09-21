---
case: cs-035
solution-for: modules/module-03-secure-architecture/case-studies/cs-035-least-privilege-egress-acl.md
difficulty: intermediate
module: 3
lecture-anchor: L11
clos: [CLO-4]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-035 Solution — Egress ACL (INSTRUCTOR ONLY)

## Model Solution

**Egress ACL (10 rules):**

| # | Rule | Anchor type | Status |
|---|---|---|---|
| 1 | permit udp 192.168.20.0/24 host <internal-resolvers> eq 53 | internal resolvers only | **enforceable** |
| 2 | deny udp any any eq 53 (log) | kills the 9 hard-coded-DNS PCs' bypass; feeds the remediation list | **enforceable** |
| 3 | permit tcp 192.168.20.0/24 <ERP published IPs> eq 443 | vendor-published IP anchor — strongest | **enforceable** |
| 4 | permit tcp host <BMS-controller> host <BMS-vendor-IP> eq 443 | 1:1 published IP; safety-critical pinned | **enforceable** |
| 5 | permit tcp host <printer-1/2> host <print-cloud IP set> eq 443 | device-scoped to service | **enforceable** (IP set via vendor; else SNI rule) |
| 6 | permit tcp 192.168.20.0/24 <mail-CDN + mailprovider SNI list> eq 443 | SNI-anchor (TLS-inspection-free SNI filtering where FW supports) | **enforceable if SNI-filter; else aspirational** |
| 7 | permit tcp 192.168.20.0/24 <vendor-portal SNI list ×6> eq 443 | SNI anchor | same caveat |
| 8 | permit tcp 192.168.20.0/24 <windowsupdate domain set> eq 443 | domain-set anchor (SNI) | same caveat |
| 9 | permit icmp any any echo/echo-reply/unreachable | diagnostics, scoped types | enforceable |
| 10 | **deny ip any any (log)** | the control that makes it least-privilege | enforceable — and the *primary* control |

**Enforceability honesty:** with no proxy and no TLS inspection, rules 6–8
are only as strong as the firewall's SNI/domain-object support; a plain
packet-ACL cannot express them (it sees IPs) — those become **aspirational
on plain hardware**, and the honest implementation is: IP-anchor the strong
ones (3,4,5), SNI-anchor the rest *if* the NGFW supports SNI objects, and
otherwise route mail/update/portal traffic through a **forward proxy**
(add one; proxy = the honest domain-level control).

**The CDN dilemma:** "permit CDN-IP:443" is a fake control because the same
IP serves update binaries, malware-hosting rentable buckets, and everything
else — you've permitted *the internet's worst neighbors* by IP association.
Two real alternatives:

1. **SNI/domain objects (NGFW or proxy):** anchor to the *name*, which is
   what the vendor actually guarantees — CDN IP rotation stops breaking
   your rules.
2. **Proxy + explicit domain allow-list:** the proxy terminates DNS/HTTP(S)
   by name; the firewall then only needs "office → proxy:3128" — the
   allow-list lives where names are enforceable. (This is why the two-person
   IT team should want the proxy: one list, one place.)

**Ransomware value (2 sentences):** the ACL degrades **C2 and bulk exfil
hard** — commodity botnets' DGA/domain rotation hits the default-deny (rule
10), hard-coded-DNS C2 dies at rule 2, and exfil to unapproved storage has
no allowed path, forcing attackers onto *your* allowed, observable services
(where volume anomalies show). It **cannot** stop attackers who ride the
allowed services themselves (mail-provider exfil, ERP data theft under
valid credentials) — egress control is a floor, not a ceiling; detection on
the allowed paths is the complement.

## Alternative Solutions

- **Full proxy-first redesign (single rule: office→proxy):** architecturally
  cleanest; as a *this-quarter* insurer response, the ACL+proxy hybrid ships
  faster; note the proxy as the year-one end-state.
- **Per-user identity egress (ZTNA-style):** strongest long-term; needs the
  identity project — out of the insurer's timeline.
- **Permit-any-443 + detect:** the honest "we can't do least-privilege
  without a proxy" stance; fails the insurer's requirement — but stating its
  limits earns credit where pretending doesn't.

## Tradeoffs

- Strictness vs breakage: new SaaS onboarding needs a rule (process, owner,
  TTL) — without an onboarding path, staff hotspot around you (see cs-032).
- IP anchors (strong, brittle) vs SNI anchors (flexible, tool-dependent):
  ERP's published IPs win as IP anchors; mail's CDN reality demands SNI.
- Deny-logging without a SIEM: 2-person IT reads weekly digests — the log
  volume must be curated (top-talkers, new-dest alerts only).

## Common Mistakes

- ACL by IP with CDN rules (the fake control).
- Forgetting the hard-coded-DNS bypass — classic audit finding.
- Default-deny without an onboarding/exception process (drives evasion).
- Claiming exfil-proofing while allowing mail attachments (say the limits).

## Instructor Prompts

- "Which rule would the attacker exploit first, and what makes it visible?"
- "Why is rule 2 (deny external DNS) arguably the highest-value rule?"
- "The insurer asks 'what can't this stop?' — answer them."

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Anchor-strength honesty; DNS-bypass closure |
| Technical accuracy | 25% | ACL semantics; CDN/SNI limits correctly stated |
| Alternatives considered | 20% | Proxy-first/ZTNA sequencing |
| Communication | 15% | 10-rule table + 2-sentence ransomware value |

**Timing:** reveal at 5:00 + 2; "what can't this stop" is the integrity test.

## CLO Mapping

- **CLO-4** — Least-privilege egress engineering with honest anchors.
