---
lecture: L04
module: 1
week: 2
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L04 Speaker Notes — Applied Packet Analysis & Web Protocols

## Delivery Guide
Module 1 closes with **tool fluency + Quiz 1**. Open with the quiz (0–20) to
guarantee clean timing, then teach filters as *questions*, not syntax: every demo
filter answers a stated question, and students predict result counts before you run
it — prediction makes learning visible. The cleartext-vs-TLS side-by-side is the
theoretical hinge for Module 6 ("metadata survives"). End by assigning the triage
workflow as a personal habit, not a class exercise.

## Timing Plan
0–20 **Quiz 1** (administer; 20-min hard stop) · 20–45 filter craft · 45–65
HTTP/TLS visibility · 65–75 break · 75–105 triage drill (timed) · 105–115 case
debrief · 115–120 Module-2 trailer. **Compression:** triage drill can drop to one
capture pair if the quiz runs long — never skip the debrief.

## Teaching Demonstrations
1. Ten filters live, students predicting counts first — keep a tally on the board.
2. Cleartext login vs same-over-TLS: list on the board what survived (SNI, sizes, timing, DNS) — the Module-6 contract.
3. `tshark -T fields` headless triage — for server-room realism.

## Expected Student Difficulties
1. Capture vs display filter confusion — rule: "capture constrains collection; display refines analysis" (repeat).
2. Base64 = encryption belief — decode one Basic-auth header live; the reveal is memorable.
3. Triage paralysis on unknown captures — enforce the checklist order strictly; the discipline is the skill.

## Discussion Facilitation
Q5 (first statistics view): there is no single right answer — grade the *reasoning*;
push for "protocol hierarchy → conversations" as the defensible default and why.
The cross-pair comparison in the drill: frame disagreement as the lesson (same
evidence, different inference → citations close the gap).

## Lab Troubleshooting (triage context)
- Slow Wireshark on big files: teach display-filter early application + restricted column sets.
- `capinfos` missing on student laptops: use Wireshark's Summary; the field names differ slightly — say so.
- HTTP objects export empty: the capture may be TLS-only — that *is* the lesson; pivot to metadata.

## Accessibility Notes
- Screen-reader users: provide the filter list as text; describe the IO-graph shapes verbally ("flat, then a 60-second spike train").
- Timed drill: offer a time-and-a-half accommodation per institutional policy.

## CS & Data Science Applications
- **CS:** this is grep-for-packets — connect to their pipeline/tooling instincts; tshark fields map to CSV/JSON exports for tooling.
- **DS:** protocol hierarchy and conversation tables are frequency tables; beacon cadence is periodicity detection — the same skills on NetFlow in L21.

## Links
Plan: `modules/module-01-network-foundations/lectures/lecture-04-applied-packet-analysis-web-protocols.md` · Student page: `docs/lectures/lecture-04-applied-packet-analysis-web-protocols.md` · Answers: `teaching/answer-keys/answer-key-module-01.md`
