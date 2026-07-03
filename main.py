import csv


class Transaction:
    def __init__(self, id, date, partner, amount, currency):
        self.id = int(id)
        self.date = date
        self.partner = partner
        self.amount = int(amount)
        self.currency = currency
        self.category = "Uncategorized"


class RuleEngine:
    def __init__(self, rules):
        self.rules = rules

    def categorize(self, transaction):
        for k in self.rules:
            if k in transaction.partner:
                transaction.category = rules[k]


rules = {
    "SPAR": "Elelmiszer",
    "Lidl": "Elelmiszer",
    "MOL": "Utazas",
    "Netflix": "Szorakozas"
}

transactions = []

with open('transactions.csv', mode = "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        transactions.append(Transaction(row['id'], row['date'], row['partner'], row['amount'], row['currency']))

engine = RuleEngine(rules)

for t in transactions:
    engine.categorize(t)
    print(f"{t.partner} - {t.category}")