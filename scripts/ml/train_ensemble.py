"""Train and compare ensemble models (RF defaults, XGBoost optimized)."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC = str(PROJECT_ROOT / "src")
print(f"DEBUG: ROOT={PROJECT_ROOT}", file=sys.stderr)
print(f"DEBUG: SRC={SRC}", file=sys.stderr)
print(f"DEBUG: SRC in path={SRC in sys.path}", file=sys.stderr)
print(f"DEBUG: SRC exists={Path(SRC).is_dir()}", file=sys.stderr)
print(f"DEBUG: __init__ exists={Path(SRC, '__init__.py').is_file()}", file=sys.stderr)
if SRC not in sys.path:
    sys.path.insert(0, SRC)
    print(f"DEBUG: inserted, now in path={SRC in sys.path}", file=sys.stderr)

import joblib
import polars as pl

from src.ml.evaluation import evaluate
from src.ml.models import train_rf, train_xgb
from src.ml.models import DEFAULT_LGBM_CONFIG, train_lgbm
from src.ml.tuning import tune_hyperparams
from src.ml.vectorizer import VectorizerConfig
from src.ml.visualization import (
    plot_confusion_matrix,
    plot_feature_importance,
    plot_model_comparison,
)

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "data" / "processed" / "cfpb_training.parquet"
DEFAULT_MODEL_DIR = ROOT / "models"
DEFAULT_REPORT_DIR = ROOT / "reports" / "validation"
DEFAULT_FIGURE_DIR = DEFAULT_REPORT_DIR / "figures"
RANDOM_STATE = 42
CLASSES = [
    "Checking or savings account",
    "Credit card",
    "Credit reporting or other personal consumer reports",
    "Debt collection",
    "Debt or credit management",
    "Money transfer, virtual currency, or money service",
    "Mortgage",
    "Payday loan, title loan, personal loan, or advance loan",
    "Prepaid card",
    "Student loan",
    "Vehicle loan or lease",
]


def load_data(input_path: Path) -> pl.DataFrame:
    return pl.read_parquet(input_path)


def temporal_split(df: pl.DataFrame, val_frac: float = 0.15, test_frac: float = 0.15):
    dates = df["date_received"].sort()
    total = len(dates)
    train_cut = dates[int(total * (1 - test_frac - val_frac))]
    val_cut = dates[int(total * (1 - test_frac))]
    train = df.filter(pl.col("date_received") < train_cut)
    val = df.filter(
        (pl.col("date_received") >= train_cut)
        & (pl.col("date_received") < val_cut)
    )
    test = df.filter(pl.col("date_received") >= val_cut)
    return train, val, test


def vectorizer_config() -> dict:
    return {
        "max_features": 8000,
        "min_df": 3,
        "max_df": 0.8,
        "ngram_range": [1, 2],
        "sublinear_tf": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--model-dir", default=str(DEFAULT_MODEL_DIR))
    parser.add_argument("--report-dir", default=str(DEFAULT_REPORT_DIR))
    parser.add_argument("--figure-dir", default=str(DEFAULT_FIGURE_DIR))
    parser.add_argument("--n-trials", type=int, default=40,
                        help="Optuna trials for XGBoost tuning (on sample)")
    parser.add_argument("--xgb-only", action="store_true",
                        help="Skip Random Forest entirely")
    parser.add_argument("--tune-sample", type=int, default=100_000,
                        help="Sample size for XGBoost tuning (0 = full)")
    parser.add_argument("--sample", type=int, default=None,
                        help="Use only N rows per split (for dev runs)")
    parser.add_argument("--lgbm-only", action="store_true",
                        help="Skip RF and XGBoost, only train LightGBM")
    parser.add_argument("--lgbm-gpu", action="store_true", default=True,
                        help="Use GPU for LightGBM (default: True)")
    parser.add_argument("--no-lgbm-gpu", action="store_false", dest="lgbm_gpu",
                        help="Disable GPU for LightGBM")
    args = parser.parse_args()

    input_path = Path(args.input)
    model_dir = Path(args.model_dir)
    report_dir = Path(args.report_dir)
    figure_dir = Path(args.figure_dir)
    n_trials = args.n_trials
    tune_sample = args.tune_sample

    print(f"Loading {input_path}...")
    df = load_data(input_path)
    print(f"Total rows: {len(df):,}")

    print("Splitting temporally...")
    train, val, test = temporal_split(df)

    if args.sample:
        train = train.sample(n=min(args.sample, len(train)), seed=RANDOM_STATE)
        val = val.sample(n=min(max(args.sample // 5, 5_000), len(val)), seed=RANDOM_STATE)

    train_texts = train["complaint_what_happened"].to_list()
    train_labels = train["product_canonical"].to_list()
    val_texts = val["complaint_what_happened"].to_list()
    val_labels = val["product_canonical"].to_list()

    print(f"Train: {len(train):,}  Val: {len(val):,}  Test (protected): {len(test):,}")

    print("Vectorizing...")
    t0 = time.time()
    vc = VectorizerConfig(vectorizer_config())
    X_train = vc.fit_transform(train_texts)
    X_val = vc.transform(val_texts)
    print(f"Done in {time.time() - t0:.1f}s. Shape: {X_train.shape}")

    results = {}
    xgb_model = None
    xgb_val_pred = []
    xgb_config = {}
    rf_model = None
    rf_val_pred = []
    lgbm_model = None
    lgbm_val_pred = []
    lgbm_config = {}

    # --- Random Forest (defaults, no tuning) ---
    if not args.xgb_only and not args.lgbm_only:
        print("\n========================================")
        print("Random Forest (defaults)")
        print("========================================")

        t0 = time.time()
        rf_model = train_rf(X_train, train_labels)
        print(f"RF training done in {time.time() - t0:.1f}s")

        model_dir.mkdir(parents=True, exist_ok=True)
        rf_path = model_dir / "cfpb_rf.joblib"
        joblib.dump({"vectorizer": vc, "model": rf_model, "config": {}}, rf_path)
        print(f"Model saved to {rf_path}")

        rf_val_pred = rf_model.predict(X_val)
        rf_ev = evaluate(val_labels, rf_val_pred, CLASSES,
                         y_train_true=train_labels, y_train_pred=rf_model.predict(X_train),
                         y_pred_proba=rf_model.predict_proba(X_val))
        results["Random Forest"] = rf_ev
        print(f"RF  accuracy={rf_ev.accuracy:.4f}  precision={rf_ev.precision_macro:.4f}  recall={rf_ev.recall_macro:.4f}  F1={rf_ev.macro_f1:.4f}  AUC={rf_ev.roc_auc:.4f}  gap={rf_ev.gap_macro_f1:.4f}")

    # --- XGBoost (tuning on sample + retrain full with early_stopping) ---
    if not args.lgbm_only:
        print("\n========================================")
        print("XGBoost")
        print("========================================")

        use_sample = tune_sample > 0 and tune_sample < len(train)
        if use_sample:
            sample_train = train.sample(n=min(tune_sample, len(train)), seed=RANDOM_STATE)
            sample_val = val.sample(n=min(max(tune_sample // 5, 5_000), len(val)), seed=RANDOM_STATE)
            s_texts = sample_train["complaint_what_happened"].to_list()
            s_labels = sample_train["product_canonical"].to_list()
            sv_texts = sample_val["complaint_what_happened"].to_list()
            sv_labels = sample_val["product_canonical"].to_list()
            print(f"Tuning sample: Train {len(sample_train):,} / Val {len(sample_val):,}")

            print("Vectorizing sample...")
            t0 = time.time()
            svc = VectorizerConfig(vectorizer_config())
            X_s_train = svc.fit_transform(s_texts)
            X_s_val = svc.transform(sv_texts)
            print(f"Done in {time.time() - t0:.1f}s. Shape: {X_s_train.shape}")

            print(f"Tuning XGBoost with {n_trials} Optuna trials (regularization enabled)...")
            t0 = time.time()
            xgb_tune = tune_hyperparams("xgb", X_s_train, s_labels, X_s_val, sv_labels, n_trials=n_trials)
            print(f"Tuning done in {time.time() - t0:.1f}s")
            print(f"Best params: {xgb_tune['best_params']}")
            print(f"Best val macro F1: {xgb_tune['best_value']:.4f}")
            xgb_config = xgb_tune["best_params"]
        else:
            xgb_config = {}

        print(f"Training XGBoost ({X_train.shape[0]:,} rows) with early_stopping...")
        t0 = time.time()
        xgb_model = train_xgb(X_train, train_labels, xgb_config, eval_set=(X_val, val_labels))
        print(f"XGBoost done in {time.time() - t0:.1f}s")

        model_dir.mkdir(parents=True, exist_ok=True)
        xgb_path = model_dir / "cfpb_xgb.joblib"
        joblib.dump({"vectorizer": vc, "model": xgb_model, "config": xgb_config}, xgb_path)
        print(f"Model saved to {xgb_path}")

        xgb_val_pred = xgb_model.predict(X_val)
        xgb_ev = evaluate(val_labels, xgb_val_pred, CLASSES,
                          y_train_true=train_labels, y_train_pred=xgb_model.predict(X_train),
                          y_pred_proba=xgb_model.predict_proba(X_val))
        results["XGBoost"] = xgb_ev
        print(f"XGB accuracy={xgb_ev.accuracy:.4f}  precision={xgb_ev.precision_macro:.4f}  recall={xgb_ev.recall_macro:.4f}  F1={xgb_ev.macro_f1:.4f}  AUC={xgb_ev.roc_auc:.4f}  gap={xgb_ev.gap_macro_f1:.4f}")

    # --- LightGBM (GPU, tuning on sample + retrain full) ---
    lgbm_config = DEFAULT_LGBM_CONFIG.copy()
    if not args.lgbm_gpu:
        lgbm_config["device"] = "cpu"

    print("\n========================================")
    print("LightGBM")
    print("========================================")

    use_sample = tune_sample > 0 and tune_sample < len(train)
    if use_sample:
        sample_train = train.sample(n=min(tune_sample, len(train)), seed=RANDOM_STATE)
        sample_val = val.sample(n=min(max(tune_sample // 5, 5_000), len(val)), seed=RANDOM_STATE)
        s_texts = sample_train["complaint_what_happened"].to_list()
        s_labels = sample_train["product_canonical"].to_list()
        sv_texts = sample_val["complaint_what_happened"].to_list()
        sv_labels = sample_val["product_canonical"].to_list()
        print(f"Tuning sample: Train {len(sample_train):,} / Val {len(sample_val):,}")

        print("Vectorizing sample...")
        t0 = time.time()
        svc = VectorizerConfig(vectorizer_config())
        X_s_train = svc.fit_transform(s_texts)
        X_s_val = svc.transform(sv_texts)
        print(f"Done in {time.time() - t0:.1f}s. Shape: {X_s_train.shape}")

        lgbm_trials = n_trials
        print(f"Tuning LightGBM with {lgbm_trials} Optuna trials (GPU enabled)...")
        t0 = time.time()
        lgbm_tune = tune_hyperparams("lgbm", X_s_train, s_labels, X_s_val, sv_labels, n_trials=lgbm_trials)
        print(f"Tuning done in {time.time() - t0:.1f}s")
        print(f"Best params: {lgbm_tune['best_params']}")
        print(f"Best val macro F1: {lgbm_tune['best_value']:.4f}")
        lgbm_config = {**lgbm_config, **lgbm_tune["best_params"]}

    print(f"Training LightGBM ({len(train):,} rows) with early_stopping...")
    t0 = time.time()
    lgbm_model = train_lgbm(X_train, train_labels, lgbm_config, eval_set=(X_val, val_labels))
    print(f"LightGBM done in {time.time() - t0:.1f}s")

    lgbm_path = model_dir / "cfpb_lgbm.joblib"
    joblib.dump({"vectorizer": vc, "model": lgbm_model, "config": lgbm_config}, lgbm_path)
    print(f"Model saved to {lgbm_path}")

    lgbm_val_pred = lgbm_model.predict(X_val)
    lgbm_ev = evaluate(val_labels, lgbm_val_pred, CLASSES,
                      y_train_true=train_labels, y_train_pred=lgbm_model.predict(X_train),
                      y_pred_proba=lgbm_model.predict_proba(X_val))
    results["LightGBM"] = lgbm_ev
    print(f"LGB accuracy={lgbm_ev.accuracy:.4f}  precision={lgbm_ev.precision_macro:.4f}  recall={lgbm_ev.recall_macro:.4f}  F1={lgbm_ev.macro_f1:.4f}  AUC={lgbm_ev.roc_auc:.4f}  gap={lgbm_ev.gap_macro_f1:.4f}")

    # --- Comparison report ---
    print("\n========================================")
    print("COMPARISON")
    print("========================================")

    report_json = {}
    model_names = list(results.keys())
    comparison_metrics = []
    weak_classes_per_model = {}

    for name, ev in results.items():
        row = {
            "model": name,
            "macro_f1": ev.macro_f1,
            "weighted_f1": ev.weighted_f1,
            "accuracy": ev.accuracy,
            "precision_macro": ev.precision_macro,
            "recall_macro": ev.recall_macro,
            "roc_auc": ev.roc_auc,
            "gap": ev.gap_macro_f1,
            "weak_classes": ev.weak_classes,
        }
        comparison_metrics.append(row)
        weak_classes_per_model[name] = [w["class"] for w in ev.weak_classes]

        per_class = {}
        for cls in CLASSES:
            cr = ev.per_class_metrics.get(cls, {})
            per_class[cls] = {
                k: round(v, 4) if isinstance(v, (int, float)) else v
                for k, v in cr.items()
            }
        if name == "XGBoost":
            cfg = xgb_config
        elif name == "LightGBM":
            cfg = lgbm_config
        else:
            cfg = {}
        report_json[name] = {
            "config": cfg,
            "train_size": len(train),
            "val_size": len(val),
            "metrics": row,
            "per_class_metrics": per_class,
        }

    # --- Figures ---
    figure_dir.mkdir(parents=True, exist_ok=True)

    for name in results:
        safe_name = name.lower().replace(" ", "_")
        if name == "XGBoost":
            preds = xgb_val_pred
            imp = xgb_model.feature_importances_
        elif name == "LightGBM":
            preds = lgbm_val_pred
            imp = lgbm_model.feature_importances_
        else:
            preds = rf_val_pred
            imp = rf_model.feature_importances_

        imp_list = imp.tolist() if hasattr(imp, 'tolist') else list(imp)

        plot_confusion_matrix(
            val_labels, preds, CLASSES,
            figure_dir / f"confusion_matrix_{safe_name}.png",
            title=f"Confusion Matrix - {name}",
        )
        plot_feature_importance(
            imp_list,
            vc.feature_names,
            figure_dir / f"feature_importance_{safe_name}.png",
            title=f"Feature Importance - {name}",
        )
        print(f"  Figures saved for {name}")

    if len(model_names) > 1:
        plot_model_comparison(
            model_names,
            {
                "Macro F1": [results[m].macro_f1 for m in model_names],
                "Accuracy": [results[m].accuracy for m in model_names],
            },
            figure_dir / "model_comparison.png",
            title=" vs ".join(model_names) + " — Validation",
        )
        print("  Comparison figure saved")

    # --- Comparison markdown ---
    tuning_info = f"Sample {tune_sample:,} / {n_trials} trials" if use_sample else "Defaults"
    md_lines = [
        "# MED-01: Comparativa de modelos ensemble",
        "",
        "## Configuración",
        "",
        "| Parámetro | Valor |",
        "|---|---|",
        "| Vectorizador | TF-IDF, unigrama+bigrama, sublinear_tf, 8K features |",
        f"| Partición | Train {len(train):,} / Val {len(val):,} / Test {len(test):,} |",
        f"| Tuning XGBoost | {tuning_info} |",
        "",
        "## Resultados sobre validation",
        "",
        "| Modelo | Macro F1 | Weighted F1 | Accuracy | Precision | Recall | ROC AUC | Gap train/val |",
        "|---|---|---|---|---|---|---|---|",
    ]

    baseline_path = report_dir / "cfpb_baseline_metrics.json"
    if baseline_path.exists():
        with open(baseline_path) as f:
            baseline_data = json.load(f)
        b_val = baseline_data.get("validation", {})
        b_gap = baseline_data.get("gap_macro_f1", "—")
        b_pass = "✅" if baseline_data.get("gap_within_threshold") else "❌"
        b_auc = baseline_data.get("test", {}).get("roc_auc", "—")
        md_lines.append(
            f"| LogisticRegression (baseline) | {b_val.get('macro_f1', '—')} | "
            f"{b_val.get('weighted_f1', '—')} | {b_val.get('accuracy', '—')} | "
            f"{b_val.get('precision_macro', '—')} | {b_val.get('recall_macro', '—')} | "
            f"{b_auc} | {b_gap} {b_pass} |"
        )
        report_json["LogisticRegression"] = {
            "notes": "from PG-3 archive",
            "val_metrics": b_val,
        }

    for name, ev in results.items():
        gap_str = f"{ev.gap_macro_f1:.4f} {'✅' if ev.gap_within_threshold else '❌'}" if ev.gap_macro_f1 else "—"
        auc_str = f"{ev.roc_auc:.4f}" if ev.roc_auc else "—"
        md_lines.append(
            f"| {name} | {ev.macro_f1:.4f} | {ev.weighted_f1:.4f} | {ev.accuracy:.4f} | "
            f"{ev.precision_macro:.4f} | {ev.recall_macro:.4f} | {auc_str} | {gap_str} |"
        )

    md_lines.extend([
        "",
        "## Clases débiles (F1 < 0.5)",
        "",
    ])
    for name, weaks in weak_classes_per_model.items():
        weak_str = ", ".join(weaks) if weaks else "Ninguna"
        md_lines.append(f"- **{name}**: {weak_str}")

    fig_list = sorted(p.name for p in figure_dir.glob("*.png")) if figure_dir.exists() else []
    md_lines.extend([
        "",
        "## Figuras",
        "",
        "Las figuras se encuentran en `reports/validation/figures/`:",
    ])
    for fname in fig_list:
        md_lines.append(f"- `{fname}`")

    md_lines.extend([
        "",
        "## Reproducibilidad",
        "",
        "```bash",
        f"python scripts/ml/train_ensemble.py --n-trials {n_trials} --tune-sample {tune_sample}",
        "```",
    ])

    report_dir.mkdir(parents=True, exist_ok=True)
    md_path = report_dir / "med_01_comparison.md"
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(f"\nReport saved to {md_path}")

    json_path = report_dir / "med_01_metrics.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report_json, f, indent=2, ensure_ascii=False)
    print(f"JSON metrics saved to {json_path}")
    print("\nDone.")


if __name__ == "__main__":
    main()
