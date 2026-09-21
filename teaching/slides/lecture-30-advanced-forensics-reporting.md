---
marp: true
theme: default
paginate: true
lecture: L30
week: 15
clos: [CLO-14, CLO-15]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# Advanced Forensics & Reporting

**Network Security · Lecture 30 · Week 15**

*From evidence to defensible findings — the analyst as author.*

<!-- notes: OPEN (2 min). Hook: "L29 handled evidence. Today: writing
the report that survives lawyers, auditors, and Monday morning." -->

---

## Learning Objectives

1. **Correlate** multi-source telemetry with derived clock skews
2. **Quantify** volume reconciliation across sources (and state the
  deltas honestly)
3. **Explain** what only packet data proves (vs flows and logs)
4. **Structure** the forensic report for three audiences
5. **Present** findings with confidence labels and stated boundaries

![bg right:34% fit](diagrams/10-forensic-timeline-sources.md)

<!-- notes: (1 min) cs-097 is today's spine — the multi-source case.
Objectives 3–4 are the report-craft core; the final's P2–P4 grades
them. -->

---

## Multi-Source Correlation: The Full Method

- Derive each source's clock skew from a **common event**
- Normalize the timeline; keep per-source precision (flows = buckets,
  PCAP = seconds)
- Merge with source tags — no unification into false certainty

<!-- notes: (6 min) cs-097's derivations: +3:30 router, −40 s sensor,
from the 15:45 common peak. The "per-source precision" rule prevents
the smooth-but-false timeline. Quiz/exam: QB-048, final P2. -->

---

## Volume Reconciliation: The Honest Ledger

| Metric | Host | Flow | PCAP |
|---|---|---|---|
| Peak window | 800 MB | 810 MB (wire + TLS) | 640 MB (30-min capture) |
| Total | 2.1 GB | ≥1.4 GB observed | — |

- Differences are *window math and overhead*, not contradictions
- The unobserved delta is **stated** (~0.7 GB, host-attributed only)

<!-- notes: (6 min) cs-097's reconciliation table. The stated-delta
discipline is what separates analyst reports from dashboard exports.
Final-P2's marking rubric mirrors this. -->

---

## What Only Packets Prove

1. **Protocol shape** — one long TLS session vs many short (automated
  export vs beaconing)
2. **Content pattern** — bulk transfer rhythm vs interactive
3. **Session boundaries** — start/stop to the second, one destination

- Flows corroborate; PCAP demonstrates

<!-- notes: (5 min) The three PCAP-only proofs from cs-097. The
"defense will ask" framing: flow buckets can't show session
boundaries — PCAP can. -->

---

## The Report's Three Audiences

| Audience | Needs | Form |
|---|---|---|
| Executive | risk + action | board paragraph (cs-094 shape) |
| Legal/regulator | provenance + confidence | sourced findings, labeled unknowns |
| Technical peer | reproducibility | methods, queries, hashes |

- One report, three sections — or three documents that agree

<!-- notes: (5 min) The audiences disagree about *detail*, never about
*facts* — consistency across audiences is the integrity test. cs-090's
phased notice is the legal register. -->

---

## Findings That Survive Cross-Examination

- Every clause: source + confidence + boundary
- Unknowns stated as unknowns (the agent-blind window)
- No smooth claims: "network-attributed, host-unattributed"
- Methods reproducible: queries and hashes in the appendix

<!-- notes: (5 min) cs-097's model paragraph read aloud again, clause
by clause. The final's P4 grading rubric: provenance (2), confidence
(2), one explicit unknown (2). -->

---

## IOC Extraction & Enrichment (Workflow, Not War Stories)

- From evidence: hashes, domains, IPs, cert serials — *labeled by
  confidence*
- Enrichment: passive sources first (WHOIS, CT logs, passive DNS)
- Dissemination: internal blocklists + TI sharing — with the same
  confidence labels

<!-- notes: (4 min) cs-094's workflow case in lecture form. The
"labeled by confidence" carry-over keeps IOC quality honest (L28's
provenance discipline). -->

---

## Legal-Hold & Integrity Operations

- Legal hold: suspend routine deletion for identified evidence stores
- Integrity: hashes + WORM storage + access logs = the custody spine
- Coordinate counsel *before* deletion routines eat the evidence

<!-- notes: (4 min) cs-096's legal-hold case in lecture form. The
"before deletion routines" line is the operational urgency. -->

---

## CS/DS Example: The Report as an Analysis Artifact

- The forensic report is a *reproducible analysis*: methods + data +
  confidence = notebook discipline with legal stakes
- Same standards DS students already know: provenance, validation,
  versioning

<!-- notes: (3 min) DS framing: the report IS a data product — the
parallel makes the standard portable for DS students. -->

---

## Activity: Write the Finding (7 min)

Given the cs-097 evidence tables: draft the 100-word legal-ready
finding. Every clause sourced; one unknown stated.

<!-- notes: (7 min incl. peer swap) Peer-review against the three
tests: every clause sourced? confidence labeled? one unknown? The
final's P4 rehearses exactly this under exam pressure. -->

---

## Case Study: cs-097 (5 min)

- The full multi-source case — correlation, reconciliation, reporting

<!-- notes: (5 min) If used in teaching slots, run cs-093
(flow-corroboration) or cs-095 (defensible report) per rotation. -->

---

## Formative Check

- Oral: the three PCAP-only proofs; the report's three audiences.

<!-- notes: (2 min) Exit oral — both anchor the final's Part II. -->

---

## References & Next

- cs-097/cs-092 case files (worked instances)
- Diagrams: `diagrams/10-forensic-timeline-sources.md`
- **Next (L31):** capstone workshop & IR simulation — you run it
