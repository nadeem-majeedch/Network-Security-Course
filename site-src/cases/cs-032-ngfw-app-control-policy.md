# cs-032 — NGFW Application-Control Policy Design

> **Simulated scenario.** The firm, app mix, and observations are fictional.

## Difficulty & Domain

- **Difficulty:** Intermediate · **Domain:** Firewall and ACL design · **CLO:** CLO-4
- **Est. time:** 12 minutes · **Anchor:** L10 (Firewalls — Concepts & Placement)

## Scenario

A 500-person professional-services firm installs an NGFW with
application-control at the internet edge. Leadership wants "shadow IT under
control" without a productivity police force. You have two weeks of
observation data (below). Design the application policy: what's allowed,
blocked, or warned — and say precisely how you'll handle **encrypted-app
identification limits** without lying about capability.

## Stakeholders

- **Leadership** — wants risk down, not a surveillance program.
- **Employees** — will route around bad policy (VPN apps, personal hotspots).
- **App vendors** — SaaS apps use CDNs/shared infrastructure; identification
  is fuzzy at edges.
- **Security team** — owns exceptions and their review cycle.

## Network Context

- NGFW at the single internet edge; full TLS inspection is *technically
  possible* but currently off (legal/privacy review pending).
- App-ID engine: identifies apps via TLS SNI, cert data, behavioral
  signatures; confidence levels (high/med/low).
- No per-user identity integration yet (IP-based policies only).

## Available Evidence

**Two-week observation (top egress apps by bytes; identification confidence):**

| App category | Examples seen | Bytes share | Confidence | Note |
|---|---|---|---|---|
| Approved SaaS (CRM, email) | vendor-owned | 38% | High | business-critical |
| Video conferencing | 2 approved vendors + 1 unknown app | 22% | High | unknown app used by 4% of staff |
| Software updates | OS/browser/IDE vendors | 14% | High | includes one unsigned-update source |
| Cloud storage | approved suite + 3 personal-use apps | 9% | High | personal apps exfil-adjacent |
| Developer tools / package registries | npm/pypi/maven mirrors | 6% | Med | mixed dev population |
| "Unknown HTTPS" (SNI-only) | long tail, 800+ distinct SNIs | 8% | Low | includes 6 SNIs matching risk feeds |
| VPN/proxy apps | 3 apps, 11 users | 2% | High | policy-evading behavior |

## Student Task

1. Build the **policy table**: category → action (allow / allow-degrade /
   warn+log / block) → rationale → *identity of enforcement given TLS
   inspection is off* (what can/can't you actually enforce?).
2. Address the **"unknown HTTPS" 8%** honestly: with SNI-only visibility,
   name what you can enforce, what you can't, and the two compensating
   options (enable selective inspection vs resolve-by-other-means).
3. Design the **VPN/proxy response** so employees don't hotspot their way
   out of policy — what makes the sanctioned path *better* than the evasive one?

## How to Approach This (Reasoning Scaffold)

- Action follows *risk × business need*, not byte share — updates are 14%
  and boring; personal cloud storage is 9% and interesting.
- "SNI-only" means app identity is often just *hostname* identity — say so.
- Enforcement without inspection is *choice architecture* (make the allowed
  path the easy path), plus reputation-based blocks.

## CLO Mapping

- **CLO-4** — Application-aware policy design with honest capability limits.

## Safety Notes

- Policy design exercise; no DPI tooling instructions beyond capability
  description.
