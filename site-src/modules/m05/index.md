---
status: complete
artifact-type: module-overview-page
module: 5
instructor-only: false
---

# Module 5 — Wireless & Cloud Network Security

**Lectures:** L17–L20 (Weeks 9–10) · **CLOs:** CLO-7, CLO-13 · **Cases:** cs-054–067

*Descriptive orientation. Wireless analysis uses lab APs and authorized
captures only; cloud work runs in the course's isolated project.*

## What this module covers

Half the network is now invisible — radio. The other half is someone else's
datacenter. You learn wireless threat mechanics and enterprise defense
(802.1X/EAP, WPA2/3), then translate the same zone-and-control thinking to
cloud VPCs: security groups, NACLs, route tables, and hybrid assurance.

## Lectures

| # | Lecture | Core idea |
|---|---|---|
| L17 | [Wireless Fundamentals & Threats](../../lectures/lecture-17-wireless-fundamentals-threats.md) | 802.11 management frames, evil twins, deauth, WEP/WPA lessons |
| L18 | [Enterprise Wireless & Rogue Defense](../../lectures/lecture-18-enterprise-wireless-rogue-defense.md) | 802.1X/EAP-TLS, WPA-Enterprise, rogue AP detection & response |
| L19 | [Cloud Networking I — VPC Design & Controls](../../lectures/lecture-19-cloud-networking-vpc-design.md) | VPC/SG/NACL model, route tables, egress design |
| L20 | [Cloud Networking II — Hybrid & Assurance](../../lectures/lecture-20-cloud-hybrid-assurance.md) | Site-to-cloud VPN, flow logs, shared-responsibility security posture |

## Labs

[Lab-09](../../labs/lab-09-wireless-characterization-cloud-segmentation.md) (wireless
characterization + VPC segmentation) and
[Lab-10](../../labs/lab-10-wpa-enterprise-cloud-flow-logs.md) (WPA-Enterprise
build + cloud flow-log analysis).

## Case studies (advanced tier begins)

cs-054–067: evil-twin evidence, deauth-storm diagnosis, 802.1X rollout
failure, SSID segmentation design, SG-vs-NACL reachability math, VPC egress
strategy, flow-log interpretation, hybrid assurance gaps. See the
[case studies guide](../../cases/index.md).

## Skills checkpoints

- Explain why open management frames enable wireless attacks and which controls mitigate each class.
- Compare WPA-Personal and WPA-Enterprise operationally and architecturally.
- Predict whether a flow is permitted by a given SG + NACL + route-table combination.
- Interpret VPC flow logs to classify accepted/rejected traffic patterns.
