"""Copy the bundled skills and agents into a Claude Code config folder.

    amagi-legal-review-skills list
    amagi-legal-review-skills install [--dest ~/.claude] [--force] [--dry-run]

Existing files are left alone unless --force is given.
"""
from __future__ import annotations

import argparse
import sys
from importlib import resources
from pathlib import Path

PKG = "amagi_legal_review_skills"


def bundled() -> list[tuple[str, str]]:
    """(relative destination path, file text) for every bundled skill and agent."""
    out: list[tuple[str, str]] = []
    for kind in ("skills", "agents"):
        root = resources.files(f"{PKG}.{kind}")
        stack = [(root, kind)]
        while stack:
            node, rel = stack.pop()
            for child in node.iterdir():
                if child.name.startswith(("__", ".")):
                    continue
                if child.is_dir():
                    stack.append((child, f"{rel}/{child.name}"))
                elif child.name.endswith(".md"):
                    out.append((f"{rel}/{child.name}", child.read_text(encoding="utf-8")))
    return sorted(out)


def install(dest: Path, force: bool = False, dry_run: bool = False) -> tuple[list[str], list[str]]:
    written, skipped = [], []
    for rel, text in bundled():
        target = dest / rel
        if target.exists() and not force:
            skipped.append(rel)
            continue
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
        written.append(rel)
    return written, skipped


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="amagi-legal-review-skills",
                                 description="Install the AmagiLabs legal review skills and agents into Claude Code. Output is not legal advice.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="show bundled skills and agents")
    p = sub.add_parser("install", help="copy skills and agents into a Claude Code folder")
    p.add_argument("--dest", default=str(Path.home() / ".claude"), help="Claude Code config folder (default ~/.claude)")
    p.add_argument("--force", action="store_true", help="overwrite files that already exist")
    p.add_argument("--dry-run", action="store_true", help="print what would be written, write nothing")
    a = ap.parse_args(argv)
    if not bundled():
        print("error: no bundled skills or agents found; the package install looks broken. "
              "Reinstall with pipx install --force amagi-legal-review-skills.", file=sys.stderr)
        return 1
    if a.cmd == "list":
        for rel, _ in bundled():
            print(rel)
        return 0
    written, skipped = install(Path(a.dest).expanduser(), a.force, a.dry_run)
    verb = "would write" if a.dry_run else "wrote"
    for rel in written:
        print(f"{verb} {rel}")
    for rel in skipped:
        print(f"skipped {rel} (exists; use --force)")
    print(f"{len(written)} {verb}, {len(skipped)} skipped -> {a.dest}")
    if written and not a.dry_run:
        print("Restart Claude Code so it picks up the new skills and agents.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
