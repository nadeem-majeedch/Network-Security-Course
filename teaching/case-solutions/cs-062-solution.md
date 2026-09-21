---
case: cs-062
solution-for: modules/module-05-wireless-cloud/case-studies/cs-062-security-group-vs-nacl-control-choice.md
difficulty: advanced
module: 5
lecture-anchor: L19
clos: [CLO-13]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-062 Solution — SG vs NACL (INSTRUCTOR ONLY)

## Model Solution

**Problem 1 — app→DB 5432, autoscale-proof:**
**Security group with source=app-tier SG** (chaining). Defense: SGs are
instance-attached and *membership-based* — a new autoscaled instance
joining the app SG inherits the grant with zero rule edits; a CIDR-based
rule (or NACL CIDR pair) rots on the first subnet re-design. Stateful
semantics fit: the DB's return traffic is automatic, no ephemeral
bookkeeping. Owner: platform (the SG chain is architecture, not app
config).

**Problem 2 — weekly-changing malicious-IP blocklist:**
**Not the NACL (alone) — the right construct is a managed
network-firewall/threat-feed layer** (provider network firewall with
feed integration, or edge WAF for HTTP); NACL is the *fallback* for
non-HTTP. Defense: NACLs *can* deny CIDRs (stateless, deny-capable —
semantically the fit), but rule-numbered NACL edits for a weekly feed
are a change-management treadmill with rule-count limits and ordering
fragility; the managed firewall consumes feeds programmatically and
logs the matches. **Keep one NACL deny-line as a cheap backstop for the
top-feed entries** (defense in depth), but the *system* of record is
the feed-integrated firewall. Owner: security (feed), platform
(backstop).

**Problem 3 — nonprod can never initiate to prod (env fence):**
**NACLs on the prod subnets** (deny nonprod CIDR ranges inbound; allow
list the rest) — *because an SG edit cannot bypass a NACL*, and the
threat model is "an app team edits an SG": SGs are app-editable in
practice; NACLs are platform-owned subnet fences. Stateless semantics
are a feature here: the fence is direction-based, not connection-based.
Add provider guardrails (SCP/Org-policy style) if available. Owner:
platform only.

**Problem 4 — web tier only via edge LB:**
**Two mechanisms, layered:** (a) SG-chaining (web SG ingress from
sg-LB's SG only), and (b) **route/design guarantee — web subnets have
no IGW route and no public IPs** (isolated-by-routing). *Failure mode of
the naive SG-source-only answer:* SGs filter by source IP/SG — they do
**not** understand HTTP; a request that reaches the instance *via any
path* (the IPv6 route you forgot, a peer-VPC path, the bastion that can
reach everything) rides a *source* that satisfies the SG — and host
headers/X-forwarded checks live in the app, which apps ignore. The
routing-layer guarantee (no inbound route exists at all) plus SG-chaining
is the pair that fails closed. Owner: platform.

**Problem 5 — DNS egress to approved resolvers only:**
**DNS firewall / resolver-policy construct** (provider DNS firewall or
outbound-endpoint policy) + SG egress blocking TCP/UDP 53 to non-resolver
destinations. Defense: SG egress rules *can* pin 53-egress to resolver
IPs, but DoH/DoT (443/853) escapes any port-53 rule — the DNS-*layer*
policy (resolver logs, domain filtering, blocking known DoH endpoints)
is the real control; the SG/NACL pieces are the fence. This is also the
anti-exfil story (cs-010/cs-025 callbacks). Owner: platform + security.

**The pattern across all five:** stateful membership-based grants (SG)
for *tiering*, stateless deny-capable fences (NACL) for *platform-owned
boundaries*, purpose-built constructs (DNS firewall, feed firewall,
routing design) where the semantics outclass both.

## Alternative Solutions

- **NACL for problem 1 (CIDR-pair allow):** works until autoscale
  re-subnets; rejected for rot.
- **SGs for problem 3 (deny via absence):** "absence-of-allow" fails the
  requirement — an app team *adds* the allow; deny-capable stateless
  fences exist for exactly this.
- **WAF-only for problem 2:** covers HTTP only; the feed-firewall covers
  all protocols — the WAF is the HTTP front of the same design.

## Tradeoffs

- SG-chaining elegance vs debuggability: SG-source rules are invisible
  in packet logs (membership, not addresses) — document the chains.
- NACL fences vs change velocity: platform-owned = slow-but-certain;
  that *is* the fence contract.
- Feed-firewall cost vs NACL backstop: buy the integration; keep the
  free backstop.

## Common Mistakes

- Choosing by familiarity (SG for everything) instead of semantics.
- Missing that SGs can't deny (problem 3's whole point).
- Port-53-only DNS control (DoH escape).
- "SG-source = only-via-LB" without the routing guarantee (problem 4's
  failure mode).

## Instructor Prompts

- "For problem 3, walk the app-team edit that defeats an SG-only fence —
  and why the NACL doesn't care."
- "Which problem did you *want* to solve with an SG but couldn't? Why?"
- "What logs would you ship to prove each control is alive?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Stateful/stateless semantics drive all five |
| Technical accuracy | 25% | Deny/order/membership mechanics correct |
| Alternatives considered | 20% | Wrong-tool variants named and rejected |
| Communication | 15% | Five defenses each a tight paragraph |

**Timing:** reveal at 5:00 + 10; problem 3 is the reveal (SGs can't
deny).

## CLO Mapping

- **CLO-13** — Cloud control-mechanism selection with semantic precision.
