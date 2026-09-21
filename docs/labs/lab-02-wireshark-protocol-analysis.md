---
lab: Lab-02
title: Packet Capture & Protocol Analysis with Wireshark
week: 2
module: 1
clos: [CLO-1]
lectures: [L03, L04]
duration: 2h (embedded in lecture block)
status: complete
artifact-type: student-lab-handout
instructor-key: teaching/lab-answer-keys/lab-02-answer-key.md
---

# Lab-02 — Packet Capture & Protocol Analysis with Wireshark

## 1. Lab Overview & CLO Mapping

This lab turns L03/L04's protocol mechanics into reading fluency: you will
dissect TCP sessions, DNS resolution, DHCP leases, and HTTP in captured frames,
then *predict* what a capture of the same conversation must contain before you
look. *CLO-1* — explain core protocols from their wire evidence. Reference
lectures: L03 (TCP/UDP/DNS/DHCP), L04 (applied analysis).

## 2. Learning Objectives

By the end you can: (1) navigate Wireshark's capture vs display filters
correctly; (2) trace a full TCP lifecycle (handshake → data → teardown) by
sequence number; (3) follow a DNS query to its answer and a DHCP DORA exchange
end-to-end; (4) reconstruct an HTTP request/response pair from stream view;
(5) justify every claim with frame numbers.

## 3. Prerequisites

Lab-01 submitted (baseline + first capture); L03 attended; dataset verified
(§6 step 1).

## 4. Estimated Duration

120 minutes: dataset verification 10 · guided dissection 40 · challenge
stations 45 · write-up 25.

## 5. Required Software & Hardware

- Lab-range VM with Wireshark ≥ 4.0 (pinned on the lab sheet), Python 3.11+.
- Dataset: `docs/labs/datasets/lab02-normal-traffic.pcap` (verify per §6).

## 6. Setup Instructions

> **Command status:** ✅ = executed/verified against the dataset at authoring
> time; ⚠️ = untested here, reference shape per official documentation.

1. ✅ Verify the dataset:

```bash
cd docs/labs/datasets && sha256sum -c SHA256SUMS
# ✅ verified: lab02-normal-traffic.pcap OK (54 packets, all IPv4)
```

2. ⚠️ Open in Wireshark: `wireshark datasets/lab02-normal-traffic.pcap` (or File → Open).
3. ⚠️ Useful display filters for this lab (reference card):

```
tcp.flags.syn == 1 && tcp.flags.ack == 0     # SYNs only
tcp.analysis.initial_rtt                      # Statistics menu, not a filter
dns.flags.response == 0                       # queries only
bootp || dhcp                                 # DHCP (Wireshark calls it bootp historically)
http.request.method == "GET"                  # HTTP requests
```

## 7. Authorization & Safety Notes

- **Authorization basis:** all analysis is confined to the instructor-authorized lab range and the pinned course datasets; anything outside that boundary is prohibited.

- The dataset is synthetic course evidence; analysis happens only on it or on
  range captures. Never capture on networks you don't own — campus Wi-Fi
  capture is a policy violation even "just to look".
- Keep original files read-only: copy before analysis (evidence habit from Lab-01 §7).

## 8. Student Tasks

1. **TCP lifecycle:** pick the HTTP conversation to 10.20.30.10:80. Record the
   3-way handshake ports/seqs, the request and response frame numbers, and both
   FIN/ACKs. Explain which side closed first.
2. **DNS:** follow one query (`updates.lab.example`). Record: transaction ID,
   query type, response answer, and the UDP port pair. Why do query and response
   share the port pair?
3. **DHCP:** locate the DORA exchange for 10.20.0.102. Record: xid, option 53
   values in each message, broadcast/multicast addressing at L2, and the
   offered lease time (option 51).
4. **HTTP:** reconstruct the GET and its response in Follow → TCP Stream. Note
   headers: Host, User-Agent, Content-Length, Content-Type.
5. **Prediction check:** before opening `lab02-normal-traffic.pcap`'s NTP
   session to 198.51.100.9, write what frames it must contain; then verify.
6. Write-up: five findings, each = claim + frame numbers + one-sentence mechanism.

## 9. Expected Observations

- Handshake seqs are per-direction; the third ACK carries no data.
- DNS: query to port 53, response from 53 with matching txid; A answers with TTL 300.
- DHCP Discover/Request broadcast (dst ff:ff:ff:ff:ff:ff, 255.255.255.255),
  Offer/ACK carry siaddr 10.20.0.1 and lease 3600 s.
- HTTP response Content-Length matches body bytes exactly — a small integrity
  intuition you will formalize with hashes later.

## 10. Analysis Questions

1. Why does TCP need sequence numbers at all — what two failure modes of the
   IP layer below does reassembly by seq solve?
2. A junior analyst says "DNS is insecure, switch to TCP". What is actually
   exposed on UDP/53 cleartext DNS, and what would (and would not) DoT/DoH fix?
3. DHCP Offer/ACK are broadcast here. What does that imply about who can spoof
   them, and which L2 control (forward-look to L06/L12) constrains it?
4. If two frames arrived with identical seq numbers for the same flow, what
   would Wireshark flag, and what retransmission scenarios produce a
   *different-payload* duplicate (why does that matter for forensics)?
5. Which of your five findings would survive as detection logic (a field +
   expected value), and which is context-dependent?

## 11. Troubleshooting

- "No DHCP frames" → your display filter used `dhcp` on an old Wireshark;
  try `bootp`.
- Stream view garbled → multiple conversations in the filter; narrow to the
  TCP stream index first (`tcp.stream eq N`).
- Wrong answer IP in DNS → you opened the wrong txid pair; match query/response
  by transaction ID, not order.

## 12. Cleanup Instructions

- Export your annotated file as `lab02-annotated.pcapng`; delete scratch copies.
- Close Wireshark; VM logout; no files left on shared paths.

## 13. Submission Requirements

- `lab02-annotated.pcapng` with bookmarks/markings on the frames cited.
- Findings table (5 rows: claim · frames · mechanism).
- Prediction-check paragraph (task 5) written **before** verification, dated.
- Analysis answers (5) with frame citations.
- Due: start of Week 3 session.

## 14. Expected Output & Evidence

| Artifact | Passing evidence |
|---|---|
| Annotated capture | bookmarks on handshake, DNS pair, DORA, HTTP pair |
| Findings table | every row has frame numbers + mechanism sentence |
| Prediction | written pre-verification; matches observed frames or explains the miss |
| Answers | cite fields (txid, option numbers, seq values), not vibes |

## 15. Grading Rubric

| Criterion | Weight | Full-credit behavior |
|---|---|---|
| Evidence discipline | 40% | frame-number citations; pre-registered prediction |
| Mechanism accuracy | 30% | correct field-level explanations (seq roles, DORA options) |
| Analysis depth | 20% | Q2/Q4 nuance (what encryption does/doesn't fix; reassembly limits) |
| Safety & policy | 10% | range/dataset-only analysis; originals preserved |

## 16. Instructor Answer Key

Model answers, per-station grading notes, common errors:
`teaching/lab-answer-keys/lab-02-answer-key.md` (instructor-only).
