---
lecture: L29
title: Forensic Fundamentals
module: 8
week: 15
hours: 2
clos: [CLO-14]
difficulty: expert
status: complete
artifact-type: teaching-plan
---

# L29 — Forensic Fundamentals

## 1. Overview & Prerequisites

- **Prerequisites:** L21 (telemetry tiers — forensic data sources), L26 (timeline/scoping discipline — now formalized as forensics), L25 (chain-of-custody basics — now graded).
- **Position:** Module 8 converts investigation skills into defensible forensic practice. The pcap/netflow timeline lab is Lab-15 part 1; L30 adds correlation and reporting. CLO-14 runs L29→L32 (Final practical + capstone).
- **Faculty prep:** prepare the case evidence pack (staged pcap slice + flow records + DHCP/DNS log excerpts for one incident), evidence-request forms, and hash tooling on lab images.
- **Common misconceptions:** "forensics = installing a GUI tool"; "IP address = attacker identity"; "the pcap proves intent"; "chain of custody is paperwork for court only."

## 2. Learning Objectives

By the end of this lecture, students can:

1. Classify network forensic evidence types (pcap, flow, logs, device configs, ARP/CAM state) by volatility, fidelity, and acquisition method (Analyze).
2. Apply chain-of-custody discipline to a digital acquisition: acquisition log, hashing, storage, transfer signatures (Apply).
3. Reconstruct a session timeline from pcap and flow records: conversation inventory, session boundaries, byte/timing analysis (Analyze/Create).
4. Extract network indicators (IPs, domains, user-agents, JA3-class fingerprints, file hashes from transferred files) with provenance notes (Apply).
5. Distinguish forensic inference from speculation: state what evidence supports, what it suggests, and what it cannot show (Evaluate).

## 3. Detailed Concepts

### 3.1 Network evidence taxonomy
- **PCAP:** full fidelity (payloads, retransmission behavior, TLS handshakes); acquisition = SPAN/tap capture (L21 placement) or on-host capture; volatility: ring-buffer overwrite — capture early, slice often.
- **Flow records:** who/when/how-much at scale; the corroboration backbone for timelines; retention depends on L21 tiering.
- **Logs:** DNS/DHCP (L03), auth, proxy, VPN — the identity glue; log-native metadata (serial numbers, session ids) becomes evidence.
- **Device state:** CAM/ARP tables, firewall counters, NAT translations (L12 CGNAT logging!), routing state — volatile, captured via show-commands transcripts with timestamps.
- Acquisition hierarchy follows L25's order of volatility; each source gets its acquisition method + tool + verification (hash).

### 3.2 Chain of custody for digital evidence
- The log *is* the evidence's biography: case id, description, source system, tool+version, acquisition time (with clock-source note), operator, hash, storage location, every transfer with signatures.
- Hashing: SHA-256 at acquisition and re-verified at every transfer; mismatch = integrity challenge — disclose, never hide.
- Working copies: analyze copies, never originals; originals sealed/immutable storage (WORM/object-lock where available).
- Institutional vs legal framing: even internal HR cases benefit; the discipline costs minutes and saves careers.

### 3.3 Timeline reconstruction from network data (the core lab skill)
- Session inventory: from flow/conn data — the conversation map (who talked to whom, when, how much).
- Session anatomy in pcap: stream reassembly, handshake boundaries, window/timing anomalies, retransmission forensics (loss vs deliberate — L04 callback).
- The dual-source rule: every timeline anchor corroborated by ≥ 2 independent sources (pcap + flow, or log + flow) — single-source anchors labeled as such.
- Clock discipline: record sensor clock sources and offsets *in the report* (L26 lesson formalized); UTC everywhere.

### 3.4 Indicator extraction with provenance
- Network IOCs: IPs/domains (with first/last seen + resolution provenance), user-agents, TLS fingerprints (JA3/JA4-class — stable enough? discuss), URIs/paths.
- File evidence: transferred files extracted from pcap (HTTP objects, SMB streams) → hash → malware-sandbox referral (with the ethics rule: only in authorized sandbox).
- Provenance note per IOC: which evidence file, which frame/record, extracted by what — the "show your work" habit that L30's report grades.

### 3.5 Inference discipline
- Evidence shows: a connection existed, bytes moved, a session used X cipher. Evidence suggests: automation (cadence), staging (patterns), compromise (with corroboration).
- Evidence cannot show (say it explicitly): intent, attribution beyond technical indicators, "the attacker" vs "the host," user vs malware action absent corroboration.
- IP ≠ person: DHCP history (L03) + auth logs + physical/port data (L12 802.1X sessions) required before any identity claim — the "IP attribution" fallacy dismantled.

## 4. Teaching Sequence (120 Minutes)

