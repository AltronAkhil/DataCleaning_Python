import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import pandas as pd
import os


def generate_charts(df):

    chart_paths = []

    charts_folder = os.path.join(
        'app',
        'static',
        'charts'
    )

    os.makedirs(charts_folder, exist_ok=True)

    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

    chart_index = 0

    # -----------------------------
    # Histogram Charts
    # -----------------------------

    for col in numeric_cols[:3]:

        try:

            fig, ax = plt.subplots(figsize=(8, 5))

            df[col].dropna().plot(
                kind='hist',
                bins=20,
                ax=ax
            )

            ax.set_title(f'Distribution - {col}')

            filename = f'chart_{chart_index}.png'

            save_path = os.path.join(
                charts_folder,
                filename
            )

            fig.savefig(save_path)
            plt.close(fig)

            chart_paths.append(f'static/charts/{filename}')

            chart_index += 1

        except Exception as e:
            print(f"Histogram error: {e}")

    # -----------------------------
    # Bar Charts
    # -----------------------------

    for col in categorical_cols[:2]:

        try:

            counts = df[col].value_counts().head(10)

            if len(counts) > 0:

                fig, ax = plt.subplots(figsize=(8, 5))

                counts.plot(
                    kind='bar',
                    ax=ax
                )

                ax.set_title(f'{col} Categories')

                filename = f'chart_{chart_index}.png'

                save_path = os.path.join(
                    charts_folder,
                    filename
                )

                fig.savefig(save_path)
                plt.close(fig)

                chart_paths.append(f'static/charts/{filename}')

                chart_index += 1

        except Exception as e:
            print(f"Bar chart error: {e}")

    # -----------------------------
    # Scatter Plot
    # -----------------------------

    if len(numeric_cols) >= 2:

        try:

            fig, ax = plt.subplots(figsize=(8, 5))

            ax.scatter(
                df[numeric_cols[0]],
                df[numeric_cols[1]]
            )

            ax.set_xlabel(numeric_cols[0])
            ax.set_ylabel(numeric_cols[1])

            filename = f'chart_{chart_index}.png'

            save_path = os.path.join(
                charts_folder,
                filename
            )

            fig.savefig(save_path)
            plt.close(fig)

            chart_paths.append(f'static/charts/{filename}')

            chart_index += 1

        except Exception as e:
            print(f"Scatter error: {e}")

    # -----------------------------
    # Missing Value Chart
    # -----------------------------

    try:

        missing_counts = df.isnull().sum()

        missing_counts = missing_counts[missing_counts > 0]

        if len(missing_counts) > 0:

            fig, ax = plt.subplots(figsize=(10, 5))

            missing_counts.sort_values(
                ascending=False
            ).plot(
                kind='bar',
                ax=ax
            )

            ax.set_title('Missing Values by Column')

            filename = f'chart_{chart_index}.png'

            save_path = os.path.join(
                charts_folder,
                filename
            )

            fig.savefig(save_path)
            plt.close(fig)

            chart_paths.append(f'static/charts/{filename}')

    except Exception as e:
        print(f"Missing chart error: {e}")

    return chart_paths
