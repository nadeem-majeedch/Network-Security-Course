# Assignment 2 — TLS Deployment Audit & Hardening Plan (Week 7)

> **Weight:** 5% · **Due:** end of week 7 · **CLO-4, CLO-6**
> **Deliverable:** audit report (4–6 pages) + prioritized hardening plan.
> **Safety:** perform configuration analysis **only** on the course lab
> range or documentation-provided outputs — never probe public sites.

## Scenario (simulated)

You are handed the TLS configuration exports of an internal lab estate
(3 services: GitLab, artifact registry, internal wiki) from the course
range: certificate details, enabled protocol versions, cipher list, and
OCSP/CRL settings. Two services share a wildcard certificate; the wiki's
certificate expired last month and was renewed manually; the registry
uses mTLS with a private CA.

## Tasks

1. **Findings register** (30): for each service — protocol versions,
   cipher strengths, certificate chain health, expiry posture, wildcard
   usage, mTLS setup. Rate each finding (H/M/L) with one-line impact.
2. **Risk analysis** (20): connect findings to the *security properties*
   (confidentiality / integrity / authentication) each weakens, and one
   realistic attack or failure per finding (e.g., downgrade exposure,
   outage-on-expiry, blast radius of a compromised wildcard key).
3. **Prioritized hardening plan** (30): ordered fixes with effort
   estimates (S/M/L) and verification method per fix. Distinguish
   *remediation* from *compensating control* where full fixes aren't
   possible.
4. **Operational sustainability** (20): propose the issuance/rotation
   automation for this estate (names of mechanisms, not vendor pitches),
   expiry monitoring, and the one-slide argument for why manual renewal
   failed here.

## Constraints

- Distinguish encryption vs authentication vs integrity *by name* in the
  risk analysis — this vocabulary discipline is graded.
- Chain-of-trust errors (missing intermediate, expired root in chain) must
  be reported as *chain* findings, not "bad certificate" blobs.

## Submission

PDF or repo Markdown. Include the raw config excerpts as an appendix.
Rubric: instructor materials.
