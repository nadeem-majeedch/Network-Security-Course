# L15 — IPsec & Legacy VPN Architecture

## 1. Learning Objectives

By the end of this session you can: (1) name IPsec's components (ESP, SA/SPD/SAD, IKE) and explain why AH is effectively retired; (2) contrast transport vs tunnel mode by what each protects; (3) walk IKEv2's two exchanges and map failures to symptoms; (4) explain NAT traversal; (5) design a route-based site-to-site tunnel — addressing, proposals, firewall, monitoring.

## 2. Key Definitions

| Term | Definition |
|---|---|
| ESP | Encapsulating Security Payload — confidentiality + integrity + origin auth (AEAD suites) |
| AH | Authentication Header — integrity only; incompatible with NAT (effectively retired) |
| SA | Security Association — one-directional relationship identified by SPI |
| SPI | Security Parameters Index — the "which key/context" pointer in each ESP header |
| SPD / SAD | Policy base (what to protect) / SA database (active SAs) |
| IKEv2 | Key-management protocol: IKE_SA_INIT + IKE_AUTH exchanges |
| NAT-T | UDP-encapsulated ESP (port 4500) when NAT sits between peers |
| Transport vs tunnel mode | Payload-only protection vs whole-original-packet-in-new-header |
| VTI | Virtual Tunnel Interface — route-based IPsec (plays well with dynamic routing) |
| PFS | Perfect Forward Secrecy on child SAs via ephemeral DH |

## 3. Detailed Explanations

### 3.1 Architecture pieces
**ESP** (protocol 50) protects payloads with AEAD suites — the modern workhorse. **AH** (protocol 51) authenticates including immutable header fields, which NAT rewrites — hence AH dies behind NAT and ESP-in-UDP (NAT-T) took over. Policy (**SPD**) decides *what* to protect; active SAs live in the **SAD**; each SA is one-directional (a tunnel = two SAs), each packet's **SPI** tells the receiver which context to use.

### 3.2 Modes: what gets protected
**Transport mode** protects the IP *payload* (original IP header visible) — host-to-host use. **Tunnel mode** wraps the *entire original packet* in a new IP header (gateway-to-gateway; inner addressing visible only to peers). Decision driver: who terminates (host vs gateway) and whether inner addressing must stay private.

### 3.3 IKEv2 lifecycle (where deployments actually break)
- **IKE_SA_INIT:** proposal negotiation (encryption/integrity/DH group) → ECDHE → shared secret; NAT-T discovery (float to UDP/4500).
- **IKE_AUTH:** identities (IP/FQDN/cert, or EAP for road-warriors), certificate validation (your L13/L14 skills apply directly), AUTH payload signs the transcript → Child SA creation.
- **Rekeying:** IKE and Child SAs rekey on timers; mismatched lifetimes are the classic "VPN died at 2 a.m." mystery.
**Failure taxonomy** (memorize): proposal mismatch (logs show no acceptable proposal), PSK mismatch, certificate-chain failure (L14 checklist), NAT-T absent (one-way ESP — "pings work, TCP dies"), **MTU/MSS pathology** (inner packets dropped — MSS clamp fixes).

### 3.4 Route-based vs policy-based
**Policy-based:** selectors match flows → encrypt; rigid, painful with overlapping subnets and dynamic routing. **Route-based (VTI):** a virtual interface + routing protocol (OSPF/BGP); encryption binds to the interface — hub-and-spoke, failover, and dynamic routing become natural. Design rule: two static sites (either works); anything dynamic (VTI).

### 3.5 Site-to-site design checklist
1. Address the tunnel (VTI /30-/31s) and define inner selectors.
2. Proposals: IKE `aes256gcm16-prfsha384-ecp384`; ESP AEAD; sane lifetimes; PFS per policy.
3. Authentication: certificates (your lab PKI) preferred; strong PSK only for lab simplicity.
4. Firewall: UDP/500, UDP/4500, ESP(50) *between peers only* — never blanket-allow.
5. Monitor: SA states, rekey counters, throughput; alert on SA-down (feeds L21).

## 4. Network Diagram: tunnel-mode encapsulation + peers

```
 Inner packet:  [IP: 10.10.5.2 → 10.20.9.7 | TCP | data]
 Tunnel mode:   [NewIP: A-peer → B-peer][ESP(SPI)| Inner packet | ICV]
                                │  encrypted/authenticated across Internet
 Site A (10.10.0.0/16) ──VTI──●━━━━━━━━━━━━━●──VTI── Site B (10.20.0.0/16)
                         IKE:500/4500, ESP:50
```

