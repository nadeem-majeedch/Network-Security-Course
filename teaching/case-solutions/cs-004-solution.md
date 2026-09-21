---
case: cs-004
solution-for: modules/module-01-network-foundations/case-studies/cs-004-fragmentation-anomaly.md
difficulty: beginner
module: 1
lecture-anchor: L02
clos: [CLO-1]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-004 Solution — Fragmentation Anomaly (INSTRUCTOR ONLY)

## Model Solution

**Root cause:** PMTUD black hole. The department uplink is PPPoE (MTU 1492).
The partner server sends 1500-byte packets (MSS 1460). At the border, the
firewall drops oversized inbound packets **and** drops ICMP type 3/code 4
("fragmentation needed") toward the server, so the server never learns to
send smaller segments. Result: retransmit → drop → retransmit, stalled transfers
that recover only when the server's retransmission with a smaller segment happens to fit.

**Why only inbound leg fragments:** outbound segments (1460+40=1500B) hit the
1492 limit going out and are either clamped at the firewall or, if allowed, the
client's own PMTUD works — the client gets ICMP from a router it can hear. The
server side has no working path to learn its error.

**PMTUD (RFC 1191) in one line:** when a router must fragment a packet with DF
set, it drops it and returns ICMP 3/4 with the next-hop MTU; the sender then
lowercases its estimate. It fails silently whenever that ICMP is filtered
anywhere on the return path.

**Two candidate fixes:**

1. **MSS clamping on the border** — rewrite MSS in the TCP SYN to ~1452
   (1492−40). Pro: immediate, no protocol dependency, standard for PPPoE.
   Con: treats the symptom; hides MTU problems; all flows pay the smaller MSS
   even when a different path has full MTU; tiny per-packet efficiency loss.
2. **Allow ICMP 3/4 through the firewall both directions + verify server-side
   PMTUD behavior** — Pro: the correct, protocol-faithful fix; fixes *all*
   protocols (ESP, QUIC, DNS-over-TCP large replies), not just TCP. Con: slower
   to prove; requires the server operator's cooperation for verification;
   some middleboxes elsewhere may still break it.

**Recommended:** do both — allow ICMP 3/4 as the standing rule, and clamp MSS
on the PPPoE uplink as belt-and-braces. Documentation must say why, so nobody
"optimizes" ICMP away next year.

## Alternative Solutions

- **Raise MTU on internal segment** — doesn't help; the bottleneck is the
  PPPoE uplink's 1492, not the internal LAN.
- **Force everyone to TCP MSS 1400 globally** — works but leaves a permanent
  hidden tax on throughput; a config archaeology trap for future admins.

## Tradeoffs

- Correctness vs speed of fix: clamping is minutes; the ICMP fix needs
  change windows and cross-team verification.
- Explicit-but-fragile (PMTUD) vs implicit-but-robust (clamping) — classical
  network-engineering tension, worth 2 minutes of debrief alone.

## Common Mistakes

- Blaming the server "for being slow" instead of reading the size budget.
- "Block all ICMP" folklore applied without distinguishing type/code.
- Fixing only the outbound leg and declaring victory — the black hole is on the
  inbound-ICMP path.
- Assuming fragmentation *reassembly* is the problem; reassembly is not
  happening here because fragmentation isn't — drops are.

## Instructor Prompts

- "Where exactly does the 'frag needed' ICMP die in your diagram?"
- "Would IPv6 change this story? (It has no router fragmentation.)"
- "How would you *verify* the fix, not just apply it?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Size-budget arithmetic; black-hole mechanism precisely located |
| Technical accuracy | 25% | PMTUD described correctly; no protocol-fairies (e.g., ICMP as monolith) |
| Alternatives considered | 20% | Both fixes with named tradeoffs, recommendation justified |
| Communication | 15% | Clear packet-walk narrative |

**Timing:** reveal at 5:00; debrief the ICMP-folklore and IPv6 questions.

## CLO Mapping

- **CLO-1** — Protocol mechanics → availability diagnosis.
