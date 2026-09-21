# cs-047 — Weak-Cipher-Suite Audit and Remediation Plan

> **Simulated scenario.** The hospital group, endpoints, and scan results are fictional.

## Difficulty & Domain

- **Difficulty:** Advanced · **Domain:** TLS and certificate problems · **CLO:** CLO-6
- **Est. time:** 12 minutes · **Anchor:** L14 (TLS Deep Dive)

## Scenario

A hospital group scans its TLS estate (results below). Leadership wants "all
weak ciphers gone." You must produce the remediation plan: rank the findings
by *actual* risk, sequence changes against clinical-system constraints, and
write the one-paragraph explanation of why "RC4 must go" and "3DES must go"
are different sentences with different urgency.

## Stakeholders

- **CISO** — board-visible plan.
- **Clinical engineering** — imaging devices with embedded TLS stacks that
  cannot update quickly.
- **IT operations** — owns the LBs and endpoints; change windows matter.
- **Assessors** — healthcare-security framework references weak-TLS findings.

## Network Context

- Endpoints: patient portal (public), HL7 interface engines (internal),
  imaging modalities (embedded stacks, vendor-frozen), admin tools.
- Terminators: 2 load balancers (config-controlled), several embedded devices.
- Client population: modern browsers (portal), clinical apps (interface
  engines), device firmware (modalities).

## Available Evidence

**Scan results (per endpoint class):**

| Endpoint class | Protocol floor | Weak suites present | Notes |
|---|---|---|---|
| Patient portal (LB) | TLS 1.2 | CBC-SHA suites enabled alongside GCM; no 1.0/1.1 | also offers RC4? **no** — clean |
| HL7 interface engines | TLS 1.0 **negotiable** | 3DES-CBC; CBC-SHA | internal-only reach |
| Imaging modalities (10 devices) | TLS 1.0 only | 3DES-CBC, RC4-128 | vendor-frozen firmware; on isolated VLAN |
| Admin tools | TLS 1.2 | CBC suites + **RC4 enabled** (legacy flag "for an old tool" — unowned) | 3 users |

## Student Task

1. Rank the **four finding classes** by real risk with one-line mechanisms
   (RC4's status, 3DES's birthday-bound reality, CBC-SHA's degrade-or-
   defend status, protocol floors) — include who can *reach* each endpoint.
2. Explain the **RC4 vs 3DES urgency difference** in one paragraph
   (prohibitions, attack state, and why "both are deprecated" isn't the
   whole answer).
3. Produce the **sequenced plan** (3 phases) that respects the imaging
   constraint — including the compensating controls that make "can't fix
   yet" defensible, and the endpoint you fix *today*.

## How to Approach This (Reasoning Scaffold)

- Risk = suite weakness × reachability × client reality — an isolated VLAN
  changes the math without making the finding vanish.
- RC4: prohibited, no safe config, must be off *everywhere* now.
  3DES: deprecated with a real (but gated) attack bound — urgency differs.
- "Vendor-frozen" doesn't mean "nothing to do": VLAN + egress policy +
  monitoring are the compensating trio.

## CLO Mapping

- **CLO-6** — Cipher-suite risk analysis and constrained remediation.

## Safety Notes

- Design exercise; no scanning of real clinical systems.
