import numpy as np


def calculate_quality_score(df):

    total_cells = df.shape[0] * df.shape[1]

    missing_values = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()
    empty_columns = df.columns[df.isnull().all()].shape[0]

    numeric_df = df.select_dtypes(include=['number'])

    outliers = 0

    for col in numeric_df.columns:

        q1 = numeric_df[col].quantile(0.25)
        q3 = numeric_df[col].quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers += ((numeric_df[col] < lower) | (numeric_df[col] > upper)).sum()

    penalty = (
        (missing_values / total_cells) * 30 +
        (duplicate_rows / len(df)) * 25 +
        (empty_columns / len(df.columns)) * 20 +
        (outliers / total_cells) * 25
    )

    quality_score = max(0, round(100 - penalty))

    return {
        'quality_score': quality_score,
        'missing_values': int(missing_values),
        'duplicate_rows': int(duplicate_rows),
        'empty_columns': int(empty_columns),
        'outliers': int(outliers)
    }