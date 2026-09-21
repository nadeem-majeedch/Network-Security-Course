---
lecture: L20
title: Cloud Networking II — Hybrid & Assurance
module: 5
week: 10
hours: 2
clos: [CLO-13]
difficulty: intermediate-advanced
status: complete
artifact-type: student-lecture-material
instructor-plan: modules/module-05-wireless-cloud/lectures/lecture-20-cloud-hybrid-assurance.md
---

# L20 — Cloud Networking II — Hybrid & Assurance

## 1. Learning Objectives

By the end of this session you can: (1) design hybrid connectivity (VPN vs dedicated interconnect; hub-and-spoke with forced inspection); (2) apply private-access patterns and hybrid DNS design; (3) explain container networking and write default-deny NetworkPolicies — and verify they *enforce*; (4) operate assurance: flow-log analytics, change alarms, reachability analysis; (5) produce a shared-responsibility matrix for a given architecture.

## 2. Key Definitions

| Term | Definition |
|---|---|
| Transit gateway / hub-spoke | Central routing hub; peering alone is **not transitive** |
| Dedicated interconnect | Physical private connectivity (DX/ExpressRoute-class) |
| Private link/endpoint | Provider/SaaS services reachable over private paths |
| Split-horizon DNS | Different answers for internal vs external query sources |
| Pod / netns | Container's isolated network namespace; veth pair to the CNI bridge |
| CNI | Container Network Interface plugin — implements pod networking *and* policy |
| NetworkPolicy | Kubernetes L3/L4 policy: selectors + ports; **requires an enforcing CNI** |
| Config drift | Manual changes diverging from declared IaC state |
| Reachability analysis | Tool-computed "who can talk to whom" from SG/route state |

## 3. Detailed Explanations

### 3.1 Hybrid connectivity patterns
Options ladder: internet+TLS → site-to-site VPN (your L15 IPsec skills, cloud edition) → dedicated interconnect (predictable latency/capacity, cost). Topology: **hub-and-spoke** with a central inspection VPC — spoke↔spoke traffic is *forced* through the hub firewall by route tables; **peering is not transitive**, so "SpokeA↔Hub, SpokeB↔Hub" does not connect SpokeA↔SpokeB (the classic broken-hybrid bug). Routing *is* the policy: if the route table doesn't send traffic through the inspection point, your firewall is decorative.

### 3.2 Private access and hybrid DNS
**Private endpoints** put provider services on private IPs (SG/endpoint-policy allow-lists — L12's skill). **PrivateLink-class** publishes your services to other VPCs/accounts without internet exposure. **Hybrid DNS** is where hybrids break: split-horizon views (internal names resolvable from cloud via forwarders/endpoints); a misconfigured forwarder leaks internal names or black-holes them. DNS is the soft spot — design it explicitly, not as an afterthought.

### 3.3 Container networking security
A pod gets its own network namespace with a veth pair to the CNI. **Default is flat**: any pod can reach any pod — L09's flat network reborn. **NetworkPolicy** fixes it: `policyTypes: [Ingress, Egress]` with a default-deny skeleton, then allow-pairs (pod/namespace selectors + ports). Two non-negotiables: **the CNI must enforce NetworkPolicy** (many defaults don't — "policies exist" ≠ "policies work" is the classic audit finding), and **default-deny first**, allow after. East-west visibility comes from CNI flow telemetry (Hubble-class) — the cloud-native flow log.

### 3.4 Assurance and drift control
- **Flow-log analytics:** top-talkers, reject spikes, new-destination learning → baselines for L23.
- **Change alarms:** SG/route/peering modifications page a human; IaC drift detection flags manual console changes — "who changed the firewall" is answered with an event, not a meeting.
- **Reachability analysis:** tools compute effective reachability from SG+route state — reading rules one-by-one misses the interactions; graphs catch them.

### 3.5 The shared-responsibility matrix (capstone artifact)
Per service row (IaaS VM, managed DB, container platform, SaaS): provider duties (fabric, hypervisor isolation, physical) vs **your** networking duties (segmentation, SG policy, egress, DNS, encryption in transit, flow-log review). The audit questions: who can change routing? who holds endpoint policies? where does egress leave your trust boundary? who reads the flow logs?

## 4. Network Diagram: hub-spoke + container policy

```
 SpokeA ──► [HUB: inspection VPC — firewall] ◄── SpokeB
     (route tables force spoke↔spoke through the hub;
      peering alone would black-hole A↔B — not transitive)

 Pod network (default flat!)                With NetworkPolicy:
 [pod][pod][pod] — any→any                  db: deny all → allow 5432 from api only
                                            api: deny all → allow from frontend
                                            enforcement: CNI-dependent — VERIFY
```

