# Lab-03 — Layer-2 Attack Evidence Analysis (ARP/DHCP)

## 1. Lab Overview & CLO Mapping

L06 taught the mechanisms; this lab reads them from evidence. You will detect
and document an **ARP sweep, ARP cache poisoning, and DHCP starvation + rogue
server offers** inside a prepared capture, then map each finding to the exact
protocol trust gap it exploits and the control that closes it. *CLO-2* —
classify network threats and map each to the protocol layer and position it
exploits. Reference lectures: L05 (threat anatomy), L06 (L2 attacks).

## 2. Learning Objectives

By the end you can: (1) recognize ARP scanning and poisoning in frame-level
evidence; (2) recognize DHCP starvation and rogue-offer patterns; (3) attribute
each attack to its exploited trust assumption; (4) name and justify the matching
mitigation (DAI+DHCP snooping, port security, rogue-server detection); (5)
write a finding in evidence→claim→recommendation form.

## 3. Prerequisites

Lab-02 submitted; L06 attended; dataset verified (§6).

## 4. Estimated Duration

120 minutes: verification 5 · discovery hunt 45 · control mapping 35 ·
findings write-up 35.

## 5. Required Software & Hardware

- Lab-range VM with Wireshark ≥ 4.0, Python 3.11+.
- Dataset: `docs/labs/datasets/lab03-l2-attacks.pcap` (54 packets).

## 6. Setup Instructions

> **Command status:** ✅ verified at authoring time; ⚠️ reference shape.

1. ✅ Verify: `cd docs/labs/datasets && sha256sum -c SHA256SUMS`
2. ⚠️ Open the capture; starter filters:

```
arp                                    # all ARP traffic
arp.opcode == 1                        # requests (who-has)
arp.opcode == 2                        # replies (is-at)
bootp.option[53] == 1                  # DHCP Discover
bootp.option[53] == 2                  # DHCP Offer
arp.src.proto_ipv4 == 10.20.0.1        # frames claiming the gateway IP
```

## 7. Authorization & Safety Notes

- **Authorization basis:** all analysis is confined to the instructor-authorized lab range and the pinned course datasets; anything outside that boundary is prohibited.

- Analysis of prepared evidence only. Do **not** reproduce these attacks on the
  range outside instructor-run demonstrations — L2 spoofing frames leak beyond
  your VM and can disrupt other students' labs; that is a policy incident.
- Your writeup must state what was *not* done (no active attacks by students) —
  the evidence-discipline habit of bounding claims.

## 8. Student Tasks

1. **ARP sweep:** identify the scanning host (IP+MAC), count probes, describe
   pacing. Is a sweep itself harmful? What does it *precede*?
2. **ARP poisoning:** find the unsolicited replies claiming 10.20.0.1. Record
   the attacker MAC, victims targeted, and reply count. Then find the victim
   HTTP session that follows and explain where its frames went (which MAC).
3. **DHCP starvation:** count Discover bursts and the spoofed client MACs.
   Record the offered addresses and the *server* identity in the offers — who
   is offering, and why is that the smoking gun?
4. **Timeline:** build a 6-row event table (time offset · event · frames ·
   interpretation) covering all three attack phases.
5. **Control mapping:** for each attack, name the control, where it enforces
   (switch port? DHCP trust boundary?), and what it checks (e.g., DAI validates
   ARP against the snooping binding table).
6. Write three findings in the form: *observed evidence (frames) → assessed
   activity → recommended control + where to verify it*.

## 9. Expected Observations

- Sweep: ~12 who-has frames from 10.20.0.66, mostly unreplied, fast cadence.
- Poisoning: 6+ is-at replies binding 10.20.0.1 → attacker MAC 02:00:55:55:aa:aa,
  addressed to two victim MACs (gratuitous-style, unrequested).
- The victim's subsequent HTTP SYN exits toward the *attacker* MAC while IP
  dst remains the gateway — the MITM pivot visible at L2.
- Starvation: 8 Discover bursts from 02:00:55:55:dd:XX, then 8 Offers claiming
  10.20.0.200 from the *attacker* IP, not the real DHCP server.

## 10. Analysis Questions

1. Why is an ARP *reply* trusted without a matching request? Name the protocol
   assumption and one legitimate use of unsolicited replies (gratuitous ARP)
   that complicates naive filtering.
2. DAI needs DHCP snooping's binding table. What breaks on ports where hosts
   use static IPs — and what's the professional fallback?
3. If the rogue DHCP server had offered *correct-looking* options except its
   own DNS pointer, what would users experience, and why is that worse than
   pool exhaustion?
4. Which of these attacks survives IPv6 (and in what form — name the NDP
   equivalent), and which control family answers it?
5. Your capture starts *after* the poisoning began. What can you still claim,
   and what can't you — how do you phrase that limit in a report?

## 11. Troubleshooting

- Filter shows nothing → case-sensitive field names (`bootp.option`), or
  you're filtering on a capture (not display) level.
- "Poisoning" looks like normal gratuitous ARP → count and targets differ:
  repeated unicast-to-victims replies claiming the *gateway* is the tell.
- Two servers in offers → cross-check siaddr/option-54; the real server is
  10.20.0.1, the rogue is 10.20.0.66.

## 12. Cleanup Instructions

- Export annotated copy; remove scratch files; VM logout. Original dataset
  stays read-only with its SHA256SUMS intact.

## 13. Submission Requirements

- `lab03-annotated.pcapng` with the three attack phases marked.
- 6-row event timeline table.
- Control-mapping table (attack → control → enforcement point → verification).
- Three findings (evidence → claim → recommendation).
- Analysis answers (5) with frame citations. Due: start of Week 4 session.

## 14. Expected Output & Evidence

| Artifact | Passing evidence |
|---|---|
| Annotated capture | all three phases bookmarked; attacker/victim MACs labeled |
| Timeline | offsets + frames + interpretation, no gaps claimed beyond evidence |
| Control mapping | controls named at the right layer (DAI/snooping ≠ "a firewall") |
| Findings | every claim traceable to frames; recommendations include verification |

## 15. Grading Rubric

| Criterion | Weight | Full-credit behavior |
|---|---|---|
| Evidence discipline | 40% | frame citations; explicit limits (capture-window bias) |
| Mechanism accuracy | 30% | trust-gap attribution per attack (L05/L06 vocabulary) |
| Analysis depth | 20% | Q1/Q2/Q4 nuance (gratuitous ARP, static-IP fallback, NDP) |
| Safety & policy | 10% | stated no-active-attacks; dataset-only work |

## 16. Instructor Answer Key

Model answers, findings exemplars, common misattributions:
`the instructor answer-key collection (not published)` (instructor-only).
