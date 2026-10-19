---

# Contract Review Playbook — Skill Reference

> **NOT LEGAL ADVICE.** This skill produces drafting aids and research notes only. Every output MUST be reviewed, verified, and approved by a licensed attorney in the relevant jurisdiction before it is relied on, sent to a counterparty, or shown to a client.

| Doc type | Playbook file |
|---|---|
| NDA (mutual or one-way) | `./legal_review\playbooks\nda.yaml` |
| MSA / SaaS subscription / vendor services | `./legal_review\playbooks\msa_saas.yaml` |
| Independent contractor / consulting | `./legal_review\playbooks\independent_contractor.yaml` |
| Employment | No seed playbook yet — use `independent_contractor.yaml` restrictive-covenant and IP clauses plus [UNVERIFIED] flags; tell the lead the playbook is missing. |

Same field layout as the lease playbooks: `id`, `heading`, `market`, `red_flags[]`, `fallback`, `walk_away`, `severity_hint`, `tags[]`. Copy `tags` verbatim into findings.

## Procedure
1. Work from the clause map, not the raw document. Quote ≤300 chars of source text per finding.
2. Walk every playbook clause; emit `clause_id: "MISSING"` findings for absent protections (no vendor IP indemnity, no exclusions in an NDA, no pre-existing-IP license, no DTSA notice where an individual signs).
3. Flip positions by `intake.client_side` (customer vs vendor; receiving vs disclosing; company vs contractor).
4. **Interaction checks** (the associate-level catches):
   - LoL cap that excludes the customer's payment obligations but includes the vendor's data-breach liability = asymmetric by construction.
   - Warranty remedy "re-performance only" + LoL cap at 3 months' fees + no termination-for-breach refund = no real remedy.
   - IP clause: WFH-only language for deliverables outside the nine 17 U.S.C. § 101 categories (most software/marketing/consulting deliverables) with no backup "hereby assigns" = company may not own the work.
   - "Agrees to assign" (future promise) ≠ present assignment — flag.
   - Feedback clause phrased as assignment (not license) inside a customer agreement = customer gives away product ideas.
   - Auto-renewal + non-renewal notice window longer than the reminder period (or no reminder) = renewal trap.
   - NDA "Purpose" narrower than the actual business need = every internal discussion is a breach.
   - Non-solicit that covers "any employee" with no prior-contact limiter; no-hire vs no-solicit distinction.
   - Suspension right for "any" late payment + no dispute mechanism = leverage inversion.
   - Terms incorporated by URL that "may be updated from time to time" + order of precedence favoring the URL terms.
   - Misclassification tells in contractor agreements: fixed hours, exclusivity, company equipment, handbook compliance, hourly pay with supervision.
5. Georgia specifics: restrictive covenants under O.C.G.A. § 13-8-50 et seq.; duration presumptions § 13-8-57; blue-pencil § 13-8-54; trade secrets § 10-1-760 et seq.; conspicuous disclaimers § 11-2-316. Anything else → [UNVERIFIED] and hand to legal-jurisdiction-researcher.

## Severity scale
Same 1-5 scale as `lease-review-playbook` (5 walk-away/illegal; 4 serious; 3 material—redline; 2 ask; 1 note).

## Exposure heuristics (feed legal-risk-scorer)
- Uncapped one-way indemnity: use deal value × 3 as planning number, flagged "unbounded".
- Data breach with liability capped at N months' fees: expected breach cost (records × $/record, [UNVERIFIED] benchmark) minus cap.
- Auto-renewal trap: one full renewal term × annual fees.
- IP ownership failure: replacement cost of deliverable + loss of exclusivity — mark "strategic".
- Misclassification: back taxes + penalties; use 30% of annual contractor pay as planning estimate [UNVERIFIED benchmark].

## Output
`finding[]` per `./legal_review\schemas\handoff_schemas.json`.
