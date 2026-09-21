---
lab: Lab-08
status: complete
artifact-type: lab-answer-key
instructor-only: true
distribution: never-publish-to-students
---

# Answer Key — Lab-08 (Site-to-Site VPN Build & Evaluate)

## Reference config (strongSwan shape; pfSense equivalent accepted)
Symmetric phase-2 selectors both sides (10.30.1.0/24 ↔ 10.30.2.0/24); IKEv2;
explicit IKE/ESP proposals identical both ends; UDP/500+4500 passed on WANs;
LAN passes for tunneled subnets. Verification: `ipsec status` → INSTALLED;
ESP frames on the WAN with outer 192.0.2.x/inner 10.30.x labeling.

## Controlled-drill expected outcomes (grading anchor)
| Drill | Expected observation | Phase attribution |
|---|---|---|
| (a) mismatch one side's phase-2 subnet | IKE SA stays up; traffic blackholes; logs show TS_UNACCEPTABLE / no child SA | Phase 2 (selectors), phase 1 healthy |
| (b) block UDP/4500 | with NAT-T needed: no NAT-T → raw ESP fails across the simulated NAT; negotiation falls back/fails | transport/encoding, not crypto |
| (c) PSK mismatch on one side | phase-1 auth failure in logs; both sides see failure (information asymmetry is itself discussable) | Phase 1 authentication |

## Analysis-question model answers
1. **Selector drift:** subnets change with re-addressing; docs rot; the change
   process that catches it: deployment checklists with peer-verified selectors
   + post-change traffic tests (the drill *is* the checklist).
2. **PSK vs certs @3 sites:** PSK rotation = n(n−1)/2 secrets to coordinate
   (3 sites → 3 PSKs, all on rotation day, all-or-nothing revocation); certs =
   per-site identity, revocation is per-cert, but needs CA ops (Lab-07 skills).
   A leaked PSK = impersonate any site; a leaked cert key = that site only
   until revoked. Recommendation: certs at 3+ sites; PSK acceptable for 2.
3. **NAT-T:** NAT rewrites IPs/ports → TCP-checksum-style ESP auth breaks and
   port-500 flows confuse; NAT-T detects NAT presence (vendor-ID/NO_PPOBE
   path) and encapsulates ESP in UDP/4500.
4. **Tunnel end ≠ trust end:** decrypted B-traffic at A is governed by A's
   segmentation/ACLs (Lab-05/Lab-06) — the zero-trust boundary re-asserts
   *inside* the decryptor; flat trust behind the tunnel is the classic failure.
5. **Agility:** swap ike/esp lines to the new suite with overlap windows
   (two proposals during migration, then prune); document rollback; at scale
   this is config-as-code with staged rollout (L16's crypto-agility made
   operational).

## Grading notes
- Drill log needs *log excerpts* per drill, not conclusions — phase
  attribution with evidence is the 30% mechanism dimension.
- The evaluation's trust-model section: full credit names where trust
  concentrates (the gateways + the CA/PSK store) and the blast radius of each.
- Common build errors: selector asymmetry (drill-a as build bug), missing
  LAN-side passes, forgetting 4500.

## Command status
✅ strongSwan ipsec.conf/status shapes verified at authoring; ⚠️ pfSense GUI
and range topology steps are environment steps.
