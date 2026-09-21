---
case: cs-005
solution-for: modules/module-01-network-foundations/case-studies/cs-005-icmp-misuse-red-flags.md
difficulty: beginner
module: 1
lecture-anchor: L02
clos: [CLO-1]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-005 Solution — ICMP Misuse Red Flags (INSTRUCTOR ONLY)

## Model Solution

**Row classification:**

| Row | Verdict | Reason |
|---|---|---|
| NMS polling (8/0 out/in) | normal | matches baseline shape, volume, periodicity |
| Router port-unreachable 3/3 out | normal | routine error signaling |
| frag-needed 3/4: zero in baseline window | notable | absence is information: if any host needed PMTUD signals, they'd appear; correlate with TCP stalls |
| timestamp 13/14 from 2 external IPs | notable | reconnaissance-ish, low volume — record IPs, not tonight's fire |
| .77/.78/.90 echo flood out, 1400 B, 1/s, random destinations | **red flag** | steady-state exact-size, many-destination echo pattern = amplification/reflection abuse (smurf-style) or beacon-style coordination |

**Two attacker purposes for the .77/.78/.90 row:**

1. **DDoS participation (amplification/reflection source or direct flood):**
   hosts send exactly-1400-byte echoes to random reflectors/victims.
   Distinguishing test: the inbound 0-responses from *random* IPs at nearly
   matching volume — a victim/reflector answering your hosts — plus the
   "unreachable" payloads inside replies (spoofed-source evidence).
2. **Covert channel / beacon (data-out or C2-over-ICMP):** steady 1/s
   exact-size echoes are a classic covert-channel carrier. Distinguishing
   test: destinations would be *few and stable* (a C2 set), not random; and
   payload entropy in a packet capture would show structure, not padding.

The evidence as given (random destinations, matching inbound replies) points
to **DDoS participation**; a 2-minute full packet capture of .77/.78/.90
resolves it definitively (few stable destinations + structured payload ⇒ C2).

**Tonight?** Wake the analyst: the pattern is consistent with your hosts
participating in attacking others — legal/reputational exposure and a
compromise indication on two/three internal hosts. One sentence of
justification is enough; this is exactly what an analyst wants at 02:10.

## Alternative Solutions

- **Defer to morning** — defensible only if you can bound the harm (rate-limit
  ICMP outbound at the edge *first*, then look at 8 a.m.). If you can't bound it
  tonight, deferring is negligence.
- **Block ICMP outbound entirely** — treats the symptom, breaks PMTUD and
  diagnostics, and blinds you to the C2-alternative; rate-limit + investigate
  is the defensible move.

## Tradeoffs

- Rate-limiting (fast, coarse) vs full-block (blunt, breaks things) vs
  per-host containment (precise, slower).
- Waking the analyst vs staffing economics — the pattern (your hosts attacking
  others) is precisely the class of event where cost of being wrong (legal,
  reputation) exceeds staffing cost.

## Common Mistakes

- Fixating on the +800% headline number instead of the shape.
- Flagging the NMS rows because "ICMP is bad."
- Treating timestamp-REQ 13/14 as the red flag (low volume, reconnaissance
  flavor, not tonight's problem).
- Missing the inbound-reply correlation that discriminates DDoS-participation
  from C2-beaconing.

## Instructor Prompts

- "What payload entropy would you expect in each hypothesis?"
- "Why exactly 1400 bytes? (Just under the classic 1500 minus overhead —
  crafted to fit one link layer; ask what that implies about intent.)"
- "Who do you call *first* — the security manager or the ISP abuse desk?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Shape-over-volume reasoning; both hypotheses named with discriminating tests |
| Technical accuracy | 25% | Correct ICMP semantics; no monolith-ICMP claims |
| Alternatives considered | 20% | Defer-vs-wake with a bounded-harm condition |
| Communication | 15% | Decisive one-sentence recommendation |

**Timing:** reveal at 5:00; debrief the 1400-byte question — it rewards
quantitative habit.

## CLO Mapping

- **CLO-1** — Indicator triage with protocol reasoning.
