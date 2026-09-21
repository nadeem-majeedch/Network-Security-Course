---
case: cs-072
solution-for: modules/module-06-detection-vulnerability/case-studies/cs-072-zeek-log-anomaly-correlation.md
difficulty: advanced
module: 6
lecture-anchor: L23
clos: [CLO-9, CLO-12]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-072 Solution — Zeek Anomaly Correlation (INSTRUCTOR ONLY)

## Model Solution

**Correlation keys that bind the three tickets:**

| Key | Binding evidence |
|---|---|
| **Source host** | all three: `10.30.5.12` |
| **Time window** | all within 14:20–14:30 |
| **Peer infrastructure** | T1's CDN domain resolves (per its A records in dns.log) into the same /24 as T2/T3's peer `198.51.100.77` — the infra bridge |
| **Behavioral cadence** | T2's ~60 s POST periodicity matches T3's TLS-flow rhythm |

**The reconstructed story:** the reporting server (documented egress:
none) is compromised and running a staged exfil with redundant channels:
(1) a **DGA/bootstrap DNS phase** — high-entropy subdomains under an
abuse-history CDN domain, 60% NXDOMAIN (trying generated domains until
one resolves); (2) **plaintext fallback channel** — periodic ~20 KB
POSTs to the resolved peer's :80 `/gate/upload` (works even if TLS
pinning/inspection fails); (3) **primary TLS channel** to the same peer
on :443 — the 210 MB bulk. Order: DNS bootstrap → probe/establish →
bulk exfil with the :80 channel as continuous dribble. The *absence* of
files.log entries confirms direction: nothing downloaded in; this is
outbound data movement.

**DNS role — two mechanisms, discriminated:**

| Mechanism | Signature in dns.log/conn.log | Fit to evidence |
|---|---|---|
| **DGA bootstrap** (find C2) | many *queries*, novel labels, high NXDOMAIN, **small response payloads**, subsequent *conn.log flow* to the resolved IP | ✅ 60% NXDOMAIN + the observed :443/:80 flows to the resolved peer |
| **DNS-tunnel exfil** (data in queries) | many queries, **large query payloads consistently**, low NXDOMAIN (attacker controls the authoritative server — every query "succeeds"), response sizes uniform | ✗ NXDOMAIN 60% + no uniform large-query pattern |

Verdict: **DGA bootstrap, then HTTP(S) exfil** — the DNS anomaly is the
*locater*, not the carrier; the carrier is the 210 MB in conn.log. (If
NXDOMAIN were ~0% and queries carried the volume, the tunnel answer
would flip the response: block DNS, not just the peer.)

**Response order:**

1. **Contain the channels:** block/deny egress for `10.30.5.12` to the
   peer IP + the CDN domain (and sinkhole the domain per cs-025 — the
   logging sinkhole keeps *sibling* visibility); the :80 and :443 paths
   both die with a host-scoped egress deny.
2. **Isolate the host** (snapshot-then-reimage per cs-065's evidence
   order); pull its process/network forensics; identify the entry vector
   (a reporting server with no egress *should* — how did it get infected?
   patch path? internal lateral?).
3. **Scope:** hunt siblings — same DNS pattern (novel high-entropy
   subdomains) across dns.log for the past 30 days; same peer IP class
   in conn.log; the *correlation rule* below automates the hunt.

**The formalized correlation rule (fields + logic):**

```
ALERT "multi-log exfil chain" WHEN in a 10-min tumbling window:
  dns.log: ≥20 novel-subdomain queries by one host under domains with
           threat-feed "abuse-history" AND nx_domain_ratio > 0.4
  AND conn.log: same host → any peer IP sharing that domain's
           resolved /24, bytes_out > 50 MB
  AND (http.log OR ssl.log): same host/peer, no SNI OR SNI∉approved set
SEVERITY: critical; SUPPRESS if host ∈ documented-egress allowlist AND
          domain ∈ approved (the false-positive gate cs-071 taught)
```

The rule encodes the *investigation*: infrastructure bridge + behavior
conjuncts — the next occurrence arrives pre-correlated.

## Alternative Solutions

- **DNS-tunnel verdict:** defensible if you weight query-payload size
  over NXDOMAIN ratio — but the *conn.log bulk to the resolved peer*
  makes the tunnel reading redundant (why tunnel 20 KB/query when the
  bulk channel moves 210 MB?); the discriminators decide, not taste.
- **Three unrelated incidents:** rejects the host+time+infra bind —
  possible in principle; the /24 bridge and cadence match make it
  improbable; state the residual (verify via host forensics, which the
  response does anyway).
- **Block only the :443 peer:** the :80 fallback keeps dribbling —
  channel redundancy means containment must be host-scoped, not
  port-scoped.

## Tradeoffs

- Correlation-rule strictness vs coverage: the conjuncts are tight (few
  FPs) but a *simpler* variant (e.g., NXDOMAIN-ratio alone) catches
  earlier stages — run both, different severities.
- Sinkhole vs hard-block the CDN domain: sinkhole preserves telemetry
  (cs-025) — but with a *known-compromised host*, hard-block the peer
  and sinkhole the domain: containment speed + sibling visibility.
- Host isolation timing vs evidence: snapshot-first (cs-065 order) —
  the entry-vector question is the *prevention* deliverable.

## Common Mistakes

- Treating the three tickets separately (the bind keys unused).
- Tunnel-verdict by DNS-volume alone (NXDOMAIN ratio + the bulk
  conn.log flip it).
- Missing the /24 infra bridge (the correlation's spine).
- Port-scoped containment against a redundant-channel adversary.

## Instructor Prompts

- "Quote the exact dns.log field pair that discriminates DGA from
  tunnel."
- "Why does the *absence* of files.log entries matter here?"
- "Which conjunct in your rule kills the most false positives?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Key-based bind; DGA-vs-tunnel discrimination |
| Technical accuracy | 25% | Zeek log semantics; channel-redundancy logic |
| Alternatives considered | 20% | Tunnel/unrelated-incidents rejections |
| Communication | 15% | Story + response order + formalized rule |

**Timing:** reveal at 5:00 + 10; the /24 bridge reveal is the moment.

## CLO Mapping

- **CLO-9** — Detection correlation engineering.
- **CLO-12** — Multi-log anomaly analysis.
