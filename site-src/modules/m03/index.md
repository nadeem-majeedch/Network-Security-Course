---
status: complete
artifact-type: module-overview-page
module: 3
instructor-only: false
---

# Module 3 — Secure Architecture & Perimeter Controls

**Lectures:** L09–L12 (Weeks 5–6) · **CLOs:** CLO-3, CLO-4 · **Cases:** cs-021–040

*Descriptive orientation. Designs below are teaching reference models, not
production configurations.*

## What this module covers

Design is where defense begins. You move from spotting attacks to shaping
networks that remove entire attack classes: segmentation that bounds blast
radius, firewalls and ACLs with engineered rulebases, and egress/NAT/proxy
controls that make lateral movement observable.

## Lectures

| # | Lecture | Core idea |
|---|---|---|
| L09 | [Defense in Depth & Network Segmentation](../../lectures/lecture-09-defense-in-depth-segmentation.md) | Zones, trust levels, blast radius, reference architectures |
| L10 | [Firewalls: Concepts & Placement](../../lectures/lecture-10-firewalls-concepts-placement.md) | Packet filter vs stateful vs NGFW, DMZ placement patterns |
| L11 | [ACLs & Rulebase Engineering](../../lectures/lecture-11-acls-rulebase-engineering.md) | Rule ordering, implicit deny, audit & shadowed-rule analysis |
| L12 | [NAT, Proxies, Egress & NAC](../../lectures/lecture-12-nat-proxies-egress-nac.md) | Egress filtering, explicit proxies, NAC admission logic |

## Labs

[Lab-05](../../labs/lab-05-segmentation-proxy-egress-design.md) (segmentation &
proxy egress design) and [Lab-06](../../labs/lab-06-firewall-rulebase-acl-audit.md)
(pfSense rulebase build & ACL audit) — both design-first, with audit evidence
from the isolated lab firewall.

## Case studies (intermediate tier begins)

This module carries cs-021–040: segmentation proposals, DMZ design review,
rulebase hygiene, egress strategy, NAC rollout judgment, and the zone-math
cases where you compute reachability from an ACL rather than guess it.
See the [case studies guide](../../cases/index.md).

## Skills checkpoints

- Propose a zone model for a stated business scenario and justify trust boundaries.
- Read an ACL top-down and predict the verdict for a given 5-tuple.
- Identify shadowed, redundant, and over-permissive rules in a real rulebase.
- Explain what NAT does and does not provide as a security control.
