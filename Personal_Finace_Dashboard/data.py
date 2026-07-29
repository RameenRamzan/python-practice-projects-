# data.py
import json
import os
import pandas as pd

CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))


def load_category_rules():
    """
    Load categorization rules from categories.json (personal, gitignored).
    Falls back to categories.example.json if the personal file doesn't exist,
    so the app still runs out of the box for anyone who clones the repo.
    """
    personal_path = os.path.join(CONFIG_DIR, "categories.json")
    example_path = os.path.join(CONFIG_DIR, "categories.example.json")
    path = personal_path if os.path.exists(personal_path) else example_path

    with open(path, "r") as f:
        return json.load(f)


def load_data(filepath):
    rules = load_category_rules()
    exact_matches = rules.get("exact_matches", {})
    fee_keywords = rules.get("fee_keywords", [])

    df = pd.read_csv(filepath, skiprows=4)

    df['Booking Date'] = pd.to_datetime(df['Booking Date'])
    df['Value Date'] = pd.to_datetime(df['Value Date'])
    df['Amount'] = df['Credit'].fillna(0) - df['Debit'].fillna(0)

    def categorize(row):
        desc = row['Description'].lower()

        for keyword, category in exact_matches.items():
            if keyword.lower() in desc:
                return category

        if any(keyword in desc for keyword in fee_keywords):
            return "Bank Charges"
        elif row['Credit'] > 0:
            return "Other Income"
        else:
            return "Other / Personal Transfer"

    df['Category'] = df.apply(categorize, axis=1)
    df['Month'] = df['Booking Date'].dt.to_period('M')

    assert df['Category'].isna().sum() == 0, "Some rows have no category!"

    return df