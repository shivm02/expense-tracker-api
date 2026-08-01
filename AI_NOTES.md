## Step 1 — Project structure
Asked AI for the initial folder layout (src/, tests/, data/) and the
dependency list in requirements.txt (fastapi, uvicorn, pytest, httpx).
Used as-is — this is a standard FastAPI project layout, nothing to
validate or change.
## Step 2 — models.py
AI-generated: the Pydantic model structure (Expense + ExpenseCreate split).
Validated: understood why two separate models are used (id is server-assigned, not client-provided) — kept as is, this is standard FastAPI practice.
## Step 3 — storage.py
AI-generated: JSON file read/write functions and id-generation logic.
Validated: checked that get_next_id() handles the empty-list case
(returns 1) and doesn't reuse ids after a delete.
## Step 4 — main.py + debugging the JSON BOM issue
AI-generated: all 4 endpoint functions in main.py (POST /expenses,
GET /expenses, GET /expenses/total, DELETE /expenses/{id}).
Bug encountered: POST requests failed with 500 errors due to a
JSONDecodeError. Root cause: PowerShell's file redirection added a
UTF-8 BOM (byte-order mark) to expenses.json, which Python's
json.load() couldn't parse even though the file visually looked
like valid JSON ([]). Diagnosed by inspecting raw file bytes with
Python, found the BOM (\xef\xbb\xbf) prefix, fixed by rewriting the
file in binary mode. Caught by reading the actual traceback, not
just the code.
Validated: manually tested all 4 endpoints via Swagger UI —
add, list, filter by category, total (overall + by category),
confirmed category filter is case-insensitive as intended.