---
lecture: L12
title: NAT, Proxies, Egress & NAC
module: 3
week: 5
hours: 2
clos: [CLO-3]
difficulty: intermediate
status: complete
artifact-type: student-lecture-material
instructor-plan: modules/module-03-secure-architecture/lectures/lecture-12-nat-proxies-egress-nac.md
---

# L12 — NAT, Proxies, Egress & NAC

## 1. Learning Objectives

By the end of this session you can: (1) explain NAT variants and which end-to-end properties each breaks or preserves; (2) design explicit vs transparent proxy placement and state TLS-interception trade-offs; (3) author an allow-list egress policy and explain BCP 38 source validation; (4) describe the 802.1X/EAP admission flow and RADIUS-attribute policy; (5) classify NAC deployment modes and failure plans.

## 2. Key Definitions

| Term | Definition |
|---|---|
| NAT / NAPT (PAT) | Address translation; many-to-one port multiplexing in the common case |
| Port forwarding | Static NAT exposing an internal service to the internet |
| Explicit proxy | Client-configured (PAC/WPAD) proxy for web traffic |
| Transparent proxy | Interception at the border without client configuration |
| Egress filtering | Policy on traffic *leaving* a zone; allow-list model for servers |
| BCP 38 / uRPF | Source-address validation: your edge drops spoofed-source packets |
| 802.1X | Port-based admission: supplicant ↔ authenticator ↔ RADIUS |
| EAP-TLS / PEAP | EAP methods: certificate-based / tunnelled-password-based |
| MAB | MAC Authentication Bypass for non-supplicant devices (identification, *not* authentication) |
| NAC | Network Access Control: admission + posture + dynamic policy (VLAN/ACL assignment) |

## 3. Detailed Explanations

### 3.1 NAT: convenience first, control second
Variants: **static NAT** (1:1 exposure), **dynamic pools** (outbound), **NAPT/PAT** (many-to-one — the default everywhere). The security truth students must internalize: NAT is **address multiplexing, not access control**. It blocks inbound connections *by accident* (no mapping exists); port-forwarding recreates exposure with one line. NAT also breaks end-to-end reachability, complicates logging (CGNAT: "who was 10.x when?"), and causes ALG pain (SIP/FTP). IPv6 removes NAT — restoring end-to-end — so *policy* must do what NAT did by accident: default-deny ingress (RFC 6092).

### 3.2 Proxies: the application-policy point
**Explicit proxies** (configured via PAC/WPAD) see and control user web traffic: URL/category policy, malware filtering, identity in logs. **Transparent proxies** intercept at the border — easier rollout, harder troubleshoot. **Reverse proxies** publish services (the L09 DMZ pattern). TLS interception buys content visibility at real cost: enterprise root-CA distribution (governance!), pinning breakage, privacy duties — decide per zone, not globally. The **proxy + egress firewall pair**: the proxy enforces application policy; the firewall blocks *bypass* (direct-to-IP 80/443) so the proxy can't be dodged.

### 3.3 Egress control and source validation
Server-zone **allow-list egress**: DNS to internal resolvers only; approved update mirrors; deny + log everything else. Those deny logs are high-value detection events — a compromised host calling out shows up as *denials*, not silent success. **BCP 38**: your edge permits only your own prefixes outbound (uRPF/ACL) — your network never amplifies anyone's attack (L08) and attribution becomes possible. Remote-work reality: the same policy idea moves to cloud enforcement points (ZTNA/SASE — L16/L20).

### 3.4 802.1X admission control
Roles: **supplicant** (client), **authenticator** (switch/WLC), **authentication server** (RADIUS). Flow: EAPoL on the port → RADIUS → Access-Accept + **attributes** (VLAN assignment, dACLs, session timeout) → port opens. Per-user keying (wireless) and dynamic VLANs make policy identity-driven — L09's zones, enforced by identity. Methods: **EAP-TLS** (certificates; strongest; needs PKI logistics) vs **PEAP-MSCHAPv2** (passwords in a TLS tunnel; ubiquitous; phishable when users ignore client cert validation — L18 detail).

### 3.5 NAC modes and failure planning
Roll out in **monitor mode** (log-only) → enforcement; guests and IoT need their own paths (**guest** portal + isolation; **MAB** for printers/cameras — MACs are spoofable, so pair MAB with isolation VLAN + posture checks). Failure design is the professional skill: RADIUS down → **critical-auth fallback VLAN** (define it *before* Monday 08:00); supplicant misconfig storms; non-supplicant fleets. And the boundary: NAC controls *admission*, not *behavior* — an authorized, compliant host can still be infected.

## 4. Network Diagram: egress pair + 802.1X flow

