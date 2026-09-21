---
lecture: L03
title: Protocol Deep Dive II — TCP, UDP, DNS, DHCP
module: 1
week: 2
hours: 2
clos: [CLO-1]
difficulty: beginner
status: complete
artifact-type: student-lecture-material
instructor-plan: modules/module-01-network-foundations/lectures/lecture-03-protocol-deep-dive-ii-transport-services.md
---

# L03 — Protocol Deep Dive II — TCP, UDP, DNS, DHCP

## 1. Learning Objectives

By the end of this session you can: (1) narrate the TCP connection lifecycle and read flags/sequence numbers as a *story*; (2) contrast TCP's reliability with UDP's datagram model and their security consequences; (3) trace DNS resolution and identify the trust weaknesses of plain UDP/53; (4) walk the DHCP DORA exchange and explain rogue-server risk; (5) distinguish normal service behavior from anomalies in a capture.

## 2. Key Definitions

| Term | Definition |
|---|---|
| Three-way handshake | SYN → SYN/ACK → ACK; establishes sequence sync + state |
| Half-open connection | SYN received, handshake never completed (backlog state) |
| Ephemeral port | Client-side temporary port (OS-dependent range, e.g., 49152–65535) |
| Recursive resolver | DNS server that performs full resolution on behalf of a client |
| NXDOMAIN | "Non-existent domain" response; volume of these is a detection signal |
| DORA | DHCP Discover → Offer → Request → Ack lease sequence |
| TXID | DNS 16-bit transaction ID — historically a spoof-guessing target |
| TTL (DNS) | Cache lifetime of a record; behavioral signal in analytics |

## 3. Detailed Explanations

### 3.1 TCP: connections you can read like a story
The handshake (SYN → SYN/ACK → ACK) synchronizes initial sequence numbers and allocates state on both ends. Every subsequent segment carries sequence/acknowledgment numbers — a *narrative* an analyst can follow in Wireshark ("Follow TCP Stream"). Flags are detection gold: **SYN without completion** = scan or SYN flood (L08's mechanism: the server's half-open backlog fills); **RST storms** = refused service or port-scan responses; **PSH bursts** = bulk push patterns. Teardown is FIN/ACK pairs (polite) vs unilateral RST. Ports: 0–1023 well-known, ephemeral above — NAT interactions arrive in L12.

### 3.2 UDP: no handshake, no mercy
UDP is connectionless: no handshake, no congestion control, and the *source address is taken on faith* — which is precisely what enables **reflection/amplification attacks** (L08): send a small request with a spoofed source, the server's larger response goes to the victim. DNS, NTP, and memcached have all served as amplifiers. Where UDP is right (DNS, DHCP, VoIP, gaming), the *application* must provide any reliability/authentication it needs — DNS later gains DNSSEC/DoT/DoH; today, know the gap.

### 3.3 DNS: the internet's address book is a trust oracle
Resolution path: stub → recursive resolver → root/TLD/authoritative, with caching governed by TTL. Records you will meet constantly: A/AAAA, CNAME, MX, NS, PTR, TXT (TXT is tunneling bait — L23). The core weakness: a UDP response is accepted when its **5-tuple + 16-bit TXID** match an outstanding query — an off-path attacker must guess the TXID and the resolver's source port (port randomization raised the bar; Kaminsky-class cache poisoning drove that hardening). Modern layers: **DNSSEC** (cryptographic chain of trust on records), **DoT/DoH** (encryption of the query path — privacy gained, network visibility changed: L23's hunts shift from payload to metadata). Detection value today: NXDOMAIN ratios, query entropy, beacon-like cadence.

### 3.4 DHCP: configuring hosts by shouting
DORA: client broadcasts **Discover**; servers reply **Offer** (IP + options); client **Requests** the chosen offer; server **Acks** (lease). Options carry the gateway, DNS servers, domain — and, abused, everything an attacker needs to become the on-path position (rogue DHCP). The lease flow is unauthenticated: an OFFER is trusted because it arrived. Second attack class: **starvation** (request many leases → pool exhaustion → availability + attacker-controlled addressing). Switch-side DHCP snooping (trust only uplink ports for server messages) is the standard control — L06/L12.

### 3.5 Reading a service baseline (the analyst's habit)
Normal: one DORA per boot; DNS TTLs ≥ 300s for stable domains; every SYN answered by SYN/ACK. Anomalies: multiple OFFERs for one Discover; short-TTL churn; NXDOMAIN floods; SYN backlog growth; RST from a host that should answer. **You can only find anomalies against a baseline** — this habit is formalized in L21–L23.

## 4. Network Diagram: DNS resolution + DHCP lease

