---
quiz: quiz-10
type: answer-key
instructor-only: true
distribution: never-publish-to-students
clos: [CLO-8, CLO-13]
marks: 10
status: complete
---

# Answer Key — Self-Check Quiz 10 (Week 9)

1. **B** — WPA2-PSK's 4-way handshake permits offline dictionary attack;
   SAE/WPA3 derivers per-attempt; Enterprise doesn't use shared passphrases.
2. **B** — clients match SSID and prefer strong signal; the fake AP wins
   association. (Captive portals are unrelated; 802.11r is roaming.)
3. **B** — NAT gateway = outbound-initiated internet access from private
   subnets; it does not admit inbound sessions, and the subnet stays
   private.
4. **B** — flow logs = flow metadata incl. accept/reject action; no
   payloads, DNS content, or PCAPs.
5. **B** — route tables (and propagated routes) decide pathing; SG/NACL
   filter *after* the path, IAM authorizes API actions.
6. **(2)** Without encryption, traffic is readable — but client isolation
   (AP-side peer blocking) stops *client-to-client* snooping/attacks
   (ARP/session theft between guests), which is the threat encryption
   wouldn't fully address either on an open net. Isolation = containment
   of the RF crowd.
7. **(2)** Most damaging NACL miss: DB subnet (and app subnet) allowing
   3306 from anywhere — direct DB exposure; the route keeping backup off
   the internet: **S3 gateway endpoint route** (private S3 access).
8. **(2)** Fixes: offline dictionary attack on captured handshakes (SAE).
   Does *not* fix: evil-twin/rogue-AP social attacks, weak passphrases
   themselves, or unmanaged client posture — WPA3-Personal is still PSK.
