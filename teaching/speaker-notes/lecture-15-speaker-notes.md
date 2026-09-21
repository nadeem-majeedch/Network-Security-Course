---
lecture: L15
module: 4
week: 8
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L15 Speaker Notes — IPsec & Legacy VPN Architecture

## Delivery Guide
IPsec intimidates students until the failure taxonomy organizes it: proposals,
auth, NAT-T, MTU, rekey. Teach the components quickly (ESP/SA/SPI), then spend the
saved minutes on the taxonomy with the capture playback (INIT/AUTH visibility,
port float). The design checklist is the deliverable — students leave with a
one-page sheet they'll build from in Lab-08. Midterm is next session (W8): remind
scope explicitly.

## Timing Plan
0–10 recap (L13/L14 → IKE uses both) · 10–35 components + modes (packet diagrams) ·
35–60 IKEv2 walk + failure taxonomy · 60–70 break · 70–90 route-based design ·
90–110 design sheet + build kickoff · 110–120 exit ticket + midterm scope. 
**Compression:** AH history to one slide; the taxonomy and design sheet are the
graded spine.

## Teaching Demonstrations
1. Tunnel-mode packet diagram: nested headers drawn live; SPI pointed at in the ESP header.
2. Capture playback: INIT visible → AUTH payload → encryption boundary; NAT-T float 500→4500 annotated.
3. `statusall` read: SA states + rekey timers — connect the 2 a.m. outage story to the timers.

## Expected Student Difficulties
1. "IPsec = one thing" — the component split (ESP vs IKE vs policy bases) must be explicit.
2. Proposal-mismatch errors read as gibberish — map log phrases to the taxonomy line by line.
3. VTI vs policy-based confusion — the routing-vs-selector distinction, with the hub-spoke example.

## Discussion Facilitation
Q3 (certs vs PSK rotation at 200 sites) is the design-judgment question: the best
answers cost out *rotation logistics*, not crypto strength. Q5 (monitoring) bridges
to L21 — SA-state as first-class telemetry; elicit the alert (SA-down threshold).

## Lab Troubleshooting (build-kickoff context)
- INIT completes, AUTH fails: identity/psk/cert mismatch — taxonomy line 2; check `statusall` messages.
- No proposals accepted: mismatched suite strings — diff both configs side by side.
- One-way traffic: NAT-T/firewall — check UDP/4500 allow and ESP filter; classic line 3.

## Accessibility Notes
- Nested-header diagrams: text-form versions (layer list) distributed.
- Log excerpts: annotated text files, not screenshots-only.

## CS & Data Science Applications
- **CS:** IKE is a negotiated protocol like TLS — same state-machine reading skill; SAs are keying-state they can reason about.
- **DS:** rekey-timer analysis is periodicity in logs again; SA-state alerting is threshold detection — continuity with their analytics thread.

## Links
Plan: `modules/module-04-crypto-protocols/lectures/lecture-15-ipsec-legacy-vpn-architecture.md` · Student page: `docs/lectures/lecture-15-ipsec-legacy-vpn-architecture.md` · Answers: `teaching/answer-keys/answer-key-module-04.md`
