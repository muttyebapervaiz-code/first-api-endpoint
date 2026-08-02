from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import db
import auth
app = FastAPI()
app.include_router(auth.router)
class Task(BaseModel):
    title: str
    done: bool = False

@app.on_event("startup")
def startup():
    db.setup()

@app.get("/")
def home():
    return {"message": "Hello! Mini backend is alive.", "status": "ok"}

@app.get("/time")
def get_time():
    from datetime import datetime
    return {"current_time": datetime.now().isoformat()}

@app.get("/tasks")
def get_tasks():
    return db.get_all()

@app.post("/tasks", status_code=201)
def create_task(task: Task):
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required")
    return db.create(task.title, task.done)

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = db.get_one(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated: Task):
    task = db.update(task_id, updated.title, updated.done)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    if not db.delete(task_id):
        raise HTTPException(status_code=404, detail="Task not found")