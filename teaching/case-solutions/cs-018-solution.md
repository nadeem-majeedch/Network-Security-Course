---
case: cs-018
solution-for: modules/module-02-network-threats/case-studies/cs-018-internal-mitm-evidence-fixes.md
difficulty: beginner
module: 2
lecture-anchor: L07
clos: [CLO-2]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-018 Solution — Internal MITM (INSTRUCTOR ONLY)

## Model Solution

**Attack sequence reconstruction:** classic **ARP-spoofing on-path position
attempt** against gateway `.1` (3 rapid spoofed replies at 0:35 = tool
signature), from a Linux laptop (DHCP fingerprint) — physically plausibly on
the **break-room switch** (unmanaged, against policy — hence "appearing on
the wrong uplink" in the capture geography). The attacker achieved: a brief
**on-path position** for `.31`'s traffic (0:35–1:10), visibility of TLS
handshake *metadata* (SNI `teller.internal.bank.example`, timing, sizes), and
the ability to drop or delay the session. The attacker **failed** to achieve
content access: the kiosk browser rejected the interception's certificate
(self-signed impersonator not trusted by clients), producing the warning
tellers saw. The session died; no data was surrendered.

**Compliance answer (precise):**

- **Customer *content*: not exposed.** TLS certificate validation held; the
  app's traffic remained encrypted end-to-end (the interception presented an
  untrusted cert, which was refused).
- **Exposed:** metadata only — SNI, IP/port, timing, packet sizes — and the
  *fact* of teller sessions (who was active when). Availability impact:
  session interruptions.
- **Caveat to document:** had the app been plaintext (HTTP), the same 35
  seconds would have exposed full teller-session content including customer
  lookups. The exposure boundary is TLS's, not the network's — and the
  *self-signed cert culture* is why tellers habitually see warnings and could
  have click-through-trained themselves on a kiosk without the block policy.

**Fix list:**

*Must-do-now (this week):*
1. **Remove/lock down the break-room unmanaged switch** (policy + physical) —
   eliminates the rogue access point for this attack class.
2. **Enable DAI + DHCP snooping** on branch switches that support it; disable
   the unmanageable ones — kills ARP on-path positioning.
3. **Disable click-through possibility entirely** (kiosk policy already did;
   extend to all endpoints) + teller-app cert trust via **internal PKI**
   (stop self-signed; issue from the internal CA so warnings are *always*
   meaningful).

*Must-do-this-quarter:*
4. **802.1X NAC** on the branch — unknown laptops can't join the LAN at all.
5. **Branch egress/segmentation review** — teller VLAN separated from
   guest/printer/general VLANs.
6. **Encrypted internal protocols everywhere** (internal TLS with real CA
   chain, SMB3) so future on-path attempts see nothing useful *even when*
   validation fails open somewhere.

## Alternative Solutions

- **Classify as "equipment malfunction."** Contradicted by the crafted
  3×-reply burst + device fingerprint; misclassification would skip the
  laptop hunt.
- **Hunt the laptop before fixing switches.** Wrong order — the laptop may
  return or relocate; config fixes are permanent regardless of the actor.
- **Buy an IPS.** An IPS with ARP-spoof signatures helps detection, but the
  gap here is *trust hygiene and L2 hardening* — cheaper fixes first.

## Tradeoffs

- Internal PKI rollout effort vs self-signed status quo: PKI is the permanent
  fix for warning-fatigue; self-signed + pinned kiosk is defensible for a
  single app but doesn't scale to 40 internal services.
- DAI on old switches may require replacement — weigh hardware refresh vs
  segmentation+802.1X-first sequencing.

## Common Mistakes

- Telling compliance "data was compromised" (it wasn't — validation held).
- Reading the certificate warning as the *attack* rather than the *defense working*.
- Missing the capture-geography clue (traffic on the wrong uplink).
- Fix list without the break-room switch — the access point that made it all possible.

## Instructor Prompts

- "What exactly did the attacker see in the ClientHello, and why does SNI
  leak even under TLS?"(foreshadows ECH, L16.)
- "Which single fix converts the tellers' warning from noise into signal?"
- "Why is 'the kiosk blocked it' not a reason to do nothing?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Sequence reconstruction; TLS content-vs-metadata boundary |
| Technical accuracy | 25% | ARP tool-signature, capture-geography, kiosk mechanics |
| Alternatives considered | 20% | Classification and sequencing alternatives weighed |
| Communication | 15% | Compliance-ready precision |

**Timing:** reveal at 5:00 + 2; the compliance answer is the graded center —
precision beats volume.

## CLO Mapping

- **CLO-2** — MITM mechanics, TLS boundary analysis, layered fixes.
