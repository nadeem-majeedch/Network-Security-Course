---
case: cs-022
solution-for: modules/module-02-network-threats/case-studies/cs-022-reflection-amplification-response.md
difficulty: intermediate
module: 2
lecture-anchor: L08
clos: [CLO-2]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-022 Solution — Reflection/Amplification DDoS (INSTRUCTOR ONLY)

## Model Solution

**Attack class: UDP reflection/amplification (multi-vector: DNS + NTP +
chargen).** The attacker sends small UDP queries with the **spoofed source IP
= the studio's IP (203.0.113.10)** to thousands of open DNS/NTP/chargen
servers. Those servers reply — legitimately, to the "source" of the request —
flooding the studio with amplified replies (50×/200×/350×). The studio never
requested anything; it is the spoofed return address. This is why blocking
"the attackers" is impossible: they are 10,700 well-meaning public servers.

**Why the source-IP spoofing works (and the network's role):** IP allows
source spoofing; BCP 38 (uRPF at the edge) prevents networks from emitting
spoofed traffic. The attacker's *ingress* network lacks uRPF — the studio's
remedy is defensive filtering, not finding one network among thousands.

**Tonight's mitigation ranking:**

| Rank | Option | Reasoning |
|---|---|---|
| 1 | **Provider ACL/flowspec dropping inbound UDP src-port 53/123/19** | Surgical: the studio's real service speaks UDP/9000 with *its* replies from source port 9000 — inbound traffic with source ports 53/123/19 is 100% attack (players never use those source ports). Zero collateral damage; provider-side = protects the uplink. |
| 2 | **Scrubbing center (4 h SLA)** | Catches all vectors + future variants; costs the SLA wait and a routing change. Right second move — pairs with #1 immediately. |
| 3 | **RTBH the /32** | Last resort: black-holes *all* traffic to the IP — real players too. It converts "service down" into "service down, deliberately" — only defensible if attack traffic is ~100% and inbound ACLs can't be deployed. |

**Structural fix:** move the matchmaker behind **anycast with always-on
scrubbing** (or a DDoS-protection CDN for UDP where feasible): the attack
spreads across many anycast sites instead of concentrating on one pipe, and
scrubbing is always engaged (no SLA race). Single-site + on-demand scrubbing
is the shape that loses this fight. Also: source-port hygiene — replying
services are fine, but the *public* service should not be the only target;
internal control planes must not share the public IP.

**Responsible-disclosure action toward the open resolvers:**

- **Should:** email abuse/security contacts of the 10,700 reflecting servers
  (the DNS/NTP/chargen operators) with evidence (timestamps, the spoofed
  queries seen in your captures) asking them to close the amplification
  (disable recursion for DNS, restrict monlist, disable chargen). This is
  *reducing the attacker's arsenal* — the correct community action.
- **Should not:** probe/scan the resolvers yourself to "confirm" they're open
  (unauthorized testing), publish a shaming list before notification, or
  attempt counter-flooding (illegal and counterproductive).

## Alternative Solutions

- **"Block the source IPs of the reflectors."** 10,700 IPs that change hourly;
  an ACL of thousands of entries at line rate — doomed; and tomorrow a new
  set. The *source-port* rule is the stable discriminator.
- **"Switch matchmaker to TCP."** TCP reflection is far weaker (handshake
  blocks spoofing) — a real architectural improvement, but a rewrite; note it
  as roadmap, not tonight.
- **"Buy more bandwidth."** Amplification arithmetic (350× chargen) makes
  bandwidth purchases a treadmill; scale the *filtering*, not the pipe.

## Tradeoffs

- Provider ACL agility vs change-window friction: ask the provider for a
  self-service flowspec/ACL portal in the contract renewal — tonight you
  need a human with a phone.
- Always-on scrubbing cost vs on-demand SLA: always-on wins when attacks are
  recurring weekly — this studio's pattern.
- AnyCast on UDP services: adds state-sync complexity for the matchmaker;
  design the anycast at the *edge filter* layer even if the service stays
  single-site initially.

## Common Mistakes

- Treating the reflecting servers as "attackers to block" — they're victims/tools.
- Missing the source-port asymmetry (inbound src 53/123/19 vs your service's
  src 9000) — the one clean filter.
- Ranking RTBH first (kills service deliberately).
- Proposing to "find the attacker network" — unattributable and not actionable
  by the victim.

## Instructor Prompts

- "Compute the attacker's cost-per-byte: 1 Gbps of chargen amplification
  needs how much attacker bandwidth?" (~3 Mbps — the economics of the attack.)
- "Why does BCP 38 at the *attacker's* edge end this attack class?"
- "What does your service's own source-port discipline guarantee for the
  inbound-ACL design?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Reflection mechanics; collateral-damage-aware ranking |
| Technical accuracy | 25% | Amplification arithmetic; uRPF/BCP 38; source-port filter |
| Alternatives considered | 20% | IP-blocking/rewrite-bandwidth alternatives rejected |
| Communication | 15% | Plan-shaped answer with should/should-not disclosure |

**Timing:** reveal at 5:00 + 2; the cost-per-byte computation is the
quantitative anchor.

## CLO Mapping

- **CLO-2** — Reflection/amplification mechanics and layered response.
