---
lecture: L16
title: Modern VPNs & Crypto Agility
module: 4
week: 8
hours: 2
clos: [CLO-5, CLO-7]
difficulty: intermediate
status: complete
artifact-type: teaching-plan
---

# L16 — Modern VPNs & Crypto Agility

## 1. Overview & Prerequisites

- **Prerequisites:** L15 (IPsec/IKE mechanics — the comparison baseline). L13 (forward secrecy, key lifecycle).
- **Position:** completes CLO-7's evaluation skill and the crypto-agility mindset (rotation, migration, PQC direction). Midterm runs in-session (Week 8 per calendar).
- **Faculty prep:** prepare WireGuard demo config pair on the range; print the three VPN scenario cards for the evaluation exercise; ready Midterm papers and seating plan.
- **Common misconceptions:** "WireGuard is automatically the right choice"; "SSL VPN = TLS is the security model"; "split tunneling is inherently insecure"; "post-quantum = replace everything next year."

## 2. Learning Objectives

By the end of this lecture, students can:

1. Explain WireGuard's design decisions (CryptoKey Routing, fixed primitive set, noise-pattern handshake, ~4k LOC) and its operational trade-offs vs IPsec (Analyze/Evaluate).
2. Evaluate TLS-VPN architectures (client VPNs, SSL-portal era → modern tunnel modes) including authentication layering and the death of the "portal" model (Evaluate).
3. Design remote-access architecture: full vs split tunnel (with kill-switch/DNS-leak reasoning), MFA integration, posture checks (Create).
4. Apply crypto-agility planning: key rotation cadence, algorithm deprecation workflow, PQC (Kyber/ML-KEM) migration direction in handshakes (Create/Evaluate).
5. Recommend a VPN solution for a given org profile, defending against one counter-scenario (Evaluate).

## 3. Detailed Concepts

### 3.1 WireGuard in depth
- Design: fixed crypto (Curve25519, ChaCha20-Poly1305, BLAKE2s, SipHash) — no negotiation → fewer downgrade surfaces; Noise IK-pattern handshake; both peers authenticated by static public keys.
- CryptoKey Routing: allowed-ips *is* the policy (routing + ACL in one) — elegant and sharp-edged (misconfig leaks, no dynamic protocol by default).
- Operational profile: tiny codebase (auditability), kernel-space speed, silent by design (no handshake responses to unauthenticated peers — scan resistance).
- Trade-offs vs IPsec: no built-in dynamic routing (BGP-over-WG is manual), identity = key not certificate ecosystem (rotation scripting required), no per-user MFA inside the protocol (solved at orchestration layer — e.g., SSO-gated config distribution).

### 3.2 TLS-VPNs and remote access architecture
- Evolution: SSL-VPN "portals" (webified apps — largely deprecated for full tunnels), modern TLS tunnels (OpenVPN/DTLS, enterprise SSL-VPN gateways) — control plane convenience vs IPsec.
- Authentication layering: device cert + user MFA (SAML/OIDC to IdP) + posture check (disk encryption, EDR present) → the ZTNA pattern; network-access-only-for-one-app (identity-aware proxy) as the end-state (L09/L20 bridge).
- Split vs full tunnel: full = visibility + control + bandwidth cost; split = performance but DNS-leak/exfil-side-channel risks; mitigations: split-DNS governance, kill-switch, per-app split (PAC/ZTNA).
- The unmanaged-device problem: BYOD → browser-isolation/VDI alternatives; endpoint posture as admission condition.

### 3.3 Key management & rotation practice
- Rotation cadences by key type: session keys (per-connection), device certs (90–398 days, ACME automation), CA roots (years, ceremony), PSKs (ban or vault-managed).
- Rotation mechanics: overlap windows (two valid keys), staged revocation (CRL/OCSP + allowlist transition), canary host first.
- Compromise playbook: which key did what (signing vs transport), blast-radius enumeration, emergency rotation drill (L27 IR link).

### 3.4 Crypto agility & PQC direction
- Agility = the *ability* to swap algorithms: versioned configs, cipher-suite policies, inventory of embedded crypto (the hard part — appliances and firmware).
- PQC today: ML-KEM (Kyber) in hybrid mode with ECDHE in TLS 1.3 (X25519Kyber768-style hybrids) and IKEv2 extensions; signatures (ML-DSA/Dilithium) trail; "harvest now, decrypt later" motivates KEM migration first.
- Realistic plan: inventory → hybrid handshakes at gateways → certificate strategy watch → no big-bang.

### 3.5 Decision framework (the graded evaluation)
- Criteria: identity model (cert vs key vs IdP-federated), scale/topology (hub-spoke dynamic routing?), client fleet management, MFA/posture integration, auditability, ops team skill, endpoint platform spread.
- Score three scenario cards (field-sales laptop fleet; 400-site retail POS; IoT device-to-cloud) → defend recommendation; instructor plays the counter-scenario advocate.

## 4. Teaching Sequence (120 Minutes)

