---
lecture: L02
title: Protocol Deep Dive I — Ethernet, ARP, IP, ICMP
module: 1
week: 1
hours: 2
clos: [CLO-1]
difficulty: beginner
status: complete
artifact-type: student-lecture-material
instructor-plan: modules/module-01-network-foundations/lectures/lecture-02-protocol-deep-dive-i-lower-layers.md
---

# L02 — Protocol Deep Dive I — Ethernet, ARP, IP, ICMP

## 1. Learning Objectives

By the end of this session you can: (1) dissect an Ethernet frame and say which fields are *trusted* and why that is a security problem; (2) narrate the ARP exchange and identify its missing authentication; (3) explain IPv4 forwarding and the IPv6 deltas (NDP, SLAAC) at security-relevant depth; (4) classify ICMP messages by diagnostic value vs abuse potential.

## 2. Key Definitions

| Term | Definition |
|---|---|
| Frame | Layer-2 PDU: dst/src MAC + EtherType + payload + FCS |
| CAM table | Switch's MAC→port learning table (built from observed *source* MACs) |
| ARP cache | IP→MAC mapping table on hosts; entries age out; replies may be unsolicited |
| Broadcast domain | Set of hosts that receive each other's broadcasts (one VLAN/segment) |
| NDP | IPv6 Neighbor Discovery (ICMPv6 types 135/136) — ARP's IPv6 replacement |
| SLAAC | Stateless Address Auto Configuration — hosts self-configure from Router Advertisements |
| PMTUD | Path MTU Discovery — uses ICMP "fragmentation needed" to avoid black-hole drops |

## 3. Detailed Explanations

