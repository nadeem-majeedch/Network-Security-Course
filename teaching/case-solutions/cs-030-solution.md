---
case: cs-030
solution-for: modules/module-03-secure-architecture/case-studies/cs-030-branch-firewall-placement.md
difficulty: intermediate
module: 3
lecture-anchor: L10
clos: [CLO-3, CLO-4]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-030 Solution — Branch Firewall Placement (INSTRUCTOR ONLY)

## Model Solution

**Comparison:**

| Criterion | Per-branch edge FW | DC-only FW | Cloud/SASE-delivered |
|---|---|---|---|
| PCI segmentation (POS↔guest/cameras) | **Enforceable locally** — the flows are intra-branch | ❌ Cannot see local flows; DC FW never touches POS↔guest — segmentation is *unprovable* | Partial: enforces WAN/cloud paths, **not** local L2 unless a CPE sits in-branch anyway |
| Guest local internet | Stays local, cheap | Must hairpin to DC (bandwidth cost, latency) | Breaks out locally via CPE/cloud POP — good |
| Branch autonomy in WAN outage | **Full** (local policy stands) | Store segments collapse or default-open — worst case | Depends on CPE fallback policy; designable |
| Ops burden (3 staff) | Historically high — **unless zero-touch + central policy** (template-managed) | Lowest device count, but no local enforcement | Lowest ops if truly cloud-managed; CPE still exists |

**Verdict: hybrid — per-branch CPE firewall running centrally-pushed
templates (zero-touch), with cloud/SASE management plane** and DC-only or
SASE handling *north-south* inspection. Reasoning: the compliance-critical
flows are *local* to the store, so enforcement must live in-branch
(eliminates DC-only); 3 staff cannot hand-manage 40 boxes, so the management
plane must be central with template policy and zero-touch provisioning
(eliminates artisanal edge firewalls); SASE alone without an in-branch CPE
cannot evidence POS↔guest segmentation (eliminates pure cloud).

**Minimum per-branch policy set (placement-proof, 5 rules):**

| # | Rule | Why it survives placements |
|---|---|---|
| 1 | POS VLAN → POS backends (DC) on app ports only | PCI data path, explicit |
| 2 | Guest Wi-Fi → internet only (no → POS, cameras, back-office) | The segmentation rule — enforceable at any in-branch enforcement point |
| 3 | Cameras → NVR/DC only; no internet | Camera-phone-home discipline |
| 4 | Back-office PC → DC management + vendor update list; no → POS | Admin path without lateral trust |
| 5 | Everything else: **deny + log**, with guest as the only exception zone | Default-deny is the evidence the auditor wants |

Wherever enforcement physically lives, these five *statements* define the
branch's policy; placement decides only *where they execute*.

## Alternative Solutions

- **DC-only:** cheapest device count; fails the PCI-enforceability test —
  the killer criterion; acceptable only if stores were rebuilt with
  host-based firewalls on POS (not this estate).
- **Pure SASE with light CPE:** the likely end-state as vendors mature; the
  CPE *is* the branch firewall — this converges with the hybrid verdict.
- **No firewalls, rely on 802.1X:** identity helps but PCI auditors want
  enforced segmentation with logs; NAC alone doesn't inspect or log flows.

## Tradeoffs

- Zero-touch central templates vs local flexibility: template discipline is
  the whole point; site exceptions go through change control, not SSH.
- Dual-carrier failover + fail-closed POS policy: during both-carrier
  outage, cash-only mode is *correct* — design the store's offline POS
  procedure alongside the firewall.
- Capex (CPE at 40 sites) vs risk: CPE refresh is the cost of enforceable
  segmentation; finance gets the audit-avoidance arithmetic.

## Common Mistakes

- Choosing DC-only because "firewalls are expensive at the edge" — misses
  that the flows needing control never leave the building.
- Policy set that names products/ports of one vendor (not placement-proof).
- Forgetting cameras (classic phone-home offenders in retail).
- No offline/failed-mode story for stores.

## Instructor Prompts

- "Which of the five rules is the auditor's favorite, and why?"
- "Where does guest traffic break out in your design — who cares, and why?"
- "If the SASE vendor has an outage, what do stores experience?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Local-flows-must-be-local-enforced insight |
| Technical accuracy | 25% | PCI segmentation logic; template/zero-touch ops model |
| Alternatives considered | 20% | All three placements honestly tabled |
| Communication | 15% | Verdict column + 5-rule policy set |

**Timing:** reveal at 5:00 + 2; "where must enforcement live" is the
takeaway sentence.

## CLO Mapping

- **CLO-3** — Enforcement placement in a multi-site design.
- **CLO-4** — Policy sets that survive placement choices.
