"""Repository-level checks that do not require project dependencies."""

from __future__ import annotations

<<<<<<< HEAD
import os
=======
import json
>>>>>>> 5558ae2204151767a53be0e45102bd04a3b6da83
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
DAILY_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")
SPEC_DIRECTORY_PATTERN = re.compile(r"^\d{3}-[a-z0-9]+(?:-[a-z0-9]+)*$")
SPEC_REQUIRED_FILES = ("spec.md", "plan.md", "tasks.md", "decisions.md")
LEGACY_SPEC_DIRECTORIES = {
    "000-problem-discovery",
    "001-cfpb-target-contract",
    "002-team-ai-workflow",
    "003-complaint-routing-experience",
    "004-agentic-harness",
}
TEAM_MEMBERS = ("José", "Abel", "Víctor", "Miguel")
MAX_TRACKED_SIZE = 10 * 1024 * 1024
IGNORED_LINK_PREFIXES = ("http://", "https://", "mailto:", "#")
FORBIDDEN_TRACKED_NAMES = {".env", "id_rsa", "id_ed25519"}
ALLOWED_GITKEEP_PATHS = {
    Path("data/external/.gitkeep"),
    Path("data/interim/.gitkeep"),
    Path("data/processed/.gitkeep"),
    Path("data/raw/.gitkeep"),
}
DELIVERY_ID_GROUPS = {
    "ESS": 10,
    "MED": 5,
    "ADV": 6,
    "EXP": 4,
}
JIRA_TRACKING_PATTERN = re.compile(r"(?m)^- Jira:\s*`PG-[1-9]\d*`\.\s*$")
JIRA_EXCEPTION_PATTERN = re.compile(
    r"(?m)^- Jira exception:\s*`(?:bootstrap|emergency|automation)`\.\s*$"
)
NON_BREAKING_HYPHEN = "\N{NON-BREAKING HYPHEN}"
IGNORED_LOCAL_DIRECTORIES = {
    ".git",
    ".venv",
    "__pycache__",
    "exports",
    "node_modules",
    "dist",
    "coverage",
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
    files: list[Path] = []
    for directory, names, filenames in os.walk(ROOT):
        names[:] = [name for name in names if name not in IGNORED_LOCAL_DIRECTORIES]
        files.extend(Path(directory) / filename for filename in filenames)
    return files


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
        "docs/project_management/jira_workflow.md",
        "docs/project_management/dailies/2026-07-22.md",
        "package.json",
        "package-lock.json",
        "openspec/config.yaml",
        ".codex/skills/openspec-propose/SKILL.md",
        ".github/prompts/opsx-propose.prompt.md",
        ".claude/commands/opsx/propose.md",
        ".cursor/commands/opsx-propose.md",
        ".gemini/commands/opsx/propose.toml",
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
        if path.name not in LEGACY_SPEC_DIRECTORIES:
            errors.append(
                "New numbered spec directories are not allowed after OpenSpec "
                f"adoption: {path.name}"
            )
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
        if path.name == ".gitkeep" and relative not in ALLOWED_GITKEEP_PATHS:
            errors.append(f"Placeholder file is not allowed: {relative}")


def check_readme_delivery_ids(errors: list[str]) -> None:
    readme_path = ROOT / "README.md"
    if not readme_path.is_file():
        return

    text = readme_path.read_text(encoding="utf-8")
    expected = {
        f"{prefix}{NON_BREAKING_HYPHEN}{index:02d}"
        for prefix, count in DELIVERY_ID_GROUPS.items()
        for index in range(1, count + 1)
    }
    missing = sorted(identifier for identifier in expected if f"| {identifier} |" not in text)
    if missing:
        errors.append(
            "README delivery IDs must use a non-breaking hyphen: "
            + ", ".join(missing)
        )

    ascii_row = re.search(r"^\| (?:ESS|MED|ADV|EXP)-\d{2} \|", text, re.MULTILINE)
    if ascii_row:
        errors.append(
            "README contains a delivery ID that can wrap at its ASCII hyphen: "
            f"{ascii_row.group(0)}"
        )


def check_delivery_state_consistency(errors: list[str]) -> None:
    readme_path = ROOT / "README.md"
    levels_path = ROOT / "docs/project_management/delivery_levels.md"
    chart_path = ROOT / "docs/assets/charts/delivery-status-2026-07-23.svg"
    if not readme_path.is_file() or not levels_path.is_file():
        return

    readme_states: dict[str, str] = {}
    for line in readme_path.read_text(encoding="utf-8").splitlines():
        columns = [column.strip() for column in line.split("|")]
        if len(columns) < 5:
            continue
        identifier = columns[1].replace(NON_BREAKING_HYPHEN, "-")
        if re.fullmatch(r"(?:ESS|MED|ADV|EXP)-\d{2}", identifier):
            readme_states[identifier] = columns[3].strip("*` ")

    level_states: dict[str, str] = {}
    for line in levels_path.read_text(encoding="utf-8").splitlines():
        columns = [column.strip() for column in line.split("|")]
        if len(columns) < 6:
            continue
        identifier = columns[1].strip("` ")
        if re.fullmatch(r"(?:ESS|MED|ADV|EXP)-\d{2}", identifier):
            level_states[identifier] = columns[3].strip("*` ")

    expected_count = sum(DELIVERY_ID_GROUPS.values())
    if len(readme_states) != expected_count:
        errors.append(
            f"README must expose {expected_count} delivery states; "
            f"found {len(readme_states)}"
        )
    if len(level_states) != expected_count:
        errors.append(
            f"delivery_levels.md must define {expected_count} delivery states; "
            f"found {len(level_states)}"
        )

    for identifier in sorted(set(readme_states) | set(level_states)):
        if readme_states.get(identifier) != level_states.get(identifier):
            errors.append(
                "Delivery state mismatch for "
                f"{identifier}: README={readme_states.get(identifier)!r}, "
                f"delivery_levels={level_states.get(identifier)!r}"
            )

    if chart_path.is_file() and level_states:
        chart = chart_path.read_text(encoding="utf-8")
        state_counts = {
            state: sum(value == state for value in level_states.values())
            for state in ("Verificado", "En curso", "No iniciado")
        }
        for state, count in state_counts.items():
            if f"{state} {count}" not in chart:
                errors.append(
                    "Delivery chart is not synchronized with delivery_levels.md: "
                    f"expected '{state} {count}'"
                )


def check_svg_assets(errors: list[str]) -> None:
    assets_directory = ROOT / "docs/assets"
    if not assets_directory.is_dir():
        return

    for path in assets_directory.rglob("*.svg"):
        relative = path.relative_to(ROOT)
        try:
            root = ET.parse(path).getroot()
        except ET.ParseError as exc:
            errors.append(f"Invalid SVG XML in {relative}: {exc}")
            continue

        namespace = ""
        if root.tag.startswith("{"):
            namespace = root.tag.split("}", 1)[0] + "}"
        if root.attrib.get("role") != "img":
            errors.append(f"SVG is missing role=\"img\": {relative}")
        if not root.attrib.get("viewBox"):
            errors.append(f"SVG is missing viewBox: {relative}")
        if root.find(f"{namespace}title") is None:
            errors.append(f"SVG is missing an accessible title: {relative}")
        if root.find(f"{namespace}desc") is None:
            errors.append(f"SVG is missing an accessible description: {relative}")

        if relative.as_posix() == "docs/assets/diagrams/readme-project-overview.svg":
            status_labels = [
                element
                for element in root.findall(f"{namespace}text")
                if (element.text or "").strip() in {"ENTRADA", "PREVISTO"}
            ]
            if len(status_labels) != 3 or any(
                label.attrib.get("text-anchor") != "middle"
                for label in status_labels
            ):
                errors.append(
                    "Primary README diagram status labels must be centered "
                    "inside their backgrounds"
                )
            pill_widths = [
                float(element.attrib.get("width", "0"))
                for element in root.findall(f"{namespace}rect")
                if element.attrib.get("class") in {"accent", "warn"}
            ]
            if len(pill_widths) != 3 or min(pill_widths, default=0) < 120:
                errors.append(
                    "Primary README diagram status backgrounds need at least "
                    "120 units of width"
                )


def check_openspec_configuration(errors: list[str]) -> None:
    package_path = ROOT / "package.json"
    lock_path = ROOT / "package-lock.json"
    config_path = ROOT / "openspec/config.yaml"
    if not package_path.is_file() or not lock_path.is_file() or not config_path.is_file():
        return

    try:
        package = json.loads(package_path.read_text(encoding="utf-8"))
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid repository tooling JSON: {exc}")
        return

    expected_version = "1.6.0"
    dependency = package.get("devDependencies", {}).get("@fission-ai/openspec")
    if dependency != expected_version:
        errors.append(
            "@fission-ai/openspec must be pinned exactly to "
            f"{expected_version}; found {dependency!r}"
        )
    if package.get("engines", {}).get("node") != ">=20.19.0":
        errors.append("package.json must require Node.js >=20.19.0")
    if package.get("scripts", {}).get("openspec:validate") != (
        "openspec validate --all --strict --no-interactive"
    ):
        errors.append("package.json is missing the strict OpenSpec validation script")

    locked_version = (
        lock.get("packages", {})
        .get("node_modules/@fission-ai/openspec", {})
        .get("version")
    )
    if locked_version != expected_version:
        errors.append(
            "package-lock.json must resolve @fission-ai/openspec "
            f"{expected_version}; found {locked_version!r}"
        )

    config = config_path.read_text(encoding="utf-8")
    required_fragments = (
        "schema: spec-driven",
        "OpenSpec manages every new change",
        "Never add CFPB narratives",
        "Include a Tracking section with one Jira key",
    )
    for fragment in required_fragments:
        if fragment not in config:
            errors.append(f"OpenSpec config is missing required policy: {fragment}")

    changes = ROOT / "openspec/changes"
    specs = ROOT / "openspec/specs"
    if not changes.is_dir():
        errors.append("Missing OpenSpec changes directory")
    if not specs.is_dir():
        errors.append("Missing OpenSpec specifications directory")


def proposal_has_jira_tracking(text: str) -> bool:
    return bool(
        "## Tracking" in text
        and (
            JIRA_TRACKING_PATTERN.search(text)
            or JIRA_EXCEPTION_PATTERN.search(text)
        )
    )


def check_jira_work_tracking(errors: list[str]) -> None:
    template_path = ROOT / ".github/pull_request_template.md"
    if template_path.is_file():
        template = template_path.read_text(encoding="utf-8")
        required_fragments = (
            "Jira work item or approved exception:",
            "OpenSpec change:",
            "Jira, OpenSpec and this PR describe the same scope and state.",
        )
        for fragment in required_fragments:
            if fragment not in template:
                errors.append(f"Pull Request template is missing Jira policy: {fragment}")

    changes_path = ROOT / "openspec/changes"
    if not changes_path.is_dir():
        return
    for change in sorted(path for path in changes_path.iterdir() if path.is_dir()):
        if change.name == "archive":
            continue
        proposal_path = change / "proposal.md"
        if not proposal_path.is_file():
            continue
        proposal = proposal_path.read_text(encoding="utf-8")
        if not proposal_has_jira_tracking(proposal):
            errors.append(
                "Active OpenSpec proposal lacks valid Jira tracking: "
                f"{proposal_path.relative_to(ROOT).as_posix()}"
            )


def main() -> int:
    errors: list[str] = []
    files = tracked_files()
    local_files = repository_files()
    check_required_paths(errors)
    check_markdown_links(local_files, errors)
    check_dailies(errors)
    check_spec_bundles(errors)
    check_tracked_files(files or local_files, errors)
    check_readme_delivery_ids(errors)
    check_delivery_state_consistency(errors)
    check_svg_assets(errors)
    check_openspec_configuration(errors)
    check_jira_work_tracking(errors)

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
