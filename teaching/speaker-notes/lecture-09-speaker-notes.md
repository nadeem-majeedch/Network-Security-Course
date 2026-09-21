---
lecture: L09
module: 3
week: 5
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L09 Speaker Notes — Defense in Depth & Network Segmentation

## Delivery Guide
Module 3 pivots from attacks to defense — open by mapping each Module-2 attack to
the defense layer that blunts it (board exercise, 3 minutes). The 5-step method is
the lecture: walk it once on the flat-office diagram, then get out of the way and
let teams run it. Zero trust lands better as "verify explicitly per session" than
as a slogan; SP 800-207 tenets on one slide, no more.

## Timing Plan
0–10 Module-2 recap mapping · 10–35 DiD + segmentation method · 35–55 VLAN/zone/DMZ
patterns (failure-mode table) · 55–65 break · 65–85 zero trust · 85–110 design
sprint · 110–120 exit ticket + Assignment-1 briefing. **Compression:** zero-trust
to one tenet slide; the failure-mode table ("what does pwned-webserver reach?")
cannot be cut — it is the design driver.

## Teaching Demonstrations
1. Failure-mode table filled live: single-leg DMZ vs back-to-back vs reverse proxy — same attack, three answers.
2. Flow-table→zones derivation: show the flows, derive the zones in front of them.
3. Microsegment preview: one Kubernetes NetworkPolicy slide (full treatment L20).

## Expected Student Difficulties
1. VLAN = security boundary (the big one) — enforce the distinction in every design critique this week.
2. Design paralysis from perfectionism — the method is iterative; "flows first, revise later."
3. Zero-trust as buzzword — force tenet-level statements ("which tenet does your control serve?").

## Discussion Facilitation
Q1 (flows vs org charts): elicit a *failure story* of org-chart design (marketing
VLAN includes the CRM nobody mapped). Peer-attack round: require attackers to name
the Module-2 attack they are using — it keeps critiques technical, not aesthetic.

## Lab Troubleshooting (design-sprint context)
- Teams without their L01 inventory: provide the standard department template.
- Diagram tooling rabbit-holes: paper is fine; the *policy table* is the deliverable.
- Scope creep into firewall CLI detail: that's L10 — park it.

## Accessibility Notes
- Zone maps: require text legends (zone name + policy) so all visual designs are screen-readable.
- Sprint timeboxing: visible countdown; accommodations per policy.

## CS & Data Science Applications
- **CS:** segmentation = access-control graphs; policy tables are rulesets they can compile — a compiler metaphor lands well.
- **DS:** flow tables are the raw material for zone derivation — clustering flows by source/dest/service is a genuine DS micro-project; offer it as optional stretch.

## Links
Plan: `modules/module-03-secure-architecture/lectures/lecture-09-defense-in-depth-segmentation.md` · Student page: `docs/lectures/lecture-09-defense-in-depth-segmentation.md` · Answers: `teaching/answer-keys/answer-key-module-03.md`
