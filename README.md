# Transaction Categorizer

A simple Python tool to read bank transactions from a CSV file and automatically categorize them based on rules defined in a JSON file.

## Features
- **CSV Parsing**: Loads bank statements from `transactions.csv`.
- **Rule Engine**: Matches transactions using keywords defined in `rules.json`.
- **Interactive Rule Addition**: If a transaction is uncategorized, the program prompts you to enter a category and keyword, then automatically saves it for future runs.

## How to Run
1. Make sure you have Python 3.9+ installed.
2. Run the application:
   ```bash
   python3 main.py
    ```

## Configuration Files
- `transactions.csv`: Input file containing your bank statements.
- `rules.json`: Key-value pairs mapping partner keywords to categories.

