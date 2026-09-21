---
lecture: L03
title: Protocol Deep Dive II — TCP, UDP, DNS, DHCP
module: 1
week: 2
hours: 2
clos: [CLO-1]
difficulty: beginner
status: complete
artifact-type: teaching-plan
---

# L03 — Protocol Deep Dive II — TCP, UDP, DNS, DHCP (Teaching Plan)

## 1. Overview & Prerequisites

- **Prerequisites:** L02 (frame/ARP/IP mechanics; capture workflow).
- **Position:** transport + core services are where most enterprise traffic lives; L07 (session attacks), L21–L23 (monitoring), and L29–L30 (forensics) all read TCP streams and DNS/DHCP records.
- **Faculty prep:** prepare two staged captures — (a) a clean web/DHCP session, (b) one with planted anomalies (odd DNS TTLs, a second DHCP OFFER) — and verify they load on lab images.
- **Common misconceptions:** "TCP sequence numbers prevent injection"; "DNS is just name lookup"; "DHCP is harmless because it's local."

## 2. Learning Objectives

By the end of this lecture, students can:

1. Explain the TCP connection lifecycle (handshake, data transfer, teardown) and the role of sequence/acknowledgment numbers, flags, and ports (Understand).
2. Contrast TCP's reliability/ordering with UDP's datagram model and name security consequences of each (Analyze).
3. Describe recursive/iterative DNS resolution, record types (A, AAAA, CNAME, MX, PTR, TXT), caching/TTL, and identify trust weaknesses in plain UDP/53 (Understand/Analyze).
4. Trace the DHCP DORA exchange and identify the trust assumption that enables rogue servers and starvation attacks (Analyze).
5. Given a capture, recognize baseline service behavior vs anomalies in TCP handshake patterns, DNS responses, and DHCP exchanges (Analyze).

## 3. Detailed Concepts

### 3.1 TCP: connections you can read like a story
- 3-way handshake: SYN → SYN/ACK → ACK; initial sequence numbers; why half-open states exist (SYN backlog — mechanism for L08 SYN flood).
- Flags (SYN/ACK/FIN/RST/PSH/URG) as detection signals: SYN without completion, RST storms, PSH-burst exfiltration patterns.
- Teardown: FIN/ACK pairs vs unilateral RST; what a scanner's RST responses reveal about port state.
- Ports and sockets: 0–1023 well-known, ephemeral ranges; NAT implications preview (L12).

### 3.2 UDP: no handshake, no mercy
- Connectionless, no congestion control, spoofable source (sets up L08 reflection/amplification: DNS, NTP, memcached historically).
- Where UDP is right (DNS, DHCP, VoIP, gaming) and what the application must do itself (retransmit, authenticate — e.g., DNS later gains DNSSEC/DoT/DoH, L16 preview not required here).

### 3.3 DNS: the internet's address book is a trust oracle
- Resolution path: stub → recursive resolver → root/TLD/authoritative; caching and TTL; negative caching.
- Records: A/AAAA, CNAME, MX, NS, PTR, TXT (TXT abuse: tunneling preview for L23 detection).
- Trust weaknesses: UDP responses accepted on 5-tuple match + guessed 16-bit TXID; birthday-style forgery (Kaminsky-style cache poisoning mechanism); no port randomization historically → source-port randomization + 0x20 encoding as hardening; DNSSEC (chain of trust), DoT/DoH (encryption, privacy + visibility trade-off) — full treatment later, orientation today.
- Detection value: beaconing domains, DGA patterns, unusual query volumes — Zeek dns.log preview.

### 3.4 DHCP: configuring hosts by shouting
- DORA (Discover, Offer, Request, Ack); lease structure, options (router, DNS, domain, TFTP/PXE abuse potential).
- Trust gap: OFFERs/ACKs are unauthenticated → rogue DHCP (MITM via crafted gateway/DNS options) and DHCP starvation (pool exhaustion → availability + attacker-controlled addresses).
- Defenses preview: DHCP snooping, port-based controls (L06/L12).

### 3.5 Reading service baselines
- Normal: one DHCP DORA per boot; DNS TTLs ≥ 300 for stable domains; SYNs answered by SYN/ACK.
- Anomalies: multiple OFFERs, short-TTL churn, NXDOMAIN floods, SYN backlog growth, RST from a host that should answer.

## 4. Teaching Sequence (120 Minutes)

