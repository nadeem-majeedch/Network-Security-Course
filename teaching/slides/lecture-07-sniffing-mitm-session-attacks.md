---
marp: true
theme: default
paginate: true
lecture: L07
week: 4
clos: [CLO-2]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# Sniffing, MITM & Session Attacks

**Network Security · Lecture 7 · Week 4**

*Interception, organized.*

<!-- notes: OPEN (2 min). Hook: "L06 gave the attacker a position on
the wire. Today: what they do with it — and what encryption takes
back." -->

---

## Learning Objectives

1. **Distinguish** sniffing capability across hub/wireless/switched
   media
2. **Explain** the MITM position's requirements and its evidence
3. **Analyze** session-hijack prerequisites in TCP and web sessions
4. **Evaluate** which controls actually break interception (crypto vs
   switch features)
5. **Read** interception evidence in proxy/DNS/ARP telemetry

<!-- notes: (1 min) Objective 4 is the lecture's thesis: switch
features fix *positioning*; encryption fixes *exposure*. Both needed. -->

---

## Sniffing by Media

| Medium | What the attacker sees |
|---|---|
| Hub / legacy | everything (physical repetition) |
| Wi-Fi (open) | everything in RF range |
| Wi-Fi (WPA2/3) | others' frames only with the key / MITM |
| Switched wired | broadcast + flooded frames only |

- L6's attacks exist to *upgrade* the switched-wire row

<!-- notes: (5 min) The table frames L6 as "position upgrade." Quiz 2
Q6 asks the switched-vs-hub contrast. Wireless rows preview L17–18. -->

---

## The MITM Position

- Requirements: be on-path (L2 tricks, rogue DHCP, DNS lies)
- Passive MITM: read only — stealthy
- Active MITM: modify/inject — detectable (latency, TLS errors)

![bg right:35% fit](diagrams/03-arp-poisoning-flow.md)

<!-- notes: (5 min) Diagram 03 revisited as position, not mechanism.
"Passive = quiet; active = evidence" — cs-018's case detects the active
variant. -->

---

## Breaking Interception I: Switch Features

- DAI/snooping/port security remove the *position*
- But position ≠ payload: a compromised host is still on-path *itself*

<!-- notes: (3 min) Scope-setting slide: switch features fix the
network's trust, not the endpoint's. Hand off to crypto. -->

---

## Breaking Interception II: Encryption

- TLS on every hop = intercepted payload is ciphertext
- The attacker's fallback: downgrade tricks, cert lies → L14's story
- DNS: DoH/DoT protects the *query* path too

<!-- notes: (5 min) "Encryption doesn't remove the attacker; it blinds
them." cs-018's defensive fixes pair both: DAI + TLS-everywhere. -->

---

## Session Hijack: TCP-Level

- Prerequisites: see the session (sniffing) + predict/know sequence
  numbers
- Blind injection vs session theft (the seq story from L03)
- Modern OSes: strong ISN PRNGs → blind hijack mostly historical;
  *on-path* hijack still real

<!-- notes: (5 min) Careful framing: historical vs current viability —
the course's technical-accuracy rule. cs-019's indicators are the web-
session variant. -->

---

## Session Hijack: Web Sessions

- Cookies/tokens ARE the session — steal the token, *be* the user
- MFA protects login, not the session — **token theft bypasses MFA**
- Controls: Secure/HttpOnly/SameSite cookies, short lifetimes, binding
  tokens to device posture

<!-- notes: (6 min) The lecture's most important slide. "MFA stops
credential theft, not session theft" — cs-100's incident lives on this
fact. Quiz-level clarity expected. -->

---

## DNS Spoofing: Redirect the Map

- Forged answer before the real one → user lands at attacker's IP
- Browser shows the *right name* — trust shattered quietly
- Fixes: resolver hardening, DNSSEC, DoH/DoT, egress DNS control

<!-- notes: (5 min) cs-020's campaign case. The "right name, wrong
place" phrase lands the deception. Egress DNS control previews L12. -->

---

## Evidence Reading: Interception in Telemetry

| Telemetry | Interception tell |
|---|---|
| Switch DAI logs | drops = attempt; misses = success |
| ARP cache dumps | duplicate IPs, MAC flapping |
| Proxy logs | impossible locations for a session |
| TLS client errors | sudden cert warnings after years of none |

<!-- notes: (4 min) Evidence-first teaching per course style. Quiz 2's
Section C scenario reads exactly this table. -->

---

## CS/DS Example: Intercepting the Dataset Pull

- Notebook → lake TLS pull; on-path attacker sees: SNI, size, rhythm
- Content stays opaque — metadata analysis still profiles the job
- Lesson: metadata is a *defense* signal too (anomaly detection, L23)

<!-- notes: (3 min) DS framing: the same metadata that leaks privacy
provides detection. Double-edged framing keeps the lesson honest. -->

---

## Activity: Whodunit, Wirelessly (5 min)

Campus Wi-Fi: a user reports the portal page looks odd. Rank the
evidence: ARP logs, proxy logs, DNS logs, client TLS warnings.

<!-- notes: (5 min) The ranking debate: client TLS warnings are the
strongest single signal (cert lie), proxy location anomaly second.
Debrief: evidence hierarchy, not equal-weight soup. -->

---

## Case Study: cs-018 (5 min)

- Internal MITM: read the evidence, then fix the network *and* the
  crypto

<!-- notes: (5 min) The case's answer pairs both control families —
that pairing is the lecture's thesis. -->

---

## Formative Check

- Oral: why does token theft beat MFA? Name one switch feature and one
  crypto control that break interception.

<!-- notes: (2 min) Exit oral — both are quiz/exam questions. -->

---

## References & Next

- RFC 8446 (TLS 1.3) — for the encryption fix
- Diagrams: `diagrams/03-arp-poisoning-flow.md`
- **Next (L08):** DoS/DDoS — when the goal isn't reading, it's
  breaking
