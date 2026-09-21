# cs-052 — WireGuard Rollout Design for Remote Staff

> **Simulated scenario.** The agency, fleet, and constraints are fictional.

## Difficulty & Domain

- **Difficulty:** Advanced-Advanced · **Domain:** VPN and secure remote access · **CLO:** CLO-7
- **Est. time:** 12 minutes · **Anchor:** L16 (Modern VPNs & Crypto-Agility)

## Scenario

A digital agency (150 remote staff, no offices) wants to replace its aging
SSL-VPN with WireGuard. Security requirements: per-device keys, identity
tie-in, no shared PSKs, session logging for compliance, and MFA somewhere.
WireGuard has no built-in MFA, no user directory, and no logging — design
the **architecture that adds what WireGuard lacks** without breaking what
it is (fast, simple, modern crypto).

## Stakeholders

- **Staff** — expect always-fast connectivity; hate reconnect prompts.
- **Compliance** — client-audit trail: who connected, from where, when.
- **Security** — key lifecycle, revocation, no lateral trust between staff.
- **Ops (2 people)** — must run this without a VPN-ops team.

## Network Context

- Current: legacy SSL-VPN, per-user passwords + MFA at the portal, session
  logs to SIEM, slow (user complaints).
- Target services: internal admin panels, Git, CI, staging environments.
- Fleet: macOS/Windows/Linux laptops; phones for on-call only.
- Compliance scope: connection metadata logs, 1-year retention.

## Student Task

1. Design the **architecture**: coordination/control plane (what manages
   peers/keys), gateway topology (hub vs mesh — pick with reasons), and
   the identity-MFA integration pattern that WireGuard doesn't natively
   have (name the standard pattern and where MFA lands).
2. Define the **key lifecycle**: per-device key generation, enrollment,
   rotation cadence, revocation (staff departure, lost laptop), and the
   compliance logging design (what's logged where, given WireGuard's
   silence).
3. Name the **two security properties WireGuard gives up** versus the
   legacy SSL-VPN in this design (e.g., post-auth app-layer session
   control), and the compensating control for each.

## How to Approach This (Reasoning Scaffold)

- WireGuard is a *data plane*; everything else (identity, MFA, logging,
  revocation) is your **control plane** — design it explicitly.
- MFA lands at *enrollment/re-auth of the control plane* and at the
  gateway's SSO front door, not inside the WireGuard handshake — say
  precisely where.
- Hub vs mesh: staff-to-staff traffic needs? Usually zero — hub-and-
  spoke with per-peer ACLs is simpler and audit-friendly.

## CLO Mapping

- **CLO-7** — Modern VPN architecture with control-plane design.

## Safety Notes

- Design exercise; no configuration dumps beyond architecture-level.
