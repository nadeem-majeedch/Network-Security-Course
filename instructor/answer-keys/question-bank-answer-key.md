---
artifact-type: answer-key
instructor-only: true
distribution: never-publish-to-students
status: complete
questions: 50
---

# Question Bank — Instructor Answer Key

> **INSTRUCTOR ONLY.** Every answer verified against the module teaching
> plans and the linked case/lab evidence. Bloom levels and CLOs per question;
> totals guaranteed by generation script (`assessments/question-bank/generate_question_bank.py`).

## Summary counts

- Questions: 50 · Total marks: 100
- Bloom: Remember 7, Understand 6, Apply 7, Analyze 16, Evaluate 10, Create 4
- CLO: CLO-1 6, CLO-10 2, CLO-11 4, CLO-12 1, CLO-13 4, CLO-14 3, CLO-15 3, CLO-2 7, CLO-3 4, CLO-4 2, CLO-5 2, CLO-6 3, CLO-7 2, CLO-8 3, CLO-9 4
- Difficulty: beginner 14, intermediate 20, advanced 7, expert 9

## Answers & Rationales


### Module 1

**QB-001 — Answer: C** (1 mk, Remember, CLO-1, beginner)

Ports are L4 (transport) addressing.

**QB-002 — Answer: B** (1 mk, Understand, CLO-1, beginner)

Unsolicited replies are the ARP-poisoning vector.

**QB-003 — Answer: B** (2 mk, Apply, CLO-1, beginner)

TTL expires in transit → drop + ICMP Time Exceeded.

**QB-004 — Answer: B** (2 mk, Analyze, CLO-1, intermediate)

ARP is link-local broadcast; routers terminate broadcast domains.

**QB-005 — Answer: C** (2 mk, Analyze, CLO-1, intermediate)

SYN-ACK proves the port listened; RST then aborts — typical of backlog/reset defense or app failure.


### Module 2

**QB-006 — Answer: B** (1 mk, Remember, CLO-2, beginner)

MAC flooding overflows the CAM table.

**QB-007 — Answer: B** (1 mk, Understand, CLO-2, beginner)

Amplification = reply ≫ request with a spoofed source.

**QB-008 — Answer: B** (2 mk, Analyze, CLO-2, intermediate)

ARP poisoning inserts the attacker on the A↔gateway path.

**QB-009 — Answer: B** (2 mk, Evaluate, CLO-2, intermediate)

Snooping designates trusted DHCP sources; untrusted offers are dropped.

**QB-010 — Answer: B** (2 mk, Evaluate, CLO-2, expert)

Forged records with long TTL persist in caches until expiry.


### Module 3

**QB-011 — Answer: B** (1 mk, Remember, CLO-3, beginner)

Unmatched = denied by default.

**QB-012 — Answer: B** (1 mk, Understand, CLO-3, beginner)

DMZ = exposed-services segment between trust boundaries.

**QB-013 — Answer: B** (2 mk, Apply, CLO-3, intermediate)

Egress control breaks C2/exfil paths.

**QB-014 — Answer: B** (2 mk, Analyze, CLO-4, intermediate)

ZT evaluates identity+device+context continuously; NAC admits once.

**QB-015 — Answer: B** (2 mk, Evaluate, CLO-4, expert)

Traffic deltas reveal undocumented dependencies — the observe-then-enforce lesson.


### Module 4

**QB-016 — Answer: B** (1 mk, Remember, CLO-5, beginner)

AES = symmetric block cipher standard.

**QB-017 — Answer: B** (2 mk, Analyze, CLO-5, intermediate)

Keyed construction = integrity + origin authentication.

**QB-018 — Answer: B** (1 mk, Understand, CLO-6, beginner)

Certificates = signed identity↔key bindings.

**QB-019 — Answer: B** (2 mk, Apply, CLO-6, intermediate)

Expiry breaks the identity claim; warnings train users to click through.

**QB-020 — Answer: B** (2 mk, Analyze, CLO-7, intermediate)

Split tunneling leaves the local untrusted LAN in the trust path.

**QB-021 — Answer: B** (2 mk, Evaluate, CLO-7, expert)

PFS: new keys independent of long-term secret → past traffic stays sealed.


### Module 5

**QB-022 — Answer: B** (1 mk, Remember, CLO-8, beginner)

Supplicant ↔ authenticator ↔ RADIUS/AAA.

**QB-023 — Answer: B** (2 mk, Analyze, CLO-8, intermediate)

SAE's per-session derivation removes offline-verifiable handshake data.

**QB-024 — Answer: B** (2 mk, Apply, CLO-8, intermediate)

RF-domain threats need RF-side sensors.

**QB-025 — Answer: B** (1 mk, Understand, CLO-13, beginner)

SG = stateful, instance-attached, allow-only.

**QB-026 — Answer: B** (2 mk, Analyze, CLO-13, intermediate)

Attribution before action (cs-065 discipline).

**QB-027 — Answer: B** (2 mk, Evaluate, CLO-13, expert)

Egress default-deny = exfil containment + logged paths.


### Module 6

**QB-028 — Answer: B** (1 mk, Remember, CLO-9, beginner)

Signatures match known patterns only.

**QB-029 — Answer: B** (2 mk, Apply, CLO-9, intermediate)

High-entropy unique subdomain churn = DNS-tunnel signature.

**QB-030 — Answer: B** (2 mk, Analyze, CLO-9, intermediate)

Trust erosion compounds beyond raw triage minutes (cs-070).

**QB-031 — Answer: B** (1 mk, Understand, CLO-10, beginner)

