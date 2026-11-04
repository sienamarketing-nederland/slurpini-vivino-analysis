# Final Project — Slurpini Vivino Analysis

**Author:** Ingelina Zilli  
**Programme:** Amsterdam Data Academy — AI Professional  
**Presentation date:** 4 November 2026

## Problem and objectives

Can a small Vivino wine sample support a transparent, reproducible shortlist? This exploratory project compares wine ratings, review counts and prices; explains a rating threshold of 4.2 and a minimum of 100 reviews; and contrasts filtering with a ranking-based alternative.

## Data

The source is a local Excel workbook named `Vivino-export.xlsx`, supplied for the coursework. The **`Italie`** worksheet contains four comma-separated wine records in the first Excel column, preceded by a CSV-style header. The analysis uses these four original wines only, not the other country sheets in the workbook. Columns: `name`, `country`, `region`, `rating`, `rating_count`, `price`. Wine vintages are in names; there is no documented observation date. The workbook contains many other sheets, which are **out of scope**.

**The original workbook is not included in this repository.** Obtain it from the original course/project source if you have permission, then place it at `data/Vivino-export.xlsx`. Do not upload confidential or restricted data. No proprietary or private source data is published here.

## Method

1. Read the first column of the `Italie` worksheet and parse the comma-separated records using Python's `csv` parser.
2. Convert `rating`, `rating_count`, and `price` to numeric values.
3. Summarise rating distribution, mean, median, minimum and maximum.
4. Filter wines with rating >= sample median (4.2) and >=100 reviews.
5. Test review minimums of 3, 50, 100, and 500 while retaining the median-rating threshold.
6. Rank all wines by rating descending, then review count descending as a tie-breaker.
7. Export tables and two charts.

This is **descriptive exploratory analysis**, not a trained predictive model. No train/test split or model accuracy metric is applicable. Evaluation uses descriptive statistics, filter sensitivity and comparison against the alternative ranking.

## Results from the four-wine course sample

- Mean rating **4.175**, median **4.2**, range **3.7–4.6**.
- With rating >=4.2 and >=100 reviews, **two wines** qualify: Sassicaia 2019 (4.6; 1,006 reviews) and Caiarossa 2015 (4.2; 506 reviews).
- With rating >=4.2, review thresholds of **3, 50, 100, 500** retain **3, 3, 2, 2** wines respectively.
- Ranking by rating and then review count also keeps Podere Ritorti (4.2; 63 reviews) in third place, illustrating how a hard cutoff excludes a potentially interesting wine.
- Review volume is not equivalent to sales, quality or statistical confidence; the 100-review cutoff is a practical choice, **not** a validated reliability threshold.

## Installation and reproduction

Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

Copy your authorised source workbook to `data/Vivino-export.xlsx`, then run from the repository root:

```bash
python src/analyze.py --input data/Vivino-export.xlsx --output outputs
```

Expected outputs: `cleaned_wines.csv`, `summary.csv`, `threshold_sensitivity.csv`, `alternative_ranking.csv`, `filtered_shortlist.csv`, `rating_histogram.png`, and `review_counts.png`.

## Limitations and future work

Only four observations, non-random selection, unclear collection date, heterogeneous wine types, possible price variability, and no verified sales or tasting outcomes. Results cannot be generalised to the wine market, and correlations cannot establish causation. A future study should use a larger documented sample, test alternative ranking weights and thresholds, and include grape variety, market segment and sales data.

## Repository structure

```text
README.md
requirements.txt
.gitignore
src/analyze.py
data/                  # Place authorised workbook here locally
outputs/               # Generated locally; not committed
```
