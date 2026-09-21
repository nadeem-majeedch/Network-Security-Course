# cs-087 — Rebuilding the Intrusion Timeline from Five Sources

> **Simulated scenario.** The intrusion and all telemetry are fictional.

## Difficulty & Domain

- **Difficulty:** Expert · **Domain:** Network forensics · **CLO:** CLO-11, CLO-12
- **Est. time:** 15 minutes · **Anchor:** L26 (Detection, Triage & Containment) with L27 recovery framing

## Scenario

A manufacturing firm's ERP server was compromised; you were handed
*five* partial telemetry sources, none complete, each from a different
team. Legal needs a defensible timeline: when did the attacker enter,
what did they touch, and what did they take? Your job is to
reconstruct the timeline and state the confidence level of each
inference — the discipline is *corroboration with explicit
uncertainty* (L26's three-way rule, extended).

## Stakeholders

- **IR (you)** — timeline author.
- **Legal** — needs defensible, sourced conclusions.
- **ERP owner** — production impact of any re-check.
- **Insurer** — will audit the timeline's sourcing.

## Network Context

- Sources: firewall logs (30-day retention), proxy logs (7-day),
  Zeek on the server VLAN (14-day), AD sign-in events (90-day),
  EDR on the ERP server (30-day).
- The event window is days 20–23 before today — inside some
  retentions, outside others.
- ERP server: internal app, AD-authed, one outbound path via proxy.

## Available Evidence

**Source-by-source (event window day 20–23):**

| Source | Coverage of window | Key content |
|---|---|---|
| Firewall | full | Allow flows to ERP:445 from one workstation daily; new outbound 443 from ERP day 22 |
| Proxy | **partial** (7-day) | ERP → unknown domain, 1.2 GB total, day 22 only |
| Zeek (server VLAN) | full | SMB sessions ERP ← W-31; LDAP reads ERP → DC day 22 03:00 |
| AD sign-ins | full | W-31 used svc_erp creds day 20 22:14 (no MFA on service account) |
| EDR (ERP) | **partial** (agent offline day 22 04:00–day 23 11:00) | day 20: credential tool; day 23 11:00: uninstall event |

## Student Task

1. Build the **corroborated timeline** — each entry tagged with its
   sources (one source = hypothesis; two = supported; three =
   corroborated) and confidence.
2. Answer the **EDR-gap question**: what happened during day 22
   04:00–day 23 11:00, and which sources let you infer it anyway?
   What *can't* you conclude about that gap?
3. Answer the **exfiltration question**: what does the 1.2 GB egress
   mean, and what additional evidence would upgrade "likely
   exfiltration" to a defensible finding for legal?
4. List the **retention failures** — what evidence is already gone
   forever, and what one-line policy change would have kept it?

## How to Approach This (Reasoning Scaffold)

- Corroboration is a *ladder*: single-source claims are hypotheses
  with a confidence label; the timeline's credibility is the sum of
  its source counts, not the number of entries.
- Absence of evidence during a gap is not evidence — the EDR-off
  window and the proxy's 7-day horizon both bound what can be
  *known*; state the bound explicitly.
- Legal needs provenance: every entry cites source + timestamp
  basis (event time vs log time) — clock skew is a finding, not a
  footnote.

## CLO Mapping

- **CLO-11** — Timeline reconstruction from partial telemetry.
- **CLO-12** — Multi-source corroboration discipline.

## Safety Notes

- Simulated; forensic methodology only, no tooling beyond log
  reading.
