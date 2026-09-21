---
lecture: L20
title: Cloud Networking II — Hybrid & Assurance
module: 5
week: 10
hours: 2
clos: [CLO-13]
difficulty: intermediate-advanced
status: complete
artifact-type: teaching-plan
---

# L20 — Cloud Networking II — Hybrid & Assurance

## 1. Overview & Prerequisites

- **Prerequisites:** L19 (VPC design, SG/NACL, flow logs), L13 (TLS/mTLS for private connectivity), L12 (egress policy — same skill, cloud scale).
- **Position:** closes Module 5: hybrid connectivity (transit/peering, VPN/DX), container networking security (NetworkPolicy), and assurance tooling (change alarms, config posture). Quiz 4 (W10) includes L19–L20 items; Assignment 7 (W14) builds on both cloud lectures.
- **Faculty prep:** pre-create hub-and-spoke sandbox VPCs with one deliberate peering misroute; prepare the NetworkPolicy starter pack (K8s cluster in the range); sample flow-log dataset for the lab.
- **Common misconceptions:** "peering is transitive"; "containers inherit the host's security"; "NetworkPolicy is enabled by default"; "flow logs = IDS."

## 2. Learning Objectives

By the end of this lecture, students can:

1. Design hybrid connectivity: site-to-site VPN vs dedicated interconnect (DX/ExpressRoute), hub-and-spoke vs mesh, and transitivity via transit gateway/router (Create/Evaluate).
2. Apply private connectivity patterns: private endpoints, private links to SaaS, and DNS resolution design for hybrid (split-horizon) (Create).
3. Explain container networking security: container netmodel (veth/bridge, CNI), default flat-network risk, and NetworkPolicy (default-deny + allow-pairs) (Analyze/Create).
4. Enable assurance controls: flow-log analysis, config-drift alarms, network posture baselining (CIS-cloud benchmarks) (Apply/Evaluate).
5. Compare on-prem vs cloud shared-responsibility implications for a given architecture and produce the responsibility matrix (Evaluate).

## 3. Detailed Concepts

### 3.1 Hybrid connectivity patterns
- Options ladder: internet+TLS (cheap, variable), site-to-site VPN (IPsec from L15 — the same skills), dedicated interconnect (DX/ExpressRoute-class: predictable latency/capacity, cost), colo-in-cloud-carrier models.
- Topology: hub-and-spoke (central inspection VPC with firewalls/inspection subnets) vs full mesh (routing/audit explosion); **transit gateway/VNet peering transitivity rules**: peering is *not* transitive — the classic broken-hybrid bug.
- Inspection discipline: hub firewall inspects spoke↔spoke and egress; routing must *force* traffic through it (route tables are the policy).

### 3.2 Private access & DNS design
- Private endpoints for cloud services (object stores, DBs): traffic never leaves the private path; SG/endpoint-policy as the allow-list (L12 pattern).
- PrivateLink/PAS-class for SaaS: provider-side NLB exposure with identity-bound policies.
- Hybrid DNS: split-horizon (internal zones resolvable from cloud via inbound/outbound endpoints/forwarders); **DNS is the hybrid attack surface** — forwarder misconfig = internal-name leakage; conditional-forwarder hygiene.

