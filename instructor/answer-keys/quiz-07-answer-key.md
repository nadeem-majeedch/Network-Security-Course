---
quiz: quiz-07
type: answer-key
instructor-only: true
distribution: never-publish-to-students
clos: [CLO-2]
marks: 10
status: complete
---

# Answer Key — Self-Check Quiz 7 (Week 3)

1. **B** — a forged reply claims another host's identity: spoofing (which
   then enables tampering/disclosure downstream).
2. **A** — snooping validates DHCP servers + rate-limiting blunts
   starvation; the other pairs mix unrelated features.
3. **B** — CAM-table overflow → fail-open flooding; default-drop would
   defeat the attack.
4. **B** — forwarding keeps the victim online so the MITM position persists
   silently; a broken victim gets investigated.
5. **A** — BPDU guard err-disables access ports receiving BPDUs; STP
   protection is about who *speaks* STP, not encryption.
6. **(2)** ARP has no per-message authentication in its original design —
   hosts accept unsolicited replies by design (statelessness + trust of
   broadcast). Compensation is *infrastructural*: Dynamic ARP Inspection
   validates replies against a trusted binding database (from DHCP
   snooping), plus port security limits MAC churn. *(1 design fact, 1
   features)*
7. **(2)** Trust **off** on the conference-room/unused port and on all user
   access ports; trust **on** only toward the legitimate DHCP server(s) on
   the trunk/core path.
8. **(2)** L2 attacks exploit *protocol trust* (ARP/STP/DHCP behavior),
   which all switches implement regardless of age — hardware refresh is
   not a mitigation; features like DAI/BPDU guard are.
