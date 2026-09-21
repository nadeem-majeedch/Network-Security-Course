---
case: cs-048
solution-for: modules/module-04-crypto-protocols/case-studies/cs-048-mtls-deployment-for-service-to-service-traffic.md
difficulty: advanced
module: 4
lecture-anchor: L14
clos: [CLO-6]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-048 Solution — mTLS Rollout (INSTRUCTOR ONLY)

## Model Solution

**Certificate model (workload identity):**

- *Who gets certs:* every **workload**, not every human — SPIFFE-style
  identity (`spiffe://fintech.internal/ns/payments/sa/ledger`) issued by the
  internal PKI's mTLS intermediate; identity follows the workload, so
  authorization can bind to it later (zero-trust posture).
- *Lifetimes:* **24-hour leaf certs, auto-rotated** by the mesh (sidecar/
  agent handles renewal; services never see key material) — short leaves
  make revocation nearly unnecessary and rotation failure loud *fast*
  (cs-044's lesson inverted: automation with monitoring, not spreadsheet).
- *Rotation mechanics:* mesh agent requests from an internal CA via
  in-cluster signing; monitor `cert_issued_failures` and
  `time_to_expiry_minimum` fleet-wide; alert T-6h (with 24 h leaves,
  thresholds compress).
- **Vendor binaries on VMs (the graded constraint):** no code changes
  possible → run a **host-level proxy/sidecar on the VM** that terminates
  mTLS: the *proxy* holds the workload identity (certs, rotation), the
  vendor binary speaks plaintext to localhost — traffic between machines
  is always mTLS-wrapped. Identity assignment: one proxy per VM-workload
  class, identity from the VM's instance metadata/role binding. This is
  the standard mesh-VM integration pattern; the honest note: localhost
  plaintext remains (bound to loopback, same trust domain as the process),
  and host-compromise already means game-over anyway.

**Rollout:**

- *Namespace ordering:* **payments first** (compliance driver, highest
  value, moderate count) → **experiences/consumer-facing namespaces**
  (blast-radius practice) → **batch/analytics** (biggest, chattiest, least
  latency-sensitive — the stress test) → **vendor-VM namespace last**
  (needs the host-proxy pattern proven in staging). Payments-first also
  front-loads the compliance evidence.
- *Permissive-to-strict mechanics:* mesh mTLS in **permissive** (accept
  plaintext + mTLS) for the namespace during a transition window; service
  teams flip clients as they onboard; namespace flips to **strict**
  (mTLS-only) when the flow inventory shows zero plaintext sources —
  strictness is *evidence-gated*, not calendar-gated. **Honest risk of
  permissive:** a misconfigured/rogue client silently downgrades to
  plaintext *during* the window (that's its function); bound the window
  (≤30 days/namespace), alarm on plaintext-accepted counts that *increase*
  after week 1, and report the counts weekly — the plaintext period is
  measured, not assumed.
- *Plaintext bound:* day 30: ≤60% (payments strict + first namespaces);
  day 90: ≤15% (all K8s strict; VMs in permissive); day 180: ~0%
  inter-machine plaintext (VM host-proxies strict). Publish the numbers —
  the audit reads the trend line, not the promise.

**Three failure modes + responses:**

| Failure mode | Mechanism | Design response |
|---|---|---|
| Cert expiry storm | CA outage during mass renewal window | CA redundancy (2 issuers), renewal jitter (not synchronized), cached last-good cert valid 24 h grace, T-6h paging |
| Sidecar/agent upgrade outage | mesh version skew breaks data plane | canary namespaces for mesh upgrades, version-skew policy (N-1 support), rollback runbook |
| Clock skew | 24-h leaves validate against wall clock; skewed host rejects valid certs | NTP discipline as a *prerequisite* (checked pre-rollout), skew alarms, grace margins in cert validity windows |

## Alternative Solutions

- **Skip mesh; per-service cert management:** works for 20 services, dies
  at 120 (rotation sprawl); the mesh's agent is the scaling answer.
- **Network-layer encryption only (IPsec/WireGuard between nodes):**
  encrypts everything cheaply but provides *no workload identity* —
  authorization can't bind to it; fine as a *complement*, not the goal.
- **mTLS at the ingress only:** the status quo that produced the audit
  finding; rejected.

## Tradeoffs

- 24-h leaves vs CA dependency: short leaves make the CA critical
  infrastructure — the redundancy/jitter design is the price of admission.
- Sidecar overhead (latency, memory) vs universal coverage: measure at the
  batch namespace (the stress test); latency-sensitive paths get direct
  mTLS libraries where justified.
- Payments-first vs easy-namespace-first: compliance driver says payments;
  risk-practice says easy-first — payments-first wins because its service
  count is moderate and the evidence clock starts.

## Common Mistakes

- Certs per *service* (static, long-lived) instead of per-workload identity
  (rotated) — reintroduces cs-044.
- Calendar-gated strictness ("we'll be strict in Q3") instead of
  evidence-gated.
- Forgetting VM/vendor binaries until month 4 (the plaintext bound blows
  up).
- No plaintext-*count* telemetry during permissive — the transition is
  unmeasured.

## Instructor Prompts

- "What exactly does the localhost plaintext leg risk, and why is it
  acceptable?"
- "Which telemetry number proves the rollout is real to an auditor?"
- "Why does 24-hour rotation change your CA's threat model?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Workload-identity model; host-proxy for vendor binaries |
| Technical accuracy | 25% | Rotation/jitter/skew mechanics |
| Alternatives considered | 20% | Node-encryption/ingress-only rejection logic |
| Communication | 15% | Ordering + plaintext-bound table |

**Timing:** reveal at 5:00 + 2; the host-proxy trick is the design payoff.

## CLO Mapping

- **CLO-6** — mTLS identity architecture and migration engineering.
