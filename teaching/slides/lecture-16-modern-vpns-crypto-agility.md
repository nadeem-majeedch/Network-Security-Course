---
marp: true
theme: default
paginate: true
lecture: L16
week: 8
clos: [CLO-5, CLO-7]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# Modern VPNs & Crypto Agility

**Network Security · Lecture 16 · Week 8**

*From tunnels to access models — and keeping the crypto replaceable.*

<!-- notes: OPEN (2 min). Hook: "The tunnel was never the point. The
*authorized access* was. Today we separate them." -->

---

## Learning Objectives

1. **Contrast** network-level VPN access with per-app access models
2. **Evaluate** WireGuard's design choices (minimalism, modern crypto)
3. **Design** the identity-over-network access shift (ZT seeds)
4. **Explain** crypto agility as a *lifecycle* requirement
5. **Map** PQ migration as an agility exercise (cs-053's frame)

<!-- notes: (1 min) Objective 3 is the module-8 capstone seed; say so.
Midterm covers through L16 — flag D2's scenario. -->

---

## The Access Model Shift

| | VPN-centric | Access-centric (ZTNA) |
|---|---|---|
| Unit | network segment | *application* |
| Identity | device on net | user + device + context, per request |
| Blast radius | whole reachable net | one app's policy |
| Failure | flat inner network | per-app policy gaps |

<!-- notes: (5 min) The table frames L16's thesis. Quiz-8 Q4/Q5 planted
this; cs-093's phase design is the full expression. The VPN's honest
remaining niche: admin planes + legacy protocols. -->

---

## WireGuard: Modern Design, Briefly

- Crypto modern-only (Curve25519, ChaCha20-Poly1305, BLAKE2)
- Minimal codebase (~4k LOC vs IPsec stacks) — auditability as security
- Stateless key exchange per session; silent by default (no unauth
  responses)
- Tradeoff: no built-in identity/SSO layer — pair with an identity
  broker

<!-- notes: (6 min) Course accuracy rule: describe design *choices* and
tradeoffs, not marketing. The identity-broker gap is the honest limit —
cs-052's rollout case lives there. Quiz-9's modern-crypto pairings
apply. -->

---

## Identity as the Perimeter (Seeds of ZT)

- Access decisions move to: who + what device + what context
- The IdP becomes the policy root — and the single point of failure
  (cs-098's weakness statement rehearses this)
- Device posture: managed, patched, compliant — the second signal

<!-- notes: (5 min) The SPOF candor is deliberate: students who can
name their architecture's weakest dependency defend better (capstone
skill). cs-093's prerequisite chain starts here. -->

---

## Crypto Agility as Lifecycle

- Inventory: what algorithms live where (the "crypto bill of materials")
- Negotiate: protocols pick the strongest mutually supported suite
- Replace: rotate algorithms without redesign (TLS suites, WG's
  framework)
- Trigger: deprecation news, breaks, **PQ timelines**

<!-- notes: (5 min) cs-053's capstone case frames PQ as the agility
stress test: the inventory + swap discipline is the answer shape.
QB-013-adjacent reasoning transfers. -->

---

## Post-Quantum: The Honest Clock

- PQ algorithms standardized (ML-KEM family) — hybrid deployments
  beginning
- Threat: harvest-now-decrypt-later (long-lived secrets)
- Action: identify long-lifetime secrets, plan hybrid key exchange

<!-- notes: (5 min) Keep conceptual per accuracy rules: no algorithm
details beyond the standardization state. The HNDL phrase is the
urgency argument students will need. -->

---

## CS/DS Example: Per-Job Credentials for the Cluster

- VPN gives network; jobs need *scoped* identity: per-job tokens
- Broker issues short-lived creds per run (cs-088's fix, modernized)
- The cluster's access story: VPN for reachability + per-job auth for
  authorization

<!-- notes: (4 min) DS framing: reachability ≠ authorization — the two-
layer answer is the capstone's DS-cluster treatment. -->

---

## Activity: The Access Decision (6 min)

Three users need three things: researcher → dataset (bulk), contractor →
one report, admin → scheduler. Full tunnel? Split? App-brokered? Decide
each with one reason.

<!-- notes: (6 min) Answers: researcher = split with posture gate;
contractor = app-brokered (never network — assignment-3's answer);
admin = VPN + jump host + phishing-resistant MFA. The variance is the
point. -->

---

## Case Study: cs-051 (5 min)

- Split-tunnel risk debate — the honest middle

<!-- notes: (5 min) If cs-051 was used in L15's case slot, run cs-053
(PQ readiness) here instead — keep the case-index rotation rule. -->

---

## Formative Check

- Oral: one thing WireGuard deliberately omits, and why it matters
  operationally.

<!-- notes: (2 min) Exit oral: identity/SSO layer → broker pairing. -->

---

## References & Next

- WireGuard whitepaper (design reference); NIST PQ migration guidance
- Diagrams: `diagrams/06-vpn-ipsec-wireguard.md`
- **Next (L17):** wireless fundamentals — RF becomes an access layer
- **Midterm next session:** modules 1–4, use the review deck
