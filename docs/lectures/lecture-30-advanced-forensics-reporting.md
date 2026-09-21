---
lecture: L30
title: Advanced Forensics & Reporting
module: 8
week: 15
hours: 2
clos: [CLO-14, CLO-15]
difficulty: expert
status: complete
artifact-type: student-lecture-material
instructor-plan: modules/module-08-forensics-capstone/lectures/lecture-30-advanced-forensics-reporting.md
---

# L30 — Advanced Forensics & Reporting

## 1. Learning Objectives

By the end of this session you can: (1) correlate heterogeneous evidence into a unified timeline and resolve apparent contradictions by *mechanism*; (2) enrich and structure IOCs with confidence scoring and sharing-eligibility review; (3) write a defensible findings report (exec summary, cited findings, limitations, control-mapped recommendations); (4) deliver a 5-minute executive briefing that survives hostile questions; (5) label confidence levels honestly in both forms.

## 2. Key Definitions

| Term | Definition |
|---|---|
| Correlation grid | Timeline anchors × evidence sources; filled cells cited, empty cells declared |
| Apparent contradiction | Sources disagree → hunt the *mechanism* that reconciles them (often evidence itself) |
| Confidence labeling | High (multiple independent corroborations) / moderate (single + mechanism-consistent) / low (hypothesis-grade) |
| Inference chain | evidence → observation → inference → conclusion, each link stating its basis |
| STIX-class IOC | Structured indicator: pattern + context + confidence + handling/sharing |
| TLP | Traffic Light Protocol — sharing-color governance for indicators |
| Executive summary | ≤1 page: impact-first, jargon-free, every line traceable to the report |
| Reproducibility | Queries included so the reader can re-run the analysis |

## 3. Detailed Explanations

### 3.1 Multi-source correlation method
Normalize first: one clock base (offset table recorded), one identity-resolution chain (DHCP + auth + 802.1X — L29), consistent host/user naming. Then the **correlation grid**: rows = timeline anchors; columns = pcap / flows / dns / proxy / auth; a filled cell is cited; an empty cell is a *declared gap*. **Apparent contradictions are opportunities:** the proxy log shows "normal browsing" during the beacon window — the mechanism (direct-IP egress bypassing the proxy) *strengthens* the finding (bypass behavior is itself evidence). When sources disagree, hunt the mechanism; document it.

### 3.2 Attribution and confidence discipline
The inference chain: evidence → observation → inference → conclusion, each link stating its basis. **Confidence vocabulary:** high = multiple independent corroborations; moderate = single source + mechanism-consistent; low = hypothesis-grade — labeled, never laundered into certainty. Technical attribution (infrastructure overlap, tooling/TTP signatures) is possible; actor-level attribution ("whodunit") is beyond network forensics alone — say so. This report feeds the L27 post-incident review: facts first, recommendations second.

