---
case: cs-053
solution-for: modules/module-04-crypto-protocols/case-studies/cs-053-crypto-agility-and-post-quantum-readiness-review.md
difficulty: advanced
module: 4
lecture-anchor: L16
clos: [CLO-5]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-053 Solution — PQ Readiness (INSTRUCTOR ONLY)

## Model Solution

**Risk-triage framework applied:**

| Item | Class | Reasoning |
|---|---|---|
| WireGuard VPN (Curve25519 handshake) | **(a) HNDL-exposed** | recorded handshakes → decrypted when CRQC exists; VPN carries long-horizon confidential flows |
| TLS 1.3 (X25519) to SaaS/partners | **(a) HNDL-exposed** | same logic; session keys derive from ECDHE |
| Internal PKI **RSA-4096 root / ECDSA intermediates (signatures)** | **(b) broken-at-scale later** | signatures are forgeable only *when* CRQC exists — certificates verify against roots *now*; migration is planned, not panicked; root-key transition is the long pole |
| Partner SFTP mandating RSA kex | **(a) HNDL-exposed** + vendor-locked | also an agility finding: no algorithm choice |
| 3 SSH RSA host-key endpoints | **(b)** | host-auth signatures; migrate to Ed25519 *now* (agility win independent of PQ) |
| Backup envelope encryption (AES-256, KMS) | **(c) unaffected** (data cipher) | Grover halves symmetric strength: AES-256 → ~128-bit effective — still safe; *but* the KMS **KEK wrap** (if RSA/ECDSA-based) is (a)/(b) — check the KMS's wrap algorithm! |
| Data at rest AES-256 everywhere | **(c)** | symmetric-only |

**HNDL logic (the justification):** a CRQC (cryptographically relevant
quantum computer) doesn't need to exist *today* to harm *today's* traffic:
an adversary records ECDH handshakes now, and decrypts the sessions' data
the day the machine exists. Confidentiality has a *time horizon* — data
still sensitive in 10 years (the governance number) must not ride
classical key exchange *today*, because protection must outlive the
harvest window. That's why the **handshake (key exchange)** is the urgent
class and the **data cipher (AES-256)** is not: Shor breaks the former,
Grover only degrades the latter. Signatures sit in between: forgery
requires the quantum machine *at verification time in the future*, so PKI
migration is a *planned* transition (hybrid roots, long ceremony) — urgent
for long-lived root artifacts, calm for leaf certs.

**Prioritized plan:**

*Phase 1 — agility foundations (0–6 months):* build the **crypto
inventory** (every protocol, algorithm, key length, key location, owner —
the table above, complete); adopt an **algorithm registry** (named
suites, approved list, deprecation dates); run one **migration drill**
(swap SSH RSA→Ed25519 fleet-wide — small, real, teaches the muscle).
Fix the SFTP exception (negotiate modern kex or retire the partner flow).
*Exit:* inventory complete; registry live; one drill done.

*Phase 2 — hybrid key exchange where HNDL bites (6–18 months):* enable
**PQ/T hybrid** (X25519+ML-KEM-768 — already deployed by major TLS
providers) on internet-facing TLS and the VPN's handshake layer (WireGuard
ecosystems are adding hybrid KEM support; plan for the client+server
coordinated upgrade). Order: **TLS first** (broadest HNDL surface,
ecosystem-ready), **VPN second** (contained fleet, coordinated rollout
easier than TLS's client zoo). *Exit:* all long-horizon-confidential
handshakes hybrid; non-hybrid endpoints inventoried with dates.
*Exit metric:* "no pure-classical key exchange protecting data with
10-year horizon."

*Phase 3 — PKI signature transition + vendor contingency (18–36
months):* plan the **hybrid root** (classical+ML-DSA) for the internal
PKI; leaf certs follow ecosystem support; **vendor appliances** that can't
PQ: wrap them — front with PQ-hybrid TLS terminators, or ring-fence with
short-horizon data only, or replace at refresh; every vendor gets a PQ
roadmap question in contracts. *Exit:* root ceremony executed; no
appliance left with a pure-classical exposure on long-horizon data.

**The sober one-liner for the CEO:** "Our data ciphers are quantum-safe
today; our *handshakes* are the actual exposure, and we're fixing those on
a dated, drilled schedule — the panic was aimed at the wrong layer."

## Alternative Solutions

- **"Migrate everything to PQ now":** immature ecosystem for signatures
  (ML-DSA just standardized; hybrid preferred), operational risk without
  urgency payoff — the phased plan is the professional answer.
- **"Wait for standards to settle entirely":** ignores HNDL on 10-year
  data — the one risk with a *deadline in the past* (harvesting started
  when your data became interesting).
- **Buy-a-box PQ VPN as the whole answer:** the appliance solves one
  handshake while the inventory/registry (the actual agility) rots —
  point-solution trap.

## Tradeoffs

- Hybrid (classical+PQ) vs pure-PQ: hybrid guards against *both* quantum
  arrival and PQ-algorithm cryptanalysis — costs handshake size/CPU
  (real for high-traffic TLS edges; measurable, acceptable).
- Inventory breadth vs speed: full-inventory-first is slower but the
  registry is what makes *every future* migration cheap — pay now.
- Vendor replacement vs ring-fencing: refresh capital vs containment toil —
  decide per appliance by data-horizon exposure.

## Common Mistakes

- "Quantum breaks AES" (Grover's quadratic speedup ≠ break; AES-256
  stands).
- Prioritizing signatures over key exchange (HNDL inversion).
- No inventory/registry — "agility" claimed but unbuildable.
- Forgetting the KMS KEK wrap algorithm in the "unaffected" pile.

## Instructor Prompts

- "Which single inventory row, if wrong, silently voids phase 2?"
- "Why is the harvest window a *past-tense* threat for 10-year data?"
- "What would you drill next after the SSH migration, and why?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | HNDL triage correctness; handshake-vs-cipher separation |
| Technical accuracy | 25% | Shor/Grover scope, hybrid mechanics, NIST selections named |
| Alternatives considered | 20% | Migrate-now/wait rejection logic |
| Communication | 15% | CEO-legible plan with dates |

**Timing:** reveal at 5:00 + 10 (the longer debrief is deliberate — this
case closes Module 4's crypto arc); the "wrong layer" one-liner is the
landing.

## CLO Mapping

- **CLO-5** — Crypto-agility planning with correct quantum-risk triage.
