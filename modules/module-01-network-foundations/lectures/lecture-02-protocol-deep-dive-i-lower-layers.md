---
lecture: L02
title: Protocol Deep Dive I — Ethernet, ARP, IP, ICMP
module: 1
week: 1
hours: 2
clos: [CLO-1]
difficulty: beginner
status: complete
artifact-type: teaching-plan
---

# L02 — Protocol Deep Dive I — Ethernet, ARP, IP, ICMP (Teaching Plan)

## 1. Overview & Prerequisites

- **Prerequisites:** L01 (CIA/risk vocabulary, vantage points); Computer Networks (encapsulation concept).
- **Position:** Layer-2/3 mechanics are the substrate of every later attack (L06–L08) and every detection (L21–L23, L29–L30). Students who cannot read these frames cannot detect attacks on them.
- **Faculty prep:** pre-generate a sanitized campus capture (5 minutes of ARP/ICMP/IPv6 NDP traffic) for the guided lab; verify Wireshark profiles on lab images.
- **Common misconceptions:** "switches make ARP attacks impossible"; "ICMP is always evil and should be blocked"; "IPv6 is just bigger addresses."

## 2. Learning Objectives

By the end of this lecture, students can:

1. Dissect an Ethernet II frame field-by-field and explain what each field is trusted for (Analyze).
2. Trace the ARP resolution flow, describe cache states, and identify why ARP has no authentication (Understand/Analyze).
3. Explain IPv4 addressing/forwarding essentials (best-effort delivery, TTL, fragmentation) and their security implications (Understand).
4. Summarize IPv6 differences relevant to security: NDP replaces ARP, SLAAC, link-local addressing (Understand).
5. Classify ICMP message types into diagnostic value vs abuse potential (ping flood, redirect, unreachable-based scanning) (Analyze).

## 3. Detailed Concepts

### 3.1 Ethernet frames and the trust in MAC addresses
- Frame anatomy: preamble → dst MAC | src MAC | EtherType | payload | FCS. FCS protects against *corruption*, not *tampering* (no authenticity).
- Switch learning: CAM table built from observed source MACs → table exhaustion (MAC flooding, L06) and MAC spoofing are protocol-native risks.
- Broadcast domains: anything any host broadcasts, all local hosts receive — the reason on-link sniffing works without any exploit.

