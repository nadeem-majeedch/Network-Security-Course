---
case: cs-045
solution-for: modules/module-04-crypto-protocols/case-studies/cs-045-self-signed-certificate-risk-assessment.md
difficulty: intermediate
module: 4
lecture-anchor: L14
clos: [CLO-6]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-045 Solution — Self-Signed Cert Triage (INSTRUCTOR ONLY)

## Model Solution

**Triage matrix:**

| Endpoint class | Current risk (mechanism) | Priority | Rationale |
|---|---|---|---|
| Browser-facing self-signed where **users click through** (subset of internal tools) | **Incident-adjacent:** trains humans to accept invalid certs — the click-through habit transfers to real MITM/phishing pages; the cert isn't the breach, the *training* is | **P1** (this quarter, out of the 5-slot capacity first) | Human-trust erosion is the compounding risk; also cheapest win |
| Customer-data APIs with **TOFU/custom trust** | **High:** key-rotation is frozen (pins break), compromise of one endpoint's key is undetectable (no CA oversight, no revocation); MITM at first-use survived | **P1** | Regulated data + no revocation path |
| Customer-data APIs **pinned by config** (ops-managed pin distribution) | **Medium:** acceptable *if* pins rotate via automation and key-compromise detection exists (see decision rule) | **P2** | Defensible permanently if monitored |
| Build/CI self-signed | **Medium-low:** high-lateral-value but machine-only clients; TOFU pain constrains rotation hygiene | **P2** | Automation-friendly migration slot |
| Legacy vendor appliances (10) | **Accept-with-controls:** firmware may not support CA certs; risk is bounded by segmenting + monitoring (below) | **P3 accept** | Capacity realism; compensating controls |
| 6 orphaned-CA certs | **P1 clean-up:** their chain can never validate or revoke — equivalent to self-signed with worse story | fold into P1 slots | |

**Grading the consultant:**

- *Right:* self-signed sprawl is a real finding; browser-facing
  click-through endpoints are genuinely urgent; consolidation onto the
  internal PKI is the correct end-state.
- *Wrong:* "all immediately" ignores (a) capacity (5/quarter — the plan
  takes a year+ regardless of the order form), (b) that some pinned
  self-signed endpoints are *more* defensible than bad-PKI migrations
  (breaking pinned clients in a hasty migration creates outages that push
  teams back to self-signed), (c) the legacy appliances may be *unable* to
  comply — an un-actionable recommendation erodes audit credibility.
- *One-line correction:* **"Sequence by trust-exposure (humans first, data
  APIs second, appliances last with compensating controls), and add
  discovery — today's list of 40 is already stale."**

**Pinning-vs-PKI decision rule:** pinning a self-signed cert is acceptable
**permanently** iff all four hold: (1) clients are *machine-only* (no human
trust decisions), (2) pin distribution is automated (config-managed, not
TOFU), (3) rotation is exercised at least annually (a pin that never
rotates is untestable), and (4) the endpoint is monitored for cert/key
anomaly (fingerprint changes alarm). Miss any one → migrate to PKI.
Monitoring that keeps it acceptable: config-drift alarms on pin stores +
fingerprint-change alerts + the quarterly scan (the missing discovery —
make it a scheduled scan, not a one-off).

## Alternative Solutions

- **Blanket PKI migration ignoring capacity:** fails on ops reality;
  produces shadow workarounds (self-signed *with worse hygiene*).
- **Accept all self-signed, monitor-only:** ignores the human-training
  harm; the P1 class is not monitorable away.
- **Public CA (Let's Encrypt) for internal endpoints:** possible for
  DNS-reachable names — actually a good option for browser-facing internal
  tools *if* the org accepts public DNS records; worth naming the variant.

## Tradeoffs

- Pinning (zero CA dependency, rotation pain) vs PKI (revocation + CA ops
  dependency): the decision rule operationalizes when each trade is right.
- Sequencing humans-first vs data-first: humans-first yields culture wins
  early; data-first reduces regulated risk earlier — the matrix takes
  humans-first because the *training harm* compounds fastest.
- Discovery cadence: quarterly scans add toil but the one-off list is the
  audit's next finding.

## Common Mistakes

- "Self-signed = bad" as the analysis (the mechanism is who-validates-how).
- Ranking by data sensitivity only (misses the click-through class).
- No monitoring story for accepted pins (acceptance without detection rots).
- Migrations that break pinned clients and recreate shadow TLS.

## Instructor Prompts

- "Which of the 22 would you migrate with *zero* client changes, and why
  does that make them good early wins?"
- "What does the lost-CA story teach about *internal* CA key custody?"
- "Why is the click-through class an 'incident' rather than a finding?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Validation-mode-differentiated triage; capacity realism |
| Technical accuracy | 25% | TOFU/pinning/revocation mechanics |
| Alternatives considered | 20% | Public-CA variant; accept-with-controls design |
| Communication | 15% | Matrix + consultant grading crisp |

**Timing:** reveal at 5:00 + 2; the decision rule is the transferable
artifact.

## CLO Mapping

- **CLO-6** — TLS trust-model triage and migration planning.
