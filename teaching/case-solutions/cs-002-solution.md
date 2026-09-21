---
case: cs-002
solution-for: modules/module-01-network-foundations/case-studies/cs-002-lost-laptop-cia-impact.md
difficulty: beginner
module: 1
lecture-anchor: L01
clos: [CLO-1]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-002 Solution — Lost-Laptop CIA Impact (INSTRUCTOR ONLY)

## Model Solution

**CIA ratings:**

| Element | Rating | Justification |
|---|---|---|
| Confidentiality | **High** | Smartcard co-located with the bag defeats the FDE unlock factor at rest; cached reports are readable. Portal cookie (up to 12 h remaining) may allow remote record access even without the disk. |
| Integrity | **Low→Med** | Disk data is unlikely to be modified before discovery, but a live portal session could create/alter record entries under the nurse's identity — integrity of *the record system*, not the disk, is the exposure. |
| Availability | **Low** | Hospital systems unaffected; the nurse loses one device (a personal-productivity impact, not a system impact). VPN cert reuse could matter only if stolen for infrastructure access. |

**Containment, in order:**

1. **Revoke/invalidate the portal session** (server-side logout-all + force
   re-auth) — limits remote access to records immediately, cheapest, highest value.
2. **Revoke the VPN device certificate** — closes the always-on tunnel path;
   independent of the portal cookie.
3. **Disable the nurse's account credentials pending re-issue** — covers
   password reuse/non-SSO paths. Remote wipe is *not* possible (no enrollment)
   and is correctly not listed as an action available in this state.

**Most consequential fact:** the smartcard being in the same bag — it converts
the FDE from a strong compensating control into no protection at rest, moving
confidentiality from *low* to *high*. Second place: the 12 h cookie with no
IP/device re-auth, which extends the confidentiality window beyond physical
possession.

## Alternative Solutions

- **Assume theft, full lockout of the nurse's identity.** Safer for patients,
  harsher on staff, disrupts care delivery; defensible if regulator risk appetite is low.
- **Wait 12 h for cookie expiry, do nothing server-side.** Relies on an
  assumption (no logout) about an active threat — rejected: expiry is not containment.
- **Treat as lost-property only, no security process.** Fails the regulator
  threshold question; the privacy officer still needs documented rationale.

## Tradeoffs

- Speed vs certainty: revoking first and investigating after protects patients
  but complicates forensics of the session (logs preserved either way).
- Blame vs reporting culture: disciplining quickly may suppress honest
  loss-reporting in future — a real cost to the hospital.

## Common Mistakes

- Rating CIA as one number ("the incident is high impact") instead of separately.
- Counting FDE as protecting the data without checking the unlock factor's location.
- Listing "remote wipe" when evidence says the device is not enrolled.
- Forgetting the portal session — the network-bound exposure outranks the disk.

## Instructor Prompts

- "Which control would have made the smartcard co-location irrelevant?"
- "What does 'availability' mean for a nurse mid-shift, and does it change the rating?"
- "If the cookie lifetime were 15 minutes, which ratings move?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Separate C/I/A with evidence-tied justifications |
| Technical accuracy | 25% | Session/cert mechanics described correctly; no impossible actions |
| Alternatives considered | 20% | ≥1 alternative with tradeoff |
| Communication | 15% | Ordered actions with what-each-limits stated |

**Timing:** reveal at 5:00; debrief on why cookie lifetime is a *network
security* parameter (bridges to L03/L07 session attacks).

## CLO Mapping

- **CLO-1** — CIA decomposition under uncertainty.
