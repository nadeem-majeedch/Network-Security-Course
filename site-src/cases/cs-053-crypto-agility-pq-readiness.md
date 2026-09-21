# cs-053 — Crypto-Agility and Post-Quantum Readiness Review

> **Simulated scenario.** The company, inventory, and timelines are fictional;
> standards references are real (NIST PQC selections) but the scenario is
> fictional.

## Difficulty & Domain

- **Difficulty:** Advanced · **Domain:** VPN and secure remote access · **CLO:** CLO-5
- **Est. time:** 15 minutes · **Anchor:** L16 (Modern VPNs & Crypto-Agility)

## Scenario

A data-analytics company (10-year data sensitivity horizon) must produce a
crypto-agility plan. Leadership heard "quantum computers will break our
VPN" and wants action now. Your job: separate the *actual* risks and
timelines from the panic, produce a **crypto inventory** framework, and a
prioritized plan — including which systems need *migration planning*
versus *monitoring*, and the harvest-now-decrypt-later (HNDL) analysis
that justifies the whole exercise.

## Stakeholders

- **CEO** — read a headline; needs a sober plan with dates.
- **Platform/security** — owns VPN (WireGuard), TLS everywhere, internal
  PKI (RSA-4096 roots), and some legacy SSH.
- **Data governance** — 10-year sensitivity horizon is their number.
- **Vendors** — some appliances can't be patched for PQ for years.

## Network Context

- VPN: WireGuard (Curve25519 + ChaCha20-Poly1305).
- TLS: 1.3 everywhere feasible (X25519, RSA/ECDSA certs from internal PKI —
  RSA-4096 root, ECDSA P-256 intermediates).
- Legacy: 3 SSH endpoints with RSA host keys; one partner SFTP with
  mandatory RSA key exchange; backup envelope encryption (AES-256, KMS).
- Data at rest: AES-256 (symmetric — not the PQ headline, and that matters).

## Student Task

1. Produce the **risk-triage framework**: which items are (a) HNDL-exposed
   (harvest now, decrypt later — key-exchange material only), (b) broken-
   at-scale risks (signatures *at future date*), (c) unaffected
   (symmetric-only). Apply it to the inventory — one table.
2. Explain the **HNDL logic** that justifies prioritization: why the VPN's
   *handshake* matters more than its *data cipher*, and why the 10-year
   horizon number drives everything.
3. Produce the **prioritized plan** (3 phases with dates): crypto-agility
   infrastructure (inventory, algorithm registry, migration drills),
   PQ/T hybrid adoption order (TLS first? VPN first? PKI last?), and the
   vendor/appliance contingency.

## How to Approach This (Reasoning Scaffold)

- The headline is wrong: quantum (Shor) breaks *public-key* key exchange
  and signatures; Grover only halves *symmetric* strength — AES-256
  stands.
- HNDL: adversaries record handshakes today, decrypt when quantum arrives —
  so *key exchange on long-horizon confidential data* is the urgent class;
  signatures are broken only *when* quantum exists (verify-then-forgery).
- Crypto-agility = the *ability to change algorithms* — inventory +
  registry + drills; the algorithm swap is the easy part once agility
  exists.

## CLO Mapping

- **CLO-5** — Crypto-agility planning with correct quantum-risk triage.

## Safety Notes

- Standards references (NIST FIPS 203/204/205 — ML-KEM/ML-DSA/SLH-DSA) are
  real; the company and timelines are fictional. No vendor pitches.
