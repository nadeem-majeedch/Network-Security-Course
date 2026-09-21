---
case: cs-040
title: Cipher/Mode Selection for Three Data Classes
difficulty: intermediate
domain: VPN and secure remote access
module: 4
lecture-anchor: L13
clos: [CLO-5]
time-estimate: 12 min (5 min reasoning + 7 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-040-solution.md
---

# cs-040 — Cipher/Mode Selection for Three Data Classes

> **Simulated scenario.** The platform, data classes, and constraints are fictional.

## Difficulty & Domain

- **Difficulty:** Intermediate · **Domain:** VPN and secure remote access · **CLO:** CLO-5
- **Est. time:** 12 minutes · **Anchor:** L13 (Cryptographic Foundations)

## Scenario

A health-data platform encrypts three data classes in flight and at rest.
You must select **algorithms + modes + key-management approach** per class
from a vendor's supported list — and defend one counter-intuitive choice.
The trap: "strongest cipher everywhere" fails on performance/compatibility
for one class, and "fast cipher" fails compliance for another.

## Stakeholders

- **Compliance** — health-data rules demand approved primitives + documented key mgmt.
- **Platform team** — latency budget on the ingestion path.
- **Data science team** — bulk analytics read most rows nightly (volume!).
- **Vendors** — support matrix below is what you can actually deploy.

## Network Context

- Ingestion path: devices → gateway → analytics store; 2 ms/millisecond
  matters at the gateway (50k msgs/sec).
- At rest: object storage with envelope encryption (KMS-provided).
- Analytics: reads 80% of rows nightly; decryption cost shows on the bill.

## Available Evidence

**Vendor support matrix:**

| Primitive/mode | Supported | Notes |
|---|---|---|
| AES-256-GCM | yes | hardware-accelerated (AES-NI) |
| AES-128-GCM | yes | accelerated |
| AES-256-CBC + HMAC-SHA-256 | yes | legacy API paths only |
| ChaCha20-Poly1305 | yes | no hardware acceleration on current fleet |
| RSA-4096 | yes | key wrap/transport only |
| ECDH P-256 + HKDF | yes | key agreement |
| KMS envelope encryption | yes | per-object DEKs, rotation supported |

**Data classes:**

1. **Device telemetry** (high volume, low sensitivity, 30-day retention).
2. **Patient records** (low volume, high sensitivity, 7-year retention,
   regulated).
3. **Analytics extracts** (bulk, medium sensitivity, shared with DS team,
   exportable).

## Student Task

1. Build the **selection table**: per class — algorithm/mode (in transit +
   at rest), key-management approach (KMS envelope? per-record DEK?
   rotation cadence), and *why* (one line each).
2. Make and defend the **counter-intuitive choice**: one class where the
   "weaker-looking" primitive is correct, naming the actual risk it avoids.
3. Identify the **one legacy path** you must still support and how to
   constrain its risk (what CBC+HMAC is and isn't providing here).

## How to Approach This (Reasoning Scaffold)

- Match *mode properties* to data shape: GCM's nonce constraints vs
  high-volume single-key use — what's the nonce-management story?
- E-A-I discipline: encryption ≠ integrity unless the mode (or HMAC) provides it.
- Key management *is* the security: rotation cadence and per-object DEKs
  matter more than 128-vs-256-bit arguments.

## CLO Mapping

- **CLO-5** — Cryptographic selection with mode/protocol correctness.

## Safety Notes

- Design exercise; no crypto implementation guidance beyond selection —
  implementation is for vetted libraries.
