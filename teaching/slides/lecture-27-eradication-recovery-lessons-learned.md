---
marp: true
theme: default
paginate: true
lecture: L27
week: 14
clos: [CLO-11]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# Eradication, Recovery & Lessons Learned

**Network Security · Lecture 27 · Week 14**

*The incident that "ends" badly ends again.*

<!-- notes: OPEN (2 min). Hook: "Announcing recovery isn't recovery.
Today: verification, clean restores, and reviews that change things." -->

---

## Learning Objectives

1. **Hunt** persistence: autostart, tasks, services, credential
  residue
2. **Apply** the safe restoration order (clean hosts ← clean data ←
  clean credentials)
3. **Run** a recovery go/no-go board with explicit criteria
4. **Reason** about backup generations during incidents
5. **Convert** reviews into owned, dated, verifiable changes

<!-- notes: (1 min) Objectives 2–4 are cs-084/c-085's design space;
objective 5 is cs-086's review case and the course's closing ethic. -->

---

## Persistence: Where They Hide

- Autostart: run keys, services, scheduled tasks
- Identity: new accounts, rogue GPOs, dumped credentials
- Trust: stolen tokens (cs-100's second token!), golden-ticket
  *capability* (concept, not recipe)

<!-- notes: (5 min) Conceptual persistence inventory per safety rules —
what to hunt, not how to forge. cs-085's AD-restore case is the deep
version. Quiz-5's containment slide pairs with this. -->

---

## The Safe Restoration Order

```
 1. eradication VERIFIED (persistence bounded)
 2. clean infrastructure (rebuilt/patched, new names if smart)
 3. clean data (pre-incident backup generations)
 4. clean credentials (rotated, reset, re-issued)
 5. clean access (MFA, egress still blocked)
```

- Any dirty layer re-taints the layers above it

<!-- notes: (6 min) The layering logic: trust flows along the rebuild
path (cs-085's answer). cs-084's restore-vs-rebuild debate applies it
to a file server. -->

---

## The Go/No-Go Recovery Board

- Criteria list (cs-084's): persistence bounded, entry closed, egress
  clean, backup generation verified, destination hardened, sign-off
  recorded
- The board *runs* — a named forum, not a feeling
- Overruled? Written risk acceptance: what's accepted, by whom, until
  when

<!-- notes: (6 min) The written-acceptance rule is the ethics of
pressure. cs-084's compromise schedule is the model. Quiz-5 Q8's
phased-notice logic is a cousin. -->

---

## Backup Generations: The Trap

- Backups *during* containment may be clean (server was isolated)
- Backups *before* detection are the canonical restore point
- Generation boundaries must be **documented** — "spot-check restored
  content" is the honest addendum

<!-- notes: (5 min) cs-084's §3 is the reasoning. Quiz-5's scenario
rewards exactly this nuance. -->

---

## AD Recovery: The Deep Version

- Compromised directory → rebuild path: clean management host →
  parallel DC build → 40-day clean restore → KRBTGT double-reset
  *after* clean infra exists
- Credentials from the dumped DB are burned material — reset before
  they touch the new domain

<!-- notes: (6 min) cs-085's sequence, compressed. The KRBTGT timing
("after clean infrastructure") is the case's signature insight —
quiz-level clarity for advanced students. -->

---

## Lessons Learned: Reviews That Change Things

- Blameless *in form*, accountable in output
- Inputs: timeline from logs, alert-config history, MTTR/MTTD, cost
- Output: ≤5 items, each **owner + date + observable done-state +
  verification**
- Aging rule: >60 days escalates to sponsor with keep/kill decided

<!-- notes: (6 min) cs-086's design is this slide's source. The
alert-config-history input is what surfaces the hidden disabled alert —
the blameless mechanics that actually work. Quiz-5/exam reporting
anchors here. -->

---

## CS/DS Example: Cluster Recovery Order

- Verify persistence bounded → rebuild nodes (rolling) → rotate
  cluster creds → re-validate lake tokens → heightened monitoring 14
  days

<!-- notes: (3 min) DS framing: rolling rebuilds preserve research
continuity — the same restoration-order logic, cluster-shaped. -->

---

## Activity: Build the Go/No-Go List (6 min)

For the cs-084 file-server restore: draft six go/no-go criteria; mark
the one that fails hardest if the persistence question is still open.

<!-- notes: (6 min) Expected: persistence-bounded is the failing
criterion — it gates everything. The activity rehearses the board
discipline. -->

---

## Case Study: cs-084 (5 min)

- RTO vs evidence vs re-infection — the recovery-speed triangle

<!-- notes: (5 min) If used, run cs-085 here per rotation. The
triangle's tension is the week's judgment peak. -->

---

## Formative Check

- Oral: name three go/no-go criteria; why does the KRBTGT reset wait?

<!-- notes: (2 min) Exit oral — both anchor the exam's scenario
section. -->

---

## References & Next

- NIST SP 800-61; vendor AD-recovery guidance (concept class)
- Diagrams: `diagrams/08-ir-lifecycle-workflow.md`
- **Next (L28):** SOC operations & threat hunting
