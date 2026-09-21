---
status: complete
artifact-type: module-overview-page
module: 1
instructor-only: false
---

# Module 1 — Network Foundations

**Lectures:** L01–L04 (Weeks 1–2) · **CLOs:** CLO-1 · **Cases:** cs-001–010

*Every module page in this course is descriptive orientation: full teaching
material lives in the lecture pages and the lab workbook.*

## What this module covers

You cannot defend or investigate a network you cannot read. Module 1 builds
fluency in the protocols themselves — not from a textbook diagram, but from
live frames on a lab switch and captures on your own adapter. The security
content starts here too: the threat landscape is introduced in the same
language the packets use.

## Lectures

| # | Lecture | Core idea |
|---|---|---|
| L01 | [Security Mindset & the Network Threat Landscape](../../lectures/lecture-01-security-mindset-threat-landscape.md) | Risk vocabulary, CIA triad, why networks are attacked |
| L02 | [Protocol Deep Dive I — Ethernet, ARP, IP, ICMP](../../lectures/lecture-02-protocol-deep-dive-i-lower-layers.md) | Frame anatomy, ARP resolution, IP addressing and fragmentation |
| L03 | [Protocol Deep Dive II — TCP, UDP, DNS, DHCP](../../lectures/lecture-03-protocol-deep-dive-ii-transport-services.md) | TCP lifecycle, UDP, name resolution, address assignment |
| L04 | [Applied Packet Analysis & Web Protocols](../../lectures/lecture-04-applied-packet-analysis-web-protocols.md) | Reading real captures, HTTP/TLS layering, evidence discipline |

## Labs

[Lab-01](../../labs/lab-01-range-orientation-baseline.md) (range orientation &
first capture) and [Lab-02](../../labs/lab-02-wireshark-protocol-analysis.md)
(TCP/DNS/DHCP trace analysis) build the capture-reading fluency that every
later module depends on.

## Case studies (beginner tier)

cs-001 asset/trust-zone inventory · cs-002 lost-laptop CIA impact ·
cs-003 abnormal ARP replies · cs-004 fragmentation anomaly · cs-005 ICMP misuse ·
cs-006 TCP half-open flood · cs-007 DNS resolution misdirection ·
cs-008 rogue DHCP · cs-009 HTTP downgrade observation · cs-010 capture hygiene.
All appear on the projector with ~5 minutes reasoning before debrief —
see the [case studies guide](../../cases/index.md).

## Skills checkpoints

- Dissect Ethernet/IP/TCP headers from a hex view without a dissector cheat sheet.
- Explain why ARP and DHCP are inherently trust-on-first-use protocols.
- Trace one DNS query end-to-end and one TCP handshake in a Wireshark capture.
- State the security consequence of each protocol shortcut (no auth, no integrity).
