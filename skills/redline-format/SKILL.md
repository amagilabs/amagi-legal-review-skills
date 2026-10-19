---

# Redline Format — Skill Reference

> **NOT LEGAL ADVICE.** This skill produces drafting aids and research notes only. Every output MUST be reviewed, verified, and approved by a licensed attorney in the relevant jurisdiction before it is relied on, sent to a counterparty, or shown to a client.

## Inline diff markup (plain text, survives email and Word paste)
- Deletion: `[-deleted text-]`
- Insertion: `{+inserted text+}`
- Unchanged text is reproduced verbatim. Never paraphrase the original; the attorney must be able to paste this over the source.
- Keep the counterparty's numbering and defined-term capitalization. If you introduce a new defined term, add it to `drafting_notes` with the clause where it should be defined.

Example:
```
Landlord may withhold consent to any assignment [-in its sole and absolute discretion-]{+, which consent shall not be unreasonably withheld, conditioned or delayed+}. {+Notwithstanding the foregoing, Tenant may, without Landlord's consent but with prior written notice, assign this Lease or sublet the Premises to a Permitted Transferee.+}
```

## Two variants, always
| Variant | Purpose | Drafting posture |
|---|---|---|
| `client_friendly` | Opening ask | Full market position from the playbook `market` field. Clean, not greedy — an ask a mid-level associate would send without embarrassment. |
| `counterparty_friendly` | Fallback we can live with | Playbook `fallback` field. Must still remove the walk-away. Written so the other side can accept it without losing face (keeps their structure, adds a limiter). |

Both variants must be **complete replacement language** — no "[insert reasonable cure period]" placeholders. Pick a number and flag it in `drafting_notes` if it's a business call.

## Rules
1. One redline per finding with severity ≥ 3. Severity 1-2: `drafting_notes` only, no redline, unless the fix is a one-word change.
2. Never change a clause the finding didn't cite. If the fix requires touching another clause (e.g., adding a defined term, fixing a cross-reference), list it under `drafting_notes.also_touch[]` — do not silently redline it.
3. Every redline must resolve to a `clause_id` that exists in the clause map, with `original_text` verbatim from the map.
4. Do not add legal claims in `rationale` beyond what the finding's `legal_basis` already carries. If you need a new legal proposition, mark it `[UNVERIFIED]` and it goes back to legal-jurisdiction-researcher.
5. Preserve mutuality where the fix is "make it mutual" — draft the mutual version, don't just delete the one-way clause.
6. Georgia residential: do not draft language that purports to waive O.C.G.A. § 44-7-2(b) protections even in the counterparty-friendly variant.

## JSON emit (per `schemas/handoff_schemas.json` → `redline`)
```json
{
  "finding_id": "F-007",
  "clause_id": "§14.2",
  "original_text": "...verbatim...",
  "client_friendly": {"replacement_text": "...", "diff": "...[-..-]{+..+}...", "rationale": "..."},
  "counterparty_friendly": {"replacement_text": "...", "diff": "...", "rationale": "..."},
  "drafting_notes": {"also_touch": ["§1 Definitions — add 'Permitted Transferee'"], "business_calls": ["cure period 10 vs 15 days"]}
}
```

## Template: cover note for the redline package (attorney sends, not the agent)
```
Attached are our proposed revisions to the [Document]. The changes are limited to [n] sections and are
intended to bring the agreement in line with market terms for [deal type]. We are happy to discuss any of them.
```
