"""Build a curated Markdown source pack for NotebookLM."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIRECTORY = ROOT / "exports/notebooklm"

STABLE_SOURCES = (
    "README.md",
    "CHANGELOG.md",
    ".specify/intent.md",
    "docs/project_management/project_principles.md",
    "docs/project_management/delivery_levels.md",
    "docs/architecture/repository_structure.md",
    "docs/architecture/system_blueprint.md",
    "docs/architecture/quality_attributes.md",
    "docs/design/ux_principles.md",
    "docs/design/documentation_visual_standard.md",
    "docs/security/security_baseline.md",
    "docs/notebooklm/source_catalog.md",
    "docs/notebooklm/project_facts.md",
    "docs/notebooklm/business_narrative.md",
    "docs/notebooklm/technical_status.md",
)


def valid_iso_date(value: str) -> str:
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use date format YYYY-MM-DD") from exc


def optional_project_sources() -> list[Path]:
    patterns = (
        "specs/[0-9]*/spec.md",
        "specs/[0-9]*/plan.md",
        "specs/[0-9]*/tasks.md",
        "specs/[0-9]*/decisions.md",
        "docs/adr/[0-9]*.md",
        "docs/product/candidates/*.md",
        "reports/**/*.md",
        "reports/**/*.json",
    )
    sources: set[Path] = set()
    for pattern in patterns:
        sources.update(ROOT.glob(pattern))
    return sorted(path for path in sources if path.is_file())


def source_paths(day: str) -> list[Path]:
    paths = [ROOT / relative for relative in STABLE_SOURCES]
    paths.extend(
        (
            ROOT / f"docs/project_management/dailies/{day}.md",
        )
    )
    paths.extend(optional_project_sources())
    return list(dict.fromkeys(path for path in paths if path.exists()))


def build_pack(day: str) -> Path:
    sources = source_paths(day)
    if not sources:
        raise RuntimeError("No source documents were found")

    output = OUTPUT_DIRECTORY / f"{day}-notebooklm-pack.md"
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# Paquete de fuentes NotebookLM — {day}",
        "",
        "> Generado desde fuentes versionadas. Revisar antes de subir a NotebookLM.",
        "",
        "## Índice de fuentes",
        "",
    ]
    lines.extend(f"- `{path.relative_to(ROOT).as_posix()}`" for path in sources)

    for path in sources:
        relative = path.relative_to(ROOT).as_posix()
        content = path.read_text(encoding="utf-8").strip()
        lines.extend(("", "---", "", f"## Fuente: `{relative}`", "", content))

    output.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--date",
        type=valid_iso_date,
        default=date.today().isoformat(),
        help="Daily date in YYYY-MM-DD format",
    )
    args = parser.parse_args()

    try:
        output = build_pack(args.date)
    except RuntimeError as exc:
        print(exc)
        return 1

    print(output.relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    sys.exit(main())
