---
diagram: 01-enterprise-segmentation
type: network-architecture
used-by: [L09, L10, L12, L26]
status: complete
---

# Diagram — Enterprise Segmentation Architecture

> **Conceptual reference model — not an exact production configuration.**
> Zone names, addressing, and product placement vary per organization.

```mermaid
flowchart TB
    Internet((Internet)) --> |"ingress: allow 80/443 only"| FW1[Edge firewall]
    FW1 --> |"DMZ segment 172.16.1.0/24"| DMZ[Public web / reverse proxy]
    DMZ --> |"allow 8443 to app tier only"| FW2[Inner firewall]
    FW2 --> |"server VLAN 10.20.0.0/24"| APP[Application tier]
    APP --> |"allow 3306 from app tier only"| FW3[Segment firewall]
    FW3 --> DB[(Database tier 10.30.0.0/24)]
    FW2 --> USERS[User VLANs 10.10.0.0/16]
    FW3 -. "telemetry tap: Zeek/NDR" .-> SENSOR[Detection sensor]
    FW1 & FW2 & FW3 -. "logs" .-> SIEM[SIEM]
```

ASCII ground truth:

```
                    ┌──────────────┐
                    │   INTERNET   │
                    └──────┬───────┘
              allow 80/443 │
                    ┌──────▼───────┐      logs      ┌────────┐
                    │ EDGE FIREWALL│───────────────►│  SIEM  │
                    └──────┬───────┘                └────────┘
                           │  DMZ 172.16.1.0/24
                    ┌──────▼───────┐
                    │  PUBLIC WEB  │  (reverse proxy, no data)
                    └──────┬───────┘
              allow 8443   │
                    ┌──────▼───────┐      tap         ┌────────┐
                    │INNER FIREWALL│·················►│  ZEEK  │
                    └──────┬───────┘  (server VLAN)  └────────┘
             ┌─────────────┼──────────────┐
             │ 10.10.0.0/16│ 10.20.0.0/24 │
      ┌──────▼─────┐ ┌─────▼──────┐ ┌─────▼──────┐
      │ USER VLANs │ │  APP TIER  │ │ SEGMENT FW │──allow 3306──► DB TIER
      └────────────┘ └────────────┘ └────────────┘      10.30.0.0/24
```

**Text description (accessibility):** the internet reaches only the edge
firewall, which admits web ports into a DMZ holding a reverse proxy. The
proxy is the only host allowed to start connections into the application
tier through the inner firewall; user VLANs sit behind the same inner
firewall; the database tier is reachable only from the application tier
on its service port. Every firewall forwards logs to the SIEM, and a
Zeek sensor taps the server-VLAN span port.
