"""Repository-level checks that do not require project dependencies."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
DAILY_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")
SPEC_DIRECTORY_PATTERN = re.compile(r"^\d{3}-[a-z0-9]+(?:-[a-z0-9]+)*$")
SPEC_REQUIRED_FILES = ("spec.md", "plan.md", "tasks.md", "decisions.md")
TEAM_MEMBERS = ("José", "Abel", "Víctor", "Miguel")
MAX_TRACKED_SIZE = 10 * 1024 * 1024
IGNORED_LINK_PREFIXES = ("http://", "https://", "mailto:", "#")
FORBIDDEN_TRACKED_NAMES = {".env", "id_rsa", "id_ed25519"}
IGNORED_LOCAL_DIRECTORIES = {
    ".git",
    ".venv",
    "__pycache__",
    "exports",
    "node_modules",
}


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [ROOT / line for line in result.stdout.splitlines() if line]


def repository_files() -> list[Path]:
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and not IGNORED_LOCAL_DIRECTORIES.intersection(path.relative_to(ROOT).parts)
    ]


def check_required_paths(errors: list[str]) -> None:
    required = (
        "README.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "CHANGELOG.md",
        ".specify/README.md",
        ".specify/intent.md",
        "docs/architecture/repository_structure.md",
        "docs/design/documentation_visual_standard.md",
        "docs/notebooklm/source_catalog.md",
        "docs/project_management/dailies/2026-07-22.md",
    )
    for relative in required:
        if not (ROOT / relative).exists():
            errors.append(f"Missing required path: {relative}")


def check_markdown_links(files: list[Path], errors: list[str]) -> None:
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in files:
        if path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        for raw_target in link_pattern.findall(text):
            target = unquote(raw_target.split("#", 1)[0].strip("<>"))
            if not target or target.startswith(IGNORED_LINK_PREFIXES):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(
                    f"Broken Markdown link in {path.relative_to(ROOT)}: {raw_target}"
                )


def check_dailies(errors: list[str]) -> None:
    directory = ROOT / "docs/project_management/dailies"
    if not directory.exists():
        errors.append("Missing dailies directory")
        return
    for path in directory.glob("*.md"):
        if path.name in {"README.md", "_template.md"}:
            continue
        if not DAILY_PATTERN.fullmatch(path.name):
            errors.append(f"Invalid daily filename: {path.name}")
            continue
        text = path.read_text(encoding="utf-8")
        for member in TEAM_MEMBERS:
            if f"## {member}" not in text:
                errors.append(f"Daily {path.name} is missing section for {member}")


def check_spec_bundles(errors: list[str]) -> None:
    directory = ROOT / "specs"
    if not directory.exists():
        errors.append("Missing specs directory")
        return
    for path in directory.iterdir():
        if not path.is_dir():
            continue
        if not SPEC_DIRECTORY_PATTERN.fullmatch(path.name):
            errors.append(f"Invalid spec directory name: {path.name}")
            continue
        for filename in SPEC_REQUIRED_FILES:
            if not (path / filename).is_file():
                errors.append(f"Spec {path.name} is missing {filename}")


def check_tracked_files(files: list[Path], errors: list[str]) -> None:
    for path in files:
        relative = path.relative_to(ROOT)
        if path.name in FORBIDDEN_TRACKED_NAMES:
            errors.append(f"Sensitive filename is tracked: {relative}")
        if path.exists() and path.stat().st_size > MAX_TRACKED_SIZE:
            errors.append(f"Tracked file exceeds 10 MiB: {relative}")


def main() -> int:
    errors: list[str] = []
    files = tracked_files()
    local_files = repository_files()
    check_required_paths(errors)
    check_markdown_links(local_files, errors)
    check_dailies(errors)
    check_spec_bundles(errors)
    check_tracked_files(files or local_files, errors)

    if errors:
        print("Repository quality checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Repository quality checks passed for "
        f"{len(files)} tracked and {len(local_files)} local files."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
