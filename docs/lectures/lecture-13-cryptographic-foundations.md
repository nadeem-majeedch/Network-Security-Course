---
lecture: L13
title: Cryptographic Foundations
module: 4
week: 7
hours: 2
clos: [CLO-5]
difficulty: intermediate
status: complete
artifact-type: student-lecture-material
instructor-plan: modules/module-04-crypto-protocols/lectures/lecture-13-cryptographic-foundations.md
---

# L13 — Cryptographic Foundations

> **Precision note (used all course):** *encryption* provides confidentiality;
*authentication* proves origin/identity; *authorization* decides permitted actions;
*integrity* detects alteration. Hashes and MACs provide integrity (MACs add
authentication); they are **not** encryption.

## 1. Learning Objectives

By the end of this session you can: (1) match primitive families to security services; (2) explain why block-cipher *mode* matters (ECB patterns, CBC malleability, GCM nonce discipline) and choose a mode for a requirement; (3) describe asymmetric mechanics — key pairs, ECDHE agreement, signatures, forward secrecy; (4) distinguish hash, MAC, and signature use cases; (5) outline PKI trust chains, certificate contents, and revocation trade-offs.

## 2. Key Definitions

| Term | Definition |
|---|---|
| Symmetric cipher | One shared key encrypts/decrypts (AES, ChaCha20) — the bulk workhorse |
| AEAD | Authenticated Encryption with Associated Data (GCM, ChaCha20-Poly1305): confidentiality + integrity in one primitive |
| Block-cipher mode | How blocks are chained (ECB/CBC/CTR/GCM); the mode is where systems break |
| Nonce | Number used once; reuse in CTR/GCM is catastrophic |
| Hash | One-way fingerprint (SHA-256/SHA-3); integrity only — *not* encryption |
| HMAC / Poly1305 | Keyed integrity: detects tampering by holders of the key |
| ECDHE | Ephemeral Diffie–Hellman on elliptic curves: session-key agreement with forward secrecy |
| Digital signature | Hash-then-sign (RSA-PSS, ECDSA, Ed25519): authenticity + non-repudiation |
| PKI | Trust infrastructure: root → intermediate → leaf certificates |
| SAN | Subject Alternative Name — the certificate field that actually identifies the host |
| OCSP / CRL | Revocation checking (online / list-based) |

## 3. Detailed Explanations

### 3.1 Primitive families and their services
Symmetric ciphers (AES-256, ChaCha20) encrypt bulk data with a shared key — fast, but key *distribution* is the hard problem. Hashes (SHA-256/3) fingerprint data for integrity; password *storage* needs slow KDFs (Argon2id/bcrypt), not raw hashes. MACs (HMAC, Poly1305) add a key to integrity — tampering by non-key-holders becomes detectable. Asymmetric crypto (RSA, ECC) solves distribution: publish a key, keep its pair private. The modern composition is **AEAD** — one primitive, one interface, fewer misuse footguns.

### 3.2 Modes: where symmetric crypto actually breaks
- **ECB:** identical plaintext blocks → identical ciphertext blocks (the encrypted-penguin picture). Structured data leaks through.
- **CBC:** needs an unpredictable IV per message; without authentication it is **malleable** (bit-flipping; padding-oracle history) — the reason TLS 1.3 deleted CBC.
- **CTR/OFB:** stream modes; **nonce reuse = catastrophic** (two-time pad: XOR of two ciphertexts leaks the XOR of plaintexts).
- **GCM:** AEAD with a strict nonce-uniqueness requirement — nonce misuse breaks both confidentiality *and* authenticity. Discipline beats algorithm choice.

### 3.3 Asymmetric essentials
Key pairs: public encrypts/verifies; private decrypts/signs. Sizes today: RSA ≥ 3072 (2048 = legacy floor), EC P-256/Curve25519-class. **Diffie–Hellman/ECDHE** lets two parties derive a shared secret over a public channel; **ephemeral** keys give **forward secrecy** — stealing tomorrow's private key does not decrypt today's captures. Signatures (hash-then-sign) provide authenticity + non-repudiation — the backbone of certificates, code signing, DNSSEC.

### 3.4 PKI: how trust gets operational
Chain: offline **root** (in trust stores) → **intermediate(s)** → **leaf** (server cert). Identity lives in the **SAN** — a cert with `DNS:server.lab` accessed by bare IP produces the classic "name mismatch" error. **Revocation:** CRLs (bulky, cached), OCSP (availability/privacy issues), OCSP stapling (server fetches, client verifies — privacy win). Lifecycle is operational reality: generation, issuance, deployment, rotation, expiry monitoring — L14 audits exactly this.

