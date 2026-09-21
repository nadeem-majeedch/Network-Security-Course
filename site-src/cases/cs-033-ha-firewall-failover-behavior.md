# cs-033 — HA Firewall Failover Behavior Verification

> **Simulated scenario.** The HA pair, test log, and findings are fictional.

## Difficulty & Domain

- **Difficulty:** Intermediate · **Domain:** Firewall and ACL design · **CLO:** CLO-4
- **Est. time:** 12 minutes · **Anchor:** L10 (Firewalls — Concepts & Placement)

## Scenario

Before go-live, you verify the HA pair of firewalls (active/standby, state
synchronization enabled). The acceptance test log shows the failover "worked"
(ping resumed) but four test cases reveal *behavioral* differences the
application owners must know about. Your deliverable: failover behavior
verdicts + the config/change list.

## Stakeholders

- **Network team** — wants sign-off with documented caveats.
- **App owners** — long-lived connections (payments!) need behavior truth.
- **Change manager** — the maintenance-window procedure depends on your verdict.

## Network Context

- A/S pair, heartbeat + state-sync links, Gratuitous ARP failover on the
  upstream switch stack.
- Downstream: core switch stack; servers default-gateway to a VRRP VIP on
  the firewall pair.
- Sessions in play: HTTPS (short), payment gateway links (hours-long,
  TLS-pinned), VoIP RTP (UDP, jitter-sensitive), IPsec tunnels to partners.

## Available Evidence

**Acceptance test log (scripted):**

| Test | Action | Result | Time |
|---|---|---|---|
| T1 | Cable-pull heartbeat on primary | Standby promoted; pings resume | 4.1 s gap |
| T2 | Long-lived HTTPS (60 s idle, then resume) | Connection survived | — |
| T3 | Payment-gateway TLS session (established 30 min) | **Reset on failover**; gateway reconnected in 90 s | RST seen |
| T4 | VoIP call during failover | 4 s audio gap, then continued | — |
| T5 | IPsec to partner tunnel | **Tunnel renegotiated** (new SA) | 45 s |
| T6 | Graceful reboot primary (failback) | Preemption enabled — brief secondary gap | 2.8 s |

Config notes: state-sync ON for TCP/UDP; session sync of *in-flight* TLS
application state is not a thing (only the 5-tuple state replicates); IPsec
SA state is device-local; preemption ON.

## Student Task

1. Explain each result mechanically: why did T2 survive while T3 reset?
   Why does T4's gap happen at all with state sync? Why must T5 renegotiate?
2. Give the **failover-behavior verdict table** (session class → survives?
   → user-visible effect → mitigation).
3. Write the **change-window procedure** (5 bullets) that makes planned
   failovers non-events, and the one config change you require (preemption).

## How to Approach This (Reasoning Scaffold)

- State sync replicates *connection state* (5-tuple, sequence numbers) —
  not application-layer context (TLS keys are per-endpoint; the *client*
  doesn't re-handshake, but what breaks in T3?)
- RTP survives on *jitter tolerance* (or the gap falls in comfort noise) —
  4 s is user-audible: why does any gap exist with state sync?
- Preemption: convenient for ops, hostile to sessions — think failback
  economics.

## CLO Mapping

- **CLO-4** — HA semantics and session-fate analysis.

## Safety Notes

- Simulated acceptance test; HA verification on your own lab pair only.
