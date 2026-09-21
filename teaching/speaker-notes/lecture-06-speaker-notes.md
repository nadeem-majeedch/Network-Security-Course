---
lecture: L06
module: 2
week: 3
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L06 Speaker Notes — Layer-2 & LAN Attacks

## Delivery Guide
Deliver the safety framing *first and verbatim* — this is the first technique
lecture. The unifying thesis does the teaching: **every L2 attack is a lie told to a
learning protocol**. All attack "demos" are instructor-run on the isolated range;
students receive captures and logs. Build the §3.6 attack→control→evidence table
*with the class* — it is kept as a course artifact and reused in L22's rule work.

## Timing Plan
0–10 recap (trees → leaves) · 10–35 ARP spoofing (capture + whiteboard) · 35–55
flooding/STP/VLAN hop (log samples) · 55–65 break · 65–75 control-mapping table ·
75–110 observation lab · 110–120 exit ticket. **Compression:** the STP block can go
to a slide if behind; ARP and the mapping table cannot.

## Teaching Demonstrations
1. Poisoned-capture playback: the duplicate IP→MAC moment — students call out the frames.
2. Switch-log exhibit pack: `show ip arp inspection statistics`, `show spanning-tree root`, MAC-table growth — read-only, annotated.
3. Double-tag anatomy on the whiteboard: two tags, ingress strip, inner tag lands — preconditions listed.

## Expected Student Difficulties
1. "Switches prevent this" — re-anchor to L02: learning ≠ validating.
2. DAI/snooping dependency confusion — draw the binding-table pipeline (snooping feeds DAI).
3. Port-security anxiety (will it break my laptop?) — legitimate-churn tuning is the answer; say it concretely.

## Discussion Facilitation
Q2 (port-security FPs) rewards specificity: IP phones + PC daisy-chains are the
classic churn source. Q4 (misconfig reopening VLAN hops): accept DTP-enabled,
native-VLAN-shared, untagged-native answers with preconditions — precision here
predicts Assignment-2 audit quality.

## Lab Troubleshooting (observation context)
- Range capture missing ARP frames: capture filter too tight (BPF `arp` required).
- Switch CLI access denied: roster credentials stale — re-issue; do not widen access.
- Teams conflating two exhibits: label every file with the attack name up front.

## Accessibility Notes
- The §3.6 table is the lesson: distribute it *before* the lab; read it aloud.
- Log exhibits: provide text copies for screen readers; describe trend arrows verbally.

## CS & Data Science Applications
- **CS:** protocol trust models map to API design (validate inputs); DAI = schema validation at L2 — a framing CS students adopt instantly.
- **DS:** duplicate-binding detection is a temporal anomaly-detection exercise (same entity, changing attributes) — a clean mini-dataset for the analytics-inclined.

## Links
Plan: `modules/module-02-network-threats/lectures/lecture-06-layer2-lan-attacks.md` · Student page: `docs/lectures/lecture-06-layer2-lan-attacks.md` · Answers: `teaching/answer-keys/answer-key-module-02.md`