### 3.1 Ethernet: a frame that trusts its sender
An Ethernet II frame carries destination MAC, source MAC, EtherType (what's inside — IPv4? 0x0800; ARP? 0x0806), payload, and a Frame Check Sequence. The **FCS detects bit errors, not tampering** — there is no authenticity: any host can *claim* any source MAC. Switches *learn* by reading source MACs of arriving frames into the CAM table and forward based on destination. Two consequences: (1) a host flooding fake source MACs can fill the CAM table (MAC flooding — L06), and (2) within a broadcast domain, every host receives broadcast traffic — the foundation of on-link sniffing (L07).

### 3.2 ARP: resolution without authentication
To send IP traffic on a LAN, a host needs the MAC for an IP: it broadcasts "who-has 10.0.0.5? tell 10.0.0.9" (opcode 1) and the owner replies "10.0.0.5 is-at aa:bb:cc:dd:ee:ff" (opcode 2). The reply is processed **even without a matching request** (gratuitous ARP is a legitimate use of this). No field is authenticated, no request↔reply correlation is enforced, and caches accept updates — so any host can *claim* any IP by sending crafted replies. This is the exact mechanism of ARP spoofing (L06): the attacker becomes the on-path position for a victim's traffic. Switch-side defenses (Dynamic ARP Inspection, DHCP snooping bindings) arrive in Module 3.

### 3.3 IPv4: addressing, forwarding, and routing realities
IPv4 delivers datagrams *best-effort*: no delivery guarantee, no ordering. Security-relevant header fields: **TTL** (decremented per hop — enables traceroute and TTL-based host fingerprinting), **Identification/Flags/Offset** (fragmentation — historically abused to evade naive inspection; PMTUD failures silently black-hole traffic, see case cs-004), **DSCP** (classification; rarely a security issue itself). Forwarding uses **longest-prefix match**: the router picks the most specific route. Crucially, **routers do not verify source addresses** — spoofed sources transit freely unless the network enforces source validation (BCP 38; your L12 lab).

### 3.4 Routing fundamentals (what Module 3 assumes)
Static routes are hand-configured; dynamic routing protocols (RIP, OSPF, BGP) let routers share reachability — an act of *trust*. Unauthenticated IGP adjacencies let an attacker inject routes (become a "better" path); OSPF supports authentication and it should be on; BGP depends on operator hygiene (RPKI origin validation is the structural fix). Design consequence you will use in Module 3: **you can only apply policy where routing sends traffic** — no firewall can inspect a path it never sees.

### 3.5 IPv6 deltas
IPv6 replaces ARP with **NDP** (ICMPv6) — which is *also* unauthenticated without SEND (RFC 3971, rarely deployed); the switch-side fixes are RA Guard and ND inspection. **SLAAC** lets hosts self-configure from Router Advertisements — so a **rogue RA** (fake router) is the IPv6 analog of a rogue DHCP server. Modern networks are dual-stack: attackers probe the stack you forgot to secure, and monitors must see both.

### 3.6 ICMP: diagnostics and abuse
Useful: echo request/reply (type 8/0 — ping), TTL exceeded (type 11 — traceroute), destination unreachable (type 3; code 4 = fragmentation needed — PMTUD). Abusable: echo floods, redirect forgery, and type-3-based scanning inferences. Policy lesson: blocking *all* ICMP breaks PMTUD — rate-limit and classify instead.

## 4. Network Diagram: ARP exchange on a segment

```
 Host A (10.0.0.9)                         Host B (10.0.0.5)
      |  [1] ARP request (broadcast)           |
      |  who-has 10.0.0.5? tell 10.0.0.9 --->  |
      |                                        |
      |  <--- [2] ARP reply (unicast)          |
      |      10.0.0.5 is-at AA:BB:CC:DD:EE:FF  |
      |                                        |
      |  [3] cache updated; IP traffic begins  |

 Attacker M (10.0.0.66) -- [2'] unsolicited reply:
      "10.0.0.5 is-at <M's MAC>"  --> accepted by A (no request check!)
```

## 5. Protocol Examples

- **Field walk (ARP request):** opcode=1, sender MAC/IP = A, target IP = 10.0.0.5, target MAC = 00:00:00:00:00:00 (unknown yet). The reply flips opcode to 2 and fills the target MAC.
- **Fragmentation:** `ping -s 2000 -M do` fails with "fragmentation needed" when the path MTU is 1500 — you just watched PMTUD work; drop that ICMP type and large transfers stall.

## 6. Configuration Concepts (concept level)

- **Port security** (switch): limit MACs per port — blunts CAM flooding.
- **RA Guard / ND inspection** (switch, IPv6): accept RAs/ND only from authorized ports.
- **Static ARP entries**: precise but unscalable — understand *why* before you propose them.

## 7. Security Implications

- Ethernet/ARP/NDP are **trust-by-construction**: no authentication on identity-critical fields.
- Switches forward; they do not verify intent — CAM/ARP manipulation is native behavior abuse.
- IPv6 changes the mechanism, not the trust model: secure and monitor both stacks.
- Every field you read today becomes a detection field (Module 6) and evidence (Module 8).

## 8. Realistic Organizational Scenario

A helpdesk ticket says a lab's printers intermittently become "unreachable." A capture shows ARP replies for the printer's IP coming from *two different MACs* seconds apart. Using §3.2 you can already hypothesize: either a legitimate failover pair (two NICs, shared IP) or ARP spoofing. The discriminator: does the second MAC also send unsolicited replies for *other* IPs? This is the reasoning chain behind **case cs-003** (abnormal ARP replies).

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "Switches make ARP attacks impossible" | Switches learn/forward; ARP processing happens *on hosts*. |
| "ICMP is evil; block it all" | You break PMTUD and diagnostics. Rate-limit + classify. |
| "IPv6 is just bigger addresses" | Different mechanisms (NDP/RA), same trust gaps, new attack surface. |
| "Ethernet FCS protects integrity" | It detects *corruption*, not tampering — no authenticity. |
| "Static ARP everywhere is a defense" | Unmanageable at scale; DAI + snooping is the real answer. |

## 10. Classroom Activities

1. **Frame-map worksheet (pairs):** from the lab capture, map one ARP exchange, one fragmented ping, one NDP exchange; mark which fields are authenticated (none) and which one field a manipulator would change.
2. **Field-guess drill:** instructor displays a frame's hex; teams identify EtherType, opcode, flags.
3. **ICMP triage:** sort 8 ICMP messages into "diagnostic value" vs "abuse potential" columns.

## 11. Problem-Solving Questions

1. Why is an ARP reply accepted without a request? Name one *legitimate* protocol behavior that relies on this.
2. A junior admin proposes blocking all ICMP at the border. What breaks, and what does an attacker still learn?
3. Construct the blind-spot scenario: network monitored for IPv4 only. Which L06 attack proceeds invisibly over IPv6?
4. Why does longest-prefix match make source spoofing hard to stop *at the destination edge* rather than at the source?
5. Two MACs claim one IP within seconds. List two innocent explanations and one malicious one, with a discriminator for each.

## 12. Exit Ticket

1. Which ARP fields would a spoofer alter, and what is the attack called?
2. Why is the Ethernet FCS not a security control?
3. Name one IPv6 mechanism that replaces an IPv4 behavior and one new risk it introduces.
4. In the fragmentation demo, why did the "don't fragment" ping fail while the second ping split?
5. Give one ICMP type of high diagnostic value and one that is mostly attack-relevant.

*(Answers: `teaching/answer-keys/answer-key-module-01.md`.)*

## 13. References

- RFC 826 (ARP); RFC 791 (IPv4); RFC 792 (ICMP); RFC 1191 (PMTUD).
- RFC 4861 (Neighbor Discovery); RFC 3971 (SEND); RFC 8200 (IPv6).
- Cisco documentation — Dynamic ARP Inspection, RA Guard (current editions).
- Kurose & Ross, *Computer Networking: A Top-Down Approach* — network-layer chapter.
- Wireshark User's Guide — Ethernet/ARP/ICMP dissections.

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-1 | §3 protocol mechanics; §5/§11 analysis skill | Quiz 1 (W2), Lab-01/02, Midterm |
