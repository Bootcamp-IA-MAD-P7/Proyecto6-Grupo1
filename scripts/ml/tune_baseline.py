"""Run multiple baseline configurations, compare results, pick the best."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRAIN_SCRIPT = ROOT / "scripts" / "ml" / "train_baseline.py"
REPORT_DIR = ROOT / "reports" / "validation"

CONFIGS = [
    {"name": "01_default", "C": 1.0, "max_features": 10000, "min_df": 1, "max_df": 1.0, "ngram_range": "1,1", "sublinear_tf": False},
    {"name": "02_regularized", "C": 0.1, "max_features": 5000, "min_df": 5, "max_df": 0.8, "ngram_range": "1,1", "sublinear_tf": False},
    {"name": "03_bigrams", "C": 0.1, "max_features": 8000, "min_df": 3, "max_df": 0.8, "ngram_range": "1,2", "sublinear_tf": True},
    {"name": "04_full_tune", "C": 0.05, "max_features": 5000, "min_df": 5, "max_df": 0.8, "ngram_range": "1,2", "sublinear_tf": True},
]

results = []

for cfg in CONFIGS:
    print(f"\n{'='*60}")
    print(f"Running {cfg['name']}...")
    print(f"{'='*60}")
    report_path = REPORT_DIR / f"cfpb_baseline_{cfg['name']}.json"
    t0 = time.time()

    cmd = [
        sys.executable, str(TRAIN_SCRIPT),
        "--C", str(cfg["C"]),
        "--max-features", str(cfg["max_features"]),
        "--min-df", str(cfg["min_df"]),
        "--max-df", str(cfg["max_df"]),
        "--ngram-range", cfg["ngram_range"],
        "--report", str(report_path),
    ]
    if cfg["sublinear_tf"]:
        cmd.append("--sublinear-tf")

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    elapsed = time.time() - t0
    print(result.stdout)

    if result.returncode != 0:
        print(f"FAILED: {result.stderr}")
        continue

    with open(report_path) as f:
        report = json.load(f)

    results.append({
        "name": cfg["name"],
        "val_macro_f1": report["validation"]["macro_f1"],
        "gap": report["gap_macro_f1"],
        "gap_ok": report["gap_within_threshold"],
        "weak_classes": [w["class"] for w in report["weak_classes"]],
        "elapsed_s": round(elapsed, 0),
    })
    print(f"Elapsed: {elapsed:.0f}s")
    print(f"Val macro F1: {report['validation']['macro_f1']:.4f}")
    print(f"Gap: {report['gap_macro_f1']:.4f}  {'PASS' if report['gap_within_threshold'] else 'FAIL'}")

print(f"\n{'='*60}")
print("SUMMARY")
print(f"{'='*60}")
print(f"{'Config':<20} {'Val F1':<10} {'Gap':<10} {'OK?':<6} {'Weak classes'}")
print("-" * 80)
for r in sorted(results, key=lambda x: -x["val_macro_f1"]):
    flag = "PASS" if r["gap_ok"] else "FAIL"
    weak = ", ".join(r["weak_classes"][:3])
    print(f"{r['name']:<20} {r['val_macro_f1']:<10.4f} {r['gap']:<10.4f} {flag:<6} {weak}")

best = max(results, key=lambda x: x["val_macro_f1"] if x["gap_ok"] else 0)
print(f"\nBest config (gap OK): {best['name']}")
print(f"  Val macro F1: {best['val_macro_f1']:.4f}")
print(f"  Gap: {best['gap']:.4f}")

# copy best report to canonical path
best_report = REPORT_DIR / f"cfpb_baseline_{best['name']}.json"
canonical = REPORT_DIR / "cfpb_baseline_metrics.json"
canonical.write_text(best_report.read_text())
print(f"\nCopied {best['name']} report to cfpb_baseline_metrics.json")
print("Done.")
