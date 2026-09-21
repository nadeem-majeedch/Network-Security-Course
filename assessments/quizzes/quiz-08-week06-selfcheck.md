---
quiz: quiz-08
week: 6
type: self-check
clos: [CLO-3, CLO-4]
lectures: [L09, L10, L11, L12]
marks: 10
duration: 15 min
bloom-range: Understand–Apply
status: complete
artifact-type: student-quiz
answer-key: instructor/answer-keys/quiz-08-answer-key.md
---

# Self-Check Quiz 8 — Week 6 (Firewalls, NAT, Proxies, Zero Trust)

> Not graded — use after L09–L12. Answers in the course answer key.

1. **(MCQ)** NAT's security reputation is best characterized as:
   A. A firewall substitute · B. An address/mapping mechanism with
   incidental filtering side-effects · C. An encryption layer ·
   D. An identity system

2. **(MCQ)** An explicit proxy differs from a transparent proxy because
   clients are:
   A. Unaware of it · B. Configured to send traffic to it deliberately ·
   C. NATed by it · D. Authenticated by IP only

3. **(MCQ)** Microsegmentation's defining property is:
   A. Perimeter-only enforcement · B. Workload-to-workload policy down to
   individual services · C. VLAN-per-floor layout · D. Single default
   gateway per host

4. **(MCQ)** Which is a *zero trust* tenet rather than a marketing claim?
   A. "No VPNs ever" · B. Per-request authorization from identity, device
   posture, and context · C. "Perimeter is dead, buy our product" ·
   D. Trust internal by default

5. **(MCQ)** In a policy decision, the signal that distinguishes zero
   trust from classic NAC is:
   A. Antivirus presence · B. Continuous evaluation per session/request ·
   C. MAC address allow-lists · D. Subnet membership

6. **(Short)** Why is a DMZ host that initiates outbound connections to the
   internet a design smell? Name the risk and one control. *(2 marks)*

7. **(Diagram)** A three-tier design shows web tier → app tier → DB tier
   with a single flat VLAN. Sketch (describe) the two segment boundaries
   you would insert first, and why those two. *(2 marks)*

8. **(Short)** State the difference between an "allow established" rule and
   an "allow any" rule in one sentence each. *(2 marks)*

**Total: 10 marks**
