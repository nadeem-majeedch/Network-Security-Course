---
case: cs-021
solution-for: modules/module-02-network-threats/case-studies/cs-021-syn-flood-diagnosis-mitigation.md
difficulty: intermediate
module: 2
lecture-anchor: L08
clos: [CLO-2]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-021 Solution — SYN Flood (INSTRUCTOR ONLY)

## Model Solution

**Diagnosis: confirmed SYN flood; the saturating resource is the *uplink
packet rate* (97%), with LB state a second-order victim.**

Key readings: completed handshakes stay flat (~350–390/s) while SYNs explode
→ the extra SYNs are never completing (flood shape). LB CPU is only 71%
→ the LB is not CPU-bound; uplink at 97% with ~90k SYNs/s of small packets
→ the wire's *packet rate* is the first bottleneck. This matters: fixes that
only protect the LB (SYN cookies) help the *service* but not the *wire* —
legit shoppers' SYNs still drown in attack SYNs at the uplink. Tonight's fix
must remove attack traffic **before** the uplink, not at the end host.

**Tonight's mitigation: activate provider scrubbing (2 h SLA) AND enable SYN
cookies immediately as the bridge.** Rationale: cookies are a config flag
(minutes, no architecture change) that stops LB-queue exhaustion now;
scrubbing (clean pipe / downstream filtering) is the only option that
relieves the uplink. If forced to choose exactly one: scrubbing — because the
uplink is the saturated resource; cookies alone would leave shoppers' SYNs
competing with attack SYNs for the same 1 Gbps.

Rejected options, named:

- **Edge SYN rate-limit:** with 12,000 source IPs, per-IP limits barely bite;
  global limits throttle real shoppers too.
- **Move DNS to a CDN tonight:** changing DNS requires TTL luck (what's the
  record's TTL? if 3600, the switch takes hours to propagate) — wrong tool
  for tonight, right for the two-week plan.

**Pre-rehearsal architecture (one paragraph):** put a **CDN/scrubbing service
in front of the origin** and move the public A record to it (with a short
TTL *before* cutover): the CDN absorbs and terminates client TLS at the edge,
applies managed L3/L4 + L7 DDoS rules, and forwards only validated traffic
over a protected path (origin pulled behind an allow-list that accepts
traffic only from the CDN's ranges). Origin's public IP is retired from DNS
entirely — direct-to-IP attacks hit a wall, and the SYN-flood class against
the origin uplink ends because the flood meets the CDN's multi-Tbps edge, not
a 1 Gbps uplink. Add: SYN cookies left permanently on, health checks exempted
from any rate rules, and a game-day runbook (scrubbing activation drilled,
not just contracted).

## Alternative Solutions

- **Scrubbing-only tonight (no cookies):** defensible; SLA latency (2 h)
  leaves a gap — cookies cost nothing and cover it.
- **Immediately null-route the noisiest /24s:** with 12k IPs spread widely,
  null-routing mostly burns legitimate ranges; a blunt instrument tonight.
- **Pay the vendor's "instant activation" premium:** the incumbent has a 2 h
  SLA — a pre-existing contractual lever beats an on-the-spot premium unless
  the SLA is breached.

## Tradeoffs

- SYN cookies: tiny CPU cost + loss of kernel-level backpressure — near-zero
  downside vs the legacy fear; tune and move on.
- CDN cutover: changes operational surface (certs, headers, caching rules)
  — schedule *before* the rehearsal, rehearse exactly that.
- Origin IP retirement: breaks hard-coded client integrations — inventory API
  consumers before flipping.

## Common Mistakes

- Choosing SYN cookies as *the* fix — misreads which resource saturated.
- Rate-limiting per-IP against a 12k-IP spread.
- Ignoring DNS TTL in the "tonight" plan.
- Rehearsal plan that adds the CDN *during* the rehearsal.

## Instructor Prompts

- "Where do the attack SYNs *die* in each option — end host, LB, uplink, or
  upstream?"
- "Why is flat handshake count the fingerprint of flood rather than flash crowd?"
- "What's your TTL and what does it cost you tonight?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Uplink-pps-first saturation analysis; tonight-vs-two-weeks separation |
| Technical accuracy | 25% | Cookies/scrubbing/TTL mechanics correct |
| Alternatives considered | 20% | Each rejected option's failure named |
| Communication | 15% | Decision-first framing the CTO asked for |

**Timing:** reveal at 5:00 + 2; the "where do SYNs die" prompt is the
transferable mental model.

## CLO Mapping

- **CLO-2** — DoS mechanics and mitigation engineering.
