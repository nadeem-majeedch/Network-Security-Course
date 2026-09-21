---
lecture: L15
title: IPsec & Legacy VPN Architecture
module: 4
week: 8
hours: 2
clos: [CLO-7]
difficulty: intermediate
status: complete
artifact-type: teaching-plan
---

# L15 — IPsec & Legacy VPN Architecture

## 1. Overview & Prerequisites

- **Prerequisites:** L13 (DH/ECDHE, signatures — IKE is their application), L14 (handshake thinking: authenticated transcripts, proposal negotiation). L09/L10 (zones/routing symmetry — placement matters).
- **Position:** the canonical network-layer VPN. Site-to-site IPsec is graded in Lab-08; L16 contrasts it with WireGuard/TLS-VPNs and completes the VPN design skill (CLO-7, Midterm).
- **Faculty prep:** pre-build the two-site lab topology (site-A/site-B ranges with routing); snapshot clean VMs; prepare the phase-failure vignette config snippets.
- **Common misconceptions:** "IPsec = one protocol"; "tunnel mode encrypts the payload only"; "NAT-T is optional detail"; "strong crypto config means a working VPN."

## 2. Learning Objectives

By the end of this lecture, students can:

1. Name IPsec's components (AH/ESP, SAD/SPD, IKE) and state which is used today and why (AH's incompatibilities) (Understand).
2. Contrast transport vs tunnel mode by *what gets protected* and where each is used (Analyze).
3. Walk through IKEv2 phase exchanges: IKE_SA_INIT (DH, proposals) → IKE_AUTH (identity, cert/EAP, child SA), and map failures to symptoms (Analyze).
4. Explain NAT traversal (NAT-T) and why ESP-in-UDP/4500 exists (Understand).
5. Design a site-to-site tunnel: addressing (VTI/route-based), proposals, phase lifecycle (rekey), firewall allow-list, and monitoring (Create/Evaluate).

## 3. Detailed Concepts

### 3.1 Architecture pieces
- **ESP** (protocol 50): confidentiality + integrity + origin auth (AEAD suites today); **AH** (protocol 51): integrity/auth only — breaks behind NAT (mutable fields) → essentially retired.
- SPD (what policy says to protect) and SAD (active SAs); selectors (src/dst/proto/ports) define what matches which SA.
- SA: one-direction (two SAs per bidirectional tunnel); identified by SPI — the packet's "which key" pointer.

### 3.2 Modes
- Transport: protects the IP *payload* (TCP header visible); host-to-host (L2TP-over-IPsec era, opportunistic concepts).
- Tunnel: protects the *entire original packet* inside a new IP header (gateway-to-gateway; site addressing visible only to tunnel peers).
- Deciding factor: who terminates (host vs gateway) and what privacy the inner addressing needs.

### 3.3 IKEv2 lifecycle (the operational heart)
- IKE_SA_INIT: proposals (encryption/integrity/DH group) → ECDHE → shared secret; NAT-T discovery (port float to 4500).
- IKE_AUTH: identities (IP/FQDN/cert/EAP for road-warriors), cert validation (L14 skills transfer), AUTH payload = transcript signature → Child SA creation.
- Rekeying: IKE rekey + Child rekey timers; mismatched lifetimes = the classic "VPN died at 2 a.m." mystery.
- Failure taxonomy students memorize: no proposal match (config mismatch logs), PSK mismatch, cert chain failure (L14 checklist applies), NAT-T absent → one-way audio-style black holes, MTU/MSS pathology (inner packets dropped — need MSS clamp).

### 3.4 Route-based vs policy-based (the modern design fork)
- Policy-based: selectors match flows → encrypt; inflexible, struggles with overlapping subnets and dynamic routing.
- Route-based (VTI): a virtual interface + routing protocol; encryption bound to the interface → plays well with BGP, redundancy, hub-spoke.
- Design decision table: two-static-sites (either fine) vs hub-spoke-with-OSPF (route-based).

### 3.5 Site-to-site design checklist (lab-ready)
1. Address the tunnel (VTI /30s or /31s); decide inner selectors.
2. Proposals: IKE (AES-GCM-16, SHA-2, group 19/20) + IPsec (AES-GCM, no PFS debate vs policy, lifetimes).
3. Auth: certificates preferred (PKI from L13) or strong PSK for lab.
4. Firewall: UDP/500, UDP/4500, ESP(50) between peers only; do not blanket-allow.
5. Monitor: SA states, rekey counters, throughput; alert on SA-down (feeds L21).

## 4. Teaching Sequence (120 Minutes)

