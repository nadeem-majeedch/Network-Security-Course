---
quiz: quiz-09
type: answer-key
instructor-only: true
distribution: never-publish-to-students
clos: [CLO-5, CLO-6, CLO-7]
marks: 10
status: complete
---

# Answer Key — Self-Check Quiz 9 (Week 7)

1. **B** — AES is a block cipher; RSA is asymmetric, SHA-1 is deprecated
   for signing, ECDSA is signatures (not key exchange).
2. **B** — asymmetric key exchange establishes the shared symmetric key;
   bulk data rides on symmetric crypto for speed.
3. **B** — validation = unbroken, trusted, unexpired, unrevoked path to a
   trust anchor; A/C/D are all *passing* conditions.
4. **B** — tunnel mode protects the entire inner packet (new outer IP
   header); transport protects only the payload.
5. **B** — one private key for many hosts: compromise is multiplied; no
   impact on validity, speed, or TLS-version compatibility.
6. **(2)** TLS 1.2's CBC-style record layer authenticates separately
   (HMAC) because the cipher alone doesn't detect modification; TLS 1.3
   removed non-AEAD suites, and AEAD (e.g., AES-GCM, ChaCha20-Poly1305)
   provides confidentiality *and* integrity in one primitive. *(1 each
   side)*
7. **(2)** Any two: key exchange/authentication strength and its
   implementation (IKE/TLS handshake, mutual auth of endpoints); endpoint
   security (what the tunnel *terminates on*); policy (what traffic is
   tunneled, split vs full); integrity of the client device; operational
   key/cert management. "AES-256" describes only the bulk cipher.
8. **(2)** Encryption terminates at each site's IPsec gateway (inner LAN
   traffic is plaintext *inside* each site); the on-path observer sees
   only outer headers (gateway IPs, SPIs) — not inner hosts, payloads, or
   protocols. Full credit states the plaintext-inside-each-site point.
