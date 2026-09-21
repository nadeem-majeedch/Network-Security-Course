---
module: 3
lectures: [L09, L10, L11, L12]
status: complete
artifact-type: answer-key
instructor-only: true
distribution: never-publish-to-students
---

# Answer Key — Module 3: Secure Architecture & Perimeter Controls

> **INSTRUCTOR ONLY — contains model answers to graded formative assessments.**
> Links: Plans `modules/module-03-secure-architecture/lectures/` · Student pages `docs/lectures/lecture-09…12` · Notes `teaching/speaker-notes/lecture-09…12-speaker-notes.md`

## L09 — Defense in Depth & Segmentation

### Formative checks (plan §11)
1. Enclave argument: domain-level segmentation breaks lateral movement between trust levels (corp ↔ servers ↔ OT); VLANs alone don't authenticate traffic between zones — the *policy enforcement point* is what matters.
2. Deficit mapping: identity (federation), network (segmentation), device (compliance gate), app (WAF/authz) — any four planes with one named control each.
3. Microsegmentation vs VLANs: policy per-workload, enforced distributed, identity-aware vs coarse L2 broadcast domain; microsegmentation answers east-west, VLANs mostly organize north-south.
4. Design failure: flat admin network reachable from user VLAN — lateral movement to management plane; the fix is a jump path + segmentation, not "a better firewall".
5. Trust zones: internet < DMZ < corporate < servers < management — direction of trust and inspection point named at each boundary.

### Exit ticket
- Zero-trust principles: verify explicitly, least-privilege, assume breach — the *counter* to flat-network trust-by-location. Answer must reference authentication per-request, not "never trust anyone" hand-waving.
- Lateral movement broken by: segmentation + east-west monitoring — not by more perimeter firewalls.

### Discussion facilitation
- Q3 (zero-trust budget): strongest answers sequence quick wins (MFA, inventory, microsegment pilot) before re-architecture; "boil the ocean" answers lose marks.

## L10 — Firewalls: Concepts & Placement

### Formative checks
1. Packet filter vs stateful: per-packet, connectionless decisions vs connection-state table (only packets belonging to established flows); stateful's win is return-traffic handling without broad accepts.
2. NGFW additions: application awareness, TLS inspection, IPS integration, identity binding — the *application layer* is the differentiator, not "more speed".
3. DMZ design: internet → DMZ (public services) → internal; published services in DMZ, separate rulebases per zone, no direct internet-to-internal accepts.
4. Egress: outbound restrictions + DNS pinning/proxying reduce C2 flexibility and accidental exfiltration — "egress is optional" is the misconception to catch.
5. HA: stateful failover (session table sync), so failover doesn't reset connections; without sync, established flows drop.

### Exit ticket
- Firewall ≠ security program: it's one enforcement point; missing patches, identity gaps, and insider paths bypass it — the answer must name at least two bypass classes.
- First rule of rulebase review: find the broadest allows (any/any) — they're where risk hides.

### Lab troubleshooting (firewall lab context)
- "Service unreachable" after policy change: check rule order first (first-match wins), then NAT binding, then the *other* direction's return rule.
- Asymmetric routing kills stateful inspection: traffic returns via a different firewall — symptom is RSTs; fix routing or use state sync.

## L11 — ACLs & Rulebase Engineering

### Formative checks
1. Order matters: first-match wins; the general deny at the top shadows specific allows below it — order by specificity, document intent.
2. Permit/deny consequence: deny without log = silent blackhole; the debugging question is always "which rule matched?" (hit counters).
3. Stateful vs ACL: an ACL is stateless — return traffic needs explicit entries (e.g., `established` keyword approximations); confusing the two is a classic error.
4. Rulebase decay: orphaned rules, overlapping permits, any/any residue; fixes: regular review, hit-count reporting, just-in-time rules with expiry.
5. Change control: intent recorded, test path defined, rollback ready — one-line change windows without rollback = fail.

### Exit ticket
- Logging both: denied attempts (detection) and permit hit-counts (hygiene) — the hygiene side is what most students forget.
- Shadowed rule: `permit tcp any any` placed before `permit tcp 10.0.0.0/8 eq 443` — the specific rule never matches.

### Lab troubleshooting (ACL lab context)
- ACL applied wrong direction (`in` vs `out` is interface-relative) — the top troubleshooting cause; require students to state direction aloud before testing.
- Implicit deny surprise: forget the explicit `permit` for return traffic when working statelessly.

## L12 — NAT, Proxies, Egress & NAC

### Formative checks
1. NAT types: static (1:1), dynamic (pool), PAT/NAPT (many:1 port-based) — PAT is what most "NAT" actually is; overloading = PAT.
2. NAT is not security: it breaks end-to-end reachability (incidental), provides no authentication/integrity, and is bypassed by outbound-initiated connections — the answer must say *why*, not just "no".
3. Forward vs reverse proxy: client-side (egress policy, caching, TLS inspection) vs server-side (publishing, load balancing, WAF); direction of the *client* is the discriminator.
4. 802.1X: supplicant ↔ authenticator ↔ authentication server (RADIUS); EAP methods carry the auth; dynamic VLAN/ACL assignment is the payoff.
5. MAB: MAC address as identity — spoofable, last-resort for non-802.1X devices (printers/IoT); MAB devices belong in the most-restricted profile.

### Exit ticket
- Egress matters because attackers operate *outbound-initiated* (C2 beacons, exfil) — perimeter-centric "inbound only" thinking misses it.
- 802.1X failure mode: unmanaged device without supplicant → MAB/restricted VLAN/quarantine; "network death" only if no fallback designed — the fallback design is the senior answer.

### Case study anchors (cs-027–cs-036) — grading pointers
- **cs-027–cs-030 (L09/L10):** architecture answers must show zones + enforcement points drawn or described; perimeter-only answers cap at pass.
- **cs-031–cs-033 (L11):** rulebase answers need order/direction/shadowing analysis, not just "add a rule".
- **cs-034–cs-036 (L12):** NAT-as-security claims must be explicitly dismantled for full credit.

## Common misconceptions (module-level)
1. "The firewall is the security boundary" — identity, endpoints, and east-west paths are boundaries too (L09).
2. "Any/any is fine, it's internal" — internal trust is exactly what zero-trust and segmentation dismantle (L09/L11).
3. "Proxies break everything" — designed correctly, they enable policy and inspection; the failure mode is unplanned deployment, not the concept (L12).
4. "802.1X is just WiFi" — wired port authentication is where most enterprise deployments live (L12).
