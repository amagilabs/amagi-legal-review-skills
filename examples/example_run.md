# Worked example: contract-review-playbook on a sample NDA

> This example is illustrative only. It shows the shape of the output, not a
> substitute for an attorney's review of any real agreement.

**Input:** `examples/sample_nda.txt` — a fictional mutual NDA between two invented
companies, Brightfield Robotics, Inc. and Cobalt Meridian Logistics LLC.

**Skill invoked:** `contract-review-playbook` (NDA row), following the procedure in
`skills/contract-review-playbook/SKILL.md`. In a full pipeline this is called by the
`legal-review-lead` agent, which first runs `legal-clause-extractor` to build a clause
map, then `legal-playbook-checker` to apply the playbook, then `redline-format` for
replacement language.

## Illustrative findings

| Clause | Issue | Severity | Why it matters |
|---|---|---|---|
| §6 Remedies | Indemnity is one-directional ("the Receiving Party shall indemnify...") and uncapped ("without limitation") | 4 | In a *mutual* NDA, an indemnity obligation that runs only one way is asymmetric by construction — the playbook's interaction check for one-way indemnities inside a nominally mutual agreement. Planning exposure: deal value x 3 (here, no deal value stated, so flag as [UNVERIFIED] pending client input). |
| §3 Obligations | No carve-out for information independently known to employees via general industry knowledge / residuals | 2 | Minor; common ask, not a dealbreaker. |
| §1 Purpose | "warehouse automation hardware integration" is reasonably specific | 1 | Note only — Purpose is not drafted so broadly that ordinary business discussion would breach it. |
| (missing) | No governing-law-aligned trade secret notice (e.g., DTSA whistleblower immunity notice, 18 U.S.C. § 1833(b)) | 3 | `clause_id: "MISSING"` — routed to `legal-jurisdiction-researcher` for a jurisdiction-specific citation check before it ships as a finding. |
| §4 Term | 1-year term with 3-year survival on confidentiality is within market range | 1 | Note only. |

## Example redline (severity >= 3 clause, §6)

Using the `redline-format` skill's two-variant convention:

```
The Receiving Party shall indemnify the Disclosing Party for any and all losses,
damages, costs, and expenses arising from any breach of this Agreement[-, without
limitation-]{+, up to a cap of [$ amount / multiple of fees], except in cases of
willful misconduct or bad-faith disclosure+}. {+Each Party's indemnification
obligations under this Section shall apply equally to breaches by the other Party.+}
```

- `client_friendly`: adds a cap and makes the obligation mutual (opening ask).
- `counterparty_friendly`: keeps counterparty's structure, adds only the cap (fallback).

## Output package (what `legal-review-lead` would assemble)

In a full run, the orchestrator agent would produce `clause_map.json`,
`findings.json`, `risk_matrix.json`, `redlines.json`, `negotiation_plan.json`,
`client_memo.md`, and an `adversarial_report.json`, bundled into a single
`REVIEW.md` with a sign-off checklist — all gated on human attorney review.
This example shows only the first layer (playbook findings + one redline) to
illustrate how the skill reasons about a document; it does not include the
full multi-agent pipeline output.

---

**Reminder:** every finding above is illustrative output from an AI skill, not
legal advice. No redline, finding, or risk score from this pack should be sent
to a counterparty or relied on by a client until a licensed attorney in the
relevant jurisdiction has reviewed it.
