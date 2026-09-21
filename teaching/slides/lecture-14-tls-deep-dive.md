---
marp: true
theme: default
paginate: true
lecture: L14
week: 7
clos: [CLO-6]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# TLS Deep Dive

**Network Security · Lecture 14 · Week 7**

*The handshake that carries the modern web's trust.*

<!-- notes: OPEN (2 min). Hook: "Every padlock you've ever trusted was
a chain of certificates. Today we audit chains." -->

---

## Learning Objectives

1. **Trace** the TLS 1.2 vs 1.3 handshakes with their security
   properties
2. **Validate** a certificate chain: path, trust anchor, SAN, expiry,
   revocation
3. **Diagnose** the three most common chain failures
4. **Design** certificate lifecycle automation (the assignment-2 arc)
5. **Argue** TLS 1.3's removal of legacy suites as security progress

![bg right:34% fit](diagrams/05-tls-handshake.md)

<!-- notes: (1 min) Diagram 05 taught fully here — the two handshake
variants. Objectives 2–3 are the practical skills (Lab-07, assignment
2). -->

---

## TLS 1.3: One Round Trip, AEAD Only

- Key share in the first flight (ClientHello)
- All legacy key-exchange and non-AEAD suites removed
- 0-RTT exists — with replay caveats (idempotent requests only)

<!-- notes: (5 min) The removal-as-progress point: fewer choices =
fewer downgrade stories (cs-046's incident case). Quiz-9 Q6's AEAD
answer lives here. The 0-RTT caveat keeps the slide honest. -->

---

## Certificates: The Identity Binding

- A certificate = identity ↔ public key, signed by an issuer
- Chain: leaf → intermediate(s) → root (in trust store)
- SAN = the hostnames the leaf may claim

<!-- notes: (4 min) Anatomy slide: the three binding fields students
must read in every cert they audit (subject, SAN, validity). QB-018
asks the definition. -->

---

## Chain Validation: The Five Checks

1. Path builds to a **trusted root**
2. Every link **unexpired** (and not-yet-valid)
3. Every link **unrevoked** (CRL/OCSP)
4. **SAN matches** the hostname you visited
5. Key usages/extension sanity (EKU, basic constraints)

<!-- notes: (6 min) The checklist is Lab-07's skeleton. cs-044's expiry
outage and cs-045's self-signed case each break one check. Quiz-9 Q3
is the validation definition. -->

---

## Chain Failures: The Big Three

| Failure | Symptom | Fix |
|---|---|---|
| Missing intermediate | works for some clients | serve the full chain |
| Expired leaf/intermediate | warnings, outages | automate renewal |
| Clock skew | "future/not yet valid" | fix time source |

- The missing-intermediate case is the sneakiest (client-caching masks
  it)

<!-- notes: (5 min) Assignment-2's F7 finding is exactly row 1. QB-046
ranks these three as its model answer — flag the alignment. -->

---

## Revocation: CRL vs OCSP

- CRL: periodic full list — complete but bulky, stale by design
- OCSP: per-cert query — fresh but adds latency + privacy + soft-fail
  traps
- OCSP stapling: server fetches proof, client verifies — best of both

<!-- notes: (5 min) The honest limits per course rules: soft-fail
browsers often ignore revocation failures — say so. cs-042's internal
PKI case weighs CRL vs OCSP for a lab estate. -->

---

## Wildcards & SAN Planning

- Wildcard: one cert, many hosts — convenience vs **blast radius**
- SAN multi-name: explicit, auditable
- Custody: one private key for many hosts concentrates compromise

<!-- notes: (4 min) Assignment-2's F1 finding (shared wildcard) is the
practical echo. Quiz-9 Q5 tests the risk characterization. -->

---

## The Click-Through Culture

- Warnings users accept unthinkingly = trained vulnerability
- Self-signed sprawl *causes* the culture (cs-042's lab estate)
- Fix: real PKI for internal services → warnings mean something again

<!-- notes: (4 min) The cultural point is the assignment-2 graded
insight: warning-fatigue is a security finding, not a user failing. -->

---

## Suite Negotiation & Downgrade Defense

- Client offers suites; server picks; versions negotiated
- TLS_FALLBACK_SCSV history; 1.3's structural downgrade removal
- Audit stance: disable legacy versions, prefer AEAD suites

<!-- notes: (5 min) cs-046's downgrade incident + cs-047's weak-suite
audit are the case pair. Keep history short; the audit checklist is the
deliverable skill. -->

---

## Certificate Lifecycle Automation

- Issue: ACME-style protocols against an internal CA
- Rotate: short lifetimes (90d or less) — automation makes it free
- Monitor: expiry telemetry with alerts at T-30/T-14/T-7
- The "why manual failed" argument: expiry is a *when*, not an *if*

<!-- notes: (5 min) Assignment-2's task 4 is this slide. The internal
PKI design (cs-042) supplies the issuing architecture. -->

---

## CS/DS Example: Trusting the Notebook Cluster

- Internal services (registry, scheduler) need browser-trusted TLS —
  internal CA + trust distribution
- mTLS tier for registry↔build (cs-042's tier-2 requirement)

<!-- notes: (3 min) DS framing: the research estate's PKI is small but
real — the tiered design from cs-042 is the answer shape. -->

---

## Activity: Validate This Chain (6 min)

Given a served chain (leaf + missing intermediate) and a client that
*sometimes* works: find the failure, name the check it violates, draft
the fix.

<!-- notes: (6 min) Lab-07's seeded artifact. The "sometimes works"
clue = client caching — the sneakiest row of the Big Three. -->

---

## Case Study: cs-048 (5 min)

- mTLS service-to-service rollout — what changes at scale

<!-- notes: (5 min) The case extends today's skills from browser TLS to
service meshes' mTLS — certificate *distribution* becomes the problem. -->

---

## Formative Check

- Oral: name the five chain-validation checks; why does 1.3 have no
  record MAC?

<!-- notes: (2 min) Exit oral — the checklist is the takeaway. -->

---

## References & Next

- RFC 8446 (TLS 1.3), RFC 5280 (certificate profile)
- Diagrams: `diagrams/05-tls-handshake.md`
- **Next (L15):** IPsec & legacy VPN architecture
