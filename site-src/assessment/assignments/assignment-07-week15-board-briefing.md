# Assignment 7 — Cloud Security Posture Review & Board Briefing (Week 15)

> **Weight:** 5% · **Due:** end of week 15 · **CLO-13, CLO-15**
> **Deliverable:** posture review (3–5 pages) + one board slide. Solo.

## Scenario (simulated)

You inherit a cloud account: 2 VPCs (prod, sandbox), 14 instances, 3 S3
buckets (one publicly readable, discovered by your own review), security
groups with `0.0.0.0/0` on 22/3389 across 6 instances, no flow logs on
the prod VPC, root account without MFA, and IAM users with long-lived
access keys. The board meets in two weeks. (Same estate class as the
Lab-10 flow-log exercise — extend, don't copy.)

## Tasks

1. **Posture findings** (30): findings register with severity, the
   *misconfiguration class* each represents (identity, network exposure,
   logging/visibility, data exposure), and the realistic first-attack
   path it enables.
2. **Remediation sequence** (25): ordered fix list with effort and
   verification per item; the ordering must respect dependency (root MFA
   and logging *before* network cleanup — why?) and name the one fix that
   changes developer workflows (and how you'd sell it).
3. **Visibility plan** (20): what telemetry to enable first (flow logs,
   audit trails, config recording) with retention, and the one detection
   you'd write immediately (what signal, what threshold).
4. **Board slide** (15): one slide — posture in board language: the risk
   trend, the two honest limits, the ask. Follow the cs-094 structure
   (decidability, no fear, no jargon).
5. **Honesty section** (10): ≤200 words — what this desk review *cannot*
   know (runtime state? identity usage? actual data sensitivity?) and
   what you'd check next.

## Constraints

- The public bucket is the emotional trigger; the *program* answer
  (logging + identity + workflow) is the graded answer — a submission
  that fixes only the bucket caps at 70%.
- Cloud-specific vocabulary (SG vs NACL, flow logs vs audit trail) must
  be used precisely; imprecision is penalized per the quiz-04 standard.

## Submission

PDF/repo Markdown + slide (PDF/PPTX). Rubric: instructor materials.
