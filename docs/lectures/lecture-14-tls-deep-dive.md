---
lecture: L14
title: TLS Deep Dive
module: 4
week: 7
hours: 2
clos: [CLO-6]
difficulty: intermediate
status: complete
artifact-type: student-lecture-material
instructor-plan: modules/module-04-crypto-protocols/lectures/lecture-14-tls-deep-dive.md
---

# L14 — TLS Deep Dive

## 1. Learning Objectives

By the end of this session you can: (1) walk the TLS 1.2 and 1.3 handshakes and name what authenticates the transcript; (2) decode a cipher-suite string and explain why TLS 1.3 shrank the suite list; (3) read a certificate chain and classify validation failures; (4) audit a TLS configuration report by severity and write the corrected config; (5) state the defender-visibility trade-offs of TLS and the metadata alternatives.

## 2. Key Definitions

| Term | Definition |
|---|---|
| Handshake | Negotiation establishing keys, ciphers, and authenticated identity |
| ECDHE | Ephemeral key agreement — the forward-secrecy requirement of every modern suite |
| Cipher suite | Named combination: key exchange + signature + bulk cipher + AEAD/hash |
| Transcript authentication | Finished messages cryptographically bind the whole handshake |
| 0-RTT | TLS 1.3 early data — fast but **replayable**; safe only for idempotent operations |
| SNI / ECH | Server Name Indication (hostname revealed) / Encrypted Client Hello (hides it) |
| HSTS | Policy forcing HTTPS (L07); includeSubDomains + preload |
| mTLS | Mutual TLS — client certificates authenticate clients (service-to-service) |
| ALPN | Application-Layer Protocol Negotiation (h2/http1.1 selection inside the handshake) |

## 3. Detailed Explanations

### 3.1 The handshakes, precisely
**TLS 1.2 (two round trips):** ClientHello (versions, suites, random) → ServerHello + Certificate + ServerKeyExchange (ECDHE params, signed) → client key exchange → ChangeCipherSpec → **Finished** (MAC over the transcript). **TLS 1.3 (one round trip):** ClientHello (key_share, supported_versions) → ServerHello + *encrypted* extensions/certificate + Finished → client Finished. In both, the **Finished** messages authenticate the entire transcript — this is the cryptographic reason L07's MITM attempts turn into visible certificate errors. **0-RTT** exists in 1.3 but is replayable: GETs tolerable, POSTs dangerous (server-side design responsibility).

### 3.2 Cipher suites and algorithm agility
Suite grammar (1.2): `TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256` = key exchange + auth + bulk + PRF. TLS 1.3 suites shrink to bulk+AEAD (`TLS_AES_128_GCM_SHA256`) because key exchange is always (EC)DHE and authentication is always the certificate. What 1.3 deleted and why: RSA key transport (no forward secrecy), CBC (padding-oracle class), RC4, SHA-1 signatures, compression (CRIME). Agility lesson: smaller negotiated surface = fewer downgrade opportunities.

### 3.3 Certificates in the handshake
Validation path: leaf → intermediates → trust-store root; identity = **SAN** match; validity window; EKU serverAuth. The failure classes you will diagnose constantly: expired, wrong-host (SAN), untrusted root (private CA undeployed), **missing intermediate** (the "works in browser, fails in curl" classic — servers must send the chain), self-signed. Ecosystem controls: **CT logs** (public issuance visibility), **CAA** (who may issue for your domain), stapled OCSP (L13).

### 3.4 Configuration audit — the graded skill
Floors: TLS 1.2 minimum, 1.3 preferred; AEAD suites only; strong groups (X25519/P-256); signature algorithms SHA-256+; compression off. Certificate hygiene: SAN complete, automated renewal (ACME), HSTS + includeSubDomains, mTLS for service-to-service. Report reading order: protocols → suites → groups → certificate → extras (renegotiation, stapling). Classify findings: critical (SSLv3/1.0 enabled, anonymous suites), major (CBC, weak groups), minor (no staple, long chains).

### 3.5 Defender visibility trade-offs
TLS hides payloads from sensors (Module-6 premise) — but DNS, IPs, SNI (until ECH), sizes, timing, and handshake fingerprints remain. TLS inspection gateways demand enterprise root-CA trust (governance), break pinning, add latency: decide per zone. Metadata analytics (beacon cadence, volume, fingerprints) replace most content inspection needs — Module 6 builds them.

## 4. Network Diagram: TLS 1.3 vs 1.2 handshake

