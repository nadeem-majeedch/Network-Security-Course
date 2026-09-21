# cs-058 — Rogue-AP Hunt Across a Building Survey

> **Simulated scenario.** The office, survey data, and triage calls are fictional.

## Difficulty & Domain

- **Difficulty:** Advanced-Advanced · **Domain:** Wireless network security · **CLO:** CLO-8
- **Est. time:** 15 minutes · **Anchor:** L18 (Enterprise Wireless & Rogue Defense)

## Scenario

A compliance-driven wireless survey of a 6-floor office building found 34
SSIDs. You must triage: authorized / neighbor / benign-personal / **rogue
(corporate-wired)** — the last class being the audit's target: APs plugged
into the corporate LAN. You have the survey table and switch data; produce
the triage, the rogue-confirmation method, and the policy that prevents
the rogues' return.

## Stakeholders

- **Compliance** — the audit requires rogue evidence + remediation.
- **Employees** — personal Mi-Fi devices are common; punitive triage
  backfires.
- **Network team** — owns the switch ports; wants precision, not witch
  hunts.
- **Facilities** — neighboring buildings' APs bleed in; not our problem to
  fix, but ours to classify.

## Network Context

- Corporate Wi-Fi: `CORP` (802.1X), `GUEST` (portal) — the only authorized
  SSIDs; controller-managed APs known by inventory (22 APs).
- Floors 1–6; neighboring buildings ~20 m away.
- Switch access ports: no port-security, no 802.1X on wired yet (that's
  the prevention gap).

## Available Evidence

**Survey summary (34 SSIDs → triaged inputs):**

| # | SSID pattern | BSSID OUI | Strongest floor | Wired-IP evidence | Initial call |
|---|---|---|---|---|---|
| 1–2 | CORP, GUEST | vendor-A (controller) | all | — | authorized |
| 3–24 | vendor-A OUI, BSSIDs matching 22 AP inventory | vendor-A | per-floor map | — | authorized |
| 25 | `linksys` | consumer vendor-B | floor 3, break room | **switch port 3-14 up, DHCP lease** | ? |
| 26 | `NETGEAR-5G` | consumer vendor-C | floor 5, exec area | no wired match | ? |
| 27–29 | `AndroidAP_xxx` | phone OUI | varies | no wired match | ? |
| 30 | `FBI_SURVEILLANCE_VAN` | phone OUI | floor 2 | none | ? |
| 31–34 | neighbor-building corp SSIDs | enterprise vendor-D | strongest at windows | none | ? |

**Switch data:** port 3-14 = break-room printer drop (unused since printer
moved), now shows a consumer AP MAC + DHCP.

## Student Task

1. Produce the **triage table**: classify all 34 (authorized / neighbor /
   benign-personal / rogue-corporate) with the deciding evidence per class.
   The `linksys` (25) is the suspected rogue — confirm the classification
   and say what makes it the *dangerous* class vs the others.
2. Design the **rogue-confirmation workflow**: how to prove (or clear) an
   SSID is corporate-wired *before* unplugging (the switch-port correlation
   chain), and the safe-removal step (who, what notice, what evidence).
3. Write the **prevention policy**: the wired-port control that makes
   rogue APs *impossible* (exact feature), the personal-Mi-Fi stance that
   avoids punitive blowback, and the quarterly survey cadence design.

## How to Approach This (Reasoning Scaffold)

- The dangerous class is defined by *wired connectivity*, not SSID
  friendliness — `linksys` on port 3-14 bridges the corporate LAN to
  unauthenticated radio; `FBI_SURVEILLANCE_VAN` on a phone is noise with
  a name.
- Confirmation = the correlation chain: BSSID's wired MAC → DHCP lease →
  switch port → then you *know*, before you touch.
- Prevention is one feature (wired 802.1X / port-security) plus a policy
  voice that doesn't criminalize phone hotspots.

## CLO Mapping

- **CLO-8** — Rogue classification, confirmation, and prevention.

## Safety Notes

- Design exercise; real surveys need authorization and neighbor-SSIDs
  are off-limits to touch.