| Time | Segment | Instructor moves |
|---|---|---|
| 0–10 | Recap: IPsec failure taxonomy card game | Rapid-fire: symptom → cause |
| 10–35 | Core: WireGuard design | Noise-pattern intuition; allowed-ips-as-policy demo on range; silent-peer scan behavior |
| 35–55 | Core: TLS-VPN + remote access design | Split-tunnel/DNS-leak vignette; ZTNA pattern sketch (bridges L09) |
| 55–70 | Core: agility + PQC | Rotation runbook walk; hybrid-KEM handshake status slide |
| 70–75 | Break (short) | — |
| 75–105 | **Midterm examination** (45 min, covers W1–W8, per calendar) | Administer; strict timing |
| 105–115 | Post-exam activity (low-stakes) | Scenario-card evaluation in pairs while papers collect |
| 115–120 | Wrap | Lab-08 completion reminder; Module-5 trailer: wireless + cloud ahead |

## 5. Technical Examples

```
# WireGuard pair on the range (peer A shown; peer B mirrored)
[Interface]
PrivateKey = <vault-issued>
Address = 10.99.0.1/30
ListenPort = 51820
[Peer]
PublicKey = <peer-B-pub>
AllowedIPs = 10.20.0.0/16          # CryptoKey Routing: route AND policy
Endpoint = 198.51.100.10:51820
PersistentKeepalive = 25

# Behavioral observations:
wg show            # handshake age, transfer counters (stuck handshake = key/route issue)
# Scan peer UDP/51820 with nmap → no response without valid static key:
#   'silent by design' — contrast with IKE responder behaviors.
```
Expected teaching points: policy + routing unified; key rotation = re-issue + AllowedIPs update (script it); MFA lives in orchestration, not the protocol.

## 6. Discussion Questions

1. "No negotiation" removes downgrade attacks but breaks what *operational* capability? Which orgs should care most?
2. Split tunnel with per-app ZTNA vs full tunnel: which gives better forensic visibility, and what does it cost the user?
3. Your 10-year-old IPsec fleet uses SHA-1 PRFs. Write the migration sequence (inventory → overlap → cutover) and the risk you cannot eliminate.
4. Why does "harvest now, decrypt later" push KEM migration ahead of signature migration?
5. Where does MFA actually enforce in each model: IPsec-EAP, WireGuard+orchestrator, ZTNA? What happens at 3 a.m. when the IdP is down in each?

## 7. Student Activity

**Scenario evaluation (during post-exam slot, pairs):** each pair takes one scenario card, scores it against the §3.5 criteria matrix, writes a 100-word recommendation, and anticipates one counter-argument. Three pairs read out; class votes; instructor arbitrates with the decision framework.

## 8. Problem-Solving Case

**Primary case — cs-051 "Split-tunnel VPN risk assessment" (intermediate):**
A company's contractor fleet uses split-tunnel VPNs; monitoring sees contractor endpoints reaching internal APIs directly *outside* the tunnel (local ISP path) and DNS resolving internal names via public resolvers. Students must (a) enumerate the exposure classes (DNS leak, lateral-egress from unmanaged endpoints, idle-tunnel abuse), (b) design the remediation matrix (full tunnel vs per-app ZTNA vs posture-gated split with split-DNS), (c) select and justify per contractor class, and (d) define the monitoring signals that verify the chosen control.
**Linked cases:** cs-052 (WireGuard rollout design), cs-053 (crypto-agility/PQC readiness review).
*(Model solutions: instructor answer-key set, Module 4.)*

## 9. Formative Assessment

*(Post-midterm quick-fire, 5 min, oral/mini-whiteboard — not graded)*

1. Name the four primitives WireGuard fixes by design.
2. What single field in a WireGuard peer config enforces both routing and ACL policy?
3. Give one reason enterprises still choose IPsec for site-to-site in 2026.
4. What is a hybrid KEM handshake composed of today?
5. Which VPN model makes the IdP's uptime a network-availability dependency — and how do you mitigate?
*(Answer key: instructor set, Module 4.)*

## 10. Summary & Key Takeaways

- WireGuard = fixed crypto + key-based identity + allowed-ips policy: brilliant where ops can script; IPsec still wins where dynamic routing/cert ecosystems rule.
- Remote access is converging on ZTNA: device identity + user MFA + posture, per-app enforcement.
- Crypto agility is an organizational capability: inventory, overlap rotations, hybrid PQC at gateways first.

## 11. References

- Donovan — WireGuard: Next Generation Kernel Network Tunnel (whitepaper, wireguard.com); Noise protocol framework spec.
- RFC 8439 — ChaCha20-Poly1305; RFC 7748 — X25519/X448.
- NIST SP 800-77 Rev. 1 — IPsec guide (comparison anchor); NIST IR 8547 — transition to PQC algorithms (draft/initial public draft status as applicable).
- NIST FIPS 203/204/205 — ML-KEM/ML-SLH/ML-DSA standards (2024) — current status discussion.
- Cloud Security Alliance — SDP/ZTNA architecture guidance (identity-aware access patterns).

## 12. CLO Mapping

| CLO | Where in this lecture | Assessed via |
|---|---|---|
| CLO-5 | §3.3–3.4 key lifecycle/agility application | Midterm (today), Assignment 3 |
| CLO-7 | §3.1–3.2 + §3.5 evaluation framework; activity §7 | Midterm (today), Capstone design |
