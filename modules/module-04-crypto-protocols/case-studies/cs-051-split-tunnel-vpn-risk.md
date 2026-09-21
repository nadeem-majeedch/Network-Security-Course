---
case: cs-051
title: Split-Tunnel VPN Risk Assessment
difficulty: advanced
domain: VPN and secure remote access
module: 4
lecture-anchor: L16
clos: [CLO-5, CLO-7]
time-estimate: 12 min (5 min reasoning + 7 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-051-solution.md
---

# cs-051 — Split-Tunnel VPN Risk Assessment

> **Simulated scenario.** The law firm, VPN policy, and threat model are fictional.

## Difficulty & Domain

- **Difficulty:** Advanced-Advanced · **Domain:** VPN and secure remote access · **CLO:** CLO-5, CLO-7
- **Est. time:** 12 minutes · **Anchor:** L16 (Modern VPNs & Crypto-Agility)

## Scenario

A law firm's remote workforce (300 lawyers) uses full-tunnel VPN. Partners
complain about video-call quality ("my home internet dies on the VPN") and
IT proposes split-tunneling to reduce load. The security lead must assess
the split-tunnel risk *honestly* — including the 2020s reality that
full-tunnel's protection was already porous (browser bypass, DNS reality,
always-on隧道). Produce: the real risk delta, the honest comparison, and a
decision with controls.

## Stakeholders

- **Partners** — want video calls that work; billable-hour reality.
- **Security lead** — must not rubber-stamp convenience.
- **Clients** — confidentiality of legal work product.
- **IT ops** — VPN concentrator capacity is real (300 full tunnels).

## Network Context

- Full-tunnel: all client traffic through VPN; internet breakouts at HQ.
- Split-tunnel proposal: corporate subnets via VPN; internet direct from
  home ISP.
- Clients: managed laptops, EDR present; home networks unmanaged (family
  devices, smart TVs).
- Threat history: one incident last year — lawyer's laptop on home Wi-Fi
  with compromised router (DNS hijack), caught because full-tunnel's DNS
  went through HQ.

## Student Task

1. Compute the **honest risk delta** of split-tunnel for this firm: list
   what protection full-tunnel *actually* provided (and what it didn't —
   browser-side SaaS, TLS everywhere) vs what split-tunnel changes
   (local-network exposure, DNS split, lateral pivot from compromised
   home devices). Format: protect-still / protection-lost / protection-myth.
2. Assess the **DNS split** question specifically — the incident above
   came through DNS: which split-tunnel design keeps *name resolution*
   protected even with direct internet?
3. Decide: **recommend split-tunnel with which controls** (or refuse)? The
   answer must be defensible to partners *and* security, in 5 bullets.

## How to Approach This (Reasoning Scaffold)

- 2026 reality: most sensitive flows are TLS to SaaS — full-tunnel sees
  them but can't read them; what it *does* protect is DNS + unencrypted
  legacy + egress policy consistency.
- The router-compromise incident is the discriminator: DNS control is the
  real home-network risk; craft the design around it.
- "Split-tunnel = bad" is 2010 folklore; the honest delta is smaller and
  specific — name each item.

## CLO Mapping

- **CLO-5** — Cryptographic/protocol realism in VPN design.
- **CLO-7** — Remote-access architecture decision-making.

## Safety Notes

- Design exercise; no evasion guidance beyond standard risk framing.
