"""Create the team's daily document without overwriting existing work."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DAILY_TEMPLATE = ROOT / "docs/project_management/dailies/_template.md"
DAILY_DIRECTORY = ROOT / "docs/project_management/dailies"


def valid_iso_date(value: str) -> str:
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use date format YYYY-MM-DD") from exc


def create_daily(day: str) -> Path:
    daily_path = DAILY_DIRECTORY / f"{day}.md"

    if daily_path.exists():
        raise FileExistsError(
            f"Refusing to overwrite: {daily_path.relative_to(ROOT)}"
        )

    daily_text = DAILY_TEMPLATE.read_text(encoding="utf-8").replace(
        "<AAAA-MM-DD>", day
    )
    DAILY_DIRECTORY.mkdir(parents=True, exist_ok=True)
    daily_path.write_text(daily_text, encoding="utf-8", newline="\n")
    return daily_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=valid_iso_date, help="Date in YYYY-MM-DD format")
    args = parser.parse_args()

    try:
        created = create_daily(args.day)
    except FileExistsError as exc:
        print(exc)
        return 1

    print(created.relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    sys.exit(main())
