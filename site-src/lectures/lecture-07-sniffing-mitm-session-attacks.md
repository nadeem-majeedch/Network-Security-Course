# L07 — Sniffing, MITM & Session Attacks

> **Scope and safety note:** mechanics are taught for detection and defense design.
> All examples are analyzed from instructor-provided lab-range captures. Interception
> of traffic on networks you do not own or are not authorized to test is illegal.

## 1. Learning Objectives

By the end of this session you can: (1) distinguish passive sniffing from active MITM by required vantage point; (2) explain downgrade and interception patterns (SSL-stripping, DNS-spoof MITM) and their structural fixes; (3) describe session-token risks (cookie flags, replay) and on-path enablers; (4) identify network evidence of MITM in captures, TLS telemetry, and proxy logs; (5) select layered mitigations per exposure class.

## 2. Key Definitions

| Term | Definition |
|---|---|
| Passive sniffing | Reading traffic on your segment without altering anything (needs on-link vantage) |
| On-path (MITM) | Positioning so traffic transits you; enables read/modify/inject |
| SSL stripping | Rewriting https→http so the session stays cleartext |
| HSTS | Server policy (header/preload) forcing browsers onto HTTPS — kills first-visit stripping after first contact |
| Session cookie | Bearer token identifying a logged-in session; the hijack target |
| Secure / HttpOnly / SameSite | Cookie flags: TLS-only / script-proof / cross-site-request limits |
| Sidejacking | Stealing session cookies from cleartext traffic and replaying them |
| mTLS | Mutual TLS — both sides present certificates (service-to-service standard, L14/L20) |

## 3. Detailed Explanations

### 3.1 Passive sniffing: reading what flows
Nothing is "hacked" — the attacker simply has (or creates) a vantage: same broadcast segment, a flooded switch (L06), a mirrored/SPAN port, or wireless monitor mode (L17). High-value legacy targets: HTTP basic/form auth, SMTP/IMAP, FTP, SNMPv1/2, telnet. Defender consequence: the protocol inventory must include "what still speaks cleartext?" — a hardening item (L24), because detection cannot un-read what already crossed the wire.

