---
lecture: L02
module: 1
week: 1
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L02 Speaker Notes — Protocol Deep Dive I (Ethernet, ARP, IP, ICMP)

## Delivery Guide
The lecture's one thesis: **L2/L3 protocols trust without authenticating** — repeat
it at each protocol. Use Wireshark's byte view, not just the dissection tree; seeing
hex makes "fields are just bytes" concrete. Plant the L06 preview deliberately
("remember this reply-accepted-without-request fact — it becomes an attack in two
weeks"). IPv6 gets orientation depth only; do not rabbit-hole into extension
headers.

## Timing Plan
0–10 oral recap (CIA/vantage) · 10–35 Ethernet + CAM (2-VM demo) · 35–55 ARP
whiteboard + capture · 55–65 break · 65–85 IPv4 fields + IPv6 deltas · 85–110
frame-map worksheet · 110–120 exit ticket. **Compression:** drop the fragmentation
demo to a static slide; keep the ARP walkthrough at full length.

## Teaching Demonstrations
1. CAM-table demo: two VMs ping; show `show mac address-table` (or bridge FDB) before/after — "the switch learned by listening to source MACs."
2. Unsolicited-reply observation: play the prepared capture where a reply arrives with no request; let students spot it.
3. PMTUD live: `ping -s 2000 -M do` fails; regular `ping -s 2000` fragments — annotate ip.flags/offset on screen.

## Expected Student Difficulties
1. Wildcard-free zone: students conflate FCS with integrity — the corruption-vs-tampering sentence must be said three times.
2. "The switch protects hosts" — show that ARP processing happens on hosts, not the switch.
3. Hex discomfort — pair strong/weak students for the worksheet.

## Discussion Facilitation
Q1 (FCS) is a precision check — accept "detects corruption" only with the reason
(no authenticity). Q3 (ICMP block-all): push for *consequences* (PMTUD), not
opinions; the best answers cite type 3/code 4.

## Lab Troubleshooting (capture context)
- Monitor/NPCAP driver missing → capture fails: pre-install and verify on images.
- Students capture nothing: wrong interface (Wi-Fi vs Ethernet) — have them confirm the active interface first.
- Fragmented ping blocked on some lab WLANs: use the wired segment.

## Accessibility Notes
- Hex projections: read key fields aloud and provide the annotated screenshot.
- Color-coded packet annotations must have shape/text redundancy (not color-only).

## CS & Data Science Applications
- **CS:** ARP/CAM are state machines — map to the FSM concepts from their systems courses; spoofing = invalid state transition.
- **DS:** capture files are structured telemetry; mention that field-level parsing (EtherType, TTL distributions) is exactly the feature-engineering they will do on flow data in L21.

## Links
Plan: `modules/module-01-network-foundations/lectures/lecture-02-protocol-deep-dive-i-lower-layers.md` · Student page: `docs/lectures/lecture-02-protocol-deep-dive-i-lower-layers.md` · Answers: `teaching/answer-keys/answer-key-module-01.md`
