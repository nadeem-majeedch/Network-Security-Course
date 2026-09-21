---
lecture: L04
title: Applied Packet Analysis & Web Protocols
module: 1
week: 2
hours: 2
clos: [CLO-1]
difficulty: beginner
status: complete
artifact-type: teaching-plan
---

# L04 — Applied Packet Analysis & Web Protocols (Teaching Plan)

## 1. Overview & Prerequisites

- **Prerequisites:** L03 (TCP/UDP/DNS/DHCP mechanics).
- **Position:** converts protocol knowledge into *tool fluency*. Every subsequent module assumes students can filter, follow, and triage captures quickly. Closes Module 1 with the first graded quiz.
- **Faculty prep:** prepare the triage capture set (three 5-minute captures: normal office, mixed web, one with an HTTP-credential reuse pattern); print triage checklist cards; ready Quiz-1 papers.
- **Common misconceptions:** "Wireshark is the only tool"; "HTTPS makes analysis impossible"; "more packets captured = better."

## 2. Learning Objectives

By the end of this lecture, students can:

1. Build and combine Wireshark capture vs display filters for a stated question (e.g., "all DNS to non-resolver hosts") (Apply).
2. Use Follow-stream, protocol hierarchy, endpoints/conversations, and IO-graph views to triage an unknown capture in ≤ 10 minutes (Apply).
3. Explain HTTP request/response structure and identify cleartext exposure classes (credentials, tokens, PII) (Understand/Analyze).
4. Describe what TLS changes at the visible layer (SNI, certificate exchange, record boundaries) and what remains inferable (timing, volumes, DNS) (Understand).
5. Execute a documented triage workflow: scope → services → anomalies → hypothesis (Apply).

## 3. Detailed Concepts

### 3.1 The analyst's toolkit hierarchy
- tcpdump: reliable capture, minimal filters (`-i`, `-nn`, `-w`, BPF syntax) — the tool that works everywhere.
- Wireshark: dissection, statistics, follow-stream — the teaching/analysis workbench.
- Capture discipline: filter *at capture* only when volume demands; prefer full capture + display filters; respect ring buffers and PII handling rules (capture files are evidence — L29 links).

