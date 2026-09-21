---
lab: Lab-08
title: Site-to-Site VPN Build & Evaluate
week: 8
module: 4
clos: [CLO-7]
lectures: [L15, L16]
duration: 2h (embedded in lecture block)
status: complete
artifact-type: student-lab-handout
instructor-key: teaching/lab-answer-keys/lab-08-answer-key.md
---

# Lab-08 — Site-to-Site VPN Build & Evaluate

## 1. Lab Overview & CLO Mapping

You will build a site-to-site tunnel between two lab "offices" (two pfSense
pairs or VM-router pairs on the range), then evaluate the design against the
L15/L16 criteria: trust model, key management, failure modes, and the
crypto-agility question. Midterm week — this lab is deliberately scoped to
finish in block. *CLO-7* — design and evaluate VPN solutions including trust
model, key management, and failure modes. Reference lectures: L15 (IPsec
architecture), L16 (modern VPNs, crypto agility).

## 2. Learning Objectives

By the end you can: (1) configure an IPsec site-to-site tunnel (IKEv2,
phase-1/phase-2 selectors) on lab routers; (2) verify tunnel state and traffic
encapsulation empirically; (3) break the tunnel in controlled ways and trace
each failure to its phase; (4) evaluate split vs full tunnel trade-offs for a
stated requirement; (5) write a VPN evaluation with trust-model and failure-mode
sections.

## 3. Prerequisites

Lab-07 submitted; L15/L16 attended; Lab-06's pfSense familiarity.

## 4. Estimated Duration

120 minutes: build 40 · verify 20 · controlled failure drills 30 · evaluation
write-up 30.

## 5. Required Software & Hardware

- Lab range: two pfSense (or Linux strongSwan) router VMs, two client VMs,
  subnet map on the lab sheet (Office-A 10.30.1.0/24 ↔ Office-B 10.30.2.0/24
  across a simulated WAN 192.0.2.0/24 — documentation ranges).

## 6. Setup Instructions

> **Command status:** ✅ verified at authoring time (strongSwan CLI shapes);
> ⚠️ = range/GUI steps, reference shape.

1. ⚠️ Snapshot both routers (`lab08-start`).
2. ⚠️ pfSense path: VPN → IPsec → add Phase 1 (IKEv2, IPv4, WAN-WAN, auth =
   pre-shared key *for the drill only* — the evaluation will critique it),
   then Phase 2 with local/remote subnets matching the map.
3. strongSwan reference shape (✅ syntax-verified at authoring time):

```bash
# /etc/ipsec.conf (Office-A)
conn office-b
  left=192.0.2.10            # A's WAN
  leftsubnet=10.30.1.0/24
  right=192.0.2.20           # B's WAN
  rightsubnet=10.30.2.0/24
  ike=aes256-sha256-modp2048!
  esp=aes256gcm16!
  keyexchange=ikev2
  auto=start
# /etc/ipsec.secrets: 192.0.2.10 192.0.2.20 : PSK "<issued-lab-psk>"
sudo ipsec restart && sudo ipsec status
# ✅ expected: 'office-b' INSTALLED after first interesting traffic
```

4. ⚠️ Firewall passes: allow UDP/500 + UDP/4500 (NAT-T) on both WANs; allow the
   tunneled subnets on the LAN sides.

## 7. Authorization & Safety Notes

- **Authorization basis:** the "WAN" and both offices are lab-range segments; only the issued routers and PSKs may be touched, and failure drills are limited to the three listed scripts.

- The "WAN" is a lab segment — nothing leaves the range. PSKs are issued per
  team and rotated at session end; treat them as real secrets anyway (the
  habit is the point).
- Failure drills are instructor-approved scripts only; no chaos beyond the
  listed three.

## 8. Student Tasks

1. **Build** the tunnel per the map; capture `ipsec status` / pfSense SA state.
2. **Verify encapsulation:** from Office-A client, ping Office-B client while
   capturing on the WAN segment: outer IPs = WAN addresses, inner = office
   subnets. Screenshot the ESP-encapsulated frames.