In-host state = accurate findings.

**QB-032 — Answer: B** (2 mk, Evaluate, CLO-10, intermediate)

Environmental scoring: exposure × criticality beats base score alone.

**QB-033 — Answer: B** (2 mk, Evaluate, CLO-12, expert)

Local corroboration + provenance before action (cs-096 hunt discipline).


### Module 7

**QB-034 — Answer: B** (1 mk, Remember, CLO-11, beginner)

NIST SP 800-61 phase model.

**QB-035 — Answer: B** (2 mk, Apply, CLO-11, intermediate)

Error asymmetry justifies acting on single-source when costs are lopsided (cs-082).

**QB-036 — Answer: B** (2 mk, Analyze, CLO-11, intermediate)

Evidence preservation + neutralization in one step.

**QB-037 — Answer: B** (2 mk, Analyze, CLO-14, intermediate)

Stating the evidence boundary honestly (cs-087).

**QB-038 — Answer: B** (2 mk, Evaluate, CLO-14, expert)

Undocumented custody transfer breaks defensibility.

**QB-039 — Answer: B** (2 mk, Evaluate, CLO-15, expert)

Outcome metrics need sourced, reproducible provenance (cs-094).


### Module 3

**QB-040 — Model answer** (3 mk, Apply, CLO-3, intermediate)

MODEL: (1) permit tcp host 10.5.5.9 10.5.5.0/24 eq 22 — admin path; (2) deny tcp any 10.5.5.0/24 eq 22 log — others; (3) permit tcp any 10.5.5.0/24 established — returns; (implicit deny closes). Order matters: permit precedes deny (first-match); denies precede any broad permits.


### Module 1

**QB-041 — Model answer** (3 mk, Analyze, CLO-1, intermediate)

MODEL: ARP spoofing of the gateway. Effect: victims' caches map the gateway IP to the attacker MAC → traffic intercepts (MITM) or drops. Corroboration: DAI switch drops/logs; capture shows unsolicited reply bursts; duplicate IP/MAC flapping in switch logs.


### Module 2

**QB-042 — Model answer** (3 mk, Analyze, CLO-2, advanced)

MODEL: Flaw — unrestricted DMZ egress turns a compromise into a beaconing/exfil channel. Redesign: DMZ egress allow-list (update repos/CDN by FQDN or IP), deny+log the rest; optionally proxy updates through a controlled path.


### Module 6

**QB-043 — Model answer** (3 mk, Analyze, CLO-9, advanced)

MODEL: C2 beacon profile (fixed periodicity, low volume, off-hours). Detection: periodicity + low-byte + repeated-dst logic (e.g., N connections within jitter window). Next step: attribute the host — EDR process review / proxy SNI for the destination (which app made it).


### Module 7

**QB-044 — Model answer** (3 mk, Evaluate, CLO-11, advanced)

MODEL: (1) EDR isolate FS01 — reversible; (2) block staging domain (proxy+DNS) — reversible; (3) suspend new service/task (not delete) — reversible, preserves evidence; (4) then scope (backup generation check, other hosts) before any irreversible rebuild/restore. Preservation: suspend/don't delete; capture task/service definitions first.


### Module 8

**QB-045 — Model answer** (4 mk, Create, CLO-15, expert)

MODEL: (1) Phase 3 extends measured controls (2 apps, 98.5% decision success, ≤7% overhead) to the remaining concentration: branch + privileged access. (2) Deferral keeps location-trust on 12 sites and admin planes for another year while measured dwells run in days. (3) Evidence: phase-gate results, MTTD trend 34→9 days, tabletop findings — the method is proven, not promised.


### Module 4

**QB-046 — Model answer** (3 mk, Analyze, CLO-6, advanced)

MODEL: (1) Intermediate not served/missing on the leaf's chain (client can't build the path — most common); (2) intermediate revoked or its validity window violates client policy; (3) clock skew on the client. (Also acceptable: name constraints on the CA blocking the SAN.)


### Module 5

**QB-047 — Model answer** (3 mk, Create, CLO-13, advanced)

MODEL: NACL on DB subnet: deny inbound 3306 (and all) from 0.0.0.0/0; allow inbound 3306 only from app-subnet CIDR; ephemeral returns out. SG on DB: allow 3306 from app-SG only. Defense in depth: NACL is the backstop — a permissive SG alone cannot override the subnet-level deny.


### Module 7

**QB-048 — Model answer** (3 mk, Analyze, CLO-14, advanced)

MODEL: Offset = +3:30 (router ahead of true time). Proof: find a second event visible in both sources (e.g., session end), compute the same offset; or check against an NTP-disciplined reference. A single event pair is a hypothesis; two+ pairs corroborate.


### Module 2

**QB-049 — Model answer** (3 mk, Create, CLO-2, advanced)

MODEL: Top threat: passphrase harvest → offline crack/peer snooping (one secret for all). Compounding: no per-user identity → no accountability, rotation is network-wide. Fix: 802.1X/WPA2-Enterprise with RADIUS; tradeoff: identity infrastructure + device onboarding cost (plus guest network for BYOD convenience).


### Module 8

**QB-050 — Model answer** (4 mk, Create, CLO-15, expert)

MODEL SHAPE (graded on coherence, not wording): e.g., 'ARP is unauthenticated broadcast (fact) → management VLANs are segmented with DAI (design) → Zeek flags gratuitous-ARP bursts (detection) → the runbook contains by isolating the switch port and rotating the affected credentials, reversible-first (response).' Each link must name its module's mechanism.

