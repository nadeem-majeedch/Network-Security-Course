---
module: 2
lectures: [L05, L06, L07, L08]
status: complete
artifact-type: answer-key
instructor-only: true
distribution: never-publish-to-students
---

# Answer Key — Module 2: Network Threats & Attack Concepts

> **INSTRUCTOR ONLY — contains model answers to graded formative assessments.**
> Links: Plans `modules/module-02-network-threats/lectures/` · Student pages `docs/lectures/lecture-05…08` · Notes `teaching/speaker-notes/lecture-05…08-speaker-notes.md`

## L05 — Threat Modeling & Attacker Anatomy

### Formative checks (plan §11)
1. STRIDE mapping: spoofing = identity claims; tampering = integrity; repudiation = auditability; information disclosure = confidentiality; DoS = availability; EoP = authorization. Any defensible mapping with the *element named* earns credit.
2. Asset-first: "What are we protecting, and what does its loss cost?" — tool-first answers lose half credit (rubric consistent with L01).
3. DFD: external entities, processes, data stores, **trust boundaries** — a DFD without boundaries isn't a threat-model diagram.
4. Kill chain / MITRE ATT&CK: chain = sequential stage model; ATT&CK = behavioral matrix post-compromise — accept any accurate contrast; penalize "ATT&CK is the new kill chain".
5. Tabletop: no live systems touched — decisions, communications, and gaps are the outputs.

### Exit ticket
- Trust boundary crossings are where attackers interpose — spoof/MITM/tampering live at interfaces, not inside components.
- ATT&CK technique phrase, e.g., "Adversary-in-the-Middle (T1557)" — exact IDs not required, the *behavior family* is.

### Discussion facilitation
- Q2 (ATT&CK as defense tool): detection coverage mapping, purple-team exercises, gap analysis — reward *operational* uses over "we read it".
- Q4 (recon defense): reduce exposure (minimize outward fingerprints), but the honest answer is "recon can't be prevented, only limited and monitored".

## L06 — Layer-2 / LAN Attacks

### Formative checks
1. MAC flooding: fills the switch CAM table → switch floods unknown-unicast → sniffing window; mitigations: port security, 802.1X, storm control. Reject "crashes the switch".
2. ARP spoofing: unsolicited/answered ARP replies poison neighbor caches → MITM; mitigations: Dynamic ARP Inspection (with DHCP snooping binding table), static ARP for critical hosts.
3. STP root claim: attacker advertises superior bridge priority → becomes root → traffic transits attacker; mitigations: root guard, BPDU guard on access ports.
4. DHCP starvation: exhaust the pool (many leases) → attacker runs a rogue DHCP server; mitigations: DHCP snooping (trust boundary on ports), port security limiting MACs.
5. VLAN-hopping: double-tagging exploits native-VLAN mismatch; mitigations: change native VLAN, tag it explicitly, disable auto-trunking (DTP off).

### Exit ticket
- Root cause: L2 protocols assume a *cooperative* LAN (no authentication of ARP/STP/DHCP claims) — "trust by adjacency" is the phrase to reward.
- Snooping + DAI pairing: snooping builds the IP→MAC binding table; DAI validates ARP against it — they are a pair, not alternatives.

### Lab troubleshooting (switching lab context)
- "No mitigation works": most common cause is applying protections on trunk ports instead of access ports — check the trust direction.
- PCAP shows flood but no attacker MAC: CAM already poisoned before capture start — reset the lab switch and re-run.

## L07 — Sniffing, MITM & Session Attacks

