---
module: 8
lectures: [L29, L30, L31, L32]
status: complete
artifact-type: answer-key
instructor-only: true
distribution: never-publish-to-students
---

# Answer Key — Module 8: Network Forensics & Capstone

> **INSTRUCTOR ONLY — contains model answers to graded formative assessments.**
> Also serves as the **capstone assessment rubric anchor** for L31–L32.

## L29 — Forensic Fundamentals

### Formative checks (plan §11)
1. Evidence classes: volatile (memory, connections — dies on reboot), transient (logs — overwritten), persistent (disk, PCAP archives); volatile-first is the ordering rule *unless* acquisition scope says otherwise.
2. Chain of custody: who touched what, when, why, with what hash — every transfer logged; the lab's custody form is the artifact.
3. Acquisition integrity: imaging (bit-for-bit) vs copying (files); hashing (SHA-256) proves unchanged; *analysis on copies, never originals*.
4. Network-specific evidence: full PCAP, flow records, Zeek logs, DHCP/DNS logs, firewall/IDS alerts — each has a *lifetime* (what expires first: DHCP leases, log rotation); expiry drives urgency.
5. Timeline construction: clock-skew normalization (NTP offsets per source) before ordering events — uncorrected skew produces impossible narratives.

### Exit ticket
- "Why image instead of copy?" — imaging captures deleted/allocated-invisible data and preserves evidentiary integrity with hashes; file copy is analysis convenience, not evidence.
- Timestamp discipline: state the source clock and its skew per artifact; the answer "everything had the same time" is only true if you verified it.

### Lab troubleshooting (forensics lab context)
- Hash mismatch on re-verify: write-blocking absent or copy-vs-image confusion — re-acquire; never "fix" the hash.
- PCAP timestamps look wrong: capture host clock vs traffic clocks — normalize with the offset table before analysis.

## L30 — Advanced Forensics & Reporting

### Formative checks
1. Encrypted-traffic analysis (passive): metadata only — cadence, volume asymmetry, SNI/JA3-style fingerprints, certificate anomalies — *without* decryption; the line between metadata analytics and content inspection is the graded ethics line.
2. Attribution honesty: technical attribution yields *infrastructure and behavior clusters*, not legal identities — "we know it was the insider" overreach fails; the report language must match the evidence.
3. Report anatomy: executive summary (decisions needed), findings (evidence-linked), timeline, root cause, recommendations (prioritized), appendices (IOCs, hashes) — the exec summary must stand alone.
4. IOC hygiene: reproducible (exact hashes, IPs with context/expiry), scoped (what they mean, confidence), actionable (where they fit detection) — a raw list without context fails.
5. Testimony framing: answer what the evidence shows, state confidence and limits, never speculate beyond data — the mock-exercise rubric enforces this.

### Exit ticket
- Metadata vs content line: who/when/how-much/patterns = metadata analysis; what-was-said = content — passive encrypted-traffic analysis lives on the metadata side, and the report says so explicitly.
- Finding an IOC "matches": state the match *conditions* (field, timeframe, confidence) and the possibility of coincidence — bare assertions fail.

### Discussion facilitation
- Q4 (report goes further than evidence): the fix is editorial, not investigative — align every claim to an exhibit; reward students who identify the *specific* sentences that overreach.

## L31 — Capstone Workshop: IR Simulation

### Formative checks
This is the **capstone dry-run** — grade against the capstone rubric dimensions, not lecture quizzes:
1. **Evidence handling (25%):** custody form complete, images hashed, analysis on copies only, volatile-first where applicable.
2. **Analysis method (30%):** corroboration discipline (no single-source conclusions), timeline with skew normalization, scope stated with confidence bounds.
3. **Containment decisions (20%):** ladder order respected, visibility costs acknowledged, reversible-first.
4. **Communication (15%):** handoff notes timestamped and self-contained; exec-summary draft presentable in 90 seconds.
5. **Team process (10%):** roles used, decisions logged, escalations on time.

### Exit ticket
- The gap list each team writes is the *actual deliverable* — it becomes their L32 prep plan; teams with empty gap lists get the instructor's diagnostic questions, not a pass.
- Common dry-run failures (share in debrief): timeline built before clock normalization; containment actions undocumented; exec summary that narrates instead of deciding.

## L32 — Capstone Defense & Course Synthesis

### Capstone defense rubric (anchor for final assessment)
| Dimension | Weight | Distinction-level behavior |
|---|---|---|
| Technical accuracy | 30% | Protocol-level precision; no invented facts; limitations stated |
| Evidence discipline | 25% | Every claim linked to an exhibit; chain of custody intact; confidence stated |
| Judgment & trade-offs | 20% | Containment/prioritization decisions justified against alternatives and costs |
| Communication | 15% | Exec summary stands alone; analyst section reproducible by a peer |
| Course synthesis | 10% | Connects at least three modules' concepts in one coherent defense posture |

**Defense logistics:** 20-minute defense (12 present + 8 questions) + 5-minute panel deliberation per team; question bank drawn from all eight modules' misconception banks (this is where synthesis is probed).

### Formative checks
1. Question anticipation: strong teams pre-draft answers to the misconception-bank questions for their scenario — evidence of rehearsal is visible in defense quality.
2. Synthesis exercise: the one-page "defense posture" must show prevention → detection → response → recovery as a connected chain, with one named control per stage from *different* modules.
3. Career pathways: acceptable answers name a specialization (detection engineering, IR, network architecture, GRC) *and* the next concrete step (certification path, home lab, open-source contribution) — vague enthusiasm fails the check.

### Exit ticket
- The thread through all eight modules: **trust is a design decision** — every module relocated or hardened a trust boundary (L2 adjacency → perimeter → identity → workload → evidence); defenses that name their trust assumptions are the mature ones.
- The one-paragraph "what I'd tell a new analyst" — graded for evidence-based humility: what they'd verify first, what they'd refuse to conclude without corroboration.

### Case study anchors (cs-085–cs-100) — grading pointers
- **cs-085–cs-090 (L29/L30):** forensic writeups graded to the same exhibit-linking standard as the capstone — these cases are rehearsal, so apply the rubric early and say so.
- **cs-091–cs-100 (L31/L32):** teams' chosen capstone cases must map to tracker entries; scope changes need instructor sign-off recorded in the tracker notes column.

## Common misconceptions (module-level)
1. "Forensics = tools" — method and custody discipline decide admissibility and accuracy; tools are instruments (L29).
2. "Decryption is required for insight" — metadata analytics carry most network investigations; content access is a separate, gated step (L30).
3. "The capstone is a bigger assignment" — it's an integration assessment: every module's rubric dimensions appear in it (L31/L32).
4. "Attribution is the goal" — the goal is *decision-quality conclusions with stated confidence*; attribution ambitions beyond evidence produce false certainty (L30).
