---
lecture: L18
title: Enterprise Wireless & Rogue Defense
module: 5
week: 10
hours: 2
clos: [CLO-8]
difficulty: intermediate-advanced
status: complete
artifact-type: teaching-plan
---

# L18 — Enterprise Wireless & Rogue Defense

## 1. Overview & Prerequisites

- **Prerequisites:** L17 (802.11 mechanics, security modes, survey skills), L12 (802.1X/NAC — same architecture, wireless air).
- **Position:** completes the wireless arc: PSK → Enterprise identity auth, plus the rogue-detection program. Quiz 4 (W10) covers L17–L18 + L19–L20 cloud items; Pract-3 (W10) is the wireless build.
- **Faculty prep:** stand up range RADIUS (FreeRADIUS) with test EAP-TLS client certs; prepare one rogue-candidate AP on a non-overlapping channel *inside the range only* for detection practice.
- **Common misconceptions:** "WPA2-PSK with a long password ≈ enterprise security"; "802.1X is only for corporate laptops"; "WIPS catches everything."

## 2. Learning Objectives

By the end of this lecture, students can:

1. Explain the 802.1X roles over the air (supplicant/authenticator/AP/auth-server) and why the RADIUS leg must live on the wire (Understand).
2. Contrast EAP methods (EAP-TLS, PEAP-MSCHAPv2, EAP-TTLS) by trust anchors, credential exposure, and deployment cost (Analyze/Evaluate).
3. Describe WPA3-Enterprise differences (192-bit mode, PMF requirement, GCMP) and when 192-bit mode actually matters (Understand/Analyze).
4. Design the enterprise wireless deployment: RADIUS redundancy, certificate provisioning, dynamic VLAN/role mapping, guest separation (Create).
5. Build the rogue-defense program: rogue classification (benign/neighbor/evil), detection sources (AP scan, WIPS, wired-side correlation), and response playbook (Create/Evaluate).

## 3. Detailed Concepts

### 3.1 802.1X over the air
- Supplicant (client) ↔ authenticator (AP/WLC) via EAPoL; authenticator ↔ RADIUS over the *wired* network → user credentials never touch the air; session keys derived per-user (PMK from RADIUS MSK).
- Per-user keying consequence: compromise of one client ≠ keys for all (the PSK defect solved).
- RADIUS attributes drive policy: VLAN assignment, ACLs/dACLs, session timeout, dynamic roles — identity-based segmentation (L09/L12 continuation).

### 3.2 EAP method selection
- **EAP-TLS:** mutual certificate auth; strongest; cost = PKI + provisioning (SCEP/ACME-class automation); MDM typically distributes.
- **PEAP-MSCHAPv2:** password-based inside TLS tunnel; ubiquitous but exposed to credential-phishing proxies (evil-twin + captive fake portal harvesting credentials); requires certificate validation discipline on clients (users click through = game over).
- **EAP-TTLS:** inner legacy auth flexibility; niche in modern deployments.
- Decision frame: managed fleet + PKI → EAP-TLS; unmanaged/BYOD → PEAP with hard client-config enforcement or move to MFA-web-auth flows.

### 3.3 WPA3-Enterprise specifics
- PMF mandatory; GCMP-256/ECDSA suites in 192-bit mode (for high-assurance contexts; most orgs run 128-bit suites fine); SAE not used in enterprise (Enterprise uses 802.1X auth as before — WPA3-Enterprise is mostly PMF+suite modernization; the "WPA3 = SAE" conflation is a common student error — quiz bait).
- Transition realities: driver support, mixed-client floors, controller/ROAMING behavior (PMF + fast transition).

### 3.4 Deployment design (the graded design skill)
- RADIUS: two+ servers, LB/VIP, backend = AD/LDAP or cert-CA; accounting on (session evidence for forensics — L29 tie).
- SSID architecture: CORPORATE (EAP-TLS, dynamic VLAN by group), GUEST (portal, client isolation, rate caps, separate VLAN/egress — L12 policy), IoT (MAB + isolation VLAN from L12).
- Certificate provisioning: MDM-driven, renewal automation, revocation workflow for lost devices.
- Roaming: 802.11r/k/v for fast secure roam; misconfigurations cause auth storms (helpdesk evidence pattern).

### 3.5 Rogue defense program
- Classification: neighbor AP (benign, out of scope), misassociated employee device (policy), rogue/evil twin (attack) — different responses.
- Detection sources: AP-side spectrum/neighbor reports, WIPS sensors (dedicated radios vs AP-integrated scan duty-cycle cost), wired-side correlation (rogue bridging wired LAN = the real danger: BSSID seen *and* a new host on a switch port).
- Response playbook: locate (RSSI triangulation/BLE-like hinting), isolate (contain/deauth authority = governance question!), remove, and post-mortem.
- Governance caution: "containment" deauths RF traffic — legal/policy boundaries in shared spectrum; escalate before containing.

## 4. Teaching Sequence (120 Minutes)

