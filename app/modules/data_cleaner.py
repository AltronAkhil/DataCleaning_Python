import pandas as pd
import numpy as np


def clean_data(df):

    df = df.copy()

    # Remove unnamed columns
    df = df.loc[:, ~df.columns.astype(str).str.contains('^unnamed', case=False)]

    # Standardize column names
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(' ', '_')
        .str.replace('-', '_')
    )

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Convert blank strings to NaN
    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)

    # Detect object columns
    object_cols = df.select_dtypes(include='object').columns

    # Clean text columns
    for col in object_cols:

        df[col] = df[col].astype(str).str.strip()

        df[col] = df[col].replace(
            [
                'unknown',
                'not available',
                'null',
                'na',
                'n/a',
                'none'
            ],
            np.nan
        )

    # Drop rows mostly empty
    threshold = int(len(df.columns) * 0.6)
    df.dropna(thresh=threshold, inplace=True)

    # Dynamically detect numeric columns
    for col in df.columns:

        numeric_version = pd.to_numeric(df[col], errors='coerce')

        numeric_ratio = numeric_version.notna().mean()

        if numeric_ratio > 0.7:
            df[col] = numeric_version

    # Dynamically detect date columns
    for col in df.columns:

        if 'date' in col or 'time' in col:

            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
            except:
                pass

    # Fill missing values dynamically
    for col in df.columns:

        if pd.api.types.is_numeric_dtype(df[col]):

            df[col] = df[col].fillna(df[col].median())

        elif pd.api.types.is_datetime64_any_dtype(df[col]):

            df[col] = df[col].fillna(method='ffill')

        else:

            mode_value = (
                df[col].mode()[0]
                if not df[col].mode().empty
                else 'Unknown'
            )

            df[col] = df[col].fillna(mode_value)

    return df.reset_index(drop=True)