### 3.5 The selection method (the graded skill)
Ask: which *service* (confidentiality/integrity/authn)? at rest or in transit? who holds keys? performance/compliance constraints? Then: files at rest → AES-256-GCM (or a hybrid scheme); signing a release → Ed25519/RSA-PSS; session key exchange → ECDHE; passwords → Argon2id; verifying a download → SHA-256 **of a signed manifest** (a bare hash can be replaced alongside the file).

## 4. Network Diagram: certificate chain of trust

```
 [Root CA]  (offline, self-signed, in OS/browser trust stores)
     │ signs
     ▼
 [Intermediate CA]  (online, pathlen-constrained)
     │ signs
     ▼
 [Leaf: CN/SAN = server.lab]  ◄── client validates chain + SAN + validity
```

## 5. Protocol Examples

- Build a lab chain: `openssl req -x509` (root) → `openssl req -new` + `openssl x509 -req -CA …` (intermediate, then leaf with SAN). Inspect with `openssl x509 -noout -text` — find SAN, EKU, signature algorithm.
- Mode failure shapes: ECB-encrypted bitmap shows outlines; CBC bit-flip flips plaintext bits downstream; GCM with a repeated nonce exposes keystream reuse.

## 6. Configuration Concepts (concept level)

- Key ceremonies and offline roots; intermediates online with pathlen constraints.
- SAN completeness (name + all aliases); automated issuance (ACME) and expiry monitoring.
- KDF parameters for password storage; nonce-generation strategy (random 96-bit for GCM or counters — never reuse).

## 7. Security Implications

- Match primitive to service; **mode discipline breaks real systems more often than key length**.
- Hash ≠ encryption; MAC ≠ signature — precision here is graded and professional.
- Forward secrecy changes incident mathematics: stolen long-term keys don't decrypt past captures (Module 8 evidence note).
- PKI is an operational system: chain errors, SAN mismatches, and expiry outages dominate real incidents (L14).

## 8. Realistic Organizational Scenario

**The pipeline key (running case).** A review finds a signing private key baked into a public container image; artifacts signed in the last 90 days are suspect. Your analysis: which capabilities the key grants, rotation with a trust transition (two-key overlap → revoke-old/verify-new), pipeline controls (secrets manager, short-lived signing tokens, layer scrubbing), and honest customer communication limits. Full case: **cs-041**; the hands-on chain build is Lab-07 part 1.

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "Hashing is encryption" | Hashes are one-way integrity fingerprints; no key, no confidentiality. |
| "Longer keys fix weak modes" | Nonce reuse and malleability defeat any key length. |
| "Secret algorithms are stronger" | Kerckhoffs: security lives in keys, not secrecy of design. |
| "CN is what browsers check" | SAN is the identity field; CN is legacy. |
| "TLS 1.3 removed RSA entirely" | It removed RSA *key transport*; RSA signatures remain (L14). |

## 10. Classroom Activities

1. **Lab PKI build (pairs):** root → intermediate → leaf with SAN; deploy on the range web VM; trigger the IP-vs-SAN mismatch deliberately and document the exact error.
2. **Primitive sorting:** 10 scenario cards → cipher/MAC/hash/signature/KDF, with one-line justifications.
3. **Mode post-mortems:** given three incident descriptions, identify the mode failure class in each.

## 11. Problem-Solving Questions

1. Why is "we use AES-256" an incomplete security claim? Name four missing facts.
2. A developer stores passwords "hashed with SHA-256" — what changes, and why?
3. Why did TLS 1.3 delete CBC suites but keep GCM/ChaCha20? Name the failure classes.
4. Your root CA key lives on a laptop "in a drawer" — what does a real key ceremony change?
5. How does forward secrecy change what evidence survives an incident (Module-8 preview)?

## 12. Exit Ticket

1. Match: AEAD, HMAC, Argon2id, ECDHE → the service each provides.
2. Why does CTR-mode nonce reuse destroy confidentiality *and* integrity?
3. Which certificate field must list `server.lab` for a browser to trust it?
4. What does OCSP stapling change about revocation checking?
5. RSA-2048 vs EC P-256: one reason to prefer each in current deployments.

*(Answers: `teaching/answer-keys/answer-key-module-04.md`.)*

## 13. References

- NIST FIPS 197 (AES); NIST SP 800-38A (modes); SP 800-38D (GCM); SP 800-57 Pt.1 (key management).
- RFC 8446 (TLS 1.3); RFC 8439 (ChaCha20-Poly1305); RFC 5280 (X.509); RFC 6960 (OCSP).
- Boneh & Shoup, *A Graduate Course in Applied Cryptography* (free draft) — foundations.
- OpenSSL documentation — req/x509/ca subcommands (current 3.x).

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-5 | §3 selection method; PKI build | Quiz 3 (W5), Assignment 3 (W7), Lab-07 |
