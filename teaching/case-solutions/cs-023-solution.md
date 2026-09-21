---
case: cs-023
solution-for: modules/module-02-network-threats/case-studies/cs-023-botnet-c2-beacon-pattern.md
difficulty: intermediate
module: 2
lecture-anchor: L08
clos: [CLO-2]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-023 Solution — C2 Beacon Pattern (INSTRUCTOR ONLY)

## Model Solution

**Classification: active exfiltration over TLS to attacker-controlled
infrastructure, with beacon-scheduled sessions (a C2-adjacent staging
pattern).** Discriminating flow features:

- **Volume without purpose:** 22 MB/night from a front-desk PC — no
  legitimate nightly job on that host plausibly uploads 22 MB (the scheduling
  app's vendor update is small and separate at 23:30). Purpose-fit is the
  first test; it fails.
- **Infrastructure rotation:** destination IP changed mid-campaign within the
  same /24 while the **DNS name stayed constant** — classic malware CDN-style
  C2 pooling; legitimate vendor endpoints don't rotate like this monthly-new
  name or not.
- **Periodicity with jitter:** ~4 min sessions ±30 s for 40+ minutes — a
  chunked upload loop, not a single "sync."
- **Nightly start ~23:40, after the legit 23:30 job:** the malware anchored
  itself to the host's established nightly activity window — low-attention
  timing. (Riding *adjacent*, not impersonating.)

**Why timing matters for containment:** the upload starts 23:40; the
contractor can plan containment for ~23:15 — *before* tonight's run —
preserving the option to capture one more session with a full-packet tap
(probably not needed: the flow evidence is already decisive) versus
stopping another 22 MB of patient data leaving **now**. Given health-privacy
exposure, the correct answer is **contain before the next run** — pull the
host from the network at end of day; do not wait to "catch it in the act."

**Tonight's containment sequence:**

1. **Network-level isolate `front-desk-2`** (switch port down / quarantine
   VLAN / block its MAC at the firewall) at ~23:15 — before the window.
   Also **block the /24 + the DNS name** at egress for *all* clinic sites —
   the other two clinics may host siblings.
2. **Snapshot before reimaging:** memory capture if tooling exists, disk
   image, and export the full flow records + DNS logs for the 30-day period
   the domain existed — this is the **evidence-preservation step most teams
   skip** (they reimage for tomorrow's shift and destroy the timeline needed
   for the regulator's "what data, when, where" questions).
3. **Scope outward:** identical nightly patterns on the other front-desk PCs
   and clinics (flow search: "sessions every ~4 min, 23:40–00:20, new-metric
   domain") — sibling-hunting before the attacker notices containment.
4. **Rebuild the host from clean media; rotate its stored credentials**
   (scheduling app, any shared accounts). Patch the old Java app stack.

**Regulatory note for the compliance consultant:** 3 nights × ~22 MB of
*unknown* content to attacker infrastructure with patient-data systems
present is a **presumed breach** until proven otherwise; the preserved
evidence (flows, DNS, disk image) is what bounds the notification scope.

## Alternative Solutions

- **"It's the vendor's new metrics/telemetry."** Plausible surface; rejected
  because telemetry doesn't rotate IPs within a /24 under a fresh domain,
  and 22 MB nightly is absurd for scheduling telemetry. Verify by asking the
  vendor for their endpoint IPs — but contain first; asking is not containing.
- **"Wait for EDR to prove intent."** No EDR exists here; waiting is a
  policy answer to a technical emergency.
- **"Block the domain only."** Half-measure: the /24 rotation means the
  campaign continues on the next IP; block name *and* range.

## Tradeoffs

- Contain-before-capture vs capture-in-the-act: with 22 MB/night of patient
  data at stake, ongoing harm outrisks marginal evidence; the disk image
  preserves the malware for later analysis.
- Blocking at egress vs pulling the host only: pulling one host stops that
  host; egress blocks stop *siblings* — do both.
- Reimage timing vs business hours: front-desk PC needed tomorrow morning —
  stage a loaner overnight; do not return the compromised image to service.

## Common Mistakes

- Convicting on periodicity alone (the 23:30 vendor job is also periodic).
- Treating the domain as stable evidence while missing the /24 rotation.
- Reimaging before evidence preservation.
- Forgetting the other two clinics — this is a fleet, not a PC.

## Instructor Prompts

- "What flow feature would a *legitimate* vendor telemetry rollout show that
  this one doesn't?"
- "Why did the malware start at 23:40 and not 02:00?" (anchoring to the
  host's observed rhythm; low attention.)
- "What does the regulator's first question require you to have preserved?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Purpose-fit test; rotation+volume discrimination |
| Technical accuracy | 25% | Flow-evidence reading correct; C2-pooling mechanics |
| Alternatives considered | 20% | Vendor-telemetry hypothesis honestly tested |
| Communication | 15% | Tonight-sequenced containment with preservation step |

**Timing:** reveal at 5:00 + 2; the "what could plausibly be uploaded" prompt
is the purpose-fit anchor.

## CLO Mapping

- **CLO-2** — Beacon/exfil pattern recognition and first-response choices.
