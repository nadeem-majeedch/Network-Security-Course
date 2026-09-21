---
case: cs-056
solution-for: modules/module-05-wireless-cloud/case-studies/cs-056-wep-legacy-device-retirement-plan.md
difficulty: advanced
module: 5
lecture-anchor: L17
clos: [CLO-8]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-056 Solution — WEP Retirement (INSTRUCTOR ONLY)

## Model Solution

**WEP break mechanics (precise):** WEP uses RC4 with a **24-bit IV**
concatenated with a shared secret per frame; the IV space (~16.7M) exhausts
fast on a busy network, producing **keystream reuse**; each reused IV pair
leaks keystream XOR relationships that statistical tools (FMS/KoreK/
PTW-class) convert into the key — and WEP's **CRC-32 integrity check is
linear and unkeyed**, so attackers can inject/modify frames and *cause* the
traffic volume that speeds cracking. Practical result: a moderately busy
WEP network yields its key in minutes, passively-then-actively. **Risk path
here:** attacker in the truck yard (radio range noted) cracks WEP → joins
the scanner SSID → that SSID sits on the same APs as corp (shared infra) →
target is the **inventory server** (customer order data) and any flat-L2
reach. The cipher is the *entry*; the data and lateral reach are the
*stakes* — state both or the "it's just old Wi-Fi" dismissal survives.

**Interim containment (buys months, honestly labeled):**

| Control | Effect |
|---|---|
| **Move WEP SSID to a dedicated VLAN/subnet** (scanner→inventory-server *only* allow-list; deny all else incl. lateral, corp, internet) | cracks give attacker a dead-end segment: scanner protocol or nothing |
| **Remove the WEP SSID from outdoor/yard-facing APs**; confine its radios to the scanner work areas (cell-size planning) | attacker must be *inside* the work area — yard cracking dies |
| **AP-side MAC allow-list** of the 12 scanner MACs on the WEP SSID | trivially spoofable but *noisy* (collisions log) — detection value, not prevention |
| **WIPS/monitoring on that SSID**: alert new associations, new MACs, injected-traffic signatures | the real interim control: the crack attempt *itself* becomes the alert |
| Inventory server: disable any local admin interfaces on that VLAN; credential hygiene | shrinks what a dead-end segment still reaches |

**What interim cannot fix:** the cipher. A determined attacker who cracks
WEP and spoofs a scanner MAC *can still inject/receive scanner-protocol
traffic* — containment bounds the blast radius and adds detection latency;
it does not make WEP safe. Say this in the risk register, dated, signed.

**Retirement path:**

- *Options matrix:* (1) **Replace scanners** (modern 802.11ac/ax, WPA3/Ent)
  — cleanest, capex ~$Xk; (2) **Wireless bridge/gateway boxes** per dock
  area (WEP side stays internal to a box that re-egresses on WPA2) —
  hack-ish, still leaves WEP on the air; (3) **Wired-only for fixed
  stations** (charging docks get Ethernet) + fewer wireless units —
  hybrid; (4) vendor's long-dead — no firmware savior exists.
- *Business case arithmetic:* replacement capex (say 12 × $1.5k = $18k)
  vs exposure: customer-order-data breach via a minutes-cracked protocol
  *adjacent to corp infrastructure* — one incident's breach-response,
  customer notification, and audit fallout exceeds capex by multiples;
  plus the open audit finding has its own cost (insurer/assessor
  scrutiny). Frame: the scanners already *are* the incident budget.
- *Decommission checklist:* replacement fleet piloted (2 scanners, 1
  week, real workflow) → cutover in two waves (6+6) with the inventory
  server's second NIC/VLAN ready → **kill the WEP SSID config on all
  APs** (verify with a survey — "no WEP beacon on any channel") →
  re-assign the interim VLAN to the new fleet's segmented role → close
  the finding with survey evidence attached.

## Alternative Solutions

- **"Keep WEP on a hardened segment forever":** fails audit standards and
  the stated risk path; acceptable only as the *dated* interim, never the
  end-state.
- **Bridge/gateway approach as final:** keeps a broken protocol on-air to
  avoid capex — buys nothing once the bridges cost half the scanners;
  false economy.
- **Scanner-protocol over serial/wired for all:** operations-accurate for
  fixed stations only; mobile picking needs wireless — hybrid answer.

## Tradeoffs

- Interim detection investment vs replacement speed: WIPS alerts are
  wasted spend if replacement ships next month — match interim depth to
  the *real* procurement timeline.
- Two-wave cutover vs big-bang: waves keep workflow alive; big-bang is
  faster but a scanner firmware surprise halts shipping — waves.
- Cell-size reduction vs coverage holes: scanner dead-zones create work
 arounds (walking to charge docks) — survey with the ops manager before
 trimming radios.

## Common Mistakes

- Treating WEP as "weak but okay for scanners" — the risk path to the
  inventory server is the argument, not the cipher's age.
- Interim controls presented as fixes (the cipher stands).
- No business-case arithmetic (ops manager needs the number, not the
  lecture).
- Decommission without the survey verification (a stale SSID config
  beaconing WEP on one AP is the classic coda).

## Instructor Prompts

- "Which interim control actually detects the *crack attempt*, and why is
  that the crown jewel?"
- "What does the survey evidence for decommission look like?"
- "Where does the $18k stand against the incident math?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Break mechanics precise; risk-path framing |
| Technical accuracy | 25% | IV/CRC/injection correctness; cell/VLAN design |
| Alternatives considered | 20% | Options matrix with honest bridge critique |
| Communication | 15% | Business case + decommission checklist |

**Timing:** reveal at 5:00 + 10; the "incident budget" line closes the
business argument.

## CLO Mapping

- **CLO-8** — Legacy wireless risk and retirement engineering.
