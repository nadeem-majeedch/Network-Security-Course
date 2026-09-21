---
case: cs-039
solution-for: modules/module-03-secure-architecture/case-studies/cs-039-nac-adoption-bypass-risks.md
difficulty: intermediate
module: 3
lecture-anchor: L12
clos: [CLO-3]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-039 Solution — 802.1X/NAC Adoption (INSTRUCTOR ONLY)

## Model Solution

**Auth policy per device class:**

| Class | Method | Role/VLAN result | Failure mode | Port enforcement |
|---|---|---|---|---|
| Managed PCs | **802.1X EAP-TLS** (certs via AD GPO) | corp role, full corp VLANs per policy | reject → **quarantine VLAN** (remediate + retry) | closed mode (no pre-auth) |
| Medical EAP-capable (30%) | EAP-TLS (client certs provisioned by clinical-eng process) | **medical role**: medical VLAN, egress allow-listed (pumps→monitoring, imaging→PACS), no lateral | auth-fail → **restricted-allow role + alarm** (never reject-and-blackhole) | closed mode with **no re-auth on success** (session persistence; periodic re-auth scheduled with clinical windows) |
| Medical MAB-only (50%) | **MAB** against inventory DB (serial→role mapping) | same medical role (narrower egress list) | MAB-miss (unknown MAC) → **quarantine-for-inventory VLAN** + ticket to clinical-eng — *not* a clinical outage: unknown medical device = procurement gap, and the device still "has network" for its clinical function within the restricted role if and only if whitelisted by vendor-port profile | closed mode |
| Medical unknown (20%) | **monitor-only phase**: open+audit role until classified | audit VLAN (full-ish egress, logged) | — | monitor mode → convert per findings |
| Guests | open SSID (no 802.1X on data ports for guests) | guest VLAN, internet-only | — | N/A (SSID-isolated) |
| BMS/doors | MAB + port-security (1 MAC, sticky) | bms VLAN, allow-listed egress only | miss → deny + alarm | closed mode |

**Three-phase adoption:**

1. **Assessment (6 wks):** switch readiness (dot1x capability audit), device
   census (probe+passive profiling), RADIUS cert pipeline design. *Exit:*
   inventory ≥95% classified; medical fleet's EAP/MAB split known.
2. **Monitor (8–12 wks):** ports in monitor mode (auth attempted, failures
   *logged not enforced*); profile mismatches reconciled weekly with
   clinical-eng. *Exit:* two consecutive weeks with <0.5% auth-failures on
   clinical ports and zero unexplained posture mismatches.
3. **Enforce (staged by building, never hospital-wide day-one):** start with
   admin buildings (managed PCs), then clinical per-floor with clinical-eng
   at the elbow. *Exit:* ongoing — enforcement is a steady state with
   exception workflow, not a project end.

**Medical-fleet special handling:** session persistence (no periodic
re-auth mid-shift), CoA (change-of-authorization) used *only* for quarantine
of confirmed-compromised devices with clinical-eng co-approval, and a
documented "clinical downtime" posture (NAC failure = fail-open for medical
roles with paging alarm — the network must fail *safe for patients*, and
fail-open-with-alarm is the risk-accepted answer, written down).

**Top-3 bypass risks + compensations:**

1. **MAB spoofing** (attacker reads a whitelisted pump MAC from a label/
   beacon, clones it): MAB proves nothing about identity. Compensation:
   MAB-ports get **port-security (1 MAC, sticky) + closed posture + role
   with minimal egress**; the spoofed device lands in a role that can do
   almost nothing (the win is *blast-radius*, not authentication). Also:
   physical security for clinical areas (the MAC is on the device).
2. **The never-authenticating port** (WAPs, cameras, printers behind
   unmanaged micro-switches, "it just works" exceptions): every exempt port
   is a permanent hole. Compensation: exceptions get **device-allowlist +
   port-security + scheduled re-validation** (quarterly), and the exception
   list is an audit artifact — count must trend to zero, not grow.
3. **Hub/handheld bridging** (one authenticated PC shares connectivity via
   hotspot/USB/mini-switch): NAC authenticates the *port*, not every MAC
   behind it. Compensation: port-security limits (1–2 MACs on user ports),
   802.1X on the *uplink-side* where possible, and egress profiling (the
   bridged device's traffic shows new fingerprints from the same port →
   CoA-quarantine the port).

## Alternative Solutions

- **Cloud/agent-based NAC for everything:** excellent for managed devices;
  the medical fleet's non-agent reality keeps network-layer 802.1X/MAB
  necessary — hybrid is the honest architecture.
- **Defer NAC; use microseg only:** segmentation limits lateral movement
  but doesn't answer "what can plug in" — the audit finding stands.
- **Reject-on-fail everywhere (strict):** maximally secure posture on
  paper; in a hospital, rejects on clinical ports are patient-safety events
  — the restricted-allow design is the professional answer.

## Tradeoffs

- Monitor-phase duration vs audit pressure: 8–12 weeks is the floor for a
  1,400-device fleet; going faster imports clinical outages that *end* NAC
  programs politically.
- Fail-open (medical) vs fail-closed (admin) per class: a single global
  failure policy is simpler and wrong here.
- MAB's inventory value vs its security emptiness: keep MAB *as inventory
  discipline* and say so to the auditor — pretending it's authentication
  invites the finding back.

## Common Mistakes

- Quarantining life-critical devices by default (clinical hazard).
- Treating MAB as authentication in the design narrative.
- Hospital-wide enforcement day ("big bang").
- No exception-list lifecycle — exceptions grow until NAC is folklore.

## Instructor Prompts

- "Which device class's *failure mode* is the riskiest design decision here?"
- "How does the pump-MAC-spoof attack fail *in practice*, given your roles?"
- "What does 'fail safe for patients' mean in your downtime posture?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Class-differentiated failure modes; patient-safety framing |
| Technical accuracy | 25% | EAP-TLS/MAB/CoA/port-security mechanics correct |
| Alternatives considered | 20% | Hybrid/strict options weighed |
| Communication | 15% | Phase table + bypass-risk list |

**Timing:** reveal at 5:00 + 2; "MAB is inventory, not identity" is the
sentence to remember.

## CLO Mapping

- **CLO-3** — NAC architecture under real-world device constraints.
