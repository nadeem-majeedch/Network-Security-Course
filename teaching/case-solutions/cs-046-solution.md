---
case: cs-046
solution-for: modules/module-04-crypto-protocols/case-studies/cs-046-tls-downgrade-incident-analysis.md
difficulty: advanced
module: 4
lecture-anchor: L14
clos: [CLO-6]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-046 Solution — TLS Downgrade Incident (INSTRUCTOR ONLY)

## Model Solution

**Mechanism:** the service runs **two TLS listeners**; the policy change a
year ago scoped to the primary listener only. The legacy listener (second
IP, legacy DNS name, unchanged config) still negotiates TLS 1.0/1.1 — and
the scan, which probes *by hostname*, found it. S1 vs S3 proves the
policy is **listener-scoped**: identical client capabilities, different
outcomes by destination name → the "service" is actually a fleet of
endpoints with divergent configs. The wildcard cert (valid) on the legacy
listener makes it look legitimate to casual inspection — cert validity ≠
policy compliance.

**Real exposure (honest quantification):**

- *What TLS 1.0 on this endpoint enables:* negotiation of old protocol
  version with whatever ciphers the legacy listener still allows. Modern
  mitigations have retired the headline attacks: BEAST is mitigated
  client-side (1/n-1 splitting) in every current browser/library; POODLE
  was SSLv3; padding-oracle (Lucky13-class) is library-patched. **No
  practical passive/active break of TLS 1.0 with AEAD-or-patched-CBC
  suites exists for an attacker in 2026.**
- *Where actual danger could arise:* (a) if the legacy listener's cipher
  list includes **export/RC4/NULL/anon** suites (verify — the dump shows
  protocols, not ciphers; the assessor's next question is exactly this);
  (b) **downgrade-to-1.0 for protocol-strip** scenarios where a *mitm*
  forces 1.0 to exploit a *then-weak* configuration — relevant only with
  on-path position and weak ciphers; (c) compliance/regulatory exposure:
  PCI DSS requires disabling ≤1.1 — the finding is real *as a finding*
  even if exploitability is low.
- *Reachability:* the legacy hostname is public-DNS-resolvable — anyone can
  attempt; exposure is not gated by "partners only."
- Verdict: **danger = low-to-medium, conditionally** (pending cipher
  audit); **finding = definite.** Distinguishing these is the fraud
  team's answer: no evidence of exploitation path with current suites,
  but the config is prohibited and must die.

**Fix + governance pair:**

1. *Technical:* set the legacy listener to `TLS1.2, TLS1.3` (or retire the
   listener and its DNS record entirely — the migration it served ended a
   year ago; decommission is the better answer); audit its cipher list in
   the same change; re-scan.
2. *Governance:* **config-as-code with listener inventory** — every TLS
   listener generated from a central template (protocol/cipher policy
   version-controlled); a scheduled **external surface discovery** (cert
   transparency + DNS + port scan of owned ranges) reconciles "listeners
   that exist" vs "listeners in config management" — drift pages the
   gateway team. The partner-migration lesson: temporary listeners need
   **retirement dates in the config itself** (annotations the reconciler
   enforces), because "temporary" outlives every team that remembers why.

## Alternative Solutions

- **Keep 1.0 with IP-allowlisting (partners-only):** technically defensible
  for a legacy partner; PCI still prohibits ≥1.0 for new deployments and
  expects documented exceptions with comp controls — viable only as a
  dated exception, not the answer.
- **Kill the DNS record only (keep listener):** the IP remains
  reachable/cert-valid; half-measure; decommission both.
- **Front with a modern proxy and forbid direct legacy-listener access:**
  adds a hop and moves the policy problem; fine if decommission needs a
  partner-notification window.

## Tradeoffs

- Immediate hard cut vs partner-notification window: legacy partners on
  1.0 break loudly — coordinate; the migration ended a year ago, so any
  partner *still* needing it is a finding of its own.
- Decommission vs remediate: decommission removes the class; remediation
  keeps the sprawl.

## Common Mistakes

- "TLS 1.0 = broken, breach imminent" (no exploit path quantified).
- "Config is right, scanner wrong" (listener-scope blindness).
- Fixing the listener without the inventory/discovery governance (the
  class recurs).
- Ignoring the cipher-list unknown (protocols ≠ ciphers).

## Instructor Prompts

- "Which evidence line *proves* listener-scoped policy — and what would
  disprove your theory?"
- "Write the fraud team's two-sentence exposure answer."
- "What config annotation would have auto-expired this listener?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Listener-scope reconstruction; exposure-vs-finding split |
| Technical accuracy | 25% | Protocol/cipher/BEAST-class honesty |
| Alternatives considered | 20% | Exception-path and proxy options |
| Communication | 15% | Assessor-ready and fraud-ready answers |

**Timing:** reveal at 5:00 + 2; the S1-vs-S3 comparison is the reveal.

## CLO Mapping

- **CLO-6** — TLS configuration mechanics and exposure assessment.
