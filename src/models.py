from pydantic import BaseModel, Field
from datetime import date


class Expense(BaseModel):
    id: int
    title: str
    amount: float = Field(gt=0, description="Expense amount, must be positive")
    category: str
    date: date


class ExpenseCreate(BaseModel):
    """Used when creating a new expense — no id needed, we'll assign it."""
    title: str
    amount: float = Field(gt=0)
    category: str
    date: date