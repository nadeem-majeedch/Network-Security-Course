---
case: cs-042
title: Internal PKI Chain Design for Lab Services
difficulty: intermediate
domain: VPN and secure remote access
module: 4
lecture-anchor: L13
clos: [CLO-5]
time-estimate: 12 min (5 min reasoning + 7 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-042-solution.md
---

# cs-042 — Internal PKI Chain Design for Lab Services

> **Simulated scenario.** The lab estate, services, and requirements are fictional.

## Difficulty & Domain

- **Difficulty:** Intermediate · **Domain:** VPN and secure remote access · **CLO:** CLO-5
- **Est. time:** 12 minutes · **Anchor:** L13 (Cryptographic Foundations)

## Scenario

A university research lab runs 25 internal services (GitLab, artifact
registry, monitoring, notebooks) on self-signed certificates — browser
warnings everywhere, and students have learned to click through warnings
(a trained vulnerability). You design the **internal PKI**: chain structure,
issuance policy, trust distribution, revocation, and the mTLS tier for
service-to-service traffic.

## Stakeholders

- **Researchers/students** — warnings must vanish; tooling must not break.
- **Lab IT (1 person)** — must run this sustainably.
- **Security** — the click-through culture is the finding.
- **Compliance** — the artifact registry signs releases; key custody matters.

## Network Context

- Services on `*.lab.university.example`; clients: lab-managed machines +
  student BYOD.
- Requirement tiers: (1) browser-trusted TLS for all services; (2) mTLS for
  the registry↔build cluster; (3) code-signing (separate problem, out of
  scope — but the chain must not conflate it).
- No network segmentation change planned; PKI is the scope.

## Student Task

1. Design the **chain**: root (offline?) → issuing intermediates (how many,
   what separation logic) → leaf profiles (server/mTLS client). Justify the
   intermediate split and lifetimes at each tier (numbers).
2. Define **issuance & trust policy**: who requests, how validated
   (domain-control for lab hosts), how trust reaches BYOD (this is the
   graded constraint — 3 distribution mechanisms with tradeoffs).
3. Design **revocation + incident posture**: what happens when the issuing
   intermediate's key leaks; why CRL vs OCSP for this estate; the
   click-through-culture note that ties it together.

## How to Approach This (Reasoning Scaffold)

- Offline root + online intermediates is the shape that makes "root key
  leak" a non-event; say what "offline" operationally means (1 person!).
- Trust distribution to BYOD is the hard part: certificate + MDM/config
  profile vs per-browser stores vs "only lab-managed gets trusted" honesty.
- Lifetimes: short leaves, mid intermediates, long root — and name what
  each lifetime buys.

## CLO Mapping

- **CLO-5** — PKI chain architecture and trust distribution.

## Safety Notes

- Design exercise; production PKI belongs to vetted tooling (step-ca,
  EJBCA, vendor CAs), not hand-rolled openssl ceremonies — say so.
