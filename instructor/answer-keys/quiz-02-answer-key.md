---
quiz: quiz-02
type: answer-key
instructor-only: true
distribution: never-publish-to-students
clos: [CLO-2]
marks: 15
status: complete
---

# Answer Key — Quiz 2 (Threat Mechanics)

> **INSTRUCTOR ONLY.** Verified against L05–L08 teaching plans; attack
> mechanics per standard references (RFC 1024-era DNS cache behavior is
> covered in L03/L07; amplification per US-CERT TA14-017A style guidance).

## Section A — MCQ

| Q | Answer | Justification |
|---|---|---|
| 1 | **B** | Public records/CT logs involve no traffic toward the target; A, C, D all touch target infrastructure. |
| 2 | **A** | MAC flooding exhausts the switch MAC table → fail-open flooding; B is ARP spoofing, C is VLAN hopping, D is ARP cache poisoning. |
| 3 | **B** | Cache poisoning = resolver accepts/caches inauthentic response; DNS is not encrypted by default (A false); queries are unicast (C false); zone transfers are optional/configured (D false). |
| 4 | **A** | Reflection amplification = reply ≫ request to a spoofed source; the other options are irrelevant to the mechanism. |
| 5 | **B** | Starvation = pool exhaustion; redirection comes from the *rogue-server* variant, not starvation itself. |

**Section A total: 5**

## Section B — Short answer (model answers)

**Q6 (3 marks).**
(a) Hub/wireless: attacker sees all traffic in the broadcast/RF domain —
frames are physically repeated to every port; control: wireless encryption
(WPA2/WPA3-Enterprise), hub elimination/switching. *(1.5)*
(b) Switched wired: attacker sees only broadcast/unicast-flooded traffic
unless they poison ARP/MAC tables to redirect or force flooding; control:
Dynamic ARP Inspection, port security, limiting flood behavior. *(1.5)*

**Q7 (3 marks).** The attacker sends SYNs with a spoofed source and never
answers SYN-ACKs; the target holds half-open state until its backlog
expires — memory/table exhaustion denies new connections. Mitigations:
host — SYN cookies/backlog tuning; network — upstream filtering (BCP 38
source validation), rate limiting/syn-flood protections on firewalls/CDN.
*(1 mechanism, 1 host, 1 network)*

## Section C — Scenario

**Q8.**
(a) **ARP spoofing** (redirection to attacker, then proxying/modifying the
intranet response) and **DNS spoofing on-path** (forged replies after
redirection) — either order accepted; also accept "rogue DHCP + DNS
redirect" if argued via the same workstation. *(2)*
(b) Corroboration: switch logs show the workstation MAC flapping gateway
identity / DAI drops; capture shows unsolicited ARP replies or forged DNS
responses with the workstation's MAC as responder. *(2 — 1 per attack)*

**Total: 15**

## Grading notes

- Q6: full credit requires both contexts *and* a control each; the classic
  misconception to catch is "switches broadcast everything" — award max 1/3
  if that claim appears.
- Q8: students who answer "MITM" without naming the enabling L2 mechanism
  earn max 1/2 in (a).
