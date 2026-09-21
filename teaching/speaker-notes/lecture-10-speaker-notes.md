---
lecture: L10
module: 3
week: 6
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L10 Speaker Notes — Firewalls: Concepts & Placement

## Delivery Guide
The state table is the star — show it, touch it, break it (asymmetric-routing
vignette). Build five rules live and plant the shadowing error deliberately: finding
it is the class's first audit win and sets up L11. The egress-policy section is the
professional differentiator; give it real minutes. The pfSense build (Lab-06 part
1) starts in-session — snapshot hygiene matters, remind students to checkpoint.

## Timing Plan
0–10 recap (one team's zone map as target) · 10–35 inspection generations + states
demo · 35–55 rulebase semantics (shadowing plant) · 55–65 break · 65–85 placement +
HA · 85–110 policy build · 110–120 exit ticket + Assignment-2 preview. 
**Compression:** HA block to slide + war story; the build window stays.

## Teaching Demonstrations
1. States-view live: generate allowed traffic, find the entry (5-tuple, timers) — "return traffic matched state, not a rule."
2. Shadowing plant: two rules, first-match kills the second; let the class prove it with a test.
3. Asymmetric-routing break: routed return path via the wrong firewall → drops; explain the design rule it teaches.

## Expected Student Difficulties
1. "Stateful = content inspection" — the states view shows tuples and timers only; DPI is a different animal.
2. Rule-order anxiety — first-match semantics + "specific before general" heuristic repeated.
3. Egress default-allow feels normal — the exfil-path walkthrough (L07 knowledge) changes minds.

## Discussion Facilitation
Q2 (TLS inspection) is a governance discussion as much as technical: steer to
breakage (pinning), privacy duties, and per-zone scoping. Q5 (allow-logging) has a
clean answer: high-value zones where *authorized* access is itself noteworthy
(mgmt, data tiers).

## Lab Troubleshooting (pfSense build context)
- GUI unreachable: wrong interface assignment — the interfaces page first, always.
- NAT/bridge confusion on the range: use the prepared snapshots; do not rebuild.
- Rules "not working": check rule order and interface binding before content — 90% of cases.
- Session loss on save: normal (state flush on some changes) — tell them in advance to avoid panic.

## Accessibility Notes
- GUI demos: describe each click + field aloud; provide keyboard-path alternatives.
- Rule listings: distribute as text; color-coding gets text labels.

## CS & Data Science Applications
- **CS:** the state table is a hash map with TTLs — data-structure framing helps CS students reason about capacity and lookups.
- **DS:** rulebase hit-counters and deny logs are the datasets they'll baseline in L21; mention log-to-analytics continuity.

## Links
Plan: `modules/module-03-secure-architecture/lectures/lecture-10-firewalls-concepts-placement.md` · Student page: `docs/lectures/lecture-10-firewalls-concepts-placement.md` · Answers: `teaching/answer-keys/answer-key-module-03.md`
