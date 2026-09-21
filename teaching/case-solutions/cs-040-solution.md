---
case: cs-040
solution-for: modules/module-04-crypto-protocols/case-studies/cs-040-cipher-mode-selection-data-classes.md
difficulty: intermediate
module: 4
lecture-anchor: L13
clos: [CLO-5]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-040 Solution — Cipher/Mode Selection (INSTRUCTOR ONLY)

## Model Solution

**Selection table:**

| Class | In transit | At rest | Key mgmt | Why (one line) |
|---|---|---|---|---|
| Device telemetry | **AES-128-GCM** (device→gateway, per-session ECDH P-256 keys) | AES-256-GCM envelope, DEK per ingest-batch, rotate 90d | KMS envelope; telemetry's low sensitivity doesn't justify per-message DEK overhead at 50k msg/s | 128-bit GCM is *not* a weak choice at this volume — AES-NI makes it the cheapest safe AEAD; nonce discipline per session via HKDF-derived nonces |
| Patient records | **TLS 1.3 (AES-256-GCM suites)** end-to-end to the records service | **AES-256-GCM envelope, DEK per record**, KMS-held KEKs, rotation 1y + on-demand re-wrap | per-record DEK so export/deletion/rotation acts record-locally (regulatory story); KEK rotation without mass-re-encryption | regulated class gets the strictest primitives *and* the strictest key lifecycle — the lifecycle is the compliance evidence |
| Analytics extracts | AES-256-GCM on export bundles | envelope with **class-level DEK** + separate DS-team key | extract DEK distinct from record DEKs; short TTL on extract keys | separates "can read extracts" from "can read records" — key topology as access control |

**The counter-intuitive choice (defend one): AES-128-GCM for telemetry.**
The risk it avoids: **nonce-management failure under volume**. At 50k
msg/s, per-record 96-bit random nonces under one long-lived key approach
birthday-bound collision risk in operationally short horizons — and GCM
nonce reuse is *catastrophic* (keystream reuse + GHASH universal forgery).
The correct engineering: per-session keys via ECDH+HKDF (nonce space resets
per session) and 128-bit keys (cheaper, equally safe key strength for
symmetric ops) — "AES-256 everywhere" is the *slower* path that tempts
teams into batching messages under one key+nonce regime for performance,
which is precisely the failure mode. 256-bit symmetric strength buys
nothing against realistic adversaries here; disciplined nonce/key hygiene
buys everything.

**Legacy path — AES-256-CBC + HMAC-SHA-256:** constrained as follows.
CBC+HMAC (Encrypt-then-MAC done correctly) *does* provide confidentiality +
integrity — it's not broken; its risks are padding-oracle class flaws in
*improper* implementations and the legacy API surface inviting misuse
(non-random IVs, MAC-then-encrypt orderings). Constrain by: gateway-only
termination for the legacy device cohort, vetted library only
(no hand-rolled CBC), EtM ordering, random IV per message, and a
**retirement date** with the vendor cohort's hardware refresh. What it is
not providing: crypto-agility — flag it in the risk register.

## Alternative Solutions

- **ChaCha20-Poly1305 for telemetry:** defensible if some device cohorts
  lack AES-NI (software AES is slow on small cores) — the fleet is
  AES-NI-equipped per evidence, so GCM wins on acceleration; credit the
  conditional reasoning.
- **Per-record DEKs for all classes:** strongest topology; KMS cost at
  telemetry volume is real money and latency — class-proportionality is the
  lesson, not maximal defense.
- **RSA-4096 wrap instead of ECDH:** works; larger handshake payloads on
  constrained devices; ECDH P-256 + HKDF is the modern default — RSA kept
  only where the vendor requires it.

## Tradeoffs

- 128 vs 256 symmetric: performance/compliance optics vs no practical
  security gain for symmetric keys — document the reasoning so auditors see
  intent, not corner-cutting.
- Rotation cadence (90d telemetry vs 1y records): shorter rotation shrinks
  exposure windows but increases KMS operational load and re-wrap risk on
  the regulated class.
- Envelope-per-record vs per-batch: per-record is the regulatory answer for
  records; per-batch elsewhere balances KMS spend.

## Common Mistakes

- "Strongest everywhere" (AES-256-GCM + RSA-4096 all tiers) without nonce/
  volume analysis.
- Choosing CBC for compatibility without naming the EtM/IV constraints —
  CBC-without-integrity is the classic.
- Ignoring key *topology* (who can decrypt extracts vs records) — the DS
  export path is where sensitivity actually leaks.
- Treating rotation as a checkbox without an operational re-wrap plan.

## Instructor Prompts

- "Compute the random-96-bit-nonce collision horizon at 50k msg/s under one
  key. What does that force?"
- "Why is per-record DEK a *regulatory* answer, not just a crypto one?"
- "What does the legacy CBC path's retirement date have to do with
  crypto-agility?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Nonce-volume analysis; class-proportional key topology |
| Technical accuracy | 25% | GCM/CBC/EtM/ECDH mechanics correct |
| Alternatives considered | 20% | ChaCha/RSA/KMS-cost options weighed |
| Communication | 15% | Table + one defended counter-intuitive choice |

**Timing:** reveal at 5:00 + 2; the nonce-arithmetic prompt is the
quantitative anchor.

## CLO Mapping

- **CLO-5** — Cryptographic selection with mode/protocol correctness.
