---
quiz: quiz-09
week: 7
type: self-check
clos: [CLO-5, CLO-6, CLO-7]
lectures: [L13, L14, L15, L16]
marks: 10
duration: 15 min
bloom-range: Understand–Apply
status: complete
artifact-type: student-quiz
answer-key: instructor/answer-keys/quiz-09-answer-key.md
---

# Self-Check Quiz 9 — Week 7 (Cryptography & Secure Channels)

> Not graded — use after L13–L16. Answers in the course answer key.

1. **(MCQ)** Which pairing is correct?
   A. RSA — symmetric encryption · B. AES — block cipher ·
   C. SHA-1 — recommended signing · D. ECDSA — key exchange

2. **(MCQ)** Hybrid encryption (e.g., TLS 1.3) uses asymmetric crypto to:
   A. Encrypt bulk data · B. Establish a shared symmetric key ·
   C. Compress payloads · D. Replace certificates

3. **(MCQ)** A certificate chain fails validation when:
   A. The leaf is signed by a trusted intermediate chain ·
   B. Any link lacks a valid path to a trusted root (or is expired/revoked) ·
   C. The key is 2048-bit · D. SAN matches the hostname

4. **(MCQ)** IPsec tunnel mode differs from transport mode because it:
   A. Encrypts only the payload · B. Encapsulates and protects the whole
   original IP packet · C. Works only with IPv6 · D. Skips authentication

5. **(MCQ)** A wildcard certificate's main operational risk is:
   A. Shorter validity · B. One key/one certificate covers many hosts —
   broader blast radius if compromised · C. Slower handshakes ·
   D. Incompatible with TLS 1.3

6. **(Short)** Why does TLS 1.2 need an explicit integrity record MAC while
   TLS 1.3's AEAD ciphers do not? *(2 marks)*

7. **(Short)** A vendor says their VPN "uses AES-256, so it's secure."
   Name two things AES-256 does *not* cover that still decide the VPN's
   security. *(2 marks)*

8. **(Diagram)** A site-to-site IPsec diagram shows two offices with
   tunnels through the internet. Label where encryption ends at each side,
   and state what an on-path observer between the gateways can see.
   *(2 marks)*

**Total: 10 marks**
