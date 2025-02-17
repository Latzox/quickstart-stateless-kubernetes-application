from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="To-Do Service")

class TodoItem(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

todos_db = []

@app.post("/todos/", response_model=TodoItem)
def create_todo(todo: TodoItem):
    todos_db.append(todo)
    return todo

@app.get("/todos/")
def get_todos():
    return todos_db
