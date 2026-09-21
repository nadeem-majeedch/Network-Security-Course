# cs-045 — Self-Signed Certificate Risk Assessment

> **Simulated scenario.** The bank, systems, and inventory are fictional.

## Difficulty & Domain

- **Difficulty:** Intermediate · **Domain:** TLS and certificate problems · **CLO:** CLO-6
- **Est. time:** 12 minutes · **Anchor:** L14 (TLS Deep Dive)

## Scenario

A bank's internal estate runs 40 TLS endpoints: 12 with real internal-PKI
certs, 22 self-signed, 6 with certificates from a private CA whose key was
lost. The security team must triage: which self-signed endpoints are
*acceptable*, which need migration, and which are *incidents*. A
consultant's report says "replace all self-signed certs immediately."
You're asked to grade that recommendation.

## Stakeholders

- **CISO** — wants a defensible triage, not a blanket order.
- **App teams** — own the 22 self-signed services.
- **Internal PKI team** — can issue from the internal CA; has capacity
  constraints (5 migrations/quarter).
- **Auditors** — expect a risk-ranked plan.

## Network Context

- Endpoints: customer-data APIs (4), internal tools (18), build/CI (8),
  legacy vendor appliances (10).
- Client trust: internal CA pinned in the fleet's trust store; self-signed
  endpoints each carry custom trust handling — some clients pin the exact
  cert (TOFU-style), some users click through (browser-facing ones).
- No discovery of *new* self-signed endpoints exists — the 40 came from a
  one-off scan.

## Student Task

1. Build the **triage matrix**: endpoint class → current risk (with
   mechanism: what the self-signed-ness actually enables/breaks) → priority
   → rationale. Not all 22 are equal — say which are *incidents* (the
   browser-facing + click-through ones).
2. Grade the consultant's recommendation: what it gets right, what it gets
   wrong (cost/ordering), and your one-line correction.
3. Design the **pinning-vs-PKI decision rule**: when is pinning a self-signed
   cert acceptable *permanently*, and what monitoring keeps it acceptable?

## How to Approach This (Reasoning Scaffold)

- The risk of a self-signed cert is not "it's self-signed" — it's
  *who validates it and how*: pinned-by-config (okay-ish), TOFU (key-rotation
  pain), click-through humans (training users to accept attacks).
- Capacity constraints (5 migrations/quarter) force prioritization — the
  triage matrix is the deliverable, not the ideal state.
- "Immediately" plans fail; sequenced plans with detection while-you-wait
  succeed.

## CLO Mapping

- **CLO-6** — TLS trust-model triage and migration planning.

## Safety Notes

- Design exercise; no real bank data.
