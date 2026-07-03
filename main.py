import csv
from dataclasses import dataclass, field
from datetime import date, datetime
import json

@dataclass
class Transaction:
    id: int
    date: date
    partner: str
    amount: int
    currency: str
    category: str = "Uncategorized"

    @classmethod
    def from_csv_row(cls, row: dict[str, str]):
        """Creates Transaction object from a CSV row dictionary."""
        try:
            return cls(
                id=int(row['id']),
                date=datetime.fromisoformat(row['date']).date(),
                partner=row['partner'],
                amount=int(row['amount']),
                currency=row['currency']
            )
        except (ValueError, KeyError) as e:
            print(f"Skipping invalid row {row}: {e}")
            return None

class RuleEngine:
    def __init__(self, rules: dict[str, str]):
        self.rules = rules

    def categorize(self, transaction: Transaction) -> str:
        """Return the category for a transaction based on rules."""
        for keyword, category in self.rules.items():
            if keyword.lower() in transaction.partner.lower():
                return category
        return transaction.category


def load_transactions(filename: str) -> list[Transaction]:
    """Loads transactions from a CSV file."""
    transactions = []
    try:
        with open(filename, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                transaction = Transaction.from_csv_row(row)
                if transaction:
                    transactions.append(transaction)
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
    return transactions

def load_rules_from_json(filename: str) -> dict[str,str]:
    """Loads categorization rules from a JSON file."""
    try:
        with open(filename, mode="r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Rules file '{filename}' not found. Using empty rules.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{filename}' Check for syntax errors.")
        return {}

def main():
    """Main function to run the transaction categorizer."""

    rules = load_rules_from_json('rules.json')
    transactions = load_transactions('transactions.csv')
    engine = RuleEngine(rules)

    for t in transactions:
        t.category = engine.categorize(t)
        print(f"Partner: {t.partner:<35} | Kategória: {t.category}")

if __name__ == "__main__":
    main()
