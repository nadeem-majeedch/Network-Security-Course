---
marp: true
theme: default
paginate: true
lecture: L13
week: 7
clos: [CLO-5]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# Cryptographic Foundations

**Network Security · Lecture 13 · Week 7**

*Turning wire-claims into wire-proofs.*

<!-- notes: OPEN (2 min). Hook: "L02's ledger said identity on the wire
is a claim. This module builds the proofs." -->

---

## Learning Objectives

1. **Distinguish** symmetric, asymmetric, and hash primitives by role
2. **Explain** why hybrid encryption is the universal pattern
3. **Apply** HMAC vs signature to the right authentication problem
4. **Reason** about key management as the actual hard problem
5. **Reject** the "AES-256 so it's secure" fallacy with two counter-
   examples

<!-- notes: (1 min) Objective 5 is quiz-9 Q7's exact answer. Objective
4 sets up assignment 2 and the PKI case (cs-042). -->

---

## Hash Functions: The Integrity Primitive

- Fixed-size digest from arbitrary input; collision & preimage
  resistance
- Uses: verification, deduplication, fingerprints
- **Not** encryption, **not** authentication alone — anyone can hash
- SHA-256 family today; MD5/SHA-1 = historical case studies

<!-- notes: (5 min) The three "not"s are the quiz. Quiz-9 Q1 + QB-017's
HMAC rationale build on this. -->

---

## Symmetric Encryption: One Shared Key

- AES (block cipher) — fast, used for bulk data everywhere
- Modes matter: CBC (careful) vs GCM/ChaCha20 (AEAD = confidentiality +
  integrity)
- The distribution problem: how do two strangers share a key?

<!-- notes: (5 min) The mode point earns its slot: AES-CBC misuse
caused real record-layer weaknesses (assignment-2's F4 finding). The
distribution problem is the cliffhanger for asymmetric. -->

---

## Asymmetric Cryptography: The Key Pair

- Public key encrypts/verifies; private key decrypts/signs
- RSA (classical), ECDSA/Ed25519 (modern signatures)
- Solves distribution: publish the public half freely
- Costs: slower, bigger — hence *hybrid* systems

<!-- notes: (5 min) Quiz-9 Q1's correct pairings live here. The
"publish freely" line answers L02's spoofing ledger — identity becomes
provable. -->

---

## Hybrid Encryption: The Universal Pattern

- Asymmetric to **establish** a shared key → symmetric to **move** data
- TLS, IPsec, PGP, VPNs — all the same shape
- The course's protocol lectures (L14–16) instantiate this pattern

![bg right:35% fit](diagrams/05-tls-handshake.md)

<!-- notes: (5 min) Diagram 05 previewed: key shares = the asymmetric
part; records = symmetric. Quiz-9 Q2 asks this exact pattern. -->

---

## HMAC & Signatures: Two Authentications

| | Key type | Verifiable by | Property |
|---|---|---|---|
| HMAC | shared secret | holders of the secret | integrity + origin |
| Signature | private/public | **anyone** | + **non-repudiation** |

- HMAC: fast peer-to-peer (TLS 1.2 record MACs, API tokens)
- Signature: public verification (certificates, code signing)

<!-- notes: (6 min) The table is the discriminator slide: who can
verify decides which tool. Midterm B3 asks exactly this; QB-017 too.
Non-repudiation = only the private-key holder could have produced it. -->

---

## Key Management: The Actual Hard Problem

- Generation: real entropy (the historical failures are entropy)
- Distribution: PKI (L14), pre-shared (PSK pain), key agreements
- Rotation: lifetime policy, revocation, emergency paths
- Storage: HSM/secret managers vs config files (assignment-2's findings)

<!-- notes: (6 min) "Crypto fails at the edges" — key management is
where. Assignment-2's findings register (expiry, manual renewal,
custody) is this slide's practical echo. cs-041's lapse case is the
RCA story. -->

---

## Crypto Agility: Designing for Replacement

- Algorithms age (MD5 → SHA-1 → …) — design for *swappability*
- Suite negotiation (TLS ciphersuites) is agility in action
- Post-quantum migration = agility's current test (cs-053's case)

<!-- notes: (4 min) Concept only: agility = protocol-level algorithm
negotiation + inventory of what uses what. cs-053 is the expert capstone
case here. -->

---

## CS/DS Example: Notebook Data at Rest

- Dataset storage: symmetric (AES) at rest, signatures for provenance
- Key storage: platform secret manager — not the notebook's `~/.aws`
  (cs-088's lesson in crypto vocabulary)

<!-- notes: (3 min) DS framing: the same primitives, applied to the
research estate; the secret-manager point ties back to module 2's
credential-hygiene cases. -->

---

## Activity: Pick the Primitive (6 min)

For each, name the right primitive: (a) verify a downloaded dataset
matches the published checksum, (b) prove an invoice came from the
CFO, (c) bulk-encrypt a backup stream, (d) authenticate an API request
server-to-server.

<!-- notes: (6 min) Answers: (a) hash compare (integrity only), (b)
signature (non-repudiation), (c) symmetric AEAD, (d) HMAC or mTLS.
The (a) nuance: no origin authentication — matches quiz-3 Q6. -->

---

## Case Study: cs-040 (5 min)

- Cipher-mode selection for data classes — match primitive to need

<!-- notes: (5 min) Classroom protocol; the case operationalizes the
mode/property distinctions from today. -->

---

## Formative Check

- Oral: why can't a plain hash prove origin? What does a signature add
  over HMAC?

<!-- notes: (2 min) Exit oral — both are midterm B3 components. -->

---

## References & Next

- NIST FIPS 180/197/203 (SHA, AES, AEAD guidance)
- Diagrams: `diagrams/05-tls-handshake.md` (preview)
- **Next (L14):** TLS deep dive — the handshake becomes concrete