### 3.3 Container networking security
- Netmodel: pod = one netns, veth pairs to CNI bridge/overlay; flat pod-to-pod by default = the L09 flat-network problem reborn.
- NetworkPolicy: ingress/egress selectors (pod/namespace labels) + ports; **default-deny first** (`policyTypes` with empty rules), then allow-pairs — the same allow-list craft as SGs/L12.
- Enforcement prerequisite: CNI must support NetworkPolicy (many defaults don't enforce — the classic audit finding: policies exist, nothing enforces them).
- East-west visibility: CNI flow logs (Hubble/Cilium-class) as the cloud-native flow-log analog (L21 bridge).

### 3.4 Assurance & drift control
- Flow-log analytics: top-talkers, reject spikes, new-destination learning (baselining for L23).
- Change alarms: SG/route/peering modifications → event-driven alert (who changed the firewall — L19 continued); IaC drift detection (manual console changes = alarms + remediation policy).
- Posture baselines: CIS cloud benchmarks; network-reachability analyzers (simulate SG/route combos to find unintended paths — reachability graphs beat reading rules one-by-one).

### 3.5 Shared-responsibility matrix (capstone artifact)
- Per-service rows (IaaS VM, managed DB, container platform, SaaS): customer-side networking duties (segmentation, SG policy, egress, DNS, encryption in transit) vs provider duties (fabric, hypervisor isolation, physical).
- The audit question set: who can change routing? who holds endpoint policies? where does egress leave your trust boundary? who reads the flow logs?

## 4. Teaching Sequence (120 Minutes)

| Time | Segment | Instructor moves |
|---|---|---|
| 0–10 | Recap: Quiz-4 debrief highlights | Two cloud items re-taught as one-liners |
| 10–35 | Core: hybrid patterns + transitivity | Hub-spoke diagram; non-transitive-peering bug walkthrough on sandbox |
| 35–55 | Core: private endpoints + hybrid DNS | Endpoint-policy allow-list demo; split-horizon failure vignette |
| 55–65 | Break | — |
| 65–90 | Core: container networking | Pod-netns picture; NetworkPolicy live: default-deny → app→db allow; enforcement-prereq caution |
| 90–110 | Student activity: flow-log lab + drift alarm | Pairs: analyze sample flow logs for anomalies; create one config-change alarm (Lab-10 part 2; cs-064..065 prep) |
| 110–120 | Wrap + formative | Exit ticket; Module-6 trailer: "you've built the network — now we watch it" |

## 5. Technical Examples

```
# Transitivity bug (sandbox, read-only diagnosis):
#   SpokeA → Hub: OK (peered). SpokeB → Hub: OK. SpokeA → SpokeB: BLACKHOLE.
#   Fix pattern: hub route tables + central inspection; or TGW attachment for transitivity.

# NetworkPolicy (K8s on range; enforcement-capable CNI assumed)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: db-default-deny, namespace: prod }
spec:
  podSelector: { matchLabels: { app: db } }
  policyTypes: [Ingress, Egress]
  ingress:
  - from: [{ podSelector: { matchLabels: { app: api } } }]
    ports: [{ port: 5432, protocol: TCP }]
  egress: []                      # db talks to nothing — strictest sane posture

# Flow-log anomaly drill (sample file):
#   app-tier → 1.2.3.4:443 every 60s, ~2KB   ← beacon-candidate (L21/L23 methodology)
#   data-tier → any external: REJECT          ← scoped-egress working as designed
```
Expected teaching points: reachability is *routing + policy combined*; default-deny-then-allow is the universal pattern (L09/L12/L20); "policy exists ≠ policy enforced."

## 6. Discussion Questions

1. Peering is non-transitive. Design the hub that makes spoke↔spoke inspection *unavoidable*, and show the route-table diff that proves it.
2. Why does DNS break hybrids more often than routing? Give the split-horizon failure that leaks internal names externally.
3. "We have 40 NetworkPolicies" — what's the first enforcement question you ask, and how do you verify it?
4. Which flow-log pattern from today's sample would you alert on first, and what's the false-positive risk?
5. For a managed Kubernetes service: write the responsibility matrix rows for networking (who owns CNI policy, who owns node SGs, who owns pod egress?).

## 7. Student Activity

**Flow-log lab + drift alarm (20 min, pairs):** analyze the staged flow-log dataset: identify one beacon-candidate, one policy-verification line, one new-destination outlier; then create an SG/route-change alarm and trigger a benign change to see it fire. Deliverable: annotated log excerpt + alarm screenshot-equivalent (event id + fields).

## 8. Problem-Solving Case

**Primary case — cs-064 "Cloud egress policy authoring" (intermediate-advanced):**
Security mandates data-tier isolation after an audit; dev teams push back ("our ETL needs the internet"). Provided: current route/SG dump and a flow-log month. Students must (a) classify destinations from flow logs (approved mirrors vs unknown), (b) author the egress policy set: data-tier private-endpoint-only, app-tier NAT + domain allow-list via egress firewall/proxy pattern, (c) design the exception workflow (time-boxed, logged), and (d) define success metrics (reject-rate trend, exception count) and the detection that catches policy bypass (direct-to-IP attempts).
**Linked cases:** cs-065 (flow-log investigation of anomalous cloud traffic).
*(Model solutions: instructor answer-key set, Module 5.)*

## 9. Formative Assessment

1. True/false: VPC peering is transitive. What construct provides transitive hub routing?
2. What two things must exist before a NetworkPolicy actually filters traffic?
3. Name the three parts of a default-deny NetworkPolicy for a DB pod.
4. Which alarm answers "who changed the route table?"
5. Give one customer-side networking duty that shared-responsibility never transfers to the provider.
*(Answer key: instructor set, Module 5.)*

## 10. Summary & Key Takeaways

- Hybrid works when routing *forces* inspection: hub-spoke + transit constructs; peering won't transit.
- Private endpoints + hybrid-DNS discipline shrink the internet surface; DNS remains the soft spot.
- Container networking is L09 flat-network redux: default-deny NetworkPolicy with a *verifying* CNI.
- Assurance = flow logs + change alarms + reachability analysis — design becomes evidence.

## 11. References

- AWS Transit Gateway & PrivateLink guides; Azure hub-spoke and Private Link documentation (current).
- Kubernetes docs — NetworkPolicy API + CNI enforcement notes; Cilium/Hubble flow-visibility docs.
- CIS Benchmarks — cloud provider & Kubernetes sections.
- CNCF — cloud native network security whitepapers (east-west patterns).

## 12. CLO Mapping

| CLO | Where in this lecture | Assessed via |
|---|---|---|
| CLO-13 | §3.1–3.5 hybrid/container/assurance skills; flow-log lab | Quiz 4 (today, partial), Quiz 5 (W14), Assignment 7 (W14), Lab-10 |
