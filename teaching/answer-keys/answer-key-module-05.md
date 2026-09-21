---
module: 5
lectures: [L17, L18, L19, L20]
status: complete
artifact-type: answer-key
instructor-only: true
distribution: never-publish-to-students
---

# Answer Key — Module 5: Wireless & Cloud Network Security

> **INSTRUCTOR ONLY — contains model answers to graded formative assessments.**
> Links: Plans `modules/module-05-wireless-cloud/lectures/` · Student pages `docs/lectures/lecture-17…20` · Notes `teaching/speaker-notes/lecture-17…20-speaker-notes.md`

## L17 — Wireless Fundamentals & Threats

### Formative checks (plan §11)
1. Open vs WEP vs WPA2 vs WPA3: open = no protection; WEP = broken (RC4, 24-bit IV, cracking in minutes); WPA2-PSK = solid when strong passphrase, vulnerable to offline attack on weak passphrases; WPA3-SAE = dragonfly handshake, forward secrecy, anti-offline — "WEP was bad because the math was weak *and* the design worse".
2. PSK vs enterprise: shared passphrase (one secret, weak revocation) vs 802.1X per-user credentials (revocation, audit, dynamic VLANs) — enterprise is the corporate answer; PSK acceptable only for IoT with separation.
3. Rogue vs evil twin: rogue = unauthorized AP on your network; evil twin = attacker's AP impersonating yours (same SSID) to harvest clients — mitigation differences: rogue = containment/hunt on *your* airspace; evil twin = client-side validation + 802.1X (clients refuse open look-alikes).
4. Deauth: management-frame spoofing forces client disassociation (management frames historically unauthenticated); mitigations: 802.11w PMF (protected management frames), RF monitoring. Classroom demos are lab-only, authorized.
5. Site survey/coverage: over-coverage extends attacker reach; under-coverage drives users to phone hotspots — coverage tuning is a security control.

### Exit ticket
- WPA2 is not broken by the 4-way handshake capture itself — the PSK-derivation allows *offline guessing of weak passphrases*; strong passphrases remain safe. Precision here earns distinction.
- First two wireless-hardening steps: 802.1X with PMF enabled, and rogue-AP monitoring — not "hide the SSID" (SSID hiding is security theater; accept its rejection as insight).

### Lab troubleshooting (wireless lab context)
- Client won't join WPA3 SSID: driver lacks SAE — lab image pinned; check adapter support list before blaming config.
- Monitor-mode capture shows nothing: wrong channel — hop or lock; country-code differences matter on lab dongles.

## L18 — Enterprise Wireless & Rogue Defense

### Formative checks
1. WIPS lifecycle: detect → classify (known/unknown/external) → locate → contain (authorized only); the *classification* step is what prevents containing your neighbor's AP (legal risk).
2. 802.1X deployment failure modes: cert validation disabled on supplicants (MITM returns), MAB fallback too broad, dynamic VLAN misassignment — validation of server certs is the top real-world gap.
3. Guest network: separate SSID/VLAN, client isolation, bandwidth caps, captive portal with ToS, no corporate reachability — "guest on the same VLAN, firewalled later" fails the design review.
4. BYOD posture: onboarding (cert provisioning), device compliance checks, network segmentation of unmanaged devices — full MDM is not the only acceptable answer; segmentation + minimum posture is.
5. Location as security input: RF containment zones (no corporate SSID in lobby/docking areas), but *never* as sole control — RF leaks; layered with 802.1X.

### Exit ticket
- Containment legality: actively deauthing an AP you don't own is unlawful interference in most jurisdictions — authorization boundary applies to RF too; the answer must state it.
- Rogue found on corporate VLAN: containment is last resort if it hosts live services — first locate, then trace the port (switch MAC table), then unplug at the switch — physical trace beats RF jamming in accuracy.

