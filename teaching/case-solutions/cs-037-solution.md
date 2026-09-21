---
case: cs-037
solution-for: modules/module-03-secure-architecture/case-studies/cs-037-nat-mode-address-plan.md
difficulty: intermediate
module: 3
lecture-anchor: L12
clos: [CLO-3]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-037 Solution — NAT Mode & Address Plan (INSTRUCTOR ONLY)

## Model Solution

**Address plan:**

- **Subsidiary renumbers its flat `10.0.0.0/16`** → split into real subnets
  under a non-colliding block, e.g., `10.40.0.0/16` carved as
  `10.40.10.0/24` (desktops), `10.40.20.0/24` (servers/app), `10.40.30.0/24`
  (printers). Rationale: the subsidiary is smaller, flatter, post-acquisition
  change-tolerant; the parent's `/16`s are load-bearing (hundreds of static
  bindings, AD sites, already-documented). Renumbering the subsidiary is
  the cheaper, safer side — *except* the printer fleet, which cannot
  reconfigure: **renumber around them** is impossible on one wire, so the
  printers keep `10.0.x` via a **NAT exception**: their VLAN keeps the old
  addressing with a boundary PAT/static 1:1 mapping, scheduled for
  retirement next year (or vendor firmware allowing gateway changes —
  whichever lands first).
- **Dual-stack runway:** new subsidiary ranges chosen outside the parent's
  planned IPv6 ULA/GUA mappings; document the IPv6 plan now (no NAT66
  surprises later).

**NAT modes per boundary:**

| Flow | Mode | Why |
|---|---|---|
| Parent DC → subsidiary app server | **Static 1:1 (or published VIP)** | app must be reached *by IP* from parent; 1:1 gives a stable address, no PAT port ambiguity; pair with firewall policy (the real control) |
| Subsidiary desktops → parent services | **NAPT (dynamic PAT)** at the boundary | many-to-few; identity-less outbound pattern is fine; PAT table = incidental flow visibility |
| Printers' legacy VLAN → parent | **Static NAT per printer** (small NAPT pool acceptable) | few devices, stable destinations; keeps hardcoded gateway semantics inside their VLAN |
| Everything else (vendor cloud, internet) | **none beyond existing edge** | don't double-NAT; keep one translation point per path |

**Security commentary — NAT ≠ firewall:**

1. **Static 1:1 "hides" the app server:** a 1:1 map forwards *any* port the
   rule allows — if the admin writes "1:1 to app server" without port
   scoping, the subsidiary-side compromise reaches every service on that
   host. The real control: **firewall policy scoping parent→app to the app
   port only**, with the 1:1 map existing purely for addressing.
2. **PAT as "isolation":** subsidiary desktops behind PAT *appear* isolated
   from HR, but PAT is translation, not policy — any route+rule change (or
   the app server as a pivot) restores reachability. The real control:
   **explicit inter-zone deny rules** (subsidiary-desktops → parent-HR:
   deny+log), with PAT kept for address conservation only. Also name:
   PAT breaks end-to-end traceability (logs show the boundary's IP) — flow
   logging at the boundary must preserve *pre-NAT* tuples for forensics.

## Alternative Solutions

- **Renumber the parent instead:** rejected — larger blast radius, more
  static config, zero benefit.
- **No renumber; double-NAT everything:** fastest merge, worst operating
  state (traceability, IPsec overlap pain, IPv6 complications); acceptable
  only as a 90-day bridge with an exit date.
- **Tunnel-and-NAT (overlay/SD-WAN) with route separation:** genuinely good
  for the interim — the overlay carries the mapping; still needs the same
  firewall policy, and the renumbering plan still stands underneath.

## Tradeoffs

- Renumber-now vs NAT-bridge: renumbering costs project time but removes a
  permanent translation layer; bridging ships the merge but creates a
  legacy TTL — set the retirement date *in the design doc*.
- 1:1-per-service vs 1:1-per-host: per-service (VIP + port) is tighter;
  per-host is simpler — with a firewall scoping ports, per-host is
  defensible and cheaper to run.

## Common Mistakes

- Using NAT *as* the isolation control (the case's trap).
- Renumbering the parent because "it's the standard."
- Forgetting pre-NAT logging at the boundary (post-NAT-only logs make
  forensics guess).
- No printer-vlan exit strategy (the exception becomes permanent folklore).

## Instructor Prompts

- "Which flow's security would break silently if the 1:1 rule were widened
  to 'any port'?"
- "Why does PAT hurt *forensics* specifically?"
- "Where does IPv6 make this whole NAT conversation easier — and what
  replaces NAT's accidental restrictions?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Side-selection logic; printer-vlan exception with exit |
| Technical accuracy | 25% | 1:1 vs NAPT semantics; pre-NAT logging |
| Alternatives considered | 20% | Bridge/overlay options with exit dates |
| Communication | 15% | Plan table + security commentary precision |

**Timing:** reveal at 5:00 + 2; the "NAT is not a firewall" commentary is
the graded spine.

## CLO Mapping

- **CLO-3** — Address-plan and NAT architecture with security honesty.
