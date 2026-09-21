---
lecture: L01
module: 1
week: 1
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L01 Speaker Notes — Security Mindset & the Network Threat Landscape

## Delivery Guide
This is a vocabulary-and-posture lecture, not a tools lecture. Anchor everything to
the CIA triad and the four vantage points — both recur in every later module. Open
with the cold-call ("what does secure mean?") and *keep the answers on the board*;
you will re-map them into CIA at minute 35 and students should watch that happen.
The ethics contract must be delivered verbatim from the course policy — it is the
license for every lab that follows. End by naming the artifact spine: "every module
gives you a professional format; today's is the trust-zone inventory."

## Timing Plan
0–10 warm-up cold-call · 10–35 risk + CIA (chalk-talk on campus poster) · 35–50
mini-case think-pair-share · 50–60 break + lab credentials · 60–85 actors +
vantage points (headline sorting) · 85–110 trust-zone inventory · 110–120 exit
ticket. **Compression guidance:** if behind, cut headline sorting to 3 headlines;
never cut the ethics section.

## Teaching Demonstrations
1. Residential-router admin page (HTTP) vs SSH session side by side — ask which CIA leg each protects and which vantage defeats it. Setup: two VMs, same switch; screenshots as backup.
2. `traceroute` to a campus host — label each hop's vantage class. No live attack content; pure mapping.
3. Headline pack (5 anonymized public incidents) — printed cards; no live links needed.

## Expected Student Difficulties
1. Confusing *threat* with *vulnerability* — force the sentence template: "If ⟨threat⟩ exploits ⟨vulnerability⟩…".
2. Believing insiders are out of scope — the negligent-admin statistic lands better than assertions.
3. Treating "risk" as vague — demand likelihood × impact phrasing every time.

## Discussion Facilitation
Q4 ("firewall = secure?") is the misconception detector: reward students who
name *what the firewall does not cover* rather than those who just say no. For
quiet rooms, run think-pair-share before cold-calling. Park strong wrong answers
on a "parking lot" board — revisit in L05.

## Lab Troubleshooting (Lab-01 context)
- Students can't reach the lab range: 90% wrong VLAN/subnet on the VM NIC — have them check adapter settings before you touch the host.
- Credential distribution failures: keep a printed fallback roster; never extend admin rights as a workaround.

## Accessibility Notes
- The topology poster is verbal-critical: describe every zone aloud as you point.
- Offer the trust-zone inventory in template form (table) for students who prefer structure.
- Headline cards: provide digital text versions for screen-reader users.

## CS & Data Science Applications
- **CS:** connect vantage points to socket/ NIC programming they know (who can bind where); the flat-network problem reappears in their distributed-systems courses.
- **DS:** headline classification is a labeling exercise — mention that incident datasets (e.g., VERIS/DBIR) are structured, analyzable corpora they will use in L21/L23 analytics.

## Links
Plan: `modules/module-01-network-foundations/lectures/lecture-01-security-mindset-threat-landscape.md` · Student page: `docs/lectures/lecture-01-security-mindset-threat-landscape.md` · Answers: `teaching/answer-keys/answer-key-module-01.md`
