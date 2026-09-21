# cs-075 — Scan-Result Prioritization Under Patch Windows

> **Simulated scenario.** The findings, exposure data, and windows are fictional.

## Difficulty & Domain

- **Difficulty:** Advanced · **Domain:** Vulnerability prioritization · **CLO:** CLO-10
- **Est. time:** 15 minutes · **Anchor:** L24 (Vulnerability Management Cycle)

## Scenario

A quarterly scan produced 3,100 findings. You have **one patch window
this month** (4 hours, 60 hosts max). You must select the patch set:
not "highest CVSS first" — a context-weighted ranking using exposure,
exploitability intel, and compensating controls, with the arithmetic
shown. Two findings will test your discipline: a CVSS-10.0 on an
unreachable host, and a CVSS-7.5 that's internet-facing with active
exploitation.

## Stakeholders

- **IT ops** — 60-host budget; every patch is change risk.
- **Security** — must defend the cut list with numbers.
- **Service owners** — their apps break if patches regress.
- **CISO** — "explain why the 10.0 isn't top" is the anticipated question.

## Network Context

- Exposure tiers: internet-facing (12 hosts), user-facing (180),
  internal-only (600), isolated (400+).
- Compensating controls map: virtual patching (IPS rules) available on
  the edge; segmentation verified for isolated tiers.
- Exploitation intel: 3 of the findings have known in-the-wild exploits
  (CISA-style catalog); the rest are "affected" only.

## Available Evidence

**Top findings (sample of the 3,100):**

| ID | CVE-class | CVSS | Host | Exposure | Wild exploit? | Compensating control | Patch effort |
|---|---|---|---|---|---|---|---|
| F1 | RCE in edge middleware | 10.0 | `iso-backup-01` (isolated, no user traffic, ACL'd to backup net only) | isolated | no | segmentation verified; no inbound path | 1 h |
| F2 | Auth-bypass in public API gateway | 7.5 | `api-gw-01` (internet) | **internet** | **yes — active campaign** | none (IPS signature immature) | 2 h (vendor hotfix) |
| F3 | Priv-esc in endpoint agent | 8.8 | all 180 user laptops | user-facing | no | EDR blocks the exploit primitive (tested) | 3 h fleet rollout |
| F4 | Info-disclosure in reporting tool | 5.3 | `rep-02` (user-facing) | user-facing | no | none | 30 min |
| F5 | RCE in internal build server | 9.8 | `build-03` (internal, but devs push code daily) | internal | no | none; holds code-signing keys | 2 h |

Plus: 3,095 more findings, mostly F4-class on internal hosts.

## Student Task

1. Build the **prioritization formula**: risk = (CVSS-anchored severity)
   × (exposure multiplier) × (exploitation multiplier) − (compensating-
   control discount) — define the multipliers with numbers and apply to
   F1–F5; rank them.
2. Make the **60-host window cut**: F2+F5 are 2 hosts — what fills the
   other 58? (Apply the formula to the F4-class population; show the
   per-host math and the threshold that governs inclusion.)
3. Write the **CISO answer for F1**: why the 10.0 waits (the
   compensating-control discount made *evidence-based*, not vibes) —
   and the one event that would instantly promote it.

## How to Approach This (Reasoning Scaffold)

- CVSS is *severity*, not risk: risk needs exposure (who can reach it)
  and exploitation (who *is* reaching it) — the multipliers encode the
  context the base score lacks.
- The discount must be *evidence-based*: "segmentation verified" means
  a tested ACL, not a diagram (the cs-026 lesson — observe-then-enforce).
- The window budget forces the threshold to be explicit: "patch
  everything scored above X" — X is where the math meets the 60-host
  reality.

## CLO Mapping

- **CLO-10** — Context-weighted vulnerability prioritization.

## Safety Notes

- Simulated findings; no exploit detail beyond catalog framing.
