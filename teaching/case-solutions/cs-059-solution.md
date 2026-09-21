---
case: cs-059
solution-for: modules/module-05-wireless-cloud/case-studies/cs-059-8021x-eap-deployment-for-enterprise-wi-fi.md
difficulty: advanced
module: 5
lecture-anchor: L18
clos: [CLO-8]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-059 Solution — 802.1X Deployment (INSTRUCTOR ONLY)

## Model Solution

**EAP decision (one paragraph):** choose **EAP-TLS**. The deciding
mechanics: PEAP-MSCHAPv2 protects the password in an outer TLS tunnel,
but the inner MSCHAPv2 exchange remains MD4/DES-era crypto — captured
inner handshakes permit offline cracking of the NT hash (and the
tooling is public), so every user password is only as strong as its
entropy against offline attack. EAP-TLS replaces the password with a
client certificate: nothing offline-attackable crosses the radio at all.
The classic objection — certificate provisioning cost — is already paid
here: **MDM covers 480/500 devices**, so enrollment/renewal/revocation
are config management, not help-desk theater. The 20 non-MDM devices are
the tail that the legacy pattern handles. PEAP remains the fallback for
the few devices that can't hold certs — but *not* the architecture.

**Architecture:**

- **RADIUS:** **two servers, two sites (or cloud-redundant)**, both
  proxies to AD; controllers configured with both; server-cert trust
  pinned on clients (via MDM Wi-Fi profile — the profile also disables
  user-bypass). Health: RADIUS response-time alerts; test-auth every
  5 min from a probe device.
- **Certificate lifecycle (MDM-driven):** enrollment at device
  check-in (SCEP/ACME-style against internal CA), renewal at T-30d
  automatic, revocation on MDM wipe/retire (plus AD account disable
  triggers RADIUS reject via group lookup); CA hygiene per cs-042
  (intermediate for Wi-Fi client certs, name-constrained).
- **Dynamic VLAN/roles (RADIUS attributes):** `staff` → corp VLAN;
  `contractor` → restricted-corp VLAN (egress-scoped); `legacy` →
  device VLAN; guest unchanged (portal SSID). The role assignment is
  where segmentation starts to *mean* something (the flat-VLAN finding
  dies here).
- **Legacy-device pattern:** **iPSK SSID** (per-device PSKs, controller
  maps PSK→identity→`legacy` VLAN): printers/scanners/room-systems get
  individual secrets, individually revocable, no lateral between device
  classes — identity-*ish* without 802.1X; each device's PSK lives in
  the device inventory with an owner (cs-028/cs-054 pattern applied).

**Rollout + day-one-outage fix:**

- **New SSID `CORP-EAP` runs alongside** `CORP-PSK` for the entire
  migration (no cutover cliff): controllers broadcast both; per-group
  MDM profile pushes the `CORP-EAP` config (pilot IT → engineering →
  everyone in 3 waves over 6 weeks); the old SSID dies only when the
  new one's auth-success telemetry hits ≥99.5% for two weeks.
- **The failure-mode design (the graded core):** when RADIUS (both!) is
  down, the *default* must be **fail-closed for new auths** —
  **explicitly not** "fall back to PSK": a PSK fallback path is a
  standing backdoor whose key management decays (the shared-PSK finding
  returns through the emergency door) and whose existence is the first
  thing an attacker asks for. The honest outages are: (a) *existing*
  sessions continue (WPA2 key caching) — so an outage under X minutes
  is invisible; (b) users fall back to hotspots (business impact =
  degraded, not dead); (c) the *real* mitigation is RADIUS redundancy
  + probe alerts (5-min detection) — fail-closed + fast detection is
  the professional answer, documented as the deliberate choice.
- **Rollback triggers:** any wave with auth-failure >2% sustained 24 h →
  pause, root-cause (usually cert-provisioning or server-cert trust),
  fix, resume; the old SSID stays up *until* decommission day —
  rollback = "still on `CORP-PSK`," not a re-architecture.

## Alternative Solutions

- **PEAP-MSCHAPv2 everywhere:** lowest provisioning effort (passwords
  already exist); accepts the offline-attack class — defensible only if
  MDM were absent; here it isn't.
- **Cloud-managed RADIUS/NAC (cloud RADIUS as a service):** kills the
  redundancy ops burden for a 4-person IT — name it; the local-CA/MDM
  integration must be validated; a legitimate co-winner for ops
  sustainability.
- **WPA3-SAE instead of 802.1X:** better PSK math, still no per-user
  identity/revocation — the *accounting* driver (who did what) decides
  for 802.1X.

## Tradeoffs

- EAP-TLS ops (CA dependency) vs password hygiene: certs make the CA
  critical infrastructure (cs-044's monitoring lesson applies — expiry
  alerts on the RADIUS server certs *and* the CA chain).
- Fail-closed vs fail-open: availability vs the backdoor class — the
  documented fail-closed stance plus redundancy is the defensible pair.
- iPSK for legacy vs 802.1X-capable firmware hunts: iPSK ships now;
  vendor-firmware upgrades may graduate devices to EAP-TLS later —
  keep the inventory tagged.

## Common Mistakes

- Choosing PEAP "for simplicity" with a 96%-MDM fleet (the deciding fact
  unused).
- Single RADIUS server (the outage designs itself).
- PSK fallback "just in case" (the backdoor).
- Client-trust-of-server-cert unpinned (users clicking through cert
  warnings = PEAP's weakness reborn via misconfig).

## Instructor Prompts

- "Why does MDM coverage flip the EAP-TLS cost argument?"
- "Walk the 'both RADIUS servers die' minute: what do users experience?"
- "Which two certificates does your monitoring watch besides client certs?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | EAP mechanics-driven decision; fail-closed rationale |
| Technical accuracy | 25% | RADIUS/MDM/iPSK/dynamic-VLAN mechanics |
| Alternatives considered | 20% | Cloud-RADIUS/PEAP/WPA3-SAE trades |
| Communication | 15% | Rollout plan with triggers |

**Timing:** reveal at 5:00 + 10; the RADIUS-death walkthrough is the
debrief's core.

## CLO Mapping

- **CLO-8** — Enterprise 802.1X architecture and rollout engineering.
