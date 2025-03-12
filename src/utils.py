import pandas as pd


def get_last_day_of_month(month):
    """Get the last day of a month"""
    date_obj = pd.to_datetime(month, format="%b %Y")
    return pd.Period(date_obj, freq="M").end_time.strftime("%d/%m/%Y")


def save_entries_to_csv(df, output_file):
    """Save DataFrame to CSV"""
    df.to_csv(output_file, index=False)
    print(f"Accounting entries saved to {output_file}")
