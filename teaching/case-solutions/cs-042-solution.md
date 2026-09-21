---
case: cs-042
solution-for: modules/module-04-crypto-protocols/case-studies/cs-042-internal-pki-chain-design.md
difficulty: intermediate
module: 4
lecture-anchor: L13
clos: [CLO-5]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-042 Solution — Internal PKI Design (INSTRUCTOR ONLY)

## Model Solution

**Chain design:**

| Tier | Count | Lifetime | Custody | Why |
|---|---|---|---|---|
| **Root CA** | 1 (offline) | 10 y | HSM/encrypted key on an air-gapped medium; signing ceremonies for intermediate issuance only | root key leak = rebuild the world; offline makes it a non-event. "Offline" for a 1-person lab = key on encrypted USB in a safe, mounted only for intermediate issuance/renewal (annual-ish) — honest operationalization |
| **Issuing: TLS-CA** | 1 | 5 y | online (service account, restricted host) | all `*.lab...` server certs |
| **Issuing: mTLS-CA** | 1 | 5 y | online | client certs for registry↔build mTLS — separation so a *client*-cert compromise can't mint server certs and vice versa |
| **Leaves** | per-service | **90 days** (automated ACME/renewal) | per-service | short leaves = small exposure windows, force automation (the automation is the sustainability story for 1 IT person) |

Code-signing keys live **outside** this chain entirely (separate HSM/token)
— conflating TLS trust with release-signing trust is how a TLS-CA compromise
becomes a supply-chain event.

**Issuance & trust policy:**

- *Requests:* automation only (ACME-style or config-managed CSRs); the lab
  IT person approves via a lightweight policy (name-constrained
  intermediates: TLS-CA constrained to `*.lab.university.example` — even a
  rogue issuance can't leave the namespace).
- *Domain validation:* internal DCN/dns-01 challenge — you control the
  zone; certificate issuance *is* the access control, so constrain + log.
- **Trust to BYOD (the graded constraint) — 3 mechanisms:**
  1. **Lab-managed machines:** root installed via config management/MDM —
     clean, complete coverage. *(Baseline.)*
  2. **Student BYOD:** self-service **trust-profile page** (downloadable
     root + install instructions per OS/browser) with honest warnings about
     what trusting an internal root means; optional: gate *sensitive*
     services to lab-managed clients only (the registry, where MITM risk
     matters) — **tiered trust**: convenience services for everyone,
     crown-jewel services for managed devices.
  3. **Public-CA escape hatch:** put genuinely public-facing services
     (if any) on Let's Encrypt and keep the internal root's surface minimal —
     the less the internal root must be trusted by strangers, the smaller
     the blast radius.

**Revocation + incident posture:**

- **CRL over OCSP for this estate:** small, centralized, 1-person ops; CRLs
  published to a static endpoint (also cached by clients); OCSP responders
  are another always-on service to run — pick the one you'll actually
  operate. (Modern alternative: short leaves + no revocation checking for
  internal mTLS, where 90-day expiry *is* the revocation — defensible and
  simpler; state it.)
- **Issuing-key leak:** revoke the intermediate (CRL), re-issue from root
  (offline ceremony — hours, not weeks), re-trust via the same distribution
  mechanisms; leaves re-issued automatically (90-day fleet churns fast).
  Root leak → full rebuild (the ceremony exists so this stays theoretical).
- **Click-through culture:** the PKI's *purpose* is making warnings rare and
  meaningful — pair the rollout with a campaign: "warnings on lab names are
  now always real findings; report, don't click." The technical fix funds
  the cultural fix.

## Alternative Solutions

- **Buy a managed private CA (cloud MSE/ACM-style):** for 1 IT person this
  is arguably the *right* answer — trade custody control for operability;
  the chain design above remains the mental model either way.
- **Single intermediate (TLS+mTLS together):** fewer moving parts; loses
  the client/server privilege separation; acceptable at this scale if
  name-constraints + leaf profiles are strict.
- **Per-service self-signed + pinned clients:** what exists now; works for
  machines, poisons humans — rejected for the click-through reason.

## Tradeoffs

- 90-day leaves vs ops load: only viable with automation; without it,
  1-year leaves and a renewal calendar (and note the tradeoff honestly).
- BYOD trust-the-root vs tiered-trust: trusting an internal root on
  personal devices is a real (if small) grant of interception *capability*
  to lab infra — tiering sensitive services to managed devices is the
  integrity-preserving middle.
- CRL ops vs short-expiry-as-revocation: short expiry wins for mTLS fleets;
  CRL wins where humans browse (they don't re-auth hourly).

## Common Mistakes

- Online root (one service compromise = PKI reset).
- No intermediate separation (client cert compromise mints server certs).
- BYOD answer = "install the root" without tiering or the capability note.
- Revocation theatre (running OCSP nobody checks) instead of honest
  short-expiry design.

## Instructor Prompts

- "What does 'offline root' mean with one IT person? Operationalize it."
- "Which service would you *not* let BYOD trust, and why that one?"
- "Your mTLS-CA key just leaked — walk the 24 hours."

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Offline-root logic; tiered BYOD trust |
| Technical accuracy | 25% | Name constraints, lifetimes, CRL/OCSP mechanics |
| Alternatives considered | 20% | Managed-CA/single-intermediate options |
| Communication | 15% | Chain table + distribution mechanisms |

**Timing:** reveal at 5:00 + 2; the "walk the 24 hours" prompt is the
incident-posture payoff.

## CLO Mapping

- **CLO-5** — PKI chain architecture and trust distribution.