| Time | Segment | Instructor moves |
|---|---|---|
| 0–10 | Recap: L02 exit-ticket answers; frame quiz | Confirm ARP/NDP lessons stuck |
| 10–35 | Core: TCP lifecycle | Wireshark "Follow TCP Stream" live; annotate flags; show half-open scan vs normal connect |
| 35–50 | Core: UDP + reflection setup | Datagram anatomy; why spoofing works; name today's amplifiers (DNS/NTP/memcached) |
| 50–60 | Break | — |
| 60–85 | Core: DNS + DHCP | Live `dig` walk-through with +trace; DORA exchange on capture; plant the rogue-OFFER observation in capture (b) |
| 85–110 | Guided lab: trace analysis | Pairs analyze capture (b): find the planted DNS + DHCP anomalies, fill worksheet (cs-006/007/008 prep) |
| 110–120 | Wrap + formative | Exit ticket; Quiz-1 reminder (end of class); preview L04: "you now own the protocols — next we make you fast with the tool" |

## 5. Technical Examples

```
# TCP lifecycle visibility
curl -s http://10.0.0.30/ >/dev/null          # then in Wireshark: tcp.stream eq N
tcpdump -i eth0 -nn 'tcp[tcpflags] & (tcp-syn|tcp-ack) != 0'

# DNS resolution mechanics
dig +trace www.example.edu                     # observe root → TLD → authoritative chain
dig www.example.edu +norecurse @10.0.0.53      # recursive vs iterative difference
dig -x 10.0.0.30                               # PTR lookup

# DHCP DORA capture on the lab segment
sudo tcpdump -i eth0 -nn -e port 67 or port 68
# Expected: Discover(0.0.0.0→255.255.255.255) → Offer → Request → Ack; note xid
```
Teaching points: 5-tuple + TXID is DNS's entire "authentication"; DHCP xid is not a security token.

## 6. Discussion Questions

1. Why can an off-path attacker inject into a TCP stream only under specific conditions (predictable ISN), while an on-path attacker can always do it? What does that imply about encryption?
2. Your SOC sees a workstation querying 400 random subdomains of one zone in 10 minutes. Give two hypotheses and one discriminating test for each.
3. Why does DHCP snooping trust "uplink" ports? What happens if that trust is misconfigured?
4. How would you detect a rogue DHCP server without any security tooling — just standard utilities?
5. If a campus moves DNS entirely to DoH/DoT, what visibility does the defender lose and what compensating controls replace it?

## 7. Student Activity

**Anomaly hunt (25 min, pairs):** capture (b) contains three planted faults. Each pair locates all three, writes the evidence line (frame number + field values) for each, and drafts a one-sentence user-visible symptom each would cause. Instructor ledgers common wrong answers: e.g., treating short DNS TTL as always malicious (CDNs do it legitimately — teach context).

## 8. Problem-Solving Case

**Primary case — cs-007 "DNS resolution misdirection symptoms" (beginner):**
A lab of 30 machines intermittently resolves the library catalog to a wrong internal address for ~10 minutes at a time. The capture shows an authoritative-looking response for the catalog name arriving to the resolver with a plausible TXID and a 300-second TTL, followed by clients getting the wrong A record. Students must (a) explain which trust property of UDP/53 failed, (b) compute what an attacker must predict to succeed, and (c) propose three layered mitigations (port/TXID randomization checks, response validation, DNSSEC deployment) and rank them by cost.
**Linked cases:** cs-006 (TCP half-open flood symptoms), cs-008 (rogue DHCP server effects).
*(Model solutions: instructor answer-key set, Module 1.)*

## 9. Formative Assessment

1. Draw the TCP handshake and label which end allocates what state.
2. Why is UDP/53 spoofable? Name the two values an off-path attacker must guess.
3. What single DHCP option value makes a rogue server a full MITM?
4. A DNS answer arrives for a query nobody sent. Is that necessarily an attack? Why/why not?
5. Give one symptom each for: SYN backlog exhaustion, rogue DHCP, NXDOMAIN flood.
*(Answer key: instructor set, Module 1.)*

## 10. Summary & Key Takeaways

- TCP gives you a readable narrative (handshake → stream → teardown); UDP gives you spoofable datagrams.
- DNS and DHCP are unauthenticated broadcast/trust services by default — their hardening (DNSSEC, DoT/DoH, snooping) is later-week content; their *weaknesses* are today's takeaway.
- Baseline-first analysis: you can only find anomalies against a known-normal service picture.

## 11. References

- RFC 9293 — TCP (obsoletes 793); RFC 768 — UDP.
- RFC 1034/1035 — DNS; RFC 2181 — DNS clarity; RFC 5452 — DNS resilience measures; RFC 7626 — DNS privacy considerations.
- RFC 2131 — DHCP; RFC 2132 — DHCP options.
- Zeek documentation — dns.log/dhcp.log field reference (preview of L23).
- Kurose & Ross — transport-layer and application-layer chapters.

## 12. CLO Mapping

| CLO | Where in this lecture | Assessed via |
|---|---|---|
| CLO-1 | §3.1–3.5 TCP/UDP/DNS/DHCP mechanics + anomaly-hunt skill | Quiz 1 (today, end of week), Lab-02, Midterm |
