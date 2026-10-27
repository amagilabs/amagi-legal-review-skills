# Goldfish review: README.md

- When: 2026-10-26 21:15
- Spec: `README.md`
- Code: `src\amagi_legal_review_skills`, `pyproject.toml`, `tests`
- Goldfish: 2 x sonnet, each with no tools and no history
- Verdicts: FIX, FIX -> overall FIX

## Goldfish 1

**Scope note:** The spec (README.md) describes the bulk of this product's behavior in terms of files I was not given — `skills/*/SKILL.md`, `agents/*.md`, and `examples/`. I can only verify the installer/CLI logic against the "Install" section of the README; I cannot verify the nine-agent pipeline, playbook content, citation-check rule, or the worked example, because those files weren't provided.

- **medium** — Spec: "`amagi-legal-review-skills install` ... copies the skills into `~/.claude/skills/` and the agents into `~/.claude/agents/`". Code never checks that `bundled()` actually found anything.
  `src/amagi_legal_review_skills/cli.py:64-72` (and `bundled()` at `cli.py:18-33`).
  Scenario: if the installed package is missing its data files (e.g. a wheel built without `package-data`, or `resources.files` resolves to an empty dir), `bundled()` returns `[]`. `main()` still prints `"0 wrote, 0 skipped -> ~/.claude"` and returns exit code `0`. The user sees what looks like a normal, successful run with nothing to skip, and has no indication that zero skills/agents were installed — a silent wrong answer rather than a loud failure.

- **low / unsure** — `tests/test_cli.py:13,16` hardcode `len(written) == 13` (4 skills + 9 agents, one file each), but `pyproject.toml:39` declares `"amagi_legal_review_skills.skills" = ["**/*.md"]` — a recursive glob implying skill folders may ship more than one `.md` file (e.g. reference docs alongside `SKILL.md`). `bundled()` (`cli.py:18-33`) walks every `.md` file recursively, not just `SKILL.md`. If any skill folder ever gains a second markdown file, `bundled()`'s count silently grows past 13 and this test starts failing — not a runtime bug, but a latent coupling between packaging intent and test assumptions I can't confirm is safe without seeing the actual `skills/` tree.

- **low** — Spec doesn't say what happens if `install` is interrupted partway (disk full, permission error mid-loop). `cli.py:install()` (`cli.py:36-47`) has no transactional guarantee: files already written stay written, the function raises an uncaught exception on the failing file, and a rerun will treat already-written files as "already there, skip" (unless `--force`). This is a spec gap rather than a bug — the failure is loud (a traceback), not silent — but worth noting since the README doesn't document resumability.

VERDICT: FIX (medium: 1, low: 2 — one marked unsure)

## Goldfish 2

**Caveat on inputs:** The spec (README.md) makes almost all of its substantive claims about the `agents/*.md` and `skills/*.md` pipeline content (the nine-agent sequence, citation verify-or-flag rule, redline two-variant format, adversarial hallucination checks, sign-off checklist) and about `examples/`. None of those files were included in this review — only the Python packaging/CLI code (`cli.py`, `__init__.py`, `pyproject.toml`, `tests/test_cli.py`) was. So this review can only verify the *installer* mechanics, not the actual legal-review pipeline behavior the README is mostly about.

- **medium** — Spec gap / silent wrong answer: nothing validates that `bundled()` actually found any skills/agents before declaring success.
  `src\amagi_legal_review_skills\cli.py:60-73`
  Scenario: if package-data resolution breaks for any reason (bad wheel build, missing `__init__.py` for the `skills`/`agents` sub-packages, namespace-package resolution returning zero children, etc.), `bundled()` silently returns `[]`. `list` then prints nothing and exits 0; `install` prints `"0 wrote, 0 skipped -> ~/.claude"` and exits 0 — looking like a clean, complete install while nothing was actually installed. The README's "That copies the skills... list shows what is bundled" promise is silently unmet with no error signal.

- **low** — Spec gap: path-type collision isn't handled.
  `src\amagi_legal_review_skills\cli.py:40-46`
  Scenario: if `target` (e.g. `~/.claude/agents/legal-review-lead.md`) already exists as a *directory* (or an existing file blocks creation of a needed parent directory), `target.write_text(...)` / `target.parent.mkdir(...)` raises an unhandled `OSError`/`IsADirectoryError`, crashing with a raw traceback instead of the skip/force behavior the README describes. Unlikely in practice, but the spec never addresses it.

- **low / unsure** — Spec gap: no handling for a broken/incomplete Claude Code install environment (permission errors on `~/.claude`, read-only filesystem) — results in a raw exception rather than a friendly message. Not explicitly promised by the spec either way, so this is a minor gap rather than a contradiction.

What checks out: the skip-unless-`--force` logic, the true no-write dry run (verified against `tests\test_cli.py:19-27`), the `--dest` override, and the `list` output all faithfully match the README's "Install" section, and the file-count math (4 skills + 9 agents = 13) is internally consistent between README, code, and tests.

VERDICT: FIX (0 high, 1 medium, 2 low)
