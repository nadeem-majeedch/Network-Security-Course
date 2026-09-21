---
case: cs-074
solution-for: modules/module-06-detection-vulnerability/case-studies/cs-074-asset-discovery-gaps-before-scanning.md
difficulty: advanced
module: 6
lecture-anchor: L24
clos: [CLO-10]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-074 Solution — Discovery Gaps Before Scanning (INSTRUCTOR ONLY)

## Model Solution

**Discovery-gap classes:**

| # | Gap class | Mechanism (what the scan misses) | Independent witness |
|---|---|---|---|
| 1 | **Cloud API-only assets** | instances without public IPs / behind cloud firewalls never answer network probes; autoscaled ephemerals live minutes | cloud-provider API (instance inventory, *authoritative*) |
| 2 | **Firewalled/stealthed on-prem hosts** | deny-all hosts drop probes; they exist, unscanned | EDR/agent fleet (a *host* witness), switch ARP/CAM tables (a *network* witness that sees without touching) |
| 3 | **Non-IP / weird devices** | serial/USB-attached, some OT and print infrastructure | asset-management integrations, physical/logical port maps |
| 4 | **Transient instances** | autoscaling appears/disappears between scan and report — the report is stale at birth | cloud API + configuration-drift detection, not point-in-time scans |
| 5 | **Off-network/roaming** | laptops on VPN/remote — no LAN presence | EDR fleet inventory (the only complete laptop witness) |
| 6 | **Shadow IT / unmanaged gear** | not in CMDB, maybe rogue-AP-bridged (cs-058) | passive traffic analysis (ARP/DHCP/mDNS census) + rogue-AP survey |
| 7 | **Stale CMDB entries (the inverse gap)** | *phantom* hosts inflate the count — scanning wastes slots and pollutes reports | reconciliation itself: CMDB-minus-witnesses = delete-list |

**Reconciliation table (this estate):**

| Host class | CMDB | Network scan | Cloud API | EDR | Passive (ARP/DHCP) | Expected delta story |
|---|---|---|---|---|---|---|
| On-prem servers (≈500) | ✓ | ✓ | — | ✓ | ✓ | consistent; deltas = firewalled ones (gap 2) |
| Cloud instances (300 claimed) | stale | ✗ (no route) | **✓ authoritative** | partial (agents on some) | — | API is the truth; CMDB is 8-mo fiction; autoscale makes it a *feed*, not a snapshot |
| Laptops (200) | ✓ | partial (on-LAN only) | — | **✓** | ✓ when on | EDR completes the roaming story |
| OT VLAN (PLCs/HMIs) | ✓ | **✗ by design (excluded)** | — | rarely | **✓** (passive only) | passive traffic + vendor docs = the *only* safe witness |
| Legacy embedded (medical-like) | ✓ | ✗ (excluded: crash history) | — | ✗ | ✓ | passive + vendor-certified agentless checks only |
| Shadow/contractor | ✗ | partial | — | ✗ | **✓** | passive census finds what nobody wrote down |
| Phantoms | ✓ | ✗ | — | ✗ | ✗ | CMDB-minus-everything → delete-list (report hygiene) |

The honest headline: **no single witness is complete; the union is the
inventory** — and the scan is one witness among five, not the
definition of coverage.

**Scan-safety plan:**

1. **Exclusions (hard):** OT VLAN and legacy-embedded VLAN are *never*
   port-scanned — witness = passive traffic + credentialed/agentless
   checks coordinated with OT engineering (vendor-certified methods
   only).
2. **Credentialed alternative:** for servers and cloud instances,
   credentialed scans (SSH/agent) replace network probing — deeper
   truth (package-level), zero port-sweep risk; cloud API-native
   assessment for instances.
3. **Rate/window controls:** scan windows off-peak, per-VLAN rate
   limits, no fragmentation/aggressive options on shared infra; print
   and IoT VLANs get the slowest profile or exclusion by crash history.
4. **The pre-flight item most teams skip — the crash-canary:** before
   the fleet run, execute the *exact scan profile* against a
   **deliberately chosen fragile-but-safe representative** — an old
   test printer / decommissioned embedded box in a test VLAN — and
   watch for hangs/crashes for 24 h. If the canary survives, the
   profile is *evidenced* safe for its class; if it dies, the profile
   is fixed before a production device teaches the lesson. (Choosing
   the canary: same OS/embedded class as the risk group, zero business
   function — the "crash it on purpose where it's cheap" principle.)

## Alternative Solutions

- **Scan-first, reconcile-later:** produces the classic "1,340 findings
  on 900 hosts, 200 duplicates, 3 crashed printers" report — the
  credibility tax; rejected.
- **EDR-as-the-only-inventory:** strong for endpoints, silent on
  network-only assets (printers, OT, unmanaged) — a witness, not the
  union.
- **Buy an ASM (attack-surface) platform:** valuable for
  internet-facing discovery; the internal-gap classes above are still
  witness-union work — procurement ≠ discovery discipline.

## Tradeoffs

- Credentialed scans (deep, safe) vs key/credential management cost:
  the vault+rotation overhead is the price of no-crash depth.
- Passive census (zero risk, shallow) vs active scan (deep, risky):
  layered witnesses convert the trade from either/or to scheduling.
- Cloud-API-as-truth vs CMDB hygiene: fix the CMDB *eventually*; make
  the API authoritative *now* — drift-fixing is a project, incidents
  are today.

## Common Mistakes

- Treating the scan as the inventory (the 1,200 number is a claim, not
  a witness).
- Scanning OT "carefully" (carefully still crashes PLCs — exclusion
  with credentialed alternatives is the professional line).
- No canary (the profile is untested until production pays).
- Phantom hosts left in reports (coverage claims decay into fiction).

## Instructor Prompts

- "Which witness is *authoritative* for each host class — and why can't
  one witness rule them all?"
- "What does the canary test actually prove, and what does it not?"
- "Which delta (CMDB-minus-everything) improves the *report* rather
  than the *security*?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Witness-union framing; canary principle |
| Technical accuracy | 25% | Gap mechanisms per class correct |
| Alternatives considered | 20% | Scan-first/EDR-only rejections |
| Communication | 15% | Reconciliation table + safety plan |

**Timing:** reveal at 5:00 + 10; "the union is the inventory" is the
takeaway.

## CLO Mapping

- **CLO-10** — Vulnerability-program discovery discipline.