```
 TLS 1.2 (2-RTT)                          TLS 1.3 (1-RTT)
 C ──ClientHello────────────►S            C ──ClientHello(key_share)──►S
 C ◄─ServerHello+Cert+SKE────             S ◄─{ext, Cert, Finished}─ encrypted
 C ──ClientKeyExchange,CCS,Finished►      C ◄─(client Finished)──
 S ◄─{app data}──────────────             C ──{app data}────────────►S
 {…} = encrypted from here on; Finished = transcript MAC
```

## 5. Protocol Examples

- `openssl s_client -connect host:443 -showcerts` — read chain order, SAN, verify code, negotiated suite. Forcing `-tls1_2` is a *testing* technique for legacy checks.
- Suite decode: `TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256` → ephemeral exchange ✓, RSA signature ✓, AEAD ✓ — a healthy 1.2 suite; `TLS_RSA_WITH_AES_128_CBC_SHA` → no forward secrecy + CBC: flag as major.

## 6. Configuration Concepts (nginx-flavored, concept level)

```
 ssl_protocols TLSv1.2 TLSv1.3;
 ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:…';
 ssl_prefer_server_ciphers off;                 # 1.3 chooses client-first anyway
 ssl_stapling on;
 add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

## 7. Security Implications

- The handshake *is* the security argument: authenticated transcript + ECDHE forward secrecy.
- TLS 1.3 is smaller *because* it deleted failure-prone choices — agility with discipline.
- Configuration auditing is a repeatable method — and directly graded (Pract-2) and reused in cloud (L20) and capstone hardening.

## 8. Realistic Organizational Scenario

**The downgrade "fix" (running case).** A legacy vendor appliance sits behind a load balancer; a security update breaks legacy negotiation, and ops responds by re-enabling TLS 1.0 end-to-end. Three weeks later an external scan flags the domain. You reconstruct the failure, assess real risk, and design the correct fix: modern TLS at the terminating LB, legacy leg isolated on a dedicated segment, timeline of the governance failure. Full case: **cs-046**; the audit-and-fix of good/bad endpoints is Lab-07 part 2 and Pract-2.

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "TLS 1.3 = automatically secure config" | Protocol ≠ policy; weak certs, bad renewal, missing HSTS still happen. |
| "Padlock = safe site" | TLS authenticates the connection to that name; phishing sites have padlocks. |
| "Certificate = encryption strength" | Certificates bind identity; suite/group policy decides strength. |
| "SSL and TLS are synonyms" | SSL (1990s) is deprecated/broken; "SSL scanner" is branding, not protocol. |
| "0-RTT is free speed" | It's replayable — safe only for idempotent operations by design. |

## 10. Classroom Activities

1. **Handshake side-by-side:** Wireshark of 1.2 vs 1.3 (lab VM keys available); annotate what authenticates what.
2. **Audit + fix (pairs):** audit good vs bad endpoints; classify findings; write the corrected config; re-verify.
3. **Suite-decode relay:** teams decode suite strings onto a whiteboard grid (kx/auth/bulk/hash) and flag vintage.

## 11. Problem-Solving Questions

1. Why is 0-RTT safe for GETs but dangerous for POSTs? Give the concrete attack.
2. TLS 1.3 removed RSA key exchange but kept RSA signatures — what property changed, and why does forward secrecy require it?
3. A site works in Chrome but `curl` fails with a certificate error: what chain defect causes this, and why do browsers mask it?
4. Your SOC wants TLS inspection everywhere: what breaks (name three), and what metadata analytics replace 80% of that need?
5. Which is worse on a public endpoint: an expired certificate or TLS 1.0 enabled? Argue severity with exploitability.

## 12. Exit Ticket

1. Name the message in each handshake that provides transcript authentication.
2. What does `TLS_AES_128_GCM_SHA256` omit that a 1.2 suite includes — and why is that OK?
3. List three certificate-validation failure classes and the client-visible symptom of each.
4. What problem does OCSP stapling solve for both CA and client?
5. Give two metadata signals usable for detection despite full TLS.

*(Answers: `teaching/answer-keys/answer-key-module-04.md`.)*

## 13. References

- RFC 8446 (TLS 1.3); RFC 5246 (TLS 1.2, legacy reference); RFC 9325 (secure TLS recommendations).
- RFC 6797 (HSTS); RFC 6844 (CAA); RFC 6962 (CT).
- Mozilla SSL Configuration Generator; NIST SP 800-52 Rev. 2 (implementation guidance).
- sslyze / testssl.sh documentation (audit tooling).

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-6 | §3 handshakes + audit method | Pract-2 (W7), Lab-07, Case sets B–C |
