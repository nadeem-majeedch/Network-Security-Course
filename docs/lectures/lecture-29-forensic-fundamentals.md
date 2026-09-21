---
lecture: L29
title: Forensic Fundamentals
module: 8
week: 15
hours: 2
clos: [CLO-14]
difficulty: expert
status: complete
artifact-type: student-lecture-material
instructor-plan: modules/module-08-forensics-capstone/lectures/lecture-29-forensic-fundamentals.md
---

# L29 — Forensic Fundamentals

## 1. Learning Objectives

By the end of this session you can: (1) classify network forensic evidence types by volatility, fidelity, and acquisition method; (2) apply chain-of-custody discipline (acquisition log, hashing, working copies); (3) reconstruct a session timeline from pcap and flow records with dual-source anchors; (4) extract network IOCs with provenance; (5) separate forensic inference from speculation — and say so in writing.

## 2. Key Definitions

| Term | Definition |
|---|---|
| Forensic evidence | Any artifact that supports a factual finding — with defensible handling |
| Chain of custody | Signed biography of an artifact: acquisition, hashes, every transfer |
| Acquisition log | Case id, artifact, tool+version, time (source), operator, hash, storage |
| Working copy | Analysis performed on verified copies; originals sealed |
| Dual-source anchor | Timeline event corroborated by ≥2 independent evidence sources |
| IOC | Indicator of compromise (IP, domain, hash, UA) — worthless without provenance |
| Provenance | Where the IOC came from: file, frame/record id, extraction method |
| Attribution fallacy | Assuming an IP proves a person; identity needs DHCP/auth/port correlation |
| Order of volatility | Evidence decay order (L25) — network artifacts often decay fastest |

## 3. Detailed Explanations

