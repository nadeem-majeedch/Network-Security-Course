---
case: cs-050
solution-for: modules/module-04-crypto-protocols/case-studies/cs-050-site-to-site-ipsec-design-between-two-sites.md
difficulty: advanced
module: 4
lecture-anchor: L15
clos: [CLO-7]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-050 Solution — Site-to-Site IPsec (INSTRUCTOR ONLY)

## Model Solution

**Architecture table:**

| Element | Design | Why |
|---|---|---|
| Tunnels | **Route-based VTI pair per ISP path**: VTI-1 over ISP-1, VTI-2 over ISP-2, both sites | route-based = dynamic routing decides path; policy-based can't fail over cleanly (selector-based, not route-based) |
| Phase 1 | IKEv2, AES-256-GCM (or 256-CBC+SHA-384 where GCM off-accel), DH group 19/20, lifetime 8h, DPD 30s | modern floor; short P1 lifetime + DPD for CGNAT/ISP churn |
| Phase 2 | AES-256-GCM, **PFS on (DH19)**, lifetime 1h, anti-replay default | PFS: sync traffic worth re-keying; 1h caps exposure per SA |
| Routing/failover | eBGP or BFD-tracked static across VTIs; ISP-1 preferred (local-pref), ISP-2 backup; failover <10 s with BFD | automatic, testable; no client-side awareness needed |
| QoS | DSCP marking **pre-encryption**, ESP honors ToS byte (copy outer), shaping per-class on egress | ESP strips ports (P2 selectors host-based mitigate) but copies ToS — per-class shaping works; per-flow shaping inside ESP does not |

**OT-isolation guarantee (structural):**

- Phase-2 selectors are **host-narrow**: engineering-jumphosts ↔ R&D-jump;
  sync-cluster ↔ R&D-cluster; **historian-replica → R&D-replica
  (unidirectional by selector + firewall)**. No selector contains OT VLAN
  ranges — a PLC *cannot* form an SA to R&D even if routing went wrong.
- Defense in depth at FW-A: OT zones → tunnel interface: **deny** (log);
  the one permitted flow is the historian's *replica push* — allowed as
  **historian-host → replica-host on the replica protocol only**, with the
  R&D side's return path constrained to the replica service (stateful
  reply). OT initiation remains structurally impossible: no selector +
  explicit deny + logged.
- Auditability: the selector table *is* the audit artifact — narrow,
  named, versioned.

**Deterministic performance:**

- **MTU/MSS arithmetic:** ISP path 1500; VTI over ISP-1 (ESP: +~73 B for
  AES-GCM/ESN-less ≈ IPsec overhead 73–76) → inner MTU ≈ 1424; the sync
  path is *one* encapsulation (VTI), not double — set inner MTU 1400 +
  MSS-clamp 1360 (safety margin); if any overlay-on-overlay appears
  (e.g., carrier L2oIP), recompute: subtract each encapsulation's overhead.
  PMTUD: allow ICMP 3/4 through the tunnel path (cs-004's lesson) — black
  holes here look like "slow sync," not errors.
- **Sync-window design:** nightly 200 GB at ~1 Gbps effective ≈ 35 min;
  schedule off-peak, rate-shape to 60% of ISP-1 (leave headroom for the
  jump-host interactivity), rsync-style delta sync to shrink the 200 GB to
  the nightly delta (usually 10–20 GB → 3–4 min). Determinism comes from
  *scheduling + shaping*, not raw bandwidth.
- Replica pull: rate-limit to 100 Mbps constant — predictable by design.

## Alternative Solutions

- **Policy-based IPsec:** familiar to OT teams; fails the failover
  requirement (selectors can't track route state) and scales poorly —
  rejected with the reason stated.
- **SD-WAN overlay instead of raw IPsec:** tempting (built-in failover);
  adds a product and op-model for two sites — fine if the org standardizes,
  overkill for a pair.
- **Separate small tunnel for historian replica:** cleaner audit story but
  another P1/P2 to operate — the host-narrow selectors achieve the same
  guarantee in one tunnel.

## Tradeoffs

- Narrow selectors (secure, more SAs) vs subnet selectors (simple, broad):
  the isolation requirement decides — narrow wins; keep a selector-name
  convention so the table stays readable.
- PFS every rekey vs CPU cost: hardware accel makes PFS cheap; on the
  OT-side's small firewall, PFS DH19 every hour is still trivial — no
  reason to disable.
- ISP-2 backup adequacy: 100 Mbps carries jump-host + throttled replica
  during outages; sync jobs *pause* (failover ≠ full capacity) — document
  the degraded-mode expectation.

## Common Mistakes

- Policy-based tunnels + "failover" wishes (mechanism mismatch).
- Subnet-wide selectors including OT ranges "for simplicity" — the
  isolation guarantee dies.
- MTU guesswork (black-hole PMTUD) instead of arithmetic.
- QoS after encryption (DSCP lost/ignored) instead of pre-encapsulation
  marking + ToS copy.

## Instructor Prompts

- "Which single design choice makes OT→R&D initiation *impossible* rather
  than prohibited?"
- "Walk the 1500-byte packet through your design — where does it fragment
  if MSS clamping is missing?"
- "What does the audit artifact for 'one-way replication' look like?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Structural isolation via selectors; route-based failover logic |
| Technical accuracy | 25% | P1/P2 params, MTU arithmetic, DSCP-over-ESP reality |
| Alternatives considered | 20% | Policy-based/SD-WAN rejection reasons |
| Communication | 15% | Architecture table as deliverable |

**Timing:** reveal at 5:00 + 2; the MTU walk-through is the quantitative
anchor.

## CLO Mapping

- **CLO-7** — Site-to-site IPsec architecture engineering.
