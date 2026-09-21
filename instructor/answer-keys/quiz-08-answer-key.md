---
quiz: quiz-08
type: answer-key
instructor-only: true
distribution: never-publish-to-students
clos: [CLO-3, CLO-4]
marks: 10
status: complete
---

# Answer Key — Self-Check Quiz 8 (Week 6)

1. **B** — NAT maps addresses and incidentally blocks unsolicited inbound;
   it is not a policy engine, identity system, or encryption.
2. **B** — explicit proxy = client-configured; transparent = intercepted
   without client awareness.
3. **B** — microsegmentation = fine-grained workload/service policies,
   independent of coarse network location.
4. **B** — per-request authorization from multiple signals is the tenet;
   A/C are slogans, D is the *opposite* of zero trust.
5. **B** — continuous, context-aware evaluation vs one-time admission
   decisions (NAC).
6. **(2)** Risk: outbound-initiating DMZ hosts reverse the flow model —
   compromise plus beaconing/exfil becomes trivial and allowed by design;
   control: explicit egress allow-list for DMZ segments (deny by default,
   log), or isolation of update paths through a proxy.
7. **(2)** Boundary 1: web tier ↔ app tier (internet-facing vs internal —
   highest exposure delta); boundary 2: app tier ↔ DB tier (protects the
   crown-jewel data store; app→DB flows are few and stable, so the policy
   is small and enforceable). Either order defensible if justified.
8. **(2)** "Allow established": only packets matching an existing,
   tracked connection (return traffic) pass — state-dependent. "Allow
   any": unsolicited new connections also pass — no state or origin
   constraint; the difference is precisely the stateful firewall's value.
