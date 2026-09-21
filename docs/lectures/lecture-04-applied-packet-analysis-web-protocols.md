---
lecture: L04
title: Applied Packet Analysis & Web Protocols
module: 1
week: 2
hours: 2
clos: [CLO-1]
difficulty: beginner
status: complete
artifact-type: student-lecture-material
instructor-plan: modules/module-01-network-foundations/lectures/lecture-04-applied-packet-analysis-web-protocols.md
---

# L04 — Applied Packet Analysis & Web Protocols

## 1. Learning Objectives

By the end of this session you can: (1) build capture vs display filters for a stated question; (2) triage an unknown capture in ≤ 10 minutes using a fixed workflow; (3) identify cleartext exposure classes in HTTP; (4) state what TLS hides and what remains inferable; (5) produce a written triage note with frame-number citations.

## 2. Key Definitions

| Term | Definition |
|---|---|
| Capture filter (BPF) | Applied *during* collection; discards non-matching packets early |
| Display filter | Applied to the already-captured file; refines analysis without data loss |
| Conversation | A source/destination pair's traffic (endpoints + ports) view |
| Protocol hierarchy | Percentage breakdown of protocols in a capture — the "what's on the wire" view |
| SNI | Server Name Indication — the hostname a TLS client reveals in the handshake |
| HSTS | HTTP Strict Transport Security — policy forcing HTTPS (full detail L14) |
| Triage note | Written analysis: scope → inventory → anomaly → hypothesis, with citations |

## 3. Detailed Explanations

