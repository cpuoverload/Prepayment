from datetime import datetime
import sys
from models import PrepaymentManager
from utils import save_entries_to_csv
import config


def main():
    month = input("Please input the month (e.g. Apr 2024): ")
    try:
        datetime.strptime(month, "%b %Y")
    except ValueError:
        print(
            "❌ Invalid format! Please enter the month in 'MMM YYYY' format, e.g., 'Apr 2024'."
        )
        sys.exit(1)

    manager = PrepaymentManager(config.DATA_FILE)
    manager.load_data()
    df_entries = manager.generate_entries_for_month(month)
    save_entries_to_csv(df_entries, config.OUTPUT_FILE)


if __name__ == "__main__":
    main()
