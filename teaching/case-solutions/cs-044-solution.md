---
case: cs-044
solution-for: modules/module-04-crypto-protocols/case-studies/cs-044-expired-certificate-outage-post-mortem.md
difficulty: intermediate
module: 4
lecture-anchor: L14
clos: [CLO-6]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-044 Solution — Expired-Certificate Post-Mortem (INSTRUCTOR ONLY)

## Model Solution

**Post-mortem:**

*Summary line:* An internally-issued mesh certificate expired unnoticed
because rotation was disabled and expiry tracking lived in a personal
spreadsheet; strict TLS validation (correctly) turned expiry into a
2-hour payment-path outage.

*Timeline highlights:*
- 09:14 cert expiry → TLS verify failures (no cert-specific alerting).
- 09:58 stale spreadsheet discovered (wrong row — the tracking artifact was
  the incident).
- 11:10 manual re-issue fully deployed — recovery gated on human cert
  handling, not on any system.

*Root cause:* certificate rotation disabled at launch and never revisited —
expiry management was a manual process owned implicitly by one person.
*Contributing causes:* 825-day lifetime (made the process invisible),
spreadsheet tracking (no system of record), no expiry monitoring, on-call
runbook didn't mention cert handling.

*What worked:* (1) **strict peer validation** — the mesh refused expired
certs rather than failing open; a softer config would have silently
downgraded security instead of paging anyone; (2) **log observability** —
TLS verify errors were identifiable within 22 minutes; diagnosis wasn't the
long pole, recovery was.

**Why 825 days *created* the incident:** certificate lifetime is a
*memory-duration contract* — it defines how often the organization must
demonstrate it still knows where its certs live. At 90 days, automation is
mandatory ( humans can't renew weekly), and any drift surfaces within a
quarter; at 825 days, the renewal event falls **past the tenure** of the
person who chose it (he left at ~month 12), past the attention of the team,
and lands on an on-call who has never seen the process. Long lifetimes
don't remove renewal work; they concentrate it into rare, orphaned events.
The "reduce toil" instinct inverted: the toil was deferred and compounded,
then paid at incident rates.

**Fix set:**

1. **Automation:** enable the mesh's built-in rotation (it existed!) —
   24-hour or 90-day leaves from the internal CA, ACME-style issuance for
   internal services; the edge team's Let's Encrypt pipeline becomes the
   template, proving the org already runs this pattern.
2. **Monitoring:** metric = `minimum_days_to_cert_expiry` across all mesh
   workloads, exported from the mesh control plane; **alerts at T-30d
   (warning) and T-7d (page)** — plus a synthetic TLS-handshake check
   booking→payment every minute (detects *any* cert/chain problem, not just
   expiry).
3. **Process artifact that survives people:** the cert inventory becomes
   *generated* (from the CA's issuance records, not a spreadsheet), reviewed
   weekly in ops sync, with a runbook entry "cert expiry playbook" linked
   from the on-call rotation doc — the system of record is the CA itself;
   the artifact is the *automation*, not a document.
4. (Culture, one line:) post-mortem action "disable nothing at launch
   without a revisit date" — the rotation feature was disabled as
   untested and nobody owned the revisit.

## Alternative Solutions

- **Buy a managed cert/CA service:** removes issuance toil; the expiry
  *monitoring* and synthetic checks remain your job regardless — vendors
  reduce the class, not the duty.
- **Longer automation-test cycle instead of enabling rotation:** keeping
  long certs until rotation is "proven" repeats the pattern (deferral);
  better: enable rotation in *staging* this week, prod next.
- **Fail-open on expired internal certs:** "availability fix" that trades a
  loud outage for silent downgrade — the anti-solution worth naming and
  rejecting explicitly.

## Tradeoffs

- Short leaves (24 h) vs incident blast radius during CA outage: short-lived
  certs make the CA a dependency — pair with cached fallback leaves or
  accept the tradeoff consciously.
- Spreadsheet vs generated inventory: generated wins; but note the tradeoff
  (one more integration) that made the spreadsheet tempting.
- Alert thresholds: T-30/T-7 assumes 90-day leaves; with 24-hour leaves the
  thresholds become hours — threshold must track the lifetime model.

## Common Mistakes

- "Human error" as root cause (the disabled automation *is* the cause).
- Fixes without monitoring (automation without T-30d alerts repeats this).
- No "what worked" section (blame-heavy post-mortems don't teach).
- Missing that the spreadsheet was the *system of record* failure.

## Instructor Prompts

- "At what certificate lifetime does 'spreadsheet tracking' statistically
  guarantee an incident?"
- "Which fix detects a *chain* problem (not expiry) — and why does that
  matter?"
- "Who owns the revisit date for every disabled security feature?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Lifetime-as-memory-contract argument; what-worked section |
| Technical accuracy | 25% | Rotation/monitoring/synthetic-check mechanics |
| Alternatives considered | 20% | Managed-CA/fail-open rejection reasoning |
| Communication | 15% | Post-mortem sections as specified |

**Timing:** reveal at 5:00 + 2; the "statistical guarantee" prompt is the
quantitative hook.

## CLO Mapping

- **CLO-6** — TLS/PKI operational failure analysis.
