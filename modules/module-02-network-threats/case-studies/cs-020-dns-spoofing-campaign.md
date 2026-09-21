---
case: cs-020
title: DNS-Spoofing Campaign on a Client Estate
difficulty: beginner
domain: DNS and DHCP security
module: 2
lecture-anchor: L07
clos: [CLO-2]
time-estimate: 12 min (5 min reasoning + 7 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-020-solution.md
---

# cs-020 — DNS-Spoofing Campaign on a Client Estate

> **Simulated scenario.** The MSP, clients, and alerts are fictional.

## Difficulty & Domain

- **Difficulty:** Beginner · **Domain:** DNS and DHCP security · **CLO:** CLO-2
- **Est. time:** 12 minutes · **Anchor:** L07 (Sniffing, MITM & Session Attacks)

## Scenario

A managed service provider (MSP) monitors 40 small-business clients. In one
week, six clients — all on the same ISP's business broadband — report
intermittent redirects: "our banking site shows our login page but then errors."
The MSP's central DNS query logs (from clients' egress) show the pattern
below. The ISP denies any problem. You are the MSP's escalation analyst.

## Stakeholders

- **Six affected client businesses** — potential credential theft.
- **The MSP** — liability and reputation.
- **The ISP** — denies involvement; is a suspect nonetheless.
- **End users** — may have submitted credentials to the impostor.

## Network Context

- All six clients use the ISP's supplied router in bridge-off mode (router
  does DHCP+DNS forwarding to ISP resolvers).
- No DNSSEC on the targeted domains (a regional bank chain and a payroll SaaS).
- Clients' endpoints are fully patched; browsers enforce HSTS on the payroll
  SaaS but **not** on the regional bank's site.

## Available Evidence

**MSP central DNS log excerpt (one affected client):**

| Time | Query | Answer seen | Cache status |
|---|---|---|---|
| 09:02:11 | `bank-regional.example` A | 198.51.100.23 (legit) | fresh |
| 09:02:59 | `bank-regional.example` A | **203.0.113.150** | fresh (0 TTL!) |
| 09:03:04 | `bank-regional.example` A | 198.51.100.23 (legit) | fresh |
| 09:03:31 | `login.bank-regional.example` A | **203.0.113.150** | TTL=1 |
| 09:14:02 | `payroll-saas.example` A | legit | — |

**Endpoint telemetry (one user):** browser hit 203.0.113.150, served a
pixel-perfect clone of the bank's login page; user entered credentials;
clone then showed "temporarily unavailable."

**Router config check (ISP-supplied):** DNS forwarder = ISP resolvers;
remote admin enabled; firmware from 2019; **no DNS-over-HTTPS/TLS available**.

## Student Task

1. Determine **where** the spoofing occurs (endpoint malware / client-router /
   ISP resolver path / authoritative compromise) using the evidence pattern —
   name the discriminating observation(s).
2. Explain why the payroll SaaS users were *spared* while bank users were hit,
   using the HSTS fact — and what this tells the ISP investigation.
3. Draft the MSP's action list: immediate user-side guidance, client-router
   mitigations, and the escalation path with the ISP (what evidence you hand them).

## How to Approach This (Reasoning Scaffold)

- Legit→bad→legit within seconds *at the resolver* with TTL=1 means the
  attacker is answering *between* the resolver and you, repeatedly — think
  about which devices sit there.
- HSTS on the payroll SaaS makes a clone useless even with a spoofed answer —
  predict which domains attackers avoid and why.
- "ISP denies" is not evidence; the discriminating data you hand them is.

## CLO Mapping

- **CLO-2** — DNS on-path attack analysis and multi-party response.

## Safety Notes

- Simulated MSP/ISP scenario. Real-world DNS testing only on authorized
  segments; phishing-kit analysis is defensive work.
