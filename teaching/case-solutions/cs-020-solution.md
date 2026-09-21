---
case: cs-020
solution-for: modules/module-02-network-threats/case-studies/cs-020-dns-spoofing-campaign.md
difficulty: beginner
module: 2
lecture-anchor: L07
clos: [CLO-2]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-020 Solution — DNS-Spoofing Campaign (INSTRUCTOR ONLY)

## Model Solution

**Location of the spoofing: on the path between the client's router and the
ISP's resolvers — i.e., the ISP last mile (or the router's forwarding itself).**

Discriminating observations:

- The MSP's *resolver-side* log shows **fresh (non-cached) contradictory
  answers seconds apart with TTL=1** — the attacker is answering the client's
  upstream queries in real time, not poisoning a cache (cache poisoning
  would show a *persistently wrong* cached answer until TTL expiry).
- Six clients sharing **one ISP last-mile technology** with no other common
  factor (different industries, different endpoint stacks) points upstream,
  not at client malware (endpoint telemetry shows clean infection-free hosts
  receiving the bogus answer).
- **TTL=1 is deliberate:** the attacker keeps answers uncacheable so each
  lookup can be re-spoofed, and so the victim's resolver doesn't hold
  evidence. Only an on-path actor between router and resolver benefits from
  this — a compromised authoritative server would be consistent, not flickering.
- Remaining ambiguity: a **compromised ISP-supplied router** (2019 firmware,
  remote admin enabled) could do the same rewriting locally. The evidence
  cannot fully separate "last-mile interception" from "router compromise" —
  and that uncertainty *is* the escalation's first question. (Credit students
  who name this boundary explicitly.)

**Why the payroll SaaS was spared:** the payroll site enforces **HSTS** — the
browser *refuses* to serve its login over plaintext and pre-pins the HTTPS
requirement, so even with a spoofed DNS answer, the clone can't present a
valid certificate; browsers hard-fail instead of showing the clone. The bank
has no HSTS, so the clone renders. Lesson for the ISP investigation: the
attacker **avoids HSTS domains** — checking which domains got spoofed maps
their target selection and confirms a *credential-harvesting* (not
surveillance) goal.

**MSP action list:**

*Immediate user-side guidance:*
1. Assume credentials submitted to the clone are burned: force password resets
   on the bank accounts, notify the bank's fraud team, enable MFA where offered.
2. Tell users the tell: "login page then error" — and to treat any
   certificate warning as a stop sign (the clone can't present a valid cert).

*Client-router mitigations:*
3. Update firmware; **disable remote admin**; change default admin creds;
   set DNS forwarder to a **DNSCrypt/DoH-capable resolver** or the MSP's own
   validating resolvers over encrypted transport where the router supports it
   — encrypted DNS removes the on-path rewrite point for the DNS step.
4. Where routers can't do encrypted DNS: pin resolvers + enable client-side
   browser DNS-over-HTTPS policies (managed browsers) for affected SMBs.

*Escalation path with the ISP:*
5. Hand the ISP the **discriminating evidence**: TTL=1 flickering answers,
   times, client router MACs/serials, and the affected-prefix list — and
   request their BNG/last-mile session logs for those windows. The ask that
   forces a real investigation: "either your last mile rewrote these answers
   or the supplied routers did; here are the serials, check both."

## Alternative Solutions

- **"Authoritative compromise of the bank's zone."** Rejected: flickering
  answers with TTL=1 and mixed legit answers are inconsistent with
  authoritative control, which would be *stable*; also the ISP-cluster
  correlation.
- **"Endpoint malware rewriting hosts."** Rejected by endpoint telemetry and
  by the *resolver-side* visibility of contradictory answers (malware on the
  endpoint wouldn't produce fresh bad answers at the resolver).
- **"Migrate all clients to DoH immediately, router-independent."** Good
  direction; as the *sole* fix it bypasses enterprise DNS controls — managed
  DoH with policy is the defensible version.

## Tradeoffs

- Encrypted DNS (DoH/DoT) kills on-path spoofing but breaks
  content-filtering/logging designs unless centrally configured — the MSP
  must run its own encrypted resolvers, not push public DoH.
- Router replacement fleet-wide vs firmware+config hardening: replacement is
  cleaner but costly; hardening now, replacement in contract renewals.
- Public disclosure timing: silent fixing protects clients' confidence but
  delays other MSPs' awareness — coordinate with the ISP first, then peers.

## Common Mistakes

- Calling it cache poisoning (the TTL=1 flicker contradicts caching).
- Treating the ISP's denial as a location conclusion.
- Missing the HSTS-differential as *evidence about attacker target selection*.
- User guidance that says "avoid the bank site" instead of "credentials are
  burned; reset and enable MFA."

## Instructor Prompts

- "Draw the four places a DNS answer can be altered; which did the evidence
  exclude, and how?"
- "Why TTL=1? What does the attacker gain against *themselves*?"
- "If the bank deployed HSTS tomorrow, what does the attacker do next?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | TTL=1 flicker → on-path logic; HSTS differential as attacker-behavior evidence |
| Technical accuracy | 25% | Poisoning-vs-on-path distinction; HSTS mechanics |
| Alternatives considered | 20% | Authoritative/endpoint hypotheses excluded with reasons |
| Communication | 15% | Three-part action list with evidence-to-ISP handoff |

**Timing:** reveal at 5:00 + 2; the "four alteration points" prompt is the
structural takeaway.

## CLO Mapping

- **CLO-2** — DNS on-path attack analysis and multi-party response.
