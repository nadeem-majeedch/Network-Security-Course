---
lecture: L05
module: 2
week: 3
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L05 Speaker Notes — Threat Modeling & Attacker Anatomy

## Delivery Guide
Module 2 opens with the *thinking* tools before the techniques. Build one attack
tree live and let students watch the minimum-cut reasoning happen; then hand the
method to them. The ATT&CK section's payoff line: "each technique page names its
data sources — that's your detection backlog speaking." Keep the kill-chain
criticism honest (non-linear reality) — students respect the caveat and it models
intellectual honesty.

## Timing Plan
0–10 ATT&CK headline sorting · 10–35 vocabulary + live tree · 35–55 kill chain +
ATT&CK narrative mapping · 55–65 break · 65–85 recon taxonomy (flow-log shapes) ·
85–110 team tree-building · 110–120 exit ticket. **Compression:** headline sorting
to 3 cards; the live tree is non-negotiable.

## Teaching Demonstrations
1. Live attack tree on the small-office diagram — AND/OR semantics, then minimum cuts, annotated.
2. Narrative→ATT&CK mapping on the matrix (projected): invoice.docm → T1566 → T1204 → T1071.001 → T1135 → T1567.002.
3. Flow-log scan shapes: `-sS` vs `-sV` patterns side by side (prepared extracts).

## Expected Student Difficulties
1. AND vs OR confusion — the AND-branch-kills trick ("one control kills the whole AND") needs two examples.
2. ATT&CK-as-checklist mindset — correct with the data-sources column: it's a *mapping* tool.
3. Passive recon feels useless ("can't detect it") — redirect to exposure reduction.

## Discussion Facilitation
Q2 (technique page → detection) is the bridge to Module 6; elicit: behavior → data
source → query — write the triple on the board and revisit in L21. For the tree
critique, attack *assumptions* ("your tree assumes the attacker starts outside"),
not the students.

## Lab Troubleshooting (observation-lab context)
- Flow extracts misformatted: provide the canonical CSV; parsing is not today's objective.
- Teams over-model (20 branches): cap at 3 top branches — depth over breadth.
- ATT&CK site slow offline: have the printed matrix page set ready.

## Accessibility Notes
- The tree diagram: provide the textual hierarchy (goal → branches → leaves) — it doubles as the screen-reader version.
- Cards: large-print and digital versions.

## CS & Data Science Applications
- **CS:** attack trees are DAGs — direct graph intuition from their algorithms course; minimum cut is a *real* graph-algorithm concept.
- **DS:** ATT&CK-mapped incident corpora support classification tasks; mention technique co-occurrence analysis as a DS final-project seed.

## Links
Plan: `modules/module-02-network-threats/lectures/lecture-05-threat-modeling-attacker-anatomy.md` · Student page: `docs/lectures/lecture-05-threat-modeling-attacker-anatomy.md` · Answers: `teaching/answer-keys/answer-key-module-02.md`
