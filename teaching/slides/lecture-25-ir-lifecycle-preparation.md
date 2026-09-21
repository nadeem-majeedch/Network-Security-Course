---
marp: true
theme: default
paginate: true
lecture: L25
week: 13
clos: [CLO-11]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# IR Lifecycle & Preparation

**Network Security · Lecture 25 · Week 13**

*Preparation is the only phase you control before it hurts.*

<!-- notes: OPEN (2 min). Hook: "Module 7's register shift: less
protocol, more judgment. Today: the system that makes judgment
repeatable." -->

---

## Learning Objectives

1. **Walk** the NIST IR lifecycle with its phase purposes
2. **Design** runbook preconditions from failure modes (the clinic
  method)
3. **Build** an escalation tree with criteria-based triggers
4. **Define** the authority matrix: who may contain what, when
5. **Evaluate** readiness with exercises, not documents

![bg right:34% fit](diagrams/08-ir-lifecycle-workflow.md)

<!-- notes: (1 min) Diagram 08 taught fully today — phases + the
reversibility loop. Objectives 2–4 are assignment-6's tasks. -->

---

## NIST Lifecycle: Four Phases

| Phase | Purpose | Course artifact |
|---|---|---|
| Preparation | be ready before | runbooks, authority, drills |
| Detection & Analysis | confirm + scope | MTTD clock starts |
| Containment/Eradication/Recovery | act + restore | reversibility rules |
| Post-Incident | learn + change | owned, dated actions |

- The loop closes: post-incident *changes preparation*

<!-- notes: (6 min) Diagram 08's phases with the course artifacts
named. Quiz-5 Q1's phase question; cs-080's team-design case sits
here. -->

---

## Runbooks: Pre-Deciding Under Calm

- A runbook = decisions pre-made: **condition set → action →
  reversibility class**
- Not narrations of theory — *decisions* (assignment-6's core rule)
- Failure modes → preconditions: "if we couldn't see flows, we couldn't
  scope — so scope needs flow retention"

<!-- notes: (6 min) The design-thinking clinic: build preconditions
from failure modes. cs-082/cs-100 patterns become runbook conditions.
Assignment-6's decision-points task rehearses exactly this. -->

---

## Escalation: Criteria, Not Names

- Analyst → SOC lead → CISO → legal — each hop has a *trigger
  criterion* (severity, data class, regulatory clock)
- The two loss-prone hops (quiz-12 Q7): triage-confidence and the
  regulatory-clock call
- Pre-approved holding statements live at the comms hop

<!-- notes: (5 min) The criteria-not-names rule survives personnel
churn. cs-099's injects test exactly the two named hops. -->

---

## The Authority Matrix

- Who may isolate a server? Disable an account? At 2 a.m.?
- Standing delegation: on-call authority for reversible actions;
  irreversible needs escalation
- cs-083's 2 a.m. DC case is the judgment boundary drill

<!-- notes: (5 min) The matrix is the exercise finding (cs-095's first
expected gap). Quiz-5 Q6's containment ordering assumes authority
exists. -->

---

## Exercises: Documents Lie, Drills Don't

- Tabletop → operational drill → full inject exercise (cs-095's design)
- Conditional injects convert rehearsal into *test*
- Every drill produces owned, dated amendments (cs-086's rule)

<!-- notes: (5 min) The course's own cs-095 design is the reference
exercise. Quiz-5's scenario section reads from this discipline. -->

---

## CS/DS Example: IR for the Cluster

- Runbook: cryptomining pattern → isolate node, rotate cluster
  credential, audit lake tokens (cs-088's sequence)
- Authority: cluster ops may isolate nodes; lake-token rotation needs
  platform + security joint call

<!-- notes: (3 min) DS framing: the cluster runbook is assignment-6's
option (a) sibling — students can write it for their own lab. -->

---

## Activity: Runbook Precondition Clinic (7 min)

For the ransomware-staging runbook: list three failure modes (telemetry,
authority, comms) and the precondition each implies.

<!-- notes: (7 min) The clinic method from cs-095's design. Expected:
flow retention → scoping; standing delegation → 2 a.m. isolation;
holding statement → exec pressure. Assignment-6's skeleton. -->

---

## Case Study: cs-079 (5 min)

- Ransomware playbook gap analysis — find the missing preconditions

<!-- notes: (5 min) Classroom protocol; cs-080 (team/escalation design)
is the alternate slot. -->

---

## Formative Check

- Oral: name the four phases and the artifact each produces.

<!-- notes: (2 min) Exit oral — the artifact-per-phase mapping is the
takeaway. -->

---

## References & Next

- NIST SP 800-61 (IR guidance)
- Diagrams: `diagrams/08-ir-lifecycle-workflow.md`
- **Next (L26):** detection, triage & containment — the clock runs
