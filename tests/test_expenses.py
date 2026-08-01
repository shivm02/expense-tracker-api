import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.storage import DATA_FILE
import json


@pytest.fixture(autouse=True)
def reset_data():
    """Reset the JSON file to empty before every test, so tests don't interfere with each other."""
    with open(DATA_FILE, "w") as f:
        json.dump([], f)
    yield


client = TestClient(app)


def test_add_expense():
    response = client.post("/expenses", json={
        "title": "Groceries",
        "amount": 45.5,
        "category": "Food",
        "date": "2026-08-01"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Groceries"
    assert data["amount"] == 45.5


def test_get_all_expenses():
    client.post("/expenses", json={"title": "Coffee", "amount": 5, "category": "Food", "date": "2026-08-01"})
    client.post("/expenses", json={"title": "Bus", "amount": 20, "category": "Transport", "date": "2026-08-01"})

    response = client.get("/expenses")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_filter_by_category():
    client.post("/expenses", json={"title": "Coffee", "amount": 5, "category": "Food", "date": "2026-08-01"})
    client.post("/expenses", json={"title": "Bus", "amount": 20, "category": "Transport", "date": "2026-08-01"})

    response = client.get("/expenses?category=Food")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Coffee"


def test_total_expenses():
    client.post("/expenses", json={"title": "Coffee", "amount": 5, "category": "Food", "date": "2026-08-01"})
    client.post("/expenses", json={"title": "Bus", "amount": 20, "category": "Transport", "date": "2026-08-01"})

    response = client.get("/expenses/total")
    assert response.status_code == 200
    assert response.json()["total"] == 25.0


def test_total_by_category():
    client.post("/expenses", json={"title": "Coffee", "amount": 5, "category": "Food", "date": "2026-08-01"})
    client.post("/expenses", json={"title": "Bus", "amount": 20, "category": "Transport", "date": "2026-08-01"})

    response = client.get("/expenses/total?category=Food")
    assert response.status_code == 200
    assert response.json()["total"] == 5.0


def test_total_with_no_expenses():
    response = client.get("/expenses/total")
    assert response.status_code == 200
    assert response.json()["total"] == 0.0


def test_delete_expense():
    add_response = client.post("/expenses", json={"title": "Coffee", "amount": 5, "category": "Food", "date": "2026-08-01"})
    expense_id = add_response.json()["id"]

    delete_response = client.delete(f"/expenses/{expense_id}")
    assert delete_response.status_code == 200

    get_response = client.get("/expenses")
    assert len(get_response.json()) == 0


def test_delete_nonexistent_expense():
    response = client.delete("/expenses/9999")
    assert response.status_code == 404