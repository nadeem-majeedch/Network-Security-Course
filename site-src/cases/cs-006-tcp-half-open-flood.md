# cs-006 — TCP Half-Open Connection Flood Symptoms

> **Simulated scenario.** The service, hosts, and counts are fictional.

## Difficulty & Domain

- **Difficulty:** Beginner · **Domain:** TCP/IP protocol analysis · **CLO:** CLO-1
- **Est. time:** 10 minutes · **Anchor:** L03 (Protocol Deep Dive II — TCP/UDP/DNS/DHCP)

## Scenario

A small hosting provider's customer portal (TCP 8443) becomes unreachable at
09:40 for external users but responds to internal users on the same server.
The provider's monitoring shows the service process healthy. The on-call
technician restarts the service; it recovers for 20 minutes, then fails the
same way. You are given the evidence below and asked to explain the failure
mechanism before the next restart "fix" is attempted.

## Stakeholders

- **Hosting customers** — cannot reach the portal.
- **On-call technician** — wants an answer, not a theory.
- **Provider management** — SLA credits ride on time-to-mitigate.

## Network Context

- Portal behind a stateful firewall doing full TCP proxy (SYN proxy off).
- Server listen backlog: 128; per-source-IP connection limit: none.
- Load balancer health checks come from an internal subnet — these keep working.

## Available Evidence

1. **Server counters at 09:41:** `SYN_RCVD 8192 / ESTABLISHED 902 / TIME_WAIT 3110`;
   at 09:35 (healthy): `SYN_RCVD 61 / ESTABLISHED 880 / TIME_WAIT 2900`.
2. **Firewall session table:** 46,000 sessions in SYN-SENT-ish state to :8443
   from 6,100 distinct external IPs, 300+ countries; sessions from the internal
   monitoring subnet are established normally.
3. **Capture slice (external side):** SYNs arriving with no completing ACK;
   the few completing handshakes come from the monitoring subnet.
4. **Source-IP histogram:** no source IP exceeds 4 SYNs/min — no single host is "attacking."

## Student Task

1. Name the failure mechanism precisely and explain why the service *process*
   is healthy while the *service* is unavailable.
2. Explain why internal users work and why a restart "fixes" it for 20 minutes.
3. Rank these mitigations for the next hour and justify your top choice:
   SYN-proxy on the firewall · per-IP rate limit · lowering the backlog ·
   provider-level upstream filtering.

## How to Approach This (Reasoning Scaffold)

- `SYN_RCVD` is the giveaway state — ask what puts a connection there and what
  clears it.
- Distinguish "the program is alive" from "the program can accept work."
- 6,100 sources × small rates is a *shape*, not a host list — think about what
  kind of mitigation works against shapes.

## CLO Mapping

- **CLO-1** — Transport-protocol mechanics explaining an availability failure.

## Safety Notes

- Simulated incident; the mitigations discussed are defensive service
  protection on your own infrastructure.
