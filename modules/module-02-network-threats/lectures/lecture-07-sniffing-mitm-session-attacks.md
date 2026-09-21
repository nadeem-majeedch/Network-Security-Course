---
lecture: L07
title: Sniffing, MITM & Session Attacks
module: 2
week: 4
hours: 2
clos: [CLO-2]
difficulty: beginner-intermediate
status: complete
artifact-type: teaching-plan
---

# L07 — Sniffing, MITM & Session Attacks (Teaching Plan)

## 1. Overview & Prerequisites

- **Prerequisites:** L06 (on-path position mechanics at L2); L04 (stream-following and filter craft).
- **Position:** explains *what an on-path attacker gains* and why encryption (Module 4) is the structural answer. Directly motivates L13–L14 and the certificate-warning symptoms students met in cs-013.
- **Faculty prep:** prepare the MITM-evidence capture (HTTP session with inserted content; TLS-strip attempt against an HSTS site) and the session-hijack narrative (cookie theft story without live theft).
- **Common misconceptions:** "HTTPS everywhere makes MITM obsolete"; "session hijacking requires malware"; "sniffing requires exploits."

## 2. Learning Objectives

By the end of this lecture, students can:

1. Distinguish passive sniffing from active MITM and identify the vantage point each requires (Understand/Analyze).
2. Explain downgrade and interception patterns (SSL-stripping, DNS spoofing to attacker hosts) and the role of HSTS/CAA/DANE-class controls (Analyze).
3. Describe session-token lifecycle risks (cookies, bearer tokens) and how on-path or XSS-adjacent position enables hijacking/replay (Analyze).
4. Identify network evidence of MITM: cert chains that fail validation, ARP anomalies (link to L06), unexpected redirects, duplicate SNI hosts (Analyze).
5. Select layered mitigations for a given exposure: TLS everywhere, HSTS, mTLS/pinning trade-offs, short token lifetimes, re-binding to user sessions (Apply/Evaluate).

## 3. Detailed Concepts

### 3.1 Passive sniffing: reading what flows
- Requirements: on-link (hub-era, flooded switch, mirrored/SPAN port, wireless monitor mode) — nothing is "hacked"; data is simply readable.
- High-value targets in cleartext era: HTTP basic/form auth, SMTP/IMAP, FTP, SNMPv1/2, telnet — and why legacy protocols persist.
- Defender consequence: protocol inventory must include "what still speaks cleartext?" (feeds L24 hardening).

### 3.2 Active MITM patterns
- ARP/MITM (L06 mechanism) → traffic now transits attacker.
- **SSL stripping:** rewrite https→http in redirects; defeat via HSTS (preloaded, includeSubDomains), and by fixing cleartext origins.
- **DNS spoofing to attacker host:** answer name with attacker IP; real cert missing → warnings users click through; mitigation: DNSSEC (validating resolver), CAA, cert transparency monitoring.
- **Evil portal / rogue CA concepts:** why the CA trust model matters; enterprise risk of installed root certs (superfish-class incidents as case discussion).
- mTLS and pinning: when they help (API-to-API), when they hurt (key operational cost, breakage).

### 3.3 Session attacks without the session
- Cookie flags: Secure, HttpOnly, SameSite — what each blocks.
- Hijack vectors on-path: steal cookie over HTTP, ride an established session (sidejacking class), replay tokens.
- Cross-adjacent (brief, network-relevant): XSS cookie theft is app-layer, but its *network signature* (data leaving to unexpected host) is detectable — L22 preview.
- Replay defenses: TLS binding, short TTL, rotation, binding token to client/session context.

### 3.4 Detection evidence table (build in class, kept as artifact)
| Pattern | Evidence source | Example field/log |
|---|---|---|
| Strip attempt | Proxy/IDS | `http` class downgrade + `ssl` follow-up failure |
| Cert warnings cluster | Endpoint logs, TLS telemetry | validation failure spike for one destination |
| Rogue resolver | DNS analytics (L23) | inconsistent answers, short TTLs |
| On-path injection | Suricata (L22) | response-body signatures, unexpected JS refs |
| Cookie theft | Proxy/NetFlow (L21) | session cookie appearing from second IP/UA |

### 3.5 Why encryption is the structural answer (Module-4 bridge)
- On-path position cannot be prevented everywhere — assume it; make intercepted traffic useless (confidentiality+integrity+server auth).
- remainder: L13 (crypto primitives) → L14 (TLS specifics: handshake, cert validation, config auditing).

## 4. Teaching Sequence (120 Minutes)

