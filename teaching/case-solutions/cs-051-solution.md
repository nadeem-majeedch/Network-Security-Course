---
case: cs-051
solution-for: modules/module-04-crypto-protocols/case-studies/cs-051-split-tunnel-vpn-risk-assessment.md
difficulty: advanced
module: 4
lecture-anchor: L16
clos: [CLO-5, CLO-7]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-051 Solution — Split-Tunnel Risk Assessment (INSTRUCTOR ONLY)

## Model Solution

**Honest risk delta:**

| Category | Item | Status under split-tunnel | Note |
|---|---|---|---|
| Protection **still holds** | Corp-subnet traffic encrypted + authenticated | ✅ unchanged | the tunnel still does its real job |
| | EDR / device posture | ✅ unchanged | endpoint controls are transport-independent |
| | SaaS confidentiality (TLS) | ✅ unchanged | was TLS-protected either way — full-tunnel *saw* it but couldn't read it |
| Protection **lost** | **Uniform egress policy** (web filtering, DLP at HQ edge) | ❌ direct-to-internet bypasses HQ egress | mitigable: cloud-run egress/ZTNA per-app replaces the HQ chokepoint |
| | **Central DNS control** | ❌ if DNS splits to home resolver — *the* incident vector (router DNS hijack) | the design fix below |
| | Unencrypted legacy app protection | ⚠️ only if such apps exist — inventory says none internet-bound | quantify: zero |
| Protection **myth** | "Full-tunnel protects against compromised home router" | ❌ was already partial: browser-to-SaaS went through the tunnel, but the *router* still carried all of it — a hostile router can drop/redirect regardless; the DNS path was the real control, and it's preservable | the honest sentence: full-tunnel's marginal protection vs a compromised router was DNS + egress, not a magic shield |
| | "Split-tunnel exposes corp LAN to home devices" | ❌ *reverse* folklore: the laptop's routes to corp go via VPN; home devices can reach the laptop, not corp — the real added surface is *local-network attacks on the laptop itself* (SMB exposure, rogue devices) | mitigable: host firewall blocks local subnet except DHCP/DNS/printer mDNS |

**Delta summary:** the *real* losses are centralized DNS + HQ-egress policy;
the real gains are performance and concentrator relief. Both losses are
replaceable with distributed equivalents — which is why the 2026 answer is
not a reflexive "no."

**DNS split design (the graded piece):** split-tunnel with **DNS
exclusions-only split** — corporate resolvers remain the *default* DNS
(jammed-through-tunnel), while only defined high-bandwidth subnets route
via VPN; direct internet flows use **encrypted DNS to corp-approved
resolvers over the internet path (DoH/DoT to corporate resolver VIPs)** —
name resolution never trusts the local router. The incident's vector
(router DNS hijack) dies even though video traffic goes direct. Add:
browser-level DoH managed policy as the second layer.

**Decision (5 bullets, partner- and security-defensible):**

1. **Yes to split-tunnel — but split by *subnets + DNS design*, not "all
   internet direct":** corp subnets via VPN; internet direct; DNS via
   corp DoH/DoT always.
2. **Egress policy moves to the edge where the user is:** cloud web/DLP
   proxy for direct flows (or ZTNA per-app replacing "tunnel to flat
   network" entirely within 12 months).
3. **Host firewall baseline for untrusted local networks:** block inbound
   local-subnet SMB/RDP; allow DHCP/DNS/print — kills the local-attack
   class split-tunnel genuinely adds.
4. **Posture stays mandatory:** EDR + cert + patch-level checks before the
   tunnel grants corp routes; split or full, a sick laptop is the bigger
   risk.
5. **Review trigger:** any incident involving local-network attack or DNS
   manipulation re-opens the decision with data — the decision is
   instrumented, not permanent.

## Alternative Solutions

- **Refuse split-tunnel; fix video with QoS:** defensible if HQ egress/DLP
  is business-critical and unreplaceable; costs partner goodwill and
  concentrator spend; the DNS incident teaches the *real* fix is DNS, not
  the tunnel.
- **Full ZTNA migration now (no split-tunnel debate):** the end-state that
  makes the question obsolete; 12-month project — the proposal above is
  the bridge, not the destination.
- **App-level split only (video domains direct):** surgical; complexity
  per-app and fragile (vendor IP/CDN churn); a legitimate variant worth
  naming.

## Tradeoffs

- Centralized policy vs performance: the cloud-egress spend is the price
  of the performance partners want.
- DNS-via-corp-DoH adds resolver dependency: keep resolvers redundant and
  anycast — otherwise you've moved the outage from the router to the
  resolver.
- Local-firewall strictness vs printing/AirDrop realities: baseline rules
  with an allow path for office-day docking networks.

## Common Mistakes

- Accepting the 2010 folklore wholesale ("split = insecure") without the
  TLS-era delta analysis.
- Missing the DNS question despite the incident handing it to you.
- Treating the home router as protected by full-tunnel (myth column).
- Decision without instrumentation/review triggers.

## Instructor Prompts

- "Which single control, kept under split-tunnel, would have caught last
  year's incident anyway?"
- "What does ZTNA do to this entire debate?"
- "Name the myth that surprised you — why is it folklore?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Three-column delta; DNS-centric design |
| Technical accuracy | 25% | Split-tunnel/DNS/DoH mechanics correct |
| Alternatives considered | 20% | Refuse/QoS and ZTNA paths weighed |
| Communication | 15% | 5-bullet decision both audiences accept |

**Timing:** reveal at 5:00 + 2; the myth column is the debrief's energy.

## CLO Mapping

- **CLO-5** — Cryptographic/protocol realism in VPN design.
- **CLO-7** — Remote-access architecture decision-making.
