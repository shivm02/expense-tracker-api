# Smart Expense Tracker API

A REST API to manage personal expenses, built with FastAPI and JSON file storage.

## Features

- Add an expense (title, amount, category, date)
- View all expenses
- Filter expenses by category
- Calculate total expenses (overall and by category)
- Delete an expense

## Tech Stack

- Python 3.11+
- FastAPI
- Uvicorn (ASGI server)
- Pydantic (data validation)
- Pytest (testing)

## Installation

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/shivm02/expense-tracker-api.git
cd expense-tracker-api
python -m venv venv
```

Activate the virtual environment:

```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
uvicorn src.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

Interactive API docs (Swagger UI): `http://127.0.0.1:8000/docs`

## Running Tests

```bash
pytest tests/ -v
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/expenses` | Add a new expense |
| GET | `/expenses` | Get all expenses |
| GET | `/expenses?category={category}` | Filter expenses by category |
| GET | `/expenses/total` | Get overall total |
| GET | `/expenses/total?category={category}` | Get total for a category |
| DELETE | `/expenses/{id}` | Delete an expense by id |

### Example: Add an expense

```bash
curl -X POST "http://127.0.0.1:8000/expenses" \
  -H "Content-Type: application/json" \
  -d '{"title": "Groceries", "amount": 45.5, "category": "Food", "date": "2026-08-01"}'
```

## Project Structure

```
expense-tracker-api/
  README.md
  AI_NOTES.md
  requirements.txt
  src/
    main.py       # API endpoints
    models.py     # Pydantic data models
    storage.py    # JSON file read/write logic
  tests/
    test_expenses.py
  data/
    expenses.json # Data storage
```

## Data Storage

Expenses are stored in `data/expenses.json`. No database setup is required.