---
case: cs-048
title: mTLS Deployment for Service-to-Service Traffic
difficulty: advanced
domain: TLS and certificate problems
module: 4
lecture-anchor: L14
clos: [CLO-6]
time-estimate: 12 min (5 min reasoning + 7 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-048-solution.md
---

# cs-048 — mTLS Deployment for Service-to-Service Traffic

> **Simulated scenario.** The fintech, mesh, and rollout constraints are fictional.

## Difficulty & Domain

- **Difficulty:** Advanced · **Domain:** TLS and certificate problems · **CLO:** CLO-6
- **Est. time:** 12 minutes · **Anchor:** L14 (TLS Deep Dive)

## Scenario

A fintech with 120 microservices (some on VMs, most on Kubernetes) wants
mTLS everywhere service-to-service. Current state: TLS-terminated at the
ingress only; internal traffic plaintext ("inside the perimeter"). The
platform team must deliver a **rollout design**: mesh choice, certificate
model, and the per-service migration mechanics — with the *plaintext
period* honestly bounded.

## Stakeholders

- **CISO** — "plaintext internal" is the audit finding.
- **Platform team** — owns the mesh; fears outages during rollout.
- **Service teams** — 40 teams; some services are vendor-shipped binaries
  that can't be modified.
- **Compliance** — payment-path services have stricter requirements.

## Network Context

- K8s services: 100; VM services: 20 (some vendor binaries).
- Current internal flows: plaintext HTTP, some Redis/DB TLS already.
- Candidate: service mesh (sidecar) with mTLS; per-namespace rollout
  supported; VMs need mesh-VM integration or a different pattern.
- Secrets/CA: internal PKI exists (cs-042-style, two intermediates).

## Student Task

1. Design the **certificate model**: who gets certs (workload identity!),
   lifetimes, rotation mechanics, and how *vendor binaries on VMs* get
   identities without code changes (the graded constraint).
2. Plan the **rollout**: namespace ordering (which first/last and why),
   permissive-to-strict mTLS mechanics (what "permissive" means and its
   honest risk), and the plaintext-period bound (what percentage of flows
   is plaintext at day 30/90/180).
3. Name the **three failure modes** mTLS introduces (cert expiry storms,
   sidecar upgrade outages, clock skew) and the design response to each.

## How to Approach This (Reasoning Scaffold)

- mTLS is identity infrastructure, not just encryption — the SPIFFE-style
  workload-identity model is the answer to "who am I talking to."
- Permissive mode is a *transition tool* with a real risk (downgrade to
  plaintext by misconfig) — bound it in time, not in hope.
- Vendor binaries can't hold certs — the *sidecar/host-proxy* holds
  identity for them; that's the whole design trick.

## CLO Mapping

- **CLO-6** — mTLS identity architecture and migration engineering.

## Safety Notes

- Design exercise; mesh selection guidance is generic, not vendor-pitched.
