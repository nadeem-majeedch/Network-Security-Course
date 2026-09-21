---
lecture: L14
title: TLS Deep Dive
module: 4
week: 7
hours: 2
clos: [CLO-6]
difficulty: intermediate
status: complete
artifact-type: teaching-plan
---

# L14 — TLS Deep Dive

## 1. Overview & Prerequisites

- **Prerequisites:** L13 (primitives, modes, PKI chain anatomy). L07 (MITM evidence patterns — now explained properly by the handshake).
- **Position:** the protocol students will audit their whole careers. Config-audit skill is graded directly (Pract-2) and reused in cloud (L20) and capstone hardening.
- **Faculty prep:** stage one good and one bad TLS endpoint on the range (bad: TLS 1.0 enabled, self-signed, weak suite order); prepare handshake Wireshark profile with TLS decryption keys for the lab VM.
- **Common misconceptions:** "TLS 1.3 = automatically secure config"; "padlock icon = safe site"; "certificate = encryption strength"; "SSL and TLS are synonyms."

## 2. Learning Objectives

By the end of this lecture, students can:

1. Walk through TLS 1.2 (two round trips) and TLS 1.3 (one round trip) handshakes, naming key roles of ECDHE, certificates, and the ChangeCipherSpec/Finished messages (Analyze).
2. Explain what the cipher suite string encodes (key exchange, signature, bulk cipher, AEAD) and why TLS 1.3 shrank the list (Understand).
3. Read a certificate chain from a handshake and identify identity (SAN), validity, EKU, and chain-of-trust errors (Analyze).
4. Given a TLS configuration report (sslyze/testssl.sh-style), classify findings by severity and produce a corrected config (Evaluate/Create).
5. Describe the visibility cost of TLS for defenders and the sanctioned alternatives (TLS inspection gateway trade-offs, metadata analytics from L21) (Evaluate).

## 3. Detailed Concepts

### 3.1 Handshake mechanics
- TLS 1.2: ClientHello (versions, suites, random) → ServerHello + Certificate + ServerKeyExchange (ECDHE params, signed) → client key exchange → ChangeCipherSpec → Finished (MAC of transcript). Two RTTs; session resumption via session IDs/tickets.
- TLS 1.3: ClientHello (key_share, supported_versions) → ServerHello + encrypted extensions/cert/Finished → client Finished. One RTT; 0-RTT early data exists but **is not replay-safe** — API design must exclude non-idempotent operations.
- Transcript integrity: everything is authenticated by Finished → stripping/injection (L07) fails at handshake, producing the cert warnings students diagnosed there.
- Downgrade protection: TLS 1.3 sentinel bytes in random + supported_versions extension; legacy-version negotiation attacks are historical (POODLE-era) but explain version hygiene.

### 3.2 Cipher suites and algorithm agility
- Suite grammar: `TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256` → (kx, auth, bulk, AEAD/prf). TLS 1.3 suites shrink to bulk+AEAD (`TLS_AES_128_GCM_SHA256`) because kx is always (EC)DHE and auth is always the cert.
- Why the shrink: removed RSA key transport (no forward secrecy), CBC (Lucky13/padding oracles), RC4, SHA-1 signatures, compression (CRIME).
- Group selection matters: P-256 vs X25519 — both fine; finite-field DHE is slow (performance reason behind ECDHE default).

### 3.3 Certificates in the handshake
- Chain validation path: leaf → intermediates → trust-store root; hostname verification against **SAN** (CN ignored by modern clients); validity window; EKU serverAuth.
- Failure classes students will diagnose: expired, wrong-host (SAN), untrusted root (private CA not deployed — L13 build), missing intermediate (the "works in browser, fails in curl" classic), self-signed.
- CT (Certificate Transparency) logs + CAA records: ecosystem visibility and issuance control; monitoring CT for *your* domains = supply-chain radar.

### 3.4 Configuration audit (the graded skill)
- Protocol floors: TLS 1.2+ only; TLS 1.3 preferred; disable compression.
- Suite policy: AEAD only (GCM, ChaCha20-Poly1305); strong ECDHE groups; signature algorithms SHA-256+.
- Cert hygiene: ≥2048 RSA or EC P-256+, SAN complete, automated renewal (ACME), HSTS + includeSubDomains (L07 payoff).
- mTLS for service-to-service (L20 microsegmentation link): client certs + trust-store discipline.
- Report reading: classify findings — critical (SSLv3/1.0 enabled, anonymous suites, cert key reuse), major (CBC suites, weak groups), minor (no OCSP staple, long chain).

### 3.5 Defender visibility trade-offs
- E2E TLS hides payloads from sensors (Module 6 premise): metadata analytics — SNI (until ECH), DNS, sizes/timing, JA3/JA4-class fingerprinting — carry detection.
- TLS inspection gateways: requires enterprise CA trust deployment (L07 governance), breaks pinning, adds latency/privacy duties; decide per-zone, not globally.
- ECH (Encrypted Client Hello): hides SNI — plan detection without hostname (IP-reputation + volume baselines).

## 4. Teaching Sequence (120 Minutes)

