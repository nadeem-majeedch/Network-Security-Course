---
case: cs-091
title: Capstone I — Full Breach-Readiness Assessment
difficulty: expert
domain: Enterprise architecture
module: 8
lecture-anchor: L29
clos: [CLO-15]
time-estimate: 20 min (5 min reasoning + 15 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-091-solution.md
---

# cs-091 — Capstone I: Full Breach-Readiness Assessment

> **Simulated scenario.** The estate and all findings are fictional.

## Difficulty & Domain

- **Difficulty:** Expert · **Domain:** Enterprise architecture · **CLO:** CLO-15
- **Est. time:** 20 minutes · **Anchor:** L29 (Capstone Architecture & Security Assessment)

## Scenario

The capstone opens on **Meridian Health Analytics** (fictional): a
health-data analytics firm — 800 staff, 2 data centers, AWS + on-prem
hybrid, 60-person data-science group. The board has commissioned a
full breach-readiness assessment before a funding round. You are the
lead assessor. This case is the *assessment phase*: inventory the
estate, find the gaps, and produce the ranked findings that the
capstone design phase (cs-092) will remediate.

## Stakeholders

- **Board** — commissioning; wants a defensible gap list.
- **CTO/CISO** — will own the remediation roadmap.
- **DS group lead** — defensive about research velocity.
- **External auditor** — shadowing for methodology.

## Network Context

- Perimeter: NGFW pair at each DC; site-to-site VPN to AWS; remote
  access via SSL VPN (no MFA — a legacy exception for one team).
- Internal: flat 10.0.0.0/16 with VLANs for voice/printed devices
  only; servers and workstations share segments.
- Cloud: two AWS accounts (prod, ds-sandbox); VPC peered; the sandbox
  has no MFA on its root, S3 buckets with research data.
- Detection: SIEM ingests fw + AD; no EDR on 40% of servers; no NDR.
- Governance: asset inventory is 70% accurate; no live IR plan
  (draft from 2 years ago).

## Available Evidence

**Assessment inputs:**
- Architecture diagrams (aspirational, not as-built).
- Firewall rulebase: 3,200 rules, 28% with "any" source, last
  reviewed 3 years ago.
- Vulnerability scans (quarterly, authenticated on 60% of assets).
- Last 2 pen tests (18 and 30 months ago) — findings list, not
  remediation status.
- DS group: 4 S3 buckets "temporarily" public ≥6 months; notebooks
  with cached credentials in a shared repo.
- AD: 41 accounts with domain-admin, 6 service accounts with
  PasswordNeverExpires.
- MTTD last 3 incidents: 34, 41, 19 days.

## Student Task

1. Produce the **assessment plan**: what you examine in what order,
   and *why that order* (which dependencies make evidence
   collection sequential?). Constraint: 2 assessor-weeks.
   Constraint: 2 assessor-weeks.
2. Produce the **findings register** (10–14 findings) with, per
   finding: evidence, affected asset scope, risk rating with
   quantitative justification, and the capability it belongs to
   (prevent/detect/respond).
3. Make the **priority argument**: the board funds 3 findings this
   quarter — which 3, and why those *given the MTTD history*
   (not just severity scores)?
4. Answer the **methodology question**: what makes this assessment
   *defensible* to the shadowing auditor (evidence standards,
   reproducibility, scope honesty)?

## How to Approach This (Reasoning Scaffold)

- Readiness is a *capability stack*: prevent → detect → respond.
  A finding's risk is not just likelihood × impact but *how long it
  goes undetected* — the MTTD history (19–41 days) is the multiplier
  that makes detection gaps rank above some prevent gaps.
- Evidence quality varies (aspirational diagrams, stale scans):
  every finding must state its evidence vintage — the auditor is
  shadowing exactly this.
- Prioritization is portfolio logic under a budget, not a sort by
  CVSS — dependencies and detection-multiplier dominate.

## CLO Mapping

- **CLO-15** — Capstone synthesis: assessment, prioritization, defense.

## Safety Notes

- Simulated estate; no live testing described.
