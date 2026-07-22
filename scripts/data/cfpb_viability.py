"""Inspect CFPB complaint data without persisting complaint narratives."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from collections import Counter
from contextlib import contextmanager
from datetime import date, datetime, timezone
from pathlib import Path
from statistics import median
from typing import Any, Iterator, TextIO


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = ROOT / "config/cfpb_viability.json"

PII_PATTERNS = {
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
    "phone": re.compile(
        r"(?<!\d)(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]?\d{4}(?!\d)"
    ),
    "ssn": re.compile(r"(?<!\d)\d{3}[-\s]?\d{2}[-\s]?\d{4}(?!\d)"),
    "url": re.compile(r"\b(?:https?://|www\.)\S+", re.IGNORECASE),
}


class ContractError(ValueError):
    """Raised when configuration or input data violates the spike contract."""


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_config(path: Path) -> dict[str, Any]:
    config = json.loads(path.read_text(encoding="utf-8"))
    required_sections = {
        "schema_version",
        "source",
        "window",
        "limits",
        "fields",
        "model_contract",
        "review_thresholds",
    }
    missing = required_sections.difference(config)
    if missing:
        raise ContractError(f"Missing configuration sections: {sorted(missing)}")

    minimum = date.fromisoformat(config["window"]["date_received_min"])
    maximum = date.fromisoformat(config["window"]["date_received_max_exclusive"])
    if minimum >= maximum:
        raise ContractError("date_received_min must be earlier than date_received_max_exclusive")

    allowed_inputs = config["model_contract"]["allowed_inputs"]
    target = config["model_contract"]["target"]
    forbidden = set(config["model_contract"]["forbidden_inputs"])
    if allowed_inputs != ["complaint_what_happened"]:
        raise ContractError("The spike permits complaint_what_happened as the only model input")
    if target != "product" or target not in forbidden:
        raise ContractError("product must be the target and must be forbidden as a model input")

    max_rows = config["limits"]["max_scanned_rows"]
    if not isinstance(max_rows, int) or max_rows < 1:
        raise ContractError("max_scanned_rows must be a positive integer")
    return config


def parse_date(value: str) -> date | None:
    cleaned = value.strip()
    if not cleaned:
        return None
    if len(cleaned) >= 10:
        try:
            return date.fromisoformat(cleaned[:10])
        except ValueError:
            pass
    for pattern in ("%Y-%m-%d", "%m/%d/%Y"):
        try:
            return datetime.strptime(cleaned, pattern).date()
        except ValueError:
            continue
    return None


def resolve_fields(fieldnames: list[str] | None, aliases: dict[str, list[str]]) -> dict[str, str]:
    if not fieldnames:
        raise ContractError("The CSV has no header")
    available = {name.strip(): name for name in fieldnames if name}
    resolved: dict[str, str] = {}
    for logical_name, candidates in aliases.items():
        match = next((available[name] for name in candidates if name in available), None)
        if match is None:
            raise ContractError(
                f"Missing required field for {logical_name}; expected one of {candidates}"
            )
        resolved[logical_name] = match
    return resolved


def percentile_summary(lengths: list[int]) -> dict[str, int | None]:
    if not lengths:
        return {"minimum": None, "median": None, "maximum": None}
    return {
        "minimum": min(lengths),
        "median": int(median(lengths)),
        "maximum": max(lengths),
    }


def inspect_rows(
    rows: Iterator[dict[str, str]],
    fieldnames: list[str] | None,
    config: dict[str, Any],
) -> dict[str, Any]:
    fields = resolve_fields(fieldnames, config["fields"])
    minimum = date.fromisoformat(config["window"]["date_received_min"])
    maximum = date.fromisoformat(config["window"]["date_received_max_exclusive"])
    max_rows = config["limits"]["max_scanned_rows"]

    class_counts: Counter[str] = Counter()
    pii_record_counts: Counter[str] = Counter()
    missing_counts: Counter[str] = Counter()
    complaint_ids: set[str] = set()
    narrative_hashes: set[str] = set()
    narrative_lengths: list[int] = []
    scanned_rows = 0
    rows_in_window = 0
    eligible_rows = 0
    duplicate_ids = 0
    duplicate_narratives = 0
    invalid_dates = 0
    pii_any_records = 0
    eligible_dates: list[date] = []
    truncated = False

    for row in rows:
        if scanned_rows >= max_rows:
            truncated = True
            break
        scanned_rows += 1

        received = parse_date(row.get(fields["date_received"], ""))
        if received is None:
            invalid_dates += 1
            continue
        if received < minimum or received >= maximum:
            continue
        rows_in_window += 1

        complaint_id = row.get(fields["complaint_id"], "").strip()
        product = row.get(fields["target"], "").strip()
        narrative = row.get(fields["narrative"], "").strip()

        if not complaint_id:
            missing_counts["complaint_id"] += 1
        if not product:
            missing_counts["target"] += 1
        if not narrative:
            missing_counts["narrative"] += 1
        if not product or not narrative:
            continue

        eligible_rows += 1
        eligible_dates.append(received)
        class_counts[product] += 1
        narrative_lengths.append(len(narrative))

        if complaint_id:
            if complaint_id in complaint_ids:
                duplicate_ids += 1
            else:
                complaint_ids.add(complaint_id)

        digest = hashlib.sha256(narrative.encode("utf-8")).digest()
        if digest in narrative_hashes:
            duplicate_narratives += 1
        else:
            narrative_hashes.add(digest)

        has_pii_pattern = False
        for name, pattern in PII_PATTERNS.items():
            if pattern.search(narrative):
                pii_record_counts[name] += 1
                has_pii_pattern = True
        if has_pii_pattern:
            pii_any_records += 1

    sorted_classes = sorted(class_counts.items(), key=lambda item: (-item[1], item[0]))
    class_distribution = [
        {
            "class": name,
            "count": count,
            "share": round(count / eligible_rows, 6) if eligible_rows else 0.0,
        }
        for name, count in sorted_classes
    ]
    thresholds = config["review_thresholds"]
    majority_share = class_distribution[0]["share"] if class_distribution else 0.0
    minority_count = class_distribution[-1]["count"] if class_distribution else 0
    pii_rate_upper_bound = (
        round(pii_any_records / eligible_rows, 6) if eligible_rows else 0.0
    )

    warnings: list[str] = []
    if len(class_distribution) < thresholds["minimum_classes"]:
        warnings.append("fewer_than_minimum_classes")
    if eligible_rows < thresholds["minimum_eligible_rows"]:
        warnings.append("fewer_than_minimum_eligible_rows")
    if minority_count < thresholds["minimum_rows_per_retained_class"]:
        warnings.append("class_below_minimum_support")
    if majority_share > thresholds["majority_share_warning"]:
        warnings.append("majority_share_above_warning")
    if pii_rate_upper_bound > thresholds["pii_pattern_rate_warning"]:
        warnings.append("pii_pattern_rate_above_warning")
    if truncated:
        warnings.append("scan_truncated_at_configured_limit")

    return {
        "contract_version": config["schema_version"],
        "window": config["window"],
        "scan": {
            "scanned_rows": scanned_rows,
            "rows_in_window": rows_in_window,
            "eligible_rows": eligible_rows,
            "truncated": truncated,
            "invalid_date_rows": invalid_dates,
        },
        "quality": {
            "missing": dict(sorted(missing_counts.items())),
            "duplicate_complaint_ids": duplicate_ids,
            "duplicate_narratives": duplicate_narratives,
            "narrative_length_characters": percentile_summary(narrative_lengths),
        },
        "classes": {
            "count": len(class_distribution),
            "distribution": class_distribution,
            "majority_share": majority_share,
            "minority_count": minority_count,
        },
        "privacy": {
            "pattern_match_counts": dict(sorted(pii_record_counts.items())),
            "records_with_any_pattern": pii_any_records,
            "pattern_rate": pii_rate_upper_bound,
            "note": "Counts are heuristic signals; no matching narrative is persisted.",
        },
        "date_coverage": {
            "minimum": min(eligible_dates).isoformat() if eligible_dates else None,
            "maximum": max(eligible_dates).isoformat() if eligible_dates else None,
        },
        "warnings": warnings,
    }


@contextmanager
def open_csv_source(path: Path) -> Iterator[TextIO]:
    if path.suffix.lower() == ".zip":
        archive = zipfile.ZipFile(path)
        candidates = [name for name in archive.namelist() if name.lower().endswith(".csv")]
        if len(candidates) != 1:
            archive.close()
            raise ContractError("The ZIP must contain exactly one CSV file")
        raw = archive.open(candidates[0])
        import io

        text = io.TextIOWrapper(raw, encoding="utf-8-sig", newline="")
        try:
            yield text
        finally:
            text.close()
            archive.close()
        return

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        yield handle


def inspect_file(path: Path, config: dict[str, Any]) -> dict[str, Any]:
    with open_csv_source(path) as handle:
        reader = csv.DictReader(handle)
        result = inspect_rows(iter(reader), reader.fieldnames, config)
    result["source"] = {
        "kind": "local_file",
        "filename": path.name,
        "sha256": file_sha256(path),
    }
    result["generated_at"] = utc_timestamp()
    return result


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_probe_url(config: dict[str, Any]) -> str:
    query = {
        "date_received_min": config["window"]["date_received_min"],
        "date_received_max": config["window"]["date_received_max_exclusive"],
        "has_narrative": "true",
        "size": 1,
        "no_highlight": "true",
    }
    return f"{config['source']['api_url']}?{urllib.parse.urlencode(query)}"


def request_json(url: str, config: dict[str, Any]) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "Proyecto6-Grupo1-CFPB-Viability/1.0",
        },
    )
    limit = config["limits"]["max_api_response_bytes"]
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = response.read(limit + 1)
        if len(payload) > limit:
            raise ContractError("API response exceeded max_api_response_bytes")
        return json.loads(payload)


def extract_product_buckets(parsed: dict[str, Any]) -> list[dict[str, Any]]:
    product = parsed.get("aggregations", {}).get("product", {})
    buckets = product.get("product", {}).get("buckets")
    if buckets is None:
        buckets = product.get("field", {}).get("buckets", [])
    return [
        {"class": bucket.get("key"), "count": bucket.get("doc_count")}
        for bucket in buckets
    ]


def probe_api(config: dict[str, Any]) -> tuple[dict[str, Any], int]:
    url = build_probe_url(config)
    base = {
        "contract_version": config["schema_version"],
        "generated_at": utc_timestamp(),
        "endpoint": config["source"]["api_url"],
        "window": config["window"],
    }
    try:
        parsed = request_json(url, config)
    except urllib.error.HTTPError as exc:
        return ({**base, "status": "blocked", "http_status": exc.code}, 2)
    except urllib.error.URLError as exc:
        return ({**base, "status": "unavailable", "error_type": type(exc.reason).__name__}, 2)

    sanitized_buckets = extract_product_buckets(parsed)
    total_matching = parsed.get("hits", {}).get("total", {}).get("value")
    if isinstance(total_matching, int) and total_matching > 0:
        for bucket in sanitized_buckets:
            bucket["share"] = round(bucket["count"] / total_matching, 6)
    return (
        {
            **base,
            "status": "available",
            "total_matching_rows": total_matching,
            "total_relation": parsed.get("hits", {}).get("total", {}).get("relation"),
            "product_distribution": sanitized_buckets,
            "meta": {
                key: parsed.get("_meta", {}).get(key)
                for key in (
                    "has_data_issue",
                    "is_data_stale",
                    "is_narrative_stale",
                    "last_indexed",
                    "last_updated",
                    "license",
                )
            },
        },
        0,
    )


def build_sample_url(
    config: dict[str, Any],
    sort: str,
    size: int,
    page: int = 1,
    search_after: str | None = None,
) -> str:
    query = {
        "date_received_min": config["window"]["date_received_min"],
        "date_received_max": config["window"]["date_received_max_exclusive"],
        "has_narrative": "true",
        "size": size,
        "sort": sort,
        "no_highlight": "true",
        "no_aggs": "true",
    }
    if page > 1 and search_after:
        query.update(
            {
                "page": page,
                "frm": (page - 1) * config["limits"]["api_page_size"],
                "search_after": search_after,
            }
        )
    return f"{config['source']['api_url']}?{urllib.parse.urlencode(query)}"


def sample_api(config: dict[str, Any]) -> dict[str, Any]:
    page_size = config["limits"]["api_page_size"]
    records_per_edge = config["limits"]["api_sample_records_per_edge"]
    records: list[dict[str, str]] = []
    records_by_edge: dict[str, list[dict[str, str]]] = {
        "oldest": [],
        "newest": [],
    }
    pages = 0

    for edge_name, sort in (
        ("oldest", "created_date_asc"),
        ("newest", "created_date_desc"),
    ):
        collected_for_edge = 0
        page = 1
        search_after: str | None = None
        known_breakpoints: dict[str, list[Any]] = {}
        while collected_for_edge < records_per_edge:
            size = min(page_size, records_per_edge - collected_for_edge)
            parsed = request_json(
                build_sample_url(config, sort, size, page, search_after), config
            )
            hits = parsed.get("hits", {}).get("hits", [])
            page_records = [hit.get("_source", {}) for hit in hits]
            records.extend(page_records)
            records_by_edge[edge_name].extend(page_records)
            collected_for_edge += len(hits)
            pages += 1
            known_breakpoints.update(
                parsed.get("_meta", {}).get("break_points", {})
            )
            if len(hits) < size:
                break
            next_page = page + 1
            breakpoint = known_breakpoints.get(str(next_page))
            if not isinstance(breakpoint, list) or len(breakpoint) != 2:
                raise ContractError(
                    f"API did not return a valid breakpoint for page {next_page}"
                )
            search_after = f"{breakpoint[0]}_{breakpoint[1]}"
            page = next_page

    fields = [
        "complaint_id",
        "date_received",
        "complaint_what_happened",
        "product",
    ]
    result = inspect_rows(iter(records), fields, config)
    result["temporal_edges"] = {
        edge_name: inspect_rows(iter(edge_records), fields, config)
        for edge_name, edge_records in records_by_edge.items()
    }
    result["source"] = {
        "kind": "api_temporal_edge_sample",
        "endpoint": config["source"]["api_url"],
        "requested_records_per_edge": records_per_edge,
        "returned_records": len(records),
        "pages": pages,
        "sorts": ["created_date_asc", "created_date_desc"],
    }
    result["generated_at"] = utc_timestamp()
    result["limitations"] = [
        "The sample covers the oldest and newest available edges, not a random population sample.",
        "PII detection uses heuristic patterns and is not a privacy certification.",
        "No narrative content is persisted in this report.",
    ]
    return result


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Probe or inspect CFPB data without persisting narratives"
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    subparsers = parser.add_subparsers(dest="command", required=True)

    probe = subparsers.add_parser("probe-api", help="Probe the documented API safely")
    probe.add_argument("--output", type=Path)

    inspect = subparsers.add_parser("inspect-csv", help="Inspect a local CSV or ZIP")
    inspect.add_argument("--input", type=Path, required=True)
    inspect.add_argument("--output", type=Path, required=True)

    sample = subparsers.add_parser(
        "sample-api", help="Inspect bounded oldest/newest API samples in memory"
    )
    sample.add_argument("--output", type=Path, required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        config = load_config(args.config)
        if args.command == "probe-api":
            payload, exit_code = probe_api(config)
            if args.output:
                write_json(args.output, payload)
            print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
            return exit_code

        if args.command == "sample-api":
            payload = sample_api(config)
            write_json(args.output, payload)
            print(args.output.as_posix())
            return 0

        if not args.input.exists():
            raise ContractError(f"Input file not found: {args.input}")
        payload = inspect_file(args.input, config)
        write_json(args.output, payload)
        print(args.output.as_posix())
        return 0
    except (ContractError, json.JSONDecodeError, OSError, zipfile.BadZipFile) as exc:
        print(f"CFPB viability check failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
