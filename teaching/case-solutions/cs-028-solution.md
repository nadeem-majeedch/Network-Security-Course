---
case: cs-028
solution-for: modules/module-03-secure-architecture/case-studies/cs-028-vlan-plan-corporate-guest-iot.md
difficulty: intermediate
module: 3
lecture-anchor: L09
clos: [CLO-3]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-028 Solution — VLAN Plan (INSTRUCTOR ONLY)

## Model Solution

**Zone plan:**

| VLAN | Name | Members | SSID | Inter-zone policy (one-liner) |
|---|---|---|---|---|
| 10 | CORP | laptops/desktops, NAS | corp (WPA2-Ent, 802.1X) | clients → servers/ports/room systems; no → IoT/GUEST |
| 20 | SERVER | NAS, print server, mgmt | — | ingress from CORP only (SMB/IPP/mgmt); no egress to internet |
| 30 | AV | TVs, conference systems | — | mDNS reflector from CORP (scoped); egress vendor cloud only |
| 40 | GUEST | guest Wi-Fi | guest (open + portal) | internet only; zero lateral; no → any internal VLAN |
| 50 | IOT | coffee machine, misc smart devices | iot (WPA2-PSK, unique per device where supported) | egress internet (allow-list by domain where possible); deny all lateral; deny → CORP/SERVER/AV |
| 60 | BMS-SEC | door panels, HVAC controller | — | egress vendor cloud (pinned); ingress only from a *vendor jumphost path* (see below); no lateral to anything |
| 70 | CAM | IP cameras | — | egress to NVR only; NVR in SERVER or its own; no internet |

**The coffee machine — two defensible options:**

1. **Quarantine-grade isolation (recommended):** joins IOT with a
   per-device PSK, allow-listed egress to its vendor cloud only, zero
   lateral. Honest answer to the office manager: "it's on a guest-grade
   leash — it works, it just can't see anything else."
2. **Don't connect it at all (offline mode):** if the vendor cloud is
   unverifiable, machines without business value stay offline — the
   *rationale* (an appliance with a mic and no patching story has negative
   value) is the teaching point. Give the office manager the framing:
   "connected if and only if we can say exactly where it talks."

**The landlord requirement — concrete arrangement (not negotiation):**
door panels live in BMS-SEC; the vendor gets **no standing network access**.
Instead: a dedicated **maintenance path** — a vendor-facing port on the
firewall (or VLAN) exposed only during scheduled windows, time-boxed by
firewall policy (recurring schedule), reachable only to the panels' config
port (not to HVAC), fully logged (session + command logs via the panels'
local logging forwarded off-box), MFA'd jumphost if the vendor supports it.
Contract language points to that path as "the" access — the landlord's
demand is satisfied *technically*, auditable, and revocable. (If the vendor
uses a cloud app: pin the panels' egress to the vendor's published endpoints
and let the cloud path be the maintenance channel — then the on-site
exposure is *zero* and the firewall schedule covers only emergency local
config.)

**The mDNS/casting problem:** casting (Chromecast/AirPlay) relies on
**multicast DNS across the *same* L2** — by default it won't cross
CORP→AV, so "casting must just work" fails the moment TVs are isolated.
Standard solutions: (1) an **mDNS reflector/gateway** (avahi-style) scoped
CORP↔AV only — pragmatic, but it bridges discovery traffic; constrain with
ACLs on which services reflect; (2) **managed casting**: room systems join
CORP (they're managed endpoints with vendor support) so no reflection is
needed — cleaner trust, higher device cost; (3) vendor's "discovery proxy"
features on enterprise Wi-Fi (controller-level mDNS policy). Tradeoff:
reflector = cheap but punches a scoped hole; managed-AV = costly but
trust-clean.

## Alternative Solutions

- **Everything on one VLAN + host firewalls:** fails for TVs/coffee
  (no host firewall); rejected.
- **IoT on GUEST SSID:** tempting; fails because guest policy must allow
  *zero* lateral — but coffee-to-vendor-cloud is egress, fine — the real
  reason to keep a separate IOT: different PSK discipline + device-level
  allow-listing; if the firewall can't do per-zone egress policy, IOT on
  GUEST is the defensible budget answer.
- **Cloud-managed SD-branch instead of VLANs:** viable product category;
  overkill for one office — name it, don't design it.

## Tradeoffs

- mDNS reflection scope vs cast-ability: reflect only CORP↔AV, never
  GUEST↔anything (guests must not see or reach room systems).
- Per-device PSKs vs one IoT PSK: per-device enables revocation; one PSK
  means one leak rotates the whole zone.
- Door-panel cloud vs scheduled on-site path: cloud = vendor-maintained
  availability but adds a cloud dependency on a *safety* system — require
  the vendor's endpoint list + pinning in the contract.

## Common Mistakes

- Putting TVs in CORP "so casting works" (untrusted cloud devices among
  crown-jewel clients' machines).
- Handing the landlord "a port on the switch" (unscoped, unlogged access).
- Forgetting cameras' egress discipline (they phone home too).
- Designing zones but not *who administers* them (management paths need
  their own rule).

## Instructor Prompts

- "Which zone's compromise would the partners notice first, and how does
  your design show that?"
- "What does the vendor's cloud endpoint list have to do with the door
  panels' *safety* function?"
- "Why is 'the coffee machine can talk to the internet' not the risk?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Trust-tiered zones; contractual access translated to scoped path |
| Technical accuracy | 25% | mDNS mechanics; SSID/VLAN mapping coherent |
| Alternatives considered | 20% | Coffee-machine + landlord options both real |
| Communication | 15% | Zone table readable by office staff |

**Timing:** reveal at 5:00 + 2; the coffee machine is the debrief's
memory hook — "negative-value appliances."

## CLO Mapping

- **CLO-3** — Zone design for mixed trust in a greenfield office.
