---
lecture: L08
module: 2
week: 4
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L08 Speaker Notes — DoS/DDoS & Infrastructure Abuse

## Delivery Guide
Classification before mitigation: the taxonomy table is the lecture's spine, and
the telemetry triage only works if students classify first. The amplification
arithmetic (compute the factors) grounds the "spoofable UDP" claim in numbers. The
flood telemetry pack comes from the instructor-run range stress test — say so; no
student-generated floods, ever. Quiz 2 runs at the end of this session.

## Timing Plan
0–10 flood-classification warm-up · 10–35 taxonomy + SYN mechanics · 35–55
amplification math + BCP 38 · 55–65 break · 65–85 botnets/C2 signatures · 85–110
telemetry triage · 110–120 **Quiz 2**. **Compression:** the C2 block can compress
to the signature table; the triage cannot — it's Quiz-2's practical rehearsal.

## Teaching Demonstrations
1. Telemetry pack walkthrough: one flood file classified live (layer, type, source character via TTL reasoning).
2. Amplification math on the board: request/response sizes → factors → abuse ranking.
3. SYN-backlog graph (prepared plot): backlog rise → cookie engagement → legit-success recovery — three phases annotated.

## Expected Student Difficulties
1. "More bandwidth" reflex — the 400 Gbps-vs-budget arithmetic deflates it; CDN absorption reframes the buy.
2. Confusing volumetric with protocol floods — the *shape* (bytes vs state) is the discriminator; make them say it.
3. BCP 38 feels like someone else's job — the egress-flood detection angle (your compromised hosts) makes it self-interest.

## Discussion Facilitation
Q3 (SYN cookie option loss): the precise answer (certain TCP options deferred) is
beyond scope — reward students who identify *statelessness* as the trade. Q5
(egress spikes): connect explicitly to L21 — this is the first detection-feed
moment of the course.

## Lab Troubleshooting (telemetry context)
- nfdump syntax variance across versions: provide the exact command sheet for the installed version.
- Students over-filter (empty output): teach broad-first; refine second.
- Timezone confusion in the telemetry: all files UTC-stamped — enforce UTC reading.

## Accessibility Notes
- Graphs: describe axes and inflection points aloud; provide the plot description text.
- Classification table: pre-distributed; verbal walkthrough of each row.

## CS & Data Science Applications
- **CS:** backlog exhaustion is resource-exhaustion scheduling — connects to OS concurrency units.
- **DS:** volumetric detection is threshold/anomaly detection on time series; amplification factors are just ratios — invite the DS students to compute per-service stats for the class.

## Links
Plan: `modules/module-02-network-threats/lectures/lecture-08-dos-ddos-infrastructure-abuse.md` · Student page: `docs/lectures/lecture-08-dos-ddos-infrastructure-abuse.md` · Answers: `teaching/answer-keys/answer-key-module-02.md`
