---
lecture: L03
module: 1
week: 2
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L03 Speaker Notes — Protocol Deep Dive II (TCP, UDP, DNS, DHCP)

## Delivery Guide
Two theses: **TCP is a readable story; UDP's source address is taken on faith**;
and **DNS/DHCP are unauthenticated trust oracles**. Follow TCP Stream live — the
moment students see a conversation reassembled, triage clicks. The DNS TXID +
5-tuple discussion is the intellectual center: it explains both the historical
poisoning arms race and why DoT/DoH changes visibility (L23 setup). Stage capture
(b) has three planted faults — do not reveal the count until after the hunt.

## Timing Plan
0–10 recap + exit-ticket debrief · 10–35 TCP lifecycle (stream follow) · 35–50 UDP
+ reflection setup · 50–60 break · 60–85 DNS + DHCP (dig +trace, DORA) · 85–110
anomaly hunt · 110–120 exit ticket + Quiz-1 reminder. **Compression:** merge the
UDP block into the TCP segment; keep the anomaly hunt at full length.

## Teaching Demonstrations
1. Follow TCP Stream on a lab HTTP fetch — show the narrative; then flags view for the handshake.
2. `dig +trace` on the projector — narrate root→TLD→authoritative; who answers authoritatively?
3. DORA capture with a *second OFFER* planted — let students discover it; it's the rogue-DHCP seed for L06.

## Expected Student Difficulties
1. Sequence-number confusion — draw the two number lines (client/server) on the board.
2. TXID "feels like authentication" — it is a 16-bit demux field, not a secret; say so explicitly.
3. Short TTLs read as malicious — CDN counterexample resets intuition.

## Discussion Facilitation
Q1 (random-subdomain SOC alert): demand *discriminating tests*, not verdicts — this
is the course's first hypothesis-driven moment and predicts L28 performance. If the
room splits evenly, that's a win: it means the evidence is genuinely ambiguous
without the resolver's log.

## Lab Troubleshooting (trace-analysis context)
- dig +trace blocked by resolver policy: provide the fallback prepared output.
- DHCP capture empty: lab segment has a relay — capture on the relay leg or use the prepared file.
- Wireshark protocol-resolution noise: disable "decode as" heuristics if DNS looks odd.

## Accessibility Notes
- Read capture lines aloud; provide text transcripts of key frames.
- The whiteboard TCP diagram: also distribute as a slide with labeled arrows.

## CS & Data Science Applications
- **CS:** TCP state machine = classic FSM; half-open backlog is a resource-exhaustion pattern they'll meet in OS courses.
- **DS:** NXDOMAIN ratios, TTL distributions, and TXID entropy are concrete statistics on logs — name them as such; L23 builds detectors from exactly these.

## Links
Plan: `modules/module-01-network-foundations/lectures/lecture-03-protocol-deep-dive-ii-transport-services.md` · Student page: `docs/lectures/lecture-03-protocol-deep-dive-ii-transport-services.md` · Answers: `teaching/answer-keys/answer-key-module-01.md`
