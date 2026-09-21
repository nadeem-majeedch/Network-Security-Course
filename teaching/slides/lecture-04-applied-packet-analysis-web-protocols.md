---
marp: true
theme: default
paginate: true
lecture: L04
week: 2
clos: [CLO-1]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# Applied Packet Analysis & Web Protocols

**Network Security · Lecture 4 · Week 2**

*Reading the wire fluently — the analyst's superpower.*

<!-- notes: OPEN (2 min). Hook: "Everything on this course's wire is
text until encryption; learn to read, and the network narrates its own
crimes." -->

---

## Learning Objectives

1. **Read** HTTP request/response pairs in a capture
2. **Explain** what TLS hides and what it *doesn't* (metadata lives)
3. **Analyze** a mixed HTTP/HTTPS session for exposure
4. **Correlate** flows, logs, and captures into one story
5. **Apply** Wireshark display-filter fluency for triage

<!-- notes: (1 min) Objective 3 is the mixed-content case (cs-009).
Objective 5 feeds Lab-02 directly. -->

---

## HTTP on the Wire (Cleartext)

```
GET /admin/login?user=bob&password=hunter2 HTTP/1.1
Host: intranet.example
Cookie: session=8f3ac...
```

- Everything visible: paths, parameters, cookies, credentials
- Security takeaway: **HTTP POST ≠ encryption** — payloads still visible

<!-- notes: (5 min) Live capture read: students gasp at the password
line every year. The teaching point is the takeaway line — POST is a
method, not a lock. -->

---

## HTTPS: What's Hidden, What Isn't

| Hidden by TLS | Still visible |
|---|---|
| URLs, payloads, cookies | DNS name (SNI), IPs, timing, sizes |

- SNI leaks the destination *server name* in the handshake
- Traffic analysis: request size patterns survive encryption

<!-- notes: (5 min) The SNI point matters for egress design (L12):
blocking by SNI is possible on encrypted flows. CS/DS: dataset exfil
size-rhythm survives encryption (cs-065's flow-log case uses exactly
this). -->

---

## The TLS Record Layer (First Look)

- Handshake → keys → records: `{type, version, length, payload}`
- AEAD records (TLS 1.3): confidentiality + integrity in one
- Full handshake anatomy = L14's deep dive — today, just the shape

<!-- notes: (3 min) Deliberately shallow — name the parts, promise L14.
Don't teach the handshake twice. -->

---

## Mixed Content: The Downgrade Window

- HTTPS page pulls `http://` subresources → cleartext window
- Attack: intercept the HTTP leg, inject content
- cs-009's case reads exactly this exposure

<!-- notes: (4 min) The mixed-content lock icon story: browsers warn,
users click through. Ties to the certificate click-through culture from
assignment 2. -->

---

## Flow Records vs Captures

| Source | Granularity | Content |
|---|---|---|
| Flow (NetFlow/IPFIX) | per-conversation aggregate | IPs, ports, bytes, timing |
| PCAP | per-packet | full headers + payloads |

- Flows = cheap, long-window, network-wide
- PCAP = expensive, short-window, total detail
- The analyst's rhythm: **flows find where, PCAP explains what**

<!-- notes: (5 min) This rhythm is the course's forensic spine (L29–30
build on it directly). Quiz 6-14 arc references it. cs-097's correlation
case is the expert version. -->

---

## Wireshark Triage Fluency

- Display filters: `http`, `dns`, `tcp.flags.syn==1`, `ip.addr==10.0.5.66`
- Follow stream = reassemble a conversation
- Statistics → conversations = the "who talks to whom" map
- Capture filters ≠ display filters (BPF vs Wireshark syntax)

<!-- notes: (6 min) Demo three filters live on Lab-02's dataset. The
"conversations" view is the 80% tool — teach that one hard. -->

---

## Correlation: One Story, Three Sources

- Proxy log: user fetched URL X at T
- Firewall log: flow allowed at T+ε
- Capture: the packets themselves
- *One story, told three ways* — discrepancy = investigation

<!-- notes: (4 min) The three-way corroboration discipline gets formal
in L26 — plant it now with a concrete triangle. -->

---

## CS/DS Example: Notebook → Data Lake

- A notebook run: DNS query, TLS handshake to lake, 40 MB pull
- Flow shows the volume; SNI shows the lake; TLS hides the content
- Anomalous = volume/destination change, not content (content is opaque)

<!-- notes: (3 min) DS framing: security analytics on *metadata* is the
daily bread — this is why flow-log fluency matters for DS students
(cs-065's case is exactly this shape). -->

---

## Activity: The Captured Conversation (6 min)

Given the seeded capture with three conversations: rank them by
suspicion, name what evidence you'd pull next for the top one.

<!-- notes: (6 min) Pairs. The seeded conversations: benign update
check, cleartext admin login, large periodic TLS. The ranking debate is
the point — evidence-based ranking, not vibes. -->

---

## Case Study: cs-010 (5 min)

- First-pass triage of an unfamiliar capture — structure your read

<!-- notes: (5 min) Teach the triage structure: conversations →
protocols → outliers → hypothesis. The case rewards method, not luck. -->

---

## Formative Check

- Oral: name two things TLS hides and two it doesn't.

<!-- notes: (2 min) Quiz-6/quiz-10 overlap; oral exit. -->

---

## References & Next

- RFC 9110 (HTTP semantics), Wireshark user guide
- Diagrams: `diagrams/05-tls-handshake.md` (preview)
- **Next (L05):** threat modeling — the attacker gets a project plan
