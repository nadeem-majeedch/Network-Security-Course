---
lecture: L06
title: Layer-2 & LAN Attacks
module: 2
week: 3
hours: 2
clos: [CLO-2]
difficulty: beginner-intermediate
status: complete
artifact-type: teaching-plan
---

# L06 — Layer-2 & LAN Attacks (Teaching Plan)

## 1. Overview & Prerequisites

- **Prerequisites:** L05 (attack modeling — we now instantiate tree leaves), L02 (Ethernet/ARP mechanics, switch learning).
- **Position:** the first *technique* lecture; every attack here is observed (not performed) in the lab range, reinforcing the ethics contract. Detection framing directly feeds L21–L22 sensor work.
- **Faculty prep:** pre-run the L2 attack scenarios on the lab range and export sanitized captures + switch logs for observation; verify students cannot affect anything outside the range.
- **Common misconceptions:** "switches are security devices"; "VLANs are a security boundary"; "L2 attacks require special hardware."

## 2. Learning Objectives

By the end of this lecture, students can:

1. Explain how ARP spoofing poisons caches, what it enables (sniffing, MITM, DoS), and how to detect it from packet evidence (Analyze).
2. Describe CAM-table flooding and distinguish it from legitimate port-security events (Analyze).
3. Outline spanning-tree manipulation (rogue root bridge) and its availability impact (Understand).
4. Classify VLAN-hopping techniques (switch spoofing/DTP; double-tagging) with their preconditions (Analyze).
5. Map each attack to its switch-side control: Dynamic ARP Inspection, DHCP snooping, port security, BPDU guard, native-VLAN hygiene (Apply/Analyze).

## 3. Detailed Concepts

### 3.1 ARP spoofing: overwriting a trust table
- Mechanism: unsolicited is-at replies update the victim's ARP cache and the attacker's NIC forwards (or drops → DoS) — bidirectional poisoning enables on-path position.
- Packet evidence: duplicate IP → different MACs in short window; gratuitous ARP bursts; the same MAC claiming multiple IPs.
- Defenses: DAI (validates ARP against the snooping binding table), DHCP snooping as its foundation, static bindings for critical hosts, 802.1X (later).

### 3.2 MAC flooding vs port security
- Mechanism: random source MACs fill the CAM table → switch floods unicast (hub behavior) → sniffing window.
- Detection: CAM-table size alerts, new-MAC rates per port.
- Control: port security (limit MAC count / sticky learning), 802.1X admission.

### 3.3 STP manipulation
- Mechanism: attacker advertises superior bridge priority → becomes root → traffic transits attacker segment (on-path) or topology churn (DoS).
- Evidence: BPDU storms, unexpected root changes in switch logs.
- Control: BPDU guard on access ports, root guard on designated uplinks, Rapid-PVST+ hygiene.

### 3.4 VLAN hopping
- Switch spoofing (DTP negotiation to trunk): attacker's port negotiates trunk → sees all VLANs. Control: disable DTP, manual access mode.
- Double-tagging: native-VLAN mismatch trick — ingress tag stripped once, leaves inner tag on another VLAN. Preconditions: knowledge of native VLAN; unidirectional; control: set unused native VLAN, tag native VLAN, don't share native between switches and hosts.
- Reality check: modern default configs + no-DTP mostly close these; *misconfiguration* reopens them — audit angle.

### 3.5 Why L2 matters more than students expect
- East-west trust: once on-segment, an attacker sees and touches everything local; segmentation (L09) is the strategic answer, L2 hygiene is the tactical one.
- Detection engineering seed: each attack above maps to a Zeek/Suricata notice or switch syslog — build the mapping table in class (used again in L22).

## 4. Teaching Sequence (120 Minutes)

