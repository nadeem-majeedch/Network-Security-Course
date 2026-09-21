---
case: cs-100
title: Capstone Integration — The Full-Scope Incident Walkthrough
difficulty: expert
domain: Multi-stage security incidents
module: 8
lecture-anchor: L32
clos: [CLO-14, CLO-15]
time-estimate: 30 min (10 min reasoning + 20 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-100-solution.md
---

# cs-100 — Capstone Integration: The Full-Scope Incident Walkthrough

> **Simulated scenario.** The incident and estate are fictional; every referenced capability is from this course.

## Difficulty & Domain

- **Difficulty:** Expert · **Domain:** Multi-stage security incidents · **CLO:** CLO-14, CLO-15
- **Est. time:** 30 minutes · **Anchor:** L32 (Capstone Defense & Course Synthesis)

## Scenario

The course's final case is the integration test: one incident, run
start-to-finish, through *every* capability the program built. A
phishing-initiated intrusion into Meridian's estate (the cs-091→
095 arc, now with IR live, ZT phase 2–3 partial, EDR at 100%,
hunt program running). You are incident commander. The deliverable
isn't just containment — it's the **walkthrough**: for each
incident phase, name the course capability it exercises, the
decision, and the evidence basis. This is the defense of the whole
curriculum in one artifact.

## Stakeholders

- **You (IC)** — run the incident.
- **The estate** — IR plan live, ZT pilots on 2 apps, EDR 100%
  servers, SIEM full, hunt baselines fresh, DS cluster per-job
  credentials (phase-2 ZT), legacy tail unsegmented.
- **Board** — will read the post-incident report (cs-094 format).
- **Counsel** — disclosure clock running (cs-090 framework).

## Network Context

- 800 staff, 2 DCs, AWS prod + ds-sandbox (federated, phase-2 ZT),
  12 branches (MPLS + ZT SaaS direct), 30 legacy workstations
  (EDR-less — the known gap), flat-ish user VLANs (segmentation
  deferred).
- Identity: one IdP (phase-2), MFA everywhere except break-glass,
  service accounts inventoried.

## Available Evidence

**The incident, by telemetry:**

| T | Event |
|---|---|
| Day 0 09:12 | phish delivered (proxy: link click, credential page POST) |
| Day 0 09:40 | attacker logs into IdP *with MFA push-approval* (user fatigued — approved) |
| Day 0 09:45 | device check: unmanaged device — **ZT policy: session allowed with read-only app set** (policy gap: finance app not in restricted set) |
| Day 0 10:20 | finance SaaS accessed; 3 invoice records exported |
| Day 0 11:05 | IdP anomaly detection (new-country impossible-travel) — alert fires |
| Day 0 11:40 | session killed; account disabled (SIEM auto + SOC manual) |
| Day 1 | hunt replay (cs-096 H4): token-refresh anomaly found — attacker had a *second* token, refreshable, now revoked |
| Day 3 | export ledger complete: 3 records, 1 individual affected |

## Student Task

1. Produce the **phase-by-phase walkthrough table**: for each
   phase (detection, containment, eradication, recovery,
   post-incident), the course capability exercised, the decision,
   the evidence basis, and what the *pre-program* estate would
   have done differently (the before/after delta — this is the
   capstone's core question).
2. Answer the **MFA-approval question**: the intrusion succeeded
   *through* MFA — what does that teach about the control's
   honest limits, and which two controls (existing in this
   estate) bounded the damage anyway?
3. Answer the **policy-gap question**: the ZT read-only fallback
   allowed the finance app — is that a *policy* failure or a
   *pilot-coverage* failure? Defend the distinction, and give the
   fix for each type.
4. Write the **board paragraph** (cs-094 format): 120 words
   maximum — incident, response, the two honest limits, the ask.

## How to Approach This (Reasoning Scaffold)

- The walkthrough's unit of analysis is the *decision*, and its
  quality dimension is the *evidence basis* — the course's
  through-line (corroboration, reversibility, asymmetry,
  awareness-vs-certainty) is what you're demonstrating.
- MFA stops credential theft, not session/consent theft — the
  honest limit; the estate bounded damage via *device trust*
  (read-only fallback) and *detection* (anomaly + hunt).
- Policy vs pilot-coverage: a policy failure means the rule was
  wrong; a coverage failure means the rule was right but the app
  inventory was incomplete — different fixes (policy redesign vs
  inventory completion), and boards deserve the distinction.

## CLO Mapping

- **CLO-14** — Forensics, recovery, and post-incident learning.
- **CLO-15** — Capstone synthesis of the full curriculum.

## Safety Notes

- Simulated incident; no real IOCs; all controls referenced are
  course-taught concepts.
