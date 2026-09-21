# cs-030 — Firewall Placement Review for a Branch Office

> **Simulated scenario.** The retail chain, links, and options are fictional.

## Difficulty & Domain

- **Difficulty:** Intermediate · **Domain:** Firewall and ACL design · **CLO:** CLO-3, CLO-4
- **Est. time:** 12 minutes · **Anchor:** L10 (Firewalls — Concepts & Placement)

## Scenario

A 40-store retail chain runs branch offices/store networks with a hub
datacenter. The current design: every branch has an ISP router doing NAT
with **no firewall**; branches reach the DC over site-to-site IPsec. A
refresh is budgeted. You must choose the firewall *placement* per branch:
edge firewall at each branch, central firewalling at the DC only, or
SASE/cloud-delivered. Constraints below.

## Stakeholders

- **Retail IT (3 people)** — cannot operate 40 custom firewall configs.
- **Compliance** — cardholder data exists in stores (POS on the LAN).
- **Finance** — per-site capex vs opex.
- **Store staff** — "if the network is down we take cash only."

## Network Context

- Branch LANs: POS terminals, back-office PC, guest Wi-Fi (separate today by
  AP only), cameras.
- DC: hosts POS backends, inventory app, guest internet breakouts at branch
  (local internet for guest Wi-Fi).
- Links: dual-carrier broadband per store, IPsec to DC.
- Compliance driver: PCI scope needs *segmentation* between POS and guest/
  cameras, with evidence.

## Student Task

1. Compare the **three placements** (per-branch edge FW / DC-only / cloud-
   delivered SASE) against: PCI segmentation enforceability, local-internet
   guest traffic, branch autonomy during WAN outage, ops burden for 3 staff.
   One table, verdict column each.
2. Pick the placement (or hybrid) and justify in 3 sentences referencing the
   table.
3. Specify the **minimum per-branch policy set** (5 rules max) that satisfies
   compliance regardless of which placement you chose — placement-proof rules.

## How to Approach This (Reasoning Scaffold)

- The question is not "which firewall is best" but "where must enforcement
  *live* for the flows that matter" — POS↔guest is *local* traffic; can a
  DC firewall even see it?
- Outage behavior is a design requirement, not a nice-to-have: cash-only
  failure mode.
- Three humans, forty sites: anything needing per-site artistry fails
  automatically — standardization is a feature.

## CLO Mapping

- **CLO-3** — Enforcement placement in a multi-site design.
- **CLO-4** — Policy sets that survive placement choices.

## Safety Notes

- Design exercise; no scanning or testing of retail infrastructure.