| Time | Segment | Instructor moves |
|---|---|---|
| 0–10 | Recap: trees → leaves | Pull one leaf from each team's L05 tree: "which leaf does today's attack instantiate?" |
| 10–35 | Core: ARP spoofing | Whiteboard poisoning state machine; play the sanitized capture; students shout out the tell-tale frames |
| 35–55 | Core: flooding, STP, VLAN hop | Switch-log samples projected; classify each event; precondition analysis for double-tagging |
| 55–65 | Break | — |
| 65–75 | Core: control mapping table | Build attack→control→evidence table on the board (kept as course artifact) |
| 75–110 | Student activity: observation lab | Teams examine range captures + switch logs; complete detection worksheet (cs-013..016 prep) |
| 110–120 | Wrap + formative | Exit ticket; trailer: "above L2: sniffing you can't see — MITM at L3+" |

## 5. Technical Examples

```
# Observation-only: inspect a captured ARP-poisoning exchange (range capture file)
tshark -r arp-spoof.pcap -Y 'arp' -T fields -e frame.time -e arp.src.proto_ipv4 \
  -e arp.src.hw_mac -e arp.opcode
# Teaching point: same IPv4 bound to two MACs within seconds = classic signature.

# CAM/ARP table views on the range switch (read-only commands shown)
show mac address-table | include Gi0/5        # count of learned MACs per port
show ip arp inspection statistics             # dropped/validated ARP counts
show spanning-tree root                       # who believes they are root, and why
```
Expected teaching points: evidence lives both on the wire and in switch logs; defenders read both.

## 6. Discussion Questions

1. Why does DAI depend on DHCP snooping? What happens to static-IP hosts under DAI, and how do you include them?
2. Port security blocks MAC flooding. Which legitimate scenario causes false positives, and how is it tuned?
3. BPDU guard and root guard protect different directions — explain each and where it belongs.
4. VLAN hopping is mostly closed by defaults. Construct the misconfiguration that reopens it.
5. An attacker has on-path position at L2. Name three next actions beyond sniffing, and one control that blunts all three.

## 7. Student Activity

**Observation lab (35 min, teams of 3):** from the exported range artifacts, each team completes a detection worksheet: for each of the four attacks, record (a) packet/log signature, (b) switch control that prevents it, (c) Zeek/Suricata rule *idea* (pseudocode fine). Teams present one row each; the class assembles the master mapping table.

## 8. Problem-Solving Case

**Primary case — cs-013 "ARP-spoofing incident: symptoms and containment" (beginner-intermediate):**
Users report intermittent certificate warnings and slow internal web access. A capture shows the gateway IP answering with the MAC of a workstation; switch logs show that workstation's port recently came online with a new MAC pattern. Students must (a) state the on-path risk in CIA terms, (b) identify the two evidence artifacts, (c) order containment steps (isolate port, flush ARP, verify gateway), and (d) propose the switch control that prevents recurrence.
**Linked cases:** cs-014 (MAC flooding), cs-015 (VLAN hopping attempt), cs-016 (STP manipulation).
*(Model solutions: instructor answer-key set, Module 2.)*

## 9. Formative Assessment

1. Which two ARP-packet properties reveal spoofing in a capture?
2. What switch feature validates ARP replies, and against what data?
3. Why is DTP disabled by default in hardened templates?
4. Name the precondition for double-tagging that native-VLAN hygiene removes.
5. Which control stops a rogue root bridge on access ports?
*(Answer key: instructor set, Module 2.)*

## 10. Summary & Key Takeaways

- L2 attacks abuse *learning* protocols (ARP, CAM, STP, DTP) — the switch believes what it hears.
- Detection = packet signature + switch log; prevention = snooping/validation controls per protocol.
- Local trust is the attacker's first prize; Module 3 turns this into architecture (segmentation, egress).

## 11. References

- RFC 826 — ARP (baseline behavior being abused).
- Cisco — Dynamic ARP Inspection, DHCP Snooping, BPDU Guard configuration guides (current docs).
- IEEE 802.1D/802.1Q — spanning tree and VLAN tagging basis.
- Zeek docs — ARP analyzer & notice framework (rule idea vocabulary for §7).
- Stallings — LAN/WAN protocol chapters (switching fundamentals).

## 12. CLO Mapping

| CLO | Where in this lecture | Assessed via |
|---|---|---|
| CLO-2 | §3.1–3.5 attack classification + control mapping; observation lab | Quiz 2 (W4), Lab-03, Case set A |
