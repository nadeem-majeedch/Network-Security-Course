---
case: cs-052
solution-for: modules/module-04-crypto-protocols/case-studies/cs-052-wireguard-rollout-design-for-remote-staff.md
difficulty: advanced
module: 4
lecture-anchor: L16
clos: [CLO-7]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-052 Solution — WireGuard Rollout (INSTRUCTOR ONLY)

## Model Solution

**Architecture:**

- **Control plane:** a coordination/management layer (self-hosted
  wg-easy/Netmaker/Tailscale-style headscale, or config-managed static
  peers) owns peer registry, key distribution, and ACLs; **MFA lands at
  (a) enrollment** — a device enrolls through an SSO+MFA portal which
  *then* provisions its key/config, and **(b) gateway front-door**: for
  sensitive services, the gateway routes to an **auth-proxy (SSO/MFA)**
  in front of admin panels — WireGuard authenticates the *device*;
  the proxy authenticates the *human* per session. This two-layer
  pattern is the standard answer to "WireGuard has no MFA": it's not
  supposed to — identity belongs to the layers above.
- **Gateway topology: hub-and-spoke** (staff↔gateway only). Reasons:
  staff-to-staff traffic is *zero* (nobody SSHes to a colleague's
  laptop — and if a workflow suggests it, redesign the workflow);
  hub gives one logging point, one ACL policy surface, simple
  revocation; mesh would multiply endpoint complexity for 2 ops people
  with no benefit. (Mesh-with-ACLs is the variant if device-to-device
  support is a real requirement later.)
- **Per-peer ACLs on the gateway:** each staff key may reach *only* the
  services their role needs (Git/CI for engineers; admin panels for
  ops) — no lateral trust between staff endpoints; the hub's policy
  *is* the zero-trust segmentation.

**Key lifecycle:**

| Stage | Design |
|---|---|
| Generation | per-device keypair, generated **on-device** at enrollment (private key never transits the server); public key + device metadata registered via the SSO+MFA portal |
| Rotation | **automatic, ≤90 days** (control-plane initiated rekey, seamless); a key that can't re-auth drops and re-enrolls via MFA |
| Revocation — departure | SSO deprovisioning triggers control-plane peer deletion; key dead within ≤60 s (heartbeat check) |
| Revocation — lost laptop | same path from the MDM/SSO "lost device" action + key deletion; because the private key never left the device, deletion = access death |
| Audit logging | WireGuard is silent by design → log at the **gateway** (conntrack/flow records: peer key-ID ↔ source IP:port, bytes, timestamps) and at the **auth-proxy** (human, SSO session, service accessed); gateway logs to SIEM, 1-year retention — compliance gets *who/where/when/what* without touching WireGuard's data plane |

**Two security properties given up vs the legacy SSL-VPN + compensations:**

| Given up | Why it mattered | Compensation |
|---|---|---|
| **Per-session application-layer auth at the VPN front door** (SSL-VPN re-authed/steered per app) | some compliance regimes like human-per-session gatekeeping at the *network* edge | auth-proxy layer provides human-per-session for sensitive apps (the compliant subset); gateway logs the rest |
| **Centralized content/agent inspection on the tunnel** (legacy SSL-VPN often pairs with endpoint-scan/agent posture at connect) | posture gating at connect time | MDM+EDR posture feeds the *enrollment/rekey* decision (control-plane policy: no healthy posture → no rekey), so posture gates persist — at rekey cadence rather than session granularity |

(The trade to name honestly: WireGuard's *crypto* is strictly better
(Noise/ChaCha20, modern handshake); what's traded is *session-layer
ceremony* — moved up-stack on purpose.)

## Alternative Solutions

- **Managed overlay (Tailscale/Teleport-class):** buys the control plane
  (SSO, ACLs, logging) as a product — the pragmatic choice for a 2-person
  ops team; the architecture above is what such products implement, and
  self-host (headscale) keeps data custody. Name the tradeoff: vendor
  dependency vs ops cost.
- **Keep SSL-VPN, tune performance:** solves complaints cheaply; keeps the
  legacy crypto/agent stack — defensible short-term, wrong direction.
- **Mesh for all:** over-permissive lateral surface + ops complexity —
  rejected with the hub rationale.

## Tradeoffs

- Hub single point: gateway redundancy (2 hubs, anycast or DNS-failover) —
  the simplicity buy needs HA spend.
- MFA-at-enrollment only vs per-session MFA: per-session for *sensitive*
  apps via proxy; blanket per-session MFA would rebuild the SSL-VPN UX the
  staff are fleeing.
- Self-hosted control plane vs managed: custody/audit vs 2-person ops
  reality — headscale-style self-host with managed-style ergonomics is the
  sweet spot.

## Common Mistakes

- Bolting MFA onto WireGuard as if it had a portal (category error — MFA
  goes at enrollment and the proxy layer).
- Shared config/keys "for simplicity" — destroys revocation and audit.
- No logging design ("WireGuard doesn't log" is not the compliance answer).
- Mesh topology by default — lateral trust nobody needs.

## Instructor Prompts

- "Walk a departed employee's key from 'offboarding ticket' to 'dead.'"
- "Where exactly does the human authenticate in your design — twice? At
  what layers?"
- "Which compliance artifact proves 'who connected from where when'?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Control-plane/data-plane separation; MFA placement |
| Technical accuracy | 25% | Key lifecycle, logging-at-gateway mechanics |
| Alternatives considered | 20% | Managed-overlay tradeoff named |
| Communication | 15% | Architecture readable by ops + compliance |

**Timing:** reveal at 5:00 + 2; "data plane vs control plane" is the
frame to install.

## CLO Mapping

- **CLO-7** — Modern VPN architecture with control-plane design.
