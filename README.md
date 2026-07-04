# Transaction Categorizer

A simple Python tool to read bank transactions from a CSV file, automatically categorize them based on rules, and store everything in a local SQLite database.

## Features
- **SQLite Database**: Stores both transactions and categorization rules in a local `transactions.db` file.
- **Auto-Initialization & Sync**: On startup, it automatically creates the database schema and incrementally imports any new transactions from `transactions.csv` or rules from `rules.json`.
- **Rule Engine**: Automatically categorizes transactions based on keyword matching.
- **Interactive Rule Addition**: When an unknown transaction is encountered, the program prompts you to enter a keyword and category, saving them directly to the database for future runs.

## How to Run
1. Make sure you have Python 3.9+ installed.
2. Run the application:
   ```bash
   python3 main.py
   ```

## Files
- `transactions.csv`: Input CSV file containing new bank statements to import.
- `rules.json`: JSON file containing initial categorization rules to seed the database.
- `transactions.db`: Local SQLite database file (automatically generated and ignored by Git).
