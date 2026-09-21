# L19 — Cloud Networking I — VPC Design & Controls

## 1. Learning Objectives

By the end of this session you can: (1) map cloud constructs to on-prem concepts (VPC↔site, subnet↔zone, route table↔forwarding); (2) distinguish security groups from network ACLs and select per use case; (3) design a 3-tier VPC with correct subnets, route tables, and least-privilege SG pairs; (4) compare egress models (NAT gateway vs private endpoints); (5) enable and read flow logs as detection evidence.

## 2. Key Definitions

| Term | Definition |
|---|---|
| VPC / VNet | Provider-isolated virtual network — your site in the cloud |
| Subnet | Address range inside a VPC; public (internet-routable) or private |
| Route table | Per-subnet forwarding rules — explicit, no implicit transitivity |
| Security group (SG) | **Stateful**, instance-scoped, allow-only rule set — a mini stateful firewall |
| NACL | **Stateless**, subnet-scoped, numbered, allow+deny rules |
| NAT gateway | Managed egress for private subnets (no inbound) |
| Private endpoint | Private path to provider services (S3/DB-class) without internet transit |
| Flow logs | Metadata records of accepted/rejected connections — the detection feed |
| Shared responsibility | Provider: fabric/hypervisor/isolation. You: segmentation, SG policy, egress, encryption |

## 3. Detailed Explanations

### 3.1 The cloud translation table
| On-prem | Cloud analog | Security delta |
|---|---|---|
| Site/campus | VPC | Soft isolation + global control-plane APIs = new attack surface |
| VLAN/zone | Subnet (+SG) | Policy is API-defined → review it as code (IaC) |
| Router | Route table | Explicit routes; connectivity is what *you* declare |
| Edge firewall | IGW + SGs/NACLs (+WAF at LB) | No L3 "box" — policy is distributed |
| ACLs | SG (stateful allow) / NACL (stateless ordered) | Two rule models coexist — know both |
The networking slice of **shared responsibility** is yours: segmentation, routing, SG policy, egress, encryption in transit. "The provider is certified" covers their fabric, not your flat VPC.

### 3.2 Security groups vs NACLs — the decision skill
- **SG:** stateful (return traffic auto-allowed), instance/ENI-scoped, **allow-only**, all rules evaluated. Use for workload-level least privilege — and **reference other SGs, not CIDRs**: "db-SG allows 5432 from app-SG" scales with autoscaling and reads like policy.
- **NACL:** stateless (must write **ephemeral-port return rules** — the classic "ping works, app breaks" bug), subnet-scoped, numbered ordered, deny-capable. Use for coarse subnet fencing (block bad ranges, explicit guest denies).
- IaC discipline: SG rules reviewed as code (your L11 audit skill transfers directly); no `0.0.0.0/0` on 22/3389 — use SSM-class session agents or a hardened bastion.

### 3.3 The reference 3-tier design (build in class)
Public ALB subnets (2 AZs) → private app subnets → private data subnets, separate route tables. SG chain: **alb-SG** (443 from anywhere) → **app-SG** (8443 from alb-SG) → **db-SG** (5432 from app-SG, egress none). NAT gateway gives the *app* tier egress; the **data** tier gets **private endpoints** (object storage/DB APIs on the private path) — its internet egress is *zero*, which turns any attempt into a logged reject.

