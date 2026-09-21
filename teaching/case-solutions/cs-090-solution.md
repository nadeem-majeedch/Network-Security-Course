---
case: cs-090
title: The Disclosure Decision (Solution)
difficulty: expert
module: 7
lecture-anchor: L27
clos: [CLO-14, CLO-15]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-090 — Solution: The Disclosure Decision

> **INSTRUCTOR ONLY.** Model solution for cs-090.

## Model Solution

### 1. The legal-clock reality

"Awareness" triggered the clock at day 0; the severity misjudgment
explains the delay but does not *erase* it — the regulator will
assess timeliness and accuracy as **separate axes**: a late-but-
accurate notice is still late. What is notified now, regardless of
forensic completeness: **the incident itself** (awareness, scope-so-
far, containment status, contact point). Investigation-in-progress
justifies *phasing*, not silence. Waiting 5 more days converts a
defensible-late notice into an indefensible-silent one.

### 2. Strategy: (b) immediate phased notice

| Strategy | Customers | Regulator | Board |
|---|---|---|---|
| (a) late-accurate | wait 12 days, then everything at once | late **and** perceived evasive | accuracy credit, timeliness penalty |
| **(b) phased now** | facts within 24 h, updates scheduled | timeliness restored (partially), accuracy preserved via updates | defensible on both axes |
| (c) wait 5 days | 14 days dark | worst case: both axes failed | indefensible |

Phasing costs: two comms cycles, some early statements revised. That
revision is *expected* under phased regimes when updates are
promised and delivered on schedule.

### 3. Day-9 phased notice skeleton

- **Fact:** unauthorized access to a support account between [dates];
  data in two storage locations confirmed accessed (ticket
  information, including ID documents for affected individuals).
- **Unknown, labeled as unknown:** three further locations *could*
  have been reached; forensic review is in progress; individuals
  affected by those locations will be contacted within [N] days if
  confirmed.
- **Action taken:** account disabled, access path closed, monitoring
  heightened (containment status).
- **Protection steps for customers:** specific, actionable (e.g.,
  document-number monitoring guidance as advised by counsel).
- **Commitment:** next update by [date + 5], and a standing contact
  channel.

### 4. Post-mortem control

The failure: severity triage misjudged a multi-day access to
customer PII as low. **Concrete control: a severity-escalation
recheck rule — any incident touching identity data or customer PII
auto-escalates for senior review within 4 hours, regardless of
initial triage score.** Add the review artifact: the day-0 triage
record + the 4-hour escalation log as standing compliance evidence.

## Alternative Solutions

- **(a) single accurate notice:** viable only if counsel judges the
  jurisdiction's regime tolerates it; the customer-trust and
  regulatory costs here dominate.
- **Notify only confirmed bucket 1–2 individuals now:** a middle
  path — but the unknown-bucket populations are *identifiable* from
  bucket membership, so phased updates can name them later; this is
  a legitimate variant of (b) with better targeting.

## Tradeoffs

- Accuracy vs timeliness: phasing pays tax on both axes but zeroes
  out neither — the alternative is paying full price on one.
- Completeness of the first notice vs speed of reassurance: customers
  forgive "we don't know yet, here's when you'll hear" far more than
  silence.

## Common Mistakes

- Treating "investigation ongoing" as a clock-stopper (it isn't —
  awareness is).
- Stating suspect buckets as confirmed (over-notice invites
  regulator scrutiny of *accuracy*).
- Stating them as ruled-out (under-notice breaks trust when
  forensics lands).
- Blaming the triage analyst in the review instead of fixing the
  escalation rule.

## Instructor Prompts

- "What exactly does 'awareness' mean here — the alert, or the day-3
  escalation?"
- "Which phrasing in the notice keeps the suspect buckets honest?"
- "If forensics later clears all 3 suspect buckets, was the phased
  notice wrong?"

## Rubric (10 pts)

| Criterion | Pts |
|---|---|
| Clock reasoning (awareness vs certainty) correct | 3 |
| Strategy chosen with three-way cost analysis | 2 |
| Notice skeleton: fact/unknown/commitment distinction clean | 3 |
| Post-mortem control concrete and reviewable | 2 |

## Safety Notes

- Simulated; principles-based — jurisdictions differ, counsel
  decides.
