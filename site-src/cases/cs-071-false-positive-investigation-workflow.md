# cs-071 — False-Positive Investigation Workflow

> **Simulated scenario.** The alert, evidence, and workflow are fictional.

## Difficulty & Domain

- **Difficulty:** Advanced · **Domain:** IDS/IPS alerts · **CLO:** CLO-9
- **Est. time:** 15 minutes · **Anchor:** L22 (IDS/IPS — Signatures & Tuning)

## Scenario

An IDS rule (`SQLi-pattern in URI`) fires 200×/day, all traced to one
internal service. The SOC *assumes* false positive and wants it
suppressed. You must run the **investigation first**: a workflow that
distinguishes "benign traffic matching the pattern" from "the pattern is
fine but the *service* is being abused" — because one of this week's
alerts is actually an XSS-adjacent probe from a compromised laptop (the
case's hidden truth). Design the workflow that would have caught it.

## Stakeholders

- **SOC analysts** — 200/day; suppression is tempting.
- **App team** — owns the service; claims "it's our health-check format."
- **Detection engineering** — owns the rule's future.
- **The hidden attacker** — a compromised laptop probing the service
  with payload-shaped URIs mixed into the health-check noise.

## Network Context

- Service: internal API `api.internal.example`, URI pattern
  `/v1/q?filter=<encoded>` where `<encoded>` *legitimately* contains
  SQL-like strings (the app's filter DSL).
- IDS rule matches URI patterns like `union select`, `--`, `' OR` —
  firing on the DSL's legit encodings.
- Source mix: 6 app health-checkers (150/day), 2 analytics jobs
  (45/day), 5 human-debug sessions (5/day) — and this week, 1 laptop
  (10/day) whose URIs encode *different* payloads than the DSL produces.

## Student Task

1. Build the **FP-investigation workflow** (steps + decision points):
   alert → source-classification → payload-diffing vs known-benign
   baseline → business-context check → disposition classes. The
   workflow must distinguish *three* outcomes: pure-FP (suppress),
   noisy-but-real-risk (retune + monitor), and true-positive-in-noise
   (escalate) — with the evidence each requires.
2. Apply it to this week's data: which evidence separates the laptop's
   10/day from the 195/day? (Name the concrete diff: payload entropy?
   URI structure? source history? response codes?)
3. Give the **disposition artifacts**: what gets recorded for each
   class so the next analyst inherits knowledge, not folklore — and
   the rule's fate (suppress / retune / keep) with justification.

## How to Approach This (Reasoning Scaffold)

- "FP" is a *disposition*, not a diagnosis — the workflow's job is to
  earn the label with evidence per-source, per-payload.
- The health-check defense ("it's our format") explains 195 alerts —
  it cannot explain *payloads the DSL never produces*; the diff is in
  the payload corpus, not the alert count.
- Response codes are the free forensic: probes that *error differently*
  than benign DSL queries are behaviorally distinct even when URIs look
  similar.

## CLO Mapping

- **CLO-9** — Alert triage workflow and disposition discipline.

## Safety Notes

- Simulated alerts; no exploitation guidance beyond triage framing.
