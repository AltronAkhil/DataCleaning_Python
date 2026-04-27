import pandas as pd


def load_dataset(filepath):

    na_values = [
        '', ' ', 'NA', 'N/A',
        'null', 'None', 'Nan',
        'Unknown', 'Not Available'
    ]

    if filepath.endswith('.csv'):

        df = pd.read_csv(
            filepath,
            na_values=na_values
        )

    elif filepath.endswith('.xlsx') or filepath.endswith('.xls'):

        df = pd.read_excel(
            filepath,
            na_values=na_values
        )

    else:
        raise ValueError('Unsupported file type')

    return df