| Time | Segment | Instructor moves |
|---|---|---|
| 0–10 | Recap: L13/L14 quiz line-up | ECDHE + transcript auth → "today we apply both to gateways" |
| 10–35 | Core: components + modes | ESP packet diagram; tunnel vs transport with two nested headers on board |
| 35–60 | Core: IKEv2 walk-through | Annotate INIT/AUTH exchange live from capture; failure-taxonomy card set distributed |
| 60–70 | Break | — |
| 70–90 | Core: route-based design | VTI + OSPF sketch; when policy-based still suffices |
| 90–110 | Student activity: design + start build | Pairs draft site-to-site design sheet, then begin Lab-08 build on range (cs-049..050 prep) |
| 110–120 | Wrap + formative | Exit ticket; Midterm scope reminder (W8); L16 trailer: "WireGuard makes this look heavy — why do enterprises still run IPsec?" |

## 5. Technical Examples

```
# StrongSwan-style config excerpt (design artifact used in Lab-08)
connections site-a-to-b {
  version = 2
  local_addrs = 203.0.113.1
  remote_addrs = 198.51.100.1
  proposals = aes256gcm16-prfsha384-ecp384
  local-1 { auth = pubkey; certs = site-a.crt }     # L13 PKI reuse
  remote-1 { auth = pubkey; id = site-b.lab }
  children vti-a2b {
    local_ts  = 10.10.0.0/16
    remote_ts = 10.20.0.0/16
    start_action = trap; updown = vti-updown; mark = 42
    esp_proposals = aes256gcm16-ecp256
  }
}

# Health checks on the range:
strongswan statusall                    # IKE SAs + Child SAs + rekey timers
tcpdump -i eth0 'udp port 500 or udp port 4500 or esp'
# Teaching point: INIT/AUTH visible until AUTH payload → then encrypted; port
# float 500→4500 proves NAT-T engaged.
```
Expected teaching points: one-way ESP = missing allow-rule or NAT-T absence; `statusall` rekey timers explain midnight deaths.

## 6. Discussion Questions

1. Why did AH die operationally? Give the NAT interaction and the ESP-replacement argument.
2. Your tunnel passes pings but MTU-heavy transfers stall. Diagnose (MSS clamp/MTU) and fix at which device?
3. Certificates vs PSK for site-to-site: what does each make *rotation* look like at 200 sites?
4. Route-based VTI + OSPF: what failover behavior do you get that policy-based IPsec cannot provide?
5. Which IPsec counters/logs belong in the SIEM (L21 preview), and which alert threshold catches a silent rekey failure?

## 7. Student Activity

**Design sheet → build kickoff (20 min, pairs):** complete the 5-step design checklist for the two-site lab (addressing, proposals, auth, firewall, monitoring); begin the Lab-08 build: peers up, INIT completes; stop at first failure and classify it with the taxonomy card. The build completes in Lab-08 (W8).

## 8. Problem-Solving Case

**Primary case — cs-050 "Site-to-site IPsec design between two sites" (intermediate):**
A company adds a branch (10.20.0.0/16) to HQ (10.10.0.0/16); both have dynamic-ish upstream IPs (DDNS), a NAT device at the branch, and a security policy requiring per-site firewalling of all tunnel traffic. Students design the full deployment: route-based VTI, NAT-T handling, cert-based auth chained to the corporate PKI, firewall rules both ends, rekey/lifetime plan, and a monitoring dashboard spec (SA state, rekeys/h, throughput). Twist: HQ security demands PFS on child SAs and denies ESP — students must justify UDP-encapsulated ESP (NAT-T) as the compliant path.
**Linked cases:** cs-049 (IKE phase-failure diagnosis).
*(Model solutions: instructor answer-key set, Module 4.)*

## 9. Formative Assessment

1. Why is there one SPI per direction, and what does the SPI tell the receiving gateway?
2. Tunnel vs transport: which header fields remain visible in each?
3. Name two failure classes with opposite symptoms: "nothing at all" vs "pings pass, everything else fails."
4. What does NAT-T float, and why does the responder need both ports allowed?
5. Why do rekey timer mismatches cause periodic outages rather than immediate failure?
*(Answer key: instructor set, Module 4.)*

## 10. Summary & Key Takeaways

- IPsec = ESP protection + IKE negotiation; today's designs are AEAD ESP, route-based, cert-authenticated.
- The failure taxonomy (proposals, auth, NAT-T, MTU, rekey) is the operational skill — logs map to causes.
- Firewall the tunnel peers narrowly; monitor SA state as first-class infrastructure.

## 11. References

- RFC 4301 — IPsec security architecture; RFC 4303 — ESP; RFC 7296 — IKEv2.
- RFC 3947/3948 — NAT traversal for IKE/UDP encapsulation of ESP.
- RFC 7383 — IKEv2 multiple key exchanges (modernization context).
- strongSwan documentation — swanctl/VTI recipes (current edition).
- NIST SP 800-77 Rev. 1 — Guide to IPsec VPNs (design authority).

## 12. CLO Mapping

| CLO | Where in this lecture | Assessed via |
|---|---|---|
| CLO-7 | §3.1–3.5 design checklist; design-sheet activity | Lab-08 (W8), Midterm, Capstone |
