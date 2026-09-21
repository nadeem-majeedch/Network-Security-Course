---
case: cs-009
solution-for: modules/module-01-network-foundations/case-studies/cs-009-mixed-content-downgrade-exposure.md
difficulty: beginner
module: 1
lecture-anchor: L04
clos: [CLO-1]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-009 Solution — Mixed Content & Downgrade Exposure (INSTRUCTOR ONLY)

## Model Solution

**Exposure inventory:**

| # | Exposure | Severity (open-Wi-Fi login) | Why |
|---|---|---|---|
| 1 | HTTP-loaded jQuery on an HTTPS page | **Critical** | Script = code execution in page origin. On-path attacker can replace it (or deny it), stealing credentials or rewriting the login flow. TLS on the page does not protect script fetched over HTTP. |
| 2 | No HSTS | **High** | First-request exposure: a new visitor typing the hostname goes HTTP first; on-path attacker can intercept/stripe the redirect (serve their own page, or keep the session plaintext). |
| 3 | Plaintext 302 redirect | **High** | The redirect is unauthenticated and unencrypted — it's attacker-editable. "We redirect everything" is not protection; the redirect *is* the attack surface. |
| 4 | Cert expires in 60 days | **Low (for this exercise)** | Operational hygiene; renewal automation question. |

**HTTP-script precision:** the on-path attacker **can** modify or replace the
script (it arrives unauthenticated), i.e., code execution in the page's origin
— full credential theft from the login form. The attacker **cannot** read or
forge the parts of the page delivered over TLS, and cannot *directly* tamper
with the HTTPS POST itself — but doesn't need to: controlling the script that
*reads the form before submission* is equivalent.

**Minimal fix list (priority order):**

1. **Load jQuery (and all subresources) over HTTPS** — kills the critical
   exposure; usually a one-line change + CDN URL update.
2. **Issue HSTS** on all responses (`max-age` ramp, `includeSubDomains` where
   safe) — converts first-request exposure into remembered-policy protection
   after first *clean* visit; document the ramp (start 300 s, raise to 31536000).
3. **Kill the HTTP listener or redirect via 301 + HSTS preloading
   consideration** — defense in depth for the unredirected-first-request case.

## Alternative Solutions

- **CSP `upgrade-insecure-requests`** as a band-aid for mixed content —
  legitimate hardening layer, but it fixes the symptom (browser-side rewrite),
  not the source config; use in addition, not instead.
- **SRI on the CDN script** — protects against a *compromised CDN* for
  HTTPS-loaded resources, but SRI cannot verify HTTP-loaded script against
  tampering on-path (the hash check happens after delivery — attacker-modified
  content with matching-hash-blocked delivery still yields broken page, not
  protection... wait — hash mismatch blocks execution. SRI *does* help: a
  modified script fails the integrity check and doesn't run). Nuanced answer:
  SRI + HTTPS + CSP is the belt-and-braces stack; none alone suffices.

## Tradeoffs

- HSTS ramp vs instant max: a wrong `includeSubDomains` can break sibling
  subdomains (mail, legacy apps) — hence the ramp.
- CDN dependency vs self-hosting the script: CDN gives edge performance and
  shared cache, but adds a supply-chain trust point (mitigate with SRI).
- Preload list: strongest first-visit protection, but entry/exit is slow and
  public — a commitment.

## Common Mistakes

- "HTTPS everywhere so we're fine" — page TLS doesn't cover HTTP subresources.
- Confusing the redirect with protection: unauthenticated redirect = attack surface.
- Proposing to "validate the script hash" without SRI (nothing validates it
  unless you add the attribute).
- Rating cert expiry as the headline finding.

## Instructor Prompts

- "Why is script different from an HTTP-loaded image, severity-wise?"
- "What does an attacker do with the plaintext redirect on first visit?"
- "Which fix removes the critical exposure with the least operational risk?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | TLS-boundary precision on the script exposure |
| Technical accuracy | 25% | HSTS/redirect/SRI mechanics correct |
| Alternatives considered | 20% | Layered stack named with roles |
| Communication | 15% | Priority-ordered fix list with reasons |

**Timing:** reveal at 5:00; use the image-vs-script question to anchor why
*what* crosses the boundary matters, not just *how* it's transported.

## CLO Mapping

- **CLO-1** — Web-protocol exposure analysis.
