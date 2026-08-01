import json
from pathlib import Path
from src.models import Expense

DATA_FILE = Path(__file__).parent.parent / "data" / "expenses.json"


def load_expenses() -> list[Expense]:
    """Read all expenses from the JSON file."""
    if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
        return []
    with open(DATA_FILE, "r") as f:
        raw = json.load(f)
    return [Expense(**item) for item in raw]


def save_expenses(expenses: list[Expense]) -> None:
    """Write all expenses back to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump([e.model_dump(mode="json") for e in expenses], f, indent=2, default=str)


def get_next_id(expenses: list[Expense]) -> int:
    """Generate the next available id."""
    if not expenses:
        return 1
    return max(e.id for e in expenses) + 1