### 3.1 The analyst's toolkit hierarchy
**tcpdump** is the everywhere-tool: reliable capture with BPF filters (`-i`, `-nn`, `-w`, `port 53`). **Wireshark** is the workbench: dissection, statistics, follow-stream. Discipline: prefer *full capture + display filters* over aggressive capture filters (you can't re-analyze packets you discarded), but filter when volume demands it. Ring buffers prevent disk exhaustion on long captures.

### 3.2 Filter craft — the twenty that matter
Capture (BPF): `host`, `net`, `port 53`, `tcp[13] & 0x12 != 0` (SYN/ACK), `vlan`. Display: `http.request`, `dns.flags.response == 0`, `tcp.analysis.flags` (retransmits, zero-window, dup-acks), `tcp.stream eq N`, `arp.duplicate-address-detected`. Statistics views: **Protocol Hierarchy** (what's actually present), **Conversations** (who talks to whom, how much), **IO Graph** (rate anomalies). Rule of thumb: hierarchy first on an unknown file, then conversations, then filters.

### 3.3 HTTP on the wire
A request line (method, path, version), headers, body; response status classes (2xx ok, 3xx redirect, 4xx/5xx errors). Cleartext exposure classes: **Basic-auth credentials**, **form-post passwords**, **session cookies**, **referrer leaks**, **API tokens in URLs**. HTTP/2 multiplexes many streams per connection; HTTP/3 (QUIC) runs over **UDP/443** — update your "web traffic" filter assumptions accordingly.

### 3.4 What TLS hides — and what it doesn't
Hidden: URLs, payloads, most headers. Still visible: DNS lookups, IPs, **SNI** (unless ECH), the certificate chain in the handshake, record sizes and **timing**. Analyst consequence: behavioral detection (beacon periodicity, volume spikes) survives encryption — this is the premise of Module 6's detection engineering and the reason your L04 triage can flag a beacon you cannot read.

### 3.5 The triage workflow (repeatable, examinable)
1. **Scope** — duration, hosts, volume (`capinfos` / capture summary).
2. **Inventory** — protocol hierarchy; top talkers.
3. **Baseline vs anomaly** — conversations + IO graph + `tcp.analysis.flags`.
4. **Hypothesis** — one testable sentence.
5. **Artifact** — triage note with frame-number citations and capture metadata (files are potential evidence — Module 8 formalizes why).

## 4. Network Diagram: what each view answers

```
 Capture file ──► [Summary/capinfos]  how long? how big?
              ──► [Protocol hierarchy] what's on the wire?
              ──► [Conversations]      who talks to whom, how much?
              ──► [IO graph]           when? (rate anomalies)
              ──► [Filters/streams]    exactly what was said/readable?
              ──► [Triage note]        scope+inventory+anomaly+hypothesis+citations
```

## 5. Protocol Examples

- Cleartext login: `http.authorization contains "Basic"` → credentials in base64 (not encryption — just encoding).
- Same login over TLS: payload unreadable; SNI reveals the hostname; handshake frames reveal the certificate.
- Beacon shape: small HTTPS flows to one external IP every ~60 s, visible in Conversations/IO graph even though content is opaque (cs-010).

## 6. Configuration Concepts (concept level)

- Capture hygiene: `-w file.pcap` with ring buffers (`-C` size, `-W` count); timestamp source recorded.
- Tailing servers without GUI: `tshark -r file.pcap -Y 'http.request' -T fields -e ip.src -e http.host`.
- Wireshark profiles: pre-configured columns (stream, SNI, TTL) make triage fast and consistent.

## 7. Security Implications

- Filter craft converts protocol knowledge (L02–L03) into *evidence*.
- Cleartext protocols are an integrity *and* confidentiality failure class (L02's FCS lesson scales up).
- Metadata survives encryption: plan detections around behavior, not content.
- Capture files are evidence: record time source, tool, and scope — now, as a habit.

## 8. Realistic Organizational Scenario

**"The internet is slow" ticket (running case).** A user complains; you receive a 5-minute capture. Protocol hierarchy: normal. Conversations: one CDN IP with a burst of retransmissions (loss — the *complaint* cause) and, separately, small periodic HTTPS flows to a single external IP (the *security* finding). The triage note separates both and cites frames. Lesson: complaints and security findings travel in the same capture — **case cs-010** trains exactly this separation.

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "HTTPS makes analysis impossible" | Content is hidden; metadata (SNI, sizes, timing, DNS) remains — and it's rich. |
| "More capture filters = better" | Aggressive filters destroy evidence; filter analysis, not collection (usually). |
| "Wireshark is the only tool" | tcpdump/tshark work everywhere; GUI is for dissection, not collection. |
| "The padlock means the site is safe" | TLS authenticates the *connection*, not the *intent* — phishing sites use valid TLS. |
| "Base64 is encryption" | Encoding ≠ encryption; Basic-auth is trivially reversible on-path. |

## 10. Classroom Activities

1. **Filter drills:** instructor poses ten questions ("show only DNS queries", "find POSTs"); teams race to correct display filters.
2. **Triage drill (pairs, timed):** unknown 5-minute capture → 5-line triage note with citations; two pairs with the same capture cross-check — disagreement is the lesson.
3. **Cleartext vs TLS side-by-side:** same login twice; list what survived encryption.

## 11. Problem-Solving Questions

1. Why is a capture file considered potential evidence? Name two metadata items to record at capture time.
2. Your site is HTTPS-only. List three things an on-path observer still learns and one defense for each.
3. When would you *not* use capture filters during collection?
4. HTTP/3 runs over UDP/443 — how does that change your "web traffic" assumptions and filters?
5. Which single statistics view do you open first on an unknown capture, and why that one?

## 12. Exit Ticket

1. Write a display filter showing only DNS queries (not responses).
2. Name two credential-exposure classes visible in plain HTTP.
3. Over TLS, which DNS artifact still reveals the destination hostname?
4. What does `tcp.analysis.flags` aggregate, and why is it a good second view?
5. Order the triage workflow steps; justify why inventory precedes anomaly hunting.

*(Answers: `teaching/answer-keys/answer-key-module-01.md`.)*

## 13. References

- Wireshark User's Guide — filter and statistics reference (current).
- RFC 9110/9112 (HTTP semantics/1.1); RFC 9000 (QUIC); RFC 9114 (HTTP/3).
- Sanders, *Practical Packet Analysis* — triage workflow chapters.
- Bejtlich, *The Practice of Network Security Monitoring* — collection discipline.
- tshark/tcpdump man pages.

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-1 | §3 filter craft + workflow; §11/§12 analysis | Quiz 1 (today), Lab-02, Midterm |
