---
case: cs-036
solution-for: modules/module-03-secure-architecture/case-studies/cs-036-mgmt-subnet-inbound-acl.md
difficulty: intermediate
module: 3
lecture-anchor: L11
clos: [CLO-4]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-036 Solution — Management-Subnet Hardening (INSTRUCTOR ONLY)

## Model Solution

**Inbound ACL to `10.90.0.0/24` (8 rules):**

| # | Rule | Purpose | Finding closed |
|---|---|---|---|
| 1 | permit tcp host <jump-1> 10.90.0.0/24 eq 22 (SSH) | jump host → mgmt SSH (switches, storage) | F1 |
| 2 | permit tcp host <jump-1> <hypervisor-mgmt IPs> eq 443 | hypervisor consoles via **MFA gateway** (443 → gateway → host) | F1, F2 |
| 3 | permit tcp host <jump-1> 10.90.0.0/24 eq 443 | BMC web (TLS) via jump only | F1 |
| 4 | permit ip <MFA-gateway-IP> <hypervisor-mgmt> | gateway's own path (gateway→target) | F2 |
| 5 | permit tcp host <vendor-jump> 10.90.0.0/24 eq 22 **time-range VENDOR-WINDOW** | vendor path, time-boxed by policy object (recurring/renewable) | F3 |
| 6 | deny ip 10.0.0.0/8 10.90.0.0/24 (log) | ops VLAN & co. blocked; the log feeds bypass-detection | F1 |
| 7 | deny ip any 10.90.0.0/24 (log) | everything else — incl. site-to-site VPN *users* (they must jump too) | F1 |
| 8 | (on each BMC, its own allowlist) permit host <jump-1-IP> (+MFA-gw) | device-level backstop: even a firewall mistake leaves BMCs bound to 16-IP allowlists | F1 (defense in depth) |

Plus: BMC per-user local accounts with TLS-only, session timeout — F2's
BMC half (BMCs can't do enterprise MFA; the *network path* being jump+MFA-
gateway-only is the compensating control, stated explicitly for the auditor).

**Jump-path adoption design (secure = fast):**

1. **Measure the bypass:** why do engineers skip it? (Typically: second
   login, slow console, no clipboard.) Fix each: **SSO** on the jump host
   (AD + MFA = one login), session *resume* for drops, bookmarks that
   deep-link per device, clipboard/file-transfer enabled for approved
   sessions.
2. **Make bypass impossible, visibly:** ACL rule 6/7 logs every direct
   attempt; a weekly "direct-access attempts" digest to ops leads converts
   bypassing from invisible habit to visible exception.
3. **Procedural:** runbooks rewritten jump-first ("open → jump → device"),
   onboarding shows jump as *the* console; exceptions (break-glass) exist as
   a *named, logged* procedure — break-glass accounts excluded from rule 6
   via a dedicated host, alarmed on use. Security that lacks break-glass
   gets bypassed by panic; design the panic path.

**Vendor lifecycle (replaces ad-hoc edits):**

| Step | Mechanism (from evidence) | Evidence produced |
|---|---|---|
| Request | Ticket with scope (which BMCs), window, named engineer | ticket ID |
| Grant | ACL line for `vendor-jump` host + **time-range** rule auto-expiry; BMC local account created per-vendor-user, scoped to named devices | firewall config diff + ticket link |
| During | Jump host **session recording** on; BMC command logs forwarded | session artifacts |
| Expire | Time-range lapses automatically; BMC account disabled; standing ACL removed on ticket close | expiry proof (no manual step = no forgotten access) |
| Review | Monthly: vendor sessions reviewed; recurring needs → standing *narrow* rule with quarterly re-approval | audit export |

## Alternative Solutions

- **Full PAM/bastion product:** the enterprise end-state (credential
  vaulting, auto-rotation); as *this* audit response it's procurement-time —
  the jump-host design is the credible interim that PAM later replaces.
- **VLAN-relocate mgmt + NAC only:** helps but audit F1 demands an ACL/
  policy artifact; NAC complements, doesn't substitute.
- **BMC-serial-only access (no network):** maximally hardened; operationally
  regressive for 60 BMCs — the allowlist+jump compromise is the defensible
  middle.

## Tradeoffs

- MFA at gateway vs on-BMC: BMCs can't MFA — the gateway carries the
  control; document that honestly for F2 closure.
- Time-based vendor rules vs standing narrow rules: standing rules rot;
  time-boxes need renewal friction — renewal *is* the review control.
- Jump-host single point of failure: rule for jump-2 standby exists (same
  rules, second host); break-glass covers both being down.

## Common Mistakes

- ACL that permits "ops VLAN → jump host" but forgets *hypervisor gateway*
  flows (rule 4) — MFA path dies silently.
- Vendor lifecycle without auto-expiry (time-range) — manual expiry = F3
  reborn.
- "Fix the people" (tell engineers to use the jump host) without fixing the
  path speed — adoption fails within a month.
- BMC allowlists ignored as a backstop layer.

## Instructor Prompts

- "Which rule fails closed if the jump host dies, and what's the 3 a.m.
  path?"
- "Why is the BMC allowlist *more* trustworthy than one firewall rule?"
- "How would you prove F3's closure to the auditor in one artifact?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Path design (jump+gateway); lifecycle with auto-expiry |
| Technical accuracy | 25% | ACL/time-range/allowlist mechanics correct |
| Alternatives considered | 20% | PAM/NAC/serial options weighed |
| Communication | 15% | Rules→findings mapping; adoption plan realistic |

**Timing:** reveal at 5:00 + 2; "secure = fast" is the adoption principle
being taught.

## CLO Mapping

- **CLO-4** — Management-plane access engineering with lifecycle controls.