```
 SERVERS zone ──► [egress ACL: allow resolver+mirrors; deny+log rest] ──► Internet
       │                     ▲ deny-log = detection feed (L21)
       └── web ──► [explicit proxy]  (bypass blocked by egress ACL)

 802.1X:  [supplicant] ──EAPoL──► [switch/WLC authenticator] ──RADIUS──► [RADIUS]
                 ◄── Access-Accept + attributes (VLAN 10, dACL) ──┘
```

## 5. Protocol Examples

- Bypass test: direct `https://93.184.216.34` from the zone → egress ACL rejects (logged); same URL via proxy → allowed. The pair works.
- RADIUS attribute read: `Tunnel-Private-Group-Id: 10` — the Accept that *assigns VLAN 10*; identity-driven segmentation in one line.

## 6. Configuration Concepts (concept level)

- Egress allow-list shape: permit udp → resolver:53; permit tcp → mirror-list:443; deny ip any log.
- uRPF/ACL source validation at the edge: permit `10.0.0.0/8` outbound; deny any log.
- Proxy PAC basics; WPAD caution (name-resolution abuse — L03 tie-in).
- Switch: `dot1x` + MAB order on ports; RADIUS server group; fallback VLAN.

## 7. Security Implications

- NAT is multiplexing; **policy is security**. Confusing them is the oldest network-security error.
- Egress control + source validation = exfiltration defense *and* amplifier hygiene in one config.
- Identity-driven admission (802.1X) operationalizes segmentation without re-cabling.
- Every NAC failure mode needs a pre-designed answer; improvisation at 08:00 Monday is how outages happen.

## 8. Realistic Organizational Scenario

**The mining incident (running case).** A university lab's open egress let hosts mine cryptocurrency; leadership mandates control. Constraints: research needs (package managers, licensed CDNs), a class needing raw sockets, and privacy rules on interception. Your design: proxy + category policy, PAC deployment, direct-egress lockout, a *time-boxed, logged* exception workflow for the sockets class (with VLAN isolation), and the monitoring rule that would have caught the pool connection. Full design: **case cs-038**; the build is the in-session lab.

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "NAT protects us" | It blocks *unsolicited* inbound by accident; L2–L7 attacks don't need it. Policy is security. |
| "Proxies are obsolete" | They are the application-policy point; pairing with egress ACLs is current practice. |
| "TLS interception is free visibility" | Governance, pinning breakage, and privacy duties are real costs — scope it. |
| "MAB authenticates devices" | MACs are spoofable; MAB identifies, isolation+posture do the protecting. |
| "NAC is a switch feature you turn on" | It's a program: PKI, MDM, fallback design, exception workflow. |

## 10. Classroom Activities

1. **Egress + source-validation lab (pairs):** implement the SERVERS allow-list; generate allowed/denied flows; capture deny logs; run the in-range spoofed-source test and show the BCP 38 counter.
2. **Fallback-VLAN design:** RADIUS dies at 07:45 — write the pre-agreed answer for 5,000 users.
3. **Proxy-bypass hunt:** given a PAC file and a route table, find the bypass path and close it.

## 11. Problem-Solving Questions

1. Deconstruct "NAT protects us": what does NAT prevent by accident, and which Module-2 attack works anyway?
2. Which three user populations/applications break first under TLS interception, and what's the governance answer?
3. Why is blocking direct-to-IP 443 egress both valuable and operationally painful?
4. Design the critical-auth fallback: what do users experience, and what did you pre-configure?
5. Your IoT fleet can't do EAP: design its admission path (MAB + which compensating controls?).

## 12. Exit Ticket

1. Which NAT variant maps one public IP:port to one internal host — and what's the exposure model?
2. Name the three 802.1X roles and the protocol between authenticator and auth server.
3. Why does BCP 38 belong on *your* edge, not just your ISP's?
4. What breaks first when TLS interception is enabled?
5. Define monitor-mode NAC and the readiness metric for enforcement.

*(Answers: `teaching/answer-keys/answer-key-module-03.md`.)*

## 13. References

- RFC 2663 / 3022 / 4787 — NAT terminology, behavior requirements.
- BCP 38 / RFC 2827; RFC 3704 — uRPF; RFC 6092 — IPv6 default-deny ingress.
- IEEE 802.1X; RFC 3748 (EAP); RFC 2865/2866 (RADIUS auth/acct).
- Squid wiki — proxy configuration, PAC/WPAD notes.
- NIST SP 800-41 Rev. 1 (egress policy context).

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-3 | §3.2–3.3 egress/proxy design; lab authoring | Assignment 1 (W5), Quiz 3, Capstone design |
