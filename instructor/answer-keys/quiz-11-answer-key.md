---
quiz: quiz-11
type: answer-key
instructor-only: true
distribution: never-publish-to-students
clos: [CLO-9, CLO-10, CLO-12]
marks: 10
status: complete
---

# Answer Key — Self-Check Quiz 11 (Week 11)

1. **A** — a SPAN/mirror point yields whatever traverses it (both
   encrypted and clear); it shows no endpoint events and needs no inline
   position to *observe*.
2. **B** — signatures match known patterns; novel behavior evades them
   (hence anomaly/behavioral complement).
3. **B** — Zeek's strength is deep protocol analysis → structured
   behavioral logs; it observes (IDS-side), doesn't block or encrypt.
4. **B** — environmental metrics adapt base severity to asset context;
   patch status is *remediation*, not scoring.
5. **B** — authenticated scans read installed packages/OS state → far
   fewer false negatives (and often fewer FPs); C is backwards.
6. **(2)** High-FP rules train analysts to distrust/ignore the alert
   class — eroding future true-positive response (trust damage compounds);
   they also bury lower-volume high-value signals in noise volume.
7. **(2)** SPAN→sensor path = packet-level evidence (Zeek/IDS data);
   firewall→SIEM = policy decisions (allows/denies, NAT, identities).
   Full credit names both mappings.
8. **(2)** Proves-it-works metric: % of criticals remediated within 7
   days (or mean time-to-remediate for criticals). Proves-it-matters
   metric: incidents/exploitable exposures attributable to unpatched
   criticals (or risk-reduction/exposure-window trend). *(1 each)*
