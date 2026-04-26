import pandas as pd


def generate_kpis(df):

    missing_values = (
        df.replace(r'^\s*$', pd.NA, regex=True)
        .isnull()
        .sum()
        .sum()
    )

    numeric_cols = len(df.select_dtypes(include=['number']).columns)

    categorical_cols = len(df.select_dtypes(include=['object']).columns)

    date_cols = len(df.select_dtypes(include=['datetime']).columns)

    return {
        'rows': len(df),
        'columns': len(df.columns),
        'missing_values': int(missing_values),
        'duplicates': int(df.duplicated().sum()),
        'numeric_columns': numeric_cols,
        'categorical_columns': categorical_cols,
        'date_columns': date_cols
    }