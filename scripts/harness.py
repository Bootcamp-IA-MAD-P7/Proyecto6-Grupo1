"""Compose a safe, role-aware task pack for any Markdown-capable AI."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.documentation.build_ai_handoff import (
    HandoffError,
    OUTPUT_DIRECTORY,
    ROOT,
    build_handoff,
    normalized_task,
    resolve_spec,
)


ACTION_SKILLS = {
    "start": "start-task",
    "verify": "verify-task",
    "review": "review-change",
    "prepare-pr": "prepare-pr",
}
ACTION_LABELS = {
    "start": "Start task",
    "verify": "Verify task",
    "review": "Review change",
    "prepare-pr": "Prepare pull request",
}
ROLE_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TASK_HEADING_PATTERN = re.compile(r"^## (T-\d{3})\b", re.MULTILINE)
TASK_STATE_PATTERN = re.compile(r"^- Estado:\s*`(\[[ x~!\-]\])`", re.MULTILINE)
STARTABLE_STATES = {"[ ]", "[~]"}
REVIEWABLE_STATES = {"[ ]", "[~]", "[x]"}


class HarnessError(RuntimeError):
    """Raised when the requested harness workflow is invalid."""


def normalize_action(value: str) -> str:
    action = value.lower()
    if action not in ACTION_SKILLS:
        choices = ", ".join(ACTION_SKILLS)
        raise HarnessError(f"Unknown action {value!r}. Choose one of: {choices}")
    return action


def resolve_role(value: str) -> Path:
    role = value.lower()
    if not ROLE_PATTERN.fullmatch(role):
        raise HarnessError("Role must use lowercase hyphen-case")
    path = ROOT / "ai-specs" / "agents" / f"{role}.md"
    if not path.is_file():
        raise HarnessError(f"Unknown role: {role}")
    return path


def task_state(spec: Path, task: str) -> str:
    tasks_path = spec / "tasks.md"
    text = tasks_path.read_text(encoding="utf-8")
    headings = list(TASK_HEADING_PATTERN.finditer(text))
    for index, match in enumerate(headings):
        if match.group(1) != task:
            continue
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        section = text[match.start() : end]
        state_match = TASK_STATE_PATTERN.search(section)
        if not state_match:
            raise HarnessError(f"Task {task} has no valid Estado field")
        return state_match.group(1)
    raise HarnessError(f"Task {task} does not exist in {spec.name}/tasks.md")


def validate_task_action(action: str, spec: Path, task: str) -> str:
    state = task_state(spec, task)
    if state == "[!]":
        raise HarnessError(f"Task {task} is blocked and cannot run action {action}")
    if state == "[-]":
        raise HarnessError(f"Task {task} is discarded and cannot run action {action}")
    if action == "start" and state not in STARTABLE_STATES:
        raise HarnessError(f"Task {task} has state {state} and cannot be started")
    if action in {"verify", "review"} and state not in REVIEWABLE_STATES:
        raise HarnessError(f"Task {task} has state {state} and cannot be {action}ed")
    if action == "prepare-pr" and state != "[x]":
        raise HarnessError(f"Task {task} must be completed before preparing a pull request")
    return state


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def build_harness_pack(
    action_value: str,
    role_value: str,
    spec_value: str,
    task_value: str,
    includes: list[str] | None = None,
    output_directory: Path = OUTPUT_DIRECTORY,
) -> Path:
    action = normalize_action(action_value)
    role_path = resolve_role(role_value)
    spec = resolve_spec(spec_value)
    task = normalized_task(task_value)
    state = validate_task_action(action, spec, task)
    skill_path = ROOT / "ai-specs" / "skills" / ACTION_SKILLS[action] / "SKILL.md"
    if not skill_path.is_file():
        raise HarnessError(f"Workflow definition not found: {relative(skill_path)}")

    role = role_path.stem
    extra_sources = [relative(role_path), relative(skill_path), *(includes or [])]
    filename = f"harness-{action}-{role}-{spec.name}-{task}.md"
    instructions = (
        f"Adopt the role defined in {relative(role_path)}.",
        f"Follow the workflow in {relative(skill_path)}.",
        f"Work only on {task} from spec {spec.name}, currently in state {state}.",
        "Treat AGENTS.md, the spec bundle and referenced contracts as authoritative.",
        "Before changing files, explain scope, planned files, blockers and checks.",
        "Do not invent decisions, evidence or implemented capabilities.",
        "Keep datasets, secrets and real CFPB narratives out of prompts and outputs.",
        "Human review is required before commit, push, pull request or merge.",
    )

    return build_handoff(
        spec.name,
        task,
        extra_sources,
        output_directory,
        title=f"# Harness pack — {ACTION_LABELS[action]} / {role} / {spec.name} / {task}",
        instruction_lines=instructions,
        output_filename=filename,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a safe role, workflow, spec and task pack for an AI assistant."
    )
    parser.add_argument("action", choices=tuple(ACTION_SKILLS))
    parser.add_argument("--role", required=True, help="Role name from ai-specs/agents")
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
        output = build_harness_pack(
            args.action,
            args.role,
            args.spec,
            args.task,
            args.include,
        )
    except (HarnessError, HandoffError, OSError, subprocess.CalledProcessError) as exc:
        print(f"Cannot build harness pack: {exc}", file=sys.stderr)
        return 1

    print(output.relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    sys.exit(main())
