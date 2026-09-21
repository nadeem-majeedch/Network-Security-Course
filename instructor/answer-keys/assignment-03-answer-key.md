---
assignment: assignment-03
type: answer-key
instructor-only: true
distribution: never-publish-to-students
clos: [CLO-5, CLO-7]
marks: 100
status: complete
---

# Answer Key — Assignment 3 (Remote-Access VPN Design)

> **INSTRUCTOR ONLY.** The graded core is the access-decision table;
> model shape below.

## Model access-decision table (the answer core)

| Class | Resources | Conditions | On condition failure |
|---|---|---|---|
| Staff (managed) | Full internal estate | MFA (phishing-resistant) + compliant device posture + managed install | Read-only web subset; no admin planes |
| Field tech (unmanaged tablet) | Work-order app + document store only | MFA + device attestation (MDM-enrolled or app-level pinning) + per-session tokens | Browser-isolated access only; no data download |
| Contractor | One reporting app | MFA + named-account + time-boxed grant + brokered access (no network-level tunnel) | Deny; expiry is default |
| Any class | Admin/management planes | Jump host + phishing-resistant MFA + session recording | Never fallback — deny |

**Full marks require:** per-class *fallback posture* (not just deny), and
the contractor class on **brokered/app-level access — not network
tunnels** (network access for a one-app need is the classic over-grant).

## Grading anchors

### 1. Requirements & user classes (20)
Trust signals stated *with their limits* ("unmanaged tablet cannot prove
posture, only app-level attestation") = top band; classes without honest
limits cap at 14/20.

### 2. Tunnel & auth design (25)
Split/full per class with the unmanaged-device argument (10); MFA type
matched to risk — phishing-resistant for admin plane, accept push+number
for staff, *not* SMS anywhere (10); one protocol choice justified
(IKEv2/DTLS for roaming-reconnect behavior is the expected shape) (5).

### 3. Access-decision table (25)
As model above. Fallback column present = 10; contractor-not-tunneled =
5; admin-plane separation = 5; conditions measurable = 5.

### 4. Risk register (20)
The four expected risks: (1) unmanaged tablet bridging untrusted LAN
(cs-051's split-tunnel failure), (2) contractor exit — access outlives
the contract without default-expiry, (3) MFA fatigue/push-approval (the
cs-100 lesson), (4) credential reuse on the password-only legacy path
during migration. L/I + compensating control each. Substituting realistic
alternatives with equal rigor: full credit.

### 5. Diagram (10)
Enforcement points match the table (cross-check two rows); brokered
contractor path visible.

## Trap notes

- "Full tunnel for everyone" — safe-looking but fails the field-tech
  reality (tablets can't all run full-tunnel clients); if argued with
  that ops honesty, full credit is possible — grade the reasoning, not
  the conclusion.
- SMS OTP appearing anywhere caps the auth sub-score at 2/10.
- Forgetting the *legacy password-only* path's decommission plan — the
  scenario says "currently" for a reason; migration sequencing is worth
  a note in the risk register.