```
 Client                 Recursive resolver              Root/TLD/Auth
   |--[1] www.example.edu? -->|                            |
   |                         |--[2] ask root/TLD/Auth --->|
   |                         |<--[3] answers (cached)  ---|
   |<--[4] A 203.0.113.10 ----|     (5-tuple + TXID match = "auth")

 Client                          DHCP server
   |--Discover (broadcast)--------->|
   |<--------Offer (IP, gw, DNS)----|
   |--Request---------------------->|
   |<-----------------------------Ack (lease)
```

## 5. Protocol Examples

- `dig +trace www.example.edu` — watch stub → root → TLD → authoritative; note who answers authoritatively.
- `dig example.edu +norecurse @resolver` — recursion flag difference made visible.
- Capture filter `port 67 or port 68` — watch DORA live on the lab segment; note the transaction ID and option fields (router = the MITM-critical option).

## 6. Configuration Concepts (concept level)

- **DHCP snooping**: mark trusted (uplink) ports; untrusted ports may not send OFFER/ACK.
- **Resolver hardening**: source-port randomization on; response validation (bailiwick) enforced; DNSSEC validation enabled.
- **Lease logging**: DHCP logs are your IP→host inventory (L21) and your identity glue in forensics (L29).

## 7. Security Implications

- TCP gives you a readable narrative; UDP gives spoofable datagrams — attack patterns follow from this.
- DNS/DHCP are unauthenticated by default; their *hardening* is later-week content, their *weaknesses* are today's takeaway.
- Every L07–L08 attack (MITM, starvation, amplification) is a direct abuse of today's mechanics.

## 8. Realistic Organizational Scenario

**The university lab (running case).** Thirty lab machines intermittently resolve the library catalog to a wrong internal address for ~10 minutes. A capture shows an authoritative-looking answer arriving at the resolver with a plausible TXID, followed by clients receiving the wrong A record. Questions you can now ask: what two values must an off-path attacker guess? What does a 300-second TTL do to the blast radius? Which three mitigations layer best (randomization checks, bailiwick/response validation, DNSSEC)? This is **case cs-007**.

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "TCP sequence numbers prevent injection" | Only against off-path guessing of unauthenticated ISNs; on-path injection always works — hence encryption. |
| "DNS is just name lookup" | It is an unauthenticated trust oracle; cache poisoning redirects *everything* downstream. |
| "DHCP is harmless because it's local" | Rogue options = full MITM; starvation = outage. |
| "A short DNS TTL is suspicious" | CDNs legitimately use short TTLs; context beats rules. |
| "Multiple DHCP OFFERs are always rogue" | Overlapping scopes/misconfig also produce them — investigate before accusing. |

## 10. Classroom Activities

1. **Anomaly hunt (pairs):** the staged capture contains three planted faults (odd DNS TTL pattern, second OFFER, half-open SYNs). Find all three; cite frame numbers; write the user-visible symptom each would cause.
2. **dig trace race:** two teams race to map resolution steps from `dig +trace` output.
3. **Flags flashcards:** instructor shows a TCP flag byte; teams call the handshake state.

## 11. Problem-Solving Questions

1. Your SOC sees a workstation querying 400 random subdomains of one zone in 10 minutes. Give two hypotheses and one discriminating test each.
2. Why does DHCP snooping trust uplink ports, and what happens if that trust is misconfigured?
3. An answer arrives for a query nobody sent. Is that necessarily an attack? Justify.
4. Give one symptom each for: SYN backlog exhaustion, rogue DHCP, NXDOMAIN flood — and the protocol evidence behind each.
5. The campus moves DNS fully to DoH/DoT. What visibility does the defender lose, and which compensating controls replace it?

## 12. Exit Ticket

1. Draw the TCP handshake and label which end allocates what state.
2. Why is UDP/53 spoofable? Name the two values an off-path attacker must guess.
3. Which single DHCP option value turns a rogue server into a full MITM?
4. Give the DNS record type most abused for tunneling.
5. Name one baseline property and one anomaly signal for DHCP.

*(Answers: `teaching/answer-keys/answer-key-module-01.md`.)*

## 13. References

- RFC 9293 (TCP, obsoletes 793); RFC 768 (UDP).
- RFC 1034/1035 (DNS); RFC 5452 (DNS resilience); RFC 7626 (DNS privacy).
- RFC 2131/2132 (DHCP core and options).
- Zeek documentation — dns.log/dhcp.log field reference (L23 preview).
- Kurose & Ross — transport and application chapters.

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-1 | §3 mechanics + anomaly-reading skill | Quiz 1 (W2), Lab-02, Midterm |