### 3.2 ARP: the protocol that trusts everyone
- Flow: who-has 10.0.0.5? tell 10.0.0.9 → is-at reply; cache entries age out (gratuitous ARP on boot/notify).
- No request/reply authentication, no request/reply correlation, replies are processed *unsolicited* → gratuitous and spoofed replies overwrite caches (mechanism behind L06 ARP spoofing).
- Defenses preview: Dynamic ARP Inspection, port security, static entries (and why static entries don't scale).

### 3.3 IPv4: addressing, forwarding, and routing realities
- Fields that matter for security: TTL (traceroute + TTL-based host detection), identification/flags/offset (fragmentation — used to evade naive inspection; PMTUD black holes), ToS/DSCP (later: QoS abuse is rare, classification useful).
- Forwarding: longest-prefix match; the default gateway is a single point of trust; source-address validation is *not* native → spoofed sources possible on many networks (sets up reflection/amplification in L08 and BCP 38 in L12).
- Routing fundamentals: static routes vs dynamic protocols (RIP/OSPF/BGP at orientation level); routers exchange *trust* about reachability — the security implication is route injection and poisoning.
- Routing protocol security notes (orientation): OSPF supports per-area authentication (cleartext legacy → MD5/HMAC modern); unauthenticated IGP adjacency lets an attacker become a router (rogue routing announcements); BGP relies on operator hygiene (RPKI/origin validation as the structural fix — mentioned, not tested).
- Design consequence carried into L09/L12: routing decides *where policy can attach*; you cannot firewall traffic your routing never sends through the policy point.

### 3.4 IPv6 security deltas (orientation level)
- NDP replaces ARP with ICMPv6 types 135/136 — still spoofable without SEND (RFC 3971, rarely deployed); RA guard / ND inspection are the switch-side defenses.
- SLAAC means hosts self-configure → rogue RA (fake router) is the IPv6 analog of rogue DHCP (L03).
- Dual-stack reality: networks are attacked on the stack people forgot to secure; monitor both.

### 3.5 ICMP: diagnostic tool and attack surface
- Useful: echo request/reply, TTL exceeded (traceroute), destination unreachable (PMTUD).
- Abusable: echo flood, smurf-class reflection (historical), redirect forgery, type-3 scanning inferences (port unreachable vs admin-prohibited distinctions).
- Policy discussion: filtering all ICMP breaks PMTUD; rate-limit and classify instead (preview of L10/L11 rule design).

## 4. Teaching Sequence (120 Minutes)

| Time | Segment | Instructor moves |
|---|---|---|
| 0–10 | Recap quiz (oral): CIA + vantage points | 5 rapid questions; correct the "switches fix everything" misconception early |
| 10–35 | Core: Ethernet + switch learning | Frame dissection on projector (Wireshark byte view); CAM-table demo with 2 VMs |
| 35–55 | Core: ARP walk-through | Whiteboard the who-has/is-at exchange; annotate the exact packet fields; plant the "no authentication" observation |
| 55–65 | Break | — |
| 65–85 | Core: IPv4 fields + IPv6 deltas | Fragmentation demo (oversized ping, `ping -l` / `-s` variants); NDP vs ARP side-by-side capture |
| 85–110 | Guided lab: capture & annotate | Students capture ARP + ICMP between two VMs, fill the frame-map worksheet (cs-003/004/005 prep) |
| 110–120 | Wrap + formative | Exit ticket; preview: "next week the same lens on TCP/DNS/DHCP" |

## 5. Technical Examples

```
# Generate a normal ARP exchange between two lab VMs, then observe:
ping -c 3 10.0.0.20
# In Wireshark: filter 'arp' → identify request (opcode 1) vs reply (opcode 2),
# sender/target MAC+IP fields; note the reply is accepted WITHOUT any prior request
# (send a gratuitous-looking reply with nemesis/scapy in the L06 lab, not today).

# Fragmentation visibility:
ping -s 2000 -M do 10.0.0.20        # expect: message too long / frag needed path
ping -s 2000                        # expect: fragments; inspect ip.flags, ip.off in capture

# ICMP classification (inbound on a test VM):
ping -c 1 10.0.0.20                  # echo request/reply (types 8/0)
traceroute 10.0.0.20                 # TTL exceeded (type 11) from intermediate hops
```
Expected teaching points: reply accepted unsolicited; fragment offsets visible; type-11 reveals path — same packets an attacker uses for mapping (L05/L06).

## 6. Discussion Questions

1. Ethernet's FCS detects bit errors. Why is that not integrity protection in the security sense?
2. If ARP replies must be authenticated, what would a minimal fix look like, and what would it cost? (Compare to NDP SEND.)
3. A junior admin proposes blocking all ICMP at the border. What legitimate protocols break, and what does the attacker still see?
4. Your network is dual-stack but monitoring only sees IPv4. Construct a concrete blind-spot scenario.
5. Why does longest-prefix-match forwarding make spoofed sources hard to stop at the destination edge?

## 7. Student Activity

**Frame-map worksheet (25 min, pairs):** from the staged capture, each pair completes a field map for one ARP exchange, one fragmented ICMP exchange, and one IPv6 NDP exchange; they must label, for each packet, (a) which fields are authenticated (answer: none), (b) which single field a manipulator would change to cause harm, and (c) which L06 attack that change enables. Pairs swap worksheets and peer-review.

## 8. Problem-Solving Case

**Primary case — cs-004 "IP fragmentation anomaly in a routed capture" (beginner):**
A helpdesk ticket reports intermittent failures loading one internal reporting site; everything else works. The provided capture (lab-generated) shows large packets from the server reaching clients but small ones succeeding where large ones fail; there are ICMP type-3 code-4 (fragmentation needed) messages that are never acted upon. Students must explain the PMTUD failure chain, identify which device silently drops ICMP, and propose two fixes (allow frag-needed; lower MSS on the path).
**Linked cases:** cs-003 (abnormal ARP replies), cs-005 (ICMP misuse red flags).
*(Model solutions live in the instructor answer-key set — Module 1.)*

## 9. Formative Assessment

1. Which ARP packet field pair would a spoofer alter, and what is the attack called?
2. Why is an Ethernet FCS not a security control?
3. Name two IPv6 mechanisms that replace IPv4-era behaviors and one new risk each introduces.
4. In the fragmentation demo, why did the "do not fragment" ping fail while the second ping split?
5. Give one ICMP type that is diagnostically valuable and one that is mostly attack-relevant.
*(Answer key: instructor set, Module 1.)*

## 10. Summary & Key Takeaways

- Ethernet/ARP/IP/ICMP are *trust-by-construction*: none authenticate their key fields.
- Switches forward; they do not verify intent. CAM/ARP table manipulation is native behavior abuse.
- IPv6 changes the mechanism (NDP/RA), not the trust model — secure and monitor both stacks.
- Every field students read today becomes a detection field in Module 6 and evidence in Module 8.

## 11. References

- RFC 826 — ARP; RFC 791 — IPv4; RFC 792 — ICMP; RFC 1191 — Path MTU Discovery.
- RFC 4861 — IPv6 Neighbor Discovery; RFC 3971 — SEND; RFC 8200 — IPv6 specification.
- Wireshark User's Guide (capture/display filters) — current edition.
- Stallings, *Cryptography and Network Security* / *Data and Computer Communications* — relevant protocol chapters.
- Kurose & Ross, *Computer Networking: A Top-Down Approach* — network-layer chapter.

## 12. CLO Mapping

| CLO | Where in this lecture | Assessed via |
|---|---|---|
| CLO-1 | §3.1–3.5 protocol mechanics + worksheet §7 dissection skill | Quiz 1 (W2), Lab-01/Lab-02, Midterm |
