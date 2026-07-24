# CFPB Complaint Dataset — EDA Report

**Spec:** 001-cfpb-target-contract / T-004  
**Date:** 2026-07-24  
**Tool:** `notebooks/01_eda.py`  
**Contract:** `config/cfpb_target_contract.json`

---

## 1. Population breakdown

| Stage | Rows |
|---|---|
| Source CSV (all rows) | 40,213,168 |
| In window + non-empty narrative+product | 2,272,802 |
| Excluded ambiguous (Credit card or prepaid card) | 111 |
| **Corpus (canonical mapped)** | **2,272,802** |
| Unique narrative groups | 1,227,982 |
| Unique complaint IDs | 2,272,802 |

## 2. Class distribution

| Class | Count | Share |
|---|---|---|
| Credit reporting or other personal consumer reports | 1,671,023 | 73.5% |
| Debt collection | 204,312 | 9.0% |
| Checking or savings account | 100,162 | 4.4% |
| Credit card | 99,509 | 4.4% |
| Money transfer, virtual currency, or money service | 83,008 | 3.7% |
| Mortgage | 34,127 | 1.5% |
| Student loan | 24,945 | 1.1% |
| Vehicle loan or lease | 24,573 | 1.1% |
| Payday loan, title loan, personal loan, or advance loan | 16,524 | 0.7% |
| Prepaid card | 9,577 | 0.4% |
| Debt or credit management | 5,042 | 0.2% |

**Imbalance ratio (majority/minority):** 331.4×  
**Majority share:** 73.5%  
**Classes <1%:** 3 (Payday loan, Prepaid card, Debt or credit management)

## 3. Temporal coverage

- Range: 2023-08-24 to 2026-06-02
- Monthly volume stable across top classes

## 4. Duplicate analysis

- **Duplicate complaint IDs:** 0 (IDs are unique)
- **Exact duplicate narratives (same hash):** 171,426 groups (1,216,246 rows involved)
  - Conflict groups (different targets): 1,744
  - Truly unique narratives (count=1): 1,056,556
  - Policy: `conflicting_target_policy = exclude_and_report` in contract

## 5. Narrative length

| Metric | Value |
|---|---|
| Mean | 1,010 chars |
| Median | 662 chars |
| P99 | 5,770 chars |
| Empty (len=0) | 0.00% |

## 6. Language detection (5k sample)

| Language | Share |
|---|---|
| English | 98.6% |
| Catalan (likely misdetected short texts) | 1.0% |
| Somali | 0.3% |
| Detection failed | 0 |

Note: "ca" (Catalan) detection is likely a false positive from very short narratives.

## 7. Missing values

- No nulls in `complaint_what_happened` or `product` (filtered)
- No nulls in `product_canonical` or `narrative_hash`

## 8. Answers to open questions

### Q-001 (language policy)
~98.6% English in 5k sample. A monolingual EN model is acceptable; multilingual evaluation deferred.

### Q-002 (duplicate treatment)
171,426 duplicate narrative groups; 1,744 with conflicting targets. Within-group policy remains `pending_eda` per contract.

### Q-003 (split strategy)
SHA-256 group key (`narrative_hash`) available for `prevent_group_cross_split`. Temporal (yearly/monthly) or stratified random split feasible.

### Q-004 (imbalance mitigation)
Majority 73.5% (Credit reporting), ratio 331.4×, 3 classes <1%. Weighted loss, oversampling, or class reduction via hierarchy are viable.

---

## Evidence

- **Notebook:** `notebooks/01_eda.py`
- **Figures:** `reports/figures/class_distribution.png`, `temporal_trend.png`, `duplicates_analysis.png`, `length_distribution.png`
- **Parquet:** `data/interim/cfpb.parquet` (gitignored)
- **Converter:** `scripts/data/convert_cfpb_to_parquet.py`
