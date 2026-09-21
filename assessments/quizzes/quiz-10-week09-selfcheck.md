---
quiz: quiz-10
week: 9
type: self-check
clos: [CLO-8, CLO-13]
lectures: [L17, L18, L19, L20]
marks: 10
duration: 15 min
bloom-range: Understand–Apply
status: complete
artifact-type: student-quiz
answer-key: instructor/answer-keys/quiz-10-answer-key.md
---

# Self-Check Quiz 10 — Week 9 (Wireless & Cloud Foundations)

> Not graded — use after L17–L20. Answers in the course answer key.
> (Graded Quiz 4 lands in week 10 — this self-check is its warm-up.)

1. **(MCQ)** Which wireless configuration exposes handshake material
   suitable for offline passphrase guessing?
   A. WPA3-Personal · B. WPA2-PSK · C. WPA2/WPA3-Enterprise with EAP-TLS ·
   D. WPA3 with SAE

2. **(MCQ)** An "evil twin" attack works because clients:
   A. Refuse stronger ciphers · B. Reuse SSIDs and auto-associate to the
   strongest-looking match · C. Require captive portals · D. Disable
   802.11r

3. **(MCQ)** A VPC route table entry `0.0.0.0/0 → nat-gateway` means:
   A. All traffic is encrypted · B. Private-subnet instances can initiate
   outbound internet traffic through NAT · C. Inbound internet traffic
   reaches instances directly · D. The subnet is public

4. **(MCQ)** Flow logs in a cloud VPC record:
   A. Packet payloads · B. Metadata of accepted/rejected flows (src, dst,
   ports, bytes, action) · C. DNS queries · D. Full packet captures

5. **(MCQ)** Which control restricts *which route a VPC may learn or use*
   toward another network?
   A. Security group · B. Route table / route propagation policy ·
   C. NACL · D. IAM policy

6. **(Short)** Why does an open guest Wi-Fi need client isolation even
   with no encryption? *(2 marks)*

7. **(Diagram)** A VPC diagram shows public subnet (ALB), private subnet
   (app), private subnet (DB), and an S3 gateway endpoint. Mark the two
   subnets where a NACL allowing 0.0.0.0/0 inbound on 3306 would be most
   damaging, and the route that keeps DB backup traffic off the internet.
   *(2 marks)*

8. **(Short)** State one thing WPA3-Personal fixes and one thing it does
   *not* fix. *(2 marks)*

**Total: 10 marks**
