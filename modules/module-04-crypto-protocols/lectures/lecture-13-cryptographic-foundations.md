---
lecture: L13
title: Cryptographic Foundations
module: 4
week: 7
hours: 2
clos: [CLO-5]
difficulty: intermediate
status: complete
artifact-type: teaching-plan
---

# L13 — Cryptographic Foundations (Teaching Plan)

## 1. Overview & Prerequisites

- **Prerequisites:** L04 (protocol fluency), L12 (egress/visibility reality — why we encrypt). Discrete math co-requisite supports modular arithmetic intuition.
- **Position:** supplies the primitives that L14 (TLS), L15–L16 (VPNs), L18 (802.1X/EAP-TLS), and L20 (cloud endpoints) all configure. Focus is *correct selection and use*, not math proofs.
- **Faculty prep:** verify OpenSSL 3.x on lab images; prepare the lab-PKI worksheet (root → intermediate → server chain); bring the "choose the primitive" scenario cards.
- **Common misconceptions:** "longer key = always better"; "hashing is encryption"; "open-source crypto is weaker than secret algorithms"; "TLS hides everything."

## 2. Learning Objectives

By the end of this lecture, students can:

1. Define the confidentiality/integrity/authentication services and match each to its primitive family (symmetric cipher, hash/HMAC, asymmetric) (Understand).
2. Explain why block-cipher *mode* matters (ECB patterns; CBC malleability; AEAD/GCM as the modern default) and choose a mode for a given requirement (Apply/Evaluate).
3. Describe asymmetric mechanics at a functional level (key pairs, signatures, Diffie–Hellman key agreement, forward secrecy concept) (Understand).
4. Distinguish hash, MAC, and signature functions and select the right one per integrity scenario (Analyze).
5. Outline PKI trust: root/intermediate chains, certificate contents (SAN!), revocation (CRL/OCSP) and the operational lifecycle that L14 exercises (Understand).

## 3. Detailed Concepts

### 3.1 Primitive families and their services
- Symmetric encryption (AES, ChaCha20): one shared key; fast; the *bulk* data workhorse. Key distribution is the hard part → asymmetric solves it.
- Hashes (SHA-256/SHA-3): fixed-size fingerprints; integrity only; password *storage* needs slow KDFs (bcrypt/Argon2/PBKDF2 — not raw hashes).
- MACs (HMAC, Poly1305): keyed integrity — detects tampering by holders of the key.
- Asymmetric (RSA, ECC): key agreement (ECDHE), digital signatures (RSA-PSS, ECDSA/Ed25519), small-actor trust bootstrapping (PKI).
- The modern composition: **AEAD** (GCM, ChaCha20-Poly1305) = confidentiality + integrity in one primitive with one misuse-resistant interface.

### 3.2 Modes: where symmetric crypto actually breaks
- ECB: identical blocks → visible patterns (penguin demo); violates confidentiality for structured data.
- CBC: needs unpredictable IV per message; malleable without authentication (padding-oracle class — L14 links to real TLS history: Lucky13/CBC removal in TLS 1.3).
- CTR/OFB: stream modes; **nonce reuse = catastrophic** (two-time pad) — the classic real-world failure.
- GCM: AEAD with nonce-uniqueness requirement; nonce misuse breaks both confidentiality and authenticity — engineering discipline over algorithm choice.

### 3.3 Asymmetric essentials
- Key pairs: public encrypts/verifies, private decrypts/signs; key sizes today: RSA ≥ 3072 (2048 = legacy floor), ECC P-256/Curve25519-class.
- Diffie–Hellman/ECDHE: two parties derive a shared secret over a public channel; **ephemeral** (ECDHE) gives forward secrecy — tomorrow's stolen private key can't decrypt today's captures.
- Signatures: hash-then-sign; provide authenticity + non-repudiation; used for certificates, code, DNSSEC (L14/L16 links).

### 3.4 PKI: how trust gets operational
- Chain: root (offline, in trust stores) → intermediate(s) → leaf (server cert). Browsers ship roots; enterprises add their own (L07 MITM-interception governance link).
- Certificate contents: subject/SAN (what actually matters today), validity, key usage/EKU, signature. SAN mismatches = most "cert errors."
- Revocation: CRLs (bulky, cached) vs OCSP (privacy + availability issues) vs OCSP stapling; soft-fail vs hard-fail trade-offs.
- Lifecycle: generation (key ceremony/CSR), issuance, deployment, rotation, expiry monitoring — the operational reality of L14's config audits.

### 3.5 Selection method (the examinable skill)
- Given a scenario: What service? (confidentiality/integrity/auth) Who holds keys? At rest vs in transit? Performance? Compliance anchors (FIPS)?
- Decision table: encrypt files at rest → AES-256-GCM or age-style hybrid; sign a release → Ed25519/RSA-PSS; session key exchange → ECDHE; store passwords → Argon2id; verify download → SHA-256 *of a signed manifest* (hash alone is spoofable).

## 4. Teaching Sequence (120 Minutes)

