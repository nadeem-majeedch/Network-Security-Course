---
case: cs-019
title: Session-Hijack Indicators in Web Traffic
difficulty: beginner
domain: Network security principles
module: 2
lecture-anchor: L07
clos: [CLO-2]
time-estimate: 12 min (5 min reasoning + 7 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-019-solution.md
---

# cs-019 — Session-Hijack Indicators in Web Traffic

> **Simulated scenario.** The SaaS, users, and logs are fictional.

## Difficulty & Domain

- **Difficulty:** Beginner · **Domain:** Network security principles · **CLO:** CLO-2
- **Est. time:** 12 minutes · **Anchor:** L07 (Sniffing, MITM & Session Attacks)

## Scenario

A project-management SaaS's security team reviews one enterprise customer's
complaint: "someone did things in my account at 3 a.m." The SaaS has full
application logs, TLS-terminated at the edge LB (so session cookies are
visible to the *platform*, not to network observers), and per-request
metadata. You must decide: session hijack, credential stuffing, or confused
user — and say what the platform should change.

## Stakeholders

- **Enterprise customer's admin** — wants a definitive answer for their board.
- **SaaS security** — platform-side remediation.
- **The real user** — whose session/device was involved.
- **SaaS legal** — notification obligations if data was accessed.

## Network Context

- App at `app.pm-saas.example`; TLS at the edge; cookies `Secure; HttpOnly`
  but **no SameSite** attribute set; session lifetime 30 days; no re-auth
  on sensitive actions.
- No MFA; enterprise customer allows "remember this device" for 30 days.
- Login endpoint rate-limited per-IP; token-authenticated API exists.

## Available Evidence

**Account `acme-4417`, 02:40–03:15 window:**

| Time | Event | IP | UA / fingerprint | Notes |
|---|---|---|---|---|
| 02:41 | page view: dashboard | 198.51.100.9 | Chrome/W10, fp=`a91c` | user's usual profile |
| 02:41 | page view: board settings | 198.51.100.9 | fp=`a91c` | — |
| 02:47 | **API call: export board** (token auth) | 203.0.113.88 | `python-requests/2.31` | **new token, created 02:44** |
| 02:48 | API call: list members | 203.0.113.88 | python-requests | same token |
| 02:52 | page view: audit-log page | 198.51.100.9 | fp=`a91c` | real user awake? |
| 03:10 | **password change succeeded** | 203.0.113.88 | python-requests | used *session cookie*, not password |
| 03:12 | board deleted (soft-delete) | 203.0.113.88 | python-requests | same session |
| 03:15 | API token `new` created | 203.0.113.88 | python-requests | persistence |

## Student Task

1. Judge the three hypotheses (session hijack / credential stuffing / confused
   user) against the evidence; pick one and defend it, citing specific rows.
2. Explain **mechanically** how the attacker most likely obtained the session
   (state your #1 vector and what in the config enabled it), and why the
   02:44 token creation + 02:47 use matters.
3. Give the platform's top-4 fixes, ordered, each mapped to the evidence row
   or config line it neutralizes.

## How to Approach This (Reasoning Scaffold)

- Fingerprint continuity vs IP continuity: which one distinguishes hijack
  from travel/VPN? The rows give you both.
- The token's *birth time* (02:44) inside the session's lifetime is a pivot
  clue — who can create tokens, and from where?
- "Confused user" must explain `python-requests` — can it? (The bar for
  rejecting a hypothesis is *impossibility*, not merely oddness.)

## CLO Mapping

- **CLO-2** — Session-attack evidence analysis and platform hardening.

## Safety Notes

- Simulated SaaS logs; session-theft *defenses* are the learning objective.
  No cookie-theft technique instructions are provided.
