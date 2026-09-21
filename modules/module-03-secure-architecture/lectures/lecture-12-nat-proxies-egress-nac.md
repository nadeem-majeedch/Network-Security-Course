---
lecture: L12
title: NAT, Proxies, Egress & NAC
module: 3
week: 5
hours: 2
clos: [CLO-3]
difficulty: intermediate
status: complete
artifact-type: teaching-plan
---

# L12 — NAT, Proxies, Egress & NAC (Teaching Plan)

## 1. Overview & Prerequisites

- **Prerequisites:** L09 (zones/enforcement points), L10 (firewall policy mechanics). Note: L10/L11 schedule alongside this lecture in Week 5–6 — this lecture supplies the NAT/egress vocabulary their rulesets assume.
- **Position:** completes the perimeter toolkit. Egress control here is the detection/exfiltration hinge that L21–L23 and the capstone's exfil scenarios depend on; BCP 38 connects back to L08's amplification mechanics.
- **Faculty prep:** verify the explicit-proxy VM (Squid) on the range; prepare the BCP 38 egress-filter exercise (spoofed-source test host permitted *inside the range only*).
- **Common misconceptions:** "NAT is a firewall"; "proxies are obsolete"; "NAC is a switch feature you turn on."

## 2. Learning Objectives

By the end of this lecture, students can:

1. Explain NAT variants (static, dynamic pool, NAPT/PAT) and state which break or preserve end-to-end properties (Understand/Analyze).
2. Design explicit vs transparent proxy placement and articulate the control/visibility trade-offs including TLS interception caveats (Evaluate).
3. Author an egress policy (allow-list model) and implement BCP 38 source filtering on the range edge (Apply/Create).
4. Describe 802.1X/EAP admission flow (supplicant/authenticator/auth server) and RADIUS attribute-driven VLAN assignment (Understand).
5. Classify NAC deployment modes (monitor vs enforce; 802.1X vs MAB for non-supplicant devices) and their failure modes (Analyze).

## 3. Detailed Concepts

### 3.1 NAT: convenience first, control second
- Static NAT (1:1 server exposure), dynamic pools (outbound), NAPT/PAT (many:one — the default home/enterprise model).
- Security reality: NAT breaks *inbound* reachability by accident, not by design — it is address multiplexing, not access control. Port-forwarding re-opens exposure; hairpinning and ALG interactions cause the classic VoIP/SIP pain.
- IPv6 note: no NAT expected; end-to-end restored → *policy* must do what NAT accidentally did (default-deny ingress — RFC 6092 tie-in from L10).
- CGNAT/large-scale NAT: logging implications (who was 10.x when? — L21/L29 evidence chain).

