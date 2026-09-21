# cs-011 — Attack Tree for a Two-Tier Web Application

> **Simulated scenario.** The application and architecture are fictional.

## Difficulty & Domain

- **Difficulty:** Beginner · **Domain:** Network security principles · **CLO:** CLO-2
- **Est. time:** 10 minutes · **Anchor:** L05 (Threat Modeling & Attacker Anatomy)

## Scenario

A startup runs a customer portal: an internet-facing nginx reverse proxy in a
DMZ subnet, which talks to an application server in an internal subnet, which
holds credentials to a managed Postgres database. The goal an attacker wants:
**read the customer database.** The CTO asks you to sketch *how* an attacker
gets there before spending money on tools.

## Stakeholders

- **CTO** — wants prioritized spend, not a firewall brochure.
- **Customers** — their data is the target.
- **Dev team** — owns the app server; will receive the hardening list.

## Network Context

- DMZ: proxy only (443 open inbound from internet).
- App subnet: 8080 open from DMZ to app server only.
- DB: managed service, reachable from app subnet on 5432, credential auth only.
- No WAF, no MFA on the admin panel (served by the app server, reachable via proxy path `/admin`).

## Available Evidence

- Architecture diagram as above (3 tiers).
- Admin panel login is username+password only; 4 staff accounts.
- Proxy and app server are patched monthly; DB patching is vendor-managed.
- Backups of the DB are restorable by the app server's service account.

## Student Task

1. Draw an **attack tree** with the goal "read customer database": ≥2 top-level
   branches (e.g., compromise proxy / compromise app / abuse admin panel /
   attack DB directly) and ≥2 leaf steps per branch.
2. Mark each **AND/OR** node correctly (which branches require *all* children?).
3. Circle the path you consider **most likely for an opportunistic attacker**
   and justify in one sentence using likelihood, not impact.

## How to Approach This (Reasoning Scaffold)

- Work backwards from the goal; each node is a *sub-goal*, not a tool name.
- OR = any child suffices; AND = all children needed — most branches are OR.
- "Most likely" ≠ "most damaging": opportunistic attackers take cheap paths.

## CLO Mapping

- **CLO-2** — Threat modeling with attack trees.

## Safety Notes

- Paper exercise; attack trees model *defensive* priorities. Do not use real
  target systems for path validation.