3. **Failure drills (document each):** (a) mismatch one side's phase-2 subnet
   → tunnel up, traffic dead — which phase and why; (b) block UDP/4500 → what
   happens with/without NAT-T; (c) change one side's PSK → phase-1 behavior
   observed in logs.
4. **Split vs full:** the brief says Office-B staff must *not* browse the
   internet through Office-A. Which tunneling policy implements that, and what
   monitoring does it require?
5. **Evaluate:** write the one-page evaluation: trust model (who can read
   traffic; where does trust concentrate), key management (PSK vs certs —
   recommend and justify for a 3-site deployment), failure modes (from your
   drills), crypto-agility (what breaks when AES-GCM→newer suite is mandated).

## 9. Expected Observations

- Phase 1 (IKE SA) establishes before phase 2 (child SAs) — the status output
  shows the hierarchy; drilling (a) proves phase-2 selectors are independent
  of phase-1 health.
- ESP frames on the WAN show only outer headers — payload invisible without
  the keys (your first "encryption works" observation).
- PSK mismatch: phase-1 negotiation fails with authentication errors in logs —
  and note *which* side learns what (a real design consideration).

## 10. Analysis Questions

1. Your drill (a) shows tunnel-up-but-traffic-dead. Why is this failure mode
   the most common in real deployments, and what change process catches it?
2. PSK vs certificate auth for your 3-site recommendation: what does each
   cost to operate at rotation time, and what does a leaked PSK vs a leaked
   cert key enable?
3. NAT-T wraps ESP in UDP/4500. Why does NAT break raw ESP, and what does the
   NAT-T negotiation actually detect?
4. Where does this tunnel *end* the zero-trust boundary? Once B's traffic
   arrives at A, what governs it (and which earlier-lab control applies)?
5. Crypto-agility: if a future standard deprecates modp2048, what exactly must
   change in your config, and how would you roll that across sites without
   downtime?

## 11. Troubleshooting

- `ipsec status` shows no INSTALLED → check phase-2 subnets *both sides* first
  (drill-a is also the top build error), then UDP/500 reachability.
- Tunnel up, no traffic → firewall on LAN side missing tunneled-subnet pass;
  also check forwarding/routing on the routers.
- pfSense logs "NO_PROPOSAL_CHOSEN" → IKE/ESP proposal mismatch between sides;
  align the cipher lines exactly.

## 12. Cleanup Instructions

- Revert both routers to `lab08-start` after sign-off; PSKs rotate at session
  end (instructor issues new ones); export your configs for submission first.

## 13. Submission Requirements

- Config exports (both sides) + SA-state screenshot.
- Encapsulation screenshot (ESP on WAN) with annotation.
- Failure-drill log (three drills: action · observed · phase attribution).
- One-page evaluation (trust model / key mgmt / failure modes / agility).
- Analysis answers (5). Due: end of session; midterm week — no extensions.

## 14. Expected Output & Evidence

| Artifact | Passing evidence |
|---|---|
| Configs | symmetric selectors; IKEv2; documented proposals |
| Encapsulation | outer/inner IPs labeled; ESP identified |
| Drill log | each failure attributed to its phase with log evidence |
| Evaluation | trust model + key-mgmt recommendation justified |

## 15. Grading Rubric

| Criterion | Weight | Full-credit behavior |
|---|---|---|
| Evidence discipline | 40% | drill log with log excerpts; screenshots annotated |
| Mechanism accuracy | 30% | phase separation, NAT-T, selector semantics correct |
| Analysis depth | 20% | trust-model + agility reasoning (Q2/Q4/Q5) |
| Safety & policy | 10% | PSK hygiene; range-only; snapshot discipline |

## 16. Instructor Answer Key

Reference configs, drill expected-outcomes table, grading notes:
`teaching/lab-answer-keys/lab-08-answer-key.md` (instructor-only).
