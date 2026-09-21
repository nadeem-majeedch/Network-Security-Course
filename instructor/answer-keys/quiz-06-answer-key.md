---
quiz: quiz-06
type: answer-key
instructor-only: true
distribution: never-publish-to-students
clos: [CLO-1]
marks: 10
status: complete
---

# Answer Key — Self-Check Quiz 6 (Week 1)

1. **A** — segment (L4) → packet (L3) → frame (L2).
2. **B** — a vulnerability is the weakness; the threat is the actor/event
   that may exploit it.
3. **A** — the standard qualitative composition: threat × vulnerability ×
   impact.
4. **B** — destination MAC selects the receiving NIC on the local link.
5. **C** — routers forward on IP destination + routing table; switches use
   MAC tables.
6. **(2)** Broadcast domain: one ARP/broadcast storm or L2 attack propagates
   to all members — its size drives sniffing/spoofing exposure. Collision
   domain: full-duplex switched links make collisions a non-issue today —
   the security-relevant point is that a switch port is its own collision
   domain, isolating physical-layer contention. *(1 per well-argued
   difference)*
7. **(2)** Primary impact: **confidentiality** (unreleased results exposed);
   second-order integrity/availability of the device. Justification must
   name the data exposure as primary.
8. **(2)** The two PCs share one broadcast domain (same switch, same VLAN);
   the router terminates that broadcast domain and is the L3 boundary to
   the internet.
