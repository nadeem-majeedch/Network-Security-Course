---
case: cs-007
solution-for: modules/module-01-network-foundations/case-studies/cs-007-dns-resolution-misdirection.md
difficulty: beginner
module: 1
lecture-anchor: L03
clos: [CLO-1]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-007 Solution — DNS Misdirection (INSTRUCTOR ONLY)

## Model Solution

**Localization:** the fault is at the **authoritative DNS layer** — specifically
the **zone's A record was changed via the registrar/DNS platform API** with a
stolen/misused credential ("ci-deploy" API key). This is **DNS hijacking**
(specifically an authoritative-level redirect via credential compromise —
sometimes called a registrar/zone hijack). Not on the application side; not a
resolver cache-poisoning case (the authoritative data itself is wrong).

**Why "some customers fine":** recursive resolvers cache the A record for
**TTL 86400 s = 24 h**. Resolvers that had the good answer cached (or whose
administrators flushed) serve it; resolvers that fetched after 10:59 cache the
bad answer for up to 24 h. Mixed answers across ISPs and over minutes = TTL
staggering + partial cache expiry, not per-user randomness.

**Response order:**

1. **Fix the record** at the authoritative host (revert A to 198.51.100.23)
   and **rotate/revoke the "ci-deploy" API key** — stops new poisoning and
   removes the vector. Fastest containment: correct data + dead credential.
2. **Lower TTL** to 300 s while recovery proceeds — so subsequent corrections
   propagate in minutes, not 24 h. (TTL changes themselves propagate on the
   old TTL — a classic wrinkle worth naming.)
3. **Notify customers to flush local caches / restart their resolvers**, and
   have the SaaS company evaluate credential reset for users who reached the
   impostor page — because their browsers may have auto-filled credentials
   into the impostor host.

**Third-place honorable mention:** check registrar account email/2FA — the
API key had to be *obtained* somehow; treat the registrar account as
potentially compromised, not just the key.

## Alternative Solutions

- **Treat as resolver cache poisoning, notify ISPs.** Rejected: the
  authoritative record history shows the origin of the bad data; ISP
  notification would have been the answer if the zone data were clean.
- **Take the domain offline "until safe."** Overreaction: correct data +
  short TTL + credential rotation is sufficient; downtime amplifies harm.
- **Deploy DNSSEC immediately, mid-incident.** DNSSEC is the right
  *structural* hardening (it makes spoofed authoritative answers detectable),
  but it's a design project (key ceremony, DS records, signer ops), not a
  5-minute response — the debrief should land it as follow-up work.

## Tradeoffs

- Fix-first vs forensics-first: revert record now, then pull API audit logs
  (they'll survive); delaying revert to "preserve state" extends customer harm.
- Revoke the key vs keep it for CI continuity — revoke; the pipeline can be
  re-keyed; the attacker's access cannot be assumed dead otherwise.
- 24 h customer-cache reality: notification is a mitigation, not a fix — set
  expectations with the SaaS company.

## Common Mistakes

- Calling it cache poisoning (the authoritative data itself was altered).
- Missing the API key as the vector and jumping to "registrar breach."
- Ignoring the TTL mechanics behind the partial impact.
- Skipping credential resets for users who hit the impostor page.

## Instructor Prompts

- "Where does the 86400 TTL *you inherited* come from, and who chose it?"
- "What would DNSSEC have changed here — and what not?"
- "The API key was used 8 days ago too. What does that imply about dwell time?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Correct layer localization + TTL mechanics |
| Technical accuracy | 25% | Hijack-vs-poisoning distinction; TTL propagation nuance |
| Alternatives considered | 20% | Rejected alternatives with reasons |
| Communication | 15% | Ordered response with what-each-contains |

**Timing:** reveal at 5:00; the DNSSEC "what it changes/not" prompt bridges to
L13–L14 (crypto and TLS trust models).

## CLO Mapping

- **CLO-1** — DNS mechanics → attack localization and response ordering.
