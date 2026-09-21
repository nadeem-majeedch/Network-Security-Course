# cs-022 — Reflection/Amplification DDoS Response Plan

> **Simulated scenario.** The game studio, networks, and factors are fictional.

## Difficulty & Domain

- **Difficulty:** Intermediate · **Domain:** Network security principles · **CLO:** CLO-2
- **Est. time:** 12 minutes · **Anchor:** L08 (DoS, DDoS & Infrastructure Abuse)

## Scenario

A game studio's matchmaker service (UDP-based) is drowning in inbound traffic
every evening for a week. The studio's own analytics say the inbound bytes far
exceed anything their players could generate. You have the traffic breakdown
below and must write the response plan: identify the attack, immediate
mitigations, and the structural fix.

## Stakeholders

- **Players** — can't queue for matches at peak hours.
- **Studio infra team** — 3 engineers, on-call rotation straining.
- **Hosting provider** — has BGP-based scrubbing and RTBH (remotely triggered
  black-hole) tooling.
- **Open resolvers on the internet** — currently abusing your IP as the
  spoofed source (you are a *victim* who appears to be an *attacker*).

## Network Context

- Matchmaker: UDP/9000, public IP `203.0.113.10/32` announced by the provider.
- Hosting provider offers: customer-triggered RTBH for /32s, BGP flowspec
  (limited), and a scrubbing center with 4 h activation SLA.
- No anycast; single site.

## Available Evidence

**Inbound traffic breakdown (peak hour):**

| Source port | Protocol | Share of inbound bytes | Amplification factor vs outbound request | Source IP count |
|---|---|---|---|---|
| 53 (DNS) | UDP | 42% | ~50× | 8,000+ |
| 123 (NTP) | UDP | 31% | ~200× (monlist-era) | 2,100 |
| 19 (chargen) | UDP | 19% | ~350× | 600 |
| 9000 (real players) | UDP | 8% | 1× | 40,000 |

Edge notes: your service replies normally to source port 9000 traffic;
inbound on 53/123/19 arrives from *thousands* of IPs at their *service*
ports, all destined to your :9000 (your source port when the attacker spoofed it).

## Student Task

1. Name the attack class and explain **mechanically** why the studio is
   receiving traffic it never requested — include the role of source-IP spoofing.
2. Rank the three immediate mitigations for tonight: RTBH your /32 ·
   provider ACL/flowspec dropping inbound UDP 53/123/19 · scrubbing center.
   Justify ordering with collateral-damage reasoning.
3. Give the structural fix (anycast/scrubbing-on-default or equivalent) and
   one **responsible-disclosure action toward the open resolvers** the studio
   should — and should not — take.

## How to Approach This (Reasoning Scaffold)

- The victim never "blocks attackers" here — the attackers are *legitimate
  servers* replying to a spoofed request that looked like it came from you.
- Amplification factor × share = where the bytes come from; blocking the
  *reply* traffic at your edge is cheaper than finding "attackers."
- RTBH is a big hammer: it drops *all* traffic to the /32 — real players too.

## CLO Mapping

- **CLO-2** — Reflection/amplification mechanics and layered response.

## Safety Notes

- Simulated scenario. Scanning the internet for open resolvers without
  authorization is prohibited; "responsible disclosure" here means notifying
  operators via abuse contacts, never testing others' services.
