from modules.kpi_generator import generate_kpis
from modules.chart_generator import generate_charts
from modules.data_cleaner import clean_data
from modules.dataset_quality import calculate_quality_score

import os


def analyze_data(df, original_filename=None):

    # Raw KPIs
    raw_kpis = generate_kpis(df.copy())

    # Clean dataset
    cleaned_df = clean_data(df)

    # Cleaned KPIs
    cleaned_kpis = generate_kpis(cleaned_df)

    # Quality Score
    quality = calculate_quality_score(cleaned_df)

    # Generate Charts
    charts = generate_charts(cleaned_df)

    # -----------------------------
    # Save Cleaned File
    # -----------------------------

    cleaned_folder = 'cleaned_data'
    os.makedirs(cleaned_folder, exist_ok=True)

    cleaned_file_path = None

    if original_filename:

        filename_without_ext = os.path.splitext(original_filename)[0]

        cleaned_file_path = os.path.join(
            cleaned_folder,
            f'{filename_without_ext}_cleaned'
        )

        # Save same format
        if original_filename.endswith('.csv'):

            cleaned_file_path += '.csv'

            cleaned_df.to_csv(
                cleaned_file_path,
                index=False
            )

        elif original_filename.endswith(('.xlsx', '.xls')):

            cleaned_file_path += '.xlsx'

            cleaned_df.to_excel(
                cleaned_file_path,
                index=False
            )

    return {

        'raw_kpis': raw_kpis,
        'cleaned_kpis': cleaned_kpis,
        'quality': quality,
        'charts': charts,
        'cleaned_file': os.path.basename(cleaned_file_path)
    }