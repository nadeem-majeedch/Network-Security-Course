---
module: 4
lectures: [L13, L14, L15, L16]
status: complete
artifact-type: answer-key
instructor-only: true
distribution: never-publish-to-students
---

# Answer Key — Module 4: Cryptographic Foundations & Applied Crypto Protocols

> **INSTRUCTOR ONLY — contains model answers to graded formative assessments.**
> Links: Plans `modules/module-04-crypto-protocols/lectures/` · Student pages `docs/lectures/lecture-13…16` · Notes `teaching/speaker-notes/lecture-13…16-speaker-notes.md`

## L13 — Cryptographic Foundations

### Formative checks (plan §11)
1. The four-way distinction (this is the module's graded core):
   - **Encryption** = confidentiality (unreadable without key).
   - **Authentication** = proof of identity/origin.
   - **Authorization** = what the authenticated identity may do (not cryptographic by itself).
   - **Integrity** = undetected-modification guarantee (MACs, AEAD).
   Any answer conflating authentication with authorization loses the point; MAC = integrity + origin authenticity *with a shared key*.
2. Symmetric vs asymmetric: AES (shared key, fast, bulk data) vs RSA/ECDH (keypair, key exchange & signatures); hybrid = asymmetric for key establishment, symmetric for data.
3. ECB failure: identical plaintext blocks → identical ciphertext (penguin picture); CBC needs random IV + padding care; GCM = AEAD but nonce-misuse catastrophic (nonce reuse leaks the auth key and XORs keystream).
4. Hash vs MAC: hash = unkeyed digest (integrity against accident, no origin proof); MAC/HMAC = keyed (integrity + origin authenticity); signatures = public-key verification (non-repudiation).
5. Salt-per-password, stored alongside hash; pepper = global secret stored separately (HSM/vault) — salt defeats precomputation, pepper adds defense against DB-only theft.

### Exit ticket
- MAC = integrity + shared-key origin; signature = integrity + private-key origin + non-repudiation. Reject "MACs are weak signatures".
- Misuse beats math: the lesson sentence is "modern primitives fail on wrong usage — nonces, IVs, key reuse — more than on broken math."

### Discussion facilitation
- Q2 ("can't we just encrypt everything?"): encryption without authentication is plaintext to an active attacker (bit-flipping, replay); AEAD or nothing.
- Q5 (quantum, honest framing): Shor breaks RSA/ECC key establishment & signatures; Grover halves symmetric security margin (AES-256 stays comfortable); "harvest now, decrypt later" motivates PQC migration *for confidentiality longevity* — no invention needed, NIST PQC standards exist.

## L14 — TLS Deep Dive

### Formative checks
1. TLS 1.2 vs 1.3: 1.3 removes RSA key transport & static DH, forward-secret (EC)DHE only, encrypts more of the handshake, 1-RTT (0-RTT with replay caveats). The security *why*: fewer modes, no legacy baggage.
2. Chain validation: leaf → intermediates → root (in trust store); check signature chain, validity window, revocation, EKU/hostname (SAN). Root = trust anchor; missing intermediate = the classic deployment failure.
3. Forward secrecy: session keys not derivable from the long-term key; (EC)DHE ephemeral keys give it — RSA key transport (removed in 1.3) lacked it.
4. E-A-I mapping for TLS: encryption (record layer AEAD), authentication (certificate chain + Finished), integrity (AEAD tag), *authorization lives in the application* (what the client may do) — TLS itself does not authorize.
5. TLS inspection trade-off: visibility vs breaking pinning, privacy/legal constraints, adding a privileged middlebox — "just inspect everything" is not a senior answer; scope it and log it.

### Exit ticket
- Pinning trade-offs: strong against rogue CAs, brittle operationally (bricks your own app on rotation) — modern guidance prefers root programs/CT over app-level pinning except high-value apps.
- The unfinished business: 0-RTT replay, long-tail old versions, cert transparency blind spots — any two earn credit.

### Lab troubleshooting (TLS lab context)
- Handshake fails after server change: expired cert chain first, then missing intermediate, then cipher-suite mismatch order.
- Wireshark shows "Application Data" only: expected for TLS 1.3 (encrypted handshake) — use keylog file in the lab to decrypt for teaching purposes only.

## L15 — IPsec & Legacy VPN Architecture

### Formative checks
1. AH vs ESP: AH = integrity/authenticity of whole packet, no confidentiality, breaks with NAT (immutable fields); ESP = encryption (+optionally auth), NAT-friendly in tunnel mode. Modern answer: ESP tunnel mode, AH is effectively legacy.
2. Tunnel vs transport: tunnel wraps whole IP (site-to-site); transport protects payload between endpoints (rare now). Site-to-site = tunnel mode between gateways.
3. IKEv1 vs IKEv2: IKEv2 fewer round trips, built-in NAT-T, MOBIKE roaming, EAP auth support; IKEv1 aggressive mode = PSK hash exposure — the security delta is concrete.
4. Split tunnel: only corporate subnets via VPN (performance, convenience) vs full tunnel (all traffic, better control/visibility) — risk: split-tunnel endpoints sit on both networks simultaneously.
5. Legacy VPN decline: ZTNA/network-layer least privilege + identity-aware proxy replace monolithic network access; VPN still right for site-to-site and some admin paths.

### Exit ticket
- Phase 1 vs Phase 2: IKE SA (identity, keys for control channel) vs IPsec SAs (the actual traffic selectors/policies) — mixing them up is the classic exam error.
- Remote-access VPN limitations: flat network access, endpoint posture blind spots, lateral movement once connected — segue to L16.

### Lab troubleshooting (VPN lab context)
- Phase 1 up, Phase 2 down: mismatched traffic selectors/proxy IDs — check both sides' subnets exactly.
- Works until NAT: NAT-T negotiation absent — enable NAT-T and confirm UDP/4500.

## L16 — Modern VPNs & Crypto-Agility

### Formative checks
1. SSL/TLS-VPN vs IPsec: clientless portal (app-level, browser) vs full tunnel client; TLS-VPN traverses restrictive networks better, IPsec still strong site-to-site.
2. ZTNA contrast: per-application grants via identity-aware broker vs network-level access; no lateral movement, no flat "on the network" state — the *application* is the boundary, not the network.
3. Crypto-agility: algorithm/protocol versions swappable without redesign — concrete forms: cipher-suite config, certificate automation (ACME), PQC-ready libraries, inventory of crypto usage.
4. DEP failure: either peer down or reachability — VPN tunnel state, then routing, then ACL on the tunnel interface; debugging order matters.
5. SASE/convergence: network/security functions delivered from cloud PoPs (SWG, CASB, ZTNA, FWaaS) — the honest framing is delivery model, not magic.

### Exit ticket
- Zero-trust ≠ product: architecture pattern (verify explicitly, least privilege, assume breach) realized via identity-aware proxies, microsegmentation, continuous evaluation — "we bought ZT" is the misconception to catch.
- VPN isn't dead: site-to-site, OT/admin enclaves, vendor access with tight scoping — the *scope* changed, not the existence.

### Case study anchors (cs-037–cs-050) — grading pointers
- **cs-037–cs-041 (L13):** the E-A-I distinction must be explicit; crypto-misuse (nonces/IVs/salts) analyses earn distinction-level marks.
- **cs-042–cs-046 (L14/L15):** protocol-mechanism accuracy (handshake steps, phase structure) required; "it's encrypted" alone fails.
- **cs-047–cs-050 (L16):** ZTNA-vs-VPN answers must address lateral movement and per-app scoping; both-sides trade-offs required.

## Common misconceptions (module-level)
1. "Encryption provides authentication" — AEAD's tag authenticates *within a key relationship*; it does not establish *who* holds the key without a protocol (certs/PSK) — precision here is graded.
2. "TLS inspection is a free win" — it trades visibility for a privileged middlebox, breaks pinning, and has privacy/legal limits (L14).
3. "AES-256 is unbreakable so we're safe" — key management, implementation, and misuse break systems long before math does (L13/L16).
4. "VPN makes you secure" — a VPN relocates the boundary; everything after it (segmentation, identity, monitoring) still applies (L15/L16).
5. "Hash passwords with SHA-256" — use password-specific KDFs (Argon2id/bcrypt/scrypt/PBKDF2 with work factors); plain fast hashes are a finding, not a design (L13).
