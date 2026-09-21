# L18 — Enterprise Wireless & Rogue Defense

## 1. Learning Objectives

By the end of this session you can: (1) explain 802.1X roles over the air and why credentials never touch the wireless link; (2) contrast EAP-TLS vs PEAP-MSCHAPv2 by trust anchors and phishing exposure; (3) state WPA3-Enterprise specifics (PMF mandatory; SAE is *not* used — quiz bait); (4) design an enterprise deployment: RADIUS redundancy, certificate provisioning, dynamic VLANs, guest separation; (5) run a rogue-defense program: classification, wired-side correlation, governed containment.

## 2. Key Definitions

| Term | Definition |
|---|---|
| Supplicant / authenticator / auth server | Client / AP-WLC / RADIUS — the 802.1X roles |
| EAP-TLS | Certificate-based mutual authentication (strongest; needs PKI logistics) |
| PEAP-MSCHAPv2 | Password auth inside a TLS tunnel (ubiquitous; phishable when client validation is skipped) |
| RADIUS attributes | Policy payload on Access-Accept: VLAN, dACLs, session timeout |
| Dynamic VLAN | Identity-driven VLAN assignment at admission |
| WPA3-Enterprise | 802.1X auth + PMF mandatory + modern suites (GCMP); 192-bit mode option |
| WIPS | Wireless IPS — rogue/attack monitoring (dedicated sensors vs AP-integrated scan) |
| Containment | Actively deauthenticating a rogue — a *governed*, RF-legal action |

## 3. Detailed Explanations

