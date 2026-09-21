---
marp: true
theme: default
paginate: true
lecture: L09
week: 5
clos: [CLO-3]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# Defense in Depth & Network Segmentation

**Network Security · Lecture 9 · Week 5**

*The attacker's map is your network's topology. Redesign the map.*

<!-- notes: OPEN (2 min). Hook: "Modules 1–2 read the attacker's
playbook. Module 3 redraws the field they play on." -->

---

## Learning Objectives

1. **Explain** defense in depth as a *portfolio*, not a stack of boxes
2. **Design** zone models driven by sensitivity + behavior
3. **Build** an initiation flow matrix with default-deny discipline
4. **Sequence** segmentation rollout without breaking operations
5. **Choose** telemetry tap points that make segmentation observable

<!-- notes: (1 min) Objective 3 is Assignment 1's core; objective 4 is
the operational-realism discriminator the rubric grades hardest. -->

---

## Defense in Depth: The Portfolio

- Every control has a failure rate — depth covers the misses
- Layers: **prevent → detect → respond** (map the course again)
- Independent failures matter: two controls failing *together* < one
  strong control twice

<!-- notes: (4 min) "Independent" is the deep point: DAI + TLS fix
different failures (position vs exposure) — that's depth. Two
firewalls from the same config bug aren't. cs-098's panel probes this
exact distinction. -->

---

## Zones: Sensitivity + Behavior

| Zone | Members | Posture |
|---|---|---|
| Internet-facing (DMZ) | reverse proxy | expose only 80/443 |
| User | workstations | no inbound from server zones |
| Server-tier | app services | inbound by design only |
| Data-tier | databases | inbound from app tier only |
| Management | admin hosts | inbound from jump hosts only |
| Guest/IoT/OT | untrusted devices | internet-only, isolated |

- Zones follow *what the machines do*, not org charts

<!-- notes: (6 min) Diagram 01's zones named. Quiz-8's zone questions
read this. The IoT/OT row carries L06's vendor-remote-access trap
(Assignment 1's graded trap). -->

---

## The Flow Matrix (Initiation Discipline)

| From ↓ / To → | DMZ | User | App | DB | Mgmt |
|---|---|---|---|---|---|
| DMZ | — | ✗ | 8443 | ✗ | ✗ |
| User | ✗ | — | 8080 | ✗ | ✗ |
| App | ✗ | ✗ | — | 3306 | ✗ |
| Mgmt | SSH | SSH | SSH | SSH | — |

- **Unlisted = denied.** The matrix *is* the policy.

<!-- notes: (6 min) Read one row aloud, then have students predict the
next. Direction (initiation) is the graded subtlety — who *starts* the
conversation. Quiz-8 Q8's established-vs-any distinction lands here. -->

---

## Default-Deny: The Posture

- Permit lists grow; deny lists rot — **default-deny scales**
- Egress too: allow-list updates, C2 paths, DNS (L12's preview)
- The audit story: "here is every allowed flow, and why"

<!-- notes: (4 min) cs-035's egress case is the expert version. The
audit-story line is the compliance argument students will defend in the
capstone. -->

---

## Microsegmentation: The Fine Grain

- VLANs = coarse zones; microsegmentation = per-workload policy
- East-west traffic: the majority of real flows, the majority of real
  lateral movement
- Implementation shapes: distributed firewalls, host policies, identity
  proxies (L12's NAC/ZT bridge)

<!-- notes: (4 min) cs-029's concept case. QB-015's traffic-drop
interpretation question is here: shadow flows reveal undocumented
dependencies. -->

---

## Segmentation Rollout: Observe First

- Phase 1: enforcement off, telemetry on — **record what actually
  flows**
- Phase 2: enforce by zone risk, with per-step rollback criteria
- The observe-then-enforce rhythm prevents the 2 a.m. page

![bg right:36% fit](diagrams/01-enterprise-segmentation.md)

<!-- notes: (6 min) Diagram 01 fully taught now: zones, enforcement
points, taps. Assignment 1 grades the phase discipline — "enforce
first" proposals cap in the rubric's developing band. -->

---

## Telemetry Taps: Making the Design Observable

- SPAN/TAP at each segment boundary → Zeek/IDS
- Firewall logs → SIEM (policy decisions)
- The design that can't see itself can't defend itself

<!-- notes: (3 min) Tap placement is objective 5. Quiz-11 Q7's
"packet-level vs policy-decision" path question reads this exact
picture. -->

---

## Segmentation Breaks Things — Plan For It

- Top forgotten flows: **DNS, NTP, backup, vendor remote access**
- Breakage detection: flow-log deltas vs baseline
- Rollback criteria per enforcement step (metric + threshold + action)

<!-- notes: (5 min) Assignment 1's "two forgotten flows" task. The
rollback criteria (metric/threshold/action) is the operational-realism
marker separating first from developing submissions. -->

---

## CS/DS Example: The Cluster Zone

- DS cluster = its own zone: compute + storage + brokered lake access
- Per-job credentials (L16's ZT seed) + egress allow-list
- The cs-088 incident is what an unsegmented cluster costs

<!-- notes: (3 min) DS framing: the cluster is the zone with the
highest-value data and the sloppiest access patterns — segmentation is
its cheapest defense. -->

---

## Activity: Zone the Hospital (7 min)

Patient records, 200 workstations, guest Wi-Fi, infusion pumps (vendor
cloud), building access control. Draw zones + 5 matrix rows.

<!-- notes: (7 min incl. debrief) This is the midterm D1 scenario —
tell students so. The infusion-pump vendor path is the trap: safety
over policy, compensating monitoring. -->

---

## Case Study: cs-026 (5 min)

- Flat-network segmentation proposal — phase it for survival

<!-- notes: (5 min) Classroom protocol; the case's phase-1 observation
discipline mirrors the lecture's rollout slide. -->

---

## Formative Check

- Oral: why does default-deny scale better than default-allow?

<!-- notes: (2 min) Exit oral. QB-011's implicit-deny + cs-035's
reasoning are the reference answers. -->

---

## References & Next

- NIST SP 800-207 (zero trust concepts — preview), vendor segmentation
  guides
- Diagrams: `diagrams/01-enterprise-segmentation.md`
- **Next (L10):** firewalls — concepts and placement
