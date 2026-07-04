import csv
from dataclasses import dataclass, field
from datetime import date, datetime
import json
import sqlite3

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


def prompt_for_new_rule(partner: str) -> tuple[str, str]:
    """Prompts user for a matching keyword and category."""
    print(f"Unknown partner: {partner}.")
    new_partner = input(f"Enter matching keyword (default: {partner}): ") or partner
    new_category = ""
    while not new_category.strip():
        new_category = input("Please enter the category: ")
    return new_partner, new_category

def init_db():
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rules (
                keyword TEXT PRIMARY KEY,
                category TEXT NOT NULL
            )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                date TEXT NOT NULL,
                partner TEXT NOT NULL,
                currency TEXT NOT NULL,
                amount INTEGER NOT NULL,
                category TEXT NOT NULL DEFAULT 'Uncategorized'

            )
    """)
    conn.commit()
    cursor.close()
    conn.close()


def seed_db(conn):
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM rules")
    rules_count = cursor.fetchone()[0]

    rules = load_rules_from_json("rules.json")
    for kw, cat in rules.items():
        cursor.execute("INSERT OR IGNORE INTO rules (keyword, category) VALUES (?, ?)", (kw, cat))
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM transactions")
    transactions_count = cursor.fetchone()[0]

    transactions = load_transactions("transactions.csv")
    for t in transactions:
        cursor.execute("INSERT OR IGNORE INTO transactions (id, date, partner, currency, amount, category) VALUES (?, ?, ?, ?, ?, ?)",
        (t.id, t.date.isoformat(), t.partner, t.currency, t.amount, t.category)
    )
    conn.commit()
    cursor.close()
 

def main():
    """Main function to run the transaction categorizer."""
    init_db()
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()
    seed_db(conn)

    cursor.execute("SELECT keyword, category FROM rules")
    rows = cursor.fetchall()

    rules = {}
    for row in rows:
        rules[row[0]] = row[1]

    cursor.execute("SELECT id, date, partner, currency, amount, category FROM transactions")
    rows = cursor.fetchall()
    transactions = []
    for row in rows:
        t = Transaction(
            id=row[0],
            date=date.fromisoformat(row[1]),
            partner=row[2],
            currency=row[3],
            amount=row[4],
            category=row[5]
        )
        transactions.append(t)

    engine = RuleEngine(rules)

    for t in transactions:
        db_category = t.category
        t.category = engine.categorize(t)
        if t.category == "Uncategorized":
            new_partner, new_category = prompt_for_new_rule(t.partner)
            rules.update({new_partner: new_category})
            cursor.execute("INSERT OR REPLACE INTO rules (keyword, category) VALUES (?, ?)",
            (new_partner, new_category))
            t.category = new_category
            cursor.execute("UPDATE transactions SET category = ? WHERE id =?", (new_category, t.id))
            conn.commit()
        elif t.category != db_category:
            cursor.execute("UPDATE transactions SET category = ? WHERE id = ?", (t.category, t.id))
            conn.commit()
        print(f"Partner: {t.partner:<35} | Category: {t.category}")
    

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
