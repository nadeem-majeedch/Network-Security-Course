# cs-044 — Expired-Certificate Outage Post-Mortem

> **Simulated scenario.** The airline, systems, and timeline are fictional.

## Difficulty & Domain

- **Difficulty:** Intermediate · **Domain:** TLS and certificate problems · **CLO:** CLO-6
- **Est. time:** 12 minutes · **Anchor:** L14 (TLS Deep Dive)

## Scenario

An airline's booking system failed for 2 hours because an internal TLS
certificate expired — *not* the public website cert (which was automated),
but the service-mesh certificate between booking and payment services.
Management wants a post-mortem that explains why "we automated our certs"
didn't cover this, and the fix. You write it.

## Stakeholders

- **Customers** — couldn't book for 2 hours.
- **Platform team** — believed certs were "handled."
- **Payment partner** — saw connection failures.
- **Auditors** — availability of regulated payment flows.

## Network Context

- Public edge: Let's Encrypt, ACME-automated, 90-day certs — mature.
- Internal mesh: certs issued by an internal CA, **825-day validity**
  (chosen "to reduce toil"), manual issuance, expiry tracked in a
  spreadsheet by one engineer.
- The mesh validates peer certs strictly (good); nothing alerted on
  upcoming expiry (the gap).

## Available Evidence

**Timeline (fictional):**

| Time (UTC) | Event |
|---|---|
| 09:14 | mesh cert for `payment-connector` expires (825 days after issuance) |
| 09:14 | booking→payment calls begin failing TLS validation |
| 09:20 | first alert: "booking error rate 40%" — no cert-specific alert existed |
| 09:41 | on-call identifies TLS verify errors in mesh logs |
| 09:58 | cert inventory spreadsheet found stale (listed 2027 expiry — wrong row) |
| 10:35 | new cert issued manually, deployed to one pod — partial recovery |
| 11:10 | full rollout; errors cease; incident closed |

**Contributing facts:** cert issued 2023 with 825-day life to "reduce
toil"; the issuing engineer left in 2024; the spreadsheet listed the wrong
renewal date; the mesh's cert-rotation feature was disabled at launch
("untested"), never revisited.

## Student Task

1. Write the **post-mortem sections**: summary line, timeline highlights
   (3 bullets), root cause vs contributing causes, and what worked (yes —
   name two things that did).
2. Explain why the 825-day choice *created* the incident (not just
   "correlated with it") — connect certificate lifetime to operational
   memory and staffing reality.
3. Give the **fix set**: the automation to enable, the monitoring to add
   (metric + alert threshold), and the process artifact that survives
   people leaving.

## How to Approach This (Reasoning Scaffold)

- Long-lived certs don't reduce toil; they *hide* it until the toil lands
  on someone who doesn't know it exists.
- "What worked" is a post-mortem skill: strict validation contained the
  blast radius to one link; logs identified TLS fast (22 min).
- Fixes must survive *staff turnover* — that's the design constraint, not
  nice-to-have.

## CLO Mapping

- **CLO-6** — TLS/PKI operational failure analysis.

## Safety Notes

- Simulated incident; standard post-mortem practice.
