---
assignment: assignment-03
week: 9
type: graded
clos: [CLO-5, CLO-7]
lectures: [L15, L16]
lab: Lab-08
marks: 100
weight: 5%
due: end of week 9
status: complete
artifact-type: student-assignment
answer-key: instructor/answer-keys/assignment-03-answer-key.md
---

# Assignment 3 — Remote-Access VPN & Secure Access Design (Week 9)

> **Weight:** 5% · **Due:** end of week 9 · **CLO-5, CLO-7**
> **Deliverable:** design document (5–8 pages) + access-decision table.
> Teams: pairs.

## Scenario (simulated)

A research organization (250 staff, 40 field technicians, 30 external
contractors) currently uses a full-tunnel SSL VPN with password-only
authentication. Field techs use unmanaged tablets; contractors need
access to exactly one reporting application. Leadership wants "modern
remote access" without a rewrite of every application.

## Tasks

1. **Requirements & segmentation of users** (20): define access classes
   (staff-managed, field-unmanaged, contractor) with the trust signals
   each can honestly present (identity, device posture, location). State
   what each class *cannot* prove.
2. **Tunnel & auth design** (25): full-tunnel vs split-tunnel per class
   with justification; authentication scheme (MFA type; phishing-resistant
   where warranted); the one protocol-level choice (DTLS/TLS, IKEv2) you'd
   standardize and why.
3. **Access-decision table** (25): class → resources → conditions (device
   posture, MFA, time) → fallback posture when a condition fails. This
   table is the graded core — it is your zero-trust seed.
4. **Risk register** (20): the four risks of this design (including the
   unmanaged-tablet reality and the contractor's exit process) with
   likelihood/impact and the compensating control for each.
5. **Diagram** (10): access path from each class to resources with
   enforcement points.

## Constraints

- Do not propose "replace everything with product X" — design within a
  conventional VPN gateway plus policy layer; the course's ZT module
  later extends this.
- Split-tunnel arguments must address the *unmanaged device* case
  explicitly (the failure mode from cs-051).

## Submission

PDF/repo Markdown + diagram. Rubric: instructor materials.
