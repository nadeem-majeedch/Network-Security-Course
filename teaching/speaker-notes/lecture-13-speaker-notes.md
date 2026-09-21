---
lecture: L13
module: 4
week: 7
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L13 Speaker Notes — Cryptographic Foundations

## Delivery Guide
Module 4 begins with the precision vocabulary (encryption/authn/authz/integrity) —
put it on the board and hold the room to it; grading later in the course assumes
it. The mode-failure demos (ECB penguin, CBC malleability, GCM nonce discipline)
are the intellectual core: students remember pictures, so the penguin earns its
minutes. The PKI chain build starts in-session (Lab-07 part 1) — verify OpenSSL
versions on images beforehand.

## Timing Plan
0–10 primitive-sorting warm-up · 10–35 families + services (incl. KDF detour) ·
35–55 modes (ECB/CBC/CTR/GCM) · 55–65 break · 65–85 asymmetric + PKI chain · 85–110
lab PKI build · 110–120 exit ticket. **Compression:** hash-collision discussion to
one slide; the chain build cannot compress — it's Pract-2's foundation.

## Teaching Demonstrations
1. ECB penguin: encrypt a bitmap with ECB vs CBC — the picture tells the story; explain *why* (identical blocks).
2. CBC bit-flip thought experiment: flip a ciphertext bit, predict the plaintext damage — malleability without integrity.
3. Chain anatomy: `openssl x509 -noout -text` on the built chain — SAN, EKU, pathlen; then request by IP to trigger the SAN mismatch live.

## Expected Student Difficulties
1. Hash = encryption (deep misconception) — the "no key, no confidentiality" sentence + KDF detour.
2. Nonce reuse feels abstract — the two-time-pad arithmetic on two short messages makes it concrete.
3. Chain-order confusion (who signs whom) — the diagram + the built chain together.

## Discussion Facilitation
Q2 (SHA-256 password storage) has a clean canonical answer (KDF: Argon2id/bcrypt) —
probe for *why* (speed is the enemy). Q5 (forward secrecy → forensics): this is a
Module-8 seed; students who connect "stolen keys ≠ past captures" today will write
better evidence caveats in L30.

## Lab Troubleshooting (PKI build context)
- `openssl` version drift (1.1 vs 3.x flag differences): images are pinned — check before class.
- SAN file syntax errors: provide the extension template; one missing `DNS:` prefix is the usual cause.
- Browser trust-store not updated after root import: restart the browser; tell them first.

## Accessibility Notes
- Crypto notation: verbalize every formula; provide plain-language restatements.
- The chain diagram: text hierarchy version distributed.

## CS & Data Science Applications
- **CS:** AEAD interfaces are API-design lessons (misuse resistance by construction); nonce strategies are state-management problems they know.
- **DS:** entropy of names/keys previews L23's qname-entropy math; randomness quality (RNG) is a statistics topic they can own — mention the 2012 Debian-class RNG lesson as historical context.

## Links
Plan: `modules/module-04-crypto-protocols/lectures/lecture-13-cryptographic-foundations.md` · Student page: `docs/lectures/lecture-13-cryptographic-foundations.md` · Answers: `teaching/answer-keys/answer-key-module-04.md`
