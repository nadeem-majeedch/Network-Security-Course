---
case: cs-071
solution-for: modules/module-06-detection-vulnerability/case-studies/cs-071-false-positive-investigation-workflow.md
difficulty: advanced
module: 6
lecture-anchor: L22
clos: [CLO-9]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-071 Solution — FP Investigation Workflow (INSTRUCTOR ONLY)

## Model Solution

**Workflow (steps + decision points):**

```
1. ALERT cluster: group 200/day by (source, URI-template, payload-class)
   ↓
2. SOURCE classification: identity + history per source
   (health-checker? CI? human? unknown laptop?) — known sources get
   expected-payload *corpora*; unknown sources never inherit a benign
   label by volume alone
   ↓
3. PAYLOAD diff vs benign corpus: decode the URI param; compare against
   the DSL's grammar (what CAN the filter DSL produce?) — anything the
   grammar cannot generate is outside "it's our format"
   ↓
4. BEHAVIOR check: response codes + timing per source (benign DSL
   queries get 200s; probes enumerate — distinct error classes, pacing)
   ↓
5. BUSINESS context: does the source have any reason to touch this
   service at all (CMDB/ticket)?
   ↓
6. DISPOSITION:
   a. PURE-FP  → source ∈ known, payload ∈ grammar, behavior normal
                 → suppress *for that source*, record corpus
   b. NOISY-RISK → source known, payload partially outside grammar,
                 behavior anomalous → retune + targeted monitoring
   c. TP-IN-NOISE → payload outside grammar + behavior probing
                 → escalate to IR (this week's laptop)
```

**Applied to this week's data — what separates the laptop's 10/day:**

| Evidence | 195/day benign | Laptop's 10/day |
|---|---|---|
| **Payload vs DSL grammar** | encodings map to documented filter operators (verifiable: decode → grammar AST) | payloads decode to *multi-clause injection scaffolding* the DSL cannot express (comment sequences `--`, stacked quotes the grammar never emits) |
| **URI structure** | fixed template `/v1/q?filter=<one-op>` | variable, op-chained URIs — the *template* differs |
| **Response codes** | uniform 200s (queries succeed) | mix of 400/500/200 — probing behavior (error-based enumeration) |
| **Source history** | 6 known checkers + 2 CI jobs, months of consistent corpora | first-seen laptop, no prior corpus, *started the same week* |
| Timing | scheduler-aligned (health checks every N min) | random intra-hour pacing |

Any *one* is suggestive; the conjunction (payload-outside-grammar + new
source + error-mix) is conclusive — and step 3 is the load-bearing one:
**the app team's "it's our format" defense is testable against the
grammar**, and the laptop's payloads fail it. That's the workflow's
whole point: the FP claim is *falsifiable*, so test it.

**Disposition artifacts:**

| Class | Artifact recorded |
|---|---|
| Pure-FP | per-source corpus entry (sampled benign payloads), suppress-scope note (source-scoped, expires on corpus drift), ticket ref |
| Noisy-risk | retune ticket, monitored-exception register w/ review date |
| TP-in-noise | IR case link, indicator export, *rule-retention note* ("this rule caught it — do not suppress") |

**The rule's fate: keep, retune, never suppress globally.** Retune:
scope-out the *six checkers' exact templates* (source+template-scoped
suppress — cheap, corpus-backed) so human/exotic traffic still matches;
the laptop's class keeps firing. Global suppression would have silenced
the week's only true positive — the counterfactual the CISO artifact
(cs-070) exists to prevent.

## Alternative Solutions

- **Suppress globally on the app team's word:** the workflow exists to
  make that reflex falsifiable; as a *decision* it fails the case —
  but naming what evidence *would* justify it (full-corpus match for
  all sources) shows the reasoning.
- **Retune to drop the DSL-encoding patterns entirely:** risks missing
  injection *hidden inside DSL-valid encodings* (double-encoding
  class) — source-scoped suppression beats pattern-narrowing here.
- **Rate-limit the alert (cs-070's filter trick) instead of
  investigating:** manages fatigue, delays the truth — pair it, don't
  substitute.

## Tradeoffs

- Per-source suppression maintenance vs global silence: corpora decay
  (DSL evolves) — corpus entries get expiry + diff-checks; the cost is
  the price of keeping TP visibility.
- Investigation depth vs 200/day volume: the workflow runs *once per
  source-class*, not per alert — clustering makes it affordable.
- Grammar-verification effort (app team time): one afternoon to export
  the filter DSL's grammar — the highest-leverage ask in the case.

## Common Mistakes

- Counting-based triage ("195 identical alerts = FP") — volume is not
  evidence; payloads are.
- Accepting "it's our format" without the grammar test (the app team
  believes it; the laptop proves otherwise).
- Global suppression (the counterfactual dead TP).
- No artifacts (next analyst re-litigates from zero).

## Instructor Prompts

- "Which step falsifies the app team's claim — quote the test."
- "The laptop fires 10/day inside 200: why does clustering save this
  investigation from drowning?"
- "What does the retention note for the rule say, verbatim?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Three-outcome workflow; falsifiable FP test |
| Technical accuracy | 25% | Payload/behavior/grammar mechanics |
| Alternatives considered | 20% | Suppress/retune/rate-limit trades |
| Communication | 15% | Workflow diagram + artifact table |

**Timing:** reveal at 5:00 + 10; the grammar test is the case's core.

## CLO Mapping

- **CLO-9** — Alert triage workflow and disposition discipline.