| Time | Segment | Instructor moves |
|---|---|---|
| 0–10 | Recap: PKI chain quiz | Trace a 3-cert chain on the board; SAN identity question |
| 10–40 | Core: handshakes (1.2 vs 1.3) | Wireshark side-by-side of both handshakes (keys available for lab VM); annotate transcript auth |
| 40–60 | Core: suites + agility | Decode two suite strings; map removed algorithms to their historical attacks |
| 60–70 | Break | — |
| 70–95 | Core: config audit method | Run the audit tool against good vs bad endpoint; classify findings live; write one corrected config |
| 95–110 | Student activity: audit + fix | Pairs audit both endpoints, produce findings table + corrected config (Pract-2 prep; cs-044..048 prep) |
| 110–120 | Wrap + formative | Exit ticket; Pract-2 briefing (W7); L15 trailer: "same machinery, tunnel instead of session" |

## 5. Technical Examples

```
# Handshake observation (range VM with keylog for decryption)
openssl s_client -connect bad.lab.local:443 -tls1_2 -showcerts </dev/null
# Read: cert chain order, SAN, verify return code, negotiated suite.

# Audit both endpoints (pattern; exact flags per tool version in lab sheet)
sslyze --certs bad.lab.local:443          # or testssl.sh equivalent
# Teaching read-out order: protocols → suites → groups → cert → misc (renegotiation,
# OCSP staple). Classify each line: critical/major/minor.

# Corrected nginx-style config (design artifact):
#   ssl_protocols TLSv1.2 TLSv1.3;
#   ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:...';
#   ssl_prefer_server_ciphers off;         # 1.3: suites chosen client-first anyway
#   ssl_stapling on;  add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
```
Expected teaching points: `-tls1_2` forces legacy negotiation — a *testing* technique; verify return code chain gives instant diagnosis class.

## 6. Discussion Questions

1. Why is 0-RTT data safe for GETs but dangerous for POSTs? Give the concrete attack.
2. TLS 1.3 removed RSA key exchange but kept RSA *signatures*. What property changed, and why does forward secrecy require it?
3. A site works in Chrome but `curl` fails with certificate error. What chain defect causes this, and why do browsers mask it?
4. Your SOC wants TLS inspection everywhere. What breaks (name 3), and what metadata analytics could replace 80% of that need?
5. Which is worse on a public endpoint: expired certificate or TLS 1.0 enabled? Argue severity with exploitability.

## 7. Student Activity

**Audit + fix sprint (15 min block within lab window, pairs):** complete findings tables for both endpoints; write the corrected server config for the bad endpoint; verify by re-running the audit and by `openssl s_client` showing TLS 1.3 + AEAD suite. Deliverable feeds Pract-2 (W7) and Lab-07 part 2.

## 8. Problem-Solving Case

**Primary case — cs-046 "TLS downgrade incident analysis" (intermediate):**
A legacy vendor appliance sits behind a load balancer; after a "security update," some clients started failing — and the ops team responded by re-enabling TLS 1.0 end-to-end. Three weeks later an external scan flags the domain. Students must (a) reconstruct the failure (why did the update break legacy negotiation), (b) assess actual risk (what attacker capability does TLS 1.0 enable today), (c) design the correct fix (terminating LB with modern TLS → internal legacy leg isolated on a dedicated segment), and (d) write the timeline showing where governance failed.
**Linked cases:** cs-044 (expired-cert outage), cs-045 (self-signed cert risk), cs-047 (weak-cipher audit + remediation), cs-048 (mTLS deployment).
*(Model solutions: instructor answer-key set, Module 4.)*

## 9. Formative Assessment

1. Name the one message in each handshake that provides transcript authentication.
2. What does `TLS_AES_128_GCM_SHA256` omit that a 1.2 suite includes, and why is that OK?
3. List three certificate-validation failure classes and the exact client-visible symptom of each.
4. Why does OCSP stapling exist (what problem does it fix for both CA and client)?
5. Give two metadata signals usable for detection despite full TLS.
*(Answer key: instructor set, Module 4.)*

## 10. Summary & Key Takeaways

- The handshake is the security argument: authenticated transcript + ECDHE forward secrecy.
- TLS 1.3 is smaller *because* it deleted failure-prone choices — algorithm agility with discipline.
- Config auditing is a repeatable method (protocols → suites → cert → extras) and a graded skill.

## 11. References

- RFC 8446 — TLS 1.3; RFC 5246 — TLS 1.2 (legacy reference).
- RFC 6797 — HSTS; RFC 8460 — TLS-based origin HSTS context; RFC 6844 — CAA; RFC 6962 — CT.
- RFC 9325 — Recommendations for Secure Use of TLS and DTLS (the config-audit authority).
- Mozilla SSL Configuration Generator & TLS guidelines (operational baselines).
- NIST SP 800-52 Rev. 2 — TLS implementation guidance for US-government-class systems (policy anchor).

## 12. CLO Mapping

| CLO | Where in this lecture | Assessed via |
|---|---|---|
| CLO-6 | §3.1–3.5 handshake/audit method; audit sprint §7 | Pract-2 (W7), Lab-07, Case sets B–C |
