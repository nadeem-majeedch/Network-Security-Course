# cs-073 — DNS-Tunneling Detection Design

> **Simulated scenario.** The network, tunnel simulation, and detectors are fictional.

## Difficulty & Domain

- **Difficulty:** Advanced · **Domain:** Network monitoring and log analysis · **CLO:** CLO-9, CLO-12
- **Est. time:** 15 minutes · **Anchor:** L23 (Zeek & Anomaly Detection)

## Scenario

A university fears DNS tunneling (students evading the captive portal —
cs-038's campus). You must design the **detection stack**: what the
tunnel's traffic looks like at each layer, which detectors catch which
variants, and the quantitative thresholds — including the honest
false-positive problem (CDNs, security scanners, and monitoring tools
*also* make weird DNS).

## Stakeholders

- **Network/security team** — owns resolvers and detectors.
- **Students** — some will test the detectors (authorized vs not — the
  policy line matters).
- **Captive-portal owner** — wants the evasion closed.
- **Audit** — wants the detection documented with FP analysis.

## Network Context

- Resolver: internal recursive; logs all queries (dns.log-style);
  egress DNS limited to the resolvers (cs-038's rule already denies
  direct :53).
- Tunnel variants to defend against: (a) TXT-record uplink/downlink
  (data in TXT), (b) A-record subdomain-encoding uplink, (c) CNAME
  chains, (d) NULL-type exotic.
- Benign weird-DNS sources: CDN CNAME chains (deep, legit), security
  scanners' rDNS lookups (reverse-pagination), monitoring TTL probes.

## Student Task

1. Characterize the **tunnel's quantitative fingerprints** per variant:
   query-name entropy/label-length stats, query *type* distribution
   (TXT/NULL vs A/AAAA), query rate per client, NXDOMAIN ratio,
   response-payload asymmetry — with plausible threshold values and
   *why* those values (bandwidth math: how much can tunnel through 1
   q/s with 250-B labels?).
2. Design the **layered detector set** (4 detectors): per-client
   entropy detector, type-distribution detector, NXDOMAIN/timeout
   detector, per-domain uniqueness detector — each with window,
   threshold, FP source, and FP mitigation.
3. Address the **policy line**: students testing your detectors — what's
   authorized (lab range, red-team window) vs not, and how the
   detector's alert payload distinguishes them (asset/identity
   enrichment).

## How to Approach This (Reasoning Scaffold)

- Tunnels are *bandwidth-through-DNS* — the bandwidth math yields the
  query-rate and label-length fingerprints (250-B labels × N q/s =
  KB/s through a protocol designed for names).
- The FP problem is structural: CDNs do CNAME chains, scanners do
  reverse-pagination — your thresholds must survive *them*, hence
  per-client baselines and type-distribution (CDNs don't TXT-flood).
- The policy line: detection without authorization-marking invites
  witch hunts — enrich alerts with identity so the *response* is
  proportionate.

## CLO Mapping

- **CLO-9** — Detector design with quantitative thresholds.
- **CLO-12** — Protocol-aware anomaly analytics.

## Safety Notes

- Detector design for defense; no tunnel-tool instructions. Student
  testing happens only in the authorized lab range.