### 3.1 Network evidence taxonomy
- **PCAP:** full fidelity (payloads, retransmits, TLS handshakes). Acquisition: SPAN/tap (L21) or on-host capture. Volatility: ring buffers overwrite — *capture early, slice often*.
- **Flow records:** the corroboration backbone — who/when/how-much at scale; retention per L21 tiers.
- **Logs:** DNS/DHCP (L03), auth, proxy, VPN — the identity glue; serial numbers and session ids become evidence.
- **Device state:** CAM/ARP tables, NAT translations (L12's CGNAT logging!), counters — captured via read-only show-command transcripts with timestamps.
Acquisition follows L25's order of volatility; each source gets tool + verification (hash).

### 3.2 Chain of custody for digital evidence
The custody log is the artifact's *biography*: case id, description, source system, tool+version, acquisition time (with clock-source note), operator, **SHA-256 at acquisition**, storage location, and every transfer with signatures. Hash mismatch = integrity challenge — *disclose it*, never hide it. **Working copies:** analyze copies; originals sealed (WORM/object-lock). Even internal HR cases benefit — the discipline costs minutes and saves careers.

### 3.3 Timeline reconstruction (the core lab skill)
1. **Session inventory** from flow/conn data: the conversation map.
2. **Session anatomy** in pcap: stream reassembly, handshake boundaries, retransmission forensics (loss vs deliberate — L04 callback).
3. **The dual-source rule:** every anchor corroborated by ≥2 independent sources (pcap + flow, or log + flow); single-source anchors *labeled as such* — never silently used.
4. **Clock discipline:** record sensor sources and offsets in the report; UTC everywhere.

### 3.4 Indicator extraction with provenance
Network IOCs: IPs/domains (with first/last seen + resolution), user-agents, TLS fingerprints (JA3/JA4-class — with stability caveats), URIs. **File evidence:** transferred objects extracted from pcap (HTTP objects, SMB streams) → hashed → sandbox referral only in authorized sandboxes. **Provenance per IOC:** which file, which frame/record, extracted how — the "show your work" habit L30's report grades.

### 3.5 Inference discipline
- Evidence *shows*: a connection existed; bytes moved; a session used cipher X.
- Evidence *suggests*: automation (cadence); staging (patterns); compromise (with corroboration).
- Evidence *cannot show*: intent; "the attacker" vs "the host"; identity without DHCP/auth/port correlation. **IP ≠ person.**
Write the distinction down — the credibility of your report lives in these labels.

## 4. Network Diagram: acquisition → custody → timeline

```
 Capture/ring buffer ──acquire──► [hash + acquisition log] ──► [sealed original]
                                        │ verified copy
                                        ▼
        [flows] + [pcap] + [logs] ──join──► timeline with dual-source anchors
        every anchor:  ts | event | [pcap frame] [flow record]   ← citations
```

## 5. Protocol Examples

```
 # Acquisition + custody (the first 10 minutes of any case):
 sha256sum case-0117-20260920.pcap >> custody.log
 # fields: case id | artifact | tool+version | time(UTC,source) | operator | hash | storage

 # Session inventory + dual-source timeline:
 tshark -r case-0117.pcap -q -z conv,tcp          # pcap-side inventory
 nfdump -r case-0117.nfcap -s record/bytes        # flow-side (same window)
 #   anchor: 02:14:11Z  10.0.20.15 -> 198.51.100.77:443  first beacon
 #           [pcap frame 1044] [flow seq 8812]           ← dual-source

 # IOC extraction with provenance:
 tshark -r case-0117.pcap --export-objects http,export/ ; sha256sum export/*
 # provenance line: "UA python-requests/2.31 — frames 1044-1090, case-0117.pcap"
```

## 6. Configuration Concepts (concept level)

- Evidence vault: immutable storage (object-lock/WORM), access logging, transfer signing.
- Ring-buffer sizing vs retention needs (the overwrite risk is a design decision).
- Standard toolset pinned per case (versions recorded in the log).

## 7. Security Implications

- Forensics = disciplined acquisition (custody + hashes + copies) + reconstruction (dual-source) + honest inference.
- Network evidence decays fastest and corroborates best — capture early, slice often.
- IP ≠ person; evidence ≠ intent — the report's credibility lives in these two distinctions.

## 8. Realistic Organizational Scenario

**The nightly beacon (running case).** A finance workstation beacons nightly (22:00±10 min) to a CDN-fronted domain, then uploads via plain HTTP (the break in the case). Provided: a 48-h pcap slice (ring-buffered, partial first night — disclose the gap), flows for both nights, DHCP + 802.1X auth excerpts. You produce the dual-source timeline (including the gap disclosure), extract IOCs with provenance, resolve the *user* via DHCP/auth correlation (a defensible identity claim), and label what remains inference-grade. Full case: **cs-092**; the timeline lab is the in-session exercise (Lab-15 part 1).

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "Forensics = installing a GUI tool" | It's method: custody, hashes, corroboration, disclosure. |
| "The IP address proves who did it" | DHCP + auth + port data correlate identity; an IP alone proves nothing about a person. |
| "The pcap proves intent" | It proves packets; intent is inference — labeled as such. |
| "Chain of custody is court-only paperwork" | It's what makes *internal* conclusions defensible. |
| "Silent gaps are OK" | Declared, explained gaps preserve credibility; hidden ones destroy it. |

## 10. Classroom Activities

1. **Timeline lab (pairs):** custody log (hash + storage + working-copy declaration), session inventory from flows, ≥6 dual-source anchors in pcap, 3 IOCs with provenance lines.
2. **Evidence-or-not drill:** six artifacts → classify + defensibility vote.
3. **Attribution-fallacy teardown:** a "we know it was Bob" claim → rebuild it with correlation or deflate it.

## 11. Problem-Solving Questions

1. A ring buffer overwrote the first 10 minutes of the incident: what do you record, and how does it affect conclusions?
2. Why analyze a copy? What custody steps make the original usable if challenged?
3. Flow data shows 2 GB leaving at 03:00 but pcap retention missed it: what corroborates the exfil story, and what can you *not* claim?
4. An exec demands "who did this": draft the two-sentence defensible answer.
5. Are JA3 fingerprints stable enough for IOCs? Give the conditions where they help and where they mislead.

## 12. Exit Ticket

1. Order four network evidence types by volatility; name each acquisition method.
2. What five fields must the custody log carry at acquisition?
3. Why is a single-source timeline anchor flagged rather than silently used?
4. Give the evidence-backed vs the speculative answer for "who did this?"
5. What makes an IOC "provenance-complete"?

*(Answers: `teaching/answer-keys/answer-key-module-08.md`.)*

## 13. References

- NIST SP 800-86 — guide to integrating forensic techniques.
- RFC 3227 — evidence collection and archiving (order of volatility).
- Casey, *Digital Evidence and Computer Crime* — custody/legal chapters.
- JA3/JA4 methodology references (TLS fingerprinting + limitations).
- Wireshark/tshark docs — export-objects, conv statistics (current).

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-14 | §3 custody/timeline/IOC craft | Lab-15 (W15), Final practical, Capstone |
