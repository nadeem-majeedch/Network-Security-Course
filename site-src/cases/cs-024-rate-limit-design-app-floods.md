# cs-024 — Rate-Limit Design Against Application-Layer Floods

> **Simulated scenario.** The ticketing platform, endpoints, and limits are fictional.

## Difficulty & Domain

- **Difficulty:** Intermediate · **Domain:** Network security principles · **CLO:** CLO-2
- **Est. time:** 12 minutes · **Anchor:** L08 (DoS, DDoS & Infrastructure Abuse)

## Scenario

A concert-ticketing platform survives the on-sale hour mostly, but ticket
scalpers' bots complete thousands of valid HTTPS requests to the *search*
endpoint, crowding out real fans. The platform owner wants a rate-limit
design for three endpoints. Numbers below. Design must survive NAT'd mobile
carriers (thousands of fans per egress IP) without locking them out.

## Stakeholders

- **Fans** — must win tickets fairly; false blocks are revenue loss.
- **Platform owner** — fairness + uptime.
- **Scalper operators** — adaptive adversaries; will react to your limits.
- **Mobile carriers** — their NATs concentrate fans behind few IPs.

## Network Context

- Endpoints: `/search` (read-heavy, 40 ms typical), `/queue` (join waiting
  room), `/checkout` (expensive, payment hooks).
- Traffic: 85% of users come through ~200 carrier NAT egress IPs; 15%
  residential, distinct IPs.
- Bots: datacenter-hosted, ~300 IPs, TLS-fingerprintable as non-browser.
- Current controls: none beyond web-server connection caps.

## Available Evidence

**On-sale hour last event (per minute):**

| Metric | `/search` | `/queue` | `/checkout` |
|---|---|---|---|
| Requests | 480k | 95k | 6k |
| P95 latency | 380 ms | 90 ms | 220 ms |
| Distinct source IPs | 3,100 | 2,900 | 1,900 |
| Distinct TLS fingerprints | 28 | 21 | 9 |
| Cart conversion (/checkout) | — | — | 2.1% (legit ~9%) |

Anecdote: one carrier egress IP sent 61k `/search` req/min — all fans, all
200-OKs; a datacenter IP sent 9k req/min with the top 3 bot fingerprints.

## Student Task

1. Explain why **per-IP rate limiting is structurally wrong here** — cite the
   evidence numbers that break it in *both* directions (false-blocks and misses).
2. Design a **three-endpoint rate-limit policy** with: limit dimension (IP /
   fingerprint / token / UA), threshold logic (fixed vs token bucket, burst),
   and the action (throttle/captcha/challenge/drop). One table.
3. State how the design responds when scalpers **rent residential proxies**
   ( defeating IP heuristics) — which dimension still separates them?

## How to Approach This (Reasoning Scaffold)

- A good limit key must be *shared by attackers* and *not shared by fans* —
  IP fails both tests here; fingerprint/token partial.
- Token bucket ≠ fixed window: bursty fans behind NAT need burst credit.
- Defense in depth: cheap broad controls first, expensive discriminating
  controls last.

## CLO Mapping

- **CLO-2** — Application-layer flood mitigation design.

## Safety Notes

- Simulated platform; anti-bot design is defensive. No scraping-tool
  instructions are provided.
