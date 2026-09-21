---
lecture: L19
title: Cloud Networking I — VPC Design & Controls
module: 5
week: 9
hours: 2
clos: [CLO-13]
difficulty: intermediate-advanced
status: complete
artifact-type: teaching-plan
---

# L19 — Cloud Networking I — VPC Design & Controls

## 1. Overview & Prerequisites

- **Prerequisites:** L09 (zone/segmentation method), L11 (rule-audit thinking — SG/NACL rules are rulebases). Same week as L17 by design: zones you built on-prem now map to cloud constructs.
- **Position:** cloud networking half of Module 5. CLO-13 runs through L19–L20 and Quiz 5 (W14)/Assignment 7 (W14); capstone designs a cloud landing zone on these skills.
- **Faculty prep:** verify cloud sandbox accounts (free-tier or range-simulated) with billing alarms *hard-capped*; pre-load the reference VPC (3-tier app) as the review target; prepare IaC starter (Terraform/CloudFormation snippet pack).
- **Common misconceptions:** "cloud provider handles security" (shared-responsibility inversion); "security groups are firewalls in the IDS sense"; "private subnet = secure subnet"; "default VPC is fine for production."

## 2. Learning Objectives

By the end of this lecture, students can:

1. Map cloud constructs to on-prem concepts: VPC/VNet ↔ site, subnet ↔ VLAN+zone, route table ↔ forwarding, IGW/NAT-GW ↔ edge devices (Analyze).
2. Distinguish security groups (stateful, instance-attached, allow-only) from network ACLs (stateless, subnet-attached, allow+deny, ordered) and select per use case (Analyze/Evaluate).
3. Design a 3-tier VPC (edge/presentation/app/data) with correct subnets (private/public), route tables, and least-privilege SG pairs (Create).
4. Explain egress models: NAT gateway vs instance egress vs private endpoints (S3/DynamoDB-class), and the logging each produces (Evaluate).
5. Enable and interpret flow logs + VPC traffic mirroring basics for the detection pipeline (L21 bridge) (Apply).

## 3. Detailed Concepts

### 3.1 The cloud translation table
| On-prem | Cloud analog | Security delta |
|---|---|---|
| Site/campus | VPC / VNet | Soft isolation boundary + global APIs = new attack surface |
| VLAN/zone | Subnet (+SG) | Segmentation policy is now API-defined (IaC!) |
| Router | Route table per subnet | Explicit routes; no implicit transitivity |
| Edge firewall | IGW + SGs/NACLs (+ WAF at LB) | No L3 "box" by default — policy is distributed |
| ACLs | SG (stateful allow) / NACL (stateless ordered) | Two different rule models coexist |
- Shared-responsibility line for *networking*: provider = physical/fabric/hypervisor isolation; customer = segmentation, routing, SG policy, encryption in transit.

