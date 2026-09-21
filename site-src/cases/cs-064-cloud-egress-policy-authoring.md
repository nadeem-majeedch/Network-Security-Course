# cs-064 — Cloud Egress Policy Authoring

> **Simulated scenario.** The platform, workload classes, and needs are fictional.

## Difficulty & Domain

- **Difficulty:** Advanced · **Domain:** Cloud network security · **CLO:** CLO-13
- **Est. time:** 15 minutes · **Anchor:** L20 (Cloud & Hybrid Assurance)

## Scenario

A fintech's cloud platform hosts 60 workloads with **default-allow egress**
("it's the cloud, we have SGs"). After cs-063-class near-misses elsewhere,
security mandates an egress policy. You author it: per-workload-class
egress profiles, the exception process, and the *authoring artifact*
(the policy-as-code shape) — with the FQDN-vs-IP problem and
allow-list-maintenance reality addressed honestly.

## Stakeholders

- **Security** — exfil/C2 paths die by default.
- **60 workload teams** — every allow-list miss is a production incident.
- **SRE** — owns the enforcement point (egress proxy/endpoints).
- **Compliance** — the policy document is an audit artifact.

## Network Context

- Workload classes: (1) stateless APIs (30), (2) batch/data (12),
  (3) third-party-integration (10), (4) legacy/monolith (5), (5) build/CI
  (3).
- Enforcement points: per-class NAT + egress proxy (FQDN-allowing),
  private endpoints for PaaS, SG egress as the coarse fence.
- Observations: 60 workloads × distinct destinations; 12 workloads
  already broken by an over-eager earlier attempt ("the allow-list
  incident").

## Student Task

1. Author the **egress profiles per class** (table): default posture,
   allowed destination *categories*, enforcement point, and the
   class-specific trap (e.g., CI's package-registry chaos).
2. Design the **exception process**: request → risk → TTL → expiry →
   metrics; and the "allow-list incident" postmortem lesson — what
   made the earlier attempt fail and how your process prevents it
   (onboarding path, not exception path).
3. Address the **FQDN-vs-IP problem** honestly: CDNs/shared IPs, pinned
   partners, and what "allow-list by FQDN at a proxy" actually enforces
   (SNI) vs what teams think it enforces.

## How to Approach This (Reasoning Scaffold)

- The earlier attempt failed socially (no onboarding path → outages →
  rollback), not technically — the process *is* the design.
- Class-based profiles beat per-workload rules: 5 profiles, not 60 —
  maintainability is the security property.
- FQDN-at-proxy = SNI-level control: say what that means for shared
  CDNs (it's hostname policy, not payload policy).

## CLO Mapping

- **CLO-13** — Egress policy engineering with realistic enforcement.

## Safety Notes

- Policy design; no evasion guidance.
