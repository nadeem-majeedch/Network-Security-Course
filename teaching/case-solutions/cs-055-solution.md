---
case: cs-055
solution-for: modules/module-05-wireless-cloud/case-studies/cs-055-open-guest-wifi-risk-containment.md
difficulty: advanced
module: 5
lecture-anchor: L17
clos: [CLO-8]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-055 Solution — Guest Wi-Fi Containment (INSTRUCTOR ONLY)

## Model Solution

**Guest architecture:**

| Layer | Control | Purpose |
|---|---|---|
| L2 | **Client isolation (PSPF-style)** on `MALL-FREE`; guests on their own VLAN | no guest↔guest frames at all — kills the lateral attack class (sniffing/ARP/NetBIOS browse) |
| L3 | Guest VRF/subnet → **internet-only**; deny to all internal/tenant ranges; rate-limit per client (e.g., 10/5 Mbps) + per-session quota | guests can't touch tenants even by routing; quotas keep one abuser from starving everyone |
| Portal | ToS **+ one-time verification (SMS OTP or email magic-link) → session-scoped ID** | correlatable identity per session without identity documents |
| Egress | **Per-session NAT pool / per-user IP mapping logged** (session ID ↔ internal port ↔ timestamp) + abuse email on the ToS page; optional: block high-abuse ports (25) and rate-limit P2P classes | the abuse-notice answer: the ISP's report resolves to a *session*, and the session resolves to an OTP-verified contact — actionable without surveillance |

**Why this passes the legal test:** accountability requires *correlation*,
not *identification* — an OTP-verified session ID, a logged NAT mapping,
and a retained log (90–180 days) turns "someone on IP X infringed" into "a
specific verified session did, contact on file." The mall's response letter
now has a recipient. What the mall must *not* do: deep-inspect and profile
guests' traffic — retention of flow metadata (who/when/where/volume) meets
the duty; content inspection exceeds it (and privacy law in most
jurisdictions).

**Evil-twin defense (honest limits):**

- *What a WIPS sees:* a duplicate SSID with a different BSSID/OUI,
  possibly stronger signal near the food court, differing security (open
  vs the mall's portal), and cloning fingerprints (same SSID beacon rate,
  different vendor OUI). The mall can **locate** the twin (RSSI triangulate),
  **warn on portal** ("verify the SSID 'MALL-FREE-SECURE' never appears —
  our network name is X"), and **ask mall security to visit the table** —
  physically addressing a person with a hotspot is a *security* matter,
  not a wireless config.
- *What the mall cannot do:* prevent the twin's radio from existing; WIPS
  containment (deauth-flooding the rogue) is legally fraught and often
  ineffective against a person sitting there — detection + human response
  is the professional play.
- *What actually saves visitors:* **TLS** — any real service (mail, bank,
  SaaS) validates certificates; the twin can only read plaintext and
  *phish portal-style* pages. So the portal warning teaches: "our portal
  never asks for email passwords; if any page does, it's not ours."
  Client-side the visitor's protections are HTTPS-everywhere defaults,
  certificate warnings *respected*, and VPN for the cautious — the mall's
  job is the warning text, not the visitor's discipline.

**Tenant-SSID fix:**

- Move each tenant to **per-tenant VLANs** (RADIUS-assigned or
  PSK→VLAN mapping on the controller) — `TENANT-CORP` stops being one L2.
- **The one control that stops cross-tenant snooping:** tenant VLANs
  terminate at the firewall with **deny tenant↔tenant** (isolation policy
  at L3) — because multiple tenants behind one controller will share
  trunk infrastructure; L2 separation alone leaves VLAN-hopping and
  controller-side misconfig as the bridge. Pair with per-tenant egress
  (their own IPs) so tenant accountability matches the guest design.
- Bonus fix: tenant SSIDs get **PMF + per-tenant credential lifecycle**
  (the shared-PSK-reset process cs-054 would prescribe).

## Alternative Solutions

- **Charge-for-Wi-Fi (paid portal):** payment *is* strong identity —
  real option; changes the mall's amenity posture; note as business
  decision.
- **Sponsor-provisioned guest certs/802.1X:** impractical for a mall's
  transient population; right answer for *tenant* staff (802.1X per
  tenant) — mention the split: guests open+portal, tenant staff
  Enterprise.
- **Ban personal hotspots:** unenforceable theater; the twin incident is a
  *response* problem, not a policy-poster problem.

## Tradeoffs

- OTP portal vs friction: SMS OTP drops conversion ~10–20%; magic-link
  email is friendlier but weaker (disposable inboxes) — pick per abuse
  history, revisit quarterly.
- Metadata retention length vs privacy: 90 days balances abuse-response
  with minimization; log *access* tightly (who can query).
- Isolation strictness vs visitor UX (AirDrop/Chromecast between friends):
  guest isolation is binary in practice — accept the loss; a "premium
  casting" lounge VLAN would re-open the class.

## Common Mistakes

- Designing portal identity as *surveillance* (ID scans) instead of
  correlation.
- Believing WIPS "containment" solves evil twins (detection + human
  response is the answer).
- Forgetting the tenant-shared-L2 finding — the food-court attacker's
  actual next target.
- No per-session egress mapping (the abuse notice stays unanswerable).

## Instructor Prompts

- "Trace one abuse notice end-to-end under your design — who gets the
  email, what do they produce?"
- "Why is physically locating the twin a mall-security play and not a
  network play?"
- "Which single control would you keep if budget forces one?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Correlation-not-identification accountability; honest twin limits |
| Technical accuracy | 25% | Isolation/VRF/NAT-mapping/WIPS mechanics |
| Alternatives considered | 20% | Paid-portal/Enterprise-for-tenants split |
| Communication | 15% | Three designs each with a testable artifact |

**Timing:** reveal at 5:00 + 10; the abuse-notice walkthrough is the
debrief's spine.

## CLO Mapping

- **CLO-8** — Public Wi-Fi architecture, liability, and threat defense.
