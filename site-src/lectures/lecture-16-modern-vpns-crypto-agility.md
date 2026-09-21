# L16 — Modern VPNs & Crypto Agility

## 1. Learning Objectives

By the end of this session you can: (1) explain WireGuard's design decisions (fixed crypto, CryptoKey Routing, minimal code) and its operational trade-offs vs IPsec; (2) evaluate remote-access architectures — full vs split tunnel, ZTNA patterns; (3) plan key rotation with overlap windows; (4) describe crypto agility and the PQC (ML-KEM hybrid) migration direction; (5) recommend a VPN solution for an org profile and defend it against a counter-scenario.

## 2. Key Definitions

| Term | Definition |
|---|---|
| WireGuard | Minimal VPN: fixed primitives (Curve25519, ChaCha20-Poly1305, BLAKE2s), Noise-IK handshake, ~4k LOC |
| CryptoKey Routing | `AllowedIPs` = routing table *and* ACL in one peer-config field |
| ZTNA | Zero-trust network access: identity-aware per-app access replacing VPN-for-everything |
| Split tunnel | Only some traffic rides the VPN (performance ↑, control ↓) |
| Full tunnel | All traffic rides the VPN (visibility ↑, bandwidth cost ↑) |
| Split DNS | Name-resolution policy that follows the tunnel split (the classic leak point) |
| Kill switch | Client policy blocking non-tunnel traffic when the tunnel drops |
| Crypto agility | The *capability* to swap algorithms: versioned configs, inventory, rotation drills |
| ML-KEM (Kyber) | NIST-standardized post-quantum KEM (FIPS 203); deployed in hybrid with ECDHE |
| Hybrid KEM | Classical ECDHE + PQ KEM combined so security holds if either survives |

## 3. Detailed Explanations

### 3.1 WireGuard in depth
Design: **fixed primitives** — no cipher negotiation, so no downgrade surface; **Noise-IK** handshake with both peers authenticated by static public keys; tiny auditable codebase; silent by design (no response to unauthenticated probes — scan resistance). **CryptoKey Routing** unifies routing and policy: a peer's `AllowedIPs` says both "these destinations route here" and "only these are allowed." Trade-offs: identity = raw keys, not a certificate ecosystem (rotation is scripted, not PKI); no native MFA inside the protocol (solved at orchestration — SSO-gated config distribution); no built-in dynamic routing (BGP-over-WG is manual).

### 3.2 Remote access: full vs split vs ZTNA
- **Full tunnel:** all traffic through the gateway — visibility and control, bandwidth cost, latency to local resources.
- **Split tunnel:** only corporate ranges ride the tunnel — performance, but **split-DNS leaks** (internal names resolved publicly), unmonitored egress from the endpoint, and idle-tunnel abuse.
- **ZTNA pattern:** device identity (cert) + user MFA (IdP) + posture check (encrypted disk, EDR present) → access to *one application*, not the network. This is where L09's zero-trust tenets land operationally. BYOD and high-risk users push toward browser isolation/VDI.

### 3.3 Key rotation as an operational discipline
Cadences: session keys per-connection; device certs 90–398 days (ACME automation); CA roots years with ceremony; PSKs — ban or vault-manage. Mechanics: **overlap windows** (two valid keys), staged revocation, canary host first, ledger with timestamps. Compromise playbook: enumerate which key did what (signing vs transport), blast radius, emergency rotation drill (feeds L27).

### 3.4 Crypto agility and PQC direction
Agility is organizational: inventory *everything* that embeds crypto (appliances, firmware — the hard part), version configs, rehearse swaps. **PQC status:** NIST standardized ML-KEM (FIPS 203), ML-DSA (204), SLH-DSA (205) in 2024; "harvest now, decrypt later" motivates migrating *key exchange* first via **hybrid KEM** handshakes (X25519 + ML-KEM in TLS 1.3 / IKEv2 extensions); signatures trail. No big-bang replacements — hybrids, gateways first, inventory always.

### 3.5 The decision framework (the graded evaluation)
Criteria: identity model (cert vs key vs IdP-federated), topology/scale (dynamic routing?), client fleet management, MFA/posture integration, auditability, ops skill, endpoint spread. Score three profiles — field-sales laptops (ZTNA-heavy), 400-site retail POS (IPsec site-to-site), IoT-to-cloud (mutual TLS, cert per device) — then defend against a counter-scenario.

## 4. Network Diagram: split vs full vs ZTNA

```
 Full tunnel:   [laptop] ──all traffic──► [VPN GW] ──► internet+corp
 Split tunnel:  [laptop] ──corp ranges──► [VPN GW] ──► corp
                        └─other traffic──► internet  (leak surface!)
 ZTNA:          [laptop+cert+MFA+posture] ──per-app──► [identity-aware proxy] ─► app
```