| Time | Segment | Instructor moves |
|---|---|---|
| 0–10 | Warm-up: 5 scenarios, pick the primitive | Rapid classify: sign/encrypt/KDF/MAC — surface misconceptions early |
| 10–35 | Core: families + services | Service→primitive mapping table built live; password-hashing detour (KDF ≠ hash) |
| 35–55 | Core: modes | ECB penguin demo; CBC malleability bit-flip thought experiment; GCM nonce discipline |
| 55–65 | Break | — |
| 65–85 | Core: asymmetric + PKI chain | OpenSSL s_client vs live capture of a cert chain; SAN mismatch anatomy; revocation trade-offs |
| 85–110 | Student activity: lab PKI build | Pairs create root→intermediate→server chain, deploy on range web VM, verify in browser (Lab-07 part 1; cs-040..043 prep) |
| 110–120 | Wrap + formative | Exit ticket; Quiz 3 recap (was W5); L14 trailer: "your chain now meets the TLS handshake" |

## 5. Technical Examples

```
# Build a two-tier PKI (lab range, pairs)
openssl genrsa -out rootCA.key 4096
openssl req -x509 -new -key rootCA.key -sha256 -days 1825 \
        -subj "/C=US/O=NSLab/CN=NSLab Root CA" -out rootCA.crt
openssl req -new -newkey ec -pkeyopt ec_paramgen_curve:P-256 \
        -keyout intCA.key -subj "/O=NSLab/CN=NSLab Intermediate" -out intCA.csr
openssl x509 -req -in intCA.csr -CA rootCA.crt -CAkey rootCA.key \
        -CAcreateserial -days 1095 -sha256 -out intCA.crt -extfile ext-ca.cnf
# then leaf: SAN file (DNS:server.lab,IP:10.0.20.10) — show the SAN-mismatch error
# when accessed by bare IP with a DNS-only SAN: teach what "identity" means to TLS.

# Inspect anything:
openssl x509 -in leaf.crt -noout -text | egrep 'Subject:|DNS:|Signature Alg'
```
Expected teaching points: chain building works because signatures bind; SAN is identity; key sizes differ by role (root RSA 4096 long-lived, leaf EC fast).

## 6. Discussion Questions

1. Why is "we use AES-256" an incomplete security claim? What four facts are missing?
2. A developer wants to store user passwords "hashed with SHA-256." What's wrong, and what do you change?
3. Why did TLS 1.3 delete CBC cipher suites but keep GCM/ChaCha20? Name the failure classes involved.
4. Your root CA key lives on an offline laptop "in a drawer." Walk through what a real key ceremony changes.
5. Why does forward secrecy change the *forensics* of an incident (Module 8 preview: what evidence survives)?

## 7. Student Activity

**Lab PKI build (25 min, pairs):** complete the root→intermediate→leaf chain with correct extensions (CA:TRUE pathlen on intermediate; EKU serverAuth + SAN on leaf), deploy to the range web VM, and deliberately request the site by IP to trigger a SAN mismatch — document the exact browser/OpenSSL error text. Deliverable: chain listing + one-paragraph "why the error" explanation.

## 8. Problem-Solving Case

**Primary case — cs-041 "Key-management lapse root-cause analysis" (intermediate):**
A post-incident review reveals the CI pipeline bakes a signing private key into a public Docker image layer; artifacts signed in the last 90 days are suspect. Students must (a) map which services/capabilities the key grants, (b) design rotation with a trust transition (two-key overlap, revoke-old/verify-new), (c) propose pipeline controls (secrets manager, short-lived signing tokens, layer-scrubbing), and (d) write the customer communication constraints — what can you honestly claim?
**Linked cases:** cs-040 (cipher/mode selection), cs-042 (internal PKI design), cs-043 (hash-collision implications).
*(Model solutions: instructor answer-key set, Module 4.)*

## 9. Formative Assessment

1. Match: AEAD, HMAC, Argon2id, ECDHE → service each provides.
2. Why does CTR-mode nonce reuse destroy confidentiality *and* integrity?
3. Which certificate field must list `server.lab` for a browser to trust it — CN or SAN?
4. What does OCSP stapling change about revocation checking, and who benefits privacy-wise?
5. RSA-2048 vs EC P-256: give one reason to prefer each in 2026-era deployments.
*(Answer key: instructor set, Module 4.)*

## 10. Summary & Key Takeaways

- Match primitive to service; mode discipline (nonces/IVs) breaks real systems more often than algorithm strength.
- Asymmetry exists to *bootstrap* trust (agreement + signatures + PKI), not to encrypt bulk data.
- PKI is an operational system — lifecycle, SAN identity, revocation — not a math abstraction.

## 11. References

- NIST FIPS 197 (AES); NIST SP 800-38A (block-cipher modes); NIST SP 800-38D (GCM).
- NIST SP 800-57 Part 1 Rev. 5 — key management & key-size guidance.
- RFC 8446 — TLS 1.3 (cipher-suite philosophy); RFC 8439 — ChaCha20-Poly1305.
- RFC 5280 — X.509 PKI certificate/CRL profile; RFC 6960 — OCSP.
- Boneh & Shoup, *A Graduate Course in Applied Cryptography* (free online draft) — foundations chapters.
- OpenSSL documentation — x509/req/ca subcommands (current 3.x).

## 12. CLO Mapping

| CLO | Where in this lecture | Assessed via |
|---|---|---|
| CLO-5 | §3.1–3.5 selection method; PKI build §7 | Quiz 3 (W5 — previewed), Assignment 3 (W7), Lab-07 |