| Time | Segment | Instructor moves |
|---|---|---|
| 0–10 | Warm-up: evidence or not? | 6 artifacts (screenshot, pcap slice, flow csv, verbal recall, config dump, hash log) → classify + defensibility vote |
| 10–35 | Core: custody discipline | Fill a real acquisition log for today's evidence pack; hash + re-verify demo; working-copy rule |
| 35–55 | Core: timeline reconstruction | Session inventory from flows; then pcap stream anatomy; dual-source anchor rule |
| 55–65 | Break | — |
| 65–85 | Core: IOC extraction + inference discipline | Extract 3 IOCs with provenance; the IP-attribution fallacy vignette |
| 85–110 | Student activity: timeline lab | Pairs: reconstruct the case timeline with dual-source anchors + custody log (Lab-15 part 1; cs-091..093 prep) |
| 110–120 | Wrap + formative | Exit ticket; L30 trailer: "one case, many sources — correlate and report" |

## 5. Technical Examples

```
# Acquisition + custody (the first 10 minutes of any case):
sha256sum case-0117-20260920.pcap >> custody.log
# custody.log fields: case id | artifact | tool+version | time(UTC, source) |
#   operator | sha256 | storage location        <- filled BEFORE analysis

# Timeline reconstruction (dual-source method):
tshark -r case-0117.pcap -q -z conv,tcp              # session inventory (pcap)
nfdump -r case-0117.nfcap -s record/bytes            # same window (flows)
# Join: match conversation endpoints/times; each timeline row cites BOTH:
#   02:14:11Z  10.0.20.15 -> 198.51.100.77:443  first beacon
#     [pcap frame 1044] [flow record seq 8812]      <- dual-source anchor

# IOC extraction with provenance:
tshark -r case-0117.pcap --export-objects http,export/   # file objects out
sha256sum export/* ; tshark -r case-0117.pcap -Y 'http.user_agent' -T fields \
  -e http.user_agent | sort | uniq -c
# Provenance line: "UA 'python-requests/2.31' — frames 1044-1090, case-0117.pcap"
```
Expected teaching points: custody before analysis, always; the dual-source habit turns observations into timeline facts; every IOC carries a where-did-this-come-from line.

## 6. Discussion Questions

1. A ring-buffer pcap overwrote the first 10 minutes of the incident. What do you record, and how does it affect your conclusions?
2. Why analyze a copy? What specific custody steps make the original usable if challenged?
3. Flow data says 2 GB left at 03:00; pcap retention missed it. What corroborates the exfil story, and what can you *not* claim?
4. An exec demands to know "who did this." Draft the two-sentence answer that is defensible.
5. JA3 fingerprints: stable enough for IOCs? Give the conditions where they help and where they mislead.

## 7. Student Activity

**Timeline lab (25 min, pairs):** from the case evidence pack: (1) complete the custody log (hash + storage + working-copy declaration), (2) build the session inventory from flows, (3) reconstruct ≥ 6 dual-source timeline anchors in pcap, (4) extract 3 IOCs with provenance lines. Deliverable: evidence-indexed worksheet — the input for L30's full report.

## 8. Problem-Solving Case

**Primary case — cs-092 "Pcap session-timeline reconstruction" (expert):**
Case file: a finance workstation beacons nightly (22:00±10 min) to a CDN-fronted domain, then uploads to an anonymous file-share via HTTP (not HTTPS — the break in the case). Provided: 48-h pcap slice (ring-buffered, partial first night), flows for both nights, DHCP + 802.1X auth excerpts. Students must (a) produce the dual-source timeline including the gap-disclosure note, (b) extract IOCs (domain, share URL, UA, transferred-file hash), (c) resolve the workstation's *user* via DHCP/auth correlation (defensible identity claim), and (d) annotate exactly which conclusions remain inference-grade.
**Linked cases:** cs-091 (custody planning), cs-093 (netflow corroboration).
*(Model solutions: instructor answer-key set, Module 8.)*

## 9. Formative Assessment

1. Order four network evidence types by volatility and name each acquisition method.
2. What five fields must the custody log carry at acquisition?
3. Why is a single-source timeline anchor flagged rather than silently used?
4. Give the evidence-backed answer vs the speculation answer for "who did this?"
5. What makes an IOC "provenance-complete"?
*(Answer key: instructor set, Module 8.)*

## 10. Summary & Key Takeaways

- Forensics = disciplined acquisition (custody, hashes, working copies) + reconstruction (dual-source timelines) + honest inference.
- Network evidence is the fastest-decaying and often the most corroborative — capture early, slice often.
- IP ≠ person; evidence ≠ intent. The report's credibility lives in these two distinctions.

## 11. References

- NIST SP 800-86 — forensic integration (acquisition, custody, reporting).
- RFC 3227 — evidence collection & archiving (order of volatility authority).
- IETF/Bitdefender-class JA3/JA4 references — TLS fingerprinting methodology + limitations.
- Casey, *Digital Evidence and Computer Computer Crime* — custody/legal framing chapters.
- Wireshark/tshark docs — export-objects, conv statistics (current).

## 12. CLO Mapping

| CLO | Where in this lecture | Assessed via |
|---|---|---|
| CLO-14 | §3.1–3.5 custody/timeline/IOC craft; timeline lab | Lab-15 (W15), Final practical, Capstone |
