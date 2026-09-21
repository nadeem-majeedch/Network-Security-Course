---
case: cs-035
title: Least-Privilege Egress ACL Authoring
difficulty: intermediate
domain: Firewall and ACL design
module: 3
lecture-anchor: L11
clos: [CLO-4]
time-estimate: 12 min (5 min reasoning + 7 min debrief)
status: complete
artifact-type: student-case
instructor-solution: teaching/case-solutions/cs-035-solution.md
---

# cs-035 — Least-Privilege Egress ACL Authoring

> **Simulated scenario.** The plant, systems, and destinations are fictional.

## Difficulty & Domain

- **Difficulty:** Intermediate · **Domain:** Firewall and ACL design · **CLO:** CLO-4
- **Est. time:** 12 minutes · **Anchor:** L11 (ACLs & Rulebase Engineering)

## Scenario

An industrial plant's office VLAN egresses to the internet unrestricted.
After a ransomware event at a sister plant, the insurer requires a
**least-privilege egress ACL** for the office VLAN. You have the observed
flows (below). Write the ACL: explicit allows, default deny, with the
*domains vs IPs* decision made explicit — and defend how the design survives
CDN-shared infrastructure without becoming "permit any 443."

## Stakeholders

- **Insurer** — wants demonstrable least-privilege.
- **Office staff** — email, ERP SaaS, vendor portals, print-cloud.
- **Plant IT (2 people)** — must maintain the ACL without a SIEM.
- **Attackers** — ransomware's exfil and C2 now face your egress.

## Network Context

- Office VLAN `192.168.20.0/24`, one egress firewall, no proxy.
- No internal DNS logging; resolvers forward to public.
- Systems: staff PCs, 2 printers (cloud-print), 1 building controller
  (vendor cloud), 1 ladder-laptop (engineering, seasonal).

## Available Evidence

**14-day observed egress (deduplicated by destination service):**

| Service | Destination | Ports | Users | Notes |
|---|---|---|---|---|
| Email SaaS | `*.mailprovider.example` + shared mail CDN | 443 | all | cert/SNI stable |
| ERP SaaS | `erp.company.example` (own domain, fixed IPs published) | 443 | all | vendor publishes 4 IPs |
| Vendor portals | 6 vendors, own domains | 443 | 12 staff | — |
| Print cloud | `print.example-cloud.com` | 443 | printers | 2 printer MACs |
| BMS vendor | `bms.vendor.example` (1 IP published) | 443 | building controller | safety-relevant |
| Windows Update | `*.windowsupdate.example` + CDN | 80,443 | all PCs | CDN-shared |
| Misc HTTPS long tail | 700+ SNIs | 443 | all | includes streaming, shopping |
| Direct DNS | 8.8.8.8, 1.1.1.1 hardcoded on 9 PCs | 53 | — | policy violation found |

## Student Task

1. Write the **egress ACL** (10 rules max): explicit allows (domain/SNI-based
   or IP — your choice, justified), the hard-coded-DNS remediation rule, and
   the default deny. Mark which rules are *enforceable* vs *aspirational*
   given no proxy/TLS inspection.
2. Resolve the **CDN dilemma**: Windows Update lives on shared CDN IPs that
   host everything — explain why "permit CDN-IP:443" is a fake control and
   give the two real alternatives.
3. State the **ransomware-value** of this ACL in 2 sentences: which attack
   steps does it actually degrade (C2? exfil? staging?) and which it cannot.

## How to Approach This (Reasoning Scaffold)

- Least privilege is *proportional to controllability*: vendor-published IPs
  are strong anchors; shared CDNs are weak anchors — pick anchors honestly.
- Hard-coded DNS isn't just policy mess — it's an *egress bypass*; the ACL
  must handle it (allow internal resolvers, deny external :53).
- The insurer wants *demonstrable* — every allow needs an owner and a reason
  string that survives an audit read-aloud.

## CLO Mapping

- **CLO-4** — Least-privilege egress engineering with honest anchors.

## Safety Notes

- Design exercise; egress controls are defensive.
