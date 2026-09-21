---
lab: Lab-15
status: complete
artifact-type: lab-answer-key
instructor-only: true
distribution: never-publish-to-students
---

# Answer Key — Lab-15 (Forensic Timeline & Findings Report)

## Ground-truth event table (seed 415 corpus)
| # | Phase | Events | Evidence |
|---|---|---|---|
| 1 | Background | user DNS+HTTP to portal | baseline context |
| 2 | Recon | 5 one-way SYNs 10.20.0.66→10.20.30.10 (22/80/443/445/3389), ~0.4 s apart | conn-level frames |
| 3 | Beacon | 24 TXT queries 10.20.0.102→resolver, 30 s cadence, 26-char base32 labels | dns frames |
| 4 | Exfil-shaped | 6 POSTs 10.20.0.102→198.51.100.9, ~120 s cadence, 64-B bodies | http frames |
| 5 | Background tail | continued portal traffic | context |

## Skew arithmetic (the graded drill)
Sensor clock +90 s fast → all sensor timestamps subtract 90 s. Beacon window
measured [T_s, T_e] sensor-time becomes [T_s−90, T_e−90] true-time; with a
~12-min active window, the shift materially reorders events against DNS-server-
sourced timestamps (which are correct) — uncorrected, beacon frames appear to
*precede* the scan that enabled them: the impossible narrative the brief
warns about. Students must show the subtraction and the corrected window.

## IOC exemplar (grading anchor)
| Value | Type | Context | Conf | Expiry/condition | Destination |
|---|---|---|---|---|---|
| 198.51.100.9 | IP | exfil POST dest | high (direct frames) | 90 d review | egress blocklist |
| *.cdn-metrics.example (26-char base32 labels) | qname pattern | beacon | high (24 obs) | pattern + 30 d | DNS RPZ + detection rule |
| 10.20.0.66, 10.20.0.102 | internal | scan src / beacon+exfil host | high | until remediated | IR ticket (not blocklist) |

Bare-IP lists without context/expiry lose the precision marks; internal IPs
destined for "blocklists" is the collateral-risk trap (Q3).

## Report exemplar skeleton (grading anchor)
- Exec (≤150 words): what (staged intrusion: recon→beacon→data-shaped POSTs),
  impact (one host, TEST-NET evidence), decisions (contain .102, block two
  externals, notify?), status (analysis-only; plan attached). No acronyms.
- Analyst: method (hashes, copy-only, skew-corrected), exhibits (E1 pcap +
  frame refs), timeline table, IOC table, limitations (30-min window, no host
  telemetry, no payload visibility), recommendations (prioritized: isolate,
  block, hunt for other beacons, add detection rule).

## Analysis-question model answers (pointers)
1. Second hash proves the *analysis process* didn't alter the exhibit —
   custody survives analysis, not just acquisition.
2. Real-case additions: host logs (process/persistence), NetFlow (window
   extension), DHCP/DNS server logs (identity mapping) — confidence improves
   first on *identity* of actors.
3. Don't block: the resolver-adjacent pattern (collateral risk to legit TXT
   users) — push to detection-rule instead; IOC automation lacks context.
4. Missing host telemetry would change: eradication scope (persistence
   unknown) — the exec decision shifts from "contain" to "contain + rebuild".
5. Defensible: "activity pattern consistent with automated beaconing;
   attribution not established." Not defensible: any named actor.

## Grading notes
- Custody record append-only with both hash checks + times = evidence spine.
- Peer exhibit-test log: what failed to reproduce is diagnostic gold — collect
  the failure list for next-semester timeline drills.
- ✅ Hash/custody/timeline shapes executed at authoring (dataset + python).

## Command status
✅ sha256/cp/python shapes executed; ⚠️ Wireshark CSV export is a GUI shape.
