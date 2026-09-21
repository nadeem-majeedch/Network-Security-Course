# cs-003 — Spotting Abnormal ARP Behavior in a Clean Capture

> **Simulated scenario.** Hosts, addresses, and the capture are fictional
> teaching data.

## Difficulty & Domain

- **Difficulty:** Beginner · **Domain:** ARP and local network threats · **CLO:** CLO-1
- **Est. time:** 10 minutes · **Anchor:** L02 (Protocol Deep Dive I)

## Scenario

You support a 40-host classroom lab. For training purposes you are given a
5-minute capture taken during a quiet period. Nothing "happened" as far as the
instructor will say. You must decide whether the ARP behavior in it is normal
or not, and justify every claim from the capture itself.

## Stakeholders

- **Lab administrator** — needs a defensible yes/no with evidence.
- **Students using the lab** — unaffected if quiet, compromised if spoofed.
- **You** — your triage verdict feeds whether an investigation is opened.

## Network Context

- `10.20.0.0/24`, gateway `10.20.0.1`, one switch, no ARP hardening configured.
- All hosts are DHCP clients except the gateway (static) and one print server (static .50).

## Available Evidence

An ARP summary from the capture (gratuitous = unsolicited announcement):

| Time | Sender | Sender MAC | Target | Opcode | Note |
|---|---|---|---|---|---|
| 0:12 | 10.20.0.1 | 00:0c:29:aa:bb:01 | broadcast | reply | gw MAC as expected |
| 0:31 | 10.20.0.44 | 00:0c:29:aa:bb:2c | broadcast | request | normal resolution |
| 0:32 | 10.20.0.1 | 00:0c:29:aa:bb:01 | 10.20.0.44 | reply | — |
| 0:58 | 10.20.0.50 | 00:0c:29:aa:bb:32 | broadcast | **gratuitous reply** | announce after boot |
| 1:20 | 10.20.0.44 | 00:0c:29:aa:bb:2c | broadcast | request | repeat for .50 |
| 1:21 | 10.20.0.50 | 00:0c:29:aa:bb:32 | 10.20.0.44 | reply | — |
| 2:05 | 10.20.0.44 | 00:0c:29:aa:bb:2c | broadcast | request | gateway lookup |
| 2:06 | 10.20.0.1 | **00:0c:29:aa:bb:99** | 10.20.0.44 | reply | **MAC ≠ table above** |
| 2:07 | 10.20.0.1 | 00:0c:29:aa:bb:01 | 10.20.0.44 | reply | real gw MAC again |
| 3:40 | 10.20.0.44 | 00:manycasts | broadcast | request | normal noise |

## Student Task

1. Mark each reply line **normal / suspicious / decisive-red-flag**, with a
   one-line reason tied to the table.
2. State what `...:99` advertising itself as the gateway is called and what it
   would enable an attacker to do on this LAN.
3. Decide: is one conflicting reply "an incident"? What single additional
   evidence item would you request before escalating, and why that one?

## How to Approach This (Reasoning Scaffold)

- Compare replies *against the host's own legitimate answer* — a conflict is
  only meaningful relative to the known-good MAC.
- Gratuitous announcements are normal at boot; judge by sender identity.
- A single spoofed reply wins the race only until the legitimate host replies
  again — think about cache overwrite timing, then about what persistence
  the attacker needs.

## CLO Mapping

- **CLO-1** — Protocol-level reasoning to identify threat indicators.

## Safety Notes

- Simulated capture; analysis is read-only. Real-world equivalents must be
  restricted to networks you administer or are authorized to test.
