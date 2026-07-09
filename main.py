from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello! Mini backend is alive.", "status": "ok"}

@app.get("/time")
def get_time():
    return {"current_time": datetime.now().isoformat()}