### 3.3 The findings report (the graded artifact)
1. **Executive summary** — ≤1 page: what happened, impact, status, top recommendations.
2. **Findings** — numbered; each with evidence citations and confidence level.
3. **Timeline appendix** — the correlation grid.
4. **IOC appendix** — provenance + sharing eligibility.
5. **Limitations** — what the evidence cannot support (gaps, retention losses, contradictions and their resolutions).
6. **Recommendations** — each mapped to a control (which module's artifact?) with owner class.
Writing rules: every claim cites evidence; every number is reproducible (query listed); evidence-voice ("was observed" — no adjectives doing analysis: "2.1 GB over 3 nights", not "massive breach").

### 3.4 IOC enrichment and sharing
Enrichment: resolution history, WHOIS context, passive DNS, fingerprint clustering — each source cited; **enrichment ≠ proof**. STIX-class structure: pattern + context (first seen, confidence, related refs) + handling. The **sharing decision** passes two gates: legal/privacy review, then handling framework (TLP-class colors) — industry sharing contributes while protecting case confidentiality.

### 3.5 The executive briefing (5 minutes, graded)
Structure: **impact → what we know (confidence-labeled) → what we did → what we ask for → questions.** Craft: no jargon without translation; one number per claim; the "so what" sentence first; rehearse the three hardest questions. Defensibility: every slide line traces to the report's citations — the briefing is the report's shadow, not a separate truth.

## 4. Network Diagram: the correlation grid

```
 | Time (UTC) | Event          | pcap  | flow | dns | proxy | auth |
 |------------|----------------|-------|------|-----|-------|------|
 | 22:07:11   | first beacon   | f1044 | s8812| —   | —     | —    |
 | 22:40–23:10| "normal" browse| —     | —    | yes | yes   | —    |
 | 23:11      | HTTP upload 4.1MB | f2100 | s9043 | — | (gap) | —  |
 Contradiction: proxy silent during beacons
   → mechanism: direct-IP egress bypasses proxy → STRENGTHENS the finding
 Empty cell = declared gap, not silence.
```

## 5. Protocol Examples

- IOC record (STIX-class sketch): `domain cdn-updates[.]xyz | first_seen 2026-09-18T22:07Z (case-0117 f1044) | confidence high (pcap + flow + 2 hosts) | sharing: eligible after legal review | related: 198.51.100.77 (SNI), 15-min POST cadence (hunt H-A)`.
- Executive-summary sentence pair: ❌ "APT-style infrastructure was massively breached" → ✅ "2.1 GB left to one external host over three nights using credentials of a finance employee (high confidence)."

## 6. Configuration Concepts (concept level)

- Report template with mandatory sections (findings/limitations/recommendations).
- IOC register with confidence + TLP fields; sharing-gate checklist.
- Briefing pack: one slide per section, every line source-tagged.

## 7. Security Implications

- Correlation is honest bookkeeping: normalize, grid, cite, resolve contradictions by mechanism, declare gaps.
- The report is the deliverable — reproducible queries, labeled confidence, control-mapped recommendations.
- The briefing is the report's shadow: impact-first and defensible, never a separate truth.

## 8. Realistic Organizational Scenario

**The two contradictions (running case).** Three nights of evidence across four sources; two apparent conflicts: (1) the proxy-bypass pattern from class; (2) the auth log shows the user *logged off* 20 minutes before the second-night exfil — mechanism: **service-account credential reuse**, not the human user. You produce the unified grid, resolve both by mechanism, restate identity claims with corrected confidence, and write the limitation that matters most: the case supports *credential compromise*, not insider action. Full case: **cs-097**; the report workshop drafts the graded Lab-15 part 2.

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "Longer reports are better" | Cited, reproducible, and readable beats long. |
| "Correlation = causation" | The grid shows co-occurrence; mechanisms make causes. |
| "Contradictions weaken findings" | Resolved contradictions often *strengthen* them (bypass is evidence). |
| "Executives need the technical appendix" | They need impact, confidence, and asks — the appendix is for engineers. |
| "The report is the end of the case" | It feeds the L27 review, the L31 capstone, and future hunts (L28). |

## 10. Classroom Activities

1. **Report workshop (pairs):** full findings report — exec summary, 5 cited findings, grid appendix, IOC appendix, limitations (must include the proxy-contradiction resolution), 3 control-mapped recommendations.
2. **Exemplar critique:** deidentified exemplar report → find its three weaknesses.
3. **Hostile-question rehearsal:** instructor asks the three hardest questions; pairs answer with citations.

## 11. Problem-Solving Questions

1. Why does the *mechanism* (proxy bypass) upgrade the finding rather than weaken it?
2. Your timeline has one anchor supported only by a DHCP log: label its confidence and state what would upgrade it.
3. Which belongs in the exec summary: "APT-class infrastructure overlap" or "2.1 GB over three nights using a finance employee's credentials"? Defend with audience analysis.
4. When does an IOC become shareable? Name the two gates and what each checks.
5. What makes a recommendation "control-mapped"? Give one from this course's own modules.

## 12. Exit Ticket

1. What five sections must the findings report contain?
2. Rewrite in evidence-voice: "Hackers massively exfiltrated tons of data."
3. What confidence label does a single-source, mechanism-consistent finding get?
4. What two things does the correlation grid make visible at a glance?
5. Name the two gates an IOC passes before external sharing.

*(Answers: `teaching/answer-keys/answer-key-module-08.md`.)*

## 13. References

- NIST SP 800-86 — reporting guidance; NIST SP 800-61 — metrics alignment.
- OASIS STIX 2.1 specification; FIRST Traffic Light Protocol (TLP).
- Casey, *Digital Evidence and Computer Crime* — admissibility chapters.
- Course-internal formats: L25 custody template, L26 timeline, L28 hunt log — the house style this report extends.

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-14 | §3 correlation + report method | Lab-15 (W15), Final practical, Capstone |
| CLO-15 | §3.3/3.5 report + briefing craft | Capstone report/defense (L31–L32) |
