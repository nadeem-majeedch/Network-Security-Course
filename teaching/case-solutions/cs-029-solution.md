---
case: cs-029
solution-for: modules/module-03-secure-architecture/case-studies/cs-029-microsegmentation-data-center.md
difficulty: intermediate
module: 3
lecture-anchor: L09
clos: [CLO-3]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-029 Solution — Microsegmentation (INSTRUCTOR ONLY)

## Model Solution

**Policy model — labels (≥6):**

| Label | Meaning | Examples |
|---|---|---|
| `tier:web` | user-facing front ends | web tier |
| `tier:app` | business logic | app tier |
| `tier:db` | databases | DB tier |
| `pci:in-scope` | CDE (cardholder data environment) | payment cluster |
| `function:batch` | analytics/batch jobs | batch group |
| `function:tooling` | internal tools | tools group |
| `vendor:msp-A/B/C` | managed-service access identity | 3 MSPs |
| `env:prod/stage` | environment fence | prod/stage |

**Default policy:** **deny all east-west**; allow only listed
`source → dest, service`. Exceptions named, not implied.

**Four example rules (no IPs):**

| Source | Dest | Service |
|---|---|---|
| `tier:web` | `tier:app` | app port (e.g., 8443) |
| `tier:app` | `tier:db` | db port (5432/3306) |
| `function:batch` | `tier:db` | read-replica port, read-only account |
| `vendor:msp-B` + `env:prod` | `tier:app` | SSH via bastion tag only |

(Plus env fence: nothing crosses `env:prod ↔ env:stage`.)

**Enforcement points:**

| Criterion | Distributed hypervisor firewall | Central FW/SDN gateway |
|---|---|---|
| Granularity | **Per-VM, tag-native** — policy follows the workload (live-migration-safe, autoscale-safe) | Per-segment; tags must be re-derived as network constructs |
| Failure mode | Fail-open (hypervisor default) if mgmt plane dies → must pin fail-closed for CDE; policy *engine* outage ≠ data-plane outage | Single box: fail-closed blocks everything; fail-open is disaster |
| Ops cost | Rule sprawl risk (400 VMs × policies) — needs label hygiene + tooling | Familiar ops, but every flow hairpins through the gateway — throughput + latency tax |

**Pick: distributed hypervisor firewall**, with (a) tag hygiene owned by SRE
via IaC (labels assigned at VM provisioning, not by hand), (b)
fail-closed pinned for `pci:in-scope`, (c) central FW retained for
north-south. Justification: 400 VMs with autoscaling make network-address
policy a maintenance treadmill; the estate already virtualizes on a
platform that can do tag-native policy — using it converts the pen test's
"shouldn't exist" paths into structural impossibilities.

**Prod-safe rollout:**

1. **Monitor-only (4–6 weeks):** enable distributed FW in log-only, export
   flow logs, build the *observed* flow matrix per label pair; reconcile
   weekly with app owners; expect surprises (backup jobs, agent update
   servers, NTP, DNS).
2. **Ring order (enforcement):** `tier:db` **first** (narrow deterministic
   flows, highest value) → `pci:in-scope` (with a change-freeze rehearsal)
   → `tier:app` → `function:batch` → `tier:web` → `function:tooling` last
   (most heterogeneous, human-driven, widest flows).
3. **PCI special treatment:** CDE gets fail-closed + its own policy
   namespace; every allow rule gets an owner + expiry review; auditors get
   the policy export as the scope-control evidence — this *shrinks PCI
   scope* by cutting non-CDE paths into the cluster.

## Alternative Solutions

- **Central-gateway-only first (later distributed):** lower initial learning
  curve; but you pay the hairpin tax forever on east-west — acceptable only
  if the platform's distributed feature is unavailable.
- **Host-firewall-only (no NSX):** works but 400 hosts of drift risk without
  central policy compute; the tag model exists precisely to avoid that.
- **Segment-of-one for PCI only (no broader rollout):** tempting minimalism;
  solves the audit question but leaves the payroll/web→DB paths — the pen
  test's actual finding — unresolved.

## Tradeoffs

- Deny-by-default vs allow-by-default start: deny-default from day one of
  *log-only* mode costs nothing and prevents matrix gaming.
- Label taxonomy breadth: 8 labels is enough; 20 becomes unmaintainable —
  labels are a schema, not free text.
- MSP vendor access: fold into tags + bastion-only paths or they become the
  permanent exception that voids the model.

## Common Mistakes

- Rules with IPs "just to start" — the estate *changes*; IP rules rot in
  months.
- Enforcing web tier first (most variable flows, max breakage).
- Forgetting agent/backup/NTP infrastructure flows — the classic day-2
  outage trio.
- No fail-mode decision documented for the CDE.

## Instructor Prompts

- "A live-migrated VM changes hosts mid-policy. What happens to its rules
  in each enforcement model?"
- "Which observed-flow surprise broke your last rollout story?"
- "How does this project *shrink* PCI scope rather than just satisfy it?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Tag-native model; failure-mode-driven enforcement choice |
| Technical accuracy | 25% | Label/service rules coherent; fail-open/closed semantics |
| Alternatives considered | 20% | Gateway/host-FW options honestly weighed |
| Communication | 15% | Policy table + rollout rings readable |

**Timing:** reveal at 5:00 + 2; the live-migration prompt is the decisive
mental model.

## CLO Mapping

- **CLO-3** — Identity-based microsegmentation design.
