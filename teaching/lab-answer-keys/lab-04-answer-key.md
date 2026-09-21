---
lab: Lab-04
status: complete
artifact-type: lab-answer-key
instructor-only: true
distribution: never-publish-to-students
---

# Answer Key — Lab-04 (MITM & Flood Telemetry)

## Dataset ground truth (generated, seed 404)
202 packets. Background: 1 DNS pair (R2). **SYN wave:** 120 SYNs →
10.20.30.10:443 from rotating 198.51.100.10–209, ~10 ms apart (≈100 SYNs/s
over ~1.2 s), zero completions. **Amplify pairs:** 40× (34-byte ANY query
from spoofed 198.51.100.x → resolver 10.20.30.53) + (≈950-byte response →
victim 10.20.0.101:40000+i); measured amplification ≈ 28×.

## Worked arithmetic (grading reference)
- Backlog: 128 half-opens ÷ (100/s × 60 s timeout) → exhausted in ≈1.3 s;
  sustained exhaustion keeps legitimate SYNs unanswered → user-visible
  timeouts, not errors.
- Amplification: ≈950/34 ≈ 28×; attacker cost 34 B outbound per 950 B inbound
  to the victim — the asymmetry is the business problem, not bandwidth pride.

## Analysis-question model answers
1. **Spoofed SYNs:** no completions because the attacker never sees SYN/ACKs
   (wrong source); anyone *receiving* replies would expose the real host —
   that's why reflection inverts direction instead.
2. **SYN cookies:** trade state memory for computation; server no longer
   remembers per-connection options (e.g., some TCP options, large windows)
   during flood mode.
3. **RRL:** drops/slips responses over threshold — legitimate resolvers asking
   the same name suffer (false negatives) to protect against reflection;
   tune per qtype (ANY etc.).
4. **BCP 38:** must be deployed at *every network's egress* (spoofed packets
   die at their origin) — global adoption lags because benefit is collective
   while cost is local; upstream scrubbing remains the operative fix.
5. **Publishing 28×:** without window/dataset context it implies real-world
   resolver behavior; synthetic ANY-on-static-payload inflates vs production
   distributions — state measurement context or don't publish.

## Grading notes
- Every rate/ratio must carry its measured window; teams computing "per the
  full file" without stating it lose evidence marks (the honest-window habit).
- Layer-correct mitigations required: SYN cookies ≠ L7 rate limiting ≠ BCP 38;
  the mapping table is where this shows.
- The web-exposure task uses lab02 as baseline — reward the *contrast*
  framing (what TLS fixes vs leaves: SNI/IPs/sizes/timing remain).

## Command status
✅ Generated + verified (202 pkts, IPv4). Filters ⚠️ Wireshark shapes.
