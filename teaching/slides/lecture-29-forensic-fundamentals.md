---
marp: true
theme: default
paginate: true
lecture: L29
week: 15
clos: [CLO-14]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# Forensic Fundamentals

**Network Security · Lecture 29 · Week 15**

*Evidence: the difference between "we think" and "we can prove."*

<!-- notes: OPEN (2 min). Hook: "Module 8: everything you've collected
becomes something you can defend in front of lawyers." -->

---

## Learning Objectives

1. **Apply** evidence-handling discipline: hash, copy, custody, record
2. **Build** timelines from logs/flows/PCAP with confidence labels
3. **Reason** about clock skew as *derivable*, not assumed
4. **Distinguish** network-attributed vs host-attributed claims
5. **Draft** a defensible finding paragraph

![bg right:34% fit](diagrams/10-forensic-timeline-sources.md)

<!-- notes: (1 min) Diagram 10 taught fully today. Objective 5 is the
final exam's P4 task; objective 3 is cs-097's signature skill. -->

---

## Evidence Handling: The Non-Negotiables

1. Hash originals **before** analysis (`sha256sum` against
  distribution)
2. Work on copies; originals read-only
3. Custody transfers documented (who, when, why)
4. Notes are evidence: timestamped, contemporaneous

<!-- notes: (6 min) The final exam's P1 grades exactly these four.
cs-091's chain-of-custody planning case is the design version. The
course's lab-labeling standard is the same discipline at smaller
stakes. -->

---

## Timeline Construction

- Every entry: event + timestamp basis + **source** + confidence
- Source ladder: 1 = supported, 2 = corroborated, 3+ = corroborated
  with redundancy
- Precision per source: flows can't claim seconds; PCAP can

<!-- notes: (6 min) Diagram 10's correlation discipline. cs-087's
five-source case is the worked instance; cs-097 adds the clock-skew
derivation. Quiz-5 Q4's labeling question reads this. -->

---

## Clock Skew: Derive, Then Normalize

- Find an event visible in **two** sources → measure the offset
- One event pair = hypothesis; two+ pairs = derivation
- Report normalizes but *discloses* the offsets

<!-- notes: (5 min) cs-097's signature move (+3:30 router, −40 s
sensor, derived from the common peak event). QB-048's question is this
slide's exam form. -->

---

## Network- vs Host-Attributed

- Network telemetry: flows/PCAP — what traversed, when, how much
- Host telemetry: what process, what user, what file
- The honest compound: **"network-attributed, host-unattributed"**
  (agent-off windows)

<!-- notes: (5 min) The phrase survives cross-examination *because* it
states the boundary. cs-087's agent-stop window is the worked case;
cs-100's board paragraph leans on it. -->

---

## Reporting: Provenance + Confidence + Unknowns

```
 "Between 13:00–18:05, svc_analytics exported 2.1 GB (±5%,
  host-measured) to one external IP [host+flow+PCAP: corroborated].
  Activity 17:30–18:05 (590 MB) is network-attributed, host-
  unattributed [supported]. ~0.7 GB predates the capture window
  [host-attributed only]."
```

- Every clause: source + confidence + boundary
- Unknowns stated as unknowns — that's what survives review

<!-- notes: (6 min) The model paragraph is cs-097's legal-ready
finding. The final's P4 grades this form. Read it aloud slowly — it's
the course's writing standard. -->

---

## CS/DS Example: Provenance for Analytics

- DS pipelines keep provenance for *reproducibility*; forensics keeps
  provenance for *defensibility* — same discipline, different stakes
- The lake's access logs = the evidence store (assignment-7's triad)

<!-- notes: (3 min) DS framing: data lineage and chain of custody are
the same mental muscle — say it explicitly, DS students hear it. -->

---

## Activity: Label the Entries (6 min)

Five timeline entries given: label each source set + confidence;
rewrite the two over-claimed ones honestly.

<!-- notes: (6 min) The over-claim rewrites are the exercise's point:
"corroborated" needs two sources; "no earlier access" needs retention
to cover it. cs-087's rubric discipline. -->

---

## Case Study: cs-091 (5 min)

- Evidence and chain-of-custody planning — design before the incident

<!-- notes: (5 min) If used, run cs-092 (pcap timeline) here per
rotation. -->

---

## Formative Check

- Oral: the four evidence-handling steps; why one event pair isn't
  enough for skew derivation.

<!-- notes: (2 min) Exit oral — P1's checklist + the derivation
standard. -->

---

## References & Next

- NIST SP 800-86 (forensic integration guidance)
- Diagrams: `diagrams/10-forensic-timeline-sources.md`
- **Next (L30):** advanced forensics & reporting
