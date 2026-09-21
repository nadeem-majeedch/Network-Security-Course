---
case: cs-032
solution-for: modules/module-03-secure-architecture/case-studies/cs-032-ngfw-app-control-policy.md
difficulty: intermediate
module: 3
lecture-anchor: L10
clos: [CLO-4]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-032 Solution — NGFW Application Policy (INSTRUCTOR ONLY)

## Model Solution

**Policy table (TLS inspection currently OFF — enforcement honesty column):**

| Category | Action | Rationale | What you can actually enforce now |
|---|---|---|---|
| Approved SaaS | Allow | Business-critical | Full (SNI high-confidence) |
| Approved video conferencing | Allow, priority QoS | Business need | Full |
| **Unknown video/meeting app (4% staff)** | **Warn + log, review in 30 days** | Small population; may be legitimate client need — ask before banning | SNI-level allow/deny works (host-level) |
| Software updates (signed sources) | Allow | Patching = security | SNI/vendor-domain allow-list |
| Unsigned-update source | **Block or warn+log** pending vendor check | Supply-chain risk | SNI block effective |
| Approved cloud storage | Allow | Sanctioned path | Full |
| **Personal cloud-storage apps** | **Block** | Data-exfil channel with zero business justification | SNI block effective (they're distinct hostnames) |
| Package registries | Allow (dev subnets only, if identity lands later: per-user) | Legit dev need, manageable risk | Subnet-scoped SNI allow |
| **Unknown HTTPS (SNI-only, 800+ SNIs)** | **Default allow + reputation overlay + log** | Blocking SNI-blind breaks business; but risk-feed SNIs (6) block now | **Can enforce:** SNI allow/deny, category feeds, volume/anomaly alerts. **Cannot:** content-level decisions, per-app policy inside shared CDNs |
| VPN/proxy apps | **Block + engage the 11 users** | Policy evasion is the finding; blocking *and* fixing the cause are both required | High-confidence identification → block works |

**The "unknown HTTPS" honest answer:** with SNI-only visibility you can
enforce *reputation* (risk feeds, newly-observed-domain policies,
category-based SNI lists) and *anomaly* (volume/periodicity per SNI), but
you cannot make content-informed decisions or reliably split apps sharing a
CDN hostname. Two compensating options: (1) **selective TLS inspection** for
the low-confidence bucket only (expensive, needs legal/privacy sign-off and
an exclusion list for health/finance/banking categories — propose scoped,
not blanket); (2) **resolve-by-other-means**: per-user agent identity
(zero-trust broker/proxy) or CASB API-side integration for the SaaS apps —
identity at the app's API, not the wire.

**VPN/proxy response — make the sanctioned path win:**
1. Block the 3 apps at the edge (SNI+signatures) *and* engage the 11 users'
   managers: find out what they needed (likely: a blocked-but-legit tool).
   Blocking without asking breeds hotspots.
2. Provide the sanctioned equivalents (documented, one-click: approved VPN
   for contractors, split-tunnel exceptions via change process).
3. Make evasion *visible*: hotspot/USB-tethering shows as "new device type"
   on the edge; NAC/802.1X flags non-corporate adapters; policy pairs the
   block with a route-to-request-portal page ("need this? click here").
4. Fix the *cause*: if the 11 users all needed the same tool, the policy
   wasn't wrong — the catalog was incomplete. Close the loop in 30 days.

## Alternative Solutions

- **Blanket TLS inspection everywhere:** maximally visible but a legal/
  privacy project (works councils, banking/health exclusions, cert-pinning
  breakage); as a *first* move it fails proportionality — selective first.
- **Block all unknown SNI:** secure-sounding; breaks the long tail of SaaS
  (which is exactly where new business apps appear); warn+log is the
  sustainable stance.
- **Per-user identity first, policy second:** sequencing mistake — policy
  value lands in two weeks; identity is a quarter-long project. Pair them.

## Tradeoffs

- Warn+log vs block for borderline apps: warning preserves goodwill and
  surfaces *intent* (who clicks through matters for the follow-up); blocks
  force shadow-hotspot behavior.
- Reputation feeds: false positives break business apps at 2 a.m.; pin
  exceptions with owners and expiry dates.
- QoS for video vs fairness: conferencing priority is business-justified;
  cap it so uploads can't starve updates/backup.

## Common Mistakes

- Byte-share-driven policy (block video because it's 22% — it's approved!).
- Claiming app-level enforcement "with SNI-only" — the honesty column is the
  graded core.
- Blocking VPN users without discovering the unmet need behind them.
- No exception process — every table row needs an owner and a review date.

## Instructor Prompts

- "Which row would break first if the vendor's app moved behind a shared
  CDN hostname?"
- "What does 'allow-degrade' mean technically for video conferencing?"
- "Legal blocks blanket inspection. What's your *scoped* ask?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Risk×need actions; honest SNI-only enforcement limits |
| Technical accuracy | 25% | App-ID mechanics, selective-inspection exclusions |
| Alternatives considered | 20% | Inspection/CASB/identity sequencing |
| Communication | 15% | Table with enforcement-honesty column |

**Timing:** reveal at 5:00 + 2; the honesty column is the transferable skill.

## CLO Mapping

- **CLO-4** — Application-aware policy design with honest capability limits.