### 3.2 Filter craft (the 20 filters that matter)
- Capture (BPF): `host`, `net`, `port 53`, `tcp[13] & 0x12 != 0` (SYN/ACK), `vlan`.
- Display: `http.request`, `dns.flags.response == 0`, `tcp.analysis.flags` (retransmits, zero window), `tcp.stream eq N`, `arp.duplicate-address-detected`.
- Statistics views: protocol hierarchy (what's actually on the wire), conversations (who talks to whom, how much), IO graph (rate anomalies).

### 3.3 HTTP on the wire
- Request line/method/headers; response status classes; cookies as session state (session hijack setup for L07).
- Cleartext exposure classes: Basic-auth credentials, form posts, session cookies, referrer leaks, API tokens.
- HTTP/2 and HTTP/3 (QUIC/UDP/443): visibility shifts — multiplexing hides per-object flows; QUIC moves analysis from TCP ports to UDP/443.

### 3.4 What TLS hides and what it doesn't
- Hidden: URLs, payloads, most headers.
- Visible: DNS resolution, IPs, SNI (unless ECH), certificate chain (in handshake), timing/volume signatures, record sizes.
- Analyst consequence: behavioral detection (beacon periodicity, volume spikes) survives encryption — the Module 6 premise.

### 3.5 The triage workflow (repeatable, examinable)
1. Scope: duration, hosts, volume (capinfos / Wireshark summary).
2. Inventory: protocol hierarchy; top talkers.
3. Baseline vs anomaly: conversations + IO graph + `tcp.analysis.flags`.
4. Hypothesis: one sentence, testable against the capture.
5. Artifact: exported packet/notes with frame numbers (evidence discipline preview).

## 4. Teaching Sequence (120 Minutes)

| Time | Segment | Instructor moves |
|---|---|---|
| 0–10 | Quiz-1 administration (20 min is §4 slot? no — see activity) | Quiz runs 0–20; buffer for late arrivals |
| 20–45 | Core: capture/filter craft | Live: build 10 filters on the big capture; students predict result counts before each |
| 45–65 | Core: HTTP/TLS visibility | Follow-stream a cleartext login (lab-only site); then the same over TLS — what survived? |
| 65–75 | Break | — |
| 75–105 | Student activity: triage drill | Teams of 2 triage one unknown capture with the checklist; 10-minute hard cap; compare workflows |
| 105–115 | Case debrief | cs-009/cs-010 walkthrough of one team's hypothesis chain |
| 115–120 | Wrap | Module-2 trailer: "next week we model the attacker looking at these same packets" |

## 5. Technical Examples

```
# Reliable capture at the shell (works on servers without GUI)
sudo tcpdump -i eth0 -nn -w office.pcap 'port 53 or port 80 or port 443'

# Wireshark display-filter drills (on the staged set)
http.request.method == "POST"                 # find form submissions
http.authorization contains "Basic"           # cleartext credential exposure
dns.qry.name contains "update" && dns.flags.response == 0
tcp.analysis.retransmission                   # loss vs deliberate anomaly discussion
tcp.flags.syn == 1 && tcp.flags.ack == 0      # connection attempts inventory

# CLI equivalents for headless triage
tshark -r office.pcap -Y 'http.request' -T fields -e ip.src -e http.host -e http.request.uri
capinfos office.pcap
```
Expected teaching points: same question, three tools; display filters refine, capture filters constrain.

## 6. Discussion Questions

1. Why is a capture file considered potential evidence? What two metadata items must you record at capture time?
2. Your site is HTTPS-only. List three things an on-path observer still learns, and one defense for each.
3. When would you *not* use capture filters during collection?
4. HTTP/3 runs over UDP/443 — how does that change your "web traffic" filter assumptions?
5. Which single Wireshark statistics view would you open first on an unknown capture, and why?

## 7. Student Activity

**Triage drill (30 min, pairs, timed):** each pair receives one unknown 5-minute capture and the checklist card (scope → inventory → anomaly → hypothesis → artifact). Deliverable: a 5-line triage note with frame-number citations and a one-sentence hypothesis. Two pairs with the same capture cross-check notes — disagreement is the lesson (same evidence, different inference; discipline closes the gap).

## 8. Problem-Solving Case

**Primary case — cs-010 "First-pass triage of an unfamiliar capture" (beginner):**
You are handed a capture from a user complaining "the internet is slow." The file shows normal DNS, a burst of TCP retransmissions to one CDN IP, and periodic ~60-second beacons of small HTTPS flows to a single external IP. Students must separate the *complaint* cause (retransmission/loss pattern) from the *security* finding (periodic beacon — later confirmed in Module 6), and state precisely what evidence supports each.
**Linked cases:** cs-009 (mixed-content/HTTP downgrade exposure).
*(Model solutions: instructor answer-key set, Module 1.)*

## 9. Formative Assessment

1. Write a display filter showing only DNS queries (not responses).
2. Name two credential-exposure classes visible in plain HTTP.
3. Over TLS, which DNS artifact still reveals the destination hostname?
4. What does `tcp.analysis.flags` aggregate, and why is it a good second view?
5. Order the triage workflow steps and justify why inventory precedes anomaly hunting.
*(Answer key: instructor set, Module 1.)*

## 10. Summary & Key Takeaways

- Fluency = filter craft + statistics views + a fixed triage workflow, not menu knowledge.
- TLS moves secrecy, not invisibility: metadata still tells a story — Module 6's foundation.
- Capture files are evidence: record scope and metadata now; Module 8 formalizes it.

## 11. References

- Wireshark User's Guide — capture/display filter reference; tcpdump/tshark man pages.
- RFC 9110/9112 — HTTP semantics & HTTP/1.1; RFC 9114 — HTTP/3; RFC 9000 — QUIC.
- Sanders, *Practical Packet Analysis* — triage workflow chapters.
- Bejtlich, *The Practice of Network Security Monitoring* — collection & analysis discipline.
- NIST SP 800-86 — guide to integrating forensic techniques (evidence-handling preview).

## 12. CLO Mapping

| CLO | Where in this lecture | Assessed via |
|---|---|---|
| CLO-1 | §3.2–3.5 tool fluency over protocols learned in L01–L03; triage workflow | Quiz 1 (today), Lab-02, Midterm |
