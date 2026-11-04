"""Reproduce the Slurpini Vivino four-wine exploratory analysis."""
import argparse
import csv
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def load_data(path: Path) -> pd.DataFrame:
    # The original workbook stores each CSV record in column A of the 'Italie' sheet.
    raw = pd.read_excel(path, sheet_name='Italie', header=None, usecols=[0])
    records = list(csv.reader(raw.iloc[:, 0].dropna().astype(str)))
    if not records or records[0] != ['name', 'country', 'region', 'rating', 'rating_count', 'price']:
        raise ValueError('Unexpected format in Italie worksheet')
    df = pd.DataFrame(records[1:], columns=records[0])
    for col in ['rating', 'rating_count', 'price']:
        df[col] = pd.to_numeric(df[col], errors='raise')
    return df


def analyze(df: pd.DataFrame, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / 'cleaned_wines.csv', index=False)
    median = float(df.rating.median())
    stats = pd.DataFrame([{'n_wines': len(df), 'mean_rating': df.rating.mean(), 'median_rating': median,
                           'min_rating': df.rating.min(), 'max_rating': df.rating.max()}])
    stats.to_csv(out / 'summary.csv', index=False)
    thresholds = pd.DataFrame([{'minimum_reviews': t, 'qualifying_wines': int(((df.rating >= median) & (df.rating_count >= t)).sum())} for t in [3, 50, 100, 500]])
    thresholds.to_csv(out / 'threshold_sensitivity.csv', index=False)
    ranking = df.sort_values(['rating', 'rating_count'], ascending=[False, False]).reset_index(drop=True)
    ranking.insert(0, 'rank', range(1, len(ranking)+1))
    ranking.to_csv(out / 'alternative_ranking.csv', index=False)
    filtered = df[(df.rating >= median) & (df.rating_count >= 100)]
    filtered.to_csv(out / 'filtered_shortlist.csv', index=False)
    plt.figure(figsize=(7, 4)); plt.hist(df.rating, bins=[3.5, 4.0, 4.5, 5.0], edgecolor='white'); plt.xlabel('Vivino rating'); plt.ylabel('Number of wines'); plt.title(f'Distribution of Vivino ratings (n={len(df)})'); plt.tight_layout(); plt.savefig(out / 'rating_histogram.png', dpi=180); plt.close()
    sorted_df = df.sort_values('rating_count')
    plt.figure(figsize=(9, 4)); plt.barh(sorted_df.name, sorted_df.rating_count); plt.xlabel('Number of ratings'); plt.title('Review counts by wine'); plt.tight_layout(); plt.savefig(out / 'review_counts.png', dpi=180); plt.close()
    print(stats.to_string(index=False)); print('\nThreshold sensitivity:\n', thresholds.to_string(index=False)); print('\nShortlist:\n', filtered[['name', 'rating', 'rating_count']].to_string(index=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='data/Vivino-export.xlsx', type=Path)
    parser.add_argument('--output', default='outputs', type=Path)
    args = parser.parse_args()
    analyze(load_data(args.input), args.output)
