# L06 — Layer-2 & LAN Attacks

> **Scope and safety note:** this lecture explains attack *mechanics* to the depth
> needed to design and verify defenses. All observation happens on the instructor's
> authorized lab range. Attempting these against networks you do not own or are not
> explicitly authorized to test is illegal and is a course-dismissal offense.

## 1. Learning Objectives

By the end of this session you can: (1) explain how ARP spoofing, MAC flooding, STP manipulation, and VLAN hopping work — as *abuse of learning protocols*; (2) identify each attack's packet/log signature; (3) map each attack to its switch-side control (DAI, DHCP snooping, port security, BPDU/root guard, DTP hygiene); (4) read a capture + switch log together as one investigation.

## 2. Key Definitions

| Term | Definition |
|---|---|
| ARP spoofing (poisoning) | Sending forged ARP replies to overwrite victims' IP→MAC caches |
| MAC flooding | Flooding fake source MACs to exhaust the switch CAM table → unicast flooding |
| STP manipulation | Advertising a superior bridge to become spanning-tree root |
| VLAN hopping | Gaining traffic from another VLAN (switch spoofing via DTP; double-tagging) |
| DAI | Dynamic ARP Inspection — validates ARP against the DHCP-snooping binding table |
| BPDU guard / root guard | Port protections against unwanted spanning-tree participation/root changes |
| DTP | Dynamic Trunking Protocol — negotiates trunk ports (disabled in hardened configs) |

## 3. Detailed Explanations

### 3.1 The unifying idea: switches *believe what they hear*
L02 established that ARP has no authentication, CAM tables learn from source MACs, and spanning tree elects a root from advertised priorities. Every attack today is the same trick: **send better-sounding lies to a learning protocol**. That framing matters — it tells you both the detection (protocol anomalies) and the control class (validate before trusting).

