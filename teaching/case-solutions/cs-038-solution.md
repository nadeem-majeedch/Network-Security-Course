---
case: cs-038
solution-for: modules/module-03-secure-architecture/case-studies/cs-038-explicit-proxy-university-lab.md
difficulty: intermediate
module: 3
lecture-anchor: L12
clos: [CLO-4]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-038 Solution — Explicit-Proxy Egress (INSTRUCTOR ONLY)

## Model Solution

**Egress routing table:**

| Zone | Egress path | Filtering profile | Logging |
|---|---|---|---|
| Teaching labs (90 PCs) | **Explicit proxy (PAC + GPO-pinned)** — managed fleet enforces config | CIPA-profile: category block (adult/malware/anon), TLS-inspect non-exempt | Full URL + user (PC identity), 90-day |
| Research cluster | **Direct (firewall-allowlisted egress)** + explicit proxy *for web* where convenient | No content filter; **reputation + malware categories only**; SSH-out to named collaborator CIDRs allowed at FW | Flow-level + malware events only — researchers get privacy-preserving logging (role-scoped access) |
| Open Wi-Fi | **Transparent** to proxy (no PAC possible on mixed devices) | Malware/crypto-lock + legal-duty categories only (no productivity filtering); **TLS-inspect OFF by default, category-exempt SNI allow** | SNI-level logs, minimal retention |
| DMZ/servers | Direct with IP allowlists (per cs-035 pattern) | — | Flow logs |

**Why research ≠ teaching-lab policy:** compliance duty attaches to minors
in *teaching* contexts; research clusters serve adults with workflows
(package managers over pinned TLS, arbitrary endpoints) that content
filters break — so research gets *security* filtering (malware/reputation)
without *content* filtering, and SSH-to-collaborators never touches the
proxy at all. The dean's duty and the researchers' workflows are both
satisfied because the routing table, not a single policy, carries the
distinction.

**Non-proxy-aware & pinned clients:**

- Open Wi-Fi → transparent interception (no client config needed).
- **Pinned apps (mobile banking, health, some messaging) break under TLS
  interception** — honest limit: certificate-pinned clients will hard-fail;
  classify by category (finance/health) into **SNI-based allow without
  inspection** (firewall sees SNI, permits, doesn't decrypt). Exemption
  mechanism: category-driven, logged, reviewed quarterly — not user-requested
  one-offs (which would erode the profile).
- Truly pinned + not-SNI-differentiated apps (rare) are the acknowledged
  residue: name them (a banking app class) and accept "fails visibly, user
  switches network" as correct behavior on an open student network.

**Anti-bypass design (the 3 firewall rules):**

| # | Rule | Effect |
|---|---|---|
| 1 | Lab VLAN → proxy IP :3128/8080 **only** (all other egress deny) | proxy is the only door |
| 2 | Any user VLAN → external **DNS** (53/853) deny; internal resolvers only | kills DNS-tunnel evasion + hardcoded resolvers |
| 3 | Lab VLAN → other-egress-IPs any-port **deny (log)** | catches VPN-over-443 to non-listed hosts; log feeds evasion review |

**Two evasion behaviors monitored:** (1) spikes of *denied* egress from lab
PCs (rule 3 log) — new VPN endpoints appear here first; (2) proxy auth/
identity anomalies — one PC identity with many concurrent sessions, or
PAC-disabled attempts (user-agent/requests without proxy headers at the
proxy). Both are *process* alarms to the lab manager, not auto-blocks —
evaders get redirected to the request portal (cs-032's lesson).

## Alternative Solutions

- **Single transparent proxy for everything:** simplest ops; fails research
  (package managers) and pinned-app UX; the routing table is the point.
- **DNS-layer filtering only (no proxy):** cheap, survives TLS, but
  category control via DNS is coarse and bypassable by IP/DoH; pair it as
  the *first* layer for Wi-Fi, not the whole design.
- **Agent-based filtering on lab PCs only:** strong per-device control;
  adds fleet management burden and does nothing for Wi-Fi — partial.

## Tradeoffs

- TLS inspection scope vs privacy: labs = yes (managed, minors, logged);
  Wi-Fi = no by default (adults, personal devices) — proportionality is the
  design.
- Exemption list growth: every exemption is audit-visible; quarterly review
  with auto-expiry keeps it a list, not a swamp.
- Research privacy vs logging: role-scoped access to research flow logs is
  the compromise that keeps the logging honest without surveillance.

## Common Mistakes

- One profile for all zones (breaks research or fails compliance).
- Forgetting the DNS rule — the classic bypass.
- TLS-inspecting pinned apps and blaming users for "broken banking."
- Anti-bypass via proxy config alone (firewall must own the enforcement).

## Instructor Prompts

- "Which single rule, if mis-ordered, silently exempts the labs?"
- "Why is 'transparent for Wi-Fi' acceptable when 'transparent for labs'
  isn't the best choice?"
- "Where does DoH fit — blocked, allowed, or routed through internal resolvers?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Zone-differentiated routing; pinned-app honesty |
| Technical accuracy | 25% | Explicit/transparent/PAC mechanics; rule ordering |
| Alternatives considered | 20% | DNS-layer/agent options weighed |
| Communication | 15% | Routing table + 3-rule anti-bypass |

**Timing:** reveal at 5:00 + 2; the "which rule mis-ordered exempts labs"
prompt rewards rule-ordering intuition from cs-031.

## CLO Mapping

- **CLO-4** — Proxy-based egress architecture with honest limits.
