---

# Lease Review Playbook — Skill Reference

> **NOT LEGAL ADVICE.** This skill produces drafting aids and research notes only. Every output MUST be reviewed, verified, and approved by a licensed attorney in the relevant jurisdiction before it is relied on, sent to a counterparty, or shown to a client.

Knowledge lives in YAML, not here. Load the right file and follow the procedure.

| Doc type | Playbook file |
|---|---|
| Commercial lease (office/retail/industrial) | `./legal_review\playbooks\commercial_lease.yaml` |
| Residential lease, Georgia | `./legal_review\playbooks\residential_lease_ga.yaml` |

Each playbook clause has: `id`, `heading`, `market`, `red_flags[]`, `fallback`, optional `walk_away`, `severity_hint`, `tags[]`.
`tags` are the eval-matching keys — copy them verbatim into `finding.tags`.

## Procedure (playbook-checker pass)
1. Read the clause map JSON (from legal-clause-extractor). Do not re-read the raw document unless a clause's text is truncated.
2. For EVERY playbook clause id, find the matching clause(s) in the map by heading/keyword. If none exists, emit a finding with `clause_id: "MISSING"` and `playbook_clause` set — a missing SNDA, missing audit right, or missing flooding disclosure is an issue.
3. For each red flag, quote the exact source text (≤300 chars) that triggers it. No quote = no finding.
4. Assign severity 1-5 using the scale below, adjusted for the client's side (`intake.client_side`). A tenant-side red flag is not a landlord-side red flag — flip.
5. Check for **interaction issues** the YAML can't express line by line (these are the ones a mid-level associate catches and a checklist misses):
   - Deposit + acceleration + reletting-without-credit = triple recovery.
   - Holdover consequential damages + no early-delivery/late-delivery symmetry.
   - Renewal option voided by "any prior default" + a late-fee clause with no grace = illusory option.
   - Relocation right + exclusive use = exclusive is meaningless.
   - Permitted-transfer carve-out missing + change-of-control trigger + personal guaranty surviving assignment.
   - "Additional rent" definition that sweeps late fees/attorney fees into rent so nonpayment of a fee supports eviction.
   - Cross-references to exhibits/sections that don't exist in the document.
6. Residential GA: any clause that waives O.C.G.A. § 44-7-13 repair duty, the deposit article, or § 44-7-20 flooding disclosure is void under § 44-7-2(b) — flag at severity 5 and say "void, but signals landlord posture".

## Severity scale
| Sev | Meaning | Action |
|---|---|---|
| 5 | Walk-away or illegal/void term; exposure ≥ 12 months' rent or personal assets | Must fix or decline |
| 4 | Serious economic or control risk; exposure 3-12 months' rent | Must redline |
| 3 | Material deviation from market; redline required | Redline |
| 2 | Minor; ask, don't fight | Ask once |
| 1 | Cosmetic / drafting | Note only |

## Exposure heuristics (feed legal-risk-scorer)
- Acceleration undiscounted: remaining months × monthly rent.
- CAM without cap: 5-8%/yr growth on current CAM × term.
- Holdover at 200%: 1 extra month's rent × 2 as planning estimate.
- Personal guaranty unlimited: full remaining rent obligation, marked "personal assets at risk".
- GA deposit bad-faith retention: 3× deposit (O.C.G.A. § 44-7-35) — landlord-side exposure.

## Output
Emit `finding[]` per `./legal_review\schemas\handoff_schemas.json`. Every finding carries `clause_id`, `page`, `line_start`, `source_quote`, `tags`, `severity`, and every legal claim carries `cite` or `[UNVERIFIED]`.
