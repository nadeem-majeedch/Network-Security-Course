---
case: cs-015
solution-for: modules/module-02-network-threats/case-studies/cs-015-vlan-hopping-attempt.md
difficulty: beginner
module: 2
lecture-anchor: L06
clos: [CLO-2]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-015 Solution — VLAN Hopping (INSTRUCTOR ONLY)

## Model Solution

**Double-tagging mechanics:** the attacker crafts a frame with **two 802.1Q
tags** — outer tag = the VLAN their port legitimately belongs to (VLAN 40),
inner tag = the target VLAN (VLAN 100). The **ingress access switch** strips
only the outer tag (it believes the frame is ordinary VLAN-40 traffic) and
forwards the residual frame — still carrying the inner tag 100 — toward the
trunk. The **core switch** now sees a tagged frame for VLAN 100 and switches
it into the server VLAN. The attacker controls both tag values; no switch
"authentication" exists at this layer — tags are just fields in the frame.

**Why it mostly failed here:** double-tagging is **one-directional and
reply-less** — the attacker can inject into VLAN 100 but receives no responses
(because the return path re-tags/forwards back to VLAN 40 incorrectly, and
the real owner of the conversation never sees a session to establish). The
CPU spike = the switches processing/parity-checking the crafted frames.
Success would have required an actual exploitable service in VLAN 100 that
acts on unolicited input (or the attacker being **on the native VLAN** —
see below).

**The one design decision that makes double-tagging useless:** **never run
user traffic on the native VLAN** (and preferably don't have a native VLAN at
all on trunks — or set it to an unused "black-hole" VLAN). Double-tagging's
inner tag trick depends on the *first* tag matching the trunk's native/untagged
expectation. With native VLAN ≠ user VLAN and unused, stripped frames land in
a dead-end VLAN.

**Four config changes and the variant each targets:**

| # | Change | Closes |
|---|---|---|
| 1 | Pin user ports: `switchport mode access` + `switchport access vlan 40`, disable DTP (`nonegotiate`) | DTP trunk-negotiation attack (attacker's port *becomes* a trunk and sees all VLANs) |
| 2 | Change native VLAN on all trunks to an unused VLAN (e.g., 999), or tag native (`vlan dot1q tag native`) | double-tagging (kills the strip-first-tag premise) |
| 3 | Prune unused VLANs from trunks (`switchport trunk allowed vlan …`) | limits any successful hop's reach into server VLANs |
| 4 | Port security + shutdown unused ports | limits the attacker's ability to sit on an orphan/unused port to iterate |

## Alternative Solutions

- **802.1X (NAC) as the primary fix.** Strong identity control, but it
  addresses *who* is on the port, not tag-crafting; correct as *additional*
  hardening, not as the tag-behavior fix.
- **"VLANs are broken, use firewalls everywhere."** Overcorrection — properly
  configured VLANs remain a valid segmentation tool; the case shows
  misconfiguration risk, not tool failure.

## Tradeoffs

- Disabling DTP everywhere vs just user ports: disabling on user ports is
  zero-risk; disabling on trunks requires static trunk config (fine, but a
  bigger change window).
- Unused-native-VLAN approach vs tag-native: both work; tag-native is cleaner
  but must be consistent on both trunk ends or the trunk breaks — test in lab.

## Common Mistakes

- Explaining hopping as "the switch is tricked into a new VLAN by DTP" — that's
  the *other* variant; double-tagging is frame-crafting.
- Saying "the attack succeeded but was detected" — no session was established.
- Omitting native-VLAN hygiene, the linchpin control.
- Proposing VTP changes as defense (VTP mode is orthogonal to tag-crafting and
  is itself an attack surface if misused).

## Instructor Prompts

- "Draw the frame before and after the ingress switch strips tag 1."
- "Why does the attacker's lack of return traffic make this 'half-duplex' hacking?"
- "Which of your four changes would have stopped the DTP variant if the
  attacker had used a *different* tool?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Hop-by-hop tag mechanics; reply-less limitation |
| Technical accuracy | 25% | Two variants distinguished; native-VLAN linchpin |
| Alternatives considered | 20% | NAC/overcorrection weighed |
| Communication | 15% | Frame-walk clarity; mapped fix table |

**Timing:** reveal at 5:00; the frame-walk prompt is the visual anchor.

## CLO Mapping

- **CLO-2** — L2 segmentation attack mechanics and hardening.
