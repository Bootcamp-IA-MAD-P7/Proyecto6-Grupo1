"""Build a safe, task-scoped context pack for an AI assistant."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIRECTORY = ROOT / "exports" / "ai-handoffs"
COMMON_SOURCES = (
    "AGENTS.md",
    "README.md",
    "CONTRIBUTING.md",
    ".specify/README.md",
    ".specify/intent.md",
    "docs/project_management/delivery_levels.md",
)
SPEC_FILES = ("spec.md", "plan.md", "tasks.md", "decisions.md")
ALLOWED_SUFFIXES = {".md", ".json", ".yml", ".yaml", ".txt"}
FORBIDDEN_SOURCE_PREFIXES = ("data/", "models/", "notebooks/", "exports/", "logs/", "tmp/")
MAX_SOURCE_BYTES = 1024 * 1024
TASK_PATTERN = re.compile(r"^## (T-\d{3})\b", re.MULTILINE)
JSON_CONTRACT_REFERENCE_PATTERN = re.compile(
    r"(?<![\w/])((?:config|docs/api)/[A-Za-z0-9_./-]+\.json)"
)


class HandoffError(RuntimeError):
    """Raised when a safe handoff pack cannot be built."""


def tracked_paths() -> set[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return {line.replace("\\", "/") for line in result.stdout.splitlines() if line}


def resolve_spec(value: str) -> Path:
    specs = ROOT / "specs"
    exact = specs / value
    if exact.is_dir():
        return exact

    matches = sorted(path for path in specs.glob(f"{value}*") if path.is_dir())
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise HandoffError(f"Spec not found: {value}")
    raise HandoffError(f"Spec prefix is ambiguous: {value}")


def normalized_task(value: str) -> str:
    candidate = value.upper()
    if not re.fullmatch(r"T-\d{3}", candidate):
        raise HandoffError("Task must use format T-NNN")
    return candidate


def safe_source(relative: str, tracked: set[str]) -> Path:
    normalized = relative.replace("\\", "/")
    candidate = (ROOT / normalized).resolve()
    try:
        candidate.relative_to(ROOT)
    except ValueError as exc:
        raise HandoffError(f"Source is outside the repository: {relative}") from exc

    repository_relative = candidate.relative_to(ROOT).as_posix()
    if repository_relative not in tracked:
        raise HandoffError(f"Source is not tracked by Git: {repository_relative}")
    if repository_relative.startswith(FORBIDDEN_SOURCE_PREFIXES):
        raise HandoffError(f"Source area is not allowed: {repository_relative}")
    if candidate.suffix.lower() not in ALLOWED_SUFFIXES:
        raise HandoffError(f"Source format is not allowed: {repository_relative}")
    if candidate.stat().st_size > MAX_SOURCE_BYTES:
        raise HandoffError(f"Source exceeds 1 MiB: {repository_relative}")
    return candidate


def source_paths(spec: Path, task: str, includes: list[str]) -> list[Path]:
    tracked = tracked_paths()
    paths = [safe_source(relative, tracked) for relative in COMMON_SOURCES]
    spec_paths = [safe_source((spec / name).relative_to(ROOT).as_posix(), tracked) for name in SPEC_FILES]

    tasks_text = (spec / "tasks.md").read_text(encoding="utf-8")
    available_tasks = set(TASK_PATTERN.findall(tasks_text))
    if task not in available_tasks:
        raise HandoffError(f"Task {task} does not exist in {spec.name}/tasks.md")

    paths.extend(spec_paths)
    bundle_text = "\n".join(path.read_text(encoding="utf-8") for path in spec_paths)
    for reference in sorted(set(JSON_CONTRACT_REFERENCE_PATTERN.findall(bundle_text))):
        paths.append(safe_source(reference, tracked))
    paths.extend(safe_source(relative, tracked) for relative in includes)
    return list(dict.fromkeys(paths))


def build_handoff(
    spec_value: str,
    task_value: str,
    includes: list[str] | None = None,
    output_directory: Path = OUTPUT_DIRECTORY,
    *,
    title: str | None = None,
    instruction_lines: Sequence[str] | None = None,
    output_filename: str | None = None,
) -> Path:
    spec = resolve_spec(spec_value)
    task = normalized_task(task_value)
    sources = source_paths(spec, task, includes or [])
    output_directory.mkdir(parents=True, exist_ok=True)
    filename = output_filename or f"{spec.name}-{task}.md"
    if Path(filename).name != filename or not re.fullmatch(r"[A-Za-z0-9_.-]+\.md", filename):
        raise HandoffError("Output filename must be a safe Markdown filename")
    output = output_directory / filename
    instructions = list(
        instruction_lines
        or (
            f"Work only on {task} from spec {spec.name}.",
            "Use the attached sources as the project contract.",
            "Before editing, summarize scope, planned files and blockers.",
            "Do not expand scope or present pending capabilities as implemented.",
            "At closure, report changed files, checks, decisions and remaining risks.",
        )
    )

    lines = [
        title or f"# AI handoff — {spec.name} / {task}",
        "",
        "> Generated from tracked project sources. Review before sharing.",
        "> Never attach datasets, secrets or real CFPB narratives.",
        "",
        "## Suggested instruction",
        "",
        "```text",
    ]
    lines.extend(instructions)
    lines.extend(("```", "", "## Source index", ""))
    lines.extend(f"- `{path.relative_to(ROOT).as_posix()}`" for path in sources)

    for path in sources:
        relative = path.relative_to(ROOT).as_posix()
        content = path.read_text(encoding="utf-8").strip()
        lines.extend(("", "---", "", f"## Source: `{relative}`", "", content))

    output.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True, help="Spec directory name or unique prefix")
    parser.add_argument("--task", required=True, help="Task identifier in format T-NNN")
    parser.add_argument(
        "--include",
        action="append",
        default=[],
        help="Additional tracked documentation source; repeat as needed",
    )
    args = parser.parse_args()

    try:
        output = build_handoff(args.spec, args.task, args.include)
    except (HandoffError, OSError, subprocess.CalledProcessError) as exc:
        print(f"Cannot build AI handoff: {exc}", file=sys.stderr)
        return 1

    print(output.relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    sys.exit(main())
