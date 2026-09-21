# cs-069 — Suricata Rule for a C2 Beacon Pattern

> **Simulated scenario.** The malware, traffic pattern, and rule draft are
> fictional. Rule *syntax and tuning concepts* are the learning objective;
> no weaponized content is included.

## Difficulty & Domain

- **Difficulty:** Advanced · **Domain:** IDS/IPS alerts · **CLO:** CLO-9
- **Est. time:** 15 minutes · **Anchor:** L22 (IDS/IPS — Signatures & Tuning)

## Scenario

Malware on one internal host beacons to its C2 over HTTPS: fixed 60 s
interval (±2 s jitter), TLS with a JA3 fingerprint observed on the
sandbox, SNI `cdn-metrics.example-ads.com`, URI pattern
`/px/<32-hex>.gif`, and a *fixed User-Agent* that no real browser on
your fleet emits. Your draft Suricata rule (below) is **too loud** — it
fires on a popular monitoring tool. Refine it: match the *behavioral*
combination, not one feature.

## Stakeholders

- **SOC** — wants one alert per true beacon chain, not 40/day.
- **Network team** — the rule runs at the edge sensor (latency budget).
- **Threat-intel** — the SNI/domain has feed history.
- **The malware** — adaptive; will change UA first, URI later.

## Network Context

- Sensor: Suricata at HQ edge (cs-066's C placement); TLS-terminating
  proxy in path for most user traffic (so some rule options see
  plaintext), *not* for this host's direct TLS (exempted).
- True-positive host: 10.20.30.44 (to be confirmed — the rule's job).
- Noise source: a legitimate synthetic-monitoring tool matching the
  draft's URI pattern from 3 hosts, every 60 s (of course it is).

## Available Evidence

**Traffic profile (sandbox):**

| Feature | Value | Real-browser/monitor-tool contrast |
|---|---|---|
| Interval | 60 s ±2 s jitter | monitors: 60 s exact (0 jitter!) |
| SNI | `cdn-metrics.example-ads.com` | monitor tool uses a *different* domain |
| URI | `/px/<32-hex>.gif` | monitor uses `/px/<fixed-id>.gif` (same id every time!) |
| UA | `Mozilla/5.0 (compatible; MetricsBot/2.4)` | monitor sends `SyntheticProbe/1.0` |
| TLS | JA3 fingerprint J | monitors use curl-like JA3 (different) |
| Response size | ~200 B, ~40 B variance | monitors: ~50 B, fixed |

**Draft rule (too loud):**
```
alert http $HOME_NET any -> $EXTERNAL_NET 443 (msg:"C2 beacon px";
http.uri; content:"/px/"; sid:9000001; rev:1;)
```

## Student Task

1. Critique the draft rule: what it matches, what it misses, why it's
   loud (feature-count = 1; no directionality scoping; no UA/URI
   structure) — and the general principle (single-feature signatures
   vs behavioral combinations).
2. Write the **refined rule** (Suricata syntax, conceptual-level): flow
   direction/ports, `http.uri` regex for `/px/<32-hex>.gif`, UA match,
   `threshold`/`detection_filter` (alert cadence design), flowbits if
   useful — and state what each keyword *buys* against the noise
   source. (Syntax precision matters; weaponization does not — no
   payload-craft content.)
3. Design the **evasion-resistance layer**: when the malware changes UA
   (first), URI-structure (second), what still binds it? Give the
   layered fallback (JA3+interval via flow analytics; SNI+feed) and the
   honest limit of signature-only detection.

## How to Approach This (Reasoning Scaffold)

- The noise source *shares* the URI prefix and the 60 s cadence — your
  discriminator set must include features it *doesn't* share: UA, hex-
  length URI structure, jitter (not expressible in a single rule —
  hence flow analytics layering).
- Alert-cadence design: one alert per (src,dst) chain per N minutes —
  the detection_filter is where the 40/day becomes 1.
- Signature + behavioral-layer thinking: rules catch the current
  configuration; the fallback layers catch the *next* one.

## CLO Mapping

- **CLO-9** — IDS signature engineering and tuning discipline.

## Safety Notes

- Defensive signature engineering; the rule targets detection, not
  emulation. No malware reproduction guidance.
