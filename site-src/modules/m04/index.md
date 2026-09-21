---
status: complete
artifact-type: module-overview-page
module: 4
instructor-only: false
---

# Module 4 — Cryptographic Foundations & Applied Protocols

**Lectures:** L13–L16 (Weeks 7–8) · **CLOs:** CLO-5, CLO-6 · **Cases:** cs-041–053

*Descriptive orientation. Crypto concepts are taught at the protocol level —
no home-rolled cryptography anywhere in this course.*

## What this module covers

Cryptography is the network's integrity and confidentiality backbone — but
only when deployed correctly. You learn what each primitive actually guarantees,
then apply that to TLS, IPsec, and modern VPN architecture, including the
operational reality of certificate lifecycles and crypto agility.

## Lectures

| # | Lecture | Core idea |
|---|---|---|
| L13 | [Cryptographic Foundations](../../lectures/lecture-13-cryptographic-foundations.md) | Symmetric/asymmetric primitives, hashes, PKI roles, key lifecycle |
| L14 | [TLS Deep Dive](../../lectures/lecture-14-tls-deep-dive.md) | TLS 1.2 vs 1.3, certificate validation, common deployment failures |
| L15 | [IPsec & Legacy VPN Architecture](../../lectures/lecture-15-ipsec-legacy-vpn-architecture.md) | AH/ESP, IKE phases, tunnel vs transport, S2S patterns |
| L16 | [Modern VPNs & Crypto Agility](../../lectures/lecture-16-modern-vpns-crypto-agility.md) | WireGuard model, ZTNA contrast, PFS, migration planning |

## Labs

[Lab-07](../../labs/lab-07-pki-tls-audit.md) (lab PKI + TLS configuration audit)
and [Lab-08](../../labs/lab-08-site-to-site-vpn.md) (site-to-site VPN build &
evaluate) — you configure and then *audit* real TLS endpoints and a lab VPN.

## Case studies (intermediate → advanced)

cs-041–053 cover PKI chain design, certificate-expiry incidents, TLS downgrade
evidence, cipher-suite negotiation debates, IPsec phase failure diagnosis, and
VPN split-tunnel tradeoffs. See the [case studies guide](../../cases/index.md).

## Skills checkpoints

- Distinguish what encryption, authentication, integrity, and authorization each guarantee — and what they do not.
- Walk TLS 1.3's handshake and name what an observer learns from it.
- Diagnose a certificate-chain failure from error strings and propose the fix class.
- Argue tunnel vs transport mode and split-tunnel vs full-tunnel for a stated use case.
