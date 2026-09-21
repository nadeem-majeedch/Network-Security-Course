---
lab: Lab-02
status: complete
artifact-type: lab-answer-key
instructor-only: true
distribution: never-publish-to-students
---

# Answer Key — Lab-02 (Packet Capture & Protocol Analysis)

## Dataset ground truth (generated, seed 402)
54 packets, all IPv4: 2 DHCP DORA exchanges (xid 0x11220001/2, offered
10.20.0.101/.102, lease 3600 s, siaddr 10.20.0.1); 3×3 DNS A queries
(www0/1/2, updates, portal — TTL 300 answers to 10.20.30.53); 3 HTTP GET/200
pairs to 10.20.30.10:80 (`portal.lab.example`, UA `lab-client/1.0`, body 21
bytes, Content-Length exact); 1 TCP session to 198.51.100.9:123 with FIN/ACK
teardown (client closes first).

## Analysis-question model answers
1. **Seq numbers:** reorder and duplication below TCP; per-direction counters
   make reassembly deterministic. Reward "two failure modes" framing.
2. **DNS/UDP:** exposed = full query/response names, sizes, timing; DoT/DoH
   encrypt the channel but the *destination* choice and volume remain visible;
   switching to TCP alone changes nothing about visibility. Precision here is
   the L04/L14 bridge — grade it hard.
3. **Broadcast offers:** anyone on the segment can answer; DHCP snooping
   constrains by trusting only uplink ports (forward-ref L06/L12 accepted).
4. **Duplicate seqs:** Wireshark flags retransmissions; different-payload
   duplicates = malicious injection or middlebox artifacts — forensic
   ambiguity that tools cannot resolve; the analyst states the ambiguity
   (L29 rehearsal).
5. **Detection logic:** e.g., "src port 68 → 67 op=2 from non-DHCP-server IP"
   survives; "HTTP has Host header" is context-dependent (browsers always
   send it).

## Grading notes
- Prediction check (task 5): must be dated/pre-registered — reward honest
  misses with mechanism explanations over retro-fitted perfection.
- Frame citations required per finding; "somewhere in the file" fails the
  evidence dimension.
- Common errors: `dhcp` vs `bootp` filter; reading DNS answers in wrong txid
  order; claiming "server closed first" without reading FIN direction.

## Command status
✅ Dataset verified (54 pkts, IPv4 only) + checksums; the display filters are
syntax-checked shapes against Wireshark 4.x documentation (⚠️ not executed in
authoring env — no GUI available). Label accordingly in class.
