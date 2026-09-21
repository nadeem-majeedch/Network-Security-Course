---
quiz: quiz-14
type: answer-key
instructor-only: true
distribution: never-publish-to-students
clos: [CLO-8, CLO-9, CLO-11, CLO-14, CLO-15]
marks: 10
status: complete
---

# Answer Key — Self-Check Quiz 14 (Final Preparation)

1. **B** — cloud visibility = flow logs, identity/API audit as
   first-class sources; payload capture is deliberate opt-in, not default.
2. **B** — prioritization is environmental: unreachable + compensated =
   lower effective priority than the base 9.8 suggests.
3. **B** — corroboration-then-contain per reversibility; immediate
   containment on single-source alerting risks wrong-action cost (though
   error asymmetry may justify immediate isolation if framed — accept
   with stated asymmetry, but B is the taught discipline).
4. **B** — acquisition→hash→store→access records are the chain;
   screenshots/USB/verbal handover break verifiability.
5. **B** — gates = evidence before expansion (cs-093's phase-gate
   design); they don't replace pilots, they *read* them.
6. **(2)** MTTD is an *outcome* metric of detection capability — it
   changes what the board does (funds/holds the program); rule counts
   are *activity* metrics with no decidability (40 rules may add noise).
7. **(2)** First-seers: **VPC flow logs** and **cloud identity/API audit
   logs** (cloud-side attack signatures); never-seer: **on-prem SPAN/Zeek
   at the core switch** (the attack never traverses the wire it mirrors).
8. **(2)** Model: *detection* — Zeek/DNS logging flags high-entropy,
   long-domain queries (tunneling heuristic) → *response* — the runbook
   contains via egress DNS restriction + resolver allow-list, then hunts
   for the beaconing host. Any correct detection→response chain earns
   credit.
