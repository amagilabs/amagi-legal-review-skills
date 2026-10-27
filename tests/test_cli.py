from amagi_legal_review_skills import cli


def test_bundled_has_all_skills_and_agents():
    rels = [r for r, _ in cli.bundled()]
    assert sum(r.startswith("skills/") and r.endswith("/SKILL.md") for r in rels) == 4
    assert sum(r.startswith("agents/") for r in rels) == 9
    assert "agents/legal-review-lead.md" in rels


def test_install_writes_then_skips(tmp_path):
    written, skipped = cli.install(tmp_path)
    assert len(written) == 13 and not skipped
    assert (tmp_path / "skills" / "redline-format" / "SKILL.md").is_file()
    written2, skipped2 = cli.install(tmp_path)
    assert not written2 and len(skipped2) == 13


def test_force_overwrites_and_dry_run_writes_nothing(tmp_path):
    target = tmp_path / "agents" / "legal-review-lead.md"
    target.parent.mkdir(parents=True)
    target.write_text("old", encoding="utf-8")
    cli.install(tmp_path, force=True)
    assert target.read_text(encoding="utf-8") != "old"
    dry = tmp_path / "dry"
    written, _ = cli.install(dry, dry_run=True)
    assert written and not dry.exists()


def test_main_list(capsys):
    assert cli.main(["list"]) == 0
    assert "agents/legal-review-lead.md" in capsys.readouterr().out


def test_main_fails_loudly_when_nothing_is_bundled(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(cli, "bundled", lambda: [])
    assert cli.main(["install", "--dest", str(tmp_path)]) == 1
    assert "no bundled skills" in capsys.readouterr().err
    assert not any(tmp_path.iterdir())
