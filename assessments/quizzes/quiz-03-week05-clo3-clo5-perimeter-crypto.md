---
quiz: quiz-03
week: 5
type: graded
clos: [CLO-3, CLO-5]
lectures: [L09, L10, L11, L12, L13]
marks: 15
duration: 20 min
bloom-range: Understand–Apply
status: complete
artifact-type: student-quiz
answer-key: instructor/answer-keys/quiz-03-answer-key.md
---

# Quiz 3 — Perimeter Controls & Crypto Foundations (Week 5, Graded)

> 20 minutes · 15 marks · CLO-3, CLO-5 · covers L09–L13.
> Answer all questions.

## Section A — Multiple Choice (5 × 1 = 5 marks)

**Q1.** A stateful firewall differs from a simple packet filter because it:

A. Encrypts allowed traffic
B. Tracks connection state and validates that reply traffic belongs to an established session
C. Inspects only layer-7 application payloads
D. Requires ACLs on every switch port

*Bloom: Understand · CLO-3 · 1 mark*

**Q2.** On Cisco-style extended ACLs, processing is:

A. Randomized for load distribution
B. First-match-wins from the top, with an implicit deny at the end
C. Last-match-wins from the bottom
D. Longest-prefix-match based

*Bloom: Remember · CLO-3 · 1 mark*

**Q3.** Which placement best reflects DMZ design?

A. Public services between two firewall layers, internal network behind the inner layer
B. Public services on the same segment as user workstations
C. Public services directly on the internet with host firewalls only
D. Public services behind the VPN concentrator

*Bloom: Apply · CLO-3 · 1 mark*

**Q4.** In symmetric cryptography, the same key:

A. Derives a public/private pair
B. Encrypts and decrypts the data
C. Only verifies signatures
D. Is always distributed via certificates

*Bloom: Remember · CLO-5 · 1 mark*

**Q5.** Hash functions in security are used to provide:

A. Confidentiality
B. Integrity verification
C. Non-repudiation by themselves
D. Key exchange

*Bloom: Understand · CLO-5 · 1 mark*

## Section B — Short Answer (2 × 3 = 6 marks)

**Q6.** Explain the difference between **encryption**, **authentication**,
and **integrity** protection in one sentence each, and name the property
that *hashing alone does not* provide. *(Bloom: Understand · CLO-5 · 3 marks)*

**Q7.** Why does a "default deny" egress ACL improve security posture even
when most traffic must still be allowed? Give two reasons tied to attacker
behavior. *(Bloom: Analyze · CLO-3 · 3 marks)*

## Section C — ACL Design (4 marks)

**Q8.** Write an ordered ACL (5 rules maximum, pseudocode accepted) for a
management VLAN `10.99.0.0/24` that must:
- allow SSH only from the admin jump host `10.99.0.10`,
- deny all other inbound management traffic,
- allow established session return traffic,
- log denied management attempts.

Label each rule's purpose. State *where* order matters. *(Bloom: Apply · CLO-3 · 4 marks)*

**Total: 15 marks**
