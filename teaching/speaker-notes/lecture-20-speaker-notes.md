---
lecture: L20
module: 5
week: 10
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L20 Speaker Notes — Cloud Networking II (Hybrid & Assurance)

## Delivery Guide
Non-transitive peering is the week's best "aha": draw it, break it, fix it with the
hub. Container networking is L09's flat network reborn — the parallel makes
NetworkPolicy intuitive; the enforcement check ("does your CNI actually enforce?")
is the professional skepticism to install. Module 5 closes here; Quiz 4 (W10)
samples L17–L20. Preview Module 6 as "you've built the network — now we watch it."

## Timing Plan
0–10 Quiz-4 debrief highlights (after exam window) — or Module-5 recap if quiz
runs at L18 · 10–35 hybrid patterns + transitivity bug · 35–55 private endpoints +
hybrid DNS · 55–65 break · 65–90 container networking (NetworkPolicy live) · 90–110
flow-log + drift-alarm lab · 110–120 exit ticket + Module-6 trailer. 
**Compression:** DNS deep-dive to the failure vignette; the transitivity bug and
NetworkPolicy enforcement check are non-negotiable.

## Teaching Demonstrations
1. Transitivity bug (sandbox): SpokeA↔Hub OK, SpokeB↔Hub OK, A↔B black-hole — fix via hub routing; show the route-table diff.
2. NetworkPolicy live: default-deny on the DB → denied test pod → api→db allow — then the enforcement question.
3. Drift alarm: trigger a benign SG change; the alarm fires — "who changed the firewall at 02:00" answered.

## Expected Student Difficulties
1. Peering-transitivity intuition (on-prem routers *are* transitive) — the diagram repetition is needed.
2. "Policies exist so we're covered" — the enforcement-prerequisite finding (CNI) is the audit reality.
3. Default-deny feels drastic — the allow-pairs restore function; design-method continuity from L09.

## Discussion Facilitation
Q2 (DNS breaks hybrids) rewards the split-horizon failure story (internal names
leaking) — connect to L03's resolver trust. Q5 (managed-K8s responsibility rows) is
capstone preparation: the matrix format repeats there.

## Lab Troubleshooting (flow-log + alarm context)
- Alarm doesn't fire: event-recorder scope misconfigured — check the resource type filter.
- NetworkPolicy "ignored": CNI without enforcement — that's the planted lesson; then switch to the enforcing CNI in the sandbox.
- Kubectl/helm version friction: pinned versions in the lab sheet.

## Accessibility Notes
- Route-table diffs: text-form provided; describe arrow directions verbally.
- K8s manifests: plain YAML (inherently accessible); read selector lines aloud.

## CS & Data Science Applications
- **CS:** NetworkPolicy selectors are label-based access control — k8s RBAC parallel; CNI enforcement = plugin architecture they know.
- **DS:** drift detection = state-vs-declared diffing at scale — an anomaly-detection framing; flow-log novelty detection previews L21/L23.

## Links
Plan: `modules/module-05-wireless-cloud/lectures/lecture-20-cloud-hybrid-assurance.md` · Student page: `docs/lectures/lecture-20-cloud-hybrid-assurance.md` · Answers: `teaching/answer-keys/answer-key-module-05.md`
