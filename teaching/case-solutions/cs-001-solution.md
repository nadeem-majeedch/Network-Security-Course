---
case: cs-001
solution-for: modules/module-01-network-foundations/case-studies/cs-001-asset-trust-zone-inventory.md
difficulty: beginner
module: 1
lecture-anchor: L01
clos: [CLO-1]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-001 Solution — Asset and Trust-Zone Inventory (INSTRUCTOR ONLY)

## Model Solution

**Inventory (key rows; full table in class):**

| Asset | Owner | Data sensitivity |
|---|---|---|
| NAS (client tax docs) | Managing partner | **High** (PII, regulated) |
| Door controller | Building vendor | **High** (physical-access impact) |
| Laptops ×10 | Employees | High–Med (client data at rest) |
| Printers | Office manager | Med (print spool retention) |
| Unknown mobile leases ×5 | Unidentified | **Unknown** — must resolve |
| Reception TV | Office manager | Low |
| AP / router | Office manager | Infrastructure (high blast radius) |

**Proposed zones (defensible minimum for a no-VLAN router):** (1) User zone,
(2) Server/data zone (NAS), (3) IoT/building zone (door, TV), (4) Guest zone
(new SSID, isolated), (5) Management zone (router, AP admin).

**Top-3 misplacements, ordered:**

1. **Door controller on the user LAN with vendor remote support on port 80** —
   a third-party-managed, plaintext-remotely-administered device sits one
   switch hop from every laptop and the NAS; compromise = pivot point +
   physical-access impact.
2. **NAS in the same L2 segment as guests and BYOD leases** — the crown-jewel
   data store is reachable from the least trusted, most compromised-prone
   devices; five unidentified leases prove the boundary is already porous.
3. **Shared, stale WPA2-PSK across employees + guests** — the credential
   protects everything at once, cannot be rotated per-person, and has been
   shared with outsiders for years; departure of one guest leaks it permanently.

## Alternative Solutions

- **Physical separation instead of VLANs:** move NAS + door controller onto a
  small second router/switch. Acceptable at this scale; costs hardware and
  cable work; less flexible as the firm grows.
- **Do nothing structural; harden in place** (rotate PSK, disable vendor
  remote port 80, inventory the unknown leases first). Legitimate first week;
  fails the assignment's zone-design goal but is the honest sequencing answer.
- **Cloud NAS migration** to sidestep local segmentation. Changes the risk,
  does not remove it (access control and identity become the boundary).

## Tradeoffs

- VLANs on new hardware vs cost/complexity for a 12-person office.
- Zone granularity vs admin capability: the office manager is not a network
  engineer; a 5-zone design nobody can operate is worse than 3 zones enforced.
- Remote vendor support convenience vs exposure — disabling it needs a
  contractual alternative (vendor on-site or client-initiated VPN).

## Common Mistakes

- Treating printers, TVs, door controllers as "not security-relevant."
- Inventing zones without saying what separates them (a zone with no control
  on the boundary is a label, not a zone).
- Inventory without owners — sensitivity classification needs an accountable party.
- Listing the unknown leases as trivia instead of flagging them as an unresolved
  identity question.

## Instructor Prompts (debrief steering)

- "Which single control would reduce the most risk for the least money?"
- "The door controller has to be reachable by the vendor — design that path."
- "What would you need to see before declaring the 5 unknown leases benign?"
- "Which zone's boundary would you monitor first, and with what?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Placement justified by reachable-from compromise, not device type |
| Technical accuracy | 25% | Zones/boundaries described with an actual control on each boundary |
| Alternatives considered | 20% | ≥1 alternative with a real cost named |
| Communication | 15% | Ordered top-3 with rationale; inventory table readable |

**Timing:** reveal solution at 5:00; spend debrief on the "unknown leases"
discussion — it foreshadows asset-inventory discipline (L24) and NAC (L12).

## CLO Mapping

- **CLO-1** — CIA/risk vocabulary applied to real placement decisions.
