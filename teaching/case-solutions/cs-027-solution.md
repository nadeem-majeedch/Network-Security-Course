---
case: cs-027
solution-for: modules/module-03-secure-architecture/case-studies/cs-027-dmz-design-review.md
difficulty: intermediate
module: 3
lecture-anchor: L09
clos: [CLO-3]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-027 Solution — DMZ Design Review (INSTRUCTOR ONLY)

## Model Solution

**Findings (ranked):**

| # | Finding | Attack path enabled | Exploitability | Blast radius |
|---|---|---|---|---|
| 1 | **DMZ web servers domain-joined to corp AD** | Web RCE → domain credential cache → corp AD attack surface from the most-exposed tier | **High** | Corp-wide |
| 2 | **"Allow DMZ→corp any" on Firewall B** | Web RCE → SMB/WMI/RDP laterally into corp; no egress discipline | **High** | Corp-wide |
| 3 | **DB service account is a domain account + no app↔DB segmentation** | App compromise → DB creds are *domain creds* → reuse them against domain controllers (no isolation) | High | DB + AD |
| 4 | **Any-port DMZ→APP** | Web RCE → unrestricted pivot to app tier, incl. management protocols if exposed | Med–High | App tier, then DB |
| 5 | **SMB-based backup pulls + monitoring via SMB from corp into DMZ** | Corp-side compromise pivots *in*; SMB into DMZ is the reverse channel attackers love; also weakens tiering | Med | DMZ→corp bridge |

**Top-2 blockers: #1 and #2** — together they are the classic
DMZ-collapse: one web RCE becomes corp-domain compromise. #3 is blocked-
adjacent (it rides #1/#2's path) but fixing the account *type* is cheap and
slashes the credential value — include it in the two-week window if vendor
capacity allows; the *go/no-go* line stays at #1/#2.

**Minimum rework (one paragraph):** rebuild the trust boundary — **remove
the web tier from corp AD** (workgroup tier or a *separate* DMZ forest with
one-way trust for management only), and **replace the DMZ→corp any-rule**
with an explicit, port-scoped flow set to named collector/patch systems
(HTTPS/443 to the patch proxy, mgmt via a jumphost with MFA, no SMB across
the boundary — switch monitoring to push-over-HTTPS or an appliance in the
DMZ). In the same window: pin the DB service account to a *local* account
(or better, a dedicated non-domain forest account), scope DMZ→APP to the
exact app ports (443/8080), and make backups **push-based** (DMZ pushes to
a DMZ-side staging, corp pulls from staging — SMB never crosses *into* the
DMZ). Two weeks is realistic for rule surgery + AD unjoin of two servers;
the AD-forest option can follow as phase 2 if unjoining slips.

## Alternative Solutions

- **Full redesign (three-firewall, separate forests, bastion):** the
  textbook end-state; as a go-live condition it fails proportionality —
  name it as roadmap, not gate.
- **Cloud WAF/CDN in front as mitigation:** reduces web-RCE likelihood but
  the blockers are *behind* the web tier; WAF is complementary, not
  compensating for #1/#2.
- **Accept blockers with monitoring-only compensations:** defensible for a
  *pilot* with no PII; this portal holds PII — monitoring does not bound the
  blast radius, so acceptance fails the audit test.

## Tradeoffs

- Workgroup tier vs separate DMZ forest: workgroup is fast and adequate for
  two servers; a forest scales to ten-plus but needs operational maturity
  (trust admin, patching identity).
- Push-vs-pull backups: push keeps SMB one-directional out of the DMZ but
  requires an agent in the tier — acceptable; pull keeps corp-side control
  but crosses the boundary backward.
- Vendor rework cost vs go-live slip: two weeks of rule surgery beats a
  breach; the *schedule* concession is the CISO's negotiating coin.

## Common Mistakes

- Ranking the any-rule first and missing the domain-join (or vice versa) —
  they are one kill chain, both must block.
- Treating "no firewall app↔DB" as the headline; without the domain-account
  finding it's a lower-order gap.
- Proposing only *new* purchases (NGFW, WAF) — the two-week answer is
  configuration surgery, not procurement.
- Forgetting the backup/monitoring reverse-path findings.

## Instructor Prompts

- "Walk the kill chain from web RCE to a domain controller with this design."
- "Which finding dies if the vendor simply unjoins two servers?"
- "What would you accept as *compensating monitoring* if go-live can't move?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Kill-chain tracing; blocker proportionality |
| Technical accuracy | 25% | AD/domain-account/SMB mechanics correct |
| Alternatives considered | 20% | Roadmap-vs-gate separation |
| Communication | 15% | Ranked table + one-paragraph rework |

**Timing:** reveal at 5:00 + 2; the "walk the kill chain" prompt is the
method being taught.

## CLO Mapping

- **CLO-3** — DMZ architecture review and risk-ranked findings.
