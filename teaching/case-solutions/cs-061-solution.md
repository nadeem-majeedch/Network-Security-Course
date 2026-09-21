---
case: cs-061
solution-for: modules/module-05-wireless-cloud/case-studies/cs-061-vpc-design-review-for-a-three-tier-app.md
difficulty: advanced
module: 5
lecture-anchor: L19
clos: [CLO-13]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-061 Solution — VPC Design Review (INSTRUCTOR ONLY)

## Model Solution

**Arbitration — walk the packet:** a packet from the internet to the DB
needs (1) a routable destination — DB has no public IP: ✗; (2) a route
from IGW — DB subnets are local-only: ✗. **Direct internet→DB: NOT
reachable as designed.** The pen-test claim is **half-true**: it's
impossible *directly*, but the design makes the DB *one app-host
compromise away* — sg-db's source is `10.0.0.0/16` (the whole VPC), so
any app instance (or *any future instance anywhere in the VPC*, including
a mislabeled/bloated one, a jump host, a test box with a public IP via
the auto-assign-on subnet 10.0.2) can initiate 5432 to the DB. The
correct summary: "not internet-reachable; one-hop reachable from any
VPC-host, and at least one VPC subnet auto-assigns public IPs — the
two-hop path exists by design."

**Findings (ranked):**

| Rank | Finding | Mechanism | Fix |
|---|---|---|---|
| 1 | **sg-db source = whole VPC** | any VPC host → DB:5432; the tiering claim is cosmetic | source = **sg-app** (SG-chaining), not CIDR |
| 2 | **Auto-assign public IP ON in a "private" subnet (10.0.2)** | any instance there gets internet-initiable inbound if its SG allows; also the app tier's IGW route tempts drift | turn OFF; re-home anything public into true public subnets behind the ALB |
| 3 | **App RT: 0.0.0.0/0 → IGW** | app instances "patch" via IGW with public-IP-less semantics broken/fragile (provider-dependent) — and egress is uncontrolled | route app subnets via **NAT gateway** (or egress proxy); egress SG scoped to needed endpoints |
| 4 | **sg-app egress 0.0.0.0/0 all** | compromised app host exfiltrates freely | egress allow-list (patch endpoints, internal services) |
| 5 | **NACLs default-allow everywhere** | no subnet fence; nothing catches SG mistakes | add *targeted* NACLs (e.g., db subnets: allow 5432 from app subnets only, deny-else; ephemeral-return handling) — defense in depth, not primary control |

**Redesign table:**

| Tier | Subnets | Route table | SG (ingress) | SG (egress) |
|---|---|---|---|---|
| Public/edge | 10.0.1/24, 10.0.2/24 (**auto-assign OFF**; ALB only, no other instances) | 0.0.0.0/0 → IGW | sg-alb: 443 from 0.0.0.0/0 | to sg-app:8080 only |
| App (private) | 10.0.11/24, 10.0.12/24 | 0.0.0.0/0 → **NAT GW** (+ S3/patch endpoints via gateway/endpoints if provider supports) | 8080 from **sg-alb** | 5432→sg-db; HTTPS→patch/registry list only |
| DB (isolated) | 10.0.21/24, 10.0.22/24 | **local only** | 5432 from **sg-app** | none (or to replication peer SG) |
| NACLs | db subnets: allow 5432 in from app CIDRs, allow ephemeral out; deny-else — *defense in depth under the SGs* | | | |

**Where NACLs add real value vs noise:** as *subnet fences* that survive
SG misconfiguration (stateless, so they catch the "whoops, sg wide-open"
class) and for explicit deny-ranges (block-listed sources, or denying
east-west between unrelated subnets). As the *primary* tiering tool they
rot: stateless ephemeral handling makes every rule change fiddly — SG
chaining is the maintainable control; NACLs are the fence behind it.

## Alternative Solutions

- **NACL-first redesign (strict allow-list NACLs per tier):** strong on
  paper; operational rot risk (ephemeral ports, churn) — keep SGs
  primary.
- **Move DB to a separate VPC/peered account:** strongest blast-radius
  separation (account-level fence); real cost: peering/endpoints/ops —
  the right end-state for PII per compliance; note it as phase 2.
- **Private endpoints instead of NAT for patching:** excellent where
  supported (no public egress at all for app tier) — provider-feature
  dependent; prefer where available.

## Tradeoffs

- SG-chaining vs CIDR-scope: chaining follows infrastructure (autoscale,
  replaces) automatically — the whole point in cloud; CIDR rules rot on
  the first re-subnet.
- NAT GW cost vs IGW+auto-assign: NAT is the price of *private* egress;
  endpoint-based patching shrinks it.
- Defense-in-depth NACLs vs change velocity: fence the *stable* tiers
  (db), leave chatty tiers SG-managed.

## Common Mistakes

- Declaring the DB "unreachable" and closing the finding (the one-hop
  path is the finding).
- Fixing sg-db with a *narrower CIDR* instead of sg-chaining (rot
  reborn).
- Leaving auto-assign ON because "no instance currently has one"
  (default-drift trap).
- NACL rewrites of everything (stateless pain, no added security over
  correct SGs).

## Instructor Prompts

- "Which single rule change collapses the pen-test's two-hop path to
  zero?"
- "Why does source=SG beat source=CIDR structurally in cloud?"
- "Where would a *stateless* control catch a mistake the stateful one
  can't?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Packet-walk arbitration; one-hop framing |
| Technical accuracy | 25% | SG/NACL/route-table mechanics precise |
| Alternatives considered | 20% | Separate-VPC/endpoints tradeoffs |
| Communication | 15% | Redesign table as deliverable |

**Timing:** reveal at 5:00 + 10; the "half-true" arbitration is the
case's honesty lesson.

## CLO Mapping

- **CLO-13** — Cloud VPC design review with control-mechanism precision.
