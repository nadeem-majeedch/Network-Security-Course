---
case: cs-061
title: VPC Design Review for a Three-Tier App
difficulty: advanced
domain: Cloud network security
module: 5
lecture-anchor: L19
clos: [CLO-13]
time-estimate: 15 min (5 min reasoning + 10 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-061-solution.md
---

# cs-061 — VPC Design Review for a Three-Tier App

> **Simulated scenario.** The cloud design, subnets, and findings are fictional.
> Generic cloud constructs (VPC/security groups/route tables/NACLs) are
> described provider-neutrally; map to your provider of study.

## Difficulty & Domain

- **Difficulty:** Advanced · **Domain:** Cloud network security · **CLO:** CLO-13
- **Est. time:** 15 minutes · **Anchor:** L19 (Cloud Networking I — VPC Design & Controls)

## Scenario

A SaaS company's three-tier app (ALB → web/app → DB) runs in one VPC with
the design below. A pen test found a path "from the internet to the
database" — the cloud team disputes it. You review: find the actual path,
rank findings, and produce the redesign with the *cloud-native* control
choices (security groups vs NACLs, route-table design, egress).

## Stakeholders

- **Cloud team** — built it; wants the finding disproven or scoped.
- **Security** — wants the design to enforce tiering structurally.
- **Compliance** — DB holds customer PII; scope question (is the DB
  internet-adjacent?).
- **SRE** — operations must survive the redesign (patching, monitoring).

## Network Context (proposed design)

```
VPC 10.0.0.0/16
├── public subnets 10.0.1.0/24, 10.0.2.0/24 (ALB; auto-assign public IP ON for 10.0.2)
├── app subnets   10.0.11.0/24, 10.0.12.0/24 (web/app EC2, public IP OFF)
├── db subnets    10.0.21.0/24, 10.0.22.0/24 (managed DB, "private")
Route tables:
  public RT: 0.0.0.0/0 → IGW
  app RT:    0.0.0.0/0 → IGW          ← ("so instances can patch")
  db RT:     local only
Security groups:
  sg-alb: ingress 443 from 0.0.0.0/0
  sg-app: ingress 8080 from sg-alb; egress 0.0.0.0/0 all
  sg-db:  ingress 5432 from 10.0.0.0/16   ← (whole-VPC source)
NACLs: default (allow all) everywhere
```

**Pen-test claim:** "internet → DB reachable." **Cloud team:** "DB has no
public IP and no IGW route; impossible."

## Student Task

1. **Arbitrate the finding**: is internet→DB reachable as designed? Walk
   the packet path precisely; if not directly, identify the *near-miss*
   structural issues that make the claim half-true (auto-assign ON,
   whole-VPC sg source, IGW-routed app subnets).
2. Rank the **five findings** with mechanism + fix (distinguish
   SG-scope fixes, route-table fixes, NACL uses where appropriate).
3. Produce the **redesign table**: per-tier subnets (public/private/
   isolated), route tables, SG chaining (source = SG, not CIDR), egress
   design (NAT/egress proxy), and where NACLs add real value vs noise.

## How to Approach This (Reasoning Scaffold)

- "No public IP" blocks *inbound initiation*; it does not address the
  *blast radius* if any app host is compromised — the DB's sg allowing
  the whole VPC is the finding's real substance.
- Walk paths precisely: what does a packet from the internet to DB need
  (public IP? route? SG allow?) — name which legs exist.
- SG chaining (source = sg-alb, sg-app) is the cloud-native tiering
  mechanism; NACLs are for subnet fences (e.g., deny known-bad ranges),
  not the primary tiering tool.

## CLO Mapping

- **CLO-13** — Cloud VPC design review with control-mechanism precision.

## Safety Notes

- Paper review of a fictional design.
