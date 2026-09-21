# cs-062 — Security Group vs NACL Control Choice

> **Simulated scenario.** The estate, five control problems, and constraints
> are fictional. Constructs described provider-neutrally.

## Difficulty & Domain

- **Difficulty:** Advanced · **Domain:** Cloud network security · **CLO:** CLO-13
- **Est. time:** 15 minutes · **Anchor:** L19 (Cloud Networking I — VPC Design & Controls)

## Scenario

A platform team must implement **five distinct control problems** in one
VPC. For each, choose the right mechanism — stateful security groups,
stateless network ACLs, or a different cloud construct entirely — and
defend it with the *stateful/stateless* semantics that make the choice
correct, not vibes.

## Stakeholders

- **Platform team** — wants maintainable controls, not clever ones.
- **Security** — wants the defense-in-depth story.
- **App teams** — will file tickets for every control that breaks them.

## Network Context

- One VPC: prod + nonprod subnets; shared-services subnet; a data subnet.
- Mechanisms available: stateful SGs (instance-attached), stateless NACLs
  (subnet-attached, rule-numbered, deny-capable), managed DNS firewall,
  private endpoints, WAF at edge.

**The five control problems:**

1. App tier may reach DB tier on 5432; nothing else may — including
   *future* app instances auto-added by autoscaling.
2. Block a known-malicious external IP range from reaching *anything* in
   the VPC (threat-feed driven, changes weekly).
3. Nonprod subnets must never initiate to prod subnets (env fence),
   enforced even if an app team edits an SG.
4. Web tier must only receive traffic through the edge load balancer —
   direct-to-instance access must fail.
5. Outbound DNS from workloads must go to approved resolvers only
   (anti-exfil/anti-DoH-escape).

## Student Task

1. For each problem: **chosen mechanism + one-paragraph defense** citing
   stateful/stateless semantics, evaluation order, deny capability, and
   who owns the rule (app team vs platform).
2. Problem 2 deserves care: why is a NACL the right (or wrong) tool for a
   weekly-changing blocklist — and what's the better construct if not?
3. Problem 4: name *two* mechanisms that achieve it and the failure mode
   of the naive one (SG-source-only) — what still gets through?

## How to Approach This (Reasoning Scaffold)

- Stateful = connection-aware, no ephemeral-return bookkeeping, no deny
  rules (in most providers) — SGs are *allow*-models.
- Stateless = every direction specified explicitly, *denies exist*,
  rule-order matters — NACLs are fence/policing tools.
- "Who owns the rule" decides maintainability: app-owned (SG) vs
  platform-owned (NACL/DNS-firewall) — mismatched ownership is how
  controls rot.

## CLO Mapping

- **CLO-13** — Cloud control-mechanism selection with semantic precision.

## Safety Notes

- Design exercise; provider-generic constructs.
