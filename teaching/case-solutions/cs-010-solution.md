---
case: cs-010
solution-for: modules/module-01-network-foundations/case-studies/cs-010-first-pass-capture-triage.md
difficulty: beginner
module: 1
lecture-anchor: L04
clos: [CLO-1]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-010 Solution — First-Pass Triage (INSTRUCTOR ONLY)

## Model Solution

**Ranked anomalies:**

1. **DNS dominates packets (41% vs <2%), 1,412 distinct names, names up to
   189 chars** — the volume × distinctness × name-length trio is the classic
   **DNS tunneling** signature (data encoded in query labels, one lookup per
   chunk). High bytes-low bytes also fits: DNS queries are small, many packets.
2. **HTTP share 18% vs 3% while HTTPS *dropped*** — plaintext traffic rose as
   encrypted traffic fell. Either a misconfiguration (something big started
   using HTTP) or deliberate plaintext C2/exfil. Two metrics moved together —
   that's why it's #2.
3. **One workstation = 2.9 GB of 6.1 GB** — nearly half the volume; combined
   with #1 it is almost certainly the tunnel endpoint; combined with #2 it
   could be a plaintext bulk transfer. Either way, identify the host first.

**#1 — two explanations and the discriminator:**

- **(a) DNS tunneling/exfiltration** (data in subdomain labels).
- **(b) A misbehaving app/update mechanism** hammering unique FQDNs (CDN
  dedup-farm, or a bug loop).
- **Discriminator: the actual query names.** Tunneling names look like
  `<high-entropy-label>.<steady-domain>.example` (one stable parent domain,
  random-looking labels); a broken updater hits a *small set of real vendor
  hostnames* repeatedly. One `dns.qry.name` sample list settles it — that's
  the next evidence item. (Acceptable secondary: the query *rate per parent
  domain*.)

**Verdict:** **suspected security incident (likely data exfiltration or C2
over DNS)** — the combination of packet-share, name length, distinctness, and
a single dominant host is not a plausible misconfiguration shape; the cost of
being wrong runs the other way. (A "misconfiguration" verdict is acceptable
only if argued with the query-name evidence request — i.e., the student's
verdict is allowed to remain conditional, but the condition must be evidence,
not hope.)

## Alternative Solutions

- **"VoIP dropped — investigate QoS first."** Defensible in a network-ops
  framing, but VoIP at 2% vs 8% is a *consequence* (bandwidth squeeze), not
  the cause; triage should chase the driver, not the symptom.
- **"Top talker is P2P/backup job."** Possible — but that hypothesis doesn't
  explain the DNS numbers; it's a #2/#3 explanation, not a #1 explanation.
- **"Insufficient evidence, collect more."** Always literally true; in triage
  you must still commit to a priority order — "collect what?" is the real answer.

## Tradeoffs

- Escalate-now vs sample-first: pulling 60 s of full packets on the top talker
  costs minutes and yields names; escalation costs an analyst-hour. Sampling
  first is usually right — but state the timebox.
- Blocking the DNS server/host immediately vs observing: blocking kills your
  visibility into the exfil; observe-with-containment (rate-limit DNS) preserves
  evidence and limits harm.

## Common Mistakes

- Ranking by "biggest number" (6.1 GB) instead of anomaly *shape*.
- Reading 41%-of-packets as 41%-of-bytes.
- Stopping at "DNS looks weird" without the tunneling-vs-updater discriminator.
- Forgetting to identify the workstation — triage that ends in "host unknown"
  isn't actionable.

## Instructor Prompts

- "Why does DNS tunneling prefer *many distinct long names* over few big ones?"
- "What one Zeek log line answers the discriminator question?"
- "The analyst on duty can do exactly one thing before lunch: what do you hand them?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Triangulated ranking; discriminator named for #1 |
| Technical accuracy | 25% | Packets-vs-bytes reasoning correct; tunneling signature right |
| Alternatives considered | 20% | Misconfiguration hypothesis honestly weighed |
| Communication | 15% | Committed verdict with priority list |

**Timing:** reveal at 5:00; this case closes Module 1 — tie back to cs-001's
inventory discipline ("know your hosts") as the follow-up action.

## CLO Mapping

- **CLO-1** — Triage over protocol summaries.
