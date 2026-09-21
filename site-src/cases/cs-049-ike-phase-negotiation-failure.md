# cs-049 — IKE Phase-Negotiation Failure Diagnosis

> **Simulated scenario.** The tunnel, logs, and partner requirements are fictional.

## Difficulty & Domain

- **Difficulty:** Advanced · **Domain:** VPN and secure remote access · **CLO:** CLO-7
- **Est. time:** 12 minutes · **Anchor:** L15 (IPsec & Legacy VPN Architecture)

## Scenario

A newly built site-to-site IPsec tunnel to a partner bank fails to
establish. Both sides believe their config matches the agreed spec. You
have the gateway logs and the proposal parameters; your job is to pinpoint
the failure *phase and parameter*, explain the message that reveals it, and
produce the corrected proposal — plus the one debugging habit that finds
this class of fault fastest.

## Stakeholders

- **Your network team** — owns the tunnel config.
- **Partner bank** — needs the traffic path live for settlement files.
- **Project manager** — wants a *specific* answer to give the bank, not
  "both sides should check."

## Network Context

- Your side: modern firewall, IKEv2 capable; spec sheet written 2 years ago
  says IKEv1 + specific proposals.
- Partner side: mainframe-adjacent security appliance, IKEv1-only
  (per their security standard), aggressive spec adherence.
- NAT device sits between the sites (carrier-grade NAT on one uplink —
  relevant!).
- Phase 2 (Quick Mode / CHILD_SA) selectors per spec: settlement subnet →
  partner subnet, TCP-only traffic expected.

## Available Evidence

**Your gateway log (attempt sequence):**

```
09:12:01  IKEv2 initiator: SA-INIT → partner:500   (no response)
09:12:05  retry SA-INIT → partner:500               (no response)
09:12:09  fallback attempt: IKEv1 main mode → partner:500
09:12:09  ← partner: IKEv1 main mode SA proposal rejected (NO_PROPOSAL_CHOSEN)
09:12:10  our IKEv1 proposal: AES-256-SHA256, DH group 14, lifetime 28800
09:12:11  partner debug (via call): expects 3DES-SHA1, DH group 2,
          lifetime 86400
09:12:15  after agreement to match partner: NAT-D payloads exchanged;
          partner rejects — "NAT detected, main mode + PSK unsupported"
```

**Spec sheet (2024, never revised):** IKEv1, AES-256/SHA-256, DH14 —
written by *your* side; the bank's standard predates it.

## Student Task

1. Identify the **three distinct failures** in sequence (protocol version,
   proposal mismatch, NAT/PSK constraint) — for each, the log line that
   reveals it and the corrected parameter.
2. Explain the **NAT + main-mode + PSK constraint** mechanically: why main
   mode with PSK breaks behind NAT, what the two standard remedies are,
   and which you'd pick with this partner.
3. Produce the **corrected proposal sheet** (one table) and name the
   **debugging habit** (one sentence) that would have found all three
   failures in the first hour.

## How to Approach This (Reasoning Scaffold)

- Read the log as a *negotiation*: each rejection names its layer —
  version → proposal → identity/NAT.
- Main mode protects identity; PSK lookup *needs* identity — NAT's IP
  translation breaks the lookup math. Know the two remedies (aggressive
  mode's cost; or certificates/other PSK-placement tricks).
- The debugging habit: read the *responder's* log, not just your own —
  NO_PROPOSAL_CHOSEN names nothing; the partner's log names everything.

## CLO Mapping

- **CLO-7** — IPsec/IKE negotiation mechanics and structured diagnosis.

## Safety Notes

- Simulated logs; VPN configuration on authorized infrastructure only.