## 5. Protocol Examples

- strongSwan-style config excerpt (design artifact used in Lab-08):

```
 connections site-a-to-b {
   version = 2
   local_addrs = 203.0.113.1
   remote_addrs = 198.51.100.1
   proposals = aes256gcm16-prfsha384-ecp384
   local-1  { auth = pubkey; certs = site-a.crt }
   remote-1 { auth = pubkey; id = site-b.lab }
   children vti-a2b {
     local_ts = 10.10.0.0/16
     remote_ts = 10.20.0.0/16
     start_action = trap; updown = vti-updown; mark = 42
     esp_proposals = aes256gcm16-ecp256
   }
 }
```

- Health read: `strongswan statusall` (SA states, rekey timers); capture `udp port 500 or 4500 or esp` — INIT/AUTH visible until the AUTH payload, then everything encrypts; port float 500→4500 proves NAT-T engaged.

## 6. Configuration Concepts (concept level)

- VTI + OSPF: routing decides what rides the tunnel; encryption follows the interface.
- Peer-scoped firewall rules only; no "ESP from anywhere."
- Rekey lifetime plan (IKE hours, child SA shorter) — aligned on *both* peers.

## 7. Security Implications

- IPsec = ESP protection + IKE negotiation; misconfigurations, not crypto, break deployments.
- NAT-T existence is why AH is gone; understanding one explains the other.
- Narrow peer-scoping and SA-state monitoring are the operational difference between a tunnel and a liability.

## 8. Realistic Organizational Scenario

**The new branch (running case).** HQ (10.10.0.0/16) adds a branch (10.20.0.0/16) with a dynamic-ish upstream (DDNS), NAT at the branch, and a security policy demanding per-site firewalling of tunnel traffic. Your design: route-based VTI, NAT-T handling, certificate auth chained to the corporate PKI, firewall rules both ends, rekey plan, monitoring dashboard — and the compliance wrinkle: PFS required, ESP blocked → justify UDP-encapsulated ESP (NAT-T) as the compliant path. Full case: **cs-050**; the build is Lab-08.

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "IPsec is one protocol" | It's ESP + IKE + policy bases; each fails differently. |
| "Tunnel mode encrypts only the payload" | Transport protects payload; tunnel protects the *whole original packet*. |
| "NAT-T is optional trivia" | Without it, NAT'ed peers black-hole ESP — the classic half-working VPN. |
| "Strong crypto config = working VPN" | Proposals, identity, MTU, and rekey timers break deployments before crypto does. |
| "Policy-based IPsec scales" | Selectors crumble with dynamic routing; route-based (VTI) is the modern answer. |

## 10. Classroom Activities

1. **Design sheet → build kickoff (pairs):** complete the 5-step checklist for the two-site lab; start the build; stop at first failure and classify it with the taxonomy card.
2. **Failure taxonomy card game:** symptom → cause, rapid-fire.
3. **Capture reading:** annotate INIT vs AUTH visibility and the NAT-T port float.

## 11. Problem-Solving Questions

1. Why one SPI per direction, and what does the SPI tell the receiving gateway?
2. Tunnel vs transport: which header fields remain visible in each?
3. Name two failure classes with opposite symptoms — "nothing at all" vs "pings pass, TCP dies" — and their causes.
4. What does NAT-T float, and why must the responder allow both ports?
5. Why do rekey-timer mismatches cause periodic outages rather than immediate failure?

## 12. Exit Ticket

1. Why is AH effectively retired? Give the NAT interaction.
2. Which exchange performs ECDHE in IKEv2, and what does the second exchange add?
3. Route-based vs policy-based: what failover capability does VTI add?
4. Name the three firewall permits a proper site-to-site needs between peers.
5. What monitoring signal catches a silent rekey failure before users do?

*(Answers: `the instructor answer-key collection (not published)`.)*

## 13. References

- RFC 4301 (architecture); RFC 4303 (ESP); RFC 7296 (IKEv2); RFC 3947/3948 (NAT-T).
- NIST SP 800-77 Rev. 1 — Guide to IPsec VPNs.
- strongSwan documentation — swanctl/VTI recipes (current).
- Course instructor plan L15 (lab build steps, authorized range).

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-7 | §3 components + design checklist | Lab-08 (W8), Midterm, Capstone |