### 3.2 Active MITM patterns
With on-path position (often obtained via L06), the attacker shapes the conversation:
- **SSL stripping:** intercept the HTTP→HTTPS redirect and rewrite it; the user's session stays cleartext. Structural fix: **HSTS** (`Strict-Transport-Security`, `includeSubDomains`, preload) — after the first HTTPS contact, the browser refuses HTTP. First-visit exposure remains; fixes are preload lists and fixing cleartext origins.
- **DNS-spoof MITM:** answer the target name with the attacker's IP; the user's browser then talks to the attacker. Without the real server's certificate the attacker cannot complete a modern TLS handshake *without detection* — which is why users clicking through certificate warnings is the actual vulnerability. Fixes: validating resolvers, DNSSEC where deployed, CAA, certificate-transparency monitoring (L14).
- **Rogue/malicious CAs:** trust is only as good as the roots installed on the device — enterprise root-CA distribution (for TLS inspection) is a governance decision with real risk (L14's trade-offs).

### 3.3 Session attacks without breaking crypto
The attacker doesn't need to decrypt TLS if the *token* leaks elsewhere: cookies sent over HTTP (no `Secure` flag), tokens readable by script (no `HttpOnly` — XSS class), cookies replayed from another device (sidejacking), long-lived sessions without rotation. Defense: `Secure`, `HttpOnly`, `SameSite`, short lifetimes + rotation, TLS binding of session material — plus *network-side detection*: the same session appearing from two IPs/user-agents is a classic proxy/flow finding.

### 3.4 The detection evidence table

| Pattern | Evidence source | What you see |
|---|---|---|
| Strip attempt | Proxy/IDS | `https→http` Location rewrite; cleartext POST follows |
| Cert-failure cluster | Endpoint/TLS telemetry | repeated validation failures for one destination |
| Rogue resolver | DNS analytics (L23) | inconsistent answers, short TTLs |
| On-path injection | Suricata (L22) | unexpected response-body signatures |
| Session reuse | Proxy/flow (L21) | same cookie value from second IP/UA in minutes |

### 3.5 Why encryption is the structural answer (Module-4 bridge)
On-path position cannot be prevented everywhere — assume it happens. Make intercepted traffic *useless*: authenticate the server (certificates), encrypt the path (TLS), bind sessions to crypto (secure cookies), and harden the identity layer (MFA). That is L13–L14's agenda; today you know exactly *why* it matters.

## 4. Network Diagram: stripping vs HSTS

```
 User ──http://shop.example──► Attacker ──► Real server (https)
        ◄─ rewritten: "stay on http" ──┘
 User ──POST password (cleartext!)──► Attacker

 With HSTS (after first contact):
 User ──https://shop.example──► Attacker (cannot present valid cert)
        ◄─ browser blocks: certificate error ──► ATTACK VISIBLE
```

## 5. Protocol Examples

- Strip attempt in a capture: HTTP 302 with `Location: http://…` from an on-path host, followed by a cleartext POST containing credentials — the two-frame story of a stolen password.
- Sidejacking in proxy/flow logs: session cookie value `sessid=…` seen from 10.0.0.44 at 09:02 and from 10.0.0.77 at 09:06 with different user-agents.

## 6. Configuration Concepts (concept level)

- HSTS header on all TLS vhosts + preload submission; redirect all HTTP→HTTPS *and* fix the cleartext origins.
- Cookie flags: `Secure; HttpOnly; SameSite=Lax` (or `Strict` where flows allow).
- Enterprise TLS-inspection CA: distribute via MDM *only* with governance sign-off (L14 privacy/ops trade-offs).

## 7. Security Implications

- Sniffing is free with vantage; MITM is cheap with misconfigured trust — both are *position* problems.
- TLS converts an invisible attack into a visible certificate error — then user behavior decides the outcome.
- Sessions are bearer tokens: whoever holds the cookie *is* the user until it expires.

## 8. Realistic Organizational Scenario

**The one-time password prompt (running case).** Finance users see an unexpected portal prompt; a week later the helpdesk correlates that all affected users sit on one switch stack. Artifacts: ARP capture segment (gateway IP answering with a workstation MAC — L06!) and proxy logs showing portal traffic with two device fingerprints. You reconstruct: position theft → portal spoof → harvested credentials. The remediation spans teams: network (DAI), IAM (reset/rotate, MFA), SOC (duplicate-session detection). Full reconstruction is **case cs-018**.

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "HTTPS everywhere makes MITM obsolete" | It removes *passive* reading; first-visit stripping, user-ignored warnings, and rogue CAs remain. |
| "Session hijacking needs malware" | A stolen cookie is enough — no payload required. |
| "Cookie flags are developer trivia" | They are the difference between a stolen password and a useless cookie. |
| "The padlock proves the site is legitimate" | It proves the connection to *that name* is encrypted — phishing sites have padlocks too. |
| "We'd see a MITM immediately" | Forwarding attackers are invisible; only *failed* TLS and anomalies reveal them. |

## 10. Classroom Activities

1. **MITM forensics (teams of 3):** two artifacts (strip-attempt capture; proxy log with duplicate sessions) → pattern, three evidence citations, CIA impact, 3-layer mitigation set.
2. **Cookie-flag workshop:** given five set-cookie headers, mark what each flag blocks.
3. **Red-team review:** instructor proposes innocent explanations for the evidence; teams defend or revise classifications.

## 11. Problem-Solving Questions

1. HSTS stops stripping after the first visit — why is the first visit still a problem, and what closes it?
2. Your org pins certificates in its mobile app. What breaks during CA rotation, and what's the operational alternative?
3. Why does `SameSite=Lax` reduce but not eliminate session theft?
4. An IDS cannot read TLS payloads — list three MITM-related detections that still work on metadata alone.
5. Which is riskier: an enterprise root CA on all laptops or user-installed CAs? Defend with a scenario.

## 12. Exit Ticket

1. Name the two conditions SSL stripping needs to succeed on first visit.
2. Which cookie flag stops JavaScript from reading a session cookie?
3. What single network observation most strongly suggests an on-path attacker between two internal hosts?
4. Why is "we have HTTPS" insufficient against a DNS-spoof MITM?
5. Give one detection that works despite TLS and name its data source.

*(Answers: `the instructor answer-key collection (not published)`.)*

## 13. References

- RFC 6797 — HSTS; RFC 8446 — TLS 1.3 (preview); RFC 6844 — CAA; RFC 6962 — CT.
- OWASP Session Management Cheat Sheet — cookie flags, token lifecycle.
- OWASP Transport Layer Protection Cheat Sheet — HSTS deployment patterns.
- Bejtlich, *The Practice of Network Security Monitoring* — detecting on-path behavior.
- Course instructor plan L07 (lab-range capture analysis).

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-2 | §3 classification + evidence mapping | Quiz 2 (W4), Lab-04, Case set A |
