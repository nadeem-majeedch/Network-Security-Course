---
artifact-type: instructor-manual
status: complete
instructor-only: true
distribution: never-publish-to-students
---

# Demonstrations, Expected Difficulties & Misconception Bank

## 1. Teaching-demonstration index (by module)

Per-lecture demo details (including fallbacks) live in each speaker note
§Teaching Demonstrations. This index supports semester planning:

| Module | Signature demonstrations | Lab-range required |
|---|---|---|
| 1 (L01–L04) | Packet-capture anatomy walk (Wireshark/tcpdump); ARP exchange live; TCP handshake + teardown captured; DNS resolution path traced; HTTP/1.1 vs cleartext-vs-TLS comparison | Yes (passive capture only) |
| 2 (L05–L08) | Threat-model wall-walk (DFD on whiteboard); ARP-spoof detection from PCAP (recorded benign lab traffic); amplification arithmetic on real-shaped samples; DDoS decision-tree drill | Attack demos: recorded/benign-lab only |
| 3 (L09–L12) | Segmentation diagram build; firewall rulebase order demo (first-match wins); ACL direction demo (in vs out); NAT translation table walk | Config lab |
| 4 (L13–L16) | ECB penguin / mode-comparison demo; TLS handshake decode (keylog-decrypted, teaching-only); IPsec phase walk in lab tunnel; cert-chain validation walkthrough | Yes |
| 5 (L17–L20) | WPA2 handshake capture + passphrase-strength discussion (no cracking outside lab); SG-vs-NACL behavior demo in cloud sandbox; VPC flow-log read | Cloud sandbox + lab RF |
| 6 (L21–L24) | nfdump queries on prepared dataset; three live IDS rules with clean-corpus test; Zeek UID-join demo; authenticated-vs-unauthenticated scan diff | Scan lab, safe-mode |
| 7 (L25–L28) | Severity-calibration drill; three-way corroboration live; persistence-map walk; feed-scoring demo | Dataset-driven |
| 8 (L29–L32) | Chain-of-custody form walk; clock-skew normalization demo; capstone dry-run facilitation; defense question drill | Forensics dataset |

## 2. Expected student difficulties (by module)

**Module 1.** Encapsulation is abstract until they read frames themselves —
the L02/L03 sequence exists so the abstraction lands on captured evidence.
Tool-flooding risk: students play with Wireshark settings instead of reading;
the guided-capture sheets constrain this.

**Module 2.** Motivational whiplash: attack lectures generate enthusiasm that
can outrun ethics — the authorization statement is repeated at every demo and
enforced in grading (safety marks). Mechanism-vs-tool confusion: students
memorize tool names instead of protocol mechanisms; grading rejects tool-only
answers.

**Module 3.** Abstraction fatigue: architecture lectures feel "soft" after
attack lectures — anchor every design statement to a Module-2 attack it
prevents. Config-syntax drag in ACL/firewall labs: reference cards, not
lectures.

**Module 4.** Math anxiety: crypto lectures scare non-theory students — the
course teaches usage-discipline, not proofs; the "misuse beats math" sentence
is the reassurance. TLS-1.3 Wireshark blindness (encrypted handshake) needs
the keylog-file workaround explicitly taught.

**Module 5.** Cloud console overwhelm: the sandbox labs provide pinned paths
(console screenshots + CLI equivalents). Wireless hardware variance: lab
dongles are pinned; students' personal adapters are out of scope for support.

**Module 6.** Alert-overload disillusionment: students discover detection is
mostly tuning — this is the honest lesson; the tuning-workflow grade rewards
the discipline. Data-format drudgery: pinned parsers and provided schemas.

**Module 7.** Role-play discomfort: tabletop and drills feel theatrical —
the debrief reframes them as decision rehearsal. Time pressure in the guided
exercise: extended-clock accommodations exist (see `accessibility.md`); the
hard clock is also a graded design feature — say both out loud.

**Module 8.** Report-writing is the wall: forensic findings are easy,
findings-as-prose is hard — sentence templates and the model report structure
in L30 exist for this. Capstone scope creep: teams try to do everything; the
rubric rewards depth on fewer dimensions.

## 3. Misconception bank (course-wide, graded against)

The ten highest-value misconceptions, with the corrective move. (Per-module
banks with more entries are in each answer key's §Common misconceptions.)

1. **"Encryption = security."** Corrective: AEAD/authenticated modes or
   nothing; encryption without integrity/authentication is bypassable by an
   active attacker (L01 plants, L13 resolves).
2. **"NAT is a firewall."** Corrective: stateful filtering ≠ address
   translation; outbound-initiated connections traverse NAT freely (L03/L12).
3. **"HTTPS means the site is safe."** Corrective: TLS authenticates
   transport, not content or operator intent (L04/L14).
4. **"The firewall is the security boundary."** Corrective: one enforcement
   point among identity, endpoint, and east-west controls (L09/L10).
5. **"WPA2 is broken."** Corrective: the handshake capture enables offline
   *passphrase guessing* on weak passphrases; strong passphrases with WPA2/3
   remain sound (L17).
6. **"More alerts = better security."** Corrective: signal quality and tuning
   discipline beat volume; suppression-without-review manufactures blind
   spots (L22).
7. **"Scanner findings are a to-do list in score order."** Corrective:
   context stack (exploitation evidence, exposure, criticality) reorders the
   queue (L24).
8. **"Containment ends the incident."** Corrective: eradication, verified
   recovery, and lessons-learned are where incidents end (L27).
9. **"Forensics needs decryption."** Corrective: metadata analytics carry
   most network investigations; content access is separately gated (L30).
10. **"Zero trust is a product you buy."** Corrective: an architecture
    pattern — verify explicitly, least privilege, assume breach — realized in
    controls, procurement follows (L16/L09).

**Bank maintenance:** after each course run, append exit-ticket-derived
misconceptions with counts; the bank feeds the defense question drill (L32).