| Time | Segment | Instructor moves |
|---|---|---|
| 0–10 | Recap: L17 survey sheets | One finding → "how would enterprise auth have changed it?" |
| 10–35 | Core: 802.1X over air + EAP methods | Role diagram; RADIUS attribute table; PEAP-phishing vignette |
| 35–55 | Core: WPA3-Enterprise + deployment design | Design checklist walk; dynamic-VLAN example table; roaming pitfalls |
| 55–65 | Break | — |
| 65–90 | Core: rogue program | Classification tree; wired-side correlation demo (range: rogue AP bridging shown via switch-port + BSSID pairing) |
| 90–110 | Student activity: WPA-Enterprise build + rogue hunt | Pairs: EAP-TLS supplicant auth against range RADIUS; then classify the planted rogue (Lab-10 part 1; cs-057..060 prep) |
| 110–120 | Wrap + formative | Exit ticket; **Quiz 4 administration** (10 min, end-of-slot); Pract-3 reminder; L20 trailer |

## 5. Technical Examples

```
# Range RADIUS + EAP-TLS client (read-only observation):
# wpa_supplicant config (fragment):
#   network={ ssid="CORP" key_mgmt=WPA-EAP
#             eap=TLS identity="user1@lab"
#             client_cert="/etc/certs/user1.crt" private_key="/etc/certs/user1.key"
#             ca_cert="/etc/certs/lab-root.crt" }
# journalctl -u freeradius | tail     # Access-Accept + Tunnel-Private-Group-Id: VLAN 10

# Verify identity-driven policy:
#   show authentication sessions int Gi0/8    (wired side anchor from L12)
#   → status AUTHORIZED, VLAN 10 assigned by RADIUS attribute.

# Rogue hunt evidence (range-only planted AP):
#   airmon/airodump survey → BSSID X claims SSID "CORP" with OPEN auth mode
#   switch MAC table: new MAC on port 24 same time-window  ← wired-side bridge!
# Teaching point: radio-only WIPS would misclassify; correlation finds the bridge.
```
Expected teaching points: credentials never on the air; RADIUS attribute = policy enforcement point; the wired-port correlation is the killer evidence.

## 6. Discussion Questions

1. Why do credentials still get phished under PEAP if the tunnel is strong? What client-side setting is the actual defense?
2. Your IoT fleet can't do EAP. Design the admission path for 300 cameras (MAB + what compensating controls?).
3. 192-bit WPA3-Enterprise: which data classes justify it, and what performance/support cost do you accept?
4. Who has authority to *contain* (deauth) a suspected rogue on your campus? What policy must exist first?
5. Fast-roaming (802.11r) improves UX but had implementation-risk history — how do you balance it in deployment?

## 7. Student Activity

**Enterprise build + rogue hunt (20 min, pairs):** (a) configure an EAP-TLS supplicant profile against the range RADIUS, capture the Access-Accept and note the assigned VLAN; (b) survey the range, find the planted rogue candidate, classify it using the detection tree, and write the one-line wired-correlation evidence. Deliverable feeds Pract-3 (W10) and Lab-10.

## 8. Problem-Solving Case

**Primary case — cs-057 "Evil-twin AP detection and response" (intermediate-advanced):**
Several executives report credential prompts on their phones at the airport lounge; back at HQ, one account shows impossible-travel logins. Provided: phone screenshot of the SSID prompt, RADIUS logs showing zero corporate associations during the window, and a user's home-lab router manual. Students must (a) reconstruct the attack (evil-twin harvesting outside corporate RF — why WIPS can't see it), (b) explain why EAP-TLS would have made the prompt *fail* rather than harvest (server-cert validation), (c) design the response (credential reset, token revocation, traveler guidance), and (d) propose the client hardening that prevents recurrence.
**Linked cases:** cs-058 (rogue-AP building hunt), cs-059 (802.1X/EAP deployment plan), cs-060 (WPA3 transition triage).
*(Model solutions: instructor answer-key set, Module 5.)*

## 9. Formative Assessment

1. On which leg do user credentials travel in 802.1X — air or wire? Why does that matter?
2. Which EAP method relies on client certificate validation as its anti-phishing anchor?
3. True/false: WPA3-Enterprise uses SAE. Correct the statement.
4. Name the evidence pairing that proves a rogue AP is *bridging* the wired network.
5. What RADIUS attribute typically enforces identity-based VLAN assignment?
*(Answer key: instructor set, Module 5.)*

## 10. Summary & Key Takeaways

- Enterprise wireless = identity-based admission (802.1X) + per-user keys + policy-by-attribute.
- EAP-TLS is the anti-phishing endpoint; PEAP survives only with enforced client validation.
- Rogue defense is a *program*: classify, correlate wired-side, govern containment.

## 11. References

- IEEE 802.1X/802.11-2020 — RSNA and PMF requirements.
- RFC 3748 — EAP; RFC 5216 — EAP-TLS; RFC 2865/2866 — RADIUS auth/acct.
- Wi-Fi Alliance — WPA3-Enterprise specification overview.
- FreeRADIUS documentation — EAP-TLS module & dynamic VLAN examples (current docs).
- NIST SP 800-153 — wireless infrastructure security guidelines.

## 12. CLO Mapping

| CLO | Where in this lecture | Assessed via |
|---|---|---|
| CLO-8 | §3.1–3.5 enterprise design + rogue program; build/hunt §7 | Pract-3 (W10), Lab-10, Quiz 4 (today), Case set C |