### Formative checks
1. Promiscuous vs monitor mode: promiscuous = all frames *on the wired segment you're attached to*; monitor = 802.11 radio frames without association. Promiscuous ≠ seeing the whole LAN (switches limit that).
2. Session hijack: steal/replay session tokens (cookies) → impersonate without credentials; mitigations: TLS everywhere, Secure/HttpOnly cookie flags, short session lifetimes, re-authentication on sensitive actions.
3. TLS 1.2 MITM gap: the certificate step is where server identity is proven; an unvalidated cert (user clicks through) voids it. SSL-strip exploits the *first-hop downgrade*, not TLS math.
4. DHCP/DNS MITM: rogue DHCP hands out attacker DNS → names resolve to attacker; mitigations: DHCP snooping, DNSSEC (origin authenticity), DoH/DoT (transit confidentiality).
5. HSTS: forces HTTPS for subsequent visits, defeating first-visit downgrade — the first-visit gap remains (hence preload lists).

### Exit ticket
- "HTTPS defeats MITM" is *conditional*: true when certificates are validated and no user override; the strip/portal attacks live in the gap before/around TLS. Reward nuance.
- Both, because they differ: TLS protects confidentiality/integrity in transit; certificate pinning/HSTS reduce downgrade exposure.

### Ethics & safety gate (must appear in every L07 grading pass)
Attack demonstrations are run **only** in the isolated lab range against attack targets the students own. Any writeup suggesting out-of-lab application of active MITM tooling loses all safety marks — this is course policy, stated in the syllabus.

## L08 — DoS, DDoS & Infrastructure Abuse

### Formative checks
1. Volumetric vs application-layer: L3/L4 floods exhaust bandwidth/conn-tables (SYN flood, amplification); L7 exhausts application logic (slowloris, expensive queries). Volumetric = bigger pipes/scrubbing; L7 = app-level rate limiting/validation.
2. Amplification arithmetic: response size ÷ request size = multiplier; reflector = third party used. DNS (UDP/53 ANY), NTP monlist, memcached (largest known) — the *UDP spoofability* is the enabler; TCP can't be spoofed this way (handshake).
3. SYN flood: half-open connections exhaust backlog; mitigations: SYN cookies, backlog tuning, upstream filtering — reject "patch the server" as sufficient.
4. Botnet economics: rental markets, bulletproof hosting, IoT default credentials — the *economics* answer earns more than the *zombies* answer.
5. Rate limiting limits: naive per-IP limits break NATted offices and shared mobile CGNAT — the collateral question has no clean answer; reward the trade-off articulation.

### Exit ticket
- Amplification is cheap because spoofed UDP + small-request/large-response = attacker bandwidth multiplied; BCP 38 (source-address validation) at networks is the structural fix — accept "egress filtering" with BCP 38 named.
- The critical question: what does *availability loss actually cost this org per hour?* — that number, not the bit-rate, drives response.

### Discussion facilitation
- Q3 (ISP vs local mitigation): upstream scrubbing is inevitable at volumetric scale; local controls still handle L7 — the layered answer wins.
- Q5 (CDN dependency): new single point of failure + new abuse surface (origin exposure) — reward students who name *both* sides.

## Common misconceptions (module-level)
1. "The tool is the attack" — a tool name without the protocol mechanism earns nothing; every L06/L07 answer must name the exploited trust gap (ARP cache trust, unauthenticated management frames, etc.).
2. "Sniffing sees everything." Corrective: switches limit promiscuous capture to broadcast/unknown-unicast — flooding/MITM is how attackers widen that window (L06→L07 link).
3. "DDoS defense starts at the server." Corrective: volumetric attacks must be absorbed upstream (scrubbing, anycast); server tuning only handles L7 residue (L08).
4. "Recon is illegal per se." Corrective: passive observation of public exposure is generally lawful; active probing without authorization is not — the authorization boundary is the teaching line (L05/L07).

## Case study anchors (cs-015–cs-026) — grading pointers
- **cs-015–cs-018 (L05):** threat models must show trust boundaries; asset-loss framing mandatory.
- **cs-019–cs-022 (L06/L07):** mechanism accuracy required (which protocol, which trust gap); generic "hacking" language loses marks.
- **cs-023–cs-026 (L08):** cost-of-downtime quantification expected; mitigation must match attack layer.
