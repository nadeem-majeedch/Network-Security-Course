# L17 — Wireless Fundamentals & Threats

> **Scope and safety note:** wireless observation happens only on the instructor's
> authorized lab APs. Capturing or analyzing networks you do not operate/own — or
> attempting to crack anything — is outside course scope and, outside a lab, illegal.

## 1. Learning Objectives

By the end of this session you can: (1) describe 802.11 frame families and the unauthenticated-history of management frames (and PMF's fix); (2) explain the 4-way handshake's real purpose (PMK confirmation — the password never crosses the air) and why the observable handshake enables offline guessing; (3) trace WEP→WPA3 evolution by the *break* that drove each change; (4) classify wireless threat classes and their evidence; (5) characterize a survey capture (RSN IE, PMF status, BSSID anomalies).

## 2. Key Definitions

| Term | Definition |
|---|---|
| Beacon / Probe | Management frames advertising/requesting network presence |
| 4-way handshake | EAPOL exchange confirming the PMK and deriving per-session keys (PTK) |
| PMK / PTK | Pairwise Master Key (from auth) / Pairwise Transient Key (per session) |
| WEP / TKIP / CCMP / GCMP | Cipher generations: broken / stopgap / WPA2 baseline / WPA3 |
| SAE | Simultaneous Authentication of Equals — WPA3's dictionary-resistant PSK replacement |
| PMF (802.11w) | Protected Management Frames — authenticates deauth/disassoc-class frames |
| RSN IE | Robust Security Network Information Element — the beacon field stating security mode |
| Rogue / evil twin | Unauthorized AP / malicious clone of a legitimate SSID |
| WIDS/WIPS | Wireless (Intrusion) Detection/Prevention — rogue and attack monitoring |

## 3. Detailed Explanations

### 3.1 802.11 mechanics that matter for security
Three frame families: **management** (beacons, probes, auth/assoc — historically *unauthenticated*), **control** (ACK/RTS/CTS), **data** (protected by the security mode). Because management frames were unauthenticated, anyone could forge deauthentications — **PMF (802.11w)** authenticates them and is mandatory in WPA3. Spectrum realities shape defense: 2.4 GHz congestion/overlap vs 5/6 GHz cleanliness; and probe requests leak device identity (MAC randomization is the privacy response — with policy consequences).

### 3.2 Association and the 4-way handshake
Association differs by mode (open/PSK/enterprise). For PSK, the **4-way handshake** lets AP and client prove they share the PMK and derive fresh per-session keys (PTK): two nonces (ANonce/SNonce) exchanged via EAPOL frames. **The password never crosses the air.** But the handshake is *observable*, so an attacker who records it can try dictionary guesses offline — the exact weakness WPA3's **SAE** (dragonfly commit-exchange) removes. Handshake capture ≠ credentials; it is a *guessing oracle* against weak passphrases.

### 3.3 The evolution: every row has a break
| Mode | Cipher/auth | The break that motivated the change |
|---|---|---|
| WEP | RC4, static IV | IV reuse + weak RC4 usage → FMS/PTW breaks; dead |
| WPA (TKIP) | RC4-based wrapper | Stopgap on old hardware; deprecated/withdrawn |
| WPA2 (CCMP) | AES-CCMP | The 15-year baseline; KRACK (2017) showed *implementation* matters (client-side nonce reinstatement) — patch discipline |
| WPA3-Personal | SAE + GCMP | PSK offline-guessing removed; early SAE side channels → keep firmware current; **transition mode keeps WPA2 alive** (downgrade exposure during migration) |
| WPA3-Enterprise | 802.1X + PMF required | Mostly modernization: PMF mandatory, 192-bit suite option (L18) |

### 3.4 Threat classes and their evidence
- **Eavesdropping:** open networks, legacy ciphers — read what flows (L07 patterns in the air).
- **Rogue AP / evil twin:** clone SSID on attacker hardware; evidence: two BSSIDs claiming one SSID; RSN mismatch between them (downgrade bait).
- **Deauth/disassociation:** management-frame abuse forcing reconnects (handshake harvesting, DoS); PMF closes the classic vector; detect via frame-rate anomalies.
- **WPS:** PIN brute-force class — disable by policy.
- **Implementation flaws:** KRACK and FragAttacks history — firmware currency is a control.

### 3.5 Reading a survey capture
From beacons, read the **RSN IE**: pairwise ciphers (CCMP/GCMP), AKM suites (PSK/SAE/802.1X), **PMF capability**. Client story: association churn, probe patterns, failure loops. Anomaly cues: identical SSID on two BSSIDs (rogue candidate), one SSID with *different* security IEs, high deauth rates.

## 4. Network Diagram: the 4-way handshake

```
 Client                                AP
   |◄──[1] ANonce──────────────────────|
   |───[2] SNonce + MIC───────────────►|   (both derive PTK from PMK+nonces)
   |◄──[3] GTK + MIC (encrypted)───────|
   |───[4] ACK/MIC────────────────────►|   group key delivered; session keys live
 Password: never on the air. Observable frames ⇒ offline guessing vs weak PSKs.
 WPA3-SAE replaces steps 0 (initial auth) with a dictionary-resistant exchange.
```

## 5. Protocol Examples

- Survey read (Wireshark): filter `wlan.fc.type_subtype == 8` (beacons); columns `wlan.ssid`, `wlan.bssid`, RSN cipher/AKM/PMF fields → produce the network inventory (Lab-09).
- Rogue-candidate evidence: SSID "CORP" on BSSID X with **open** auth vs the real network's WPA2/3 — the RSN mismatch is the tell.

## 6. Configuration Concepts (concept level)

- Security-mode policy: WPA2-CCMP floor, WPA3-SAE where clients allow; PMF enabled; WPS disabled.
- Transition-mode migration plan: WPA2/WPA3 mixed → WPA3-only per building (L18 builds the enterprise version).
- Camera/IoT SSID: separate VLAN + isolation (their firmware won't move fast — contain it).

## 7. Security Implications

- Wireless is L2 in the air: same attack logic as L06–L07, new evidence format (beacons, IEs, EAPOL).
- Security modes evolve by *breaks* — knowing the break tells you what the mode actually fixes.
- Survey-reading (RSN IE, PMF, BSSID correlation) is the entry skill for both defense and rogue hunting.

## 8. Realistic Organizational Scenario

**The campus floor (running case).** One WPA2-PSK SSID for staff, a hidden SSID for cameras running a legacy TKIP profile, open guest with an HTTP captive portal; 40% of clients crowding 2.4 GHz channel 6 with high retries. You rank the three findings with evidence, design the WPA2→WPA3 transition phases, isolate the camera SSID, fix the portal, and define ongoing rogue detection. Full case: **cs-054**; the survey characterization is Lab-09 part 1.

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "Hidden SSIDs are secure" | Beacons/probes still leak; hiding breaks clients, not attackers. |
| "The password travels during connection" | The 4-way handshake exchanges nonces; the PSK never crosses the air. |
| "WEP is gone so legacy doesn't matter" | Printers, sensors, and "temporary" networks still run TKIP/WEP — audit them. |
| "WPA3 is immune to attacks" | SAE removes offline PSK guessing; implementation and transition-mode weaknesses remain. |
| "MAC filtering adds real security" | MACs are trivially spoofed (and randomized by phones) — use 802.1X (L18). |

## 10. Classroom Activities

1. **Survey characterization (pairs):** range capture → network inventory per BSSID (SSID, channel, security mode from RSN IE, PMF, client estimate); flag two rogue/misconfig candidates with evidence lines.
2. **Evolution-table drill:** given a break (IV reuse, KRACK, offline dictionary), name the mode that answered it.
3. **Handshake annotation:** label the four EAPOL frames and state what each contributes.

## 11. Problem-Solving Questions

1. Why does hiding an SSID not reduce attack surface, and what does it break operationally?
2. WPA3 transition mode keeps WPA2 alive — what downgrade exposure does that create, and how do you phase it out?
3. What attack class does PMF close, and what breaks first when you enable it?
4. MAC randomization on phones: what breaks in network policy, and what replaces it?
5. If offline dictionary attacks are the PSK weakness, why hasn't every network moved to WPA3-Enterprise?

## 12. Exit Ticket

1. Which frame family carries beacons, and why was it historically unauthenticated?
2. Does the client ever transmit the PSK in the 4-way handshake? What do the nonces produce?
3. Name the break that motivated each: WEP→WPA, WPA2→WPA3.
4. Which management-frame attack does PMF mitigate?
5. Which three RSN-IE fields state a network's security posture?

*(Answers: `the instructor answer-key collection (not published)`.)*

## 13. References

- IEEE 802.11-2020 — security sections (RSNA, PMF/802.11w).
- Wi-Fi Alliance — WPA3 specification overview (SAE, PMF).
- KRACK (Vanhoef & Piessens, 2017) and FragAttacks (2021) advisories — implementation lessons.
- Wireshark wiki — 802.11 IE field reference.
- NIST SP 800-153 — wireless infrastructure security guidelines.

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-8 | §3 fundamentals + survey skill | Lab-09 (W9), Quiz 4 (W10), Case set C |
