---
case: cs-006
solution-for: modules/module-01-network-foundations/case-studies/cs-006-tcp-half-open-flood.md
difficulty: beginner
module: 1
lecture-anchor: L03
clos: [CLO-1]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-006 Solution — Half-Open Flood (INSTRUCTOR ONLY)

## Model Solution

**Mechanism:** a **SYN flood (classic DoS, on-path-optional)** exhausting the
server's half-open connection resources. Attack SYNs complete only the first
handshake step; the kernel holds state in `SYN_RCVD` until timeout. With
`SYN_RCVD 8192` (backlog saturated) the kernel stops accepting new handshakes
— the process is healthy, the *queue* is full, so `listen()` accepts nothing.
This is resource exhaustion at the kernel queue, not process death.

**Why internal users work:** load-balancer health checks and internal
management traffic arrive on interfaces/subnets where the firewall or kernel
prioritizes/pre-allows them; more precisely, internal monitoring traffic comes
from a small, known subnet whose established sessions predate the flood and
whose SYN consumption is tiny — the shared queue is still mostly full, so
"internal works" is a graceful-degradation artifact, not immunity.

**Why restart "fixes" it:** restart clears kernel queues — the attacker's
queue entries flush, users recover, and the flood refills the queue in ~20
minutes. A restart treats the symptom (queue state), not the cause (unsolicited
SYNs).

**Mitigation ranking for the next hour:**

| Rank | Mitigation | Why |
|---|---|---|
| 1 | **upstream scrubbing (uRPF loose-mode + upstream scrubbing)** | 6,100 IPs across 300+ countries with ≤4 SYN/min each is a botnet shape; the only lever that actually stops the flood before it consumes resources is filtering close to the source or scrubbing upstream. Provider filtering (ACLs at the edge) is immediate. |
| 2 | **SYN proxy on the firewall** | Answers the handshake on the server's behalf, holds no server state until the client completes; converts the attack from "server queue exhaustion" to "firewall CPU" — buys hours of headroom while upstream scrubbing comes online. |
| 3 | **Per-IP rate limit** | Nearly useless here: every IP is ≤4/min, below any useful threshold. Included precisely to test whether students pick shape-blind controls. |
| 4 | **Lower the backlog** | Actively harmful: fewer half-open slots → fails sooner, helps nobody. |

**Top choice: upstream scrubbing/filtering.** SYN proxy is the correct
*tactical* shield while scrubbing ramps; per-IP limits and backlog tuning are
misfit tools for a distributed low-and-slow shape.

## Alternative Solutions

- **SYN cookies** (kernel feature) — worth naming; if the server had them
  enabled the failure would not occur. Retroactively enabling is a mid-incident
  kernel change; defensible but riskier than firewall SYN proxy.
- **Null-route top talkers** — the histogram shows no top talkers; would
  null-route thousands of legit-ish IPs; rejected.
- **Move the portal behind a CDN/scrubbing service** — the *right* long-term
  architecture; too slow for "next hour" but the debrief should land it as the
  strategic fix.

## Tradeoffs

- SYN proxy: firewall CPU vs server queue — you're choosing which box sweats.
- Upstream filtering: fastest relief but depends on the provider's tooling and
  escalation path — a Monday-morning conversation to have *before* the incident.
- Restart reflex: feels like action; burns credibility and loses forensic state.

## Common Mistakes

- Saying "the server crashed" — counters prove the process is healthy.
- Picking per-IP rate limiting because it's the familiar control (shape-blind).
- Listing "lower the backlog" as if tuning knobs free resources.
- Missing that internal users working is queue-priority artifact, not evidence
  the attack is external-only.

## Instructor Prompts

- "What does the 46,000-session firewall number tell you about the attacker's budget?"
- "Why does this attack not show up as high per-IP bandwidth?"
- "If SYN cookies were on, what would the counters look like instead?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Queue-vs-process distinction; shape-based mitigation logic |
| Technical accuracy | 25% | Correct `SYN_RCVD` mechanics; no impossible actions |
| Alternatives considered | 20% | Ranking justified, incl. why familiar controls misfit |
| Communication | 15% | Ranked table with one-line whys |

**Timing:** reveal at 5:00; the ranking exercise is the debrief's center of
gravity — push on "why is the familiar control wrong here."

## CLO Mapping

- **CLO-1** — TCP handshake mechanics → DoS failure analysis.
