---
case: cs-024
solution-for: modules/module-02-network-threats/case-studies/cs-024-rate-limit-design-app-floods.md
difficulty: intermediate
module: 2
lecture-anchor: L08
clos: [CLO-2]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-024 Solution — Rate-Limit Design (INSTRUCTOR ONLY)

## Model Solution

**Why per-IP fails in both directions:**

- **False-blocks:** one carrier egress IP = 61k req/min of *legit* fans. Any
  per-IP threshold that catches scalpers' 9k req/min catches that carrier IP
  7× over — you'd lock out thousands of fans behind one NAT.
- **Misses:** scalpers spread over ~300 datacenter IPs at 9k/min each —
  individually modest; and when they later rent residential proxies, per-IP
  becomes *indistinguishable from fans by construction*. A key that honest
  users share and attackers can rent is a broken key.

**Three-endpoint policy:**

| Endpoint | Primary key | Threshold (token bucket) | On exceed | Rationale |
|---|---|---|---|---|
| `/search` | **TLS/HTTP fingerprint class + session token** (IP only as backstop) | ~60 req/min per *session*, burst 30; fingerprint-class budget: 400 req/min per fingerprint | serve cached/shaped response → then **JS proof-of-work challenge** | Fans behind one NAT share the fingerprint mix (real browsers); bots share 3 fingerprints → class budget starves bots, not NATs. |
| `/queue` | **session token + fingerprint class** | 1 join per session; re-poll ≤ 12/min/session | over-poll → hold position, serve static status | The queue's job is fairness; the *queue itself* is the rate limiter — don't let bots pre-join via API without a session. |
| `/checkout` | **session token + payment-intent** (never IP) | 3 checkout attempts/15 min/session; hard cap per payment instrument | >3 → step-up (SMS/email confirm), not silent drop | Checkout is expensive *and* fraud-adjacent; false-block costs are highest — use step-up, not drop. |

Backstop layer (edge): per-IP *connection* limits (SYN/conn caps) to stop
volumetric abuse of the TLS stack itself — but never the application limit.

**When scalpers rent residential proxies:** IP, UA, and even fingerprint
diversify; what still separates them is **behavioral token economics** —
they need *many* sessions *per real human operator*, coordinated timing
(on-sale second), and no real conversion (their carts don't pay: 2.1% vs 9%).
So: session-minting rate per *account*, per *payment instrument*, and per
*JavaScript-capable challenge pass* becomes the limiting dimension, plus
conversion-scored reputation (challenge sources whose sessions never
convert). Proxies defeat network keys; they don't defeat the queue's
one-session-per-verified-human economics.

## Alternative Solutions

- **CAPTCHA everywhere:** breaks accessibility and mobile UX; use only as
  the challenge behind fingerprint-budget exceedance, not the front line.
- **Paid/verified-fan pre-registration:** strong fairness control; business
  decision — mention as the structural answer for mega-on-sales.
- **Pure queue-before-any-work (virtual waiting room):** actually the
  strongest single control for the on-sale hour; the design above embeds it
  (`/queue` first, work only after admission).

## Tradeoffs

- Fingerprint budgets vs browser diversity: fingerprint classes must be
  versioned (browser releases change); stale classes lock out new browsers —
  keep budgets generous and challenges cheap.
- Strict checkout limits vs gift-buying/helpdesk scenarios: step-up (prove
  possession of email/phone) beats hard blocks.
- Challenge difficulty vs accessibility: proof-of-work must have a
  non-JS/accessibility fallback path or you've built a wall for disabled fans.

## Common Mistakes

- One global per-IP rule for all three endpoints (the NAT lockout).
- Token bucket omitted → bursty NAT fans trip fixed windows.
- Dropping at `/checkout` (highest false-block cost) instead of step-up.
- Believing fingerprinting is *stable* forever — version drift, and proxies
  with real browsers eventually match fingerprints too; behavioral keys carry
  the long game.

## Instructor Prompts

- "Which endpoint has the *highest* cost of a false positive, and how does
  your design reflect that?"
- "Why is the waiting room itself the strongest anti-bot control for this
  business?"
- "Scalpers buy 5,000 real SIM-verified accounts. Which dimension still
  works?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Both-direction IP failure argument; key-selection logic |
| Technical accuracy | 25% | Token-bucket mechanics; fingerprint-class budgeting |
| Alternatives considered | 20% | Waiting-room/step-up design space |
| Communication | 15% | Clean three-endpoint table |

**Timing:** reveal at 5:00 + 2; the "which endpoint hurts most if you're
wrong" prompt anchors proportionality.

## CLO Mapping

- **CLO-2** — Application-layer flood mitigation design.