### 3.4 Egress models
- **NAT gateway:** simple, managed — but data-tier traffic *can* reach the internet (exfil surface).
- **Private endpoints:** provider services over private IPs — policy checkpoints + no internet transit.
- **Scoped SG egress:** the default "allow all egress" on SGs is a trap — scope it (L12's allow-list skill, cloud edition). DNS discipline: VPC resolver + private hosted zones + outbound DNS filtering.

### 3.5 Flow logs (the detection feed — L21 bridge)
VPC/subnet/ENI-level metadata: accept/reject, bytes, direction → S3/SIEM. **Reject lines are gold**: data-tier attempting internet egress = exfil attempt or misconfig, either way alert-worthy. Add **change alarms**: who modified an SG or route table at 02:00 is a first-class security question (L20 continues).

## 4. Network Diagram: 3-tier VPC with SG chain

```
 Internet ─► [IGW] ─► ALB (public-a/public-b, SG: 443 from 0.0.0.0/0)
                          │ (from alb-SG)
                      APP tier (private, NAT-GW egress, SG: from alb-SG)
                          │ (from app-SG, 5432 only)
                      DATA tier (private, NO internet egress,
                                 private endpoint for object store,
                                 SG: from app-SG, egress: none)
   flow logs → SIEM: REJECT data→internet = page someone
```

## 5. Protocol Examples

- IaC-flavored rule pattern (provider-neutral pseudocode): `sg.db.ingress(5432, from=sg.app)` — reference-by-id, not CIDR.
- Flow-log lines (staged teaching set): `2 10.40.11.5 10.40.21.9 5432 ACCEPT` (expected); `2 10.40.21.9 52.94.x.x 443 REJECT` (data-tier internet attempt — hardening working *and* alerting).

## 6. Configuration Concepts (concept level)

- Separate route tables per tier; NAT-GW only where egress is justified.
- SG change alarms + route-change alarms (config-recorder class tools).
- VPC Flow Logs: all-traffic vs reject-only (cost vs coverage decision), destination = SIEM.

## 7. Security Implications

- Cloud networking = your segmentation method (L09) expressed as APIs — reviewable, automatable, and *driftable*.
- SG-by-reference + scoped egress + private endpoints = the exfil-resistant default.
- The control plane is the new perimeter: who can change SGs/routes *is* a security control.

## 8. Realistic Organizational Scenario

**The inherited VPC (running case).** One flat /16; everything in public subnets with public IPs; one giant SG allowing all-internal; the database reachable from the internet through a forgotten rule. Your deliverable: the five worst findings with evidence, the target 3-tier design (subnets, route tables, SG pairs by reference), a migration plan that doesn't break the running app (staged SGs, log-only equivalents), and the post-migration detection set. Full case: **cs-061**; the build + harden is Lab-09 part 2.

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "The provider handles security" | Shared: they secure the fabric; you secure your VPC design, SGs, egress. |
| "Private subnet = secure subnet" | Private = no direct internet *inbound*; routing and SG policy still decide reachability. |
| "SGs are just firewalls" | They're stateful, allow-only, instance-scoped — different model, different bugs. |
| "NACLs need no return rules" | They're stateless: forget ephemeral return rules and apps break. |
| "Default VPC is fine for production" | It's a convenience scaffold — flat and permissive by design. |

## 10. Classroom Activities

1. **VPC build + harden (pairs):** deploy the starter 3-tier; apply the checklist — scoped egress, data-tier no-internet verification (curl test fails *with evidence*), flow logs on, one SG-change alarm.
2. **SG-vs-NACL sorting:** eight requirements → which construct, why.
3. **Flow-log reading drill:** annotate ACCEPT/REJECT lines; classify each as expected, misconfig, or investigation-worthy.

## 11. Problem-Solving Questions

1. Why is "the provider is certified, so we're secure" wrong *for networking specifically*? Give the boundary for three services.
2. SG rules referencing other SGs instead of CIDRs — what breaks during migration, and what does it buy day-to-day?
3. Data tier needs object storage: NAT-GW vs private endpoint — security, cost, and egress-policy consequences?
4. Which NACL use cases justify stateless complexity? Argue both sides.
5. Who can change an SG in your org? If "any developer with console access," which two controls fix it?

## 12. Exit Ticket

1. One property making SGs stateful; one making NACLs stateless.
2. Why reference SGs by id instead of CIDR in tier rules?
3. Which construct puts object storage on a private path — NAT-GW or private endpoint?
4. Which two flow-log fields make reject lines a high-value detection?
5. Name the cloud control that answers "who changed the firewall at 02:00?"

*(Answers: `the instructor answer-key collection (not published)`.)*

## 13. References

- AWS VPC User Guide (SGs, NACLs, flow logs, private endpoints); Azure VNet/NSG docs — current.
- NIST SP 800-144 — cloud security guidance; CSA CCM — networking domain.
- CIS Benchmarks — cloud provider baseline sections.
- Terraform/CloudFormation documentation — IaC review practice.

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-13 | §3 design/decision skills; build | Lab-09/10, Quiz 4 (partial), Quiz 5 (W14), Assignment 7 |
