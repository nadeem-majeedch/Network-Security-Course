# Lab-01 — Lab-Range Orientation, Baseline & Topology Documentation

## 1. Lab Overview & CLO Mapping

You cannot defend a network you have not documented. This lab establishes the
course's working environment and produces the **security baseline** every later
lab measures against. *CLO-1* — explain core protocols and identify their
security-relevant properties. Reference lectures: L01 (mindset, assets), L02
(Ethernet/IP mechanics you will draw).

## 2. Learning Objectives

By the end you can: (1) connect to the lab range and verify tool versions;
(2) enumerate and document lab hosts, addressing, and services into a topology
diagram; (3) capture a first packet set and relate observed frames to your
diagram; (4) state the range's authorization boundary in your own words.

## 3. Prerequisites

L01 attended; syllabus §9 ethics policy read and lab rules sheet signed.
No prior Wireshark experience required (Lab-02 develops it).

## 4. Estimated Duration

120 minutes: orientation 20 · documentation 45 · first capture 35 · review 20.

## 5. Required Software & Hardware

- Lab-range VM image (instructor-provided; includes Wireshark, tcpdump, Python 3.11+).
- Your signed lab rules sheet (paper or PDF).
- No personal adapters or outside networks — range only.

## 6. Setup Instructions

> **Command status:** ✅ = executed and verified against the generated course
> datasets at authoring time; ⚠️ = untested in the authoring environment,
> provided as a reference shape verified against official tool documentation.

1. ⚠️ Boot the range VM and log in with the issued credentials.
2. ⚠️ Verify tools: `wireshark --version`, `tcpdump --version`, `python --version` — record versions in your notebook (version drift is the #1 lab failure).
3. ✅ Regenerate the course datasets (also your first evidence-integrity practice):

```bash
python docs/labs/setup/generate_lab_datasets.py
cd docs/labs/datasets && sha256sum -c SHA256SUMS   # ✅ verified: all OK
```

4. ⚠️ Ping each range host the instructor lists; note which respond (this is *authorized* — they are course targets).

## 7. Authorization & Safety Notes

- Every target in this lab is lab-owned; the instructor's host list **is** the authorization boundary. Nothing outside it may be probed — not your neighbor's laptop, not the campus network, not the internet.
- Capture only on the range's virtual interfaces.
- This course's safety marks are real marks (manual §2): state the boundary in your report.

## 8. Student Tasks

1. Draw the range topology: hosts, subnets, gateways, services (draw.io or paper photo). Mark **trust boundaries** (internet↔range, user net↔server net) and justify each.
2. Build a baseline table: host, IP/MAC, OS guess (from TTL behavior), open services found, who can reach it.
3. Capture 2 minutes on the range interface while a neighbor pings your host and fetches the range web page; save `baseline-first-capture.pcapng`.
4. In the capture, find: one ARP exchange, one ICMP echo, one TCP 3-way handshake. Note frame numbers.
5. Write the baseline paragraph: "Normal for this range looks like…" (≥3 quantitative anchors: hosts seen, protocols seen, broadcast rate).

## 9. Expected Observations

- ARP requests broadcast (ff:ff:ff:ff:ff:ff), replies unicast — your L02 reading confirmed on your own wire.
- ICMP echo request/reply pairs symmetric; TTLs matching the host table.
- The handshake: SYN → SYN/ACK → ACK with per-direction sequence numbers.
- Broadcasts (ARP, DHCP if lease renewals occur) dominate background noise — your first "what is normal" data point.

## 10. Analysis Questions

1. Why do ARP requests broadcast but ARP replies unicast? What attack does that asymmetry enable (name the trust assumption)?
2. Your topology has at least two trust boundaries — what control would you place at each, and what traffic would it inspect?
3. Which host had the lowest TTL in replies, and why does that suggest hop distance rather than OS (why is TTL-as-OS-guess unreliable)?
4. The baseline paragraph is the seed of detection engineering (L21). What would you *not* see if you only captured 30 seconds instead of 2 minutes?
5. State the authorization boundary of this lab and one consequence of exceeding it.

## 11. Troubleshooting

- `sha256sum` mismatch → regenerate and re-verify; never analyze from unverified files (report the incident in your submission — that's evidence discipline, not failure).
- Wireshark shows no interfaces in the VM → run as the issued user, check virtual adapter is up (`ip a` / `ipconfig`).
- No handshake visible → neighbor's fetch didn't cross your capture point; re-run while the fetch is in flight; note the capture filter used.

## 12. Cleanup Instructions

- Remove capture files from shared folders; keep your own copy for the submission.
- Log out of the range VM; leave the VM running (instructor reverts snapshots).
- Return the signed rules sheet if paper.

## 13. Submission Requirements

- Topology diagram (image or PDF) with trust boundaries labeled.
- Baseline table (CSV or Markdown).
- `baseline-first-capture.pcapng` + the baseline paragraph.
- Answers to the 5 analysis questions with cited frame numbers.
- Due: start of Week 2 session.

## 14. Expected Output & Evidence

| Artifact | Passing evidence |
|---|---|
| Diagram | ≥2 subnets, gateway, ≥3 hosts, ≥2 labeled trust boundaries |
| Table | all enumerated hosts, MAC+IP, ≥1 service each |
| Capture | contains ARP + ICMP + TCP handshake; file opens cleanly |
| Paragraph | ≥3 quantitative anchors, references its own capture |
| Answers | frame numbers cited for every claim |

## 15. Grading Rubric

| Criterion | Weight | Full-credit behavior |
|---|---|---|
| Evidence discipline | 40% | frame numbers cited; capture matches claims; quantitative anchors |
| Mechanism accuracy | 30% | protocol-level explanations (ARP asymmetry, TTL, handshake) |
| Analysis depth | 20% | trust-boundary reasoning; limits of observations stated |
| Safety & policy | 10% | boundary stated; rules sheet signed; range-only actions |

## 16. Instructor Answer Key

Model answers, grading notes, and common failure modes:
`the instructor answer-key collection (not published)` (instructor-only distribution).
