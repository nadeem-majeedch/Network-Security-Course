# cs-037 — NAT Mode Selection and Address-Plan Review

> **Simulated scenario.** The company, address plan, and requirements are fictional.

## Difficulty & Domain

- **Difficulty:** Intermediate · **Domain:** Enterprise architecture · **CLO:** CLO-3
- **Est. time:** 12 minutes · **Anchor:** L12 (NAT, Proxies, Egress & NAC)

## Scenario

A company acquired a subsidiary and must merge networks. You must choose
NAT modes per boundary and fix the address plan. Constraints: the
subsidiary's app must be reachable *from* the parent by IP; overlapping
`10.0.0.0/16` ranges exist on both sides; the subsidiary's printer fleet
hard-codes its gateway; dual-stack is coming next year. Deliver the NAT
design + address-plan fixes + the security commentary (NAT is not a
firewall).

## Stakeholders

- **Network architect (you)** — design that survives the merge.
- **App owners** — parent→subsidiary app access must not break.
- **Print fleet owner** — printers can't be reconfigured this year.
- **Security** — NAT must not become the *implicit* isolation story.

## Network Context

- Parent: `10.0.0.0/16` (HQ), `10.20.0.0/16` (DC).
- Subsidiary: `10.0.0.0/16` (flat — everything), default gateway hardcoded
  `10.0.0.1` on printers.
- Merge target: routed link between parent DC and subsidiary edge.
- Security requirement: subsidiary desktop VLAN must not initiate to parent
  HR subnet (NAT alone will be relied on by default — fix that).

## Student Task

1. Propose the **address plan**: which side renumbers (and what to), what
   stays, and why (cost × risk × the printer constraint).
2. Choose **NAT modes** per boundary: where 1:1 (static), where NAPT
   (dynamic PAT), where none — with the *reason* each choice fits its flow.
3. Write the **security commentary**: two concrete flows where NAT alone
   gives false isolation, and what real control replaces it.

## How to Approach This (Reasoning Scaffold)

- Overlap has three cures: renumber one side, NAT the overlap away, or
  tunnel-and-NAT at the boundary — pick per side based on who can change.
- Printers that can't change are a *plan* constraint, not a blocker:
  renumber around them or NAT their subnet's egress explicitly.
- The exam question underneath: NAT changes *reachability*, not
  *authorization* — name the flows where people confuse the two.

## CLO Mapping

- **CLO-3** — Address-plan and NAT architecture with security honesty.

## Safety Notes

- Design exercise; no live renumbering.
