---

# Legal Citation Check — Skill Reference

> **NOT LEGAL ADVICE.** This skill produces drafting aids and research notes only. Every output MUST be reviewed, verified, and approved by a licensed attorney in the relevant jurisdiction before it is relied on, sent to a counterparty, or shown to a client.

## Zero-tolerance rule
A citation is either **verified** (resolved against a primary source or the curated allowlist) or **[UNVERIFIED]**. There is no third state. A finding may ship with `[UNVERIFIED]` (the attorney sees it); a finding may never ship with a confident-looking cite that nobody checked.

## Allowlist
`./legal_review\eval\citations_allowlist.json` — curated list with `confidence` field.
- `high`: scaffold author is confident of section + topic. Still verify on first client use.
- `verify` / `verify-*`: known to exist in substance, section number or current status uncertain. Treat as `[UNVERIFIED]` until legal-jurisdiction-researcher confirms with a source URL.
- Not in list → `[UNVERIFIED]` until confirmed; then add to the allowlist with the source URL and date.

## Citation normalization (so allowlist matching works; mirrors `run_eval.py`)
- Strip subsection suffixes for matching: `O.C.G.A. § 44-7-34(a)` → `O.C.G.A. § 44-7-34`.
- Normalize whitespace and `§`/`Sec.`/`Section` → `§`.
- `et seq.` matches the starting section.
- Case cites match on `Party v. Party` plus court/year.

## Verification procedure (legal-jurisdiction-researcher)
1. For each `legal_basis[].cite`, search primary sources first: state legislature site (GA: `legis.ga.gov`; FL: `leg.state.fl.us`), `law.cornell.edu`, `govinfo.gov`, `ecfr.gov`, court opinions on `courtlistener.com` or the court's site. Secondary sources (law-firm alerts, Justia annotations) are corroboration only.
2. Confirm THREE things: the section exists, it says what the claim says, and it is current (check amendment year; Georgia's Safe at Home Act 2024 changed landlord-tenant sections).
3. Record `{"cite", "claim", "status": "verified|[UNVERIFIED]", "source_url", "checked_on": "YYYY-MM-DD", "note"}`.
4. If the claim is right but the section is wrong, fix the section and say so — do not silently accept.
5. If you cannot reach a primary source (WebFetch blocked, paywalled), status stays `[UNVERIFIED]` with `note: "could not reach primary source"`.

## Clause-reference resolution (legal-adversarial-reviewer)
1. Load `clause_map.json`. Build the set of `clause_id`s.
2. For every `finding.clause_id`, `redline.clause_id`, and every `§`-style reference inside memo text: must be in the set, or be the literal `MISSING` (with `playbook_clause` populated).
3. For every `finding.source_quote`: must appear verbatim (whitespace-normalized) in the clause's `text`. A quote that isn't in the document is a hallucination — fail the run.
4. Cross-references inside the source document itself (e.g., "as defined in Section 22") that point to nonexistent sections are a **finding**, not a failure.

## Fail conditions (run does not reach the client)
- Any cite not in allowlist and not tagged `[UNVERIFIED]`.
- Any `clause_id` that does not resolve.
- Any `source_quote` not found in the source.
- Memo contradicts the risk matrix (e.g., memo says "low risk" while a severity-5 finding exists).
- Disclaimer line missing.

## Disclaimer (verbatim, required in every client-facing artifact)
`Not legal advice; requires review by a licensed attorney in [jurisdiction].`
