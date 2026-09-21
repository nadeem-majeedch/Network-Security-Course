---
case: cs-007
title: DNS Resolution Misdirection Symptoms
difficulty: beginner
domain: DNS and DHCP security
module: 1
lecture-anchor: L03
clos: [CLO-1]
time-estimate: 10 min (5 min reasoning + 5 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-007-solution.md
---

# cs-007 — DNS Resolution Misdirection Symptoms

> **Simulated scenario.** The registrar, domains, and addresses are fictional.

## Difficulty & Domain

- **Difficulty:** Beginner · **Domain:** DNS and DHCP security · **CLO:** CLO-1
- **Est. time:** 10 minutes · **Anchor:** L03 (Protocol Deep Dive II — TCP/UDP/DNS/DHCP)

## Scenario

Starting 11:05, some customers of a mid-size SaaS company report being taken
to a competitor's parking page when they type the SaaS product's URL. Others
reach the product normally. The SaaS company swears nothing changed on their
side. Your managed-service team gets the ticket and the evidence below.

## Stakeholders

- **SaaS customers** — being sent to an impostor page (some entered credentials).
- **SaaS company** — brand and trust damage; they claim innocence.
- **Your MSSP team** — must localize the fault before accusations fly.
- **The registrar/DNS provider** — potentially the compromise point.

## Network Context

- SaaS domain: `acme-cloud.example` (simulated TLD example for teaching).
- Customers are spread across three residential ISPs and two mobile carriers.
- The SaaS company uses one registrar with DNS hosting on the same platform.
- No DNSSEC is deployed on the zone.

## Available Evidence

1. **Resolver tests from the affected ISPs' resolvers:**
   - ISP-A resolvers: `acme-cloud.example → 198.51.100.23` (correct).
   - ISP-B resolvers: `acme-cloud.example → 203.0.113.190` (impostor host).
   - Mobile carrier resolvers: mixed answers within minutes.
2. **Authoritative NS records:** unchanged for 400 days; SOA serial current.
3. **Zone A record history (registrar API):** the A record was changed at
   10:59 via the registrar's API by an API key named "ci-deploy" (created 4
   months ago, last used 8 days ago).
4. **TTL:** A record TTL 86400 (24 h) — matches "some customers fine, some
   poisoned" during the day.

## Student Task

1. Localize the fault: is this on the SaaS company's side, the customers', or
   in between? Identify the compromise point and the attack type by name.
2. Explain the "some customers fine" observation using TTL mechanics.
3. Order the next three response actions and say what each one contains.

## How to Approach This (Reasoning Scaffold)

- Different resolvers disagreeing ⇒ it's not the application, it's the *answer
  distribution* layer.
- Ask who *can* change the answer at each layer: authoritative server, DNS
  hoster, registrar, zone owner credentials.
- The API-key detail is not trivia — it's the compromise vector.

## CLO Mapping

- **CLO-1** — DNS mechanics applied to attack localization.

## Safety Notes

- Simulated incident; do not test against real domains or registrars.