### 3.2 ARP spoofing: stealing the on-path position
Attacker sends unsolicited ARP replies: "10.0.0.1 (gateway) is-at ⟨attacker MAC⟩" to the victim, and "10.0.0.9 (victim) is-at ⟨attacker MAC⟩" to the gateway (bidirectional poisoning). The victim then sends gateway-bound traffic *to the attacker*, who forwards it (invisible interception — L07's position) or drops it (DoS). **Packet evidence:** duplicate IP → different MACs in a short window; gratuitous-ARP bursts. **Controls:** DHCP snooping builds the IP→MAC binding table; DAI validates every ARP packet on untrusted ports against it; static bindings cover critical static hosts.

### 3.3 MAC flooding: breaking the switch's memory
Fake frames with random source MACs fill the CAM table; the switch degrades to flooding unknown unicasts — a hub for a moment — enabling sniffing. **Evidence:** new-MAC rates per port, CAM-table utilization alarms. **Control:** port security (MAC count limits, sticky learning); 802.1X admission (L12) starves the attack of a foothold.

### 3.4 STP manipulation: becoming the root
Spanning tree elects the bridge with the best (lowest) priority as root. An attacker advertising a superior BPDU becomes root: traffic now transits their segment (on-path) or topology churn causes outages (availability). **Evidence:** unexpected root changes in switch logs; BPDU storms. **Controls:** BPDU guard on access ports (any BPDU = err-disable), root guard on designated uplinks (do not accept better roots there).

### 3.5 VLAN hopping: two shapes
- **Switch spoofing:** the attacker's port negotiates a trunk via DTP → sees all VLANs. Control: `switchport mode access` + DTP disabled — hardened templates do this by default.
- **Double-tagging:** craft a frame with two 802.1Q tags; the ingress switch strips the outer (native) tag and the inner tag lands on another VLAN. Preconditions: knowledge of the native VLAN; traffic is one-directional. Controls: don't share native VLAN with hosts, tag the native VLAN, move unused ports to an unused VLAN.

### 3.6 The attack → control → evidence table (your Module-2 artifact)

| Attack | Position gained | Packet/log evidence | Primary control |
|---|---|---|---|
| ARP spoofing | On-path (bidirectional) | duplicate IP↔MACs; gratuitous bursts | DAI + DHCP snooping |
| MAC flooding | Sniffing window | new-MAC rate; CAM alarms | port security, 802.1X |
| STP manipulation | On-path / DoS | root-change logs; BPDU storms | BPDU + root guard |
| VLAN hop (DTP) | Full trunk view | unexpected trunk on access port | disable DTP, access mode |
| VLAN hop (double-tag) | One-way cross-VLAN | malformed outer-tag frames | native-VLAN hygiene |

## 4. Network Diagram: ARP poisoning position

```
 Victim (10.0.0.9)          Attacker            Gateway (10.0.0.1)
      |  poisoned: "GW is-at A"  |  poisoned: "V is-at A" |
      |------------------------->|<-----------------------|
      |                          |                        |
      |====== victim->gateway traffic transits attacker ===|
              (attacker forwards: invisible; drops: DoS)
```

## 5. Protocol Examples

- Poisoning capture shape: two ARP replies, seconds apart — `10.0.0.1 is-at AA:BB…` then `10.0.0.1 is-at CC:DD…`. The *second* reply is the lie; the capture alone proves the change, not the intent — corroborate with switch logs.
- Switch-side read: `show ip arp inspection statistics` (dropped/validated counts), `show spanning-tree root` (who believes they are root, since when).

## 6. Configuration Concepts (concept level)

- DHCP snooping: `ip dhcp snooping` + trust uplinks → feeds DAI's binding table.
- DAI: `ip arp inspection` on access VLANs; add static bindings for static-IP hosts.
- Hardened port template: access mode, DTP off, port-security, BPDU guard on.

## 7. Security Implications

- L2 attacks are *position theft* — they enable everything in L07 (sniffing/MITM/session attacks).
- Detection = packet signature + switch log; either alone is weaker.
- East-west trust is the attacker's first prize: L2 hygiene (tactical) + segmentation (strategic, L09) answer it together.
- Misconfiguration reopens defaults: audit posture, not purchase orders.

## 8. Realistic Organizational Scenario

**The certificate warnings (running case).** Finance users report intermittent certificate warnings on the intranet portal. A capture shows the gateway IP answering with a workstation's MAC; switch logs show that workstation's port online with a new MAC pattern hours earlier. You now know: ARP poisoning gave an attacker the on-path position, and the warnings were TLS *failing to be fooled* — the visible edge of an invisible attack. Containment and prevention design is **case cs-013**.

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "Switches are security devices" | Switches are *learning* devices; security comes from validation features. |
| "VLANs are a security boundary" | VLANs isolate broadcast; policy needs enforcement points (L09). |
| "L2 attacks need special hardware" | They need a protocol lie and a port — ordinary laptops suffice. |
| "DAI blocks everything until configured" | Static-IP hosts need explicit bindings — plan the exception list. |
| "Port security breaks Wi-Fi/printers" | Tune limits + sticky learning; test legitimate churn before enforcing. |

## 10. Classroom Activities

1. **Observation lab (teams of 3):** from range captures + switch logs, complete the §3.6 table for all four attacks — signature, control, and a Zeek/Suricata rule *idea*.
2. **Lie detector drill:** instructor shows five ARP log excerpts; teams classify legit-failover vs poisoning with reasoning.
3. **Control mapping race:** attack card → control card → evidence card, timed.

## 11. Problem-Solving Questions

1. Why does DAI depend on DHCP snooping, and what must you add for static-IP hosts?
2. Port security blocks MAC flooding — which legitimate scenario causes false positives, and how is it tuned?
3. BPDU guard and root guard protect different directions — explain each and its correct placement.
4. Construct the misconfiguration that reopens double-tagging on a modern switch.
5. An attacker has on-path position at L2. Name three next actions beyond sniffing and one control that blunts all three.

## 12. Exit Ticket

1. Which two ARP-packet properties reveal spoofing in a capture?
2. What switch feature validates ARP replies, and against what data?
3. Why is DTP disabled in hardened templates?
4. Name the precondition double-tagging needs that native-VLAN hygiene removes.
5. Which control stops a rogue root bridge on access ports?

*(Answers: `the instructor answer-key collection (not published)`.)*

## 13. References

- RFC 826 — ARP (the behavior being abused).
- Cisco configuration guides — DHCP Snooping, DAI, BPDU/root Guard (current).
- IEEE 802.1D / 802.1Q — spanning tree and VLAN tagging basis.
- Zeek documentation — ARP analyzer and notice framework.
- Course instructor plan L06 (lab range observations, authorized environment only).

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-2 | §3 classification + §3.6 mapping | Quiz 2 (W4), Lab-03, Case set A |
