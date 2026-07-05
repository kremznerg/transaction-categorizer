# Transaction Categorizer - TODO

## Phase 1: Console CLI Application
- [x] Create `transactions.csv` sample file
- [x] Create `rules.json` file for rules
- [x] Create GitHub repository
- [x] Create class to store transactions (`Transaction`)
    - `from_csv_row` classmethod: receives CSV row as dictionary and stores key-value pairs into transaction object attributes
- [x] Create class to load rules and categorize transactions (`RuleEngine`)
    - `__init__`: receives rules as a dictionary
    - `categorize`: categorizes a transaction object based on partner name
- [x] Load and store rules into dictionary (`load_rules_from_json`)
- [x] Read `transactions.csv`, store as `Transaction` objects and save to a list (`load_transactions`)
- [x] Interactive rule handling in CLI: prompts for category if unrecognized and saves it
    - Load existing rules and transactions
    - Loop through transactions
    - If a transaction category remains "Uncategorized", prompt the user
    - Add and save the new rule, update the transaction category and print the result
- [x] Statistics: monthly aggregation by category and display on screen
- [x] Database integration: store data in SQLite database (`transactions.db`)

## Phase 2: FastAPI Web API
- [ ] Build basic app structure (Hello World endpoint `GET /` and run with Uvicorn)
- [ ] Transactions endpoint (`GET /api/transactions`): fetch transactions from SQLite database as JSON
- [ ] Rules endpoint (`GET /api/rules`): fetch rules from the database
- [ ] Add rule endpoint (`POST /api/rules`): save a new category rule to the database
- [ ] Manual transaction categorization (`PUT /api/transactions/{id}`): modify a specific transaction's category in the DB
- [ ] Monthly statistics endpoint (`GET /api/statistics/monthly`): return monthly category-wise statistics as JSON