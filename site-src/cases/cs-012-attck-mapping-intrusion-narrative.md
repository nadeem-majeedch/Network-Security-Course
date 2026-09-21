# cs-012 — Mapping an Intrusion Narrative to ATT&CK Tactics

> **Simulated scenario.** The intrusion narrative is fictional, written for
> teaching; it resembles no specific real incident.

## Difficulty & Domain

- **Difficulty:** Beginner (stretch) · **Domain:** Network security principles · **CLO:** CLO-2
- **Est. time:** 10 minutes · **Anchor:** L05 (Threat Modeling & Attacker Anatomy)

## Scenario

You are given a sanitized post-incident narrative (below) from a logistics
company. Your SOC manager wants the story expressed in ATT&CK tactic terms so
the team can see *where detections existed and where they didn't*.

## Stakeholders

- **SOC manager** — wants tactic-level coverage mapping.
- **IT operations** — featured in the narrative (VPN without MFA).
- **Executive team** — will read the summary line of your mapping.

## Network Context

- Remote staff connect via VPN with username+password only.
- File servers hold customer shipment data.
- Egress web is proxied; DNS is not logged centrally.

## Available Evidence

**Sanitized narrative (fictional):**

> 1. Attacker bought an employee's password from a criminal marketplace.
> 2. Logged into the company VPN at 02:50 from a residential IP.
> 3. Scanned internal subnets from the VPN session, found file servers.
> 4. Accessed `\\fs01\finance` shares with the same reused password.
> 5. Copied 2 GB of finance spreadsheets over SMB for 40 minutes.
> 6. Deleted the VPN session logs before disconnecting (admin rights on VPN box
>    via a default credential).

## Student Task

1. For each numbered step, name the **ATT&CK tactic** (e.g., Initial Access,
   Discovery, Collection, ...) and a one-phrase technique description in your
   own words — exact technique IDs are welcome but not required.
2. Identify the **earliest point** the attacker was detectable with the
   company's *current* logging (state what log would have caught it).
3. Name the **two tactics** where the company had *zero* chance of detection
   as configured, and what one logging change each would need.

## How to Approach This (Reasoning Scaffold)

- Tactics are the *why* (objective); techniques are the *how*. Sort the
  narrative into objectives first.
- "Detectable with current logging" is a factual question — check each step
  against the stated logging (VPN, proxy, SMB/file server, no DNS).
- The narrative ends with log deletion — that tactic has implications for
  what you can trust in the story.

## CLO Mapping

- **CLO-2** — Kill-chain/ATT&CK framing of an intrusion.

## Safety Notes

- Fictional narrative; ATT&CK is a public defensive framework. No exploit
  detail is requested or provided.
