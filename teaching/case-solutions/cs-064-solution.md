---
case: cs-064
solution-for: modules/module-05-wireless-cloud/case-studies/cs-064-cloud-egress-policy-authoring.md
difficulty: advanced
module: 5
lecture-anchor: L20
clos: [CLO-13]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-064 Solution — Egress Policy (INSTRUCTOR ONLY)

## Model Solution

**Egress profiles per class:**

| Class | Default posture | Allowed categories | Enforcement | Class trap |
|---|---|---|---|---|
| Stateless APIs (30) | deny-by-default | own SaaS deps (FQDN list), patch endpoints, telemetry | egress proxy (FQDN) + SG fence | API teams forget vendor status-page/webhook endpoints — include webhook *inbound* design note (they call *out* to vendors) |
| Batch/data (12) | deny + endpoints | storage via **private endpoints**, package repos, none-internet otherwise | endpoints (no NAT at all where possible) | the cs-063 class: no internet route is the whole policy; dataset sync via endpoints |
| Third-party integration (10) | deny + explicit | partner API FQDNs **pinned to partner-published IP ranges where published** | proxy + IP pinning where available | partners hide behind CDNs — the pinned-IP ask goes in *contracts*; where refused: FQDN + volume anomaly alerts |
| Legacy/monolith (5) | **logging-first tier** | everything, logged (30-day observation) | proxy observe-mode, SG fence later | can't enumerate deps without observing — policy *earns* its allow-list from telemetry, not fromguessing |
| Build/CI (3) | deny + category | package registries by *category feed* (npm/pypi/maven mirrors), git hosts, artifact proxy | proxy + internal artifact-proxy (cache layer) | registry chaos (1000s of CDN hosts) — the **internal artifact proxy** is the architectural fix: CI talks to *one* FQDN; the proxy pulls the world |

**Exception process (and the lesson):**

| Step | Mechanism |
|---|---|
| Request | template: destination, business owner, why-not-standard, expected volume |
| Risk review | security triage ≤2 days; auto-approve low-risk categories |
| Grant | **TTL (90 days max)**, owner, metrics tag at the proxy |
| Expiry | auto-expire + renewal review (renewal *is* the review); expired = deny with a "request portal" HTTP response |
| Metrics | per-allow hit counts; zero-hit allows auto-expire (dead rules die) |

**The "allow-list incident" lesson:** the earlier attempt failed because
it was **exception-first** (60 teams × guessed lists = outages →
executive rollback). Your design is **onboarding-first**: observe-mode
telemetry *generates* each class's real list (legacy tier explicitly
does this), profiles are versioned policy-as-code with canary
enforcement (one class at a time), and the exception path exists for
the residue — not as the primary mechanism. Process order: observe →
propose per class → canary enforce → strict. The social fix (no
surprise outages) is what makes the technical policy survive.

**FQDN-vs-IP honesty:**

- **What FQDN-allowing at a proxy actually enforces:** the *hostname in
  SNI/Host* (and post-decryption, the URL host) — it is **hostname
  policy, not payload or true-destination policy**. If a partner's API
  shares a CDN hostname with the rest of the world, your "allow
  partner.example" permits the CDN's whole neighborhood *under that
  name*; if a vendor rotates IPs hourly, FQDN-pinning is the *only*
  thing that survives — IP pinning dies.
- So: pin IP ranges **where the partner publishes them** (contractual
  ask), FQDN where CDN-shared, and detect abuse with **volume/novelty
  anomalies per allow** (an allow that suddenly serves 100× traffic is
  an incident, whatever the name says). State in the policy doc:
  "FQDN allow ≠ content allow" — auditors and teams both need that
  sentence.

## Alternative Solutions

- **IP-only egress (no proxy):** strongest semantics for pinned
  partners; dies against CDNs and rots on rotation — viable only for
  the integration class with contractual IPs.
- **Zero egress + private endpoints everywhere:** the maximal design;
  breaks legacy/build classes — the tiering (observe-first for legacy,
  endpoints for data) is the honest gradient.
- **Service-mesh egress policies:** fine inside clusters; the
  *platform-level* egress (NAT/proxy/SG) still needs this policy —
  layers, not substitutes.

## Tradeoffs

- 5 profiles vs 60 bespoke rules: profiles under-fit edge cases →
  exceptions; that's the *intended* pressure (exceptions are visible
  and TTL'd).
- TTL'd exceptions vs ops friction: renewal ceremony is the control;
  auto-renew would hollow it.
- Artifact-proxy build cost vs registry chaos: the proxy pays for
  itself in build determinism alone — security is the bonus.

## Common Mistakes

- Big-bang enforcement (the allow-list incident, again).
- FQDN allow treated as payload-level security (the honesty sentence
  missing).
- Exceptions without TTL/metrics (the swamp).
- No observe phase for the classes that can't enumerate their own deps.

## Instructor Prompts

- "Which class do you enforce last, and what evidence gates it?"
- "Write the one sentence about FQDN allows that belongs in the audit
  doc."
- "What does the zero-hit-expiry rule do to the allow-list's size over
  a year?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Onboarding-first process; observe-to-enforce gradient |
| Technical accuracy | 25% | FQDN/SNI semantics; endpoint/proxy mechanics |
| Alternatives considered | 20% | IP-only/zero-egress/mesh layers |
| Communication | 15% | Profile table + exception lifecycle |

**Timing:** reveal at 5:00 + 10; the FQDN honesty sentence is the
deliverable.

## CLO Mapping

- **CLO-13** — Egress policy engineering with realistic enforcement.
