from typing import Dict, List
import pandas as pd
import datetime
import config
from utils import get_last_day_of_month


class Prepayment:
    """Represents a prepayment item, such as Webhosting"""

    def __init__(
        self,
        item_name: str,
        invoice_number: str,
        invoice_amount: float,
        amortization_schedule: Dict[str, float],
    ) -> None:
        self.item_name = item_name
        self.invoice_number = invoice_number
        self.invoice_amount = invoice_amount
        self.amortization_schedule = amortization_schedule

    def generate_entries(self, month: str) -> List[Dict[str, str | float]]:
        """Generate accounting entries for a specific month"""
        amount = self.amortization_schedule.get(month, 0)
        if amount == 0:
            return []

        return [
            {
                "Date": get_last_day_of_month(month),
                "Description": f"Prepayment amortisation for {self.item_name}",
                "Reference": self.invoice_number,
                "Account": config.ACCOUNT_CODES["EXPENSE"],
                "Amount": abs(amount),
            },
            {
                "Date": get_last_day_of_month(month),
                "Description": f"Prepayment amortisation for {self.item_name}",
                "Reference": self.invoice_number,
                "Account": config.ACCOUNT_CODES["PREPAYMENT"],
                "Amount": -abs(amount),
            },
        ]


class PrepaymentManager:
    """Manages multiple prepayment items"""

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.prepayments: List[Prepayment] = []

    def load_data(self) -> None:
        """Load data from Excel/CSV and create Prepayment objects"""
        df = pd.read_excel(self.filepath, skiprows=2)  # skip first two rows
        df = df[df["Items"].notna()]  # remove rows where "Items" is NaN

        # select the date columns
        date_columns = [col for col in df.columns if isinstance(col, datetime.datetime)]

        # convert datetime to str (e.g. Jan 2024)
        df.rename(
            columns={col: col.strftime("%b %Y") for col in date_columns},
            inplace=True,
        )

        # update the date columns to be strings
        date_columns = [col.strftime("%b %Y") for col in date_columns]

        for _, row in df.iterrows():
            schedule = (
                row[date_columns].dropna().to_dict()
            )  # pick the date columns and drop NaN values

            self.prepayments.append(
                Prepayment(
                    row["Items"], row["Invoice number"], row["Invoice amount"], schedule
                )
            )

    def generate_entries_for_month(self, month: str) -> pd.DataFrame:
        """Generate accounting entries for a specific month for all prepayment items"""
        entries = []
        for prepayment in self.prepayments:
            entries.extend(prepayment.generate_entries(month))
        return pd.DataFrame(entries)
