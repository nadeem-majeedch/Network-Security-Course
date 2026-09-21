---
lecture: L17
title: Wireless Fundamentals & Threats
module: 5
week: 9
hours: 2
clos: [CLO-8]
difficulty: intermediate-advanced
status: complete
artifact-type: teaching-plan
---

# L17 — Wireless Fundamentals & Threats (Teaching Plan)

## 1. Overview & Prerequisites

- **Prerequisites:** L04 (capture/analysis fluency), L06 (L2 attack reasoning — wireless is L2 in the air). L07 (MITM classes — evil-twin is their wireless form).
- **Position:** Module 5 opens with the RF/protocol reality that determines everything in L18 (enterprise auth) and the wireless half of the capstone hardening. Ethics note: all observation happens on instructor-controlled APs in the range.
- **Faculty prep:** configure range APs (one WPA2-PSK, one WPA3-SAE, one open-captive); pre-capture association/4-way-handshake samples for analysis; verify monitor-mode adapters.
- **Common misconceptions:** "hidden SSIDs are secure"; "WEP is gone so legacy doesn't matter"; "MAC filtering adds real security"; "WPA3 is immune to offline attacks."

## 2. Learning Objectives

By the end of this lecture, students can:

1. Describe 802.11 frame families (management/control/data) and the unauthenticated-in-the-clear nature of management frames (Understand).
2. Explain the association flow and the 4-way handshake's actual purpose (PMK confirmation — not password transmission) (Analyze).
3. Trace the WEP → WPA → WPA2 (CCMP) → WPA3 (SAE, GCMP) evolution, naming the break that motivated each change (Analyze).
4. Classify wireless threat classes: eavesdropping, rogue/evil-twin AP, deauth/disassociation (management-frame abuse), KRACK-class implementation flaws, WPS weaknesses (Analyze).
5. Characterize a wireless capture: identify networks, security modes, and anomalies (client-churn, beacon anomalies) from a lab survey capture (Apply).

## 3. Detailed Concepts

### 3.1 802.11 mechanics that matter for security
- Frames: management (beacons, probes, auth/assoc), control (RTS/CTS, ACK), data; management frames historically unauthenticated (protected-management-frames, PMF/802.11w, is the fix — WPA3 requires it).
- Channels/bands intuition: 2.4 GHz congestion + overlap vs 5/6 GHz; implications for rogue detection and survey design.
- Probe requests: passive leaking of device identity/previous SSIDs (privacy angle; MAC randomization reality).

### 3.2 Association + the 4-way handshake
- Open/WEP/PSK/Enterprise association differences; open-network captive portals as an *authorization* layer only.
- 4-way handshake (PSK case): AP↔client exchange nonces → derive PTK; **the password never crosses the air**; offline dictionary attacks are possible because the handshake is observable → dictionary-resistant SAE is the WPA3 answer.
- Handshake capture ≠ password capture: what students may and may not infer from captures (ethics + accuracy).

### 3.3 Security-mode evolution and its breaks
- WEP: static keys + RC4 IV reuse → broken (FMS/PTW); killed.
- WPA (TKIP): stopgap on old hardware; deprecated, formally withdrawn.
- WPA2 (CCMP/AES): the 15-year baseline; KRACK (client-side nonce reinstallation, 2017) showed *implementation* matters; patching discipline required.
- WPA3: SAE (dragonfly) replaces PSK handshake (offline-dictionary resistant), GCMP suites, PMF required, H2E (hash-to-element) fixing side channels; transition-mode caveats (downgrade exposure), early SAE side-channel research → why PMF + current firmware matters.

### 3.4 Threat classes (the detection catalog)
- Eavesdropping: open networks, cleartext legacy; consequence framing (L07 patterns in the air).
- Rogue AP / evil twin: same SSID, attacker's BSS; detection: BSSID/signal correlation, beacon anomalies; enterprise answer in L18 (802.1X + WIPS).
- Deauth/disassociation: management-frame abuse → forced reconnection (handshake harvesting, DoS); PMF closes the classic vector; detect via frame-rate anomalies.
- WPS: PIN brute-force class; disable WPS policy.
- Implementation classes: KRACK-history, Fragment-and-Assemble (802.11 frames reassembly flaws) — the lesson: firmware currency is a control.

### 3.5 Reading a survey capture
- Beacon inventory: SSID/BSSID/RSN IE (cipher suites, AKM suites, PMF capability).
- Client story: association churn, probe patterns, failure sequences (assoc-then-deauth loops).
- Anomaly cues: two BSSIDs one SSID (rogue candidate), beacons with identical SSID but different RSN ( downgrade-bait), high deauth rates.

## 4. Teaching Sequence (120 Minutes)

