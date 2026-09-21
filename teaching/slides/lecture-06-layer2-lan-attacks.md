---
marp: true
theme: default
paginate: true
lecture: L06
week: 3
clos: [CLO-2]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# Layer-2 & LAN Attacks

**Network Security · Lecture 6 · Week 3**

*The local network trusts everyone — watch what that costs.*

<!-- notes: OPEN (2 min). Hook: "L03 said ARP trusts whoever shouts
first. Today: everyone shouts." -->

---

## Learning Objectives

1. **Explain** MAC flooding's mechanism and its fail-open consequence
2. **Trace** ARP poisoning to its MITM conclusion (diagram 03)
3. **Analyze** rogue DHCP as both availability and interception attack
4. **Detect** spanning-tree manipulation in switch telemetry
5. **Design** the switch-feature control set that breaks each attack

<!-- notes: (1 min) Objective 5 is the module's payoff: every attack
slide ends with its switch control. Quiz 2 + quiz 7 + Lab-03 all read
this. -->

---

## MAC Flooding: Exhaust the Table

- Switch CAM/TCAM table is finite
- Flood of *claimed* source MACs → table full
- Fail-open behavior: unknown unicast **flooded to all ports**
- Attacker now sees unicast traffic — a sniffing position

![bg right:36% fit](diagrams/03-arp-poisoning-flow.md)

<!-- notes: (5 min) The mechanism is resource exhaustion, same class as
SYN floods (state = resource). Diagram 03's right side shows the
position; the defense slide follows. Quiz 2 Q2 tests this. -->

---

## Port Security: The Table Guard

- Limit MACs per port; violation → restrict/shutdown
- Stops flooding at the access layer
- Limits: legitimate MAC churn (VoIP+PC chains) needs config care

<!-- notes: (4 min) Honest limitation slide — port security misfires on
legitimate downstream hubs/VM traffic; "limit + violation mode" is the
config judgment. -->

---

## ARP Poisoning: The Full Loop

- Fake replies to victim + gateway → traffic detours through attacker
- Forwarding keeps the victim *online* (stealth)
- Variants: interception, tampering, session theft

<!-- notes: (6 min) Walk diagram 03 fully now — both fake replies, the
forwarding, the payload copy. "Why does the attacker forward?" quiz
question — because a broken victim gets investigated. cs-013's case is
the containment story. -->

---

## Dynamic ARP Inspection: The Binding Check

- DHCP snooping builds the IP↔MAC binding table (trusted ports)
- DAI checks every ARP reply on untrusted ports against bindings
- Mismatch → dropped + logged — the attack dies at the switch

<!-- notes: (5 min) The two-feature pairing: snooping feeds DAI. Quiz 7
Q2 + quiz 2's Section C both test the pairing. Static bindings for
critical servers = the exception path. -->

---

## Rogue DHCP: Both Bladed

- Starvation mode: exhaust the pool (availability)
- Rogue mode: offer evil gateway/DNS (interception)
- Clients can't tell legit from rogue — **any OFFER wins**

<!-- notes: (4 min) Recap from L03, now as attack. The "victims work
fine" point is the scary one — repeat it. -->

---

## DHCP Snooping + Rate Limiting

- Trust only ports toward real DHCP servers
- Rate-limit DISCOVER bursts (starvation blunted)
- Option-82 insertion for tracking (site-dependent)

<!-- notes: (4 min) The snooping→DAI dependency repeats — same binding
table serves both. Lab-03's evidence reads these logs. -->

---

## VLAN Hopping: Double-Tag & Trunk Abuse

- Switches strip one 802.1Q tag; a *second* tag can smuggle VLAN ids
- Auto-trunking on access ports = the enabler
- Fix: disable auto-trunking, explicit trunk allow-lists, native VLAN
  hygiene

<!-- notes: (5 min) Conceptual only — no payload crafting. The enabler
is config hygiene, not exploit genius: "the attack is a *default
setting*." cs-015's case reads the attempt evidence. -->

---

## Spanning-Tree Manipulation

- Attacker claims root bridge (lowest priority) → traffic reroutes
  through them
- BPDU guard on access ports: BPDUs there = err-disable
- Root guard on designated ports: root stays where it belongs

<!-- notes: (4 min) STP manipulation is the least-known L2 attack —
spend the time. Quiz 7 Q5 tests BPDU guard's definition. cs-016's case
detects it. -->

---

## The L2 Control Set (Cheat Slide)

| Attack | Control |
|---|---|
| MAC flooding | port security |
| ARP poisoning | DHCP snooping + DAI |
| Rogue DHCP | DHCP snooping + rate-limit |
| VLAN hop | trunk hygiene + native VLAN care |
| STP abuse | BPDU guard + root guard |

- All *switch features* — the wire's trust is fixable at the box

<!-- notes: (3 min) The table is Quiz 2's answer matrix. Read it as
"attack → control" pairs; students should be able to reconstruct it
from mechanisms, not memorize. -->

---

## CS/DS Example: The Cluster's Flat Management LAN

- GPU nodes + scheduler + storage on one unsegmented LAN
- One poisoned ARP entry = dataset-in-flight interception
- Control set above + management-VLAN segmentation (L09)

<!-- notes: (3 min) DS framing: the lab cluster is the realistic flat
LAN. The "one ARP entry" phrasing makes the stakes concrete. -->

---

## Activity: Switch Log Reading (6 min)

Given switch telemetry: DAI drops from one port, MAC-table churn on
another, BPDU on a third — which attack is each, and which control
*already worked*?

<!-- notes: (6 min) Lab-03's dataset. Key insight: a drop log is a
*control succeeding* — students read drops as failures at first. -->

---

## Case Study: cs-014 (5 min)

- MAC-flooding signs — what does the switch see before fail-open?

<!-- notes: (5 min) The tell: MAC count per port climbing + new-MAC rate.
cs-014's reasoning per protocol. -->

---

## Formative Check

- Oral: attack → control pairs for ARP poisoning and rogue DHCP.

<!-- notes: (2 min) Exit oral — the pairing is the examinable unit. -->

---

## References & Next

- IEEE 802.1Q, vendor switch-security guides (concept references)
- Diagrams: `diagrams/03-arp-poisoning-flow.md`
- **Next (L07):** sniffing, MITM, session attacks — interception gets
  organized