## 5. Protocol Examples

```
 apiVersion: networking.k8s.io/v1
 kind: NetworkPolicy
 metadata: { name: db-default-deny, namespace: prod }
 spec:
   podSelector: { matchLabels: { app: db } }
   policyTypes: [Ingress, Egress]
   ingress:
   - from: [{ podSelector: { matchLabels: { app: api } } }]
     ports: [{ port: 5432, protocol: TCP }]
   egress: []            # the DB talks to nothing — strictest sane posture
```
- Flow-log anomaly drill: `app-tier → 1.2.3.4:443 every 60s ~2KB` = beacon candidate (L21/L23 methodology); `data-tier → external REJECT` = scoped egress *working*.

## 6. Configuration Concepts (concept level)

- Hub route-table diff proving inspection is unavoidable; TGW attachment for transitivity where needed.
- Private-endpoint policy allow-lists; conditional forwarders documented per zone.
- NetworkPolicy test harness: deploy a test pod, attempt the denied flow, confirm rejection.

## 7. Security Implications

- Hybrid works when routing *forces* inspection; peering alone is not a design.
- Containers default flat — NetworkPolicy with a *verifying* CNI is the fix; assume nothing enforces until tested.
- Drift is the cloud threat actor's quiet ally: alarms + IaC discipline keep design = reality.

## 8. Realistic Organizational Scenario

**The egress mandate (running case).** Security mandates data-tier isolation after an audit; dev teams push back ("ETL needs the internet"). Provided: route/SG dump plus a month of flow logs. Your deliverable: classify destinations from the logs, author the egress policy set (data-tier private-endpoint-only; app-tier NAT + domain allow-lists), design a time-boxed exception workflow, and define success metrics (reject-rate trend, exception count) plus the bypass detection (direct-to-IP attempts). Full case: **cs-064**; the flow-log lab + alarm is the in-session exercise. Quiz 4 (W10) samples L19–L20; Assignment 7 (W14) builds on both.

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "Peering is transitive" | It is not; spokes can't see each other without a hub/TGW design. |
| "Containers inherit host security" | Pod networking is its own namespace; flat-by-default until policy enforces. |
| "NetworkPolicy is enabled by default" | It's an API; enforcement depends on the CNI. |
| "Flow logs are an IDS" | They're metadata — detection comes from analysis on top (L21+). |
| "IaC means no drift" | Manual console changes drift silently without alarms and reconciliation. |

## 10. Classroom Activities

1. **Transitivity bug diagnosis (sandbox):** SpokeA↔Hub OK, SpokeB↔Hub OK, A↔B black-hole — fix with hub routing; show the route-table diff.
2. **NetworkPolicy lab:** apply default-deny to a DB; verify enforcement with a denied test pod; add the api→db allow.
3. **Flow-log + alarm lab (pairs):** find the beacon candidate, the policy-verification line, the new-destination outlier; create an SG-change alarm and trigger it.

## 11. Problem-Solving Questions

1. Design the hub that makes spoke↔spoke inspection *unavoidable* — show the route-table diff.
2. Why does DNS break hybrids more often than routing? Give the split-horizon failure that leaks internal names.
3. "We have 40 NetworkPolicies" — what's the first enforcement question, and how do you verify?
4. Which flow-log pattern would you alert on first, and what's the false-positive risk?
5. For managed Kubernetes: write the responsibility-matrix networking rows (CNI policy, node SGs, pod egress).

## 12. Exit Ticket

1. True/false: VPC peering is transitive. What construct provides transitive routing?
2. What two things must exist before a NetworkPolicy actually filters traffic?
3. Name the three parts of a default-deny NetworkPolicy for a DB pod.
4. Which alarm answers "who changed the route table"?
5. Give one customer-side networking duty shared responsibility never transfers to the provider.

*(Answers: `teaching/answer-keys/answer-key-module-05.md`.)*

## 13. References

- AWS Transit Gateway & PrivateLink guides; Azure hub-spoke and Private Link docs (current).
- Kubernetes docs — NetworkPolicy API and CNI enforcement notes; Cilium/Hubble docs.
- CIS Benchmarks — cloud and Kubernetes sections.
- CNCF — cloud native network security whitepapers.

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-13 | §3 hybrid/container/assurance skills | Quiz 4 (partial), Quiz 5 (W14), Assignment 7, Lab-10 |
