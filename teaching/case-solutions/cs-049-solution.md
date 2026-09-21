---
case: cs-049
solution-for: modules/module-04-crypto-protocols/case-studies/cs-049-ike-phase-negotiation-failure-diagnosis.md
difficulty: advanced
module: 4
lecture-anchor: L15
clos: [CLO-7]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-049 Solution — IKE Negotiation Failure (INSTRUCTOR ONLY)

## Model Solution

**The three distinct failures:**

| # | Failure | Revealing log line | Corrected parameter |
|---|---|---|---|
| 1 | **Protocol version mismatch** — you initiate IKEv2; partner is IKEv1-only | `SA-INIT → partner:500 (no response)` ×2 — v2 packets *silently dropped* by the v1-only appliance | Initiate **IKEv1** to this partner (or partner upgrades — not this week) |
| 2 | **Phase-1 proposal mismatch** | `NO_PROPOSAL_CHOSEN` after your main-mode attempt; partner debug names it | Match partner standard: **3DES-SHA1, DH group 2, lifetime 86400** — i.e., you adopt their archaic spec *or* negotiate an exception; this asymmetry (your AES-256 spec vs their 3DES standard) is the real finding of the case |
| 3 | **NAT + main-mode + PSK incompatibility** | `NAT detected, main mode + PSK unsupported` — NAT-D payloads expose the translated addresses | One of: **aggressive mode** (works with PSK+NAT but exposes identities — bad for a bank) or **certificate auth** (main mode survives NAT: identity isn't PSK-derived) — or eliminate NAT (below) |

**NAT + main-mode + PSK mechanics:** main mode protects identities by
encrypting identity payloads — but with **pre-shared keys**, the responder
must *find* the PSK before decrypting, and its lookup key is the peer's IP
address. NAT rewrites the source IP, so the responder looks up the PSK by
the CGNAT address, finds nothing (or the wrong PSK), and authentication
fails structurally — not a bug, a design property. Aggressive mode sends
identity in the clear (so ID-based PSK lookup works) at the cost of
identity exposure and (historically) faster offline PSK guessing.
**Pick for a bank: certificates** — main mode's identity protection is the
point with a bank partner; if the partner's appliance can't do certs, the
fallback is aggressive mode *with a long random PSK* documented as a
residual risk, or better: **eliminate the NAT** — the carrier uplink's CGNAT
is your side's problem; a static IP upgrade removes failure #3 wholesale
and is the cleanest fix in the whole incident.

**Corrected proposal sheet:**

| Parameter | Value | Note |
|---|---|---|
| IKE version | IKEv1 (partner-bound) | revisit at partner refresh |
| Phase 1 | 3DES-SHA1, DH2, 86400s (or negotiated exception: AES-256/SHA-256/DH14) | partner standard vs your spec — escalate the gap |
| Auth | **Certificates** (main mode intact) | PSK only if certs impossible; then aggressive mode + long PSK + risk note |
| NAT-T | enabled, port 4500 | needed even after NAT removal? harmless if yes |
| Phase 2 (CHILD_SA) | settlement ↔ partner subnets, ESP AES (per final phase-1 outcome) | TCP-only expectation is a *routing* matter, not IPsec's |
| Lifetime (P2) | partner-aligned | rekey storms otherwise |
| DPD | on, 30s | CGNAT bindings time out |

**The debugging habit (one sentence):** *get the responder's log first* —
your side's `NO_PROPOSAL_CHOSEN` names no parameter, but the partner's
log names every mismatch; an hour of joint-log reading replaces a day of
config archaeology.

## Alternative Solutions

- **Push the partner to IKEv2:** the correct *strategic* answer (their
  standard is a legacy finding in itself); fails this week's settlement
  deadline — name it as the roadmap item with the risk note on 3DES/DH2.
- **Aggressive mode + PSK immediately:** fastest to green; wrong for a
  bank (identity exposure + PSK-guessing surface) — the case grades the
  judgment, not the speed.
- **Static IP / remove NAT:** the quiet structural fix that deletes one
  failure class — often the cheapest real answer.

## Tradeoffs

- Adopting 3DES/DH2 vs negotiation delay: settlement traffic on legacy
  crypto is a *risk acceptance* — document it with an expiry tied to the
  partner's platform refresh.
- Certificates vs PSK ops cost: certs need PKI ops on both sides; with a
  bank, that investment is justified once, forever.

## Common Mistakes

- Treating it as "one config error" — three layers failed in sequence.
- Fixing proposals without addressing NAT (tunnel still fails).
- Choosing aggressive mode without naming its cost.
- Proposal sheet without lifetimes/DPD (the rekey-storm follow-up ticket).

## Instructor Prompts

- "Why does PSK lookup care about the peer's *IP* at all?"
- "Which failure would survive if you fixed only #1 and #2?"
- "What does the 2-year-old spec sheet teach about VPN documentation?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Three-layer sequence; NAT/PSK main-mode mechanics |
| Technical accuracy | 25% | IKEv1/v2, NAT-D, mode tradeoffs correct |
| Alternatives considered | 20% | Cert-vs-PSK vs NAT-removal judgment |
| Communication | 15% | Proposal sheet PM-ready |

**Timing:** reveal at 5:00 + 2; "responder's log first" is the habit to
install.

## CLO Mapping

- **CLO-7** — IPsec/IKE negotiation mechanics and structured diagnosis.
