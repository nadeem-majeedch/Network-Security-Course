---
quiz: quiz-04
type: answer-key
instructor-only: true
distribution: never-publish-to-students
clos: [CLO-8, CLO-13]
marks: 15
status: complete
---

# Answer Key — Quiz 4 (Wireless & Cloud Network Security)

> **INSTRUCTOR ONLY.** Verified against L17–L20 teaching plans; WPA3 SAE
> per Wi-Fi Alliance/IEEE 802.11 materials; cloud constructs per public
> provider documentation (SG stateful allow-only; NACL stateless subnet).

## Section A — MCQ

| Q | Answer | Justification |
|---|---|---|
| 1 | **B** | WPA3's SAE replaces PSK's offline-guessable handshake with per-attempt derivation — the structural fix, not parameter tuning. |
| 2 | **B** | The authenticator (AP/switch) relays EAPoL ↔ RADIUS; DHCP/CA/accounting are not EAP relays. |
| 3 | **A** | SGs are stateful, attached to instances, allow-only; B describes network ACLs. |
| 4 | **B** | RF-domain threats (rogue AP/evil twin) are invisible to wired sensors; the others are wired/cloud-visible. |
| 5 | **B** | Split tunneling lets remote-network traffic bypass the tunnel — the untrusted LAN shares the path; MTU/firewall distractors are operational, not trust, issues. |

**Section A total: 5**

## Section B — Short answer (model answers)

**Q6 (3 marks).** SG: **stateful** (return traffic auto-allowed), attached
to instances, default **deny inbound/allow outbound** (typical), allow
rules only. NACL: **stateless** (both directions need explicit rules),
subnet-scoped, numbered **allow *and* deny** rules, default allows within
the VPC. Incident-monitoring difference: NACL deny counters give a cheap
subnet-level tripwire; SG changes are API-audited, so watch the audit log
— a change to an SG is itself an incident signal. *(1 state+scope, 1
default posture, 1 monitoring)*

**Q7 (3 marks).** Enterprise wins: (1) **per-user credentials** — one
stolen shared PSK compromises everyone, and offboarding/rotation is
account-level not network-wide; (2) **central auth + accounting**
(RADIUS) — identity-based access, logs per user, policy per group.
Cost: infrastructure/identity integration (AAA + certificate or credential
management), plus per-site server dependencies — a real ops burden.
*(1, 1, 1)*

## Section C — Scenario

**Q8.**
(a) Verify: (1) **attribution first** — enumerate installed agents/update
services on the instance and match destination/CA to a legitimate vendor
(check vendor-published endpoint), then (2) **behavior comparison** —
compare volume/destination history in flow logs vs the agent's documented
pattern and peer instances. Only then judge. *(2)*
(b) Control: an **egress-control construct at the subnet/edge** (NACL or
egress-only firewall/route-table change) containing without touching the
instance; fastest attribution: **VPC flow logs** (destination, port,
volume, timestamps) cross-checked with instance identity. *(2)*

**Total: 15**

## Grading notes

- Q6: accept provider-specific variants if the *stateful vs stateless*
  distinction is exact; that distinction is the graded core.
- Q8: students who jump to "block it" without the verification step lose
  (a) — the quiz is testing verification discipline, matching cs-065.
