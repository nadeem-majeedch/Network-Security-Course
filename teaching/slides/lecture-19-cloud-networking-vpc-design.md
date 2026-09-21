---
marp: true
theme: default
paginate: true
lecture: L19
week: 9
clos: [CLO-13]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# Cloud Networking I — VPC Design & Controls

**Network Security · Lecture 19 · Week 9**

*Your data center is now API calls. So is its security.*

<!-- notes: OPEN (2 min). Hook: "Everything you learned on boxes
becomes API calls this week — including the mistakes." -->

---

## Learning Objectives

1. **Design** a tiered VPC: subnets, route tables, gateways
2. **Distinguish** security groups vs network ACLs by state and scope
3. **Explain** NAT gateways and egress patterns
4. **Read** VPC flow logs as the cloud's flow telemetry
5. **Choose** endpoints/peering designs that keep traffic off the
   internet

![bg right:34% fit](diagrams/09-cloud-vpc-controls.md)

<!-- notes: (1 min) Diagram 09 taught across today and L20. Objective 2
is quiz-4 Q3/Q6's core; objective 4 is cs-065's case. -->

---

## The Tiered VPC

- Public subnet: load balancer / web tier (IGW path)
- Private subnets: app tier, DB tier (NAT for outbound-only)
- Route tables decide *paths* — the control before the filter

<!-- notes: (5 min) Diagram 09's topology: the three subnets and their
routes. Quiz-10 Q3's NAT-route question reads this. "Route first,
filter second" is the design order. -->

---

## Security Groups: Stateful, Instance-Level

- Attached to instances/enis; **allow-only** rules; stateful (return
  traffic auto-allowed)
- Reference other SGs (app-SG → db-SG) — policy follows topology
- Default posture: deny in, allow out — tighten that too

<!-- notes: (6 min) Quiz-4 Q3 is the definition. The SG-reference
feature is the cloud-native policy elegance — quiz-10's DB question
uses it. The "tighten outbound" line previews egress discipline. -->

---

## Network ACLs: Stateless Subnet Edge

- Numbered rules, allow *and* deny, stateless (both directions
  explicit)
- The **backstop**: a permissive SG mistake can't override the NACL
  deny
- Ephemeral-port return rules are the classic NACL breakage

<!-- notes: (6 min) QB-047's design question is exactly the backstop
pattern. Quiz-4 Q6's monitoring difference: NACL deny counters as cheap
tripwires. -->

---

## NAT & Egress Patterns

- NAT gateway: private subnets initiate outbound; no inbound sessions
- Egress discipline cloud-style: allow-list via NACL/edge firewall/
  proxy
- cs-065's anomaly case = an uncontrolled egress story

<!-- notes: (4 min) The continuity: egress control is the course's
recurring theme, now in cloud vocabulary. Quiz-10 Q3's route-table
answer anchors here. -->

---

## Flow Logs: The Cloud's Telemetry

- Metadata per flow: src/dst, ports, bytes, **accept/reject**, time
- VPC/subnet/ENI scoping; deliver to storage/SIEM
- No payloads — behavior only (privacy + volume tradeoff)

<!-- notes: (6 min) cs-065's case reads exactly these columns. The
accept/reject action field is the tripwireQuiz-10 Q4 mentions. CS/DS
students: this is *your* daily data shape. -->

---

## Endpoints & Peering: Keep Traffic Home

- S3/object-storage gateway endpoints: backup/data paths skip the
  internet
- Peering/transit: inter-VPC flows with explicit route control
- Quiz-10 Q5's answer: route tables/propagation govern path choices

<!-- notes: (4 min) The quiz-10 Q7 diagram question (S3 endpoint route)
anchors here. "Keep crown-jewel paths off the internet" is the design
mantra. -->

---

## The Cloud Control Set

| Concern | Control |
|---|---|
| Tier isolation | subnets + SG references |
| Subnet edge | NACLs (backstop) |
| Outbound | NAT + egress allow-list |
| Visibility | flow logs + audit trail |
| Data paths | gateway endpoints |

<!-- notes: (3 min) Reference table mirroring L06/L17's pattern. Quiz
4's matrix coverage. -->

---

## CS/DS Example: The DS Sandbox Account

- Sandbox VPC: compute + dataset staging; SG-referenced lake access
- No public IPs on compute; endpoints for package/data paths
- The cs-088 cluster story, cloud-native edition

<!-- notes: (3 min) DS framing: the sandbox account is where research
freedom and security discipline negotiate — the design above is the
treaty. -->

---

## Activity: Fix This VPC (6 min)

Given: DB SG allows 3306 from 0.0.0.0/0; no flow logs; DB in public
subnet. Rank fixes; state which control catches a *repeat* mistake.

<!-- notes: (6 min) Fixes: move DB private, SG to app-SG reference,
NACL deny 3306 (backstop), enable flow logs + audit trail. The
"repeat-mistake" answer: audit-trail alerting on SG changes (L20's
detection). -->

---

## Case Study: cs-061 (5 min)

- VPC design review for a three-tier app — read the design like an
  auditor

<!-- notes: (5 min) Classroom protocol; cs-062 (SG vs NACL choice) is
the alternate slot. -->

---

## Formative Check

- Oral: stateful vs stateless — which is the backstop, and why?

<!-- notes: (2 min) Exit oral: NACL = backstop because it filters after
SG mistakes can't undo the subnet deny. -->

---

## References & Next

- Provider security-group/NACL documentation (control classes)
- Diagrams: `diagrams/09-cloud-vpc-controls.md`
- **Next (L20):** hybrid & assurance — logs, identity, and trust
