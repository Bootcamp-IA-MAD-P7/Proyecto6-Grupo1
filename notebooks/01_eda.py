# %% [markdown]
# CFPB Complaint Dataset — EDA
#
# Answers Q-001 through Q-004 from spec `001-cfpb-target-contract` / T-004.
# No real narratives are displayed or persisted in Git, logs, or reports.

# %%
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import polars as pl

plt.rcParams["figure.dpi"] = 150
plt.rcParams["font.size"] = 9

ROOT = Path.cwd().resolve()
if ROOT.name == "notebooks":
    ROOT = ROOT.parent
CONTRACT = json.loads((ROOT / "config" / "cfpb_target_contract.json").read_text())
PARQUET = ROOT / "data" / "interim" / "cfpb.parquet"
FIGS = ROOT / "reports" / "figures"
FIGS.mkdir(parents=True, exist_ok=True)

# %%
df = pl.read_parquet(PARQUET)
print(f"Shape: {df.shape}")
print(f"Memory: {df.estimated_size('mb'):.1f} MB")
print(f"Columns: {df.columns}")

# %%
df.head(3)

# %% [markdown]
# ## 1. Population breakdown

# %%
total_source = 40_213_168
print(f"Source CSV (all rows): {total_source:,}")
print()
print("Corpus (in window, narrative+product non-null, canonical mapped):")
print(f"  {df.shape[0]:,} rows")
print(f"  {df['narrative_hash'].n_unique():,} unique narrative groups")
print(f"  {df['Complaint ID'].n_unique():,} unique complaint IDs")
print(f"  {df['product_canonical'].n_unique()} canonical classes")

# %%
by_product = df.group_by("product_canonical").agg(pl.len().alias("count")).sort("count", descending=True)
total = by_product["count"].sum()
print(f"Total corpus: {total:,}")

# %% [markdown]
# ## 2. Class distribution and imbalance

# %%
fig, ax = plt.subplots(figsize=(10, 5))
labels = by_product["product_canonical"].to_list()
counts = by_product["count"].to_list()
colors = plt.cm.tab20(np.linspace(0, 1, len(labels)))
bars = ax.barh(range(len(labels)), counts, color=colors)
ax.set_yticks(range(len(labels)))
ax.set_yticklabels(labels, fontsize=8)
ax.set_xlabel("Number of complaints")
ax.set_title("Canonical class distribution")
for i, (bar, c) in enumerate(zip(bars, counts)):
    ax.text(bar.get_width() + total * 0.005, bar.get_y() + bar.get_height() / 2,
            f"{c:,} ({c/total*100:.1f}%)", va="center", fontsize=7)
ax.set_xlim(0, max(counts) * 1.25)
fig.tight_layout()
fig.savefig(FIGS / "class_distribution.png")
plt.show()

# %%
majority = counts[0]
majority_share = majority / total
print(f"Majority class: {labels[0]} ({majority:,} — {majority_share:.1%})")
print(f"Minority class: {labels[-1]} ({counts[-1]:,} — {counts[-1]/total:.2%})")
print(f"Imbalance ratio (majority/minority): {majority / counts[-1]:.1f}x")
print(f"Classes with <1% share: {sum(1 for c in counts if c/total < 0.01)}")

# %% [markdown]
# ## 3. Temporal evolution

# %%
temporal = df.with_columns(
    pl.col("Date received").str.strptime(pl.Date, "%Y-%m-%d").alias("date_parsed")
)
print(f"Range: {temporal['date_parsed'].min()} to {temporal['date_parsed'].max()}")

# %%
monthly = (
    temporal
    .with_columns(pl.col("date_parsed").dt.truncate("1mo").alias("month"))
    .group_by(["month", "product_canonical"])
    .agg(pl.len().alias("count"))
    .sort("month")
)

top_5 = monthly.group_by("product_canonical").agg(pl.sum("count").alias("total")).sort("total", descending=True).head(5)["product_canonical"].to_list()
monthly_top5 = monthly.filter(pl.col("product_canonical").is_in(top_5))

fig, ax = plt.subplots(figsize=(12, 4))
for label in top_5:
    sub = monthly_top5.filter(pl.col("product_canonical") == label).sort("month")
    ax.plot(sub["month"].to_list(), sub["count"].to_list(), label=label, linewidth=1)
ax.legend(fontsize=7, ncol=2)
ax.set_title("Monthly complaints by product (top 5 classes)")
ax.set_ylabel("Complaints")
ax.xaxis.set_major_locator(mticker.MaxNLocator(8))
fig.tight_layout()
fig.savefig(FIGS / "temporal_trend.png")
plt.show()

# %% [markdown]
# ## 4. Duplicate analysis

# %%
dup_ids = df.group_by("Complaint ID").agg(pl.len().alias("count")).filter(pl.col("count") > 1)
print(f"Duplicate complaint IDs: {dup_ids.shape[0]:,} groups, {dup_ids['count'].sum() - dup_ids.shape[0]:,} redundant rows")

# %%
grouped = df.group_by("narrative_hash").agg([
    pl.len().alias("count"),
    pl.n_unique("Complaint ID").alias("unique_ids"),
    pl.col("product_canonical").n_unique().alias("targets_n_unique"),
    pl.col("product_canonical").alias("targets"),
])

exact_dup = grouped.filter(pl.col("count") > 1)
print(f"Exact duplicate narrative groups: {exact_dup.shape[0]:,}")
print(f"Rows involved: {exact_dup['count'].sum():,}")
print(f"Groups with different targets (conflict): {exact_dup.filter(pl.col('targets_n_unique') > 1).shape[0]:,}")

# %%
conflict_groups = exact_dup.filter(pl.col("targets_n_unique") > 1)

fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))

multiplicity = grouped["count"].value_counts(name="freq").sort("count")
axes[0].bar(multiplicity["count"].to_list(), multiplicity["freq"].to_list(), width=0.6)
axes[0].set_xlabel("Narratives per hash group")
axes[0].set_ylabel("Groups (log scale)")
axes[0].set_title("Duplicate group size distribution")
axes[0].set_yscale("log")

axes[1].bar(["Same target", "Conflicting target"], [
    exact_dup.filter(pl.col("targets_n_unique") == 1).shape[0],
    conflict_groups.shape[0],
])
axes[1].set_ylabel("Duplicate groups")
axes[1].set_title("Narrative duplicates by target agreement")
fig.tight_layout()
fig.savefig(FIGS / "duplicates_analysis.png")
plt.show()

# %%
print(f"Total narrative groups: {grouped.shape[0]:,}")
print(f"  Unique (count=1): {grouped.filter(pl.col('count') == 1).shape[0]:,}")
print(f"  Duplicate groups: {exact_dup.shape[0]:,}")
print(f"  Conflict groups:  {conflict_groups.shape[0]:,}")
print(f"  Total redundant:  {exact_dup['count'].sum() - exact_dup.shape[0]:,}")

# %% [markdown]
# ## 5. Narrative length distribution

# %%
lengths = df["Consumer complaint narrative"].str.len_chars()
print(f"Length stats (n={lengths.len():,}):")
print(f"  Mean:   {lengths.mean():.0f}")
print(f"  Median: {lengths.median():.0f}")
print(f"  Std:    {lengths.std():.0f}")
print(f"  Min:    {lengths.min():.0f}")
print(f"  Max:    {lengths.max():.0f}")
print(f"  P1:     {lengths.quantile(0.01):.0f}")
print(f"  P99:    {lengths.quantile(0.99):.0f}")
empty_pct = (lengths == 0).sum() / lengths.len() * 100
print(f"  Empty (len=0): {empty_pct:.2f}%")

# %%
fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))

trimmed = lengths.filter(lengths < lengths.quantile(0.99))
axes[0].hist(trimmed.to_numpy(), bins=80, density=True, alpha=0.7)
axes[0].axvline(lengths.median(), color="red", linestyle="--", label=f"Median={lengths.median():.0f}")
axes[0].axvline(lengths.mean(), color="orange", linestyle=":", label=f"Mean={lengths.mean():.0f}")
axes[0].set_xlabel("Narrative length (characters)")
axes[0].set_ylabel("Density")
axes[0].set_title("Narrative length (P99 clipped)")
axes[0].legend(fontsize=7)

top6 = by_product.head(6)["product_canonical"].to_list()
box_data = []
for label in top6:
    vals = df.filter(pl.col("product_canonical") == label)["Consumer complaint narrative"].str.len_chars()
    box_data.append(vals.to_numpy())
axes[1].boxplot(box_data, orientation="horizontal", showfliers=False)
axes[1].set_yticklabels([l[:20] for l in top6])
axes[1].set_xlabel("Narrative length (characters)")
axes[1].set_title("Length distribution by product (top 6)")

fig.tight_layout()
fig.savefig(FIGS / "length_distribution.png")
plt.show()

# %% [markdown]
# ## 6. Language detection (Q-001)

# %%
SAMPLE_SIZE = 100_000
rng = np.random.default_rng(42)
indices = rng.choice(df.shape[0], size=min(SAMPLE_SIZE, df.shape[0]), replace=False)
sample = df[indices]

# %%
try:
    from langdetect import DetectorFactory, LangDetectException, detect
    DetectorFactory.seed = 42
    detected = []
    fail = 0
    texts = sample["Consumer complaint narrative"].to_list()
    for t in texts[:5000]:
        try:
            lang = detect(t[:500])
            detected.append(lang)
        except LangDetectException:
            detected.append("unknown")
            fail += 1
    lang_counts = Counter(detected)
    total_ok = sum(lang_counts.values())
    print(f"Language detection (n={total_ok}):")
    for lang, cnt in lang_counts.most_common(10):
        print(f"  {lang}: {cnt:,} ({cnt/total_ok:.1%})")
    print(f"  Failed: {fail}")
    print(f"  Non-English: {total_ok - lang_counts.get('en', 0):,} ({(total_ok - lang_counts.get('en', 0))/total_ok:.1%})")
except ImportError:
    print("langdetect not available")

# %% [markdown]
# ## 7. Summary (Q-001 to Q-004)

# %%
summary = {
    "Q-001 Language": {
        "Finding": "~98.6% English in 5k sample (langdetect 1.0.9).",
        "Implication": "A single-language (EN) model may be viable; language policy TBD.",
    },
    "Q-002 Duplicates": {
        "Finding": f"{exact_dup.shape[0]:,} duplicate narrative groups ({conflict_groups.shape[0]:,} with conflicting targets).",
        "Implication": "Conflicts must be excluded or resolved; within-group policy TBD.",
    },
    "Q-003 Split": {
        "Finding": "SHA-256 group key available; temporal (yearly/monthly) or stratified random split feasible.",
        "Implication": "prevent_group_cross_split=true enforced; final split TBD.",
    },
    "Q-004 Imbalance": {
        "Finding": f"Majority={majority_share:.1%}, ratio {majority/counts[-1]:.1f}x, {sum(1 for c in counts if c/total<0.01)} classes <1%.",
        "Implication": "Weighted loss or oversampling likely needed; strategy TBD.",
    },
}
for k, v in summary.items():
    print(f"\n### {k}")
    print(f"  {v['Finding']}")
    print(f"  → {v['Implication']}")

# %%
print("EDA cells complete. All figures in reports/figures/")
