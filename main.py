import csv
from dataclasses import dataclass, field
from datetime import date, datetime

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

def main():
    """Main function to run the transaction categorizer."""
    rules = {
        # Bevételek
        "Fizetes": "Bevetel",
        "OTP Bank Kamat": "Bevetel",

        # Élelmiszer
        "SPAR": "Elelmiszer",
        "Lidl": "Elelmiszer",
        "Tesco": "Elelmiszer",
        "Auchan": "Elelmiszer",
        "ALDI": "Elelmiszer",

        # Utazás és közlekedés
        "MOL": "Utazas",
        "OMV": "Utazas",
        "Shell": "Utazas",
        "MÁV": "Kozlekedes",
        "Budapesti Kozlekedesi Kozpont": "Kozlekedes",
        "BKK Automata": "Kozlekedes",

        # Számlák és rezsi
        "E.ON": "Szamlak",
        "MVM": "Szamlak",
        "Digi": "Szamlak",
        "Telekom": "Szamlak",

        # Szórakozás és előfizetések
        "Netflix": "Szorakozas",
        "Spotify": "Szorakozas",
        "HBO": "Szorakozas",
        "Cinema City": "Szorakozas",
        "Libri": "Kultura",

        # Étterem és ételrendelés
        "Wolt": "Etterem",
        "Foodora": "Etterem",
        "Netpincer": "Etterem",
        "McDonalds": "Etterem",
        "KFC": "Etterem",
        "Burger King": "Etterem",
        "Starbucks": "Kavezo",

        # Drogéria és egészség
        "Rossmann": "Drogeria",
        "DM": "Drogeria",
        "Gyogyszertar": "Egeszseg",

        # Ruházkodás
        "H&M": "Ruhazkodas",
        "Zara": "Ruhazkodas",
        "Pull&Bear": "Ruhazkodas",

        # Sport és szabadidő
        "Decathlon": "Sport",

        # Lakberendezés és barkács
        "Praktiker": "Barkacs",
        "IKEA": "Lakberendezes",
        "Obi": "Barkacs",
    }

    transactions = load_transactions('transactions.csv')
    engine = RuleEngine(rules)

    for t in transactions:
        t.category = engine.categorize(t)
        print(f"Partner: {t.partner:<35} | Kategória: {t.category}")

if __name__ == "__main__":
    main()