| Time | Segment | Instructor moves |
|---|---|---|
| 0–10 | Warm-up: spectrum picture | Show a channel-overlap plot; why 2.4 GHz is the wild west |
| 10–35 | Core: frames + handshake | Annotate the 4-way handshake capture live; correct the "password on the air" myth |
| 35–55 | Core: evolution table | WEP→WPA3 table with the *break* that drove each row; KRACK story: design vs implementation |
| 55–65 | Break | — |
| 65–85 | Core: threat classes + PMF | Deauth demo description (no live attack — video/capture evidence); PMF as the control |
| 85–110 | Student activity: survey capture characterization | Pairs analyze the survey capture, fill the network inventory sheet (Lab-09 part 1; cs-054..056 prep) |
| 110–120 | Wrap + formative | Exit ticket; L19 same-week trailer: "wired zones → cloud zones"; Quiz-4 reminder (W10) |

## 5. Technical Examples

```
# Monitor-mode survey on range adapter (lab only):
sudo airmon-ng start wlan0           # → wlan0mon
sudo airodump-ng wlan0mon -w survey  # observe: BSSID, PWR, beacons, #Data, WPA3/WPA2 labels
# Read-only analysis of the saved survey file in Wireshark:
#   filter: wlan.fc.type_subtype == 8        (beacons)
#   fields:  wlan.ssid, wlan.bssid, rsn.pcs, rsn.akms, rsn.pmf
# Teaching points: RSN IE tells the security mode; two BSSIDs claiming one SSID
#   = rogue-candidate flag; PMF bit absent = deauth-vulnerable legacy profile.

# 4-way handshake frames (pre-captured, no live cracking):
#   EAPOL frames 1-4: ANonce/SNonce → PTK derivation; explain why offline guessing
#   is possible (handshake observable) and why WPA3-SAE changes that (dragonfly commit).
```
Expected teaching points: security mode is read from Information Elements, not SSID names; handshake knowledge ≠ credentials.

## 6. Discussion Questions

1. Why does hiding an SSID not reduce attack surface? What does it break operationally?
2. WPA3 transition mode keeps WPA2 alive for old clients. What downgrade exposure does that create, and how do you phase it out?
3. PMF wasn't required in WPA2. What attack class does enabling it close, and what breaks first when you turn it on?
4. MAC randomization on phones: what breaks in network policy (MAC allowlists, DHCP reservations), and what should replace them?
5. If offline dictionary attacks are the PSK weakness, why hasn't every network moved to WPA3-Enterprise?

## 7. Student Activity

**Survey characterization (25 min, pairs):** from the range survey capture, complete a network inventory: per BSSID — SSID, band/channel, security mode (from RSN IE), PMF status, client count estimate; flag two rogue-candidate or misconfiguration findings with evidence lines. Deliverable feeds Lab-09 and the L18 enterprise build.

## 8. Problem-Solving Case

**Primary case — cs-054 "WPA2-PSK wireless audit of a campus floor" (intermediate-advanced):**
A campus floor runs one WPA2-PSK SSID shared by staff, a second "hidden" SSID for IoT cameras, and open guest with captive portal. A survey capture shows: camera SSID using TKIP (legacy profile), guest portal over HTTP, and 40% of clients on 2.4 GHz channel 6 with high retry rates. Students must (a) rank the three findings by risk with evidence, (b) design the migration plan (WPA2→WPA3 transition phases, camera-SSID isolation VLAN), (c) specify guest-network controls (client isolation, portal over HTTPS), and (d) define the ongoing rogue-detection approach for the floor.
**Linked cases:** cs-055 (open guest Wi-Fi containment), cs-056 (WEP legacy retirement).
*(Model solutions: instructor answer-key set, Module 5.)*

## 9. Formative Assessment

1. Which 802.11 frame family carries beacons, and why was it historically unauthenticated?
2. In the 4-way handshake, does the client ever transmit the PSK? What do the nonces produce?
3. Name the break that motivated each: WEP→WPA, WPA2→WPA3-SAE.
4. What management-frame attack does PMF mitigate?
5. From a beacon, which three RSN-IE fields tell you the network's security posture?
*(Answer key: instructor set, Module 5.)*

## 10. Summary & Key Takeaways

- Wireless is L2 in the air: same attack logic, new evidence (beacons, IEs, handshake frames).
- Security modes evolve by *breaks*: WEP (IV reuse) → TKIP stopgap → CCMP baseline → SAE dictionary-resistance.
- Survey-reading (RSN IE, PMF, BSSID correlation) is the entry skill for both defense and rogue hunting.

## 11. References

- IEEE 802.11-2020 standard — security sections (RSNA, PMF/802.11w).
- Wi-Fi Alliance — WPA3 specification overview (SAE, PMF requirement).
- RFC-era KRACK disclosures (Vanhoef & Piessens 2017) and FragAttacks (2021) advisories — implementation-lesson case studies.
- 802.11 frames in Wireshark wiki (IE field reference).
- NIST SP 800-153 — guidelines for secruity of wireless infrastructure (survey/planning anchor).

## 12. CLO Mapping

| CLO | Where in this lecture | Assessed via |
|---|---|---|
| CLO-8 | §3.1–3.5 fundamentals + survey characterization | Lab-09 (W9), Quiz 4 (W10), Case set C |