| Time | Segment | Instructor moves |
|---|---|---|
| 0–10 | Recap: vantage-point ladder | Map L6 attacks to the four L01 vantage points |
| 10–35 | Core: sniffing + MITM patterns | Play strip-attempt capture; annotate redirect rewrite; connect to cs-013 symptoms |
| 35–55 | Core: sessions & tokens | Cookie-flag demo (lab-only app); sidejacking story with proxy-log evidence |
| 55–65 | Break | — |
| 65–75 | Core: detection evidence table | Build the §3.4 table together on board |
| 75–110 | Student activity: MITM forensics | Teams work the two captures: identify pattern, evidence lines, mitigation set (cs-017..020 prep) |
| 110–120 | Wrap + formative | Exit ticket; trailer: "tomorrow: when the attack is volume, not stealth" |

## 5. Technical Examples

```
# Evidence 1: downgrade attempt shape (from range capture)
tshark -r mitm.pcap -Y 'http.response and http.location contains "http://"' \
  -T fields -e frame.number -e ip.src -e http.location
# Teaching point: https→http Location header = strip attempt; then look for the
# victim's cleartext POST that followed (http.request.method == POST).

# Evidence 2: certificate failure pattern (endpoint side)
# Browser/console shows: ERR_CERT_AUTHORITY_INVALID for one host repeatedly,
# while other hosts validate — compare chain: attacker-presented issuer vs real CA.

# Evidence 3: session from two origins (proxy/flow story, no live theft)
# Same session cookie value appearing from 10.0.0.44 and 10.0.0.77 with
# different user-agents within 5 minutes = sidejacking hypothesis.
```
Expected teaching points: each pattern is *detectable*; mitigation differs per pattern (HSTS vs DNSSEC vs token hygiene).

## 6. Discussion Questions

1. HSTS stops stripping after first visit. Why is the first visit still a problem, and what closes it?
2. Your org pins certificates for its mobile app. What breaks during CA rotation, and what's the operational alternative?
3. Why does SameSite=Lax reduce (not eliminate) session theft risk?
4. An IDS cannot read TLS payloads. List three MITM-related detections that still work on metadata.
5. Which is riskier: an enterprise root CA installed on all laptops, or allowing user-installed CAs? Defend with a scenario.

## 7. Student Activity

**MITM forensics workshop (35 min, teams of 3):** two staged artifacts (strip-attempt capture; proxy/flow log with duplicate sessions). Teams produce: pattern classification, three evidence citations (frame numbers/log lines), CIA impact statement, and a 3-layer mitigation set (immediate, config, architectural). Instructor runs a "red team" pass: tries to refute one team's classification with an innocent explanation (e.g., dev environment redirects).

## 8. Problem-Solving Case

**Primary case — cs-018 "Internal MITM: evidence and defensive fixes" (beginner-intermediate):**
Finance users report a one-time password prompt on the intranet portal. A week later, the helpdesk correlates: all affected users were on one switch stack. Provided artifacts: ARP capture segment, proxy logs showing portal traffic with two different device fingerprints. Students must reconstruct the incident (who, where, what was exposed), state whether credentials or sessions were likely taken, and produce a remediation plan with owners (network team: DAI; IAM: token rotation; SOC: detection rule for duplicate sessions).
**Linked cases:** cs-017 (passive-sniffing exposure), cs-019 (session-hijack indicators), cs-020 (DNS-spoofing campaign).
*(Model solutions: instructor answer-key set, Module 2.)*

## 9. Formative Assessment

1. Name the two conditions SSL stripping needs to succeed on first visit.
2. Which cookie flag stops JavaScript from reading a session cookie?
3. What single network observation most strongly suggests an on-path attacker between two internal hosts?
4. Why is "we have HTTPS" insufficient against DNS-spoof MITM?
5. Give one detection that works despite TLS and name its data source.
*(Answer key: instructor set, Module 2.)*

## 10. Summary & Key Takeaways

- Sniffing is free with vantage; MITM is cheap with misconfigured trust — both are *position* problems.
- The durable answer is cryptographic: authenticate the endpoint, encrypt the path, harden sessions.
- Every MITM pattern leaves metadata evidence — build the habit of reading captures as an incident responder.

## 11. References

- RFC 6797 — HTTP Strict Transport Security (HSTS); RFC 8446 — TLS 1.3 (preview for L14).
- RFC 6844 — CAA records; RFC 6962 — Certificate Transparency.
- OWASP Session Management Cheat Sheet — cookie flags, token lifecycle.
- Bejtlich, *The Practice of Network Security Monitoring* — detecting on-path behavior from NSM data.
- Engelbardt/Belcher-era sidejacking literature ( Firesheep-era analyses) — historical context for §3.3.

## 12. CLO Mapping

| CLO | Where in this lecture | Assessed via |
|---|---|---|
| CLO-2 | §3.1–3.5 attack classification + evidence mapping | Quiz 2 (W4 — end of week), Lab-04, Case set A |