### 3.2 Proxies: the policy point for user traffic
- Explicit (configured in client/PAC) vs transparent (intercepted at the border) vs reverse (publishing services — L09 DMZ pattern).
- What they buy: URL/category policy, malware filtering, user-identity in logs, caching; what they cost: TLS interception complexity (cert trust deployment, breakage of pinning apps, privacy governance).
- PAC/WPAD mechanics + WPAD attack caution (name-resolution abuse — L03/L06 tie-in).
- Proxy + egress firewall = complementary pair: proxy enforces *application* policy; firewall enforces *network* policy (block direct-to-IP egress so the proxy can't be bypassed).

### 3.3 Egress control & source validation
- Allow-list egress design for servers: resolver-only DNS, approved update mirrors, package repos, time sources; everything else denied+logged.
- Detection dividend: egress denials are high-value alerts (L21/L22 link) — a compromised host calling out shows up as denials, not silent success.
- BCP 38 uRPF/ACL source filtering at the edge: your network never originates spoofed packets → you stop being an amplifier (L08) and enable attack attribution.
- Remote-worker reality: egress moves to SASE/ZTNA clouds — same policy idea, different enforcement point (L16/L20 bridge).

### 3.4 Network Access Control (802.1X)
- Roles: supplicant (client) / authenticator (switch/WLC) / authentication server (RADIUS); EAP methods (EAP-TLS strongest, PEAP-MSCHAPv2 common, risks of password-fallback).
- Flow: EAPoL on the port → RADIUS → Access-Accept + attributes (VLAN assignment, ACLs, dACLs, SGT tags) → port opens.
- Dynamic VLAN/ACL assignment = identity-driven segmentation (L09 operationalized).
- MAB (MAC Authentication Bypass) for printers/IoT: MACs are spoofable → MAB is identification, not authentication; pair with isolation VLAN + posture checks.

### 3.5 NAC modes and failure planning
- Monitor mode (log-only) → enforcement rollout; guest/contractor flows; certificate provisioning logistics (the real-world killer).
- Failure modes: RADIUS down → critical-auth fallback VLAN (define it!), supplicant misconfig storms, IoT fleet without supplicants.
- Dead-drop clarity: NAC controls *admission*, not *behavior* — a compliant, authorized host can still be malware-infected.

## 4. Teaching Sequence (120 Minutes)

| Time | Segment | Instructor moves |
|---|---|---|
| 0–10 | Recap: rulebases from L10/L11 | Quick poll: who logged any denies yesterday? Bridge: "denies only matter if egress can't bypass" |
| 10–35 | Core: NAT variants + truth about NAT-as-firewall | Port-forward failure-mode vignette; v6 default-deny contrast |
| 35–55 | Core: proxies + egress design | Squid demo on range; PAC file walkthrough; block direct-to-IP egress demo |
| 55–65 | Break | — |
| 65–90 | Core: 802.1X/NAC | Role/flow diagram; RADIUS attribute table; monitor-vs-enforce rollout story |
| 90–110 | Student activity: egress + BCP38 lab | Pairs: implement allow-list egress for SERVERS zone; uRPF/ACL spoof test inside range (cs-037..039 prep) |
| 110–120 | Wrap + formative | Exit ticket; Quiz 3 administration (10 min, end-of-slot per calendar); Assignment-1 due reminder |

## 5. Technical Examples

```
# Explicit proxy enforcement pair (range): force web via proxy, then deny bypass
ip firewall filter add chain=forward src-address=10.0.10.0/24 \
  dst-address-type=!local dst-port=80,443 protocol=tcp action=reject
# Teaching point: client attempts direct https://1.2.3.4 → rejected; via proxy → allowed.

# Egress allow-list for SERVERS zone (design artifact):
# permit udp 10.0.20.0/24 -> 10.0.53.0/24 eq 53
# permit tcp 10.0.20.0/24 -> MIRRORS eq 443
# deny   ip 10.0.20.0/24 -> any log        # the high-value alert source

# BCP 38 edge source filter (concept shown on range edge):
access-list 120 permit ip 10.0.0.0 0.0.255.255 any
access-list 120 deny   ip any any log       ! anything else leaving = spoofed
# Spoof test host (range-only) sends src=8.8.8.8 → dropped at edge; verify counter.

# 802.1X flow (read-only observation on range switch):
show authentication sessions interface Gi0/8   ! method, status, assigned VLAN
```
Expected teaching points: egress denials as alert feed; uRPF as *your* network's hygiene duty; dynamic VLAN as identity-based segmentation.

## 6. Discussion Questions

1. "NAT protects us." Deconstruct: what does NAT prevent by accident, and which Module-2 attack works anyway?
2. Your proxy intercepts TLS to filter malware. Which three user populations/applications will break first, and what's the governance answer?
3. Why is blocking direct-to-IP 443 egress both valuable and operationally painful (TLS/SNI-less tools, CDNs, legitimate admin tooling)?
4. MAB authenticates nothing. Why do we still use it, and how do we reduce its risk?
5. Design the critical-auth fallback: RADIUS is down at 08:00 Monday. What do 5,000 users experience, and what did you pre-configure to make it survivable?

## 7. Student Activity

**Egress + source-validation lab (20 min, pairs):** implement the SERVERS allow-list egress on the range firewall; generate three test flows (allowed resolver DNS, allowed mirror HTTPS, denied arbitrary egress) and capture the deny log lines; then run the in-range spoofed-source test and show the BCP 38 counter increment. Deliverable: one-page egress policy + test evidence.

## 8. Problem-Solving Case

**Primary case — cs-038 "Explicit-proxy egress policy for a university lab" (intermediate):**
A computer lab must allow web research, package managers (pip/apt), and licensed-courseware CDNs — but block file-sharing sites and arbitrary outbound. The current open egress caused a mining incident. Students design: proxy + category policy, PAC deployment, direct-egress lockout, exceptions process for a class needing raw sockets (with VLAN isolation), and the monitoring rule that would have caught the mining pool connection. Trade-off discussions: privacy of interception, exception sprawl.
**Linked cases:** cs-037 (NAT mode selection/address plan), cs-039 (802.1X adoption plan and bypass risks).
*(Model solutions: instructor answer-key set, Module 3.)*

## 9. Formative Assessment

1. Which NAT variant maps one public IP:port to one internal host — and what's the exposure model?
2. Name the three 802.1X roles and the protocol between authenticator and auth server.
3. Why does BCP 38 belong on *your* edge (not just your ISP's)?
4. What breaks first when TLS interception is enabled, and what's the standard mitigation for enterprise trust?
5. Define monitor-mode NAC and the metric that tells you you're ready to enforce.
*(Answer key: instructor set, Module 3.)*

## 10. Summary & Key Takeaways

- NAT is multiplexing, not security; policy (default-deny, allow-lists) is security.
- Proxies are the application-policy point; firewalls must prevent their bypass — pairs, not rivals.
- Egress control + source validation = exfiltration defense *and* amplifier hygiene.
- 802.1X turns identity into network admission; plan failure modes before rollout.

## 11. References

- RFC 2663 — NAT terminology; RFC 3022 — traditional NAT; RFC 4787 — UDP NAT behavioral requirements.
- BCP 38 / RFC 2827 — ingress filtering; RFC 3704 — uRPF.
- RFC 6092 — IPv6 simple security (default-deny ingress).
- Squid wiki — proxy configuration & PAC/WPAD notes (current docs).
- IEEE 802.1X-2010/802.1X-2020 port-based access control; RFC 2865 — RADIUS; RFC 3748 — EAP.
- NIST SP 800-125-era NAC-related guidance (context for posture checks).

## 12. CLO Mapping

| CLO | Where in this lecture | Assessed via |
|---|---|---|
| CLO-3 | §3.1–3.3 egress/NAT design decisions; activity §7 policy authoring | Assignment 1 (W5), Quiz 3 (today), Capstone design |
