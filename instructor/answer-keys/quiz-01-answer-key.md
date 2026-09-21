---
quiz: quiz-01
type: answer-key
instructor-only: true
distribution: never-publish-to-students
clos: [CLO-1]
marks: 15
status: complete
---

# Answer Key — Quiz 1 (Protocol Foundations)

> **INSTRUCTOR ONLY.** Answers verified against L01–L03 teaching plans and
> standard protocol specifications (IEEE 802.1, RFC 9260-era TCP behavior,
> RFC 826 ARP).

## Section A — MCQ

| Q | Answer | Justification (one line) |
|---|---|---|
| 1 | **B** | L2 switching uses destination MAC; source IP and ports are L3/L4; ARP opcode is protocol metadata. |
| 2 | **B** | SYN → SYN-ACK → ACK is the handshake; distractors reorder flags or mix in FIN. |
| 3 | **C** | ARP requests are link-layer broadcast on the local segment; routers do not forward them. |
| 4 | **C** | UDP is connectionless, no delivery guarantee; retransmission/windowing are TCP features. |
| 5 | **B** | TTL decrements per hop and drops the packet at 0 — loop containment. |

**Section A total: 5**

## Section B — Short answer (model answers)

**Q6 (3 marks — 1 per element).** Confidentiality: data is readable only by
authorized parties (protects against eavesdropping/disclosure). Integrity:
data is not altered in transit or at rest without detection (protects against
tampering). Availability: systems and services remain usable when needed
(protects against outage/DoS).
*Grading note: award full credit only if all three are tied to the right
protection goal; examples optional.*

**Q7 (3 marks).** A FIN closes the connection cooperatively after data
transfer (4-way, both sides finish). A RST aborts immediately — sent when a
segment arrives for a port with no listening socket, or when a session is
abnormally terminated. During reconnaissance, a RST from a port you did not
contact indicates the host is *rejecting* unexpected traffic — commonly the
signature of a scan response or an in-flight spoofed/unsolicited probe.
*Grading: 1 mark cooperative-close vs abort; 1 mark no-socket/reject
meaning; 1 mark recon interpretation.*

## Section C — Packet interpretation

**Q8.**
(a) **Gratuitous/unsolicited ARP replies** enabling ARP cache poisoning
(ARP spoofing). *(1)*
(b) The gateway entry for 10.0.5.1 in victims' ARP caches now maps to
attacker MAC `…:99`; traffic to the gateway is redirected through the
attacker (interception/MITM position). *(1)*
(c) **Dynamic ARP Inspection** (switch validates ARP against a binding
database) — full credit also for DAI precursor DHCP snooping, or static
ARP entries on critical hosts. *(2)*

**Total: 15**

## Grading notes

- Section C: partial credit 1 mark for naming the feature without binding it
  to the attack (e.g., "port security" alone — related but not the ARP fix —
  earns 1 of 2).
- If ≥60% of the class misses Q5, revisit TTL/loop behavior at the start of
  L04 (per instructor manual accessibility guidance).
