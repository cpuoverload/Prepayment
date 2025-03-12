import pandas as pd
from pandas import DataFrame


def get_last_day_of_month(month: str) -> str:
    """Get the last day of a month

    Args:
        month: Month in format 'MMM YYYY' (e.g. 'Apr 2024')

    Returns:
        Last day of the month in format 'DD/MM/YYYY'
    """
    date_obj = pd.to_datetime(month, format="%b %Y")
    return pd.Period(date_obj, freq="M").end_time.strftime("%d/%m/%Y")


def save_entries_to_csv(df: DataFrame, output_file: str) -> None:
    """Save DataFrame to CSV

    Args:
        df: DataFrame containing accounting entries
        output_file: Path to output CSV file
    """
    df.to_csv(output_file, index=False)
    print(f"Accounting entries saved to {output_file}")
