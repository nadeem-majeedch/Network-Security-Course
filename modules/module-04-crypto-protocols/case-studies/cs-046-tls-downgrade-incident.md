---
case: cs-046
title: TLS Downgrade Incident Analysis
difficulty: advanced
domain: TLS and certificate problems
module: 4
lecture-anchor: L14
clos: [CLO-6]
time-estimate: 12 min (5 min reasoning + 7 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-046-solution.md
---

# cs-046 — TLS Downgrade Incident Analysis

> **Simulated scenario.** The gateway, configs, and captures are fictional.

## Difficulty & Domain

- **Difficulty:** Advanced · **Domain:** TLS and certificate problems · **CLO:** CLO-6
- **Est. time:** 12 minutes · **Anchor:** L14 (TLS Deep Dive)

## Scenario

A payment processor's quarterly PCI scan flags: "TLS 1.0/1.1 still
negotiable on the partner gateway." The gateway team is confused — they
disabled those protocols a year ago. A capture from the scan window (below)
shows what actually happened. Reconstruct the mechanism, assess real
exposure, and fix it.

## Stakeholders

- **PCI assessor** — the finding blocks attestation.
- **Gateway team** — believes the config is right.
- **Partner banks** — some legacy integrations are the reason TLS 1.0 was
  once allowed.
- **Fraud team** — wants real exposure quantified, not checkbox panic.

## Network Context

- Partner gateway terminates TLS from bank partners; some legacy partners
  once required old TLS.
- A year ago the team set `protocols = TLS1.2, TLS1.3` on the *primary*
  listener. An **old second listener** (created during a migration, bound to
  a second IP on the same host, still DNS-reachable as a legacy hostname)
  kept its original config.
- Scans hit both hostnames.

## Available Evidence

**Capture summary (scan window):**

| Probe | Hostname:port | ClientHello version | ServerHello result |
|---|---|---|---|
| S1 | gateway.bank.example:443 | TLS 1.0 | **handshake aborted** (no shared protocol) |
| S2 | gateway.bank.example:443 | TLS 1.3 | success (TLS 1.3) |
| S3 | legacy-gw.bank.example:443 | TLS 1.0 | **success (TLS 1.0!)** |
| S4 | legacy-gw.bank.example:443 | TLS 1.3 | success (TLS 1.3) |
| S5 | gateway.bank.example:443 | TLS 1.0 with fallback SCSV | aborted |

**Config dump (second listener):** `protocols = TLSv1.0, TLSv1.1, TLSv1.2` —
unchanged since migration; cert = same wildcard cert (valid).

## Student Task

1. Reconstruct the **mechanism**: why the scan finding exists despite the
   team's config change; what S1 vs S3 proves about *listener-scoped* vs
   *service-scoped* policy.
2. Assess **real exposure**: what could a TLS 1.0-capable endpoint
   actually enable against *this* gateway (consider ciphers available to
   1.0, BEAST-class concerns honestly, and who can reach the legacy
   hostname); distinguish the "finding" from the "danger."
3. Give the **fix + governance pair**: the technical change, plus the
   config-management control that prevents listener sprawl from
   re-creating this (and the partner-migration lesson).

## How to Approach This (Reasoning Scaffold)

- TLS policy applied to *a listener*, not to *the service* — config
  drift lives at the boundary you forgot exists.
- Exposure analysis is quantitative-ish: TLS 1.0's remaining protocol
  weaknesses vs modern cipher suites the listener still allows — what
  attack actually applies in 2026?
- The governance fix matters more than the one-line config change:
  *discovery* of listeners, not memory of them.

## CLO Mapping

- **CLO-6** — TLS configuration mechanics and exposure assessment.

## Safety Notes

- Simulated environment; scanner findings interpretation is defensive.
