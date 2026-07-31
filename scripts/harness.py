"""Compose a safe, role-aware task pack for any Markdown-capable AI."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

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
    safe_source,
    tracked_paths,
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
CHANGE_PATTERN = ROLE_PATTERN
JIRA_KEY_PATTERN = re.compile(r"^PG-[1-9]\d*$")
JIRA_EXCEPTIONS = {"automation", "bootstrap", "emergency"}
JIRA_BROWSE_URL = "https://miguel-redondo.atlassian.net/browse"
LEGACY_JIRA_MAP = {
    ("001-cfpb-target-contract", "T-004"): "PG-2",
    ("003-complaint-routing-experience", "T-006"): "PG-4",
    ("003-complaint-routing-experience", "T-007"): "PG-5",
}
TASK_HEADING_PATTERN = re.compile(r"^## (T-\d{3})\b", re.MULTILINE)
TASK_STATE_PATTERN = re.compile(r"^- Estado:\s*`(\[[ x~!\-]\])`", re.MULTILINE)
STARTABLE_STATES = {"[ ]", "[~]"}
REVIEWABLE_STATES = {"[ ]", "[~]", "[x]"}
MINIMUM_NODE_VERSION = (20, 19, 0)
OPENSPEC_ENTRYPOINT = (
    ROOT / "node_modules" / "@fission-ai" / "openspec" / "bin" / "openspec.js"
)
OPENSPEC_CONFIG = ROOT / "openspec" / "config.yaml"
OpenSpecRunner = Callable[[tuple[str, ...]], dict[str, Any]]


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


def node_executable() -> str:
    executable = shutil.which("node")
    if not executable:
        raise HarnessError(
            "Node.js is not available. Install Node.js 20.19.0 or newer."
        )
    return executable


def node_version() -> tuple[int, int, int]:
    result = subprocess.run(
        [node_executable(), "--version"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    match = re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)", result.stdout.strip())
    if not match:
        raise HarnessError(f"Cannot parse Node.js version: {result.stdout.strip()}")
    version = tuple(int(part) for part in match.groups())
    if version < MINIMUM_NODE_VERSION:
        required = ".".join(str(part) for part in MINIMUM_NODE_VERSION)
        found = ".".join(str(part) for part in version)
        raise HarnessError(f"Node.js {required} or newer is required; found {found}")
    return version


def openspec_command(*arguments: str) -> list[str]:
    node_version()
    if not OPENSPEC_ENTRYPOINT.is_file():
        raise HarnessError(
            "OpenSpec is not installed locally. Run `npm ci` from the repository root."
        )
    if not OPENSPEC_CONFIG.is_file():
        raise HarnessError("OpenSpec is not initialized: openspec/config.yaml is missing")
    return [node_executable(), str(OPENSPEC_ENTRYPOINT), *arguments]


def run_openspec_text(*arguments: str) -> str:
    environment = os.environ.copy()
    environment["OPENSPEC_TELEMETRY"] = "0"
    result = subprocess.run(
        openspec_command(*arguments),
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=environment,
    )
    return result.stdout.strip()


def run_openspec_json(arguments: tuple[str, ...]) -> dict[str, Any]:
    output = run_openspec_text(*arguments)
    try:
        parsed = json.loads(output)
    except json.JSONDecodeError as exc:
        raise HarnessError("OpenSpec returned invalid JSON") from exc
    if not isinstance(parsed, dict):
        raise HarnessError("OpenSpec returned an unexpected JSON document")
    return parsed


def doctor_report() -> tuple[bool, list[str]]:
    lines: list[str] = []
    try:
        version = node_version()
        lines.append(f"PASS Node.js {'.'.join(str(part) for part in version)}")
        if not OPENSPEC_ENTRYPOINT.is_file():
            raise HarnessError(
                "OpenSpec is not installed locally. Run `npm ci` from the repository root."
            )
        openspec_version = run_openspec_text("--version")
        lines.append(f"PASS OpenSpec {openspec_version}")
        doctor = run_openspec_text("doctor")
        if "OpenSpec root: ok" not in doctor:
            raise HarnessError("OpenSpec doctor did not confirm the project root")
        lines.append("PASS OpenSpec project root")
        validation = run_openspec_json(
            ("validate", "--all", "--strict", "--no-interactive", "--json")
        )
        failed = validation.get("summary", {}).get("totals", {}).get("failed")
        if failed != 0:
            raise HarnessError(f"OpenSpec strict validation reports {failed} failure(s)")
        total = validation.get("summary", {}).get("totals", {}).get("items", 0)
        lines.append(f"PASS OpenSpec strict validation ({total} item(s))")
    except (HarnessError, OSError, subprocess.CalledProcessError) as exc:
        lines.append(f"FAIL {exc}")
        return False, lines
    return True, lines


def normalize_change(value: str) -> str:
    change = value.lower()
    if not CHANGE_PATTERN.fullmatch(change):
        raise HarnessError("OpenSpec change must use lowercase hyphen-case")
    return change


def resolve_jira_tracking(
    jira: str | None,
    jira_exception: str | None,
    *,
    required: bool,
) -> tuple[str | None, str | None]:
    if jira and jira_exception:
        raise HarnessError("--jira and --jira-exception cannot be combined")
    if jira:
        if not JIRA_KEY_PATTERN.fullmatch(jira):
            raise HarnessError("Jira key must use format PG-N, for example PG-12")
        return jira, None
    if jira_exception:
        if jira_exception not in JIRA_EXCEPTIONS:
            choices = ", ".join(sorted(JIRA_EXCEPTIONS))
            raise HarnessError(f"Jira exception must be one of: {choices}")
        return None, jira_exception
    if required:
        raise HarnessError(
            "OpenSpec work requires --jira PG-N or "
            "--jira-exception bootstrap|emergency|automation"
        )
    return None, None


def jira_tracking_lines(
    jira: str | None,
    jira_exception: str | None,
) -> list[str]:
    if jira:
        return [
            f"- Jira work item: [{jira}]({JIRA_BROWSE_URL}/{jira})",
            "- Jira stores owner, status and blockers; OpenSpec remains authoritative.",
        ]
    if jira_exception:
        return [
            f"- Jira exception: `{jira_exception}`",
            "- The exception must be justified in the OpenSpec proposal and Pull Request.",
        ]
    return [
        "- Jira work item: legacy compatibility without an assigned Jira item.",
    ]


def openspec_context_source(value: str) -> str:
    normalized = value.replace("\\", "/")
    is_windows_absolute = bool(
        re.match(r"^[A-Za-z]:/", normalized)
    ) or normalized.startswith("//")
    if is_windows_absolute:
        marker = "/openspec/"
        marker_index = normalized.lower().find(marker)
        if marker_index == -1:
            raise HarnessError("OpenSpec referenced a file outside the repository")
        return normalized[marker_index + 1 :]

    candidate = Path(value).resolve()
    try:
        return candidate.relative_to(ROOT).as_posix()
    except ValueError as exc:
        raise HarnessError(
            "OpenSpec referenced a file outside the repository"
        ) from exc


def _openspec_sources(
    instructions: dict[str, Any],
    role_path: Path,
    skill_path: Path,
    includes: list[str],
) -> list[Path]:
    tracked = tracked_paths()
    requested = [
        *COMMON_OPENSPEC_SOURCES,
        relative(role_path),
        relative(skill_path),
        relative(OPENSPEC_CONFIG),
    ]
    context_files = instructions.get("contextFiles", {})
    if not isinstance(context_files, dict):
        raise HarnessError("OpenSpec instructions contain invalid contextFiles")
    for values in context_files.values():
        if not isinstance(values, list):
            raise HarnessError("OpenSpec instructions contain invalid context paths")
        for value in values:
            requested.append(openspec_context_source(str(value)))
    requested.extend(includes)
    return list(dict.fromkeys(safe_source(item, tracked) for item in requested))


COMMON_OPENSPEC_SOURCES = (
    "AGENTS.md",
    "README.md",
    "CONTRIBUTING.md",
    ".specify/intent.md",
    "docs/project_management/delivery_levels.md",
    "docs/project_management/jira_workflow.md",
)


def build_openspec_harness_pack(
    action_value: str,
    role_value: str,
    change_value: str,
    includes: list[str] | None = None,
    output_directory: Path = OUTPUT_DIRECTORY,
    runner: OpenSpecRunner = run_openspec_json,
    jira: str | None = None,
    jira_exception: str | None = None,
) -> Path:
    action = normalize_action(action_value)
    role_path = resolve_role(role_value)
    change = normalize_change(change_value)
    jira, jira_exception = resolve_jira_tracking(
        jira,
        jira_exception,
        required=True,
    )
    skill_path = ROOT / "ai-specs" / "skills" / ACTION_SKILLS[action] / "SKILL.md"
    if not skill_path.is_file():
        raise HarnessError(f"Workflow definition not found: {relative(skill_path)}")

    validation = runner(
        ("validate", change, "--type", "change", "--strict", "--json")
    )
    validation_items = validation.get("items", [])
    if not validation_items or not all(item.get("valid") for item in validation_items):
        raise HarnessError(f"OpenSpec change {change} does not pass strict validation")

    status = runner(("status", "--change", change, "--json"))
    if not status.get("isComplete"):
        raise HarnessError(f"OpenSpec planning artifacts are incomplete for {change}")

    apply = runner(("instructions", "apply", "--change", change, "--json"))
    if apply.get("state") == "blocked":
        missing = ", ".join(apply.get("missingArtifacts", [])) or "unknown artifacts"
        raise HarnessError(f"OpenSpec change {change} is blocked by {missing}")
    progress = apply.get("progress", {})
    if action == "prepare-pr" and progress.get("remaining") != 0:
        raise HarnessError(
            f"OpenSpec change {change} has unfinished tasks and cannot prepare a PR"
        )

    sources = _openspec_sources(
        apply,
        role_path,
        skill_path,
        includes or [],
    )
    output_directory.mkdir(parents=True, exist_ok=True)
    role = role_path.stem
    filename = f"harness-{action}-{role}-openspec-{change}.md"
    output = output_directory / filename
    status_summary = {
        "change": status.get("changeName"),
        "schema": status.get("schemaName"),
        "planningComplete": status.get("isComplete"),
        "artifacts": status.get("artifacts", []),
    }
    apply_summary = {
        "state": apply.get("state"),
        "progress": progress,
        "tasks": apply.get("tasks", []),
    }
    instructions = (
        f"Adopt the role defined in {relative(role_path)}.",
        f"Follow the workflow in {relative(skill_path)}.",
        f"Work only on OpenSpec change {change}.",
        (
            f"Use Jira work item {jira} only for owner, status and blockers."
            if jira
            else f"Use the approved Jira exception {jira_exception} for this change."
        ),
        "Treat OpenSpec artifacts, AGENTS.md and referenced contracts as authoritative.",
        "Before changing files, explain scope, planned files, blockers and checks.",
        "Do not invent decisions, evidence or implemented capabilities.",
        "Keep datasets, secrets and real CFPB narratives out of prompts and outputs.",
        "Human review is required before commit, push, pull request, archive or merge.",
    )
    lines = [
        f"# Harness pack — {ACTION_LABELS[action]} / {role} / OpenSpec {change}",
        "",
        "> Generated from tracked project sources and the local OpenSpec CLI.",
        "> Never attach datasets, secrets or real CFPB narratives.",
        "",
        "## Suggested instruction",
        "",
        "```text",
        *instructions,
        "```",
        "",
        "## Work tracking",
        "",
        *jira_tracking_lines(jira, jira_exception),
        "",
        "## OpenSpec status",
        "",
        "```json",
        json.dumps(status_summary, ensure_ascii=False, indent=2),
        "```",
        "",
        "## OpenSpec apply state",
        "",
        "```json",
        json.dumps(apply_summary, ensure_ascii=False, indent=2),
        "```",
        "",
        "## Source index",
        "",
        *(f"- `{relative(path)}`" for path in sources),
    ]
    for path in sources:
        content = path.read_text(encoding="utf-8").strip()
        lines.extend(("", "---", "", f"## Source: `{relative(path)}`", "", content))
    output.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return output


def build_harness_pack(
    action_value: str,
    role_value: str,
    spec_value: str,
    task_value: str,
    includes: list[str] | None = None,
    output_directory: Path = OUTPUT_DIRECTORY,
    jira: str | None = None,
) -> Path:
    action = normalize_action(action_value)
    role_path = resolve_role(role_value)
    spec = resolve_spec(spec_value)
    task = normalized_task(task_value)
    mapped_jira = LEGACY_JIRA_MAP.get((spec.name, task))
    if jira and mapped_jira and jira != mapped_jira:
        raise HarnessError(
            f"{spec.name}/{task} is mapped to {mapped_jira}, not {jira}"
        )
    jira, _ = resolve_jira_tracking(jira or mapped_jira, None, required=False)
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
        (
            f"Use Jira work item {jira} only for owner, status and blockers."
            if jira
            else "This legacy task has no Jira item; do not invent one."
        ),
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
        description="Run diagnostics or generate a safe OpenSpec/legacy task pack."
    )
    parser.add_argument("action", choices=(*ACTION_SKILLS, "doctor"))
    parser.add_argument("--role", help="Role name from ai-specs/agents")
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--change", help="OpenSpec change identifier")
    source.add_argument("--spec", help="Legacy spec directory name or unique prefix")
    parser.add_argument("--task", help="Legacy task identifier in format T-NNN")
    tracking = parser.add_mutually_exclusive_group()
    tracking.add_argument("--jira", help="Jira work item in format PG-N")
    tracking.add_argument(
        "--jira-exception",
        choices=sorted(JIRA_EXCEPTIONS),
        help="Controlled exception when no Jira item can exist",
    )
    parser.add_argument(
        "--include",
        action="append",
        default=[],
        help="Additional tracked documentation source; repeat as needed",
    )
    args = parser.parse_args()

    if args.action == "doctor":
        ok, lines = doctor_report()
        print("\n".join(lines))
        return 0 if ok else 1
    if not args.role:
        parser.error("--role is required for task actions")
    if args.change and args.task:
        parser.error("--task cannot be combined with --change")
    if args.spec and not args.task:
        parser.error("--task is required with --spec")
    if not args.change and not args.spec:
        parser.error("choose --change or the legacy --spec/--task pair")

    try:
        if args.change:
            output = build_openspec_harness_pack(
                args.action,
                args.role,
                args.change,
                args.include,
                jira=args.jira,
                jira_exception=args.jira_exception,
            )
        else:
            if args.jira_exception:
                parser.error("--jira-exception is only valid with --change")
            output = build_harness_pack(
                args.action,
                args.role,
                args.spec,
                args.task,
                args.include,
                jira=args.jira,
            )
    except (HarnessError, HandoffError, OSError, subprocess.CalledProcessError) as exc:
        print(f"Cannot build harness pack: {exc}", file=sys.stderr)
        return 1

    print(output.relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    sys.exit(main())
