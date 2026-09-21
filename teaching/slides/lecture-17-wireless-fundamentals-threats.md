---
marp: true
theme: default
paginate: true
lecture: L17
week: 9
clos: [CLO-8]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# Wireless Fundamentals & Threats

**Network Security · Lecture 17 · Week 9**

*The network edge is now the air.*

<!-- notes: OPEN (2 min). Hook: "The wire trusted the closet. The air
trusts no closet — everything is in the blast radius." -->

---

## Learning Objectives

1. **Explain** the RF domain as a shared, untrusted medium
2. **Contrast** WPA2-PSK, WPA3-Personal, WPA2/3-Enterprise by threat
   model
3. **Analyze** the evil-twin and rogue-AP attack classes
4. **Describe** 802.1X's three roles in wireless auth
5. **Design** guest wireless with client isolation discipline

<!-- notes: (1 min) Objective 2 is quiz-4's Q1; objective 3 maps to
cs-057/cs-058 cases. -->

---

## RF: The Shared Medium

- Everything radios to everyone in range — walls are advisory
- Frame injection/observation is a *physical* property
- Security = encryption + identity, layered on an open medium

<!-- notes: (4 min) The "walls are advisory" line frames every wireless
control as compensating for physics. -->

---

## WPA2-PSK: The Shared Secret Problem

- One passphrase for everyone → capture handshake → **offline
  dictionary attack**
- One leaked key = network-wide exposure; rotation = pain
- Personal mode is for homes/small offices, not campuses

<!-- notes: (5 min) Quiz-4 Q1 + quiz-10 Q1's exact territory. cs-054's
campus-audit case is the worked instance; cs-049/QB-049 connect PSK's
blast radius to Enterprise. -->

---

## WPA3-Personal: SAE Fixes the Offline Crack

- SAE: per-handshake key derivation — captured handshakes don't verify
  guesses offline
- *Doesn't* fix: weak passphrases, rogue/evil-twin APs, client posture
- Transition mode coexistence caveats (downgrade bait)

<!-- notes: (5 min) The two-slide honesty: what SAE fixes, what it
doesn't. Quiz-10 Q8 asks exactly this pair. The downgrade-bait caveat
is the transition-mode honesty per course rules. -->

---

## WPA2/3-Enterprise: 802.1X

- Three roles: **supplicant** (client), **authenticator** (AP),
  **authentication server** (RADIUS)
- Per-user credentials → accountability, per-user revocation, logs
- EAP methods: EAP-TLS (certs, strongest), PEAP-MSCHAPv2 (legacy)

<!-- notes: (6 min) Quiz-4 Q2 + quiz-10's Enterprise row. cs-059's
deployment case is the implementation story. The EAP-method note is
the audit nuance: Enterprise with weak EAP still leaks. -->

---

## Evil Twin & Rogue AP

- **Evil twin**: attacker broadcasts your SSID, stronger signal —
  clients auto-associate
- **Rogue AP**: an *unauthorized* AP plugged into your network —
  physical-layer backdoor
- Both defeated by: client-side verification, 802.1X, RF monitoring

<!-- notes: (6 min) The distinction matters: evil twin impersonates;
rogue AP infiltrates. cs-057's detection-response case + cs-058's
survey case pair them. Quiz-4 Q4: WIDS sees both; wired IDS sees
neither. -->

---

## Guest Wireless Discipline

- Separate SSID/VLAN; **client isolation** (peers can't talk)
- Internet-only policy; captive portal as *registration*, not security
- Bandwidth caps = hygiene, not control

<!-- notes: (4 min) Quiz-10 Q6's isolation rationale: without
encryption, isolation stops peer snooping. cs-055's containment case
is the design story. -->

---

## The Wireless Control Set

| Threat | Control |
|---|---|
| Offline crack | WPA3-SAE / Enterprise |
| Evil twin | 802.1X + client verification + WIDS |
| Rogue AP | RF survey + WIDS + port security |
| Peer snooping | client isolation |
| Weak EAP | EAP-TLS policy |

<!-- notes: (3 min) Reference table mirroring L06's control-set slide —
same teaching pattern, different layer. Quiz-4's matrix. -->

---

## CS/DS Example: The Research Wing's SSID

- DS cluster mgmt SSID: Enterprise-only, no PSK fallback
- The cs-088 intrusion started as wired brute-force — wireless variant
  would target this SSID

<!-- notes: (3 min) DS framing: research SSIDs carry credential-bearing
sessions — Enterprise + isolation is the baseline. -->

---

## Activity: Audit This Floor (6 min)

Floor audit data: SSID "StaffNet" (WPA2-PSK, 2019 passphrase), SSID
"Guest" (open, no isolation), unknown AP "Free_Fast_WiFi". Rank the
findings; propose fixes in order.

<!-- notes: (6 min) cs-054's data shape. Ranking: Guest-no-isolation
(immediate), StaffNet-PSK (migration), unknown AP (locate — could be
evil twin *or* rogue; different fixes!). -->

---

## Case Study: cs-057 (5 min)

- Evil twin detection and response — client-side tells first

<!-- notes: (5 min) The tells: cert mismatches on portal, sudden 802.1X
failures, WIDS alert. Classroom protocol. -->

---

## Formative Check

- Oral: why does a captured WPA2 handshake enable offline attack — and
  why doesn't WPA3's?

<!-- notes: (2 min) Exit oral — SAE's per-handshake derivation is the
answer anchor. -->

---

## References & Next

- Wi-Fi Alliance WPA3 overview; IEEE 802.1X
- **Next (L18):** enterprise wireless operations & rogue defense
