---
lecture: L30
title: Advanced Forensics & Reporting
module: 8
week: 15
hours: 2
clos: [CLO-14, CLO-15]
difficulty: expert
status: complete
artifact-type: teaching-plan
---

# L30 — Advanced Forensics & Reporting

## 1. Overview & Prerequisites

- **Prerequisites:** L29 (custody, single-case timeline, IOC extraction). L26–L28 (incident documentation and hunt logs — this report synthesizes those formats).
- **Position:** the capstone's reporting standard is set here. Students write the full findings report (graded draft — Lab-15 part 2), then defend versions of it in L31–L32. CLO-15 (communication) is formally assessed for the first time.
- **Faculty prep:** extend the L29 case with one additional evidence source (proxy logs with a contradicting-looking entry — the "apparent contradiction" teaching moment); prepare the report rubric and a deidentified exemplar report.
- **Common misconceptions:** "longer reports are better"; "correlation = causation"; "the report is the end of the case"; "executives need the technical appendix."

## 2. Learning Objectives

By the end of this lecture, students can:

1. Correlate heterogeneous evidence (pcap + flow + logs + identity) into a unified timeline, resolving apparent contradictions explicitly (Analyze/Create).
2. Enrich and structure IOCs: STIX-class representation, confidence scoring, and sharing-eligibility review (Apply/Evaluate).
3. Write a defensible findings report: executive summary, technical findings with evidence citations, limitations, and recommendations mapped to controls (Create).
4. Present findings to an executive audience: the 5-minute briefing — impact-first, jargon-free, defensible under questioning (Create).
5. Distinguish and document confidence levels and inference chains in both report forms (Evaluate).

## 3. Detailed Concepts

