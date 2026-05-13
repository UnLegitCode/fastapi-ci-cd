import json
import os
import redis

from fastapi import FastAPI, BackgroundTasks

from app.models import Task
from app.tasks import send_notification

tasks_db = [
    {
        "id": 1,
        "title": "Task 1",
        "description": "First task"
    },
    {
        "id": 2,
        "title": "Task 2",
        "description": "Second task"
    }
]

CACHE_KEY = "tasks_cache"

app = FastAPI()
redis_client = redis.Redis(host='python_pro_redis', port=6379, db=0, decode_responses=True, password=os.getenv("REDIS_PASSWORD"))

@app.get("/tasks")
def get_tasks():
    cached_tasks = redis_client.get(CACHE_KEY)

    if cached_tasks:
        return json.loads(cached_tasks)

    redis_client.set(CACHE_KEY, json.dumps(tasks_db), ex=60)

    return tasks_db

@app.post("/tasks")
def create_task(task: Task, background_tasks: BackgroundTasks):
    tasks_db.append(task.dict())

    redis_client.delete(CACHE_KEY)

    background_tasks.add_taskaaa(send_notification, task.id, task.title)

    return {
        "message": "Task created",
        "task": task
    }