## 5. Protocol Examples

```
 [Interface]                    # WireGuard peer A (lab range)
 PrivateKey = <vault-issued>
 Address = 10.99.0.1/30
 ListenPort = 51820
 [Peer]
 PublicKey = <peer-B-pub>
 AllowedIPs = 10.20.0.0/16      # route AND policy — CryptoKey Routing
 Endpoint = 198.51.100.10:51820
 PersistentKeepalive = 25
```
- `wg show`: handshake age + transfer counters; a stuck handshake = key/route issue.
- Scan the port with nmap: *no response* without a valid static key — silent by design (contrast: IKE responders reply to probes).

## 6. Configuration Concepts (concept level)

- Rotation runbook: generate → distribute via orchestrator (SSO-gated) → overlap → revoke old → verify.
- Split-DNS governance: corporate resolver pushed with the tunnel; kill-switch policy on clients.
- Hybrid-KEM readiness: gateway/OS support matrix; inventory of embedded crypto first.

## 7. Security Implications

- Fixed crypto removes negotiation attacks but freezes you to one primitive set — agility must come from *orchestration*.
- Split tunneling trades visibility for performance; the DNS leak is where most "split-tunnel risk" actually lives.
- ZTNA makes the IdP a network-availability dependency — design for its outage (break-glass access).

## 8. Realistic Organizational Scenario

**The contractor fleet (running case).** Contractors use split-tunnel VPNs; monitoring shows internal APIs reached directly *outside* the tunnel and internal names resolved publicly. Your assessment: enumerate exposure classes (DNS leak, unmanaged-endpoint egress, idle-tunnel abuse), design the remediation matrix (full tunnel vs per-app ZTNA vs posture-gated split + split-DNS), select per contractor class, define verification signals. Full case: **cs-051**; the scenario-card evaluation runs in class; the Midterm (W8) closes Module 4.

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "WireGuard is automatically the right choice" | Brilliant where ops can script keys and routing; IPsec/PKI ecosystems still fit enterprises better in many cases. |
| "SSL VPN = TLS is the security model" | TLS is the transport; authN/authZ architecture decides security. |
| "Split tunneling is inherently insecure" | Unmanaged: yes-ish. Managed with split-DNS + ZTNA per-app: often the right trade. |
| "Post-quantum = replace everything now" | Migrate key exchange first, via hybrids; inventory before deployment. |
| "Rotation is an IT chore" | It is a *security capability*; drills make compromise survivable. |

## 10. Classroom Activities

1. **WireGuard pair on the range:** bring up peers; `wg show`; scan-resistance observation; then mis-set `AllowedIPs` and watch the leak.
2. **Scenario evaluation (pairs):** score one org profile against the §3.5 criteria; write a 100-word recommendation; anticipate one counter-argument.
3. **Split-tunnel leak hunt:** given a route table + resolver config, find the DNS leak and fix the policy.

## 11. Problem-Solving Questions

1. "No negotiation" removes downgrade attacks but breaks which *operational* capability — and which orgs should care most?
2. Split vs per-app ZTNA: which gives better forensic visibility, and what does it cost the user?
3. Your 10-year-old IPsec fleet uses SHA-1 PRFs — write the migration sequence and name the risk you cannot eliminate.
4. Why does "harvest now, decrypt later" push KEM migration ahead of signature migration?
5. Where does MFA actually enforce in each model (IPsec-EAP, WireGuard+orchestrator, ZTNA), and what happens when the IdP is down at 3 a.m.?

## 12. Exit Ticket

1. Name the four primitives WireGuard fixes by design.
2. Which single peer-config field enforces both routing and ACL policy?
3. Give one reason enterprises still choose IPsec for site-to-site.
4. What is a hybrid KEM handshake composed of today?
5. Which VPN model makes the IdP a network-availability dependency — and how do you mitigate?

*(Answers: `the instructor answer-key collection (not published)`.)*

## 13. References

- WireGuard whitepaper (Donenfeld) and wireguard.com documentation; Noise protocol framework.
- RFC 8439 (ChaCha20-Poly1305); RFC 7748 (X25519).
- NIST SP 800-77 Rev. 1 (IPsec); NIST FIPS 203/204/205 (ML-KEM/ML-DSA/SLH-DSA, 2024); NIST PQC migration guidance (IR 8547 draft status as applicable).
- CSA — SDP/ZTNA architecture guidance.

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-5 | §3.3–3.4 key lifecycle/agility | Midterm (W8), Assignment 3 |
| CLO-7 | §3.1–3.2 + decision framework | Midterm (W8), Capstone design |
