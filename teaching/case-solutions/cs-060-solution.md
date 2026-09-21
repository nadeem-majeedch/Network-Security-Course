---
case: cs-060
solution-for: modules/module-05-wireless-cloud/case-studies/cs-060-wpa3-transition-compatibility-triage.md
difficulty: advanced
module: 5
lecture-anchor: L18
clos: [CLO-8]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-060 Solution — WPA3 Transition Triage (INSTRUCTOR ONLY)

## Model Solution

**Mechanical explanations:**

- *What transition mode changes on the air:* the SSID advertises both
  WPA2- and WPA3-capable security; WPA3-capable clients negotiate the
  modern path (which in Enterprise mode centers on **PMF — 802.11w
  management-frame protection — being required**, plus newer cipher
  negotiation; SAE's hash-to-curve dragonfly handshake is the *personal*
  WPA3 story, not the Enterprise one — the answer must keep these
  straight). Legacy clients associate exactly as before (WPA2), so the
  *mode itself* doesn't break them — **the seams do**: PMF becomes
  required for the WPA3 path, and management frames that were previously
  unprotected (and tolerable) now get protection-retransmission
  semantics some old drivers mishandle.
- *Cohort B (2017–19 tablets, drops every ~10 min):* a **2019 driver
  mishandling PMF-protected management frames** — likely unhandled
  retransmission/robust-management-frame timers; the association
  succeeds (it's WPA2-path or partial-PMF), then the periodic
  management exchange (beacon-interval checks, RRM/BSS-transition
  frames now PMF-protected) trips the bug → driver drops and
  re-associates ("no internet" windows). The ~10-min cadence smells
  like a controller's periodic unicast management action.
- *Cohort C (2015 dongles, hard fail):* the driver **refuses PMF at
  association** — it never completes any path that requires 802.11w;
  in transition mode the controller offers a WPA2-without-PMF path,
  but these drivers also choke on the *advertised* capability
  information elements (some 2015-era chipsets fail parsing/behaving
  with the newer RSNE/PMF advertising) → association never starts.
  Hard hardware-generation limit, not a settings bug.

**Per-cohort decisions:**

| Cohort | Decision | Action | Security cost |
|---|---|---|---|
| A (~1,800) | none — this is the fleet | keep on WPA3 path; baseline telemetry | — |
| B (~120 tablets) | **accommodate + vendor chase** | file/vendor driver update (2019→current); interim: separate `LEGACY-EAP` SSID (WPA2-Enterprise, EAP-TLS *same* RADIUS, PMF optional, **separate VLAN with restricted egress**) | legacy SSID lacks PMF → disruption-class attacks possible on *that* SSID; bounded by VLAN + cohort size; sunset date attached |
| C (40 dongles) | **replace** (vote) | 2015 chipsets can't do PMF at all — no driver will fix parsing-level failure; replace with ~802.11ac/ax USB or built-in | zero — decommissioning *removes* the WPA2-only surface; the business case writes itself (40 dongles) |

**WPA3-only endgame:**

- **Retirement criteria for transition mode:** (1) cohort-B SSID
  population <1% of associations (or driver-update fleet-complete);
  (2) cohort-C replaced; (3) 30 days of controller telemetry with zero
  WPA2-path negotiations on the main SSID; then **flip to WPA3-only
  (PMF required, no WPA2 IEs advertised)**.
- **The honest residual-risk statement:** *while transition mode runs, it
  is not WPA3's security* — the mode deliberately permits legacy
  association, so an on-path adversary can influence legacy-capable
  clients to use the WPA2 path (downgrade exposure: the classic
  management-frame attacks against the WPA2-path sessions; PMF-off
  cohorts are the target-rich ones). Transition mode is a *compatibility
  bridge*, not a security upgrade for mixed fleets; the security
  upgrade arrives at the flip. Say this in the design doc and the
  risk register — the bridge has a toll, and the date matters.
- **Campus policy that gets there:** device-standard policy (new
  purchases: WPA3-capable certification required) + the legacy-SSID
  sunset governance (each semester review; population metric
  published) — the endgame is a *procurement + telemetry* engine, not
  a config flip someday.

## Alternative Solutions

- **Flip straight to WPA3-only now:** cleanest security; strands B+C
  (160 devices) — acceptable only with replacement funding pre-cleared;
  the triage exists to scope what "stranded" actually costs.
- **Stay WPA2-Enterprise, skip WPA3:** WPA2-Enterprise + EAP-TLS + PMF
  *enabled* is already a strong posture — an honest alternative worth
  naming; the case's campus wants the WPA3 endgame, but the security
  delta for an EAP-TLS fleet is smaller than headlines suggest (PMF
  and cipher-hardening, not an identity-model change).
- **Per-cohort SSIDs forever:** SSID sprawl as architecture — the
  legacy SSID is a *bridge with a sunset*, not a permanent tier.

## Tradeoffs

- Driver-update chase vs replacement cost: vendor chase is free but
  slow (B's vendor is 2019-era; expect silence) — set a 90-day decision
  gate.
- Legacy SSID segmentation depth: restricted-VLAN beats shared-VLAN;
  don't over-invest in a bridge with a sunset date.
- Telemetry investment (association-path counting) vs blind flip: the
  counter is the retirement *evidence* — build it, it's cheap.

## Common Mistakes

- Confusing SAE (personal WPA3) with Enterprise transition mechanics —
  the answer that says "dragonfly broke the tablets" fails the case.
- Treating transition mode as WPA3 security (the residual-risk honesty
  is the graded point).
- Replacing cohort-C *before* exhausting the accommodation analysis
  (the dongles fail at parsing level — document *why* replacement is
  forced).
- No sunset governance (legacy SSID becomes permanent folklore).

## Instructor Prompts

- "Which frames, exactly, did cohort B's driver mishandle — and why every
  ~10 minutes?"
- "What does the downgrade attack against transition mode look like, and
  who is exposed?"
- "Where does PMF-enabled WPA2-Enterprise sit relative to WPA3 for an
  EAP-TLS fleet?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Seams-not-mode failure logic; residual-risk honesty |
| Technical accuracy | 25% | PMF/transition/SAE-vs-Enterprise precision |
| Alternatives considered | 20% | Flip-now/stay-WPA2 trades |
| Communication | 15% | Cohort table + endgame criteria |

**Timing:** reveal at 5:00 + 10; the SAE-vs-Enterprise clarification is
the accuracy bar.

## CLO Mapping

- **CLO-8** — WPA3 migration mechanics and fleet triage.
