from fastapi import FastAPI, HTTPException
from typing import Optional
from src.models import Expense, ExpenseCreate
from src.storage import load_expenses, save_expenses, get_next_id

app = FastAPI(title="Smart Expense Tracker API")


@app.post("/expenses", response_model=Expense)
def add_expense(expense: ExpenseCreate):
    """Add a new expense."""
    expenses = load_expenses()
    new_expense = Expense(id=get_next_id(expenses), **expense.model_dump())
    expenses.append(new_expense)
    save_expenses(expenses)
    return new_expense


@app.get("/expenses", response_model=list[Expense])
def get_expenses(category: Optional[str] = None):
    """View all expenses, optionally filtered by category."""
    expenses = load_expenses()
    if category:
        expenses = [e for e in expenses if e.category.lower() == category.lower()]
    return expenses


@app.get("/expenses/total")
def get_total(category: Optional[str] = None):
    """Calculate total expenses, overall or by category."""
    expenses = load_expenses()
    if category:
        expenses = [e for e in expenses if e.category.lower() == category.lower()]
    total = sum(e.amount for e in expenses)
    return {"category": category, "total": round(total, 2)} if category else {"total": round(total, 2)}


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    """Delete an expense by id."""
    expenses = load_expenses()
    remaining = [e for e in expenses if e.id != expense_id]
    if len(remaining) == len(expenses):
        raise HTTPException(status_code=404, detail=f"Expense with id {expense_id} not found")
    save_expenses(remaining)
    return {"message": f"Expense {expense_id} deleted"}