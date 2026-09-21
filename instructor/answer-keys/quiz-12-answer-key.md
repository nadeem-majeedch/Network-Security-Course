---
quiz: quiz-12
type: answer-key
instructor-only: true
distribution: never-publish-to-students
clos: [CLO-11, CLO-12]
marks: 10
status: complete
---

# Answer Key — Self-Check Quiz 12 (Week 13)

1. **B** — reversibility ordering is the discipline; waiting risks the
   incident, rebuild-first destroys evidence.
2. **B** — dwell time = initial compromise → detection (some definitions
   extend to containment; accept if the access→detection core is present).
3. **B** — operational TI = actionable indicators + context for
   detection/response; strategic TI is the board tier.
4. **B** — runbooks pre-decide under calm; A/C/D are incidental.
5. **C** — NetFlow = flow metadata; EDR is endpoint, Zeek is network
   protocol logging, SIEM aggregates logs (not payloads).
6. **(2)** Mechanism: the review converts incident evidence into owned,
   dated control changes — closing the specific path used. Failure mode
   when skipped: the same entry vector recurs (and the org pays twice for
   one lesson).
7. **(2)** The two loss-prone hand-offs: **analyst → SOC lead** (triage
   confidence threshold unclear — "is this real?") and **CISO → legal**
   (the regulatory-clock trigger — teams wait for certainty). Either
   defensible pairing with mechanism.
8. **(2)** Check 1: **local corroboration** — does the indicator match
   observed telemetry (proxy/DNS/EDR) *in context* (right host, time,
   direction)? Check 2: **indicator provenance/age** — is the feed's
   source reliable, is the IOC still current, could it be a benign
   coincidence (CDN/shared infra)? Containment only after the pair.
