---
marp: true
theme: default
paginate: true
lecture: L15
week: 8
clos: [CLO-7]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# IPsec & Legacy VPN Architecture

**Network Security · Lecture 15 · Week 8**

*Tunnels: networks trusting networks, proven cryptographically.*

<!-- notes: OPEN (2 min). Hook: "Module 4's pattern — hybrid crypto —
becomes architecture this week." -->

---

## Learning Objectives

1. **Differentiate** transport vs tunnel mode by what they protect
2. **Walk** the IKE two-phase negotiation and its failure modes
3. **Design** a site-to-site IPsec deployment (selectors, PFS, lifetime)
4. **Assess** split-tunnel trust honestly
5. **Position** legacy VPNs in the modern access architecture

![bg right:34% fit](diagrams/06-vpn-ipsec-wireguard.md)

<!-- notes: (1 min) Diagram 06 taught here. Objective 3 is Lab-08's
design task; objective 4 is assignment-3's graded risk argument. -->

---

## Two Modes, Two Protections

- **Transport**: protect payload only (host-to-host, gateway-to-gateway
  control traffic)
- **Tunnel**: protect the *entire* inner packet — new outer header
  (gateway-to-gateway sites)
- Quiz shortcut: tunnel = whole packet; transport = payload

<!-- notes: (4 min) Quiz-9 Q4's exact answer. Diagram 06's packet story
shows tunnel mode's encapsulation. -->

---

## IKE: The Negotiation Dance

- Phase 1: gateways authenticate each other (certs or PSK) → secure
  channel
- Phase 2: negotiate the traffic *selectors* (what subnets/ports ride
  the tunnel)
- Failure modes: PSK mismatch, selector mismatch, NAT-traversal gaps

<!-- notes: (6 min) cs-049's negotiation-failure case is the diagnostic
story: read the IKE logs, find the mismatched selector. The NAT-T note
previews cloud deployments. -->

---

## Site-to-Site Design Decisions

| Decision | Options | Guidance |
|---|---|---|
| Authentication | certs vs PSK | certs scale; PSK is a shared secret |
| PFS | on/off | on: new keys per rekey, old traffic sealed |
| Lifetimes | phase timers | shorter = smaller blast window |
| Selectors | subnets/ports | least necessary traffic |

<!-- notes: (6 min) cs-050's design case walks this table. The PFS row
is quiz-9's expert question (QB-021): past traffic stays sealed if the
long-term key later leaks. -->

---

## Split Tunnel: The Honest Risk

- Full tunnel: all traffic through corporate — control, visibility,
  cost
- Split: only corporate ranges tunnel — efficient, but the *local*
  untrusted network shares the device's trust path
- Mitigations: device posture checks, MDM, browser-isolation for the
  risky class

<!-- notes: (6 min) Assignment-3's graded argument is this slide.
cs-051's case is the tradeoff debate. The unmanaged-device row is where
the honesty lives. -->

---

## Legacy VPNs: What They Still Do Well

- Network-level access for legacy protocols that can't do per-app auth
- Site-to-site links (the inter-org glue)
- The straight answer: VPNs aren't wrong — they're *network-scoped*

<!-- notes: (4 min) The course's honest-technology stance: legacy ≠
bad; scope ≠ principle. L16 adds the modern overlay; cs-093's phase-3
positions VPNs in the admin-plane niche. -->

---

## CS/DS Example: The Research VPN

- Cluster access for off-site researchers: VPN + per-job credentials
  (L16's ZT seed)
- Split-tunnel for data transfer performance + device posture gates

<!-- notes: (3 min) DS framing: researchers move datasets; performance
vs control tension is real — the posture-gate compromise is the
defensible middle. -->

---

## Activity: Diagnose the Dead Tunnel (6 min)

Given IKE logs: Phase 1 completes; Phase 2 fails with selector mismatch
(10.2.0.0/16 vs 10.2.9.0/24). Find it, propose the fix, state who
verifies.

<!-- notes: (6 min) Lab-08's seeded fault. The fix is a config change
on *both* ends — the "who verifies" answer is the operational maturity
marker. -->

---

## Case Study: cs-052 (5 min)

- WireGuard rollout for remote staff — modern alternative evaluation

<!-- notes: (5 min) The case pairs with L16's modern-VPN lecture;
today it's the evaluation-discipline practice. -->

---

## Formative Check

- Oral: what does tunnel mode protect that transport doesn't? Why is
  PSK the weaker Phase-1 choice?

<!-- notes: (2 min) Exit oral — both are examinable (quiz 9, QB-021). -->

---

## References & Next

- RFC 4301/7296 (IPsec/IKEv2)
- Diagrams: `diagrams/06-vpn-ipsec-wireguard.md`
- **Next (L16):** modern VPNs & crypto agility — ZTNB vs tunnel
