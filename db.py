import psycopg
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg.connect(DATABASE_URL)

def setup():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    done BOOLEAN NOT NULL DEFAULT FALSE
                )
            """)
            cur.execute("SELECT COUNT(*) FROM tasks")
            if cur.fetchone()[0] == 0:
                cur.execute("INSERT INTO tasks (title, done) VALUES (%s, %s)", ("Buy milk", False))
                cur.execute("INSERT INTO tasks (title, done) VALUES (%s, %s)", ("Walk the dog", False))
                cur.execute("INSERT INTO tasks (title, done) VALUES (%s, %s)", ("Read a book", True))

def get_all():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks")
            return [{"id": r[0], "title": r[1], "done": r[2]} for r in cur.fetchall()]

def get_one(task_id):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
            r = cur.fetchone()
            return {"id": r[0], "title": r[1], "done": r[2]} if r else None

def create(title, done):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING *", (title, done))
            r = cur.fetchone()
            return {"id": r[0], "title": r[1], "done": r[2]}

def update(task_id, title, done):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING *", (title, done, task_id))
            r = cur.fetchone()
            return {"id": r[0], "title": r[1], "done": r[2]} if r else None

def delete(task_id):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tasks WHERE id = %s RETURNING id", (task_id,))
            return cur.fetchone() is not None