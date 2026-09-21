---
marp: true
theme: default
paginate: true
lecture: L12
week: 5
clos: [CLO-3]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# NAT, Proxies, Egress & NAC

**Network Security · Lecture 12 · Week 5**

*The edge's supporting cast — and one honest demotion for NAT.*

<!-- notes: OPEN (2 min). Hook: "NAT has a reputation. Today we
audit it." -->

---

## Learning Objectives

1. **Characterize** NAT accurately: address mechanism with incidental
   filtering side-effects
2. **Distinguish** explicit vs transparent proxy use
3. **Design** an egress control policy (the course's repeated theme)
4. **Explain** NAC's admission model vs zero-trust's continuous model
5. **Debate** the privacy cost of TLS inspection honestly

<!-- notes: (1 min) Objective 1 is quiz-8's precise answer; objective 5
is the ethics-adjacent judgment the course grades. -->

---

## NAT: The Honest Audit

- Purpose: address translation (RFC 3022) — many-to-one, one-to-one,
  port-forwarding
- *Incidental* filtering: unsolicited inbound can't map to a host
  (no state)
- Not a firewall: no policy engine, no identity, no logging discipline
- IPv6 removes the address crunch — the "NAT security" crutch goes with
  it

<!-- notes: (6 min) Quiz-8 Q1 is this slide's exact answer. The IPv6
point matters: "we have NAT" is not an architecture. cs-037's
address-plan case is the operational companion. -->

---

## Proxies: Standing In For Clients

- **Explicit**: clients configured to use it — visible, authenticatable
- **Transparent**: traffic intercepted en route — invisible to users
- Value: one egress point → policy, logging, caching, malware scan
- Proxy + TLS = the MITM-by-design question (next slide)

![bg right:34% fit](diagrams/01-enterprise-segmentation.md)

<!-- notes: (5 min) Diagram 01's proxy position. cs-038's university
explicit-proxy case carries the deployment depth. -->

---

## TLS Inspection: The Honest Cost

- Mechanism: proxy re-terminates TLS with its own CA on clients
- Gains: URL/content policy on encrypted traffic
- Costs: privacy (legal/HR implications), endpoint trust (root CA),
  breakage (cert pinning apps)
- Judgment: inspect *classes* of traffic, not everything — with
  governance sign-off

<!-- notes: (6 min) The ethics slide: technical capability vs
proportionate use. The "classes not everything" line is the graded
judgment. Quiz-4's shadow of this appears in L14's TLS depth. -->

---

## Egress Control: Who You Become

- The L11 egress ACL + proxy = the egress policy stack
- Default-deny + allow-list: updates, DNS, sanctioned SaaS
- Value proven twice already: C2 containment (L08), cluster hygiene
  (L10)

<!-- notes: (4 min) Continuity slide: egress is the course's recurring
high-value control (cs-035, QB-013, QB-027). Students should predict
the slide's content by now — that's learning. -->

---

## NAC: Admission Control

- Assess devices at join: posture (patched? AV?), identity, role
- Grant: VLAN/segment membership per verdict
- Limits: point-in-time verdict; posture checks are gameable;
  MAB/IoT corners are soft

<!-- notes: (5 min) cs-039's adoption case explores the bypass risks.
NAC's "one-time admission" limitation is the setup for zero trust
(L16's per-request contrast, quiz-8 Q5). -->

---

## NAC vs Zero Trust (Preview)

| Dimension | NAC | Zero trust |
|---|---|---|
| Decision | at admission | per request/session |
| Signals | posture at join | identity + device + context, continuous |
| Trust model | segment membership | never implicit |

- Course arc: NAC is a *tool*; ZT is a *model* (module 8's capstone
  designs it)

<!-- notes: (4 min) The table is quiz-8 Q4/Q5's territory. Keep the
bridge short — L16 and cs-093 carry the depth. -->

---

## CS/DS Example: Egress for the Notebook Fleet

- Notebooks: package index, artifact registry, lake API — allow-list
- Pre-commit hooks + egress = the credential-leak containment pair
  (cs-088 → assignment-7 continuity)

<!-- notes: (3 min) DS framing: egress is *proportional* protection for
a research estate — the two-line allow-list pattern again. -->

---

## Activity: Design the Egress Policy (6 min)

Estate: workstations, servers, GPU cluster, VoIP. Draft the allow-list
classes and one *denied-but-logged* class you'd watch first.

<!-- notes: (6 min) The "watch first" class is the telemetry hook —
usually servers' outbound (legit less common, attacker-favored). -->

---

## Case Study: cs-037 (5 min)

- NAT mode & address plan — operationally honest design

<!-- notes: (5 min) The case keeps NAT in its honest lane: address
planning, not security architecture. -->

---

## Formative Check

- Oral: three things NAT is not. One signal NAC can't see after
  admission.

<!-- notes: (2 min) Exit oral: not a firewall/policy/identity system;
post-admission drift, credential swap, session hijack — any honest
answer. -->

---

## References & Next

- RFC 3022 (NAT), NIST SP 800-207 (ZT preview)
- Diagrams: `diagrams/01-enterprise-segmentation.md`
- **Next (L13):** cryptographic foundations — claims become proofs
