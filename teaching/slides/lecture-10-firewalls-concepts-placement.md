---
marp: true
theme: default
paginate: true
lecture: L10
week: 6
clos: [CLO-3, CLO-4]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# Firewalls: Concepts & Placement

**Network Security · Lecture 10 · Week 6**

*The policy engine at the trust boundary.*

<!-- notes: OPEN (2 min). Hook: "A firewall is not a box — it's a
decision point. Today we place decisions, not hardware." -->

---

## Learning Objectives

1. **Distinguish** packet filtering, stateful inspection, NGFW classes
2. **Explain** the state table's role in validating return traffic
3. **Place** firewalls across a segmented estate with rationale
4. **Analyze** high-availability behavior and its security limits
5. **Evaluate** NGFW features (app control, IPS) against their costs

<!-- notes: (1 min) Objective 2 is quiz/midterm core; objective 5 sets
L11–12's engineering depth. -->

---

## Packet Filtering: The First Match

- Per-packet, per-interface rules; stateless
- Cheap, fast, blind to connection context
- The ACL mechanics live in L11 — today, the concept

<!-- notes: (3 min) One-slide class intro; L11 does the mechanics.
Quiz-8 Q1's contrast comes next slide. -->

---

## Stateful Inspection: The Connection Table

- Track conversations: `src/dst, ports, seq, timers`
- Return traffic matched to **existing** state — no rule needed
- New connections evaluated by policy; sessions get state entries

![bg right:36% fit](diagrams/04-acl-stateful-flow.md)

<!-- notes: (6 min) Diagram 04's flow taught fully. Quiz-8 Q8's
"established vs any" distinction + midterm A5 both read this. The
"state = resource" refrain returns (DoS continuity). -->

---

## NGFW: Beyond the Port

- Application awareness (identify apps despite ports), user identity,
  integrated IPS, TLS inspection (with costs)
- Value: policy on *what* is said, not just where it connects
- Costs: latency, complexity, TLS-privacy tradeoffs, false-app verdicts

<!-- notes: (5 min) Balanced slide per course accuracy rule: NGFW is
real value + real cost. cs-032's app-control case explores the policy
side; the privacy cost of TLS inspection is a governance question, not
just technical. -->

---

## Placement: Where Decisions Go

| Position | Decision |
|---|---|
| Edge | what the internet may touch (DMZ rules) |
| Behind DMZ | what DMZ may initiate (the forgotten one!) |
| Server/User boundary | east-west control |
| Data tier | crown-jewel-only ingress |
| Management plane | who administers anything |

- Every zone boundary from L09 = one decision point

<!-- notes: (6 min) Diagram 01's firewalls named with their policies.
The "behind DMZ egress" row is the classic miss (QB-042's design
question is exactly this). -->

---

## HA Pairs: Availability vs Security

- Active/standby failover keeps the policy alive when hardware dies
- Failover syncs state — but *both* share config bugs (bug ≠ box)
- Session sync gaps during failover = brief state loss

<!-- notes: (4 min) cs-033's case explores failover behavior. The
honest limit: HA buys uptime, not correctness — config review remains
the control. -->

---

## The State Table Under Fire

- Connection tables are finite — floods target them (L08's continuity)
- Timeouts matter: long-lived idle entries vs churn
- Sizing + SYN-proxy behaviors = the operational knobs

<!-- notes: (4 min) Continuity slide: floods exhaust state; sizing and
timeouts are the defense knobs. Quiz-level: state = resource. -->

---

## Virtual & Cloud Firewalls

- Same concepts, new placement: SG/NACL (L19) = distributed stateful/
  stateless pairs
- Edge appliance vs microsegmentation agents vs identity proxies
- The concept portability point: **policy classes survive the platform
  change**

<!-- notes: (4 min) Bridge to module 5: cloud changes *where*, not
*what*. Quiz 4 Q3's SG definition plants the seed. -->

---

## CS/DS Example: The Cluster's Egress Firewall

- GPU nodes need: package mirrors, lake API, schedulers
- Everything else: denied + logged (cs-088's cryptomining was exactly
  an egress failure)
- One allow-list, huge risk reduction

<!-- notes: (3 min) DS framing: the cluster egress allow-list is the
single highest-value control for research estates. Concrete and cheap. -->

---

## Activity: Place the Decisions (6 min)

Diagram 01 without firewalls: place four decision points, name each
one's policy in one line.

<!-- notes: (6 min) Pairs on the printed diagram. Debrief against the
placement table — the "behind DMZ" point recurs as the commonly missed
one. -->

---

## Case Study: cs-030 (5 min)

- Branch firewall placement — throughput, egress, and management
  tradeoffs

<!-- notes: (5 min) The case's branch context previews module 5's
SaaS-direct breakout (cs-093's branch handling). -->

---

## Formative Check

- Oral: what does the state table add beyond an ACL? What does HA *not*
  buy you?

<!-- notes: (2 min) Exit oral — both are examinable. -->

---

## References & Next

- NIST SP 800-41 (firewall policy guidance)
- Diagrams: `diagrams/04-acl-stateful-flow.md`
- **Next (L11):** ACLs & rulebase engineering — the rules themselves
