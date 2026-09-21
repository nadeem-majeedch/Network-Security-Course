---
case: cs-069
solution-for: modules/module-06-detection-vulnerability/case-studies/cs-069-suricata-rule-for-a-c2-beacon-pattern.md
difficulty: advanced
module: 6
lecture-anchor: L22
clos: [CLO-9]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-069 Solution — Suricata C2 Beacon Rule (INSTRUCTOR ONLY)

## Model Solution

**Draft critique:**

| Defect | Consequence |
|---|---|
| Single feature (`/px/` prefix) | matches the *monitoring tool* (its URIs start `/px/`) → 3 hosts × 1440/day = the noise floor |
| No UA constraint | the malware's fixed MetricsBot UA — its most distinctive header — unused |
| No URI *structure* | `/px/<32-hex>.gif` vs monitor's `/px/<fixed-id>.gif` — the discriminating difference is the hex-length, and `content:"/px/"` can't see it |
| No cadence control | even a correct match alerts per-request → alert storm |
| No directionality/protocol scoping beyond ports | matches proxy-terminated plaintext too — fine, but scope explicitly |

*Principle:* single-feature signatures scale noise linearly with
feature-popularity; **behavioral combinations** (feature *sets* unlikely
to co-occur benignly) scale detection. The rule's job is to encode the
co-occurrence.

**Refined rule (conceptual-level Suricata syntax):**

```
alert http $HOME_NET any -> $EXTERNAL_NET 443 \
  (msg:"C2 beacon px pattern (hex-uri + MetricsBot UA)"; \
   flow:established,to_server; \
   http.uri; pcre:"/\/px\/[0-9a-f]{32}\.gif$/"; \
   http.user_agent; content:"MetricsBot/2.4"; \
   detection_filter:track by_src,by_dst,count 3,seconds 300; \
   classtype:trojan-activity; sid:9000002; rev:2;)
```

What each keyword buys:

| Keyword | Buys |
|---|---|
| `flow:established,to_server` | directionality — client-side beacon only; kills server-side reflection noise |
| `pcre` on uri (32-hex + `.gif` anchor) | the URI *structure* the monitor tool lacks (its id is fixed, not 32-hex) — the strongest in-rule discriminator |
| `http.user_agent` content | the co-occurrence pair: hex-uri **AND** MetricsBot UA — monitor tool fails the second conjunct; false-positive class collapses |
| `detection_filter track by_src,by_dst count 3 / 300s` | cadence design: needs 3 matches in 5 min per pair — a *single* stray request can't alert; a 60 s beacon chain (3 hits in ~2 min) alerts once per chain-window; 40/day → ~1 per chain |
| (optional) `flowbits` | chain the TLS JA3 fingerprint (separate rule sets a bit when JA3 J seen from same src; this rule requires the bit) — two-signal conjunction across protocols; adds precision at complexity cost — acceptable if the JA3 is stable in the sandbox |

Result against the noise source: monitor tool fails UA *and* hex-structure
→ zero matches; against the beacon: matches → one alert per 5-min chain.

**Evasion-resistance layer (when it adapts):**

| Adaptation | Signature fate | Fallback that still binds |
|---|---|---|
| Change UA | rule dies (UA conjunct) | **JA3 + interval** via flow analytics: JA3 J + 60±2 s periodicity per (src,dst) — the *behavioral* fingerprint survives UA/URI edits; alert in Zeek/flow pipeline |
| Change URI structure (drop `/px/hex.gif`) | rule dies | SNI + threat-feed reputation + *interval* analytics; also JA3 persists (TLS stack rarely rewritten) |
| Change TLS stack (new JA3) | JA3 layer dies | interval+size-shape analytics (deterministic 60 s ± 2 s, ~200 B responses) — the *timing* is the last fingerprint to fall; and endpoint EDR sees the process |

*Honest limit:* signature-only detection catches the *current* config;
durable detection is the layered stack (rule → JA3/flow analytics →
timing/shape → EDR). Each layer's cost rises as its precision falls —
that trade is the discipline.

## Alternative Solutions

- **Drop the rule; rely on flow analytics only:** consistent layering,
  but the rule is the *cheap high-precision* layer — keep it for the
  current config, layer the rest.
- **JA3-only rule:** single-feature again (JA3s are shared by benign
  tooling) — same noise trap, different feature.
- **IP-blocklist the C2 immediately without a rule:** containment beats
  detection for *known* infra, but kills your visibility into other
  infected hosts (they'll use the next IP); rule + block are complements
  (cs-025's sinkhole lesson applies).

## Tradeoffs

- Rule precision (UA+hex+filter) vs adaptation speed: precise rules die
  fast when malware iterates — budget the rev cycle (intel feed → rule
  update SLA).
- detection_filter thresholds: too low → noise returns; too high →
  slow chains missed — 3-in-300 s fits a 60 s beacon with margin; tune
  per observed cadence.
- flowbits complexity vs precision: two-signal conjunctions are worth it
  for high-value families, not for every rule — precision budgeting.

## Common Mistakes

- "Fixing" loudness by loosening the rule (the opposite direction).
- Missing that the *noise source shares the cadence* — cadence alone
  can't discriminate (the monitor tool is 60 s exact, which is itself a
  discriminator *against* the jittered beacon — use it in the analytics
  layer: exact-periodicity = monitor; jittered = beacon).
- Alert-per-request (no filter) → alert fatigue kills the rule socially.
- No fallback layer named (signature-only = detection debt).

## Instructor Prompts

- "Which two features does the monitor tool *not* share — and why is
  their conjunction the rule's spine?"
- "The malware drops the UA tomorrow: what fires, what doesn't?"
- "Why is exact 60 s periodicity *suspicious* in the analytics layer?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Behavioral-combination logic; noise-source discrimination |
| Technical accuracy | 25% | Suricata keyword semantics (pcre/filter/flowbits) |
| Alternatives considered | 20% | Layered-fallback design |
| Communication | 15% | Keyword-buy table + evasion layering |

**Timing:** reveal at 5:00 + 10; the monitor-tool discrimination is the
tuning lesson.

## CLO Mapping

- **CLO-9** — IDS signature engineering and tuning discipline.
