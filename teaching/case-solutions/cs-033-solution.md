---
case: cs-033
solution-for: modules/module-03-secure-architecture/case-studies/cs-033-ha-firewall-failover-behavior.md
difficulty: intermediate
module: 3
lecture-anchor: L10
clos: [CLO-4]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-033 Solution — HA Failover Behavior (INSTRUCTOR ONLY)

## Model Solution

**Mechanics per test:**

- **T2 (idle HTTPS survives):** state-sync replicated the 5-tuple + sequence
  context; after 60 s idle the resumed packets match the replicated state —
  the new active forwards them. Application unaware.
- **T3 (payment TLS reset):** the 5-tuple state *replicated*, but the
  session's liveness depends on the payment gateway's TLS/application
  keepalives; during the 4.1 s promotion window + G-ARP convergence, missed
  keepalives/ACKs triggered the *gateway's* timeout → RST. (Sub-case worth
  teaching: some TLS stacks treat mid-session address/ARP transition as
  hostile.) The 90 s reconnect is the application's own retry — acceptable,
  but it's a *visible* event for payments.
- **T4 (VoIP 4 s gap):** state-sync for UDP replicated the flow, but the
  *first* seconds after promotion still drop: ARP re-learning downstream +
  the standby's forwarding tables warming. RTP's jitter buffer absorbs some
  (comfort noise), but 4 s is audible — state sync ≠ zero-gap.
- **T5 (IPsec renegotiated):** SA/child-SA state is **device-local** (keys,
  counters); it is not part of session sync. New active must re-IKE. 45 s is
  normal; partner sees a blip.

**Verdict table:**

| Session class | Survives failover? | User-visible effect | Mitigation |
|---|---|---|---|
| Short/idle HTTPS | ✅ | none | — |
| Long-lived TLS (payments) | ⚠️ *mostly* — resets on keepalive-timeout races | one reconnect (90 s) | app-side retry/backoff; schedule failovers in low-volume windows; ask vendor for graceful-LB/timeout tuning |
| VoIP RTP | ⚠️ brief gap | ≤4 s audio | none needed beyond expectation-setting; QoS priority |
| IPsec tunnels | ❌ (renegotiates) | 45 s tunnel blip | DPD tuning; partner-notification in change plan; consider dual-tunnel to second peer |
| Any | — | 2.8–4.1 s promotion gap | failover testing cadence; alarms on heartbeat loss |

**Change-window procedure (planned failovers become non-events):**

1. Announce + verify low-volume window (payments dashboard check).
2. Force failover to standby; wait promotion (verify via mgmt plane, not pings).
3. Observe T3-class sessions: payment-gateway reconnects count = the
   acceptance metric; abort/rollback if >N.
4. Verify IPsec re-establishment to *all* partners (checklist per tunnel).
5. Post-change: watch drop counters + app-owner channels for 30 min;
   document session-survival stats in the change record.

**Required config change: disable preemption** (or preemption with dwell
timer + scheduled failback window). Failback's 2.8 s gap exists *only* for
ops convenience — sessions pay for it twice. Failback should be a planned
event, not an automatic one.

## Alternative Solutions

- **Active/active with session load-sharing:** halves the blast radius
  (half the sessions fail) — a real option at this vendor tier; costs
  asymmetric-routing discipline and licensing; mention as roadmap.
- **Move long-lived TLS off the firewall path (SD-WAN/LB termination):**
  architectural answer for payments; out of scope this cycle.

## Tradeoffs

- State-sync completeness vs heartbeat timing: tighter hello/dead timers
  shorten T1's gap but raise false-failover risk on flappy links — test
  with cable-pull *and* link-degradation, not just pull.
- Preemption-on vs session cost: ops convenience vs user-visible blips;
  dwell timers are the compromise if policy requires preemption.

## Common Mistakes

- Claiming "state sync = zero impact" — T3/T4/T5 are the counter-evidence.
- Attributing T3's reset to the firewall "dropping" the session (it's the
  *endpoint's* keepalive timeout).
- Leaving preemption on because "it sounds right."
- No per-tunnel IPsec verification step in the procedure.

## Instructor Prompts

- "What exactly replicates, and what never can?"
- "Why is failback worse than failover for sessions?"
- "Which acceptance metric would you put in the change record?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Replicated-vs-local state distinction per test |
| Technical accuracy | 25% | G-ARP/keepalive/SA mechanics correct |
| Alternatives considered | 20% | A/A + architectural options weighed |
| Communication | 15% | Verdict table + 5-bullet procedure |

**Timing:** reveal at 5:00 + 2; "what replicates and what never can" is the
core sentence.

## CLO Mapping

- **CLO-4** — HA semantics and session-fate analysis.
