# cs-074 — Asset-Discovery Gaps Before Scanning

> **Simulated scenario.** The estate, scan plan, and gaps are fictional.

## Difficulty & Domain

- **Difficulty:** Advanced · **Domain:** Vulnerability prioritization · **CLO:** CLO-10
- **Est. time:** 15 minutes · **Anchor:** L24 (Vulnerability Management Cycle)

## Scenario

A security team plans its first full vulnerability scan. The asset
inventory says 1,200 hosts. You must find the **discovery gaps first**:
what a network scan will miss, what it will break (OT/legacy devices),
and the pre-scan reconciliation that turns "1,200 hosts" into a
*scan-safe plan* — because scanning without discovery discipline creates
both blind spots and outages.

## Stakeholders

- **Security team** — wants complete scan coverage.
- **OT/plant team** — PLCs that crash under port-scans (real outage
  history).
- **Cloud teams** — 300 instances "somewhere" in two accounts.
- **Help desk** — will absorb every broken printer/legacy box.

## Network Context

- On-prem: 900 hosts claimed (CMDB), across 6 VLANs incl. OT VLAN
  (PLCs, HMIs) and a legacy VLAN (medical-device-like embedded boxes).
- Cloud: 300 instances in 2 accounts, CMDB entries stale by 8 months;
  ephemeral autoscaling unaccounted.
- Roaming: 200 laptops — on/off network; VPN-only workers.
- Unmanaged reality: shadow IT (cs-058's rogue AP history), contractor
  gear.

## Student Task

1. Enumerate the **discovery-gap classes** (≥6) with mechanism: what
   each gap hides from a network scan (e.g., cloud API-only assets,
   firewalled hosts, transient instances, non-IP devices) — and the
   *independent discovery source* that closes each (CMDB vs cloud API
   vs passive traffic vs EDR fleet vs DHCP logs).
2. Apply to this estate: produce the **reconciliation table** — source
   pairs (CMDB vs scan vs cloud API vs EDR) and the expected deltas
   (who appears in which source only) for each host class.
3. Design the **scan-safety plan**: the OT/legacy exclusion + credentialed
   alternative (agentless-safe methods), rate/window controls, and the
   pre-flight checklist item most teams skip (a *crash-canary*: which
   host class do you deliberately test first, and why?).

## How to Approach This (Reasoning Scaffold)

- A network scan sees *IPs that answer* — everything else (cloud-only,
  firewalled, transient, non-IP, off-network) is invisible; each class
  needs a different witness.
- OT devices aren't "scan carefully" — many are "don't scan at all"
  (port-sweeps crash firmware); the credentialed/agentless alternative
  is the professional answer.
- The canary principle: run the scan *profile* against the most
  fragile-yet-safe representative first — it proves the profile before
  production pays.

## CLO Mapping

- **CLO-10** — Vulnerability-program discovery discipline.

## Safety Notes

- No active scanning guidance beyond safety framing; OT protection is
  the point.
