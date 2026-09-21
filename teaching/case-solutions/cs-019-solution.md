---
case: cs-019
solution-for: modules/module-02-network-threats/case-studies/cs-019-session-hijack-indicators.md
difficulty: beginner
module: 2
lecture-anchor: L07
clos: [CLO-2]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-019 Solution — Session Hijack Indicators (INSTRUCTOR ONLY)

## Model Solution

**Hypothesis judgment: session hijack — confirmed.**

- **Not credential stuffing:** no failed-login burst anywhere; the attacker
  never presents a password (03:10 password change rode the *session cookie*).
- **Not confused user:** a `python-requests/2.31` user-agent performed state-
  changing actions (password change, board deletion) from a new IP — users
  don't script their own sabotage at 3 a.m.; also, the real user was browsing
  from their usual fingerprint (`a91c`) *during* the attacker's window
  (02:52 row) — **two simultaneous principals, one account**.
- **Hijack evidence:** attacker actions ride the *cookie session* (03:10/03:12)
  while the real user's fingerprint stays consistent; attacker fingerprint
  (`python-requests`) is uniform; token created 02:44, used 02:47 — the
  session had *token-creation rights*.

**Most likely acquisition vector:** the user's session cookie was stolen
**client-side or in transit before TLS** — most plausibly via the browser
(e.g., infostealer malware on the user's device reading cookie stores, or a
malicious browser extension), because the platform terminates TLS at the edge
(so network sniffing of the cookie is out) and the cookie lacked **SameSite**,
but SameSite governs cross-*site* request attachment, not theft — so the
config evidence that *enabled abuse at scale* is: **30-day session lifetime +
no re-auth on sensitive actions + token-creation rights from a hijacked
session**. State it carefully: the *theft* vector is endpoint-side (not
provable from these logs); the *amplification* is platform-side (provably
config).

**Why 02:44→02:47 matters:** the attacker minted a persistence token *before*
acting, so deleting the session (user's eventual logout) wouldn't evict them —
persistence planning indicates deliberate tradecraft, not experimentation.

**Platform top-4 fixes:**

| # | Fix | Neutralizes |
|---|---|---|
| 1 | **Step-up re-auth (MFA) for sensitive actions** (password change, exports, token creation, deletions) | 03:10, 02:47, 03:15 rows — a stolen cookie alone can no longer do damage |
| 2 | **Fingerprint/IP-anomaly enforcement:** new IP + new UA on a session triggers re-auth or block | 02:47 onward (new IP + UA) |
| 3 | **Shorten session life; rotate cookie on privilege actions** | 30-day window the attacker enjoyed |
| 4 | **Audit trail for token lifecycle + notify on token creation** | 02:44 row went unnoticed until forensics |

## Alternative Solutions

- **"Malware on the real user's laptop" as a separate hypothesis.** Actually
  compatible — it's the *mechanism* of theft, not an alternative to hijack;
  credit students who separate vector-from-classification this cleanly.
- **"Insider with API token"** — rejected: token was created 02:44 from the
  *hijacked session context*; insider-with-existing-token would skip it.
- **"VPNs explain the IP change"** — the real user never changed IP; the
  *attacker* did. Misreads the rows.

## Tradeoffs

- Step-up MFA friction vs security: apply to destructive/sensitive verbs only,
  not every request — preserves usability.
- IP-anomaly strictness: enterprise users on rotating corporate NATs generate
  false positives — fingerprint weighting reduces this.
- Session shortening vs "remember this device" feature: the feature itself
  becomes the persistence layer; redesign it with re-auth anchors.

## Common Mistakes

- Choosing "credential stuffing" because a password change occurred (it rode
  the session).
- Calling SameSite the missing theft control (it's a request-attachment control).
- Ignoring the 02:52 co-presence row — the single cleanest hijack proof.
- Fix list that only shortens sessions (the attacker only needed minutes).

## Instructor Prompts

- "Which single log row, if deleted, would most weaken our case — and what
  does that say about attacker log-awareness?"
- "Why is token-creation-from-session a design smell?"
- "Would MFA at *login* have stopped this? (No — the session was stolen
  post-login. Step-up is the fix.)"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Hypothesis rejection with row citations; co-presence proof |
| Technical accuracy | 25% | Cookie/SameSite/token mechanics correct |
| Alternatives considered | 20% | Vector vs classification kept distinct |
| Communication | 15% | Evidence-mapped fix table |

**Timing:** reveal at 5:00 + 2; the "MFA at login wouldn't have helped" prompt
is the conceptual payoff.

## CLO Mapping

- **CLO-2** — Session-attack evidence analysis and platform hardening.
