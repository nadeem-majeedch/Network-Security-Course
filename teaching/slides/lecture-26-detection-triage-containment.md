---
marp: true
theme: default
paginate: true
lecture: L26
week: 13
clos: [CLO-11, CLO-12]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# Detection, Triage & Containment

**Network Security · Lecture 26 · Week 13**

*The first hour writes the whole story.*

<!-- notes: OPEN (2 min). Hook: "Every alert triaged today is someone's
tomorrow — the alert-burden wall is real." -->

---

## Learning Objectives

1. **Triage** an alert with three-way corroboration (IDS ↔ Zeek ↔
  flow)
2. **Locate** the attacker's *current* position, not just their history
3. **Sequence** containment by reversibility class
4. **Decide** kill-vs-observe with explicit deciding evidence
5. **Brief** leadership in triage-ready facts + labeled unknowns

![bg right:34% fit](diagrams/08-ir-lifecycle-workflow.md)

<!-- notes: (1 min) Objectives 3–4 are the module's judgment core
(cs-081–083 cases); objective 5 is cs-099's inject discipline. -->

---

## Triage: Corroborate Before You Contain

- The alert says *something*; corroboration says *what and where*
- IDS alert ↔ Zeek behavior ↔ flow volume/timing — three-way minimum
- Single-source + error asymmetry = the cs-082 exception (act anyway,
  *stated*)

<!-- notes: (6 min) The rule and its exception, both honest. Quiz-5
Q3's confidence-labeling + cs-087's timeline discipline root here. The
"stated" matters: the asymmetry argument must be explicit. -->

---

## "Where Are They Now?" Beats "What Did They Do?"

- History informs; *current position* targets containment
- Live session? Active tooling? Persistence? — each changes the order
- cs-081's phishing case: the live VPN session is the first target

<!-- notes: (5 min) The reorientation slide: containment aims at the
present tense. The three status checks (session/tooling/persistence)
are the drill. -->

---

## Containment: Reversible Before Irreversible

| Order | Action | Class |
|---|---|---|
| 1 | EDR isolate host | reversible |
| 2 | Block domains/IPs | reversible |
| 3 | Suspend tasks (not delete) | reversible + evidence |
| 4 | Rotate credentials | semi (user cost) |
| 5 | Rebuild/restore | irreversible — last |

- Evidence note: suspend ≠ delete; isolate ≠ wipe

<!-- notes: (7 min) THE slide of module 7. Quiz-5 Q6 is its exam form;
diagram 08's loop is its picture. The credential row: blast radius =
credential, not host (cs-088's principle). -->

---

## Kill vs Observe: The Judgment Call

- Kill: attacker mid-operation, persistence found → cap the damage
- Observe: host clean, scope unknown → buy intel, watch exits
- The flip condition: *state what evidence flips your answer* (cs-081's
  rule)

<!-- notes: (6 min) cs-081's judgment case: dump alert flips it to
kill. "State the flip condition" is the discipline that makes judgment
defensible — cs-099 scores it. -->

---

## The Executive Brief

- Three sentences: what happened, what you did, what you need
- Facts + labeled unknowns; never invented certainty
- The pre-approved holding statement (assignment-6's comms task)

<!-- notes: (5 min) cs-099's inject-3 line: "I won't guess" ages
best. cs-090's phased-notice logic previews the legal frame. -->

---

## Case Chain: The Module's Judgment Arc

- cs-081: first-hour triage (corroborate, sequence, brief)
- cs-082: pre-encryption ransomware (asymmetry, act)
- cs-083: the 2 a.m. domain controller (partial containment)
- cs-099: the exercise — decisions on the clock

<!-- notes: (4 min) The arc map: each case adds one judgment layer.
Students should know which skill each case drills. -->

---

## CS/DS Example: Containing the Cluster

- Node isolation: scheduler drain first (research continuity),
  containment second — the *order* is the judgment
- Credential rotation beats node rebuild (cs-088's answer, again)

<!-- notes: (3 min) DS framing: containment in research estates has a
mission-continuity tax — sequencing it is the skill. -->

---

## Activity: Sequence the Containment (6 min)

Inject: staging egress + task creation on FS-mirror + svc_ops login on
DB-mirror. Sequence five actions with reversibility labels.

<!-- notes: (6 min) cs-099's compressed drill. Expected order:
isolate FS, block domains, disable svc_ops estate-wide, suspend tasks,
(evidence) — rebuild stays last. -->

---

## Case Study: cs-081 (5 min)

- The phishing first-hour — corroboration, sequence, legal brief

<!-- notes: (5 min) If used, run cs-082 here instead per rotation. The
first-hour discipline is the week's assessment centerpiece. -->

---

## Formative Check

- Oral: why suspend-not-delete? What evidence flips kill→observe?

<!-- notes: (2 min) Exit oral — both are quiz/exam anchors. -->

---

## References & Next

- NIST SP 800-61; SANS IR handbook (method references)
- Diagrams: `diagrams/08-ir-lifecycle-workflow.md`
- **Next (L27):** eradication, recovery & lessons learned
