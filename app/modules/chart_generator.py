import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import pandas as pd
import os
import missingno as msno


def generate_charts(df):

    chart_paths = []

    os.makedirs('static/charts', exist_ok=True)

    numeric_cols = [
        col for col in df.select_dtypes(include=['number']).columns
        if 'unnamed' not in col.lower()
    ]

    categorical_cols = [
        col for col in df.select_dtypes(include=['object']).columns
        if 'unnamed' not in col.lower()
    ]

    chart_index = 0

    # Histogram for first 3 numeric columns
    for col in numeric_cols[:3]:

        plt.figure(figsize=(8, 5))
        df[col].dropna().hist(bins=20)
        plt.title(f'Distribution - {col}')

        filename = f'static/charts/chart_{chart_index}.png'
        plt.savefig(filename)
        plt.close()

        chart_paths.append(filename)
        chart_index += 1

    # Bar charts for first 2 categorical columns
    for col in categorical_cols[:2]:

        value_counts = df[col].value_counts().head(10)

        if len(value_counts) > 0:

            plt.figure(figsize=(8, 5))
            value_counts.plot(kind='bar')
            plt.title(f'Category Distribution - {col}')

            filename = f'static/charts/chart_{chart_index}.png'
            plt.savefig(filename)
            plt.close()

            chart_paths.append(filename)
            chart_index += 1

    # Scatter Plot
    if len(numeric_cols) >= 2:

        plt.figure(figsize=(8, 5))

        plt.scatter(
            df[numeric_cols[0]],
            df[numeric_cols[1]]
        )

        plt.xlabel(numeric_cols[0])
        plt.ylabel(numeric_cols[1])
        plt.title('Scatter Plot')

        filename = f'static/charts/chart_{chart_index}.png'
        plt.savefig(filename)
        plt.close()

        chart_paths.append(filename)
        chart_index += 1

    # Correlation Heatmap
    if len(numeric_cols) >= 2:

        corr = df[numeric_cols].corr()

        plt.figure(figsize=(10, 6))
        plt.imshow(corr, interpolation='nearest', cmap='coolwarm')
        plt.colorbar()

        plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
        plt.yticks(range(len(corr.columns)), corr.columns)

        plt.title('Correlation Heatmap')

        filename = f'static/charts/chart_{chart_index}.png'
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()

        chart_paths.append(filename)
        chart_index += 1

    # Missing Values Map
    plt.figure(figsize=(10, 5))
    msno.matrix(df)

    filename = f'static/charts/chart_{chart_index}.png'
    plt.savefig(filename)
    plt.close()

    chart_paths.append(filename)

    return chart_paths