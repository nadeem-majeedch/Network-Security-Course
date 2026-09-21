---
quiz: quiz-07
week: 3
type: self-check
clos: [CLO-2]
lectures: [L05, L06]
marks: 10
duration: 15 min
bloom-range: Understand–Apply
status: complete
artifact-type: student-quiz
answer-key: instructor/answer-keys/quiz-07-answer-key.md
---

# Self-Check Quiz 7 — Week 3 (Threat Modeling, L2 Attacks)

> Not graded — use after L05/L06. Answers in the course answer key.

1. **(MCQ)** In STRIDE, a forged ARP reply maps most directly to:
   A. Information disclosure · B. Spoofing · C. Repudiation ·
   D. Elevation of privilege

2. **(MCQ)** Which pair *both* mitigates rogue DHCP?
   A. DHCP snooping + rate-limiting DHCP messages
   B. Port security + CDP
   C. DAI + STP root guard
   D. 802.1Q + VTP pruning

3. **(MCQ)** MAC flooding succeeds when the switch:
   A. Drops unknown unicast by default · B. Fails open and floods ·
   C. Enables DHCP snooping · D. Runs RSTP

4. **(MCQ)** An attacker's first step after ARP-spoofing a gateway is
   usually to:
   A. Encrypt the victim's disk · B. Enable forwarding to avoid breaking
   the victim's connectivity · C. Change the victim's IP · D. Disable the
   victim's NIC

5. **(MCQ)** BPDU guard protects by:
   A. Blocking BPDUs on access ports that should never see them ·
   B. Encrypting STP frames · C. Prioritizing root bridges · D. Rate-limiting ARP

6. **(Short)** Explain in ≤3 sentences why ARP cannot be "fixed" by
   authentication alone at the protocol level, and what switch features
   compensate. *(2 marks)*

7. **(Diagram)** A diagram shows a switch with VLAN 10 (users) and VLAN 20
   (servers), a trunk to the core, and an unused port labeled "conference
   room." Mark the two ports where DHCP snooping trust should be *off*, and
   the one where it must be *on*. *(2 marks)*

8. **(Short)** A student says: "Our switches are new, so Layer-2 attacks
   don't apply." Give the one-sentence correction. *(2 marks)*

**Total: 10 marks**
