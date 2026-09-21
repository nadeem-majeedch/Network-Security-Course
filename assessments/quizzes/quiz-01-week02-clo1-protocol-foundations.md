---
quiz: quiz-01
week: 2
type: graded
clos: [CLO-1]
lectures: [L01, L02, L03]
marks: 15
duration: 20 min
bloom-range: Remember–Apply
status: complete
artifact-type: student-quiz
answer-key: instructor/answer-keys/quiz-01-answer-key.md
---

# Quiz 1 — Protocol Foundations (Week 2, Graded)

> 20 minutes · 15 marks · CLO-1 · covers L01–L03.
> Answer all questions. State assumptions where a question is open-ended.

## Section A — Multiple Choice (5 × 1 = 5 marks)

**Q1.** A switch forwards a frame using which header field?

A. Source IP address
B. Destination MAC address
C. TCP port number
D. ARP opcode

*Bloom: Remember · CLO-1 · 1 mark*

**Q2.** During a TCP three-way handshake, the correct flag sequence is:

A. SYN → ACK → SYN-ACK
B. SYN → SYN-ACK → ACK
C. SYN → ACK → FIN
D. SYN → ACK → ACK

*Bloom: Remember · CLO-1 · 1 mark*

**Q3.** A host sends an ARP request for its default gateway. The request is:

A. Unicast to the gateway
B. Multicast to 224.0.0.1
C. Broadcast on the local segment
D. Forwarded to the destination by the router

*Bloom: Understand · CLO-1 · 1 mark*

**Q4.** Which statement about UDP is correct?

A. UDP guarantees delivery through retransmission
B. UDP provides flow control via windowing
C. UDP is connectionless with no delivery guarantee
D. UDP establishes a session before data transfer

*Bloom: Understand · CLO-1 · 1 mark*

**Q5.** The Time-To-Live field in an IP header primarily prevents:

A. Packet fragmentation
B. Routing loops
C. ARP cache poisoning
D. TCP half-open connections

*Bloom: Understand · CLO-1 · 1 mark*

## Section B — Short Answer (2 × 3 = 6 marks)

**Q6.** In one sentence each, state what the **confidentiality**, **integrity**, and **availability** members of the CIA triad protect against. *(Bloom: Remember · CLO-1 · 3 marks)*

**Q7.** A TCP connection is closing. Explain, in 2–3 sentences, why a **RST** differs from a normal **FIN** exchange, and what a RST from a port you did *not* contact usually indicates during reconnaissance. *(Bloom: Understand · CLO-1 · 3 marks)*

## Section C — Packet Interpretation (4 marks)

**Q8.** A capture shows: `ARP Reply: 10.0.5.1 is-at aa:bb:cc:00:11:22`, followed 40 seconds later by an unsolicited second reply: `10.0.5.1 is-at aa:bb:cc:00:11:99` from a different MAC.

(a) Name the protocol behavior being abused. *(1 mark)*
(b) State which host table entry changes and the impact on traffic to 10.0.5.1. *(1 mark)*
(c) Name one switch feature or host-side control that mitigates it. *(2 marks)*

*Bloom: Apply · CLO-1 · 4 marks*

**Total: 15 marks**
