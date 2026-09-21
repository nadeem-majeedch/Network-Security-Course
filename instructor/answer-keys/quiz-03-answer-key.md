---
quiz: quiz-03
type: answer-key
instructor-only: true
distribution: never-publish-to-students
clos: [CLO-3, CLO-5]
marks: 15
status: complete
---

# Answer Key — Quiz 3 (Perimeter Controls & Crypto Foundations)

> **INSTRUCTOR ONLY.** Verified against L09–L13 teaching plans; ACL semantics
> per vendor documentation (Cisco extended ACL first-match + implicit deny).

## Section A — MCQ

| Q | Answer | Justification |
|---|---|---|
| 1 | **B** | Stateful inspection = connection table + reply validation; encryption is VPN/NGFW-optional, L7 is a proxy/NGFW feature, port ACLs are unrelated. |
| 2 | **B** | Top-down first match, implicit deny-all ends the list; longest-prefix is a *routing* concept. |
| 3 | **A** | Classic two-layer DMZ; the distractors collapse trust boundaries. |
| 4 | **B** | Symmetric = one shared key for both directions; A describes asymmetric, C signatures (asymmetric), D certificate distribution is for public keys. |
| 5 | **B** | Hashes verify integrity; they do not encrypt (A), sign by themselves (C — need a keyed construction), or exchange keys (D). |

**Section A total: 5**

## Section B — Short answer (model answers)

**Q6 (3 marks).** Encryption protects *confidentiality* (unreadable without
the key); authentication proves *who/what* you are talking to (identity
verification); integrity protection detects *modification* (tamper
evidence). Hashing alone does not provide **authentication of origin** —
anyone can recompute a plain hash, so it cannot prove who produced the
message (that needs a keyed MAC or a signature).
*Grading: 1 per sentence; the "hashing alone" point is the discriminator —
students saying "hashing = encryption" cap at 2/3.*

**Q7 (3 marks).** (1) Attack tooling that scans/beacons on "any reachable
port" loses its easy paths — recon produces a shorter, noisier result;
(2) egress filtering breaks C2/exfil channels that rely on arbitrary
outbound ports/DNS-style tunnels, forcing attackers onto observed,
logged paths. Also credit: reduces accidental shadow services; shrinks
the lateral playbook. *(1.5 per reason, tied to attacker behavior)*

## Section C — ACL design (model answer)

```
! 1. Allow SSH from the jump host only
permit tcp host 10.99.0.10 host 10.99.0.0/24-eq-22 eq 22    ! admin path
! 2. Deny all other inbound management ports, logged
deny   tcp any 10.99.0.0/24 eq 22 log                        ! other SSH: deny+log
deny   tcp any 10.99.0.0/24 eq 443 log                       ! other mgmt: deny+log (example)
deny   udp any 10.99.0.0/24 eq 161 log                       ! SNMP: deny+log (example)
! 3. Allow established return traffic
permit tcp any 10.99.0.0/24 established                      ! session replies
! implicit deny all
```

**Model rubric (4 marks):**
- Correct first rule with host scoping to the jump host *(1)*
- Explicit deny-with-log for other management traffic before any broad
  permits *(1)*
- `established` return rule positioned after the denies *(1)*
- Order argument: first-match-wins means the jump-host permit must precede
  the deny rules, and denies must precede any broad permit; implicit deny
  closes the list *(1)*

**Total: 15**

## Grading notes

- ACL pseudocode is acceptable; syntax errors are not penalized if match
  logic (src/dst/port/order) is right.
- Watch the misconception "implicit deny makes rule 1 redundant" — it
  inverts first-match-wins; cap Q8 at 2/4 if that claim appears.
