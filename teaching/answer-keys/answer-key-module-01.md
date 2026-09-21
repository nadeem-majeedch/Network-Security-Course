---
module: 1
lectures: [L01, L02, L03, L04]
status: complete
artifact-type: answer-key
instructor-only: true
distribution: never-publish-to-students
---

# Answer Key — Module 1: Network Foundations & Analysis

> **INSTRUCTOR ONLY — contains model answers to graded formative assessments.**
> Links: Plans `modules/module-01-network-foundations/lectures/` · Student pages `docs/lectures/lecture-01…04` · Notes `teaching/speaker-notes/lecture-01…04-speaker-notes.md`

## L01 — Security Mindset & Threat Landscape

### Formative checks (plan §11)
1. **CIA mapping:** Patient records (confidentiality); sensor/monitoring feeds (integrity); 999-call taking and dispatch (availability). Accept any correctly-reasoned mapping with a one-line justification — penalize "integrity" used loosely for "quality".
2. **Threat/vulnerability/impact:** Unpatched VPN gateway (vulnerability) + ransomware crew targeting VPNs (threat) + encrypted file servers (impact). The exploit chain is the sentence connecting them.
3. **Defense-in-depth:** at least three distinct controls on different assumptions (e.g., patch management, MFA, segmented backups, monitoring) — one control named twice doesn't count.
4. **Asset first:** "What are we protecting, and what does its loss cost?" — reject answers that begin with tools.
5. **Ethics boundary:** scanning only systems you own or have written authorization to test; the lab rules sheet embodies it.

### Exit ticket (expected answers)
- The missing control is almost always **availability** — accept disk encryption (C), least-privilege (C), DLP (C) as reasonable answers if justified.
- Lab rules: authorization boundary + no out-of-scope targets; "written permission from the system owner" is the gold-standard phrasing.

### Discussion facilitation (Q1–Q5)
- Q2 (hospital): elicit that detection/response capacity is what converts a breach into a *managed* incident.
- Q3 (budget argument): strongest answer frames security spend as downtime/loss-avoidance economics with the incident-cost curve.
- Q5 (ethics): accept "curiosity" and "career" as normal motivations; the line is *authorization*, and every later lab enforces it.

## L02 — Protocol Deep Dive I

### Formative checks
1. Frame anatomy: dst MAC (6 B) + src MAC (6 B) + EtherType (2 B) → 0x0800 is IPv4, 0x86DD is IPv6. The trailer question (FCS) is optional depth.
2. ARP request is **broadcast** (ff:ff:ff:ff:ff:ff); reply is **unicast** — and gratuitous ARP is unsolicited and cache-updating (spoofing relevance).
3. IPv6 advantages: 128-bit space, no broadcast, SLAAC, built-in ICMPv6 roles (NDP/RA); the removal of NAT-as-security is a common wrong claim — NAT was never a security control.
4. Hop limit: decremented by every router; at 0 the packet is dropped and ICMPv6/ICMP Time Exceeded returned (traceroute's mechanism).
5. `tcpdump -e` shows the link-layer header (MACs); add `-v` for TTL/hop-limit visibility.

### Routing fundamentals (added subsection — assess these)
- Static vs dynamic: static = configured, predictable, no protocol exposure but no adaptation; dynamic = learned, adapts, but introduces protocol attack surface.
- Routing protocol security: neighbor authentication (e.g., OSPF/OSPFv3 authentication, RIPv2 digest), passive interfaces, prefix filtering. Accept "authenticate neighbors and filter what you advertise/accept" as the core.
- Policy-attachment consequence: a routing policy pointing to a dead/misconfigured path blackholes traffic — same failure shape as a bad ACL (deny-all by accident).

### Exit ticket
- Spoofing is cheap at L2 because ARP trusts unsolicited replies — the trust gap is the answer, not "Ethernet is old".
- Static route with wrong next hop: traffic blackholes at that router; diagnosis: `traceroute` stops there.

## L03 — Protocol Deep Dive II

### Formative checks
1. Handshake: SYN → SYN/ACK → ACK. Second ACK carries the first data; sequence numbers are per-direction. Reject "three SYNs".
2. RST vs FIN: FIN is the orderly close (both sides finish); RST aborts immediately — and often signals "no such port" (scan-value: closed ports answer RST).
3. DNS: recursive resolver does the legwork *for* the stub; each query's RD flag distinguishes them. DNS uses UDP/53 first, TCP/53 on truncation (TC flag) or zone transfer.
4. DHCP: Discover (broadcast) → Offer → Request → ACK (DORA); lease renewal unicast. DHCP snooping is the L2 trust-boundary control (forward-look to L06/L12).
5. Wireshark display filters vs capture filters — `tcp.port == 443` (display) vs `port 443` (capture, BPF); the three-way handshake filter is `tcp.flags.syn == 1 && tcp.flags.ack == 0`.

### Exit ticket
- The key identifiers: src/dst IP + ports + protocol; reject "MAC address" (changes per hop, and NAT rewrites IPs).
- Sequence numbering answers the "duplicate/reorder" question: TCP reassembles by seq — cache it; it returns in L23 reassembly and L29 forensics.

## L04 — Applied Packet Analysis

### Formative checks
1. HTTP/1.1 vs /2: text headers vs binary HPACK-framed streams and multiplexing over one connection; HTTP/2 obsoletes naive "one TCP connection per object" reasoning.
2. Unencrypted path: every middlebox (proxy, IDS, ISP) sees it; SNI/hostname even in TLS 1.2 — encrypted DNS/ECH reduce but don't remove all metadata (forward-look to L14).
3. TLS handshake markers: ClientHello/ServerHello/Certificate/Finished; in TLS 1.3 the visible round-trip shrinks and the cert is encrypted — a favorite misconception-catcher.
4. HTTP status families: 2xx success, 3xx redirect, 4xx client error, 5xx server error; 401 vs 403 (authentication vs authorization — the distinction returns in L13's E-A-I framework).
5. Content-Length vs chunked: length-known upfront vs streaming chunks terminated by a zero-length chunk — parsing assumptions differ.

### Exit ticket
- Reassembly artifacts: overlapping segments, out-of-order delivery, retransmissions with *different* payloads — tools may disagree; the analyst answers "why".
- Evidence checklist: full bidirectional stream, request *and* response headers, timing, and the completeness caveat (any missing packets are stated, never assumed).

## Case study anchors (cs-001–cs-014) — grading pointers
- **cs-001/002/003 (L01):** reward asset-first reasoning; penalize tool-first.
- **cs-004–cs-010 (L02/L03):** the mechanism must be protocol-accurate (e.g., "attacker answers ARP" not "hacks the switch").
- **cs-011–cs-014 (L04):** full-credit analysis names the exact fields observed and the confidence limits (missing packets, retransmission ambiguity).

## Common misconceptions to correct on record (module-level)
1. "Encryption = security" — encryption without authentication/integrity is bypassable (L13 dismantles this properly; Module 1 only plants the seed).
2. "NAT is a firewall" — stateful filtering and NAT are different functions that often cohabit a box (L12 revisits).
3. "HTTPS means the site is safe" — TLS authenticates transport, not content or intent (L14 revisits).
4. "IPv6 has no ARP" — correct at the name level, but NDP replaces it and has its own trust issues (RA guard, etc.).
