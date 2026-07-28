from fastapi import FastAPI, HTTPException
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import sqlite3

app = FastAPI()

class Task(BaseModel):
    title: str
    done: bool = False

tasks = []
next_id = 1

conn = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        done BOOLEAN NOT NULL DEFAULT 0
    )
""")
conn.commit()

cursor.execute("SELECT COUNT(*) FROM tasks")
count = cursor.fetchone()[0]

if count == 0:
    cursor.execute("INSERT INTO tasks (title, done) VALUES ('Buy milk', 0)")
    cursor.execute("INSERT INTO tasks (title, done) VALUES ('Walk the dog', 0)")
    cursor.execute("INSERT INTO tasks (title, done) VALUES ('Read a book', 1)")
    conn.commit()

@app.get("/")
def home():
    return {"message": "Hello! Mini backend is alive.", "status": "ok"}

@app.get("/time")
def get_time():
    return {"current_time": datetime.now().isoformat()}

@app.get("/tasks")
def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append({"id": row[0], "title": row[1], "done": bool(row[2])})
    return result

@app.post("/tasks", status_code=201)
def create_task(task: Task):
    cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (task.title, task.done))
    conn.commit()
    new_id = cursor.lastrowid
    return {"id": new_id, "title": task.title, "done": task.done}
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    if row:
        return {"id": row[0], "title": row[1], "done": bool(row[2])}
    raise HTTPException(status_code=404, detail="Task not found")
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Task not found")
    cursor.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (updated_task.title, updated_task.done, task_id)
    )
    conn.commit()
    return {"id": task_id, "title": updated_task.title, "done": updated_task.done}

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Task not found")
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    return