### 3.1 Multi-source correlation method
- Source normalization: one clock base (offset table), one identity resolution chain (DHCP + auth + 802.1X — L29), one naming scheme for hosts/users.
- The correlation grid: rows = timeline anchors; columns = evidence sources; a cell filled = cited; empty = declared gap (never silently blank).
- **Apparent contradictions** (today's teaching centerpiece): proxy log shows the host "browsing normally" during the beacon window — resolution: proxy bypass for direct-IP traffic; the contradiction *strengthens* the finding (bypass behavior is itself evidence). Method: when sources disagree, hunt the mechanism that reconciles them; document it.

### 3.2 Attribution and confidence discipline
- The inference chain: evidence → observation → inference → conclusion; each link states its basis. Confidence vocabulary: (high) multiple corroborating independent sources; (moderate) single-source + mechanism-consistent; (low) hypothesis-grade — labeled, never laundered into certainty.
- Technical attribution vs actor attribution: infrastructure overlap, tooling signatures (TTPs), timing patterns — with the honesty that takedown-level attribution is beyond network forensics alone.
- The L27 connection: the findings report feeds the IR post-incident review; facts first, recommendations second.

### 3.3 The findings report (graded artifact)
- Structure: (1) Executive summary — ≤ 1 page: what happened, impact, status, top recommendations; (2) Findings — numbered, each with evidence citations and confidence level; (3) Timeline appendix — the correlation grid; (4) IOC appendix — with provenance + sharing-eligibility; (5) Limitations — what the evidence cannot support (gaps, retention losses, contradictions and their resolutions); (6) Recommendations — each mapped to a control (L09–L24 artifacts) with owner class.
- Writing rules: every claim cites evidence; every number is reproducible (query listed); tense discipline (evidence says "was observed"); no adjectives doing analysis ("massive breach" vs "2.1 GB to one external host across 3 nights").
- Reproducibility: analysis queries included (the reader can re-run them) — the habit from L29's provenance lines, formalized.

### 3.4 IOC enrichment and sharing
- Enrichment: resolution history, WHOIS/registration context, passive DNS, fingerprint clustering — each enrichment source cited; enrichment ≠ proof.
- STIX-class structure: pattern (domain/IP/hash), context (first seen, confidence, related campaign refs), handling (sharing eligibility per L25 governance).
- Sharing decision: legal/privacy review gate; industry sharing contributes while protecting case confidentiality — the ethics-policy tie.

### 3.5 The executive briefing (5 minutes, graded)
- Structure: impact → what we know (confidence-labeled) → what we did → what we ask for (decisions/resources) → questions.
- Craft rules: no jargon without translation, one number per claim, the "so what" sentence first, anticipated-questions prep (the three hardest questions rehearsed).
- Defensibility: every slide line traces to the report's citations — the briefing is the report's shadow, not a separate truth.

## 4. Teaching Sequence (120 Minutes)

| Time | Segment | Instructor moves |
|---|---|---|
| 0–10 | Recap: L29 worksheets | One timeline row reviewed; introduce the contradiction source pack |
| 10–35 | Core: correlation method | Build the correlation grid live; resolve the proxy contradiction as a class |
| 35–55 | Core: report anatomy | Rubric walk; deidentified exemplar critique (find its 3 weaknesses) |
| 55–65 | Break | — |
| 65–90 | Core: IOC enrichment + briefing craft | STIX-class example; the 5-minute structure; one live "hostile question" demo |
| 90–110 | Student activity: report workshop | Pairs draft the full findings report (Lab-15 part 2; cs-094..097 prep) |
| 110–120 | Wrap + formative | Exit ticket; L31 briefing: bring the report — design reviews + IR simulation next |

## 5. Technical Examples

```
# Correlation grid (excerpt from the class case)
# | Time (UTC)      | Event                  | pcap   | flow  | dns  | proxy | auth |
# |-----------------|------------------------|--------|-------|------|-------|------|
# | 22:07:11        | first beacon           | f1044  | s8812 | —    | —     | —    |
# | 22:40–23:10     | "normal" browsing      | —      | —     | yes  | yes   | —    |
# | 23:11           | HTTP upload 4.1MB      | f2100  | s9043 | —    | (gap) | —    |
# | contradiction   | proxy silent during beacon     → mechanism: direct-IP egress
#                    (flow s8812 is NOT via proxy) → strengthens bypass finding.

# IOC record (STIX-class sketch, case-cited):
#   domain: cdn-updates[.]xyz | first_seen: 2026-09-18T22:07Z (case-0117 f1044)
#   confidence: high (pcap + flow + 2 hosts) | sharing: eligible after legal review
#   related: 198.51.100.77 (TLS SNI match), POST cadence 15min (hunt H-A)
```
Expected teaching points: the grid makes gaps *visible* (and honest); contradictions resolved by mechanism-hunting become evidence; the IOC record is case-cited or it doesn't exist.

## 6. Discussion Questions

1. The proxy contradiction: why does the *mechanism* (proxy bypass) upgrade the finding rather than weaken it?
2. Your timeline has one anchor supported only by a DHCP log. Label its confidence and justify what you'd need to upgrade it.
3. Which belongs in the executive summary: "APT28-style infrastructure overlap" or "2.1 GB to one external host over 3 nights, using credentials of a finance employee"? Defend with audience analysis.
4. When does an IOC become shareable? Name the two gates and what each checks.
5. What makes a recommendation "mapped to a control"? Give one from this course's own modules.

## 7. Student Activity

**Report workshop (20 min block within lab window, pairs):** complete the findings report for the L29/L30 case: executive summary, 5 numbered findings with citations + confidence, correlation-grid appendix, IOC appendix, limitations section (must include the proxy contradiction resolution), and 3 control-mapped recommendations. Deliverable = Lab-15 part 2; the best report's executive summary becomes the L31 briefing exemplar.

## 8. Problem-Solving Case

**Primary case — cs-097 "Multi-source timeline correlation" (expert):**
Case extension: three nights of evidence, four sources (pcap partial, flows complete, proxy, auth), two apparent contradictions: (1) the proxy-bypass pattern from class, (2) an auth log showing the user *logged off* 20 minutes before the second-night exfil — resolution: service-account reuse (credential-material theft, not the human user). Students must produce the unified correlation grid, resolve both contradictions by mechanism, restate the identity claims with corrected confidence, and write the limitation that matters most: the case supports credential compromise, not insider action.
**Linked cases:** cs-094 (IOC extraction/enrichment), cs-095 (findings report drafting), cs-096 (legal-hold scenario).
*(Model solutions: instructor answer-key set, Module 8.)*

## 9. Formative Assessment

1. What five sections must the findings report contain?
2. Write one sentence: evidence-voice (no adjectives doing analysis).
3. What is the confidence level of a finding supported by one source with a plausible mechanism — and how is it labeled in the report?
4. What two things does the correlation grid make visible at a glance?
5. Name the two gates an IOC passes before external sharing.
*(Answer key: instructor set, Module 8.)*

## 10. Summary & Key Takeaways

- Correlation is honest bookkeeping: normalize, grid, cite, resolve contradictions by mechanism, declare gaps.
- The report is the deliverable: reproducible queries, labeled confidence, control-mapped recommendations.
- The briefing is the report's shadow — impact-first, defensible, rehearsed against hostile questions.

## 11. References

- NIST SP 800-86 — reporting guidance; NIST SP 800-61 — metrics alignment (MTTD/MTTR).
- OASIS — STIX 2.1 specification (IOC structure); FIRST — traffic-light-protocol (TLP) sharing framework.
- Casey — *Digital Evidence and Computer Crime* — report/legal admissibility chapters.
- Course-internal: L25 custody template, L26 timeline format, L28 hunt-log format (the house style this report extends).

## 12. CLO Mapping

| CLO | Where in this lecture | Assessed via |
|---|---|---|
| CLO-14 | §3.1–3.3 correlation + report method; workshop §7 | Lab-15 (W15), Final practical, Capstone |
| CLO-15 | §3.3/§3.5 report + briefing craft | Capstone report/defense (L31–L32), Assignment 6 (feedback loop) |
