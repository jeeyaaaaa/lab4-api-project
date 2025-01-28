from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from the environment
API_KEY = os.getenv("LAB4_API_KEY")

# Initialize the FastAPI app
app = FastAPI()

# Task model
class Task(BaseModel):
    task_id: int
    task_title: str
    task_desc: Optional[str] = ""
    is_finished: bool = False

# Mock database
task_db = [
    {"task_id": 1, "task_title": "Laboratory Activity", "task_desc": "Create Lab Act 2", "is_finished": False}
]

# Root route for testing deployment
@app.get("/")
def read_root():
    return {"message": "Welcome to the Task API!"}

# --- Version 1 (apiv1) ---
@app.get("/apiv1/tasks/{task_id}")
def read_task_v1(task_id: int):
    task = next((task for task in task_db if task["task_id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    return {"status": "ok", "task": task}

@app.post("/apiv1/tasks", status_code=status.HTTP_201_CREATED)
def create_task_v1(task: Task):
    if any(t['task_id'] == task.task_id for t in task_db):
        raise HTTPException(status_code=400, detail="Task ID already exists.")
    task_db.append(task.dict())
    return {"status": "ok", "task": task}

@app.patch("/apiv1/tasks/{task_id}")
def update_task_v1(task_id: int, task: Task):
    existing_task = next((t for t in task_db if t["task_id"] == task_id), None)
    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    
    if task.task_title:
        existing_task['task_title'] = task.task_title
    if task.task_desc is not None:
        existing_task['task_desc'] = task.task_desc
    if task.is_finished is not None:
        existing_task['is_finished'] = task.is_finished

    return {"status": "ok", "task": existing_task}

@app.delete("/apiv1/tasks/{task_id}", status_code=status.HTTP_200_OK)
def delete_task_v1(task_id: int):
    global task_db
    task = next((t for t in task_db if t["task_id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    
    task_db = [t for t in task_db if t["task_id"] != task_id]
    return {"status": "ok", "message": "Task deleted successfully."}

# --- Version 2 (apiv2) ---
@app.get("/apiv2/tasks/{task_id}")
def read_task_v2(task_id: int):
    task = next((task for task in task_db if task["task_id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    return {"status": "ok", "task": task}

@app.post("/apiv2/tasks", status_code=status.HTTP_201_CREATED)
def create_task_v2(task: Task):
    if any(t['task_id'] == task.task_id for t in task_db):
        raise HTTPException(status_code=400, detail="Task ID already exists.")
    task_db.append(task.dict())
    return {"status": "ok", "task": task}

@app.patch("/apiv2/tasks/{task_id}")
def update_task_v2(task_id: int, task: Task):
    existing_task = next((t for t in task_db if t["task_id"] == task_id), None)
    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    
    if task.task_title:
        existing_task['task_title'] = task.task_title
    if task.task_desc is not None:
        existing_task['task_desc'] = task.task_desc
    if task.is_finished is not None:
        existing_task['is_finished'] = task.is_finished

    return {"status": "ok", "task": existing_task}

@app.delete("/apiv2/tasks/{task_id}", status_code=status.HTTP_200_OK)
def delete_task_v2(task_id: int):
    global task_db
    task = next((t for t in task_db if t["task_id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    
    task_db = [t for t in task_db if t["task_id"] != task_id]
    return {"status": "ok", "message": "Task deleted successfully."}

# Route to retrieve all tasks
@app.get("/apiv1/tasks")
@app.get("/apiv2/tasks")
def get_tasks():
    if not task_db:
        return Response(content="No tasks found.", status_code=status.HTTP_204_NO_CONTENT)
    return {"status": "ok", "tasks": task_db}
