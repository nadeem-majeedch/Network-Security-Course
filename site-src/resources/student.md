---
status: complete
artifact-type: student-resources-page
instructor-only: false
---

# Student Resources

Everything you need to run the course environment on your own laptop, plus
the study aids built into the course.

## Course environment

| Tool | Used in | Install notes |
|---|---|---|
| VirtualBox/VMware + lab VMs | Labs 01–16 | Course OVA distributed in week 1; 8 GB RAM minimum recommended |
| Wireshark / tshark | Labs 01–04, 15 | wireshark.org; add yourself to the dumpcap group on Linux |
| pfSense VM | Labs 05, 06 | Lab range image; snapshots before each rulebase exercise |
| Suricata | Labs 11, 13 | suricata.io; use the course ruleset bundle |
| Zeek | Labs 12, 13, 15 | zeek.org; course log-bundle provided for analysis tasks |
| Cloud sandbox | Labs 09, 10 | Instructor-provisioned project; **never** use personal cloud accounts for coursework |

The dataset generator (`docs/labs/setup/generate_lab_datasets.py` in the
repository) produces the deterministic PCAPs and logs used across labs —
regenerating gives byte-identical evidence for reproducible submissions.

## Study aids in this course

- **100 case studies** with the five-step classroom protocol — see
  [Case Studies](../cases/index.md). The reasoning reps are the exam prep.
- **Weekly self-check quizzes** (ungraded) for every week — ask in the LMS.
- **The three through-lines** that the final exam explicitly tests:
  1. *Every shortcut in a protocol is a security decision someone inherited.*
  2. *Design beats patching: zone boundaries and default-deny remove attack classes.*
  3. *Evidence discipline is a security skill — captures, logs, and timelines must survive scrutiny.*

## Reference shelf

- Official protocol references: RFCs for TCP (9293), DNS, DHCP, ICMPv4/6.
- NIST: SP 800-41 (firewalls), SP 800-77 (IPsec), SP 800-94 (IDPS),
  SP 800-207 (zero trust), SP 800-61r2 (incident handling).
- OWASP Cheat Sheet Series for TLS and session management.
- Course textbook list and weekly readings: see the
  [course description](../course/description.md) and lecture pages.

## Accessibility

If you need accommodations for timed assessments or lab work, contact the
instructor in week 1 — all lab VMs run at accessible resolutions and all
course material is screen-reader tested where formats allow.
