---
lecture: L19
module: 5
week: 9
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L19 Speaker Notes — Cloud Networking I (VPC Design & Controls)

## Delivery Guide
Cloud week: the translation table (on-prem → cloud) does the conceptual lifting —
walk it once, then hold students to SG-by-reference and scoped egress in every
review. The billing-safety talk precedes any console work: hard-capped sandbox
accounts, no personal credentials. The stateless-NACL return-rule bug is the
canonical "ping works, app breaks" — demo it from the prepared environment, don't
recreate live.

## Timing Plan
0–10 recap (L17 findings → "zones as APIs") · 10–35 translation table + shared
responsibility · 35–55 SG vs NACL (stateless-return demo) · 55–65 break · 65–85
3-tier reference design (IaC side-by-side) · 85–110 VPC build + harden · 110–120
exit ticket + L20 trailer. **Compression:** shared-responsibility quiz to 3
services; the build window is Lab-09 part 2 — protect it.

## Teaching Demonstrations
1. Translation table walk: each on-prem construct → cloud analog → *security delta* (the third column is the lecture).
2. Stateless-return bug: prepared environment where ping succeeds and the app fails; class diagnoses.
3. Flow-log reading: the ACCEPT-vs-REJECT lines from the staged set — the data-tier internet attempt is the finding.

## Expected Student Difficulties
1. "Private subnet = secure" — routing + SG policy decide reachability; private is *not* a policy.
2. SG-by-CIDR habit (from firewalls) — reference-by-id scales with autoscaling; show the migration pain of CIDR hardcoding.
3. Cloud-cost anxiety — the hard-capped sandbox + "everything today is free-tier reproducible" reassurance.

## Discussion Facilitation
Q5 (who can change an SG) lands the control-plane point: the best answers pair
*IaC-only changes* with *change alarms* — governance plus detection. Q3 (NAT vs
private endpoint) has clean axes: exfil surface, cost, policy checkpoint.

## Lab Troubleshooting (build context)
- Console/IaC auth failures: sandbox profiles pre-issued; no personal accounts in the lab.
- Data-tier curl succeeds (shouldn't): route table still attached to NAT — the finding IS the lesson; have them diff routes.
- Flow logs not appearing: delivery lag (minutes) — note it; use the prepared historical set for analysis.

## Accessibility Notes
- Console screenshots: every visual step narrated; CLI alternatives provided for all actions.
- IaC snippets: plain text (they are) — emphasize copy-paste-friendly workflow.

## CS & Data Science Applications
- **CS:** SGs-as-references = capability-based access control; IaC is declarative programming — both map to CS abstractions they own.
- **DS:** flow logs are the cloud-native flow telemetry — the L21 analytics pipeline ingests exactly this format; preview the continuity.

## Links
Plan: `modules/module-05-wireless-cloud/lectures/lecture-19-cloud-networking-vpc-design.md` · Student page: `docs/lectures/lecture-19-cloud-networking-vpc-design.md` · Answers: `teaching/answer-keys/answer-key-module-05.md`