### 3.2 Security groups vs NACLs (the decision skill)
- SG: stateful (return auto), instance/ENI-scoped, allow-only, all-rules evaluated. Best: workload-level least privilege (`app-tier SG` may `5432/tcp` from `web-tier SG` only — reference-by-SG, not by CIDR!).
- NACL: stateless (needs ephemeral-port return rules), subnet-scoped, numbered ordered rules, deny-capable. Best: subnet-level coarse fencing (block bad reputation ranges, enforce deny patterns like explicit guest-blocks).
- The classic bug: stateless NACL return rules forget ephemeral range (1024–65535 or the OS's actual range) → "works with ping, breaks with app traffic."
- IaC discipline: SG rules reviewed as code (L11 audit skill transfers directly); no `0.0.0.0/0 on 22/3389` — SSM/ Bastion patterns instead.

### 3.3 Reference 3-tier design (build in class)
- Subnets: public-ALB (2 AZs), private-app, private-data; separate route tables; NAT-GW in public app egress only (not on data tier).
- SG pairs: ALB-SG (443 from anywhere), app-SG (from ALB-SG only), db-SG (from app-SG on 5432 only) — *reference by SG id*: zero-CIDR rules, automatically scales with autoscaling.
- Bastion/SSM: prefer agent-based session (no inbound 22); if bastion: dedicated SG + MFA + session logging.
- Peering/transit-gateway preview for multi-VPC (L20 hybrid).

### 3.4 Egress control in cloud
- NAT-GW for app tier (with its own cost/availability story); **private endpoints** for S3/object stores so data-tier traffic never rides the internet path (exfil-surface reduction + policy checkpoints).
- Instance-level egress SG rules (default-allow-egress is a trap: scope it — L12 allow-list thinking is the same skill).
- DNS discipline: VPC resolver, private hosted zones, outbound DNS firewalling (domain allow-lists) — the L12 pattern, cloud edition.

### 3.5 Visibility primitives (bridge to L21)
- Flow logs: VPC/subnet/ENI level; fields (accept/reject, bytes, direction); deliver to S3/Lake → SIEM; reject-only vs all-traffic cost trade-offs.
- Traffic mirroring: packet-level tap for the lab (IDS in cloud — Suricata on a mirror target).
- Cloud-side networking alerts: SG-change alarms, route-table-change alarms (Config/Rules-class) — *who changed the firewall* is a first-class detection.

## 4. Teaching Sequence (120 Minutes)

| Time | Segment | Instructor moves |
|---|---|---|
| 0–10 | Recap: L17 survey findings | One pair's rogue-candidate finding → segue: "zones in the air; now zones as APIs" |
| 10–35 | Core: translation table + shared responsibility | Table walk; responsibility-boundary quiz with 5 service examples |
| 35–55 | Core: SG vs NACL | Stateless-return bug demo (staged); SG-reference-by-id vs CIDR debate |
| 55–65 | Break | — |
| 65–85 | Core: 3-tier reference design | Build it live in console/IaC side-by-side; NAT-GW vs private-endpoint egress story |
| 85–110 | Student activity: segmented VPC build | Pairs build the 3-tier VPC from starter IaC, then harden per checklist (Lab-09 part 2; cs-061..063 prep) |
| 110–120 | Wrap + formative | Exit ticket; L20 trailer: hybrid + assurance; Assignment-7 preview (W14) |

## 5. Technical Examples

```
# Reference design (IaC snippet pattern; provider-neutral pseudocode)
resource "vpc" "prod" { cidr = "10.40.0.0/16" }
resource "subnet" "public-a"  { cidr = "10.40.1.0/24";  az = "a" }   # ALB only
resource "subnet" "private-app-a" { cidr = "10.40.11.0/24"; az = "a" }
resource "subnet" "private-data-a" { cidr = "10.40.21.0/24"; az = "a" }

resource "sg" "alb"  { ingress 443 from 0.0.0.0/0; egress to sg.app  }
resource "sg" "app"  { ingress 8443 from sg.alb;  egress to sg.db 5432; egress 443 via NAT }
resource "sg" "db"   { ingress 5432 from sg.app;  egress none }       # scoped, not default-allow

# Flow-log reading drill (staged file):
#   2 10.40.11.5 10.40.21.9 5432 ACCEPT ...   ← expected app→db
#   2 10.40.11.5 52.94.x.x 443 REJECT ...     ← data-tier tried internet egress!
# Teaching point: REJECT lines are the exfil/hardening goldmine; SG changes alarm.
```
Expected teaching points: SG-reference chains make tiers legible; scoped egress is deliberate; flow logs turn design into evidence.

## 6. Discussion Questions

1. Why is "the provider is certified, so we're secure" wrong for networking specifically? Give the boundary for three services.
2. SG rules that reference *other SGs* instead of CIDRs — what breaks during a migration, and what does it buy you day-to-day?
3. Your data tier needs object storage. NAT-GW vs private endpoint: security, cost, and egress-policy consequences of each?
4. Which NACL use cases justify stateless complexity at all? Argue both sides.
5. Who can change an SG in your org? If the answer is "any developer with console access," what two controls fix it?

## 7. Student Activity

**Segmented VPC build + harden (25 min, pairs):** deploy the starter 3-tier VPC, then apply the hardening checklist: scoped SG egress, data-tier no-internet verification (curl test *fails* — evidence!), flow logs on, one SG-change alarm. Deliverable: architecture sheet + three flow-log lines annotated as evidence.

## 8. Problem-Solving Case

**Primary case — cs-061 "VPC design review for a three-tier app" (intermediate-advanced):**
An inherited VPC: one flat /16, everything in public subnets with public IPs, one giant SG allowing all-internal, RDS reachable from the app *and* the internet through a forgotten port-forward-like rule. Students must (a) enumerate the five worst findings with evidence, (b) produce the target 3-tier design (subnets, route tables, SG pairs referencing by id), (c) write the migration plan that doesn't break the running app (staged SGs, log-only equivalents where possible), and (d) define the post-migration detection set (flow-log rejects, SG-change alarms).
**Linked cases:** cs-062 (SG vs NACL choice), cs-063 (overly permissive route/NAT exposure).
*(Model solutions: instructor answer-key set, Module 5.)*

## 9. Formative Assessment

1. Give one property that makes SGs stateful and one that makes NACLs stateless.
2. Why reference SGs by id instead of CIDR in tier rules?
3. Which construct puts an object-store connection on a private path — NAT-GW or private endpoint?
4. In flow logs, which two fields make reject-lines a high-value detection source?
5. Name the cloud control that answers "who changed the firewall at 02:00?"
*(Answer key: instructor set, Module 5.)*

## 10. Summary & Key Takeaways

- Cloud networking = your segmentation method (L09) expressed as APIs; IaC makes rules reviewable as code.
- SG = workload-level stateful allow-lists (reference by id); NACL = subnet-level stateless fencing (mind ephemeral returns).
- Scoped egress + private endpoints + flow logs = the exfil-resistant, evidence-producing default.

## 11. References

- AWS — VPC User Guide: security groups, NACLs, flow logs, private endpoints (current docs); Azure — NSG/ASG and VNet documentation equivalents.
- NIST SP 800-144 — cloud security guidance; CSA CCM — networking domain (shared responsibility anchors).
- CIS Benchmarks — VPC/NSG baseline sections.
- Terraform provider docs / CloudFormation templates — IaC review practice.

## 12. CLO Mapping

| CLO | Where in this lecture | Assessed via |
|---|---|---|
| CLO-13 | §3.1–3.5 design/decision skills; VPC build §7 | Lab-09/10, Quiz 4 (partial W10), Quiz 5 (W14), Assignment 7 |
