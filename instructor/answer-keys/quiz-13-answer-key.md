---
quiz: quiz-13
type: answer-key
instructor-only: true
distribution: never-publish-to-students
clos: [CLO-1, CLO-2, CLO-3, CLO-5]
marks: 10
status: complete
---

# Answer Key — Self-Check Quiz 13 (Midterm Preparation)

1. **A** — the week-3→5 progression: attack (ARP spoofing) → switch
   defense (DAI) → architectural defense (segmentation).
2. **B** — many distinct sources + unanswered SYNs = distributed SYN
   flood; reflection shows *replies* to the victim, not SYNs from many
   sources.
3. **A** — both enforce the perimeter/egress trust boundary; B mixes
   physical security, C mixes layers, D mixes domains.
4. **B** — "maintained" = operational lifecycle (automation + monitored
   expiry); A/D are good settings but don't prove maintenance; C is a
   key-size fact.
5. **A** — none/symmetric/asymmetric key usage is the differentiator.
6. **(2)** Most common class: **default-allow / shadow rules** (ACLs and
   firewall bases that permit more than intended, or rules nobody
   remembers adding). Verification habit: periodic rule-base review +
   flow-log reconciliation (match real traffic to rules; hunt the
   unused/overly-broad entries).
7. **(2)** MFA points: **VPN concentrator** (remote access) and
   **management interfaces** (jump/admin paths) — accept "inner FW admin"
   or "DMZ host admin" as the second. Most-forgotten flow: **DMZ → inner
   initiations** (or DMZ outbound updates to internet) — designers
   remember inbound web, forget the DMZ's own egress/lateral needs.
8. **(2)** Model: *ARP is unauthenticated broadcast* (protocol fact) →
   *deploy DAI with DHCP snooping bindings and segment management VLANs*
   (defense decision). Any correct protocol→defense chain (DNS →
   authenticated resolvers/DoH; TCP handshake → SYN cookies; MAC table →
   port security) earns full credit.
