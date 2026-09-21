---
case: cs-058
solution-for: modules/module-05-wireless-cloud/case-studies/cs-058-rogue-ap-hunt-across-a-building-survey.md
difficulty: advanced
module: 5
lecture-anchor: L18
clos: [CLO-8]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-058 Solution — Rogue-AP Triage (INSTRUCTOR ONLY)

## Model Solution

**Triage table:**

| Class | Items | Deciding evidence |
|---|---|---|
| Authorized (24) | CORP, GUEST + 22 inventoried controller APs (vendor-A BSSIDs match inventory + floor map) | BSSID ↔ AP inventory 1:1 |
| **Rogue-corporate (1)** | **#25 `linksys`** — consumer AP, floor-3 break room, **switch port 3-14 up with DHCP lease** | BSSID's wired MAC = DHCP lease on a live corporate port: the LAN is bridged to unauthenticated radio — the audit's target class |
| Benign-personal (4) | #26 `NETGEAR-5G` (no wired match; likely exec-area Mi-Fi/router), #27–29 `AndroidAP_*` (phone OUI), #30 `FBI_SURVEILLANCE_VAN` (phone OUI, joke SSID — verify it's a phone BSSID, not a laptop bridge) | no wired correlation; OUI = handset/portable; classification is *provisional* until the confirmation workflow clears them |
| Neighbor (4) | #31–34 enterprise-D OUI, strongest at windows, match the neighboring building's known corp SSIDs | location physics + external OUI; record and ignore (never touch) |

**Why `linksys` is the dangerous class and the others aren't:** the danger
metric is *wired corporate connectivity offered over open radio* — an
attacker (or any passerby) associates to `linksys` and is *on the corporate
LAN* without 802.1X, past every wireless control, adjacent to floor 3's
wired estate. The phone hotspots offer only the owner's mobile data
(privacy of the owner, not the corporate LAN); neighbor APs aren't ours at
all. `FBI_SURVEILLANCE_VAN` looks alarming and is the *least* risky —
evidence-driven classification beats name-driven panic (the case's joke
with a purpose).

**Rogue-confirmation workflow (before unplugging):**

1. **Correlation chain:** survey BSSID (radio MAC) → AP's *wired* MAC
   (consumer APs often use one MAC for both — else match OUI + DHCP
   fingerprint) → **DHCP lease table** (hostname `linksys`, lease on
   3-14's subnet) → **switch port 3-14** (MAC table) → port's drop
   history (printer's former drop — explains placement). Chain complete =
   confirmed; partial = investigate, don't yank.
2. **Clear or condemn benign-personal:** for #26/#30 — check for *any*
   wired correlation across the last 30 days of DHCP/MAC tables; none =
   personal device, no corporate bridge. (A laptop *bridging* its Mi-Fi
   would show the laptop's wired+wireless pairing — check that pattern
   specifically; that's the sneaky variant of the class.)
3. **Safe removal:** change ticket → unplug port 3-14 (or shut it) →
   photograph/keep the AP (evidence: compliance artifact + device
   forensics if policy asks "who plugged this in") → notify break-room
   occupants with the *why* (open corporate bridge) — punitive tone
   creates the next hidden AP; educational tone creates a reporter.
4. **Evidence pack for audit:** survey table, correlation chain, switch
   logs, removal ticket, before/after survey — the compliance deliverable
   is the *chain*, not the yank.

**Prevention policy:**

- **The exact feature: wired 802.1X (or MAB+port-security) on all access
  ports** — unknown devices get no DHCP, so a rogue AP *cannot bridge the
  LAN* even if plugged in. Interim: port-security (1 MAC) + DHCP
  snooping on access ports; the break-room printer drop class (unused but
  live ports) gets **administratively shut** — dead ports are rogue
  invitations.
- **Personal-Mi-Fi stance (no blowback):** personal hotspots are *allowed*
  (they carry no corporate bridge) as long as they never touch corporate
  wired ports or corporate laptops' bridging features (USB-tether policy
  on managed laptops); the policy voice: "we don't police your phone; we
  police the wall ports."
- **Quarterly survey cadence:** automated controller/WIPS spectrum +
  SSID scan quarterly + annual *manual* walk-survey (the compliance
  artifact); deltas auto-triaged by the same evidence chain — the survey
  becomes a *pipeline*, not a project.

## Alternative Solutions

- **Yank `linksys` immediately, document later:** operationally fine,
  evidence-weak — the audit wants the chain; also risks missing a *second*
  rogue sharing the pattern.
- **WIPS auto-containment of all unknown SSIDs:** illegal-adjacent (floods
  neighbors' APs — #31–34 are *theirs*), ineffective against wired rogues
  anyway (contain the SSID, the port still bridges) — rejected with
  reasons.
- **Ban all personal hotspots:** unenforceable and punitive — drives the
  next rogue deeper (hidden, not absent).

## Tradeoffs

- Confirmation depth vs response speed: the chain takes an hour; an
  open-corporate-bridge left up takes days of exposure — for a *confirmed*
  open bridge, parallel-path: shut the port *and* complete the chain.
- 802.1X-on-wired cost (projects, printer/MFA exceptions) vs rogue
  elimination: it's the only *structural* kill; exceptions process
  (printers via MAB) is the price.
- Survey automation vs walk-survey realism: automated catches beacons;
  the annual walk catches the powered-down-then-moved rogue — both, on
  cadence.

## Common Mistakes

- Classifying by SSID name/scariness (`FBI_VAN` panic, `linksys` shrug).
- Confirmation skipped — unplugging with no chain (evidence + wrong-port
  risk).
- Neighbor APs touched (legal line).
- Prevention as "policy memo" instead of the wired-port feature.

## Instructor Prompts

- "Which data source proves the `linksys` is *wired*? Name the chain."
- "What makes the laptop-bridged hotspot the sneaky variant of the rogue
  class?"
- "Why is auto-containment worse than useless here?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Wired-bridging as the danger metric; evidence-first triage |
| Technical accuracy | 25% | BSSID/DHCP/MAC-chain mechanics |
| Alternatives considered | 20% | Containment/ban rejections reasoned |
| Communication | 15% | Triage table + workflow steps |

**Timing:** reveal at 5:00 + 10; the FBI-van joke lands the
evidence-over-name lesson.

## CLO Mapping

- **CLO-8** — Rogue classification, confirmation, and prevention.
