---
case: cs-066
solution-for: modules/module-06-detection-vulnerability/case-studies/cs-066-sensor-placement-plan-for-an-enterprise-edge.md
difficulty: advanced
module: 6
lecture-anchor: L21
clos: [CLO-12]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-066 Solution — Sensor Placement (INSTRUCTOR ONLY)

## Model Solution

**Placement plan (8 sensors):**

| Chokepoint | Sensors | Load math | What it detects |
|---|---|---|---|
| A: DC-1 core | **3** (filtered view) | 40 Gbps raw; after exclusions ≈ 5–6 Gbps analyzed (see math) — 2 Gbps/sensor × 3 = 6 Gbps | lateral movement (SMB/WinRM/RDP anomalies), data-staging (server-to-server volume shifts), protocol abuse, DC-resident C2 |
| B: DC-2 core | **1** (filtered) | 25 Gbps raw → ~4 Gbps after exclusions; replication-class traffic dominates and is *baselinable*, not needful of full inspection | DR-site lateral, replication abuse (exfil disguised as backup traffic) |
| C: HQ internet edge | **2** (full view — highest threat density) | 6 Gbps → per-sensor 3 Gbps; near capacity → same exclusions as DC | C2 beaconing, drive-by/exploit-kit patterns, exfil-to-internet, VPN abuse, DNS-tunneling |
| E: Cloud VPC egress | **1** (flow-analytics, not packet) | 3 Gbps; cloud mirror-agent costs more than value → flow-log analytics + Zeek-on-logs where feasible | workload egress anomalies (cs-065), cloud C2, cost-attack class |
| G: OOB/management plane | **1** (full capture — cheap at 0.1 Gbps) | trivial volume | admin-plane abuse: credential use anomalies, lateral to BMCs, shadow-admin |

**Volume math for A (the graded core):** 40 Gbps raw cannot fit 3
sensors (6 Gbps capacity) — the *only* honest play is reduction:

| Exclusion | Bytes saved | Blindness cost |
|---|---|---|
| Replication/backup flows (known hosts, known ports, known window) | ~40–50% | backup-window abuse invisible at A — compensated by B's sensor + volume baselines |
| Streaming/media + CDN fetches from server VLANs | ~10–15% | low; server media use is anomalous by definition (alert on the *attempt*) |
| Encrypted-to-known-SaaS from *user* VLANs traversing DC | ~15% | TLS content already invisible; keep SNI/metadata — small real loss |
| Patch/mirror traffic (pinned endpoints) | ~5% | low |

Result: ≈5–6 Gbps of *decision-relevant* traffic on 3 sensors at ~90%
sustained — tight but honest; the exclusion table *is* the design
artifact (each row's blindness is named and compensated, not waved).

**Residual blind spots + compensation:**

| Blind spot | Compensation |
|---|---|
| Branch *local* traffic (never backhauls — e.g., branch-to-branch printers/local NAS) | branch switch flow export to SIEM (cheap, metadata-level); accept no packet view |
| Cloud *east-west* inside VPC (sensor sees only egress) | cloud flow logs + agent-based telemetry (EDR) in cloud hosts |
| TLS content everywhere (by design) | SNI/DNS/JA3-class metadata from sensors + EDR process context |
| F (HQ→DC WAN) unmonitored | deliberate: duplicates A∪C views; if a sensor frees up later, F is next in line — state the priority queue |

## Alternative Solutions

- **Unfiltered sensors at A/B (buy 12):** the honest answer if budget
  allowed; with 8, filtering is the engineering — but *name* that the
  right long-term ask is 12.
- **All 8 on the internet edge:** maximum per-packet threat density but
  zero east-west (where dwell time happens) — the coverage-graph trap.
- **Skip G, add F:** WAN links see the same conversations A and C
  already see (transit, not origin); G's admin-plane value dominates.

## Tradeoffs

- Filtered depth vs unfiltered breadth: exclusions are permanent
  decisions — review quarterly (the excluded classes drift).
- Packet sensors at C vs flow-only: C's 6 Gbps on 2 sensors is the
  plan's tightest fit; a third sensor here would force dropping G —
  edge is worth it (threat density), G stays.
- Cloud mirror-agent cost vs flow-analytics: egress anomalies (the
  actual cloud threat per cs-065) are *volumetric* — flow analytics
  suffice; packet-level cloud capture buys little extra here.

## Common Mistakes

- Dividing raw Gbps by sensor capacity without a reduction strategy (the
  math must be shown, exclusions named).
- Missing that D backhauls *through* A (branch traffic is already in
  A's view — D sensors duplicate).
- No blind-spot table (an audit reads the plan as over-claiming).
- Forgetting the management plane (the highest-value-per-byte purchase).

## Instructor Prompts

- "Which exclusion row would you fight hardest to keep, and why?"
- "Show the math that kills D from the list."
- "What does the G-sensor see in week one that no other sensor can?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Value×visibility logic; reduction math with named costs |
| Technical accuracy | 25% | SPAN/tap/flow mechanics; sensor capacity realism |
| Alternatives considered | 20% | 12-sensor ask, edge-only, F-vs-G tradeoff |
| Communication | 15% | Plan + exclusion table + blind spots |

**Timing:** reveal at 5:00 + 10; the exclusion table is the artifact to
emulate.

## CLO Mapping

- **CLO-12** — Monitoring architecture and coverage engineering.
