# Transaction Categorizer - TODO

## Phase 1: Console CLI Application
- [x] `transactions.csv` mintafájl létrehozása
- [x] `rules.json` fájl létrehozása a szabályoknak
- [x] GitHub repository létrehozása
- [x] Osztály létrehozása a tranzakciók tárolására (`Transaction`)
    - `from_csv_row` osztálymetódus: CSV sort dictionaryként kap, és elmenti a kulcs-érték párokat a tranzakció objektum adattagjaiba
- [x] Osztály létrehozása a szabályok beolvasására és a tranzakciók kategorizálására (`RuleEngine`)
    - `__init__`: megkapja a szabályokat szótár (dictionary) formában
    - `categorize`: egy tranzakció objektumot kategorizál a partner neve alapján
- [x] Szabályok beolvasása és elmentése szótárba (`load_rules_from_json`)
- [x] `transactions.csv` beolvasása, elmentése `Transaction` objektumokba, és azok listába mentése (`load_transactions`)
- [x] Interaktív szabálykezelés parancssorban: ha nem ismer fel kategóriát, rákérdez és elmenti
    - Beolvassuk a meglévő szabályokat és tranzakciókat
    - Végigmegyünk a tranzakciókon
    - Ha egy tranzakció kategóriája "Uncategorized" marad, bekérjük a felhasználótól
    - Hozzáadjuk és elmentjük az új szabályt, majd frissítjük a tranzakció kategóriáját és kiírjuk az eredményt
- [x] Statisztikák: havi szinten kategóriánkénti összesítés és kiírás
- [x] Adatbázis használat: adatok tárolása SQLite adatbázisban (`transactions.db`)

## Phase 2: FastAPI Web API
- [ ] Alapszerkezet felépítése (Hello World endpoint `GET /` és futtatás uvicorn-nal)
- [ ] Tranzakciók végpont (`GET /api/transactions`): tranzakciók lekérése az SQLite adatbázisból JSON formátumban
- [ ] Szabályok végpont (`GET /api/rules`): szabályok lekérése az adatbázisból
- [ ] Új szabály hozzáadása végpont (`POST /api/rules`): új kategória szabály mentése az adatbázisba
- [ ] Tranzakció kategorizálása manuálisan (`PUT /api/transactions/{id}`): konkrét tranzakció kategóriájának módosítása a DB-ben
- [ ] Havi statisztika végpont (`GET /api/statistics/monthly`): a havi kategóriánkénti statisztikák visszaadása JSON-ként