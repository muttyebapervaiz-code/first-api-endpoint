# First API Endpoint — Task Manager (FastAPI + SQLite)

A simple CRUD (Create, Read, Update, Delete) REST API for managing tasks, built with **FastAPI** and backed by a **SQLite** database. This project started as an in-memory task API and was upgraded to persist data using SQLite, so tasks survive server restarts.

Built as part of the FlyRank Backend AI Engineering Internship — Week 3, Assignment A2: *Connecting your CRUD to the database*.

## Why SQLite?

SQLite was chosen for this project because:

* **Single file** — the entire database lives in one file (`tasks.db`), no separate database server to install or run.
* **Zero setup** — Python's `sqlite3` module is built into the standard library, so there is nothing extra to install.
* **Persistence** — unlike the original in-memory version, data written to SQLite survives a server restart, because it's saved to disk instead of living only in a Python variable.

For a small project like this, SQLite gives real persistence without the overhead of setting up a full database server (like PostgreSQL or MySQL).

## Database file

The database file is `tasks.db`. It is created automatically the first time the app runs — if the file doesn't exist yet, `sqlite3.connect("tasks.db")` creates it, and the `tasks` table is created if missing.

`tasks.db` is **git-ignored** (see `.gitignore`), so every fresh clone of this repo starts with a clean database. On first run, three example tasks are seeded automatically (only if the table is empty).

## How to run this project

```bash
# 1. Clone the repo
git clone https://github.com/muttyebapervaiz-code/first-api-endpoint.git
cd first-api-endpoint

# 2. Create and activate a virtual environment
python -m venv venv
venv\\Scripts\\activate      # Windows
# source venv/bin/activate # macOS/Linux

# 3. Install dependencies
pip install fastapi uvicorn

# 4. Run the server
uvicorn main:app --reload
```

Once running, open **http://127.0.0.1:8000/docs** to try out all endpoints via the interactive Swagger UI. `tasks.db` will be created automatically in the project folder, seeded with three example tasks.

## API Endpoints

|Method|Endpoint|Description|
|-|-|-|
|GET|`/tasks`|List all tasks|
|GET|`/tasks/{task\_id}`|Get a single task by id|
|POST|`/tasks`|Create a new task|
|PUT|`/tasks/{task\_id}`|Update an existing task|
|DELETE|`/tasks/{task\_id}`|Delete a task|

All endpoints use **parameterized SQL queries** (`?` placeholders) — user input is never glued directly into a SQL string, which protects against SQL injection.

## Exploring the database by hand (Stage 4)

I opened `tasks.db` in **DB Browser for SQLite** and ran several queries directly against the database, outside of the API, to see how the API and the database file share the exact same source of truth.

**Query run:**

```sql
UPDATE tasks SET done = 1;
```

**What it returned:** This query had no `WHERE` clause, so it updated **every single row** in the table, marking all tasks as done — not just one. This was a deliberate exercise, and it taught me how dangerous it is to forget a `WHERE` clause in an `UPDATE` or `DELETE` statement, since it's easy to accidentally overwrite or delete an entire table.

*(Screenshot of DB Browser for SQLite showing the `tasks` table — add screenshot here, e.g. `!\[DB Browser screenshot](screenshots/db-browser.png)`)*

## Project structure

```
first-api-endpoint/
├── main.py          # FastAPI app with all CRUD endpoints
├── tasks.db          # SQLite database (auto-created, git-ignored)
├── .gitignore
└── README.md
```

## Tech stack

* Python 3
* FastAPI
* SQLite (via Python's built-in `sqlite3` module)
* Uvicorn (ASGI server)
* DB Browser for SQLite (for manual database inspection)



**## Stage 0 — Postgres in Docker**



Start database:

docker run --name taskdb -e POSTGRES\_PASSWORD=dev -e POSTGRES\_DB=tasks -p 5432:5432 -v taskdata:/var/lib/postgresql/data -d postgres:16

