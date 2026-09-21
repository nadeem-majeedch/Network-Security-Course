---
capstone: defense-guide
type: student-guide
weeks: [16]
duration: 25 min per team
status: complete
artifact-type: student-capstone
instructor-scoring: instructor/answer-keys/capstone-rubric-bands.md
---

# Oral Defense & Presentation Guide (Week 16)

> 25 minutes per team: **10 minutes presentation + 15 minutes questions.**
> Three panelists. This guide is the preparation standard (Self-Check
> Quiz 16 rehearses it).

## Presentation (10 minutes — strict)

Suggested split:
- **3 min** — the organization and its top three risks (not the diagram
  tour; the *pains* that shaped the design).
- **4 min** — architecture walk: zones, enforcement, telemetry; one
  control's verification evidence shown live (the strongest one).
- **2 min** — the incident exercise: what it caught, what it missed, the
  amendments.
- **1 min** — the board paragraph read aloud (yes, aloud — it tests your
  cs-094 discipline).

*Anti-patterns: 10 minutes of tool demos; reading the report; apologizing
for unfinished work instead of framing it as the deferral it is.*

## The five question archetypes (prepare all five)

1. **Dependency** — "X goes down Monday 9 a.m. What happens?" Have the
   break-glass/fallback answer with the named component.
2. **Adversarial** — "How does your design fail silently?" Name the drift
   mode *and* its reviewer cadence (who watches the watcher).
3. **Alternative** — "Why not just buy Y / do the simpler thing?" Answer
   with the tradeoff you evaluated, not product disdain.
4. **Scope** — "What did you deliberately not do?" The honest deferral:
   risk accepted + pairing control + who agreed.
5. **Evidence** — "What measured result backs this claim?" Every claim in
   the presentation must trace to your evidence pack; if it can't, don't
   say it.

## The weakness statement

Prepare to offer, unprompted, after the presentation:

> "The design's weakest point is [X]. We mitigated with [Y], tested by
> [Z]. If that mitigation fails, the fallback is [W], and we'd tell
> [stakeholder] that the posture temporarily changed."

Teams that name the weakness first convert the panel's best attack into
their credibility moment.

## Scoring (how the 15 minutes earns criterion-6 marks)

| Signal | Points effect |
|---|---|
| Evidence-chained answers (every claim → artifact) | +3 |
| Weakness statement offered unprompted with fallback | +2 |
| Survives an adversarial chain (names reviewer cadence) | +2 |
| Fallback positions pre-thought (cut/keep/never-cut) | +2 |
| Composed under the "fails silently" follow-up | +1 |
| Written-risk framing on live concessions | +1 |
| Deflection, unfamiliarity with own build, improvised certainty | −2 each |

## Logistics

- Panel: one network-architecture archetype, one SOC-lead archetype, one
  DS-faculty archetype (questions stress all three courses' angles).
- Scored independently, then reconciled (rubric bands).
- Your report must be submitted 48 h before the defense; panels read it
  first — the presentation is for *judgment*, not summary.
