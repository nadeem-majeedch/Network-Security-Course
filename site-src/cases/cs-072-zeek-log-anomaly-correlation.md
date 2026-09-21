# cs-072 — Zeek-Log Anomaly Correlation

> **Simulated scenario.** The Zeek logs, anomalies, and correlations are fictional.

## Difficulty & Domain

- **Difficulty:** Advanced · **Domain:** Network monitoring and log analysis · **CLO:** CLO-9, CLO-12
- **Est. time:** 15 minutes · **Anchor:** L23 (Zeek & Anomaly Detection)

## Scenario

A Zeek sensor covers a company's egress. Three separate anomalies
surfaced across *different* Zeek logs (dns, http, conn) for the same
10-minute window. Alone, each is weak; correlated, they may be one
story. Reconstruct the story, name the correlation keys that bind the
logs, and decide the response.

## Stakeholders

- **SOC analyst** — three tickets, one story (hopefully).
- **Detection engineering** — wants the correlation formalized into a
  rule.
- **Network team** — DNS egress policy implications.
- **Data owner** — if it's exfil, which dataset?

## Network Context

- Zeek logs: dns.log (queries/responses), http.log (plaintext +
  proxy-decrypted), conn.log (all flows), ssl.log (SNI), files.log
  (extracted file analysis).
- Egress: via proxy for user VLANs; direct for servers.
- The window: Tue 14:20–14:30; one server host `10.30.5.12` (a reporting
  server) is the common thread *if* you find it.

## Available Evidence

**The three anomalies (as separate tickets):**

| Ticket | Log | Anomaly |
|---|---|---|
| T1 | dns.log | `10.30.5.12` queried 41 novel subdomains of `updates-metrics.example-cdn.net` in 10 min; labels look high-entropy; NXDOMAIN ratio 60% |
| T2 | http.log | same host, 9 HTTP POSTs to `198.51.100.77` (no SNI — raw IP), URI `/gate/upload`, body sizes 18–24 KB, periodic ~60 s |
| T3 | conn.log | same host: outbound to `198.51.100.77:443` *also* present (TLS, SNI = none/CN mismatch) concurrent with T2's :80 posts; total 210 MB out in window |

Context: `10.30.5.12` is a *reporting* server whose documented egress is
"none" (it sends reports internally). The DNS domain appears in a
threat feed as "bulk-registration CDN, previously abused." Zeek's
files.log shows nothing (no files transferred *in*).

## Student Task

1. **Bind the anomalies**: name the correlation keys (host, time, peer
   infrastructure, behavioral cadence) and reconstruct the most likely
   single story — what is `10.30.5.12` doing, in what order, using which
   channels?
2. Explain the **DNS behavior's role**: 41 novel high-entropy subdomains
   + 60% NXDOMAIN in 10 minutes from a server with *no documented DNS
   use* — give the two candidate mechanisms (C2 DGA bootstrap vs
   DNS-tunnel exfil) and the evidence that discriminates (what in the
   dns.log/conn.log decides?).
3. Decide the **response order** (contain/eradicate steps) and the
   **correlation rule** you'd formalize (which fields, which logic) so
   the next occurrence arrives as one alert, not three tickets.

## How to Approach This (Reasoning Scaffold)

- The bind is *host + time + infrastructure overlap* — T1's CDN domain
  resolving to T2/T3's peer IP class is the infra bridge; look for it.
- NXDOMAIN-heavy novel subdomains from a no-DNS-use server: DGA
  bootstrap (trying domains until one resolves) vs tunneling (every
  query carries data, few NXDOMAINs) — the NXDOMAIN ratio and
  query/response *sizes* discriminate.
- The story should explain *both* :80 POSTs and :443 TLS to the same
  peer — fallback channels are redundancy, not coincidence.

## CLO Mapping

- **CLO-9** — Detection correlation engineering.
- **CLO-12** — Multi-log anomaly analysis.

## Safety Notes

- Simulated logs; defensive analysis only.
