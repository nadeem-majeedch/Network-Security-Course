---
case: cs-054
solution-for: modules/module-05-wireless-cloud/case-studies/cs-054-wpa2-psk-wireless-audit-of-a-campus-floor.md
difficulty: advanced
module: 5
lecture-anchor: L17
clos: [CLO-8]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-054 Solution — WPA2-PSK Audit (INSTRUCTOR ONLY)

## Model Solution

**PSK exposure mechanics:** in WPA2-PSK, the passphrase *is* (via PBKDF)
the **PMK** — identical for every client. The 4-way handshake is captured
passively by anyone in radio range; possession of the PSK lets them derive
the same PMK and, with one captured handshake, compute that session's PTK
and decrypt that client's traffic (pairwise keys don't save you when the
secret they derive from is public). Worse, wall-posting makes offline
attack pointless — the visitor just *reads* the secret. Rotation is the
only retroactive control because a leaked PSK cannot be revoked per-user —
there is no identity to revoke; "nobody malicious has it" fails because
(a) you can't enumerate who has it, (b) guests share it onward, and (c)
the threat isn't only visitors — any compromised client's user has it
forever until rotation.

**Findings (ranked):**

| Rank | Finding | Mechanism | Class |
|---|---|---|---|
| 1 | Wall-posted shared PSK across all roles | one secret, no revocation, guest distribution by poster | **architectural** |
| 2 | WPS enabled on 2 APs | offline PIN attack class / registrar compromise; pure config hygiene | config hygiene |
| 3 | Single flat subnet for laptops+sensors+guests | any Wi-Fi client lateral to all others; no role boundary | architectural |
| 4 | PMF disabled | unprotected management frames → deauth/disruption class trivially available (note: *detecting* this needs monitoring, not testing) | config hygiene |

**Migration design:**

- **Phase 1 (this month):** kill WPS (config change, zero user impact);
  enable PMF where client fleet tolerates (laptops yes, sensors per vendor
  matrix); create **`CAMPUS-IOT` SSID**: WPA2-PSK with a *long random
  32+ char* passphrase (not human-memorable, never posted), per-sensor
  PSKs if the vendor supports them, IoT VLAN with allow-listed egress +
  no lateral (cs-028 pattern). Guest SSID: open + portal, zero lateral.
- **Phase 2 (this quarter):** `CAMPUS-ENT` (WPA2/WPA3-Enterprise, EAP-TLS
  or PEAP-MSCHAPv2 against RADIUS/AD) for all 40 laptops; per-user creds
  = revocation, logging, and the end of shared-secret math.
- **Phase 3:** decommission `CAMPUS-PSK` entirely; sensors live on the
  hardened IoT SSID; guests never touch researcher traffic.
- **Culture/policy control:** a written **credential-posting ban** paired
  with a *guest portal that actually works* — wall-posting thrives when
  the sanctioned guest path is hostile; fix the convenience gap, don't
  just forbid the workaround.

## Alternative Solutions

- **Rotate the PSK monthly and call it done:** improves revocation latency
  from "yearly" to "monthly" but keeps the one-secret architecture —
  partial credit only.
- **WPA3-SAE for everything:** sensors can't (PSK-only firmware, and SAE's
  transition-mode dance re-introduces downgrade exposure); laptops yes —
  the fleet reality shapes the answer.
- **Private PSK (iPSK) per device:** excellent middle path where the
  controller maps identity/MAC→per-device PSKs — name it as the IoT-SSID
  upgrade if supported.

## Tradeoffs

- Enterprise rollout cost (RADIUS, cert/provisioning UX) vs PSK hygiene:
  the laptop fleet is small (40) — cost is trivial vs the finding's size.
- IoT SSID strictness vs sensor function: allow-list egress per vendor
  endpoint; sensors that phone home beyond the list are procurement
  findings, not network exceptions.
- PMF with old clients: some fail to associate — the vendor matrix gates
  the phase-1 scope honestly.

## Common Mistakes

- "Stronger password" as the fix (the architecture — one shared secret —
  is the finding).
- Missing WPS despite it being in the evidence (classic config-hygiene
  miss).
- Forgetting the sensor fleet and designing Enterprise-for-all (strands
  30 devices).
- No guest-path fix (the wall-posting culture regrows).

## Instructor Prompts

- "Why does one captured handshake + the wall-posted PSK decrypt that
  client's traffic — walk the key hierarchy."
- "Which finding is a 10-minute fix, and which is a procurement cycle?"
- "What makes the IoT SSID's PSK different in kind from the wall-posted one?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Key-hierarchy mechanics; architectural-vs-hygiene split |
| Technical accuracy | 25% | PMK/PTK, PMF, WPS, SAE-transition correctness |
| Alternatives considered | 20% | iPSK/WPA3 tradeoffs named |
| Communication | 15% | Findings table + phased migration |

**Timing:** reveal at 5:00 + 10; the key-hierarchy walk is the teaching
core.

## CLO Mapping

- **CLO-8** — Wireless security mechanics and migration planning.
