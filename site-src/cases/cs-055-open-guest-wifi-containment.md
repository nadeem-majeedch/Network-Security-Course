# cs-055 — Open Guest Wi-Fi Risk Containment

> **Simulated scenario.** The mall, SSIDs, and abuse reports are fictional.

## Difficulty & Domain

- **Difficulty:** Advanced-Advanced · **Domain:** Wireless network security · **CLO:** CLO-8
- **Est. time:** 15 minutes · **Anchor:** L17 (Wireless Fundamentals & Threats)

## Scenario

A shopping mall offers open guest Wi-Fi. Two events this month: (1) a
tenant reports a "fake mall Wi-Fi" appearing near the food court (evil-twin
suspicion); (2) mall management received an abuse notice — copyright
infringement from an IP that resolves to *their* guest egress. You must
contain both risks with an architecture: guest isolation design, the
evil-twin defense, and the egress/accountability story that keeps the mall
off the hook legally without becoming a surveillance apparatus.

## Stakeholders

- **Mall visitors** — expect free, working Wi-Fi.
- **Tenants** — their staff connect; tenant data must not be reachable.
- **Mall legal/management** — abuse-notice liability, guest privacy.
- **ISP** — forwarded the abuse notice; wants accountable egress.

## Network Context

- Open SSID `MALL-FREE`, portal with ToS checkbox, no isolation between
  guest clients (one L2), egress via mall's single public IP.
- Tenant SSIDs: `TENANT-CORP` (per-tenant PSKs) on the *same* controller,
  one shared subnet — separate SSID, same L2 segmentation failure.
- No WIPS (wireless IDS), no client isolation, portal logs ToS acceptance
  only (no identity).

## Student Task

1. Design the **guest architecture**: client isolation mechanisms (L2 +
   L3 + rate), portal policy, egress identity (per-session? per-device?),
   and the legal-accountability design — what exactly must the portal
   capture to make abuse notices actionable *without* ID cards?
2. Design the **evil-twin defense**: what a WIPS sees, what the mall can
   and cannot do about an attacker on the food-court table, and the
   *client-side* protections that actually save visitors (captive-portal
   vs TLS reality).
3. Address the **tenant-SSID finding**: same-controller, shared-subnet —
   the fix that separates tenants from guests *and from each other*, with
   the one control that stops cross-tenant snooping.

## How to Approach This (Reasoning Scaffold)

- Open Wi-Fi's real risks: (a) lateral client attacks (no isolation), (b)
  evil twins (unfixable at the AP — mitigable client-side), (c) egress
  liability (everyone shares one IP — the abuse notice problem).
- Accountability without surveillance: session-scoped identifiers +
  ToS + traffic-class policy; the portal needs *correlatable* identity
  (device/OTP), not identity documents.
- The tenant finding is the sleeper: guests and tenant PSKs sharing an
  L2 means the food-court attacker's next step is tenant traffic.

## CLO Mapping

- **CLO-8** — Public Wi-Fi architecture, liability, and threat defense.

## Safety Notes

- Design exercise; evil-twin *defense* framing only — no twin-deployment
  guidance.
