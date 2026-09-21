---
case: cs-093
title: Capstone III — Zero-Trust Migration Design (Solution)
difficulty: expert
module: 8
lecture-anchor: L31
clos: [CLO-15]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-093 — Solution: Zero-Trust Migration Design

> **INSTRUCTOR ONLY.** Model solution for cs-093.

## Model Solution

### 1. What zero trust means *here*

**Policy model:** access decisions move from network location to
per-request evaluation: *identity* (who, from which directory
principal) + *device* (managed? compliant?) + *context* (location,
risk signals from SIEM/EDR) + *app sensitivity* — evaluated per
session, enforced at the app, not the perimeter.

**What replaces VPN-centric access:** remote access becomes
per-app (identity-aware proxy / app-level access), not network-
level tunneling; the VPN shrinks to the admin-plane use case
(privileged access), not user access.

**Prerequisite chain (each step unblocks the next):**

| Step | Unblocks |
|---|---|
| 1. **Identity consolidation** — AWS accounts federate to the corporate IdP; DS cluster identities flow from the same IdP with per-job scoping | Per-request decisions have one subject space |
| 2. **Device trust** — managed-device posture feeds the policy engine (EDR present + compliant = device signal) | Conditional access has a second signal; unmanaged-device policy possible |
| 3. **Policy engine + app inventory** — the top-20 app flow analysis becomes the app catalog with sensitivity labels | Policies written against *apps*, not subnets |
| 4. **Per-app enforcement** — IAP/ZTNA in front of pilot apps; ERP gets a low-latency path (see phasing) | The model becomes enforceable without big-bang |
| 5. **Privileged access** — admin-plane moves to the ZT model last (PAM + session recording) | Highest-risk access migrated with the most maturity |

### 2. Migration phasing

**Phase 1 (Q1–Q2): identity + device.** IdP federation for AWS and
the DS cluster (per-job scoped credentials — cs-088's fix at
architecture level). Gate: 100% of AWS access via IdP; device
posture signal live for ≥90% of managed endpoints.

**Phase 2 (Q2–Q3): pilot apps.** Select **2 apps by policy
variety**: (a) analytics platform (AWS, sensitive, remote-heavy —
stresses device + location policies), (b) expense SaaS (low
sensitivity, browser-based — stresses onboarding mechanics and
unmanaged-device policy). Gates: pilot user cohorts ≥95% success
rate on access decisions, no SLO breach, per-request overhead
measured (velocity probe institutionalized: synthetic experiment
runs before/after; ≤10% gate).

**Phase 3 (Q3–Q4): branch + ERP.** Branch handling: MPLS remains
for ERP latency (the SLO is architectural — ERP stays reachable
from branch networks via the existing path *but* requests are
still identity-evaluated at the app tier; location becomes one
signal, not the boundary). 4 internet-breakout sites move SaaS to
direct ZT access (drops hairpin). Gate: ERP p95 ≤150 ms with
identity evaluation on; branch support tickets flat.

**Phase 4 (Y2): privileged access + legacy tail.** Admin plane to
PAM with session recording; the VPN shrinks to break-glass.
Legacy apps that can't do per-request auth get *compensating
segmentation* (the cs-092 design doc finally builds, scoped to
the legacy tail only). Gate: VPN user-population <5% of staff;
legacy compensating controls documented.

**DS-cluster treatment:** cluster access via IdP-issued per-job
credentials + brokered data-lake access (no long-lived cached
tokens) — the guardrail applies: synthetic training-run probe
measures overhead; per-session (not per-request) auth chosen
where per-request breaches 10%.

### 3. What zero trust will NOT fix (honest list)

- **Email/phishing of humans** — ZT shrinks blast radius; the
  initial-access *attempts* continue (paired with: phishing-
  resistant MFA + mail controls).
- **Supply-chain compromise** of trusted update channels (cs-089)
  — ZT does not authenticate *vendor integrity* (paired with:
  update-channel pinning + SBOM process).
- **Data-lake abuse by legitimate identities** — per-request auth
  authorizes the *access*, not the *intent* (paired with: data
  access analytics + egress monitoring).
- **Unpatched/legacy app vulnerabilities** reachable by
  authorized users (paired with: vuln mgmt cadence from cs-092).
- **Insider misuse within authorized scope** — the model's own
  honest boundary.

### 4. Board argument

Phase gates + measured guardrails beat big-bang because: (a) each
gate produces *evidence* (access-decision success rates, SLO
compliance, velocity probe deltas) that de-risks the next
tranche — the board funds outcomes, not faith; (b) rollback is
designed-in (per-app enforcement means per-app rollback); (c) the
guardrail mechanism is institutional, not personal trust — the DS
velocity probe *already exists* from cs-092 and generalizes: any
policy change that breaches a measured SLO rolls back
automatically. Big-bang alternatives fail here specifically: 12
branches + latency-sensitive ERP + a research cluster with a
measured guardrail = too many simultaneous variables.

## Alternative Solutions

- **Product-first (buy ZTNA, retrofit identity):** faster demo,
  weaker model — per-request decisions inherit the AD/AWS split;
  the prerequisite chain exists for a reason.
- **Segmentation-only (build the cs-092 design):** defensible as
  risk-reduction but doesn't deliver the remote-access model the
  board mandated; the two are complementary (legacy tail).

## Tradeoffs

- Per-request vs per-session enforcement: stronger policy vs
  overhead on experiment paths — resolved per-workload by the
  measured guardrail, not by ideology.
- ERP on MPLS with app-level identity: keeps latency SLO while
  surrendering "no trusted network" purity — honest ZT is
  risk-based, not dogmatic.

## Common Mistakes

- Treating ZTNA procurement as the program (product ≠ model).
- Piloting two similar apps (no policy variety proven).
- Forgetting privileged access until last-minute (admin plane is
  the highest-risk access; sequence it deliberately).
- Claiming ZT fixes phishing or insider misuse (it doesn't).

## Instructor Prompts

- "Why is identity consolidation *the* root prerequisite here?"
- "What makes two specific apps a better pilot than the two
  biggest?"
- "Which item on the not-fixed list most surprises the board?"

## Rubric (10 pts)

| Criterion | Pts |
|---|---|
| Policy model + prerequisite chain with unblock logic | 3 |
| Phasing with measurable gates + pilot-variety logic | 3 |
| Not-fixed list + pairings | 2 |
| Board argument (evidence-driven gates, guardrail mechanism) | 2 |

## Safety Notes

- Simulated; no vendor endorsement.
