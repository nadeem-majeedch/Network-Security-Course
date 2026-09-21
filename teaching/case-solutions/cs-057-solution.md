---
case: cs-057
solution-for: modules/module-05-wireless-cloud/case-studies/cs-057-evil-twin-ap-detection-and-response.md
difficulty: advanced
module: 5
lecture-anchor: L18
clos: [CLO-8]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-057 Solution — Evil-Twin Response (INSTRUCTOR ONLY)

## Model Solution

**Attack economics & mechanics:** the operator's investment was a portable
device and a cloned portal page — hours, not skills. The payoff was
*credential phishing*: room+surname pairs (loyalty-account takeover
potential, room-charge fraud) and any passwords typed into the clone's
generic forms. **Which guests lost what:** guests whose devices
auto-associated with the twin (stronger RSSI + open SSID match) and then
*typed* credentials into the cloned portal were exposed; guests who
reached real services over TLS with valid certificates were *not*
content-exposed — the twin cannot break TLS, only display phishing pages
and harvest what's volunteered. The honest statement: "exposure = whatever
was typed into a page the twin served; encrypted traffic was not
readable." Also: the twin could serve *captcha-walls* and session-reset
pages to harvest *more* typing — the clone's reach is human attention,
not crypto.

**Notification duty analysis:**

- *Bound the set:* the hotel cannot enumerate twin-associations (no WIPS,
  no logs from the attacker's device). Honest bound: **all guests who
  used Wi-Fi Fri–Sun** (denominator from real-network association logs +
  the twin-association estimate 40–90). Two notification shapes:
  (a) *blanket* to all weekend guests (over-inclusive, safest,
  PR-heavier), or (b) *lobby-weighted* (rooms/folios with lobby-anchored
  sessions) — under-inclusive risk if a guest sat in the restaurant.
  **Recommend (a)** with precise language — the over-claim costs some
  anxiety; the under-claim costs trust and possibly legal exposure.
- *What the notice says:* dates, location (lobby-area Wi-Fi), what
  happened (fraudulent network impersonated ours; some guests may have
  entered credentials into a fake sign-in page), what we did (removed it,
  deploying detection), and concrete actions (change loyalty-account
  password if reused; watch folio/charges; we will re-secure accounts on
  request). *What it does NOT say:* no claim that payment cards were
  compromised (no evidence), no "our network was hacked" framing (the
  hotel's network was *not* the attacker's platform — say it once,
  factually, in the PR line: "a fraudulent look-alike network, not our
  infrastructure, was involved").

**Hardening plan:**

1. **WIPS deployment** (controller-integrated or dedicated sensors): scope
   = lobby + conference + restaurant floors first (twin geography);
   alerts on duplicate-SSID/different-BSSID, OUI mismatch, RSSI-anomaly
   beacons. Budget note: WIPS *containment* off (legal/practical);
   detection-only.
2. **Portal authentication fix (kills the clone):** the phishing worked
   because the portal asks for *room+surname* with no verification —
   re-architect: portal verifies against PMS with a **one-time code
   delivered to the room / key-card tap / booking-reference** — a twin
   cannot fake what it can't validate (the code goes to the *real* room's
   phone). Guests on the twin never receive a code → the clone's page
   visibly fails → detection-by-design. This is the single highest-value
   control in the plan.
3. **Client guidance (3 bullets that work):** (i) "Our portal never asks
   for passwords — only your room code; a password prompt means leave";
   (ii) "Check the padlock — anything sensitive (mail, bank) must show
   HTTPS with no warnings; on our Wi-Fi or any Wi-Fi"; (iii) "Odd
   re-prompts of the sign-in page = report to front desk immediately"
   (turns the missed signal into a sensor).
4. **IR improvement:** front-desk/duty-manager runbook entry: "Wi-Fi
   password/portal complaint → log + escalate to network vendor same
   shift" — the Sat complaints were dismissable only because no path
   existed; make the sensor human.

## Alternative Solutions

- **WPA3/Enterprise for guests:** kills twins-by-open-SSID (twin can't
  match the enterprise auth) but wrecks the guest UX for a hotel — the
  *portal-code* design achieves the anti-phish property with the right UX.
- **Notify nobody, harden silently:** avoids PR; fails duty-of-care and
  any loyalty-account fraud that surfaces later with press — rejected.
- **Over-notify ("payment cards possibly affected"):** maximally cautious
  but factually unsupported — creates card-brand/processor questions the
  evidence can't answer; the notice's discipline *is* the legal answer.

## Tradeoffs

- Blanket vs weighted notification: trust/legal safety vs anxiety volume —
  blanket wins on the facts as given.
- Portal-code UX (extra step) vs clone-immunity: the step *is* the
  control; design it to be 10 seconds (key-card tap) not 2 minutes.
- WIPS cost vs a lobby-only scope: full-property sensing is ideal;
  phased-by-geography matches the threat's actual shape.

## Common Mistakes

- "All guest traffic was exposed" (TLS says otherwise — precision
  matters to the notice's credibility).
- Notification set = "guests who complained" (under-inclusive).
- Client guidance as vague cyber-hygiene instead of three *hotel-specific*
  testable sentences.
- No process fix for the missed complaint signal.

## Instructor Prompts

- "Which control makes the twin's phishing page *visibly fail*? Why does
  that matter more than detection?"
- "Draft the PR one-liner — where exactly does 'hacked' go?"
- "What would the twin operator's next iteration be, and which of your
  controls still holds?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Phishing-not-crypto harm scoping; notification-bound logic |
| Technical accuracy | 25% | Twin mechanics, portal-code design, WIPS scope |
| Alternatives considered | 20% | Enterprise-UX and over/under-notify trades |
| Communication | 15% | Notice language + 3 guidance bullets |

**Timing:** reveal at 5:00 + 10; the "visibly fail" control is the
debrief's headline.

## CLO Mapping

- **CLO-8** — Rogue-AP incident response and control design.
