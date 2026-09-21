# cs-038 — Explicit-Proxy Egress Policy for a University Lab

> **Simulated scenario.** The university, labs, and requirements are fictional.

## Difficulty & Domain

- **Difficulty:** Intermediate · **Domain:** Firewall and ACL design · **CLO:** CLO-4
- **Est. time:** 12 minutes · **Anchor:** L12 (NAT, Proxies, Egress & NAC)

## Scenario

A university CS department runs 3 teaching labs (90 PCs), a research cluster,
and open Wi-Fi. The egress firewall currently allows all 443. The dean wants
CIPA-style filtering for teaching labs **without** breaking the research
cluster's package managers or the open Wi-Fi's usability. You design the
**explicit-proxy architecture**: which traffic goes where, how non-proxy-
aware clients are handled, and how the design resists bypass.

## Stakeholders

- **Dean** — compliance duty for minors in teaching labs.
- **Researchers** — pip/npm/apt/curl workflows must survive untouched.
- **Students** — open Wi-Fi must not become a wall of prompts.
- **IT security** — the proxy is also the logging point.

## Network Context

- Egress: 10 Gbps; current firewall does NAT only.
- Teaching labs: managed Windows PCs, all traffic must traverse the proxy
  (enforceable — managed fleet).
- Research cluster: Linux, package managers to CDNs, some SSH out to
  collaborator clusters.
- Open Wi-Fi: mixed devices (laptops/phones), many TLS-pinned apps.
- Proxy: explicit mode + transparent option available; PAC files supported.

## Student Task

1. Design the **egress routing table**: zone → egress path (explicit proxy /
   transparent / direct) → filtering profile → logging level. Justify each
   choice in one line (esp. why research cluster ≠ teaching-lab policy).
2. Handle **non-proxy-aware and pinned clients**: which path, and what the
   honest enforcement limit is (name the app classes that will not work
   behind TLS-interception and the exemption mechanism).
3. Give the **anti-bypass design**: the 3 firewall rules that make the proxy
   the only path, and the 2 behaviors you monitor to catch evasion.

## How to Approach This (Reasoning Scaffold)

- One policy size never fits: compliance scope (minors in labs) ≠ research
  freedom ≠ guest usability — the *routing table* is the policy.
- Pinned apps (mobile banking, some SaaS) break under TLS interception —
  exemptions are a feature with an audit trail, not an admission of failure.
- Bypass resistance lives at the *firewall* (route/destination enforcement),
  not at the proxy (which is only as good as its reachability).

## CLO Mapping

- **CLO-4** — Proxy-based egress architecture with honest limits.

## Safety Notes

- Policy design; content filtering is a compliance duty for minors —
  discuss over-blocking tradeoffs too.