### Discussion facilitation
- Q3 (executive wants PSK removed): sequence the migration — pilot 802.1X, cert onboarding, sunset PSK per device class; "flip the switch Monday" answers lose marks.

## L19 — Cloud Networking I: VPC Design & Controls

### Formative checks
1. VPC/subnet design: IP plan per environment (prod/non-prod separation), public/private subnets via IGW vs NAT gateway, route tables per subnet — the route table *is* the segmentation enforcement point at L3.
2. SG vs NACL: SG = stateful, instance-level, allow-only, evaluates all rules; NACL = stateless, subnet-level, numbered ordered rules, allow+deny. Both: return traffic auto-allowed by SG, NACL needs explicit ephemeral-port rules.
3. Hub-spoke vs peering: central inspection (firewall/NVA in hub) and shared services vs peering's lower latency/direct paths — hub-spoke wins when consistent inspection matters.
4. Egress control: dedicated egress subnets/NAT with allow-lists, VPC flow logs *always on* — "default allow out" is the design smell.
5. Shared-responsibility: provider secures *of* the cloud (fabric, hypervisor), customer secures *in* the cloud (SGs, NACLs, routes, IAM) — the security-group misconfig case is squarely customer-side.

### Exit ticket
- SG != security group of the box alone: it's stateful microsegmentation — but default "allow all egress" undermines it; tighten egress too.
- NACL ephemeral ports: stateless means return traffic for outbound connections needs inbound ephemeral-range allowance — the classic broken-connection diagnosis.

### Lab troubleshooting (cloud lab context)
- Instance unreachable after SG edit: inbound rule AND source SG reference check; then NACL order/ephemeral return path.
- Route table shows 0.0.0.0/0 to NAT but no internet: NAT gateway in a subnet without IGW route, or no elastic IP attached — check both.

## L20 — Cloud & Hybrid Assurance

### Formative checks
1. CNI/network policy: default-deny both directions then allow per app path; policy is *additive* across plugins — the "I added a policy, why does traffic still flow?" answer is usually another namespace's allow-all.
2. Container egress: same allow-list discipline as VPC; DNS is the escape hatch to watch — egress without DNS policy is half an egress.
3. Hybrid landing zone: ExpressRoute/Direct Connect with private peering, IP plan that doesn't collide, DNS resolution strategy (conditional forwarders), consistent inspection at the boundary.
4. Flow telemetry in cloud: VPC flow logs / NSG flow logs feed the same analysis stack as L21 — retention and cost are the operational constraints; sample at capture or aggregate in the pipeline.
5. Assurance artifacts: config baselines (IaC drift), policy-as-code checks in CI, periodic review calendar — "we set it up right once" is not assurance.

### Exit ticket
- Container network policy isn't a firewall replacement: it's one layer; host firewalls, node segmentation, and image/registry controls still apply — layered answer required.
- Hybrid trust boundary: the interconnect is a trust boundary like any other — inspect it, log it, and scope its routes; "private link = trusted" is the misconception.

### Case study anchors (cs-051–cs-062) — grading pointers
- **cs-051–cs-055 (L17/L18):** wireless answers must name the *specific* protocol mechanism (SAE, PMF, 802.1X) — generic "use WPA2/3" caps at pass.
- **cs-056–cs-059 (L19):** SG/NACL differences must be applied to the scenario, not recited; egress discipline expected.
- **cs-060–cs-062 (L20):** hybrid answers need boundary inspection + DNS + routing coherence; single-dimension answers lose marks.

## Common misconceptions (module-level)
1. "Cloud is secure by default" — the default VPC/SG posture is convenience-oriented, not threat-oriented (L19).
2. "WPA3 makes wireless uncrackable" — handshake protections improve; implementation bugs and downgrades remain (L17).
3. "Network policies = Kubernetes firewall" — no L7 inspection, additive semantics, plugin-dependent enforcement (L20).
4. "Private connection means no inspection needed" — trust boundaries need visibility regardless of transport (L20).
