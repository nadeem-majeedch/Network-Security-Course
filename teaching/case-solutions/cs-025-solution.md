---
case: cs-025
solution-for: modules/module-02-network-threats/case-studies/cs-025-sinkholing-egress-tradeoffs.md
difficulty: intermediate
module: 2
lecture-anchor: L08
clos: [CLO-2]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-025 Solution — Sinkholing vs Egress Blocking (INSTRUCTOR ONLY)

## Model Solution

**Answer to the CIO — the visibility ledger:**

| Control | Telemetry preserved | Telemetry destroyed | Cost |
|---|---|---|---|
| **Resolver sinkhole (RPZ)** | DNS queries keep arriving → **new DGA domains become visible immediately** (the resolver sees every attempt); per-host query history retained | Post-resolution telemetry: TLS SNI to the botnet IPs, flow volumes, timing *of successful connections* | Zero for the client; attacker sees "failure" and may switch resolvers (DoH) — watch for that |
| **Egress block (deny to IPs/domains)** | Deny logs (who tried, when) — a weaker, flatter signal | TLS-phase SNI/stream metadata for those destinations; flow records show only denies; **new-domain attempts that resolve elsewhere (DoH/alt-résolver) are invisible to both** | Loses the richest metadata at exactly the point you want it |
| **Both** | DNS-side + deny-side logs | Same as egress-block for the TLS phase; plus **attribution ambiguity** (did the sinkhole or the block stop it?) — investigate carefully | Operational complexity; alert routing must deduplicate |

**Key insight the answer must include:** the DGA rotates every 6 hours, so
*observed-domain blocking is a decaying asset* — its coverage half-life is
hours. The **functional** control is "malware cannot successfully resolve or
connect to *unvetted registrar-pattern domains*" — which is resolver-side
(RPZ sinkhole on the 3 registrar patterns + threat-intel feed) with the
resolver as the primary *sensor*, egress as the secondary net.

**Detection-preserving containment design:**

1. **RPZ sinkhole** the 17 observed domains *and* the 3 registrar patterns at
   the internal resolvers; **sinkhole answers point at a logging sinkhole
   host** (not NXDOMAIN) — you get a HTTP-level touch log of every infected
   host's continued attempts (per-host beacon cadence preserved).
2. **Firewall:** egress *allow* to the sinkhole only; deny-list the pooled IP
   ranges at the edge (coarse, low-churn ranges) — the deny logs become the
   secondary alert stream, not the primary.
3. **Keep the sensor pointed at the sinkhole:** export sinkhole touch logs +
   resolver query logs to the SIEM; alert on *first-touch per host per new
   domain* — this is your new-DGA-detection channel and the metric by which
   you know eradication succeeded (zero touches for 72 h).
4. **Watch the DoH escape hatch:** alert on client DoH bootstrap (known DoH
   provider SNI/ports from endpoints) — the CIO's real risk is "attacker
   moves to encrypted resolver," and that shows up *here* first.

**OT workstations — 30-day compensating plan:** (1) resolver-side sinkhole
already covers them (no agent needed); (2) network containment: move them to
a restricted VLAN with egress only to vendor-certified endpoints (allow-list
by SNI/domain at the NGFW); (3) monitor: sinkhole-touch alerts at
*first-touch* with paging (not digest) for these two hosts; (4) endpoint:
read-only access to their event logs centrally; EDR-lite/auditd equivalent
if vendor allows. **Residual risk (one sentence):** a compromise on those
hosts with a hardcoded-IP C2 (no DNS) and an allow-listed vendor endpoint
would evade detection until the vendor-certification window allows reimage —
accepted and time-boxed by this plan.

## Alternative Solutions

- **Block egress only (no sinkhole):** fastest to deploy; trades away the
  new-DGA visibility — explicitly worse given the 6-hour rotation.
- **NXDOMAIN sinkhole instead of logging sinkhole:** cheaper; loses the
  per-host touch telemetry that measures eradication progress.
- **Do nothing network-side; reimage the 9 hosts and isolate the 2:** leaves
  the DGA pool free to re-resolve from *any* future infected host — the
  network control is the reusable asset; endpoint cleanup is per-host and
  already scheduled.

## Tradeoffs

- Logging-sinkhole touches vs alert noise: dedupe per host per 5-min window;
  keep first-touch alerts sharp.
- Registrar-pattern RPZ rules vs false positives: pattern-blocks can catch
  benign domains; scope to the 3 specific patterns + monitor RPZ hit stats
  weekly.
- OT isolation vs vendor support: vendor-certified endpoints allow-list is
  the compromise that keeps both safety and security.

## Common Mistakes

- Saying "we lose visibility" without splitting *which* telemetry dies where.
- Treating the observed-domain list as the control (it decays in 6 hours).
- NXDOMAIN-ing without realizing it kills the touch-telemetry channel.
- Ignoring DoH as the attacker's counter-move.

## Instructor Prompts

- "Which telemetry type tells you about a domain *nobody has observed yet*?"
- "Why is a logging sinkhole a *sensor*, in one sentence?"
- "Who owns the risk acceptance for the two OT hosts, and until what date?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Telemetry ledger; DGA half-life drives the *functional* control |
| Technical accuracy | 25% | RPZ/sinkhole/deny-log mechanics; DoH escape awareness |
| Alternatives considered | 20% | Egress-only/NXDOMAIN/endpoint-only weighed |
| Communication | 15% | CIO-legible answer + one-sentence residual risk |

**Timing:** reveal at 5:00 + 2; the ledger table is the deliverable to
emulate.

## CLO Mapping

- **CLO-2** — Containment design with explicit visibility trade-offs.
