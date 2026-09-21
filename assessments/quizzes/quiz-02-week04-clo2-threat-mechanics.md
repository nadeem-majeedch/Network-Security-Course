---
quiz: quiz-02
week: 4
type: graded
clos: [CLO-2]
lectures: [L05, L06, L07, L08]
marks: 15
duration: 20 min
bloom-range: Remember–Analyze
status: complete
artifact-type: student-quiz
answer-key: instructor/answer-keys/quiz-02-answer-key.md
---

# Quiz 2 — Threat Mechanics (Week 4, Graded)

> 20 minutes · 15 marks · CLO-2 · covers L05–L08.
> Answer all questions.

## Section A — Multiple Choice (5 × 1 = 5 marks)

**Q1.** Which reconnaissance activity is *passive*?

A. ICMP echo sweep of a target subnet
B. Reading public DNS records and certificate transparency logs
C. TCP SYN scan of a web server
D. Traceroute toward the target network

*Bloom: Understand · CLO-2 · 1 mark*

**Q2.** MAC flooding attempts to compromise a switch by:

A. Exhausting the TCAM/MAC address table so the switch floods frames
B. Spoofing the default gateway's MAC address
C. Sending malformed 802.1Q tags
D. Flooding the ARP cache of end hosts

*Bloom: Understand · CLO-2 · 1 mark*

**Q3.** A DNS spoofing attack succeeds primarily because:

A. DNS over UDP uses encryption by default
B. The resolver accepts and caches an inauthentic response
C. DNS queries are always broadcast
D. Zone transfers are mandatory between servers

*Bloom: Understand · CLO-2 · 1 mark*

**Q4.** In a reflection/amplification DDoS, the attacker most relies on:

A. Services that reply larger than the request to a spoofed source
B. Encrypting the attack traffic
C. Slow TCP handshakes
D. IPv6 extension headers

*Bloom: Analyze · CLO-2 · 1 mark*

**Q5.** DHCP starvation harms clients mainly by:

A. Corrupting their DNS caches
B. Exhausting the address pool so legitimate clients get no lease
C. Forcing duplicate IP addresses on servers
D. Resetting the default gateway

*Bloom: Understand · CLO-2 · 1 mark*

## Section B — Short Answer (2 × 3 = 6 marks)

**Q6.** Distinguish **sniffing** in two contexts: (a) what an attacker gains
on a hub or wireless segment vs (b) a switched wired segment, and name one
control that limits each. *(Bloom: Analyze · CLO-2 · 3 marks)*

**Q7.** Explain why a **SYN flood** exhausts a target without the attacker
completing handshakes, and name two mitigation locations (host and
network). *(Bloom: Analyze · CLO-2 · 3 marks)*

## Section C — Scenario (4 marks)

**Q8.** Users report intermittent redirection of the intranet site to an
unknown server. Flow records show one workstation sending high-volume
traffic to the whole user VLAN.

(a) Name the two most likely Layer-2 attacks consistent with both symptoms. *(2 marks)*
(b) For each, give one piece of corroborating evidence you would look for in
switch logs or a packet capture. *(2 marks)*

*Bloom: Analyze · CLO-2 · 4 marks*

**Total: 15 marks**
