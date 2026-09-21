# cs-082 — Ransomware Pre-Encryption: Wait or Act?

> **Simulated scenario.** All events, hosts, and telemetry are fictional.

## Difficulty & Domain

- **Difficulty:** Expert · **Domain:** Multi-stage security incidents · **CLO:** CLO-11, CLO-12
- **Est. time:** 15 minutes · **Anchor:** L26 (Detection, Triage & Containment)

## Scenario

You are the on-call analyst for a mid-size logistics firm. At 21:47 an
EDR alert fires on a file server: mass file-rename activity. Two
minutes earlier, the same host showed a scheduled-task creation and a
new service. You suspect the pre-encryption stage of a ransomware
event. The CFO is asleep; the CEO is pinging you. Do you kill the host
now, or wait for the encryption to confirm and risk the whole file
share?

## Stakeholders

- **SOC (you)** — owns the next 10 minutes.
- **File-server owner** — the share serves 400 staff.
- **Backup operator** — offline copies, 6-hour RPO.
- **Executive** — wants a one-line answer, now.

## Network Context

- File server: 8 TB share, 200 concurrent SMB users by day.
- Backups: nightly, offline, verified — last run 18:00 (RPO ≈ 6 h).
- EDR covers servers; no NDR on the server VLAN; flow records exist.
- Perimeter egress via proxy; the host has been idle for weeks.

## Available Evidence

| T | Event |
|---|---|
| 21:44 | new scheduled task + new service on FS01 (EDR) |
| 21:45 | outbound TLS to a previously unseen domain (proxy, 2 MB in 3 min) |
| 21:47 | mass file-rename activity (EDR behavioral rule) |
| 21:48 | SMB share handles spike from one workstation (flow) |

## Student Task

1. Decide: **act now vs wait for confirmation**. Justify with the
   evidence *and the cost of each wrong answer* (act-wrong vs
   wait-wrong).
2. Give the **containment sequence** you would run in the next 10
   minutes, labeled reversible/irreversible.
3. Name the **two telemetry gaps** that made this hard, and the one
   control that would have removed the ambiguity.
4. Draft the **one-line executive answer** (what happened, what you
   did, what you need).

## How to Approach This (Reasoning Scaffold)

- Asymmetry of errors: acting on a false positive costs a reboot;
  waiting on a true positive costs a share. When the cost ratio is
  this lopsided, act.
- Pre-encryption stages (staging, shadow-copy tampering, task
  creation) are the *only* window where containment is cheap.
- The 2 MB egress before renaming suggests staging — this is not a
  rename glitch.

## CLO Mapping

- **CLO-11** — Containment decision under time pressure.
- **CLO-12** — Correlating endpoint + perimeter + flow signals.

## Safety Notes

- Simulated scenario; no ransomware samples or destructive payloads.