### 3.1 802.1X over the air
Supplicant ↔ authenticator speaks EAPoL; authenticator ↔ RADIUS rides the **wired** network — so user credentials never touch the air (the PSK model's core defect solved). On Accept, RADIUS returns **attributes**: VLAN assignment, ACLs, timeouts — identity-driven segmentation (L09/L12 operationalized). Per-user keying means one compromised client ≠ keys for everyone.

### 3.2 EAP method selection
- **EAP-TLS:** mutual certificates; strongest; the anti-phishing property comes from *client-side server validation* — a fake AP cannot present a cert the client trusts. Cost: PKI + provisioning (MDM/SCEP/ACME automation).
- **PEAP-MSCHAPv2:** password inside a TLS tunnel; works everywhere. The phishing path: an evil twin *outside* TLS with a lookalike portal harvests passwords before PEAP ever starts; users who click through certificate warnings complete the theft. Client-side validation discipline is the actual defense.
- **EAP-TTLS:** inner-legacy flexibility; niche today.

### 3.3 WPA3-Enterprise specifics (precision!)
WPA3-Enterprise uses **802.1X** authentication — **SAE is the WPA3-*Personal* method, not Enterprise** (the most common quiz error). What Enterprise modernizes: **PMF mandatory**, GCMP suites, optional **192-bit mode** (GCMP-256/ECDSA) for high-assurance data classes, with real performance/support costs to justify.

### 3.4 Deployment design (the graded design skill)
- **RADIUS:** two+ servers behind a VIP; backend AD/LDAP or cert-CA; **accounting on** (session records are forensic evidence — L29).
- **SSID architecture:** CORPORATE (EAP-TLS, dynamic VLAN by group), GUEST (portal, client isolation, separate VLAN/egress — L12), IoT (MAB + isolation VLAN).
- **Certificate provisioning:** MDM-driven, automated renewal, revocation workflow for lost devices.
- **Roaming:** 802.11r/k/v for fast secure roam — misconfigurations produce auth storms (a helpdesk-visible failure pattern).

### 3.5 The rogue-defense program
1. **Classify:** neighbor AP (benign, out of scope) vs mis-associated employee device (policy) vs rogue/evil twin (attack) — different responses.
2. **Detect:** AP-side neighbor reports, WIPS sensors (dedicated radios cost scan duty-cycle; AP-integrated trades performance), and — the killer source — **wired-side correlation**: a BSSID seen over the air *and* a new unknown host on a switch port = the rogue is *bridging* your LAN.
3. **Respond:** locate (RSSI), decide containment (deauth authority = governance + RF-legal review), remove, post-mortem. Radio containment can interfere with neighboring lawful networks — policy before power.

## 4. Network Diagram: 802.1X + rogue correlation

```
 [Supplicant] ──EAPoL──► [AP/WLC] ──RADIUS──► [RADIUS/AD]
        ◄──── Access-Accept + VLAN attr (dynamic policy) ────┘
 credentials: never on the air (wired leg only)

 Rogue hunt:  over-the-air: BSSID X claims "CORP" (open!)
              on-the-wire: new MAC appears on switch port 24 same window
              ⇒ bridge confirmed ⇒ escalate per playbook (not auto-deauth)
```

## 5. Protocol Examples

- supplicant config fragment (lab): `network={ ssid="CORP" key_mgmt=WPA-EAP eap=TLS identity="user1@lab" client_cert=… private_key=… ca_cert=… }` — then read the RADIUS log: `Access-Accept`, `Tunnel-Private-Group-Id: 10`.
- Evil-twin evidence chain: survey shows clone with mismatched RSN; switch MAC table shows a new MAC on a wired port in the same time window.

## 6. Configuration Concepts (concept level)

- RADIUS redundancy + accounting; dynamic-VLAN group mapping table.
- MDM cert profiles: auto-enrollment, renewal window, revocation runbook.
- SSID policy sheet: auth method, PMF, VLAN, client isolation, band steering per SSID.

## 7. Security Implications

- Enterprise wireless = identity-based admission + per-user keys + policy-by-attribute.
- EAP-TLS makes the fake AP *fail visibly*; PEAP survives only with enforced client validation.
- Rogue defense is a program, not a product: classify, correlate wired-side, govern containment.

## 8. Realistic Organizational Scenario

**The airport prompt (running case).** Executives report odd credential prompts at an airport lounge; back at HQ, one account shows impossible-travel logins. Artifacts: a phone screenshot of the prompt, RADIUS logs showing zero corporate associations during the window, and a home-router manual. Your reconstruction: an evil twin *outside corporate RF* (why WIPS can't see it), why EAP-TLS would have made the prompt fail rather than harvest, response (reset, token revocation, traveler guidance), and the client hardening that prevents recurrence. Full case: **cs-057**; the enterprise build + planted-rogue hunt is the in-session lab (Lab-10 part 1, Pract-3).

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "WPA2-PSK with a long password ≈ enterprise" | One shared key for all; no per-user identity, attribution, or revocation. |
| "WPA3-Enterprise uses SAE" | No — SAE is Personal; Enterprise is 802.1X with PMF mandatory. |
| "PEAP is safe because of the TLS tunnel" | The tunnel protects the password *in transit*; fake portals harvest before TLS begins. |
| "WIPS catches everything" | Radio-only WIPS misses off-site clones; wired-side correlation finds bridges. |
| "Containment is always allowed" | Deauthing RF can hit neighbors; governance + legality first. |

## 10. Classroom Activities

1. **Enterprise build + rogue hunt (pairs):** configure an EAP-TLS supplicant against the range RADIUS; capture the Accept + assigned VLAN; then classify the planted rogue with the detection tree and write the wired-correlation evidence line.
2. **Method-selection debate:** managed fleet + PKI vs BYOD-heavy — choose and defend EAP-TLS vs PEAP.
3. **Rogue classification drill:** six scenario cards → neighbor / policy-violation / attack, with response each.

## 11. Problem-Solving Questions

1. Why do credentials still get phished under PEAP if the tunnel is strong — and which client setting is the real defense?
2. Your IoT fleet can't do EAP: design admission for 300 cameras (MAB + compensating controls).
3. Which data classes justify 192-bit WPA3-Enterprise, and what costs do you accept?
4. Who has authority to contain a suspected rogue on your campus, and what policy must exist first?
5. 802.11r improves UX but had implementation-risk history — how do you balance it in deployment?

## 12. Exit Ticket

1. On which leg do user credentials travel in 802.1X — air or wire? Why does it matter?
2. Which EAP method relies on client certificate validation as its anti-phishing anchor?
3. True/false: WPA3-Enterprise uses SAE. Correct the statement.
4. Name the evidence pairing that proves a rogue AP is bridging the wired network.
5. Which RADIUS attribute typically enforces identity-based VLAN assignment?

*(Answers: `the instructor answer-key collection (not published)`.)*

## 13. References

- IEEE 802.1X / 802.11-2020 (RSNA, PMF).
- RFC 3748 (EAP); RFC 5216 (EAP-TLS); RFC 2865/2866 (RADIUS).
- Wi-Fi Alliance — WPA3-Enterprise overview.
- FreeRADIUS documentation — EAP-TLS and dynamic VLAN examples.
- NIST SP 800-153 — wireless infrastructure security.

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-8 | §3 design + rogue program | Pract-3 (W10), Lab-10, Quiz 4 (W10), Case set C |
