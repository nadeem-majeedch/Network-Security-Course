---
case: cs-086
title: Post-Incident Review That Produces Change (Solution)
difficulty: expert
module: 7
lecture-anchor: L27
clos: [CLO-14]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-086 — Solution: Post-Incident Review That Produces Change

> **INSTRUCTOR ONLY.** Model solution for cs-086.

## Model Solution

### 1. Review format redesign

**Inputs (mandatory before the meeting):** timeline (assembled from
logs, not memory), alert configuration history (would have shown the
disabled alert), MTTR/MTTD numbers, cost estimate of the incident.

**Agenda (60 min, roles assigned):**
1. Timeline walk (10) — facilitator narrates; no editorializing.
2. Contributing-factor analysis (20) — "what made each step easy?"
   (the disabled alert, the missing NDR, the VPN without MFA) —
   *systems*, not people.
3. Action item negotiation (20) — each factor becomes ≤2 items with
   owner, date, done-state; the group must reach agreement or
   escalate, not defer.
4. Close (10) — read back every item; facilitator confirms each is
   contract-shaped.

**Roles:** facilitator (process owner, not stakeholder), scribe,
system owners (the people who can commit), one exec sponsor (present
for the last 10 minutes, signs the item list).

**Blameless mechanics that surface the hidden fact:** the alert
config history is *automatically* in the input pack — the disabled
alert appears as a system fact ("alert X silenced 3 weeks prior"),
not a confession. Norm stated up front: "We analyze the system that
allowed silencing, not the person who silenced it." The follow-through
then fixes the *system* (change control on alert configs).

### 2. Conversion rule

A real item = **owner (named person) + date + observable done-state
+ verification method**. Applied:

| Vague item | Converted |
|---|---|
| "Review external access" | "Owner: NetEng lead. By Mar 15. Done-state: VPN requires MFA for all groups (pilot group exempted list ≤5 named accounts, approved by CISO). Verification: config export attached to the item." |
| "Consider better monitoring" | "Owner: SOC lead. By Apr 1. Done-state: Zeek sensor deployed on server VLAN; SMB staging detection live; verification: detection fires on the cs-082 replay dataset in staging." |

### 3. Follow-through mechanism

- **Standing 30-minute forum**, monthly, same owner as the facilitator
  role: open items reviewed by exception (only overdue + new).
- **Aging rule:** any item open >60 days auto-escalates to the exec
  sponsor with a keep/kill decision recorded — killing is legitimate
  (conditions changed) but must be *decided*, not drifted.
- **Metric:** % of items closed by their date, reported in the SOC
  dashboard next to MTTD/MTTR — the review's health is measured like
  the incident's.

### 4. Compliance evidence

- The review doc itself: timeline, contributing factors, signed item
  list with owners/dates.
- The item tracker export showing closure with verification evidence
  (config exports, detection replay results).
- The aging-rule escalations (or their absence) — proof the process
  had teeth.

## Alternative Solutions

- **External facilitator** for high-stakes incidents: buys candor at
  cost/context; good practice for the first post-incident cycle.
- **Written async review** instead of meeting: scales better,
  weaker at negotiation; acceptable for low-severity incidents.

## Tradeoffs

- Strictness vs speed: contract-shaped items take longer to negotiate
  but close; vague items are instant and never close.
- Blameless vs accountability: accountability attaches to *system
  fixes*, not individuals — conflating them kills candor.

## Common Mistakes

- 14 items from one incident (cap at ~5 — prioritize by risk).
- "Review" as a done-state (unverifiable by definition).
- Blameless framing that never names the system gap.

## Instructor Prompts

- "What specifically in this design would have surfaced the disabled
  alert?"
- "Why cap action items — what does 14 items predict about closure?"
- "Who should own the follow-through forum, and why not the CISO?"

## Rubric (10 pts)

| Criterion | Pts |
|---|---|
| Format with inputs/agenda/roles producing owned items | 3 |
| Conversion rule + two applied examples | 3 |
| Follow-through mechanism with aging/escalation | 2 |
| Compliance evidence package defined | 2 |

## Safety Notes

- Simulated; no real-incident references.
