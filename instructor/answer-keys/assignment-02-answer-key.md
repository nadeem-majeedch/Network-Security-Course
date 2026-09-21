---
assignment: assignment-02
type: answer-key
instructor-only: true
distribution: never-publish-to-students
clos: [CLO-4, CLO-6]
marks: 100
status: complete
---

# Answer Key — Assignment 2 (TLS Deployment Audit)

> **INSTRUCTOR ONLY.** The lab-range configs embed the findings below;
> grade against the register students *should* produce.

## Expected findings register (the answer core)

| # | Service | Finding | Property weakened | Severity |
|---|---|---|---|---|
| F1 | GitLab + wiki | **Shared wildcard certificate** | Authentication scope — one key compromise covers both hosts | M (H if the wildcard also faces users) |
| F2 | Wiki | **Expired certificate, manual renewal** | Availability (outage) + authentication warnings train click-through culture | H |
| F3 | GitLab | TLS 1.0/1.1 still enabled alongside 1.2 | Confidentiality/integrity — downgrade exposure | H (protocol deprecation) |
| F4 | Registry | CBC-mode suites without AEAD preference | Integrity (record-layer) | M |
| F5 | Registry | mTLS with private CA — but **no revocation check configured** | Authentication lifecycle | M |
| F6 | All | No expiry monitoring/automation | Availability/auth across estate | M |
| F7 | Chain | Wiki chain ships without intermediate (works via client caching only) | Authentication — breaks for some clients | M |

*Students finding F7 (the sneaky chain finding) and arguing click-through
culture (F2's second-order effect) are in the top band.*

## Grading anchors

### 1. Findings register (30)
All seven core findings present with per-service structure = 25+; H/M/L
ratings defensible; "chain findings reported as chain errors" respected.
Submissions that blob everything as "weak ciphers" cap at 18/30.

### 2. Risk analysis (20)
Property vocabulary (confidentiality/integrity/authentication) used
*correctly and by name* per finding = the graded core (10). Realistic
attack/failure per finding (10): downgrade for F3, outage+training for
F2, blast radius for F1, unrevokable mTLS identity for F5.

### 3. Hardening plan (30)
Ordered by risk (not by ease) (10); effort + verification per item (10);
remediation vs compensating distinction used correctly — e.g., disabling
TLS 1.0/1.1 = remediation; shortened cert lifetime + monitoring while
automation lands = compensating (10).

### 4. Sustainability (20)
Named mechanisms (ACME-style automation, config management, monitoring
hooks — vendor-neutral) (10); the "why manual failed" argument: manual
scales with estate size, automation doesn't — expiry is a *when*, not an
*if* (10).

## Traps & misconception notes

- Students recommending "disable TLS 1.0" without a compatibility note
  miss the ops dimension — accept either way if consistency holds, but
  note it.
- "Wildcard certificates are always bad" — over-correction; the finding
  is blast radius + key custody, not prohibition. Cap risk-analysis at
  15/20 if this absolutism appears unqualified.
- mTLS ≠ magic: without revocation checking, a compromised client cert
  stays valid — F5's point.
