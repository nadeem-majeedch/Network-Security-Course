---
case: cs-068
solution-for: modules/module-06-detection-vulnerability/case-studies/cs-068-log-pipeline-coverage-gap-analysis.md
difficulty: advanced
module: 6
lecture-anchor: L21
clos: [CLO-12]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-068 Solution — Coverage Gap Analysis (INSTRUCTOR ONLY)

## Model Solution

**Coverage matrix:**

| Step | Telemetry required | Status | Specific gap |
|---|---|---|---|
| 1. Phishing → credential capture | mail-gateway verdicts + proxy click-through + (ideally) credential-use anomalies | **Partial** | mail gateway logs exist but *click telemetry* (which user clicked when) missing from proxy correlation — user-to-proxy identity join absent |
| 2. VPN login w/ stolen creds | VPN (time, geo, device) + HR leaver/joiner + impossible-travel logic | **Partial→Absent** | VPN logs exist; **device fingerprint + geo fields absent**; HR feed is *daily* (leaver detection latency 24 h = useless for 02:00 logins) |
| 3. Internal recon from VPN session | VPN *post-auth traffic* attribution + east-west flow | **Absent** | firewall logs are deny+summary only — **no allow-flow records**; post-VPN-recon traffic is invisible (the recon *worked*, so denies never fire) |
| 4. SMB staging to file server | file-server share audit + volume baselines | **Absent** | no file-share auditing ingested at all; the staging class is wholly blind |
| 5. Cloud exfil via NAT egress | VPC flow + NAT metrics + class baselines | **Partial** | flow logs exist but no baseline alerting (cs-063's exact lesson) — data exists, detection absent |
| 6. Firewall log tampering | off-box config/change evidence + integrity proofs | **Absent** | firewall logs are *self-reported*; no config-diff feed, no external reconciliation — the sensor reports on itself |
| 7. Persistence via scheduled task | EDR task/autorun telemetry | **Present** | EDR covers laptops properly — the one honest ✓ (say so) |

**The two most dangerous gaps:**

1. **Step 3 (internal recon):** the *classic* over-claim — "we have
   firewall logs" is true and useless: allow-traffic is summarized,
   denies only. Recon that succeeds generates no denies. The tabletop
   team answered "we'd see port scans" because dashboards show deny
   spikes; post-auth recon inside allow-ranges is invisible. **Absent,
   claimed present.**
2. **Step 6 (log tampering):** the meta-gap — every *other* claim rests
   on sources that an attacker (or insider) can silence at the
   firewall/log layer; without off-box integrity evidence, coverage
   claims generally are conditional on the attacker's restraint.
   Over-claiming happened here because *nobody asks a sensor to prove
   it wasn't silenced* in a tabletop.

*Why over-claiming happened (meta-lesson):* coverage was reasoned
**source-first** ("we ingest 14 sources") not **step-first** ("which
fields and correlations does *this step* need?"); dashboards visualize
what exists, so they can't show the class of absence. The fix is the
matrix itself — step-first, field-level, honest statuses.

**Fix backlog:**

| # | Fix | Enables | Cost tier | Order |
|---|---|---|---|---|
| 1 | Enable **allow-flow export** at the firewall (or NetFlow) | step 3 recon detection | config | 1 — cheapest, un-blinds the claimed step |
| 2 | **File-share audit** on the file server + ingest | step 4 staging | project (server config + schema) | 2 |
| 3 | **Off-box firewall config-diff + syslog mirror to second collector** | step 6 tamper-evidence | project | 3 — protects every other claim |
| 4 | VPN log **device/geo fields** + hourly (not daily) HR feed | step 2 | config + project | 4 |
| 5 | **Class-baseline alerts** on cloud flow (per cs-063/065) | step 5 | config | 5 |
| 6 | Proxy↔mail **user-click correlation** | step 1 | project | 6 |

## Alternative Solutions

- **Buy more SIEM storage/features first:** the gaps are *sources and
  fields*, not analytics capacity — procurement solves none of the six.
- **Cover step 1 with awareness-training metrics:** a control, not
  telemetry; the gap remains blind — but pair it with #6 honestly.
- **Full NDR procurement:** would solve 3/4 expensively; the two config
  fixes deliver the majority of step-coverage for a fraction —
  sequencing discipline.

## Tradeoffs

- Fix #1's volume cost (allow-flows are big): filter to internal+VPN
  ranges; the recon class lives there.
- Hourly HR feed vs privacy/process: joins/leavers hourly is a process
  ask, not a technical one — budget the conversation.
- Off-box mirrors add ops surface: the second collector is the *point*
  (tamper target separation) — keep it minimal and hardened.

## Common Mistakes

- Source-level answers in a step-level matrix ("we have VPN logs").
- Marking partial as present (the tabletop's whole lesson).
- Skipping the tampering class (it conditions all other coverage).
- Backlog ordered by ease instead of by claim-criticality (#3's
  config-fix outranks flashier projects).

## Instructor Prompts

- "Which step's coverage claim died on a *field*, not a source?"
- "Why does step 3 generate zero denies — and why did the dashboard
  suggest otherwise?"
- "What makes fix #3 the guardrail for every other row?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Step-first, field-level precision |
| Technical accuracy | 25% | Log-source capabilities correct |
| Alternatives considered | 20% | Procurement-vs-config sequencing |
| Communication | 15% | Matrix + 6-item backlog |

**Timing:** reveal at 5:00 + 10; "dashboards can't show absence" is the
meta-lesson to land.

## CLO Mapping

- **CLO-12** — Detection-coverage engineering at step level.
