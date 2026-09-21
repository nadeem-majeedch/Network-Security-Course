# cs-089 — Tainted Update: Multi-Stage Intrusion via a Trusted Channel

> **Simulated scenario.** The vendor, intrusion, and all telemetry are fictional; not based on any historical event.

## Difficulty & Domain

- **Difficulty:** Expert · **Domain:** Multi-stage security incidents · **CLO:** CLO-11, CLO-12, CLO-15
- **Est. time:** 20 minutes · **Anchor:** L26 (Triage & Containment) + L28 (Threat Intelligence)

## Scenario

A widely deployed operations-monitoring agent auto-updated across
your estate three weeks ago. Yesterday, TI flagged the update
channel as serving tainted builds to some customers. You have ~4,000
endpoints and 600 servers running the agent. Legal has asked what
you know; the vendor is sending a "clean" build tomorrow; the CEO
wants to know if you're affected *today*. You must scope a
multi-stage intrusion where the entry vector was *trusted
infrastructure* — and the attacker's dwell depends on what the
tainted build actually did.

## Stakeholders

- **SOC/IR (you)** — scoping under time pressure.
- **Legal/comms** — disclosure posture needs evidence, not guesses.
- **Vendor** — cooperative but slow; their telemetry ≠ your truth.
- **CEO** — one question: are we affected?

## Network Context

- Agent: auto-update channel (HTTPS), vendor-signed builds, update
  rings: pilot (50), early (400), broad (4,150).
- Telemetry: EDR fleet-wide, proxy logs (90-day), Zeek at the edge,
  AD sign-ins, flow records.
- The vendor says: "tainted builds deployed between day −21 and day
  −14; builds before/after clean; behavior varies by environment."

## Available Evidence

**Fleet telemetry, day −21 → today:**

| Signal | Observation |
|---|---|
| EDR | 3 servers show anomalous child processes from the agent (day −19, −18, −17); 0 endpoints |
| Proxy | 3 same servers → 6 unknown domains, low-volume HTTPS, day −19 onward, ~90 min/day cadence |
| Zeek | same 3 servers; TLS SNI matches proxy findings; no other hosts |
| AD | svc_ops (agent's service account) used interactively on 1 of the 3 servers, day −17 |
| Flow | the 3 servers → 2 internal servers (backup infra + build server) starting day −16 |

## Student Task

1. Scope the intrusion: **who is affected** (hosts), **how deep**
   (stages reached), with the evidence for each stage of your
   judgment — and the honest "cannot determine" set.
2. Answer the **vendor-trust question**: which vendor claims can you
   *verify locally* (update manifests, build hashes, EDR timeline)
   and which must you take on faith? What do you ask them for?
3. Produce the **containment strategy for a trusted-channel
   compromise**: what changes when the *delivery mechanism* is the
   attacker (vs one host)? Sequenced, with the update-channel
   decision (halt? pin? replace?).
4. Answer the CEO: a **three-sentence status** — affected?, doing
   what, what you need — that stays true as facts develop.

## How to Approach This (Reasoning Scaffold)

- Trusted-channel compromise scopes by *channel*, not by symptom:
  everyone who received the tainted build is suspect until proven
  otherwise — but "suspect" ≠ "affected"; evidence stratifies.
- The service account is the pivot: agent → svc_ops → interactive
  use → internal spread. Cut the identity path, not just the hosts.
- Vendor claims are *hypotheses* with provenance; your telemetry is
  *evidence*. Verify what's verifiable (build hash on a tainted-ring
  host, manifest timeline) before betting containment on their story.

## CLO Mapping

- **CLO-11** — Scoping multi-stage intrusions.
- **CLO-12** — Local verification vs external claims.
- **CLO-15** — Capstone-level synthesis (architecture + IR + intel).

## Safety Notes

- Simulated; no real vendor or incident; no exploit detail.
