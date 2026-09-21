---
exam: midterm
week: 8
type: exam
clos: [CLO-1, CLO-2, CLO-3, CLO-4, CLO-5, CLO-6, CLO-7]
lectures: [L01, L16]
marks: 100
duration: 120 min
status: complete
artifact-type: student-exam
answer-key: instructor/answer-keys/midterm-answer-key.md
---

# Midterm Examination — Network Security (Week 8)

> **Duration:** 120 minutes · **Total:** 100 marks · **Coverage:** L01–L16
> (Modules 1–4). Answer **all** questions in Sections A–C and **one** of
> Section D's two choices. State assumptions; blank work earns no partial
> credit.

## Section A — Multiple Choice (10 × 2 = 20 marks)

**A1.** The frame field a switch uses for forwarding decisions:
A. Source IP · B. Destination MAC · C. TCP port · D. DNS name

**A2.** ARP poisoning succeeds because ARP:
A. Is encrypted · B. Accepts unsolicited replies without authentication ·
C. Requires DHCP · D. Uses TCP

**A3.** A switch whose MAC table overflows will typically:
A. Drop all frames · B. Flood frames to all ports (fail-open) ·
C. Reboot · D. Enable STP

**A4.** First-match-wins ACL processing means:
A. Bottom rule wins · B. Top rule matching first wins; unmatched → implicit deny ·
C. Most specific wins · D. All matching rules apply

**A5.** Stateful firewalls validate return traffic using:
A. Route tables · B. The connection/state table · C. ARP caches ·
D. NAT pools

**A6.** HMAC differs from a plain hash by:
A. Output length · B. Incorporating a secret key (origin authentication) ·
C. Speed · D. Algorithm age

**A7.** A certificate chain validates when:
A. The leaf is long-lived · B. An unexpired, unrevoked path reaches a trusted root ·
C. The key is RSA · D. The SAN is a wildcard

**A8.** IPsec tunnel mode protects:
A. Only the payload · B. The entire original IP packet (new outer header) ·
C. Only TCP · D. Only UDP

**A9.** The TLS 1.3 handshake sends the client's key share:
A. After the server certificate · B. In its first flight (ClientHello) ·
C. Never · D. Only in session resumption

**A10.** DHCP snooping's trust model:
A. All ports trusted · B. Only ports toward legitimate DHCP servers are trusted ·
C. No ports trusted · D. Trust by MAC address

## Section B — Short Answer (4 × 7.5 = 30 marks)

**B1.** Distinguish **threat**, **vulnerability**, and **risk** with one
example of each on the same asset. *(Bloom: Understand · CLO-1 · 7.5)*

**B2.** Explain how a **rogue DHCP server** harms clients (two distinct
effects), and name the switch feature that prevents it. *(Bloom: Analyze · CLO-2 · 7.5)*

**B3.** Distinguish **encryption**, **authentication**, and **integrity**
protection, and state which of the three a *digital signature* provides
beyond HMAC. *(Bloom: Understand · CLO-5 · 7.5)*

**B4.** Explain **why split-tunnel VPN on unmanaged devices** is a trust
problem, and the compensating control you'd apply if the business
requires split tunneling. *(Bloom: Evaluate · CLO-7 · 7.5)*

## Section C — Applied Analysis (2 × 15 = 30 marks)

**C1. ACL DESIGN.** Write an ordered ACL (≤6 rules, pseudocode fine) for
the management VLAN `10.99.0.0/24`:
- SSH only from jump host `10.99.0.10`,
- HTTPS monitoring only from the monitoring subnet `10.99.5.0/24`,
- all other management-plane traffic denied and logged,
- established return traffic permitted.
Label each rule; state where order matters and why. *(Bloom: Apply · CLO-3 · 15)*

**C2. PACKET ANALYSIS.** A capture from a user VLAN shows, over 5 minutes:
(i) 3,000 ARP replies claiming `10.5.0.1 is-at <MAC-X>` from three
different source MACs; (ii) one host `10.5.0.66` sending 900 DNS queries
for unique subdomains of `update-cdn[random].com`; (iii) SYN packets from
`10.5.0.66` to `10.5.0.1:445` at 50/s.
Identify **each** behavior, the attack class it represents, one immediate
containment per behavior, and the one switch feature that would have
prevented (i). *(Bloom: Analyze · CLO-2 · 15)*

## Section D — Scenario Design (choose ONE, 20 marks)

**D1. SEGMENTATION.** A hospital network: flat /16; assets = patient-record
servers, 200 workstations, guest Wi-Fi, medical IoT (infusion pumps,
vendor cloud), building access control. Propose a zone model (≥5 zones),
the flow matrix's 5 most critical rows, and the phasing that avoids
patient-care disruption. *(Bloom: Create · CLO-3 · 20)*

**D2. SECURE CHANNELS.** A firm of 500 staff migrates from password VPN to
modern access: define the authentication design (MFA types per user
class), the tunnel policy (full vs split per class), and the certificate
lifecycle supporting both. *(Bloom: Create · CLO-5/CLO-7 · 20)*

**Total: 